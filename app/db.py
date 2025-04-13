from blacksheep import Application
from piccolo.engine import engine_finder
from utils.db_check import check_database
from utils.logging import get_logger

logger = get_logger(__name__)


def configure_db(app: Application):
    async def open_database_connection_pool(application: Application):
        try:
            engine = engine_finder()
            if engine is None:
                raise Exception("No engine found")
            await engine.start_connection_pool()
            logger.info(
                f"postgresql version: {await engine.get_version()}, "
                "The database connection pool is opened and then the database check is run."
            )
            await check_database(engine)
        except Exception:
            logger.error("Unable to connect to the database")

    async def close_database_connection_pool(application: Application):
        try:
            engine = engine_finder()
            if engine is None:
                raise Exception("No engine found")
            await engine.close_connection_pool()
        except Exception:
            logger.error("Unable to close the database connection pool")

    app.on_start += open_database_connection_pool
    app.on_stop += close_database_connection_pool
