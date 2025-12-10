import logging
import os
from asyncio import TaskGroup
from http import HTTPStatus
from typing import Any
from typing import TypedDict

from fastapi import APIRouter
from fastapi import HTTPException
from hiku.endpoint.graphql import AsyncGraphQLEndpoint
from hiku.endpoint.graphql import GraphQLRequest
from hiku.endpoint.graphql import SingleOrBatchedRequest
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from sellio.graph.schema import SCHEMA

router = APIRouter(tags=["GraphQL"])
log = logging.getLogger(__name__)

DEFAULT_ERROR_MESSAGE = "Unexpected error occurred."

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "../templates")
)


class GraphErrorDetails(TypedDict):
    message: str
    operationName: str
    exceptionClass: str
    exceptionMessage: str


class GraphErrorResponse(TypedDict):
    errors: list[GraphErrorDetails]


class GraphOkResponse(TypedDict):
    data: dict[str, Any] | None


class GraphOkResponseWithValidationErrors(GraphOkResponse):
    errors: list[dict[str, Any]] | None


GraphResponse = (
    GraphOkResponse | GraphOkResponseWithValidationErrors | GraphErrorResponse
)

SingleOrBatchedGraphResponse = GraphResponse | list[GraphResponse]


class GraphqlEndpoint(AsyncGraphQLEndpoint):
    def _error_response(
        self,
        exception: Exception,
        operation_name: str,
        message: str = DEFAULT_ERROR_MESSAGE,
        variables: dict[str, Any] = None,
    ) -> GraphErrorResponse:
        log.exception(
            "Exception occurred while dispatching graphql query. "
            f"{operation_name=}, {variables=}"
        )
        return GraphErrorResponse(
            errors=[
                GraphErrorDetails(
                    message=message,
                    operationName=operation_name,
                    exceptionClass=exception.__class__.__name__,
                    exceptionMessage=str(exception),
                )
            ]
        )

    async def safe_dispatch(
        self, graph_request: GraphQLRequest, context: dict | None
    ) -> GraphResponse:
        operation_name = graph_request.get("operationName")
        try:
            response = await super(AsyncGraphQLEndpoint, self).dispatch(
                graph_request, context
            )
            return response
        except Exception as e:
            return self._error_response(
                exception=e,
                operation_name=operation_name,
                variables=graph_request.get("variables"),
            )

    async def dispatch(
        self, data: SingleOrBatchedRequest, context: dict | None = None
    ) -> SingleOrBatchedGraphResponse:
        if isinstance(data, list):
            async with TaskGroup() as tg:
                tasks = (
                    tg.create_task(self.safe_dispatch(item, context))
                    for item in data
                )
            return list(task.result() for task in tasks)

        else:
            return await self.safe_dispatch(data, context)


endpoint = GraphqlEndpoint(
    SCHEMA,
    batching=True,
)


@router.post("/graphql")
async def graphql_endpoint(request: Request):
    try:
        request_data = await request.json()
    except Exception:
        raise HTTPException(HTTPStatus.BAD_REQUEST)
    return await endpoint.dispatch(request_data)


@router.get("/graphiql", response_class=HTMLResponse)
async def graphiql_endpoint(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="graphiql.html",
        context={"base_url": request.base_url},
    )
