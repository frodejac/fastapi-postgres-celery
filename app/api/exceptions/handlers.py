from typing import Any, Callable, Dict, Type, Union

from fastapi import Request
from fastapi.responses import JSONResponse

from app.repos.exceptions.exceptions import ResourceNotFoundException


async def handle_resource_not_found(_: Request, exc: ResourceNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
        },
    )


exception_handlers: Dict[Union[int, Type[Exception]], Callable[..., Any]] = {
    ResourceNotFoundException: handle_resource_not_found,
}
