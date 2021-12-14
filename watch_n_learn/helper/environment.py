from os import getenv

FASTAPI_LOGIN_TOKEN_VALUE = getenv("FASTAPI_LOGIN_TOKEN")

SESSION_MIDDLEWARE_TOKEN_NAME = getenv("SESSION_MIDDLEWARE_TOKEN")

WATCH_N_LEARN_PEPPER = getenv("WATCH_N_LEARN_PEPPER")

for variable in [
    FASTAPI_LOGIN_TOKEN_VALUE, SESSION_MIDDLEWARE_TOKEN_NAME,
    WATCH_N_LEARN_PEPPER
]:
    if variable is None:
        print(f"{variable} is not set")
