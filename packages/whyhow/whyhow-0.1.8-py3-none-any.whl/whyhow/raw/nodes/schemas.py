"""Collection of Pydantic models for the node routers."""

from typing import Literal

from whyhow.raw.autogen import (
    Name1,
    NodeChunksResponse,
    NodeCreate,
    NodesResponse,
    NodeUpdate,
    Type,
)
from whyhow.raw.base import (
    PathParameters,
    QueryParameters,
    RequestBody,
    ResponseBody,
)

# Auxiliary models
NodeNameRaw = Name1
NodeTypeRaw = Type


# GET /nodes/{node_id}
class GetNodePathParameters(PathParameters):
    """Path parameters for the get node endpoint."""

    node_id: str


class GetNodeResponseBody(ResponseBody, NodesResponse):
    """Response body for the get node endpoint."""


# GET /nodes
class GetAllNodesQueryParameters(QueryParameters):
    """Query parameters for the get all nodes endpoint."""

    skip: int | None
    limit: int | None
    name: str | None
    type: str | None
    workspace_name: str | None
    workspace_id: str | None
    graph_name: str | None
    graph_id: str | None
    chunk_ids: list[str] | None
    order: Literal["ascending", "descending"] | None


class GetAllNodesResponseBody(ResponseBody, NodesResponse):
    """Response body for the get all nodes endpoint."""


# POST /nodes
class CreateNodeRequestBody(RequestBody, NodeCreate):
    """Request body for the create node endpoint."""


class CreateNodeResponseBody(ResponseBody, NodesResponse):
    """Response body for the create node endpoint."""


# PUT /nodes/{node_id}
class UpdateNodePathParameters(PathParameters):
    """Path parameters for the update node endpoint."""

    node_id: str


class UpdateNodeRequestBody(RequestBody, NodeUpdate):
    """Request body for the update node endpoint."""


class UpdateNodeResponseBody(ResponseBody, NodesResponse):
    """Response body for the update node endpoint."""


# DELETE /nodes/{node_id}
class DeleteNodePathParameters(PathParameters):
    """Path parameters for the delete node endpoint."""

    node_id: str


class DeleteNodeResponseBody(ResponseBody, NodesResponse):
    """Response body for the delete node endpoint."""


# GET /nodes/{node_id}/chunks
class GetNodeChunksPathParameters(PathParameters):
    """Path parameters for the get node chunks endpoint."""

    node_id: str


class GetNodeChunksResponseBody(ResponseBody, NodeChunksResponse):
    """Response body for the get node chunks endpoint."""
