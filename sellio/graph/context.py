from sellio.graph import TGraphContext
from sellio.services.db import main_db


def get_graph_context(ec_context: dict | None = None) -> TGraphContext:
    return {
        "db.session_async": main_db,
        **(ec_context or {}),
    }
