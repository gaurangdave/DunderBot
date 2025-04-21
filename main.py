from cli.bot import run_bot
from cli.setup import initialize, reset_app

import typer
import os

app = typer.Typer()

## command to setup the app for the first time.
@app.command()
def setup():
    os.system("cls")
    initialize()

## command to reset the app and initialize again.
@app.command()
def reset():
    os.system("cls")
    reset_app()

## command to run the command line bot.
@app.command()
def run():
    os.system("clear")
    run_bot()


if __name__ == "__main__":
    app()
