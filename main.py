#main.py is the entry point for the application
#It initializes global logging and executes the CLI

from pathlib import Path
from app.cli import run as run_cli
import logging
import sys


#Create the logs directory (if it doesn't already exist)
Path("logs").mkdir(parents=True, exist_ok=True)

#Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("logs/graph-admin-cli.log"),
        logging.StreamHandler()
    ]
)

# Initialize logger for main entry point
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Graph Admin CLI application starting...")

    try:
        run_cli()
        logger.info("Graph Admin CLI application completed successfully.")

    except Exception as e:
        logger.critical(f"Unhandled application crash: {e}", exc_info=True)
        sys.exit(1)
