from hiku.expr.core import S
from hiku.graph import Field
from hiku.graph import Node
from hiku.types import Integer
from hiku.types import String

from sellio.db_graph import company_sg

CompanyNode = Node(
    "Company",
    [
        Field("id", Integer, company_sg),
        Field("name", String, company_sg.c(S.this.name)),
        Field("email", String, company_sg.c(S.this.email)),
        Field("phone", String, company_sg.c(S.this.phone)),
    ],
)
