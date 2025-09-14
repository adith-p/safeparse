from pathlib import Path

# Base directory of your project
BASE_DIR = Path(__file__).resolve().parent

# Database files
IDENTIFIER_DB = BASE_DIR / "../data/identifier.sqlite"
VAULT_DB = BASE_DIR / "../data/vault.db"
EVENT_LOG = BASE_DIR / "../data/event.log"