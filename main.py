from uvicorn.main import run

from watch_n_learn import create_server

def main(local: bool) -> None:

    run(create_server(local), host="127.0.0.1" if local else "0.0.0.0")

if __name__ == "__main__":
    main(True)
