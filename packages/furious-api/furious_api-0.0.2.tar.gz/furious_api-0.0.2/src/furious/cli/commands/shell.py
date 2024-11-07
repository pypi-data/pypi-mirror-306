import asyncio
import sys

from asgi_lifespan import LifespanManager

from furious.cli.config import REPLs
from furious.cli.discover import import_app


def embed(repl=REPLs.PT):
    app = import_app()
    match repl:
        case REPLs.PT:
            embed_ptpython(app)
        case REPLs.B:
            embed_bpython(app)
        case REPLs.I:
            embed_ipython(app)
        case _:
            raise Exception(
                f'Unknown Python REPL "{repl}". '
                "Available REPLs are: {REPLs.values()}"
            )


def embed_ptpython(app):
    from ptpython.repl import embed

    async def start():
        async with LifespanManager(app):
            embed_result = await embed(return_asyncio_coroutine=True)
            return embed_result

    sys.exit(asyncio.run(start()))


def embed_bpython(app):
    import bpython

    async def start():
        async with LifespanManager(app):
            embed_result = bpython.embed(return_asyncio_coroutine=True)
            await embed_result

    sys.exit(asyncio.run(start()))


def embed_ipython(app):
    import IPython
    import nest_asyncio

    nest_asyncio.apply()

    async def start():
        async with LifespanManager(app):
            return IPython.embed(colors="Linux")

    sys.exit(asyncio.run(start()))
