living document of stuff

## API reference

Create a user with superuser privileges:

```bash
docker-compose -f services/docker-compose.development.yaml exec web python manage.py createsuperuser
```

Create the superuser with email `'test@test.com'` and password `'test'`.

Check that API endpoint `/v1/auth/tokens/obtain/` works by running:

```bash
curl --header "Content-Type: application/json" -X POST http://127.0.0.1:8000/v1/auth/tokens/obtain/ --data '{"primary_email": "test@test.com", "password": "test"}'
```

Result:

```bash
{"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU4NTg0MzAxMCwianRpIjoiYzljMDU2MTA3OTU5NGFmZmE2MWU4YmUxOTlkNjQyMTQiLCJ1c2VyX2lkIjoxfQ.o5Kc_5R_KOItWFD0Wt4p30ph3NrvkmWG2MbZA3MI3kU","access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg0NjMzNzEwLCJqdGkiOiJlYjVjNzE4MzEwYjQ0ZmY4OWUxOTg5Mzg4YTI4NjBmMyIsInVzZXJfaWQiOjF9.1vjAyd7o-tZudvYtunOUsSawKpWsvUCcUADFbnTi0i8"}
```

check that API endpoint `/v1/auth/tokens/refresh/` works by running:

```bash
curl --header "Content-Type: application/json" -X POST http://127.0.0.1:8000/v1/auth/tokens/refresh/ --data '{"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU4NTg0MzAxMCwianRpIjoiYzljMDU2MTA3OTU5NGFmZmE2MWU4YmUxOTlkNjQyMTQiLCJ1c2VyX2lkIjoxfQ.o5Kc_5R_KOItWFD0Wt4p30ph3NrvkmWG2MbZA3MI3kU"}'
```

Result:

```bash
{"access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg0NjM0NTkwLCJqdGkiOiIxYjM5ZmY5OGRmYWU0NTcxYTcxYWMwZTA1MWRiNDcxMCIsInVzZXJfaWQiOjF9.xRN7_m4ER8FF4d9K1Y8lVFDX97q9bj6P3sh8uokWLZ8","refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU4NTg0Mzg5MCwianRpIjoiYTYxYWUxMzY0ZjMzNGFmZTlmOTJjODJlODY5MGEwNDgiLCJ1c2VyX2lkIjoxfQ.yWlFr21KXQIGpd8zD9yLzZ5hAya5NP-eCdCXli6dWic"}
```

## Deployment snippets
