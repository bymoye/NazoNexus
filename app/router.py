from blacksheep import Application
from blacksheep.utils.meta import import_child_modules
from app.settings import BASE_DIR
from utils.logging import get_logger

logger = get_logger(__name__)


def configure_router(app: Application) -> None:
    """
    Configure the router for the application.
    """

    folders = [
        folder
        for folder in BASE_DIR.iterdir()
        if folder.is_dir()
        and not folder.name.startswith("_")
        and (folder / "__init__.py").exists()
        and (folder / "endpoints").exists()
    ]
    for folder in folders:
        folder_name = folder.name
        endpoints_module = folder / "endpoints"
        if endpoints_module.exists():
            import_child_modules(endpoints_module)
            logger.info(f"Imported {folder_name}.endpoints")
