from typing import Annotated
from typing import AsyncGenerator

from fastapi import Depends
from fastapi import Request

from sellio.settings import Config


async def config_dependency(request: Request) -> AsyncGenerator[Config, None]:
    if config := request.state.config:
        yield config
    else:
        raise RuntimeError("Config is missing in appstate")


ConfigDependency = Annotated[Config, Depends(config_dependency)]
