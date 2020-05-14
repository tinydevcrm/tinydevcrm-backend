# Flight rules

## What are flight rules?

A guide for core developers and core maintainers of `tinydevcrm-dashboard` about
what to do when things go wrong.

>   *Flight rules* are the hard-earned body of knowledge recorded in manuals
>   that list, step-by-step, what to do if X occurs, and why. Essentially, they
>   are extremely detailed, scenario-specific standard operating procedures.
>
>   NASA has been capturing our missteps, disasters, and solutions since the
>   early 1960s, when Mercury-era ground teams first started gathering "lessons
>   learned" into a compendium that now lists thousands of problematic
>   situations, from engine failure to busted hatch handles to computer
>   glitches, and their solutions.

-- Chris Hadfield, *An Astronaut's Guide to Life*.

## `psql` connections to AWS RDS instances time out

### Problem

When I attempt to connect to the RDS instance using a default configuration for
test / free tier instances, I get this error:

```bash
$ psql -h database-1.cxkynbxqwzwy.us-east-1.rds.amazonaws.com

psql: could not connect to server: Connection timed out

Is the server running on host "database-1.cxkynbxqwzwy.us-east-1.rds.amazonaws.com" (172.31.32.234) and accepting TCP/IP connections on port 5432?

$
```

### Solution

1. Set public accessibility for the RDS instance to "on" to grant the database a
   public IP address.

2. Add an inbound rule to the VPC security group for "all traffic" and my IP
   address (ideally VPN server IP address).

__________

