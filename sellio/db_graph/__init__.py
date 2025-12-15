from hiku.sources.graph import SubGraph

from sellio.db_graph.graph import _GRAPH

company_sg = SubGraph(_GRAPH, "company")
product_sg = SubGraph(_GRAPH, "product")
order_sg = SubGraph(_GRAPH, "order")
delivery_info_sg = SubGraph(_GRAPH, "delivery_info")


__all__ = ("company_sg", "product_sg", "order_sg", "delivery_info_sg")
