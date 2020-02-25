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

## 1. `psql` connections to AWS RDS instances time out

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

When I attempt to connect to the RDS instance using a default configuration for
test / free tier instances, I get this error:

```bash
$ psql -h database-1.cxkynbxqwzwy.us-east-1.rds.amazonaws.com

psql: could not connect to server: Connection timed out

Is the server running on host "database-1.cxkynbxqwzwy.us-east-1.rds.amazonaws.com" (172.31.32.234) and accepting TCP/IP connections on port 5432?

$
```

### Solution

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
