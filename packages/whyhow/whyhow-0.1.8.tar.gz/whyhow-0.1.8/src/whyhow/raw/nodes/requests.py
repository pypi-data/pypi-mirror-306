"""Requests for the nodes endpoints."""

from typing import Any, Literal

from httpx import AsyncClient, Client

from whyhow.raw.base import ErrorReturnType, SuccessReturnType, asend, send
from whyhow.raw.nodes.schemas import (
    CreateNodeRequestBody,
    CreateNodeResponseBody,
    DeleteNodePathParameters,
    DeleteNodeResponseBody,
    GetAllNodesQueryParameters,
    GetAllNodesResponseBody,
    GetNodeChunksPathParameters,
    GetNodeChunksResponseBody,
    GetNodePathParameters,
    GetNodeResponseBody,
    NodeNameRaw,
    NodeTypeRaw,
    UpdateNodePathParameters,
    UpdateNodeRequestBody,
    UpdateNodeResponseBody,
)


# sync functions
def get_node(
    client: Client,
    node_id: str,
) -> SuccessReturnType[GetNodeResponseBody] | ErrorReturnType:
    """Get a node by its ID."""
    url = "/nodes/{node_id}"
    path_parameters = GetNodePathParameters(node_id=node_id)

    return send(
        client=client,
        url=url,
        method="get",
        path_parameters=path_parameters,
        response_body_schema=GetNodeResponseBody,
    )


def get_all_nodes(
    client: Client,
    skip: int | None = None,
    limit: int | None = None,
    name: str | None = None,
    type: str | None = None,
    workspace_name: str | None = None,
    workspace_id: str | None = None,
    graph_name: str | None = None,
    graph_id: str | None = None,
    chunk_ids: list[str] | None = None,
    order: Literal["ascending", "descending"] | None = None,
) -> SuccessReturnType[GetAllNodesResponseBody] | ErrorReturnType:
    """Get all nodes."""
    url = "/nodes"
    query_parameters = GetAllNodesQueryParameters(
        skip=skip,
        limit=limit,
        name=name,
        type=type,
        workspace_name=workspace_name,
        workspace_id=workspace_id,
        graph_name=graph_name,
        graph_id=graph_id,
        chunk_ids=chunk_ids,
        order=order,
    )

    return send(
        client=client,
        url=url,
        method="get",
        query_parameters=query_parameters,
        response_body_schema=GetAllNodesResponseBody,
    )


def create_node(
    client: Client,
    name: str,
    type: str,
    graph: str,
    properties: (
        dict[
            str,
            str
            | int
            | bool
            | float
            | list[str | int | bool | float | None]
            | None,
        ]
        | None
    ) = None,
    chunks: list[str] | None = None,
    strict_mode: bool = False,
) -> SuccessReturnType[CreateNodeResponseBody] | ErrorReturnType:
    """Create a node."""
    url = "/nodes"
    if properties is None:
        properties = {}
    if chunks is None:
        chunks = []
    body = CreateNodeRequestBody(
        name=name,
        type=type,
        graph=graph,
        properties=properties,
        chunks=chunks,
        strict_mode=strict_mode,
    )

    return send(
        client=client,
        url=url,
        method="post",
        request_body=body,
        response_body_schema=CreateNodeResponseBody,
    )


def update_node(
    client: Client,
    node_id: str,
    name: str | None = None,
    type: str | None = None,
    graph: str | None = None,
    properties: dict[str, Any] | None = None,
    chunks: list[str] | None = None,
) -> SuccessReturnType[UpdateNodeResponseBody] | ErrorReturnType:
    """Update a node by its ID."""
    url = "/nodes/{node_id}"
    path_parameters = UpdateNodePathParameters(node_id=node_id)
    body = UpdateNodeRequestBody(
        name=NodeNameRaw(root=name) if name is not None else None,
        type=NodeTypeRaw(root=type) if type is not None else None,
        graph=graph,
        properties=properties,
        chunks=chunks,
    )

    return send(
        client=client,
        url=url,
        method="put",
        path_parameters=path_parameters,
        request_body=body,
        response_body_schema=UpdateNodeResponseBody,
    )


def delete_node(
    client: Client,
    node_id: str,
) -> SuccessReturnType[DeleteNodeResponseBody] | ErrorReturnType:
    """Delete a node by its ID."""
    url = "/nodes/{node_id}"
    path_parameters = DeleteNodePathParameters(node_id=node_id)

    return send(
        client=client,
        url=url,
        method="delete",
        path_parameters=path_parameters,
        response_body_schema=DeleteNodeResponseBody,
    )


