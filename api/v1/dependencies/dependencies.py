from fastapi import Request

from core.router import Router
from core.workflow import Workflow


def get_router(request: Request) -> Router:
    return request.app.state.router

def get_workflow(request: Request) -> Workflow:
    return request.app.state.workflow
