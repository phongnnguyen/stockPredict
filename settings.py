from dotenv import load_dotenv
from pathlib import Path
import os
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
TOKEN_SLACK = os.getenv("TOKEN_SLACK")
SOURCE_WEB = os.getenv("SOURCE_WEB")
CHANNEL = os.getenv("CHANNEL")
