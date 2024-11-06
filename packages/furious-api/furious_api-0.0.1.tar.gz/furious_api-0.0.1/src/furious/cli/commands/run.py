import uvicorn

from furious.cli.config import get_config
from furious.cli.discover import get_app_import_string


def run_app(host, port):
    """
    Runs the app in the development mode
    """
    app_import_str = get_app_import_string()
    config = get_config()
    uvicorn.run(
        app_import_str,
        host=host,
        port=port,
        reload=True,
        root_path=config.workdir,
    )
