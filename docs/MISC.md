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

Check that API endpoint `/v1/auth/users/register/` works by running:

```bash
curl --header "Content-Type: application/json" -X POST http://127.0.0.1:8000/v1/auth/users/register/ --data '{"primary_email": "test2@test.com", "password": "test"}'
```

Result:

```bash
{"full_name":null,"primary_email":"test2@test.com"}
```

Check that API endpoints like `/v1/data/test/` are protected if a token isn't
passed, and that they deliver results if a token is passed:

```bash
curl --header "Content-Type: application/json" -X GET http://127.0.0.1:8000/v1/data/test/
```

Result:

```bash
{"detail":"Authentication credentials were not provided."}
```

With credentials:

```bash
# {"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU4NTg0NDYwNi$ianRpIjoiZGIxNjRhZDc0OGUzNDMzNDk1MGNmZGE5NmM3ZTYwOWMiLCJ1c2VyX2lkIjoxfQ.-AVJLNtakQGFdVFgewqedHO5n69l4DZ$q-6RTasmbeU","access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg0NjM1MzA2LCJqdGkiOiIzNmYxZTc3Y2QzNWM0ZjE5OWNjYjk3MTY2ZTYxNWE5NSIsInVzZXJfaWQiOjF9.dFQ4iY_WfxmAlotHs94B4XIjR-Kkgm0e2GBKklaCXPs"}
curl --header "Content-Type: application/json" -X POST http://127.0.0.1:8000/v1/auth/tokens/obtain/ --data '{"primary_email": "test@test.com", "password": "test"}'

curl --header "Content-Type: application/json" --header "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg0NjM1MzA2LCJqdGkiOiIzNmYxZTc3Y2QzNWM0ZjE5OWNjYjk3MTY2ZTYxNWE5NSIsInVzZXJfaWQiOjF9.dFQ4iY_WfxmAlotHs94B4XIjR-Kkgm0e2GBKklaCXPs" -X GET http://127.0.0.1:8000/v1/data/test/
```

Result:

```bash
{"hello":"world"}
```

Test that blacklisting a JWT token via API endpoint `/v1/auth/tokens/blacklist` works:

```bash
$ curl --header "Content-Type: application/json" -X POST http://127.0.0.1:8000/v1/auth/tokens/obtain/ --data '{"primary_email": "test@test.com", "password": "test"}'
{"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU4NTg0NTQ3OSwianRpIjoiMGRiZDBiZjc2ZjliNGQxMTlkNzUyYjkxMGU4ODI0NDgiLCJ1c2VyX2lkIjoxfQ.DPhGBKUsVvCAGbLXLrEPp3DJM5vkZ1vho2psIuZCWs4","access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg0NjM2MTc5LCJqdGkiOiI2OGU0YjAzMjE5ODc0OGVkYjAwMGJlMDcyYjVmNzhhNCIsInVzZXJfaWQiOjF9._xa4b1jnESwvInfkxVqE-XPtXvAIiFCr6ThoC8FPCLU"}(tinydevcrm-api) yingw787@yingw787-ThinkPad-P1-Gen-2:~/sr

$ curl --header "Content-Type: application/json" -X POST http://127.0.0.1:8000/v1/auth/tokens/blacklist/ --data '{"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU4NTg0NTQ3OSwianRpIjoiMGRiZDBiZjc2ZjliNGQxMTlkNzUyYjkxMGU4ODI0NDgiLCJ1c2VyX2lkIjoxfQ.DPhGBKUsVvCAGbLXLrEPp3DJM5vkZ1vho2psIuZCWs4"}'

$ curl --header "Content-Type: application/json" -X POST http://127.0.0.1:8000/v1/auth/tokens/refresh/ --data '{"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU4NTg0NTQ3OSwianRpIjoiMGRiZDBiZjc2ZjliNGQxMTlkNzUyYjkxMGU4ODI0NDgiLCJ1c2VyX2lkIjoxfQ.DPhGBKUsVvCAGbLXLrEPp3DJM5vkZ1vho2psIuZCWs4"}'
```

Result:

```bash
{"detail":"Token is blacklisted","code":"token_not_valid"}
```

## Deployment snippets
