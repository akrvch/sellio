from hiku.sources.graph import SubGraph

from sellio.db_graph.graph import _GRAPH

company_sg = SubGraph(_GRAPH, "company")
product_sg = SubGraph(_GRAPH, "product")
category_sg = SubGraph(_GRAPH, "category")


__all__ = (
    "company_sg",
    "product_sg",
    "category_sg",
)