Using the [AWS RDS
documentation](https://aws.amazon.com/premiumsupport/knowledge-center/rds-cannot-connect/)
on why a local client cannot connect to the RDS instance, I used `nslookup` in
order to lookup whether the instance has a resolved server address:

```bash
$ nslookup database-1.cxkynbxqwzwy.us-east-1.rds.amazonaws.com
Server:         127.0.0.53
Address:        127.0.0.53#53

Non-authoritative answer:
Name:   database-1.cxkynbxqwzwy.us-east-1.rds.amazonaws.com
Address: 172.31.32.234
```

Using the [AWS RDS tutorial
documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToPostgreSQLInstance.html),
the following advice is given about usual errors:

> Troubleshooting Connection Issues
>
> If you can't connect to the DB instance, the most common error is Could not
> connect to server: Connection timed out. If you receive this error, do the
> following:
>
> - Check that the host name used is the DB instance endpoint and that the port
>   number used is correct.
>
> - **Make sure that the DB instance's public accessibility is set to Yes.**
>
> - Check that the security group assigned to the DB instance has rules to allow
>   access through any firewall your connection might go through. For example,
>   if the DB instance was created using the default port of 5432, your company
>   might have firewall rules blocking connections to that port from company
>   devices.
>
>   To fix this failure, modify the DB instance to use a different port. Also,
>   make sure that the security group applied to the DB instance allows
>   connections to the new port.
>
> Check whether the DB instance was created using a security group that doesn't
> authorize connections from the device or Amazon EC2 instance where the
> application is running. For the connection to work, the security group you
> assigned to the DB instance at its creation must allow access to the DB
> instance. For example, if the DB instance was created in a VPC, it must have a
> VPC security group that authorizes connections.
>
> You can add or edit an inbound rule in the security group. For Source, choose
> My IP. This allows access to the DB instance from the IP address detected in
> your browser. For more information, see Amazon Virtual Private Cloud VPCs and
> Amazon RDS.
>
> Alternatively, if the DB instance was created outside of a VPC, it must have a
> database security group that authorizes those connections.
>
> By far the most common connection problem is with the security group's access
> rules assigned to the DB instance. If you used the default DB security group
> when you created the DB instance, the security group likely didn't have access
> rules that allow you to access the instance. For more information about Amazon
> RDS security groups, see Controlling Access with Security Groups.
>
> If you receive an error like `FATAL: database some-name does not exist when
> connecting`, try using the default database name postgres for the --dbname
> option.

By default, public accessibility to the RDS instance is turned off, and access
is only granted to EC2 instances registered with the VPC security group. This
may increase the importance of separating out concerns and catering ops towards
using AWS Elastic Beanstalk or even AWS Amplify for simplicity (which would
detract from the goal of making a single deployable from anywhere).

After modifying the RDS instance to enable public accessibility, `psql` from
local client continues to fail. I need to add an inbound rule to the security
group. To do this:

1.  Go to the [AWS RDS home console](https://console.aws.amazon.com/rds/home).

2.  Click on "DB Instances" link.

3.  In the "Databases" window, select the appropriate database resource (e.g.
    `database-1` by database identifier).

4.  In the "$DATABASE" window, in the "Connectivity & Security" tab, click on
    the appropriate VPC security group in the top right of the card, which
    should take you to the "Resource Groups" window in the AWS Elastic Compute
    Cloud (EC2) window.

5.  Click on the "Actions" button (next to the blue "Create Security Group"
    window) and in the menu dropdown, click on "Edit Inbound Rules". Click on
    "Add Rule", select "All Traffic", and for the "Source" selection, hit "My
    IP". I'm connecting via my VPN server, which should have a fixed IP address.

6.  Attempt to re-connect, using command:

    ```bash
    $ psql \
        --host=database-1.cxkynbxqwzwy.us-east-1.rds.amazonaws.com \
        --port=5432 \
        --username=postgres \
        --password \
        --dbname=postgres
    Password:
    psql (11.7 (Ubuntu 11.7-2.pgdg19.10+1), server 11.5)
    SSL connection (protocol: TLSv1.2, cipher: ECDHE-RSA-AES256-GCM-SHA384, bits: 256, compression: off)
    Type "help" for help.

    postgres=>
    ```

    I was able to successfully connect to the RDS instance in `psql` using this
    method.

## Use `pg_cron` with AWS RDS

### Problem

I deployed a PostgreSQL instance on Amazon Web Services (AWS) Relational
Database Service (RDS) with the intention to test whether extension `pg_cron`
could be created, and whether it was indeed supported by AWS, as per [this blog
post](https://www.alibabacloud.com/help/doc-detail/150355.htm) by Alibaba Cloud
discussing `pg_cron` configuration on AWS RDS last updated on February 24th of
this year (2020). Using `pg_cron` is imperative to TinyDevCRM as it enables
automated event generation, and precludes a need to consider a hybrid cloud
approach (Citus Cloud supports `pg_cron`, but since Citus Data was acquired by
Microsoft, it is only available via Azure).

### Solution

As of this writing (February 25th, 2020), I confirmed that AWS RDS does not
support extension `pg_cron`. I checked this via `psql` query `SHOW
rds.extensions;`

```bash
postgres=> CREATE EXTENSION pg_cron;
ERROR:  Extension "pg_cron" is not supported by Amazon RDS
DETAIL:  Installing the extension "pg_cron" failed, because it is not on the list of extensions supported by Amazon RDS.
HINT:  Amazon RDS allows users with rds_superuser role to install supported extensions. See: SHOW rds.extensions;
postgres=>
```

This is the full list of RDS extensions supported by AWS RDS PostgreSQL:

```bash
address_standardizer, address_standardizer_data_us, amcheck, aws_commons, aws_s3, bloom, btree_gin, btree_gist, citext, cube, dblink, dict_int, dict_xsyn, earthdistance, fuzzystrmatch, hll, hstore, hstore_plperl, intagg, intarray, ip4r, isn, jsonb_plperl, log_fdw, ltree, orafce, pageinspect, pgaudit, pgcrypto, pglogical, pgrouting, pgrowlocks, pgstattuple, pgtap, pg_buffercache, pg_freespacemap, pg_hint_plan, pg_prewarm, pg_repack, pg_similarity, pg_stat_statements, pg_transport, pg_trgm, pg_visibility, plcoffee, plls, plperl, plpgsql, plprofiler, pltcl, plv8, postgis, postgis_tiger_geocoder, postgis_topology, postgres_fdw, prefix, sslinfo, tablefunc, test_parser, tsm_system_rows, tsm_system_time, unaccent, uuid-ossp
```

## Delete a superuser from Django

### Problem

After switching to Django from Flask, and committing to implementing a JSON Web
Token authentication scheme, I'm implementing a custom user in order to work
around the templated Django authentication scheme according [to the Django
documentation](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project).
However, after mistakenly creating a superuser, deleting a superuser is not so
straightforward. [This Stack Overflow
post](https://stackoverflow.com/a/26713562/1497211) works fine for deleting an
ordinary Django user, but it will fail for a custom user:

```bash
$ python manage.py shell
Python 3.8.1 (default, Jan  8 2020, 22:29:32)
[GCC 7.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from django.contrib.auth.models import User
>>> User.objects.get(username='$USERNAME', is_superuser=True).delete()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/path/to/manager.py", line 184, in __get__
    raise AttributeError(
AttributeError: Manager isn't available; 'auth.User' has been swapped for 'authentication.CustomUser'
```

### Solution

Instead of referencing `django.contrib.auth.models`, reference `$PROJECT.models`
instead:

```bash
>>> authentication.models.CustomUser
<class 'authentication.models.CustomUser'>
>>> authentication.models.CustomUser.objects
<django.contrib.auth.models.UserManager object at 0x7f9e78dbb0d0>
>>> authentication.models.CustomUser.objects.get(username='$USERNAME', is_superuser=True)
<CustomUser: $USERNAME>
>>> authentication.models.CustomUser.objects.get(username='$USERNAME', is_superuser=True).delete()
(1, {'admin.LogEntry': 0, 'authentication.CustomUser_groups': 0, 'authentication.CustomUser_user_permissions': 0, 'authentication.CustomU
ser': 1})
```

Keep in mind that the `models.py` may not be exposed outside of the package:

```bash
>>> from authentication import CustomUser
Traceback (most recent call last):
  File "<console>", line 1, in <module>
ImportError: cannot import name 'CustomUser' from 'authentication' (/path/to/api.tinydevcrm.com/src/authentication/__init__.py$
>>> import authentication
>>> authentication.CustomUser
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: module 'authentication' has no attribute 'CustomUser'
>>> dir(authentication)
# When I discovered models were namespaced via 'models'
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', 'admin', 'models'$
```

## JSON Web Token does not appear to be verified on https://jwt.io

### Problem

When I entered in my JWT refresh token, a large red validation error message
showed up, saying "Signature unverified". I thought my JWT refresh token was
copied wrong, or the token was incorrectly generated due to a dependency error.

### Solution

The JWT token was successfully decoded, as could be seen in the "Decode" tab
next to the "Encode" tab. To verify a JWT token, you need the correct encryption
algorithm (in this case, HS256 or the default), *as well as the secret key*.
After entering in the secret key (which should only be done for development and
never test or production environments), a blue check appears that says
"Signature Verified".

## Debug a Django REST API call

### Problem

I've favored using `ipdb` to set traces, and using `ipdb` in Flask is trivial;
you can drop it in anywhere within the Python code, and `flask run` will result
in the `ipdb` context being tripped properly. Django is not that simple; adding
a `ipdb` trace to `serializers.py` or `settings.py` or `urls.py` may not work
properly, since the server does appear to pre-process and cache things like
configuration settings before it becomes live.

### Solution

From [this Stack Overflow answer](https://stackoverflow.com/a/1118271/1497211),
you can debug a Django view function by adding a `pdb` trace within a given HTTP
method:

```python
# /path/to/$PROJECT/views.py
class CustomUserCreate(APIView):
    def post(self, request, format='json'):
        import ipdb
        ipdb.set_trace()
        # rest of function
```

Start up the Django server:

```bash
conda activate $CONDA_ENV && python -m ipdb /path/to/manage.py runserver
```

Then, you can submit a given `curl` request:

```bash
curl --header "Content-Type: application/json" -X POST http://127.0.0.1:8000/api/user/create/ --data '{"email": "test2@test.com", "username": "test2", "password": "12345678"}'

# Or:
curl \
  --header "Content-Type: application/json" \
  -X POST \
  --data '{"email": "test2@test.com", "username": "test2", "password": "12345678"}' \
  http://127.0.0.1:8000/api/user/create/
```

This should drop you into a `pdb` context:

```python
System check identified no issues (0 silenced).
March 04, 2020 - 18:18:13
Django version 3.0.3, using settings 'src.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
> /path/to/views.py(22)post()
     21
---> 22         serializer = CustomUserSerializer(data=request.data)
     23         if serializer.is_valid():

ipdb>
```

## Debug an Elastic Beanstalk application deployment issue

### Problem

Looking at `eb health` did not help, since it only gives information regarding
HTTP statuses for each AWS Elastic Beanstalk deployment instance. Looking at the
AWS Elastic Beanstalk GUI console did not help, since the logs were not rich
enough in order to deduce the actual problem. Looking at `eb config` did not
help either because of the numerous deployment settings.

### Solution

Looking at `eb logs` helped resolve this issue. A section of file `/var/log/httpd/error_log` indicated the following:

```text
[Mon Mar 09 21:31:07.670251 2020] [:error] [pid 28463] [remote 172.31.15.94:52] ModuleNotFoundError: No module named 'src.settings'
[Mon Mar 09 21:31:08.883469 2020] [:error] [pid 28463] [remote 172.31.41.113:17464] mod_wsgi (pid=28463): Target WSGI script '/opt/python/current/app/src/src/wsgi.py' cannot be loaded as Python module.
[Mon Mar 09 21:31:08.883518 2020] [:error] [pid 28463] [remote 172.31.41.113:17464] mod_wsgi (pid=28463): Exception occurred processing WSGI script '/opt/python/current/app/src/src/wsgi.py'.
[Mon Mar 09 21:31:08.883660 2020] [:error] [pid 28463] [remote 172.31.41.113:17464] Traceback (most recent call last):
[Mon Mar 09 21:31:08.883706 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]   File "/opt/python/current/app/src/src/wsgi.py", line 16, in <module>
[Mon Mar 09 21:31:08.883710 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]     application = get_wsgi_application()
[Mon Mar 09 21:31:08.883726 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]   File "/opt/python/run/venv/local/lib/python3.6/site-packages/django/core/wsgi.py", line 12, in get_wsgi_application
[Mon Mar 09 21:31:08.883730 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]     django.setup(set_prefix=False)
[Mon Mar 09 21:31:08.883735 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]   File "/opt/python/run/venv/local/lib/python3.6/site-packages/django/__init__.py", line 19, in setup
[Mon Mar 09 21:31:08.883739 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]     configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
[Mon Mar 09 21:31:08.883744 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]   File "/opt/python/run/venv/local/lib/python3.6/site-packages/django/conf/__init__.py", line 76, in __getattr__
[Mon Mar 09 21:31:08.883747 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]     self._setup(name)
[Mon Mar 09 21:31:08.883752 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]   File "/opt/python/run/venv/local/lib/python3.6/site-packages/django/conf/__init__.py", line 63, in _setup
[Mon Mar 09 21:31:08.883755 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]     self._wrapped = Settings(settings_module)
[Mon Mar 09 21:31:08.883760 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]   File "/opt/python/run/venv/local/lib/python3.6/site-packages/django/conf/__init__.py", line 142, in __init__
[Mon Mar 09 21:31:08.883764 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]     mod = importlib.import_module(self.SETTINGS_MODULE)
[Mon Mar 09 21:31:08.883769 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]   File "/opt/python/run/venv/lib64/python3.6/importlib/__init__.py", line 126, in import_module
[Mon Mar 09 21:31:08.883772 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]     return _bootstrap._gcd_import(name[level:], package, level)
[Mon Mar 09 21:31:08.883777 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]   File "<frozen importlib._bootstrap>", line 994, in _gcd_import
[Mon Mar 09 21:31:08.883783 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]   File "<frozen importlib._bootstrap>", line 971, in _find_and_load
[Mon Mar 09 21:31:08.883788 2020] [:error] [pid 28463] [remote 172.31.41.113:17464]   File "<frozen importlib._bootstrap>", line 953, in _find_and_load_unlocked
[Mon Mar 09 21:31:08.883804 2020] [:error] [pid 28463] [remote 172.31.41.113:17464] ModuleNotFoundError: No module named 'src.settings'
[Mon Mar 09 21:31:10.617469 2020] [mpm_prefork:notice] [pid 28458] AH00169: caught SIGTERM, shutting down
```

This led to find [this Stack Overflow
answer](https://stackoverflow.com/a/7887521/1497211) regarding issues around
your Django app name vs. your core folder name. From this information, I changed
`src/src` to `src/core`, and submitted a redeployment.

### `make aws-login` fails with MFA token

#### Problem

This failure assumes an IAM user has been configured for the command line as per
instructions in `SETUP.md` in `tinydevcrm-infra`.

Sometimes, given a long enough session, the MFA token will become invalid, and
ECR logins will fail as a result, instead of `awscli` requesting a new token:

```bash
$ make aws-login
An error occurred (UnrecognizedClientException) when calling the GetAuthorizationToken operation: The sec
urity token included in the request is invalid.
make: *** [Makefile:28: aws-login] Error 255
```

#### Resolution

Re-export `AWS_PROFILE`, and try again:

```bash
$ export AWS_PROFILE=tinydevcrm-user
$ make aws-login
$(aws ecr get-login --no-include-email)
WARNING! Using --password via the CLI is insecure. Use --password-stdin.
WARNING! Your password will be stored unencrypted in /home/yingw787/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
```

### `make publish-app` fails with authentication error

#### Problem

When running `make publish-app` or otherwise pushing Docker images to AWS ECR,
sometimes the process errors out:

This is different from having `awscli` properly configured and having an MFA
token for the AWS IAM user.

```bash
ERROR: compose.cli.main.main: denied: Your authorization token has expired. Reauthenticate and try again.
```

#### Resolution

AWS ECR requires its own login.

Re-run `make aws-login` and then re-try the push:

```bash
make aws-login
make publish-app
```

This should be templated out in the `Makefile` using dependent targets.

### `make publish-app` fails with tag not found error

#### Problem

Publishing `app`, `db`, and `nginx` Docker images requires the latest commit
tag. If those tagged images don't exist on the local compute instance, then
`docker push` will error out:

```bash
ERROR: compose.cli.main.main: tag does not exist: 267131297086.dkr.ecr.us-east-1.amazonaws.com/tinydevcrm-ecr/app:aafc2c5
```

#### Resolution

Ensure that the `docker build` process is run before every push. This should be
templated out in the `Makefile`.