def get_node_chunks(
    client: Client,
    node_id: str,
) -> SuccessReturnType[GetNodeChunksResponseBody] | ErrorReturnType:
    """Get all chunks for a node by its ID."""
    url = "/nodes/{node_id}/chunks"
    path_parameters = GetNodeChunksPathParameters(node_id=node_id)

    return send(
        client=client,
        url=url,
        method="get",
        path_parameters=path_parameters,
        response_body_schema=GetNodeChunksResponseBody,
    )


# async functions
async def aget_node(
    client: AsyncClient,
    node_id: str,
) -> SuccessReturnType[GetNodeResponseBody] | ErrorReturnType:
    """Get a node by its ID."""
    url = "/nodes/{node_id}"
    path_parameters = GetNodePathParameters(node_id=node_id)

    return await asend(
        client=client,
        url=url,
        method="get",
        path_parameters=path_parameters,
        response_body_schema=GetNodeResponseBody,
    )


async def aget_all_nodes(
    client: AsyncClient,
    skip: int | None = None,
    limit: int | None = None,
    name: str | None = None,
    type: str | None = None,
    workspace_name: str | None = None,
    workspace_id: str | None = None,
    graph_name: str | None = None,
    graph_id: str | None = None,
    chunk_ids: list[str] | None = None,
    order: Literal["ascending", "descending"] | None = None,
) -> SuccessReturnType[GetAllNodesResponseBody] | ErrorReturnType:
    """Get all nodes."""
    url = "/nodes"
    query_parameters = GetAllNodesQueryParameters(
        skip=skip,
        limit=limit,
        name=name,
        type=type,
        workspace_name=workspace_name,
        workspace_id=workspace_id,
        graph_name=graph_name,
        graph_id=graph_id,
        chunk_ids=chunk_ids,
        order=order,
    )

    return await asend(
        client=client,
        url=url,
        method="get",
        query_parameters=query_parameters,
        response_body_schema=GetAllNodesResponseBody,
    )


async def acreate_node(
    client: AsyncClient,
    name: str,
    type: str,
    graph: str,
    properties: (
        dict[
            str,
            str
            | int
            | bool
            | float
            | list[str | int | bool | float | None]
            | None,
        ]
        | None
    ) = None,
    chunks: list[str] | None = None,
    strict_mode: bool = False,
) -> SuccessReturnType[CreateNodeResponseBody] | ErrorReturnType:
    """Create a node."""
    url = "/nodes"
    if properties is None:
        properties = {}
    if chunks is None:
        chunks = []
    body = CreateNodeRequestBody(
        name=name,
        type=type,
        graph=graph,
        properties=properties,
        chunks=chunks,
        strict_mode=strict_mode,
    )

    return await asend(
        client=client,
        url=url,
        method="post",
        request_body=body,
        response_body_schema=CreateNodeResponseBody,
    )


async def aupdate_node(
    client: AsyncClient,
    node_id: str,
    name: str | None = None,
    type: str | None = None,
    graph: str | None = None,
    properties: dict[str, Any] | None = None,
    chunks: list[str] | None = None,
) -> SuccessReturnType[UpdateNodeResponseBody] | ErrorReturnType:
    """Update a node by its ID."""
    url = "/nodes/{node_id}"
    path_parameters = UpdateNodePathParameters(node_id=node_id)
    body = UpdateNodeRequestBody(
        name=NodeNameRaw(root=name) if name is not None else None,
        type=NodeTypeRaw(root=type) if type is not None else None,
        graph=graph,
        properties=properties,
        chunks=chunks,
    )

    return await asend(
        client=client,
        url=url,
        method="put",
        path_parameters=path_parameters,
        request_body=body,
        response_body_schema=UpdateNodeResponseBody,
    )


async def adelete_node(
    client: AsyncClient,
    node_id: str,
) -> SuccessReturnType[DeleteNodeResponseBody] | ErrorReturnType:
    """Delete a node by its ID."""
    url = "/nodes/{node_id}"
    path_parameters = DeleteNodePathParameters(node_id=node_id)

    return await asend(
        client=client,
        url=url,
        method="delete",
        path_parameters=path_parameters,
        response_body_schema=DeleteNodeResponseBody,
    )


async def aget_node_chunks(
    client: AsyncClient,
    node_id: str,
) -> SuccessReturnType[GetNodeChunksResponseBody] | ErrorReturnType:
    """Get all chunks for a node by its ID."""
    url = "/nodes/{node_id}/chunks"
    path_parameters = GetNodeChunksPathParameters(node_id=node_id)

    return await asend(
        client=client,
        url=url,
        method="get",
        path_parameters=path_parameters,
        response_body_schema=GetNodeChunksResponseBody,
    )
