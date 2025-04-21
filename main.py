from utils.setup import initialize

import typer

app = typer.Typer()

## command to setup the app for the first time.
@app.command()
def setup():
    initialize()

## command to reset the app and initialize again.
@app.command()
def reset():
    pass

## command to run the command line bot.
@app.command()
def cli():
    pass


if __name__ == "__main__":
    app()
