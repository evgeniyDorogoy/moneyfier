import click

from moneyfier_api.api_v1 import app
from bots.telegram_bots import main


def run_server():
    app.run(host="0.0.0.0", port=5000)


def run_bot():
    main()


@click.command()
@click.option('-b', '--runbot', is_flag=True, help="Run Telegram bot")
@click.option('-s', '--runserver', is_flag=True, help="Run application server")
def execute(runserver, runbot):
    if runserver:
        run_server()
    elif runbot:
        run_bot()


if __name__ == '__main__':
    execute()
