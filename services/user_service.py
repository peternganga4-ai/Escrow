"""BridgeEscrow - user CRUD operations"""


import core.database as db
import core.models as models
import core.config as config
from .ledger import add_ledger_entry

