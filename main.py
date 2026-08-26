import logging
from pathlib import Path
from app.cli import run as run_cli

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

if __name__ == "__main__":
    run_cli()