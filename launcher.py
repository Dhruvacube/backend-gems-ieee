import sys, asyncio, click, subprocess, importlib, traceback, uvicorn

from vars import BASE_DIR
from .database import Base, Session

try:
    import uvloop  # type: ignore
except ImportError:
    if sys.platform.startswith(("win32", "cygwin")):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    uvloop.install()


@click.group(invoke_without_command=True, options_metavar="[options]")
@click.pass_context
def main(ctx):
    """Lays out the steps on how to launch the api server."""
    if ctx.invoked_subcommand is None:
        # print("In the same bash terminal type out the following command to start the server:")
        # print("uvicorn main:app --host 0.0.0.0 --port 80")
        uvicorn.run("main:app", port=80, log_level="info")

async def create_tables():
    engine = Session.get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    engine = Session.get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@main.group(short_help="database stuff", options_metavar="[options]")
def db():
    pass


@db.command(
    short_help="initialises the databases for the API", options_metavar="[options]"
)
@click.argument("models", nargs=-1, metavar="[models]")
def init(models):
    """This manages the migrations and database creation system for you."""
    run = asyncio.get_event_loop().run_until_complete
    if not models:
        models = [
            f"database.models.{e}" for e in filter(lambda a: False if (a.lower() == "__init__.py" or a.lower() == "__init__") else Trie,(BASE_DIR / "database/models").walk(on_error=print)[3]) # type:ignore
        ]
    else:
        models = [
            f"database.models.{e.lower()}"
            for e in models
        ]
    for ext in models:
        try:
            importlib.import_module(ext)
        except Exception:
            click.echo(f"Could not load {ext}.\n{traceback.format_exc()}", err=True)
            return
    run(create_tables())
    click.echo("Tables created in the database.")

@db.command(short_help="removes a model's table", options_metavar="[options]")
@click.argument("models", metavar="<models>", default="all")
def drop(models):
    """This removes a database and all its migrations.

    You must be pretty sure about this before you do it,
    as once you do it there's no coming back.

    Also note that the name must be the model name.
    """
    run = asyncio.get_event_loop().run_until_complete
    click.confirm("Do you really want to do this?", abort=True)
    if models.lower() == "all":
        models = [
            f"database.models.{e}" for e in filter(lambda a: False if (a.lower() == "__init__.py" or a.lower() == "__init__") else Trie,(BASE_DIR / "database/models").walk(on_error=print)[3]) # type:ignore
        ]
    else:
        models = [
            f"database.models.{e.lower()}"
            for e in models
        ]
    for ext in models:
        try:
            importlib.import_module(ext)
        except Exception:
            click.echo(f"Could not load {ext}.\n{traceback.format_exc()}", err=True)
            return
    run(drop_tables())
    click.echo("Tables deleted from the database.")

@db.command(short_help="Create migrations for the databases")
@click.option("--message", prompt=True)
def makemigrations(message):
    """Update the migration file with the newest schema."""
    click.confirm("Do you want to create migrations?", abort=True)
    subprocess.run(  # skipcq: BAN-B607
        ["alembic", "revision", "--autogenerate", "-m", message],
        check=False,
    )
    click.echo("Created migrations.")

@db.command(short_help="Migrates from an migration revision")
@click.option("--upgrade/--downgrade", default=True)
@click.argument(
    "revision", nargs=1, metavar="[revision]", required=False, default="head"
)
def migrate(upgrade, revision):
    """Runs an upgrade from a migration"""
    if upgrade:
        subprocess.run(  # skipcq: BAN-B607
            ["alembic", "upgrade", revision],
            check=False,
        )
    else:
        subprocess.run(  # skipcq: BAN-B607
            [
                "alembic",
                "downgrade",
                "base" if revision.lower() == "head" else revision,
            ],
            check=False,
        )


if __name__ == "__main__":
    main()
