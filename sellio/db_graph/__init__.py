from hiku.sources.graph import SubGraph

from sellio.db_graph.graph import _GRAPH

company_sg = SubGraph(_GRAPH, "company")
product_sg = SubGraph(_GRAPH, "product")


__all__ = (
    "company_sg",
    "product_sg",
)
