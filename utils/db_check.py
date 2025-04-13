import subprocess
from piccolo.engine import Engine
from utils.logging import get_logger
from app.settings import BASE_DIR

logger = get_logger(__name__)


async def check_uuidv7(engine: Engine):
    """
    Check if the uuidv7 function is valid and the pg_uuidv7 extension is installed.
    """
    try:
        uuid_v7_func_exist = await engine.run_ddl(
            "SELECT proname FROM pg_proc P JOIN pg_namespace n ON P.pronamespace = n.OID "
            "WHERE n.nspname = 'public' AND P.proname = 'uuid_generate_v7';"
        )

        if uuid_v7_func_exist:
            logger.info("uuid_generate_v7 is valid, pass")
        else:
            logger.warning("uuid_generate_v7 is not valid")
            # 检查是否存在 pg_uuidv7 扩展
            logger.info("check pg_uuidv7 extension")
            uuidv7_extension_exist = await engine.run_ddl(
                "SELECT * FROM pg_available_extensions WHERE name = 'pg_uuidv7';"
            )
            if uuidv7_extension_exist:
                logger.info("pg_uuidv7 extension is valid, then install it")
                await engine.run_ddl('CREATE EXTENSION IF NOT EXISTS "pg_uuidv7";')
            else:
                logger.warning(
                    "pg_uuidv7 extension is not valid, and then install function version"
                )
                await engine.run_ddl(
                    BASE_DIR.joinpath(
                        "resource/sql", "create_uuidv7_function.sql"
                    ).read_text()
                )
                logger.info("uuidv7 function is installed")
    except AttributeError:
        logger.warning(
            "The uuid_generate_v7 function is not supported by this database engine."
        )

    except Exception as e:
        logger.error(f"Error checking uuidv7: {e}")


async def run_migration():
    """
    Check if the migration is valid and the pg_uuidv7 extension is installed.
    """
    subprocess.run(
        ["piccolo", "migrations", "forwards", "all"], stdout=subprocess.DEVNULL
    )
    logger.info("Migration is completed, please check the migration status.")
    subprocess.run(
        ["piccolo", "migrations", "check"],
        check=True,
    )


async def check_database(engine: Engine):
    await check_uuidv7(engine)
    await run_migration()
