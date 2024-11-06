"""Nodes resource."""

from typing import Any, AsyncIterator, Iterator

from whyhow.raw import (
    acreate_node,
    adelete_node,
    aget_all_nodes,
    aget_node,
    aget_node_chunks,
    aupdate_node,
    create_node,
    delete_node,
    get_all_nodes,
    get_node,
    get_node_chunks,
    update_node,
)
from whyhow.resources.base import AsyncResource, Resource, validate
from whyhow.schemas import Chunk, ChunkMetadata, Node


class NodesResource(Resource):
    """Nodes resource."""

    def get(self, node_id: str) -> Node:
        """Get a nodes.

        Parameters
        ----------
        node_id : str
            The node ID.

        Returns
        -------
        Node
            The node.
        """
        result = get_node(self.client, node_id)
        body = validate(result)

        node = Node(
            node_id=body.nodes[0].field_id,
            created_at=body.nodes[0].created_at,
            updated_at=body.nodes[0].updated_at,
            name=body.nodes[0].name,
            label=body.nodes[0].type,
            properties=body.nodes[0].properties,
            graph_id=body.nodes[0].graph,
            chunk_ids=body.nodes[0].chunks,
        )

        return node

    def get_all(
        self,
        limit: int = 10,
        name: str | None = None,
        type: str | None = None,
        workspace_name: str | None = None,
        workspace_id: str | None = None,
        graph_name: str | None = None,
        graph_id: str | None = None,
        chunk_ids: list[str] | None = None,
    ) -> Iterator[Node]:
        """Iterate over all nodes.

        Parameters
        ----------
        limit : int, optional
            The maximum number of nodes to fetch in each request.
        name : str, optional
            The name of the node to filter by.
        type : str, optional
            The type of the node to filter by.
        workspace_name : str, optional
            The name of the workspace to filter by.
        workspace_id : str, optional
            The ID of the workspace to filter by.
        graph_name : str, optional
            The name of the graph to filter by.
        graph_id : str, optional
            The ID of the graph to filter by.
        chunk_ids : list[str], optional
            The IDs of the chunks to filter by.

        Yields
        ------
        Node
            A node.

        """
        skip = 0
        while True:
            result = get_all_nodes(
                self.client,
                limit=limit,
                skip=skip,
                name=name,
                type=type,
                workspace_name=workspace_name,
                workspace_id=workspace_id,
                graph_name=graph_name,
                graph_id=graph_id,
                chunk_ids=chunk_ids,
            )
            body = validate(result)

            for node in body.nodes:
                skip += 1
                yield Node(
                    node_id=node.field_id,
                    created_at=node.created_at,
                    updated_at=node.updated_at,
                    name=node.name,
                    label=node.type,
                    properties=node.properties,
                    graph_id=node.graph,
                    chunk_ids=node.chunks,
                )

            if len(body.nodes) < limit:
                break

    def create(
        self,
        name: str,
        type: str,
        graph_id: str,
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
    ) -> Node:
        """Create a mode.

        Parameters
        ----------
        name : str
            The name of the mode.
        type : str
            The type of the mode.
        graph_id : str
            The graph ID.
        properties : dict[str, str | int | bool | float | list[str | int | bool | float | None] | None], optional
            The properties of the node.
        chunks : list[str], optional
            The IDs of the chunks.
        strict_mode : bool, optional
            Whether to use strict mode.

        Returns
        -------
        Node
            The created node.
        """
        result = create_node(
            self.client, name, type, graph_id, properties, chunks, strict_mode
        )
        body = validate(result)

        node = Node(
            node_id=body.nodes[0].field_id,
            created_at=body.nodes[0].created_at,
            updated_at=body.nodes[0].updated_at,
            name=body.nodes[0].name,
            label=body.nodes[0].type,
            properties=body.nodes[0].properties,
            graph_id=body.nodes[0].graph,
            chunk_ids=body.nodes[0].chunks,
        )

        return node

    def update(
        self,
        node_id: str,
        name: str | None = None,
        type: str | None = None,
        graph_id: str | None = None,
        properties: dict[str, Any] | None = None,
        chunks: list[str] | None = None,
    ) -> Node:
        """Update a node.

        Parameters
        ----------
        node_id : str
            The node ID.
        name : str, optional
            The new name for the node.
        type : str, optional
            The new type for the node.
        graph_id : str, optional
            The new graph ID for the node.
        properties : dict[str, Any], optional
            The new properties for the node.
        chunks : list[str], optional
            The new chunks for the node.

        Returns
        -------
        Node
            The updated node.
        """
        result = update_node(
            self.client, node_id, name, type, graph_id, properties, chunks
        )
        body = validate(result)

        node = Node(
            node_id=body.nodes[0].field_id,
            created_at=body.nodes[0].created_at,
            updated_at=body.nodes[0].updated_at,
            name=body.nodes[0].name,
            label=body.nodes[0].type,
            properties=body.nodes[0].properties,
            graph_id=body.nodes[0].graph,
            chunk_ids=body.nodes[0].chunks,
        )

        return node

    def delete(self, node_id: str) -> Node:
        """Delete a node.

        Parameters
        ----------
        node_id : str
            The node ID.
        """
        result = delete_node(self.client, node_id)
        body = validate(result)

        node = Node(
            node_id=body.nodes[0].field_id,
            created_at=body.nodes[0].created_at,
            updated_at=body.nodes[0].updated_at,
            name=body.nodes[0].name,
            label=body.nodes[0].type,
            properties=body.nodes[0].properties,
            graph_id=body.nodes[0].graph,
            chunk_ids=body.nodes[0].chunks,
        )

        return node

    def get_chunks(self, node_id: str) -> list[Chunk]:
        """Get the chunks of a node.

        Parameters
        ----------
        node_id : str
            The node ID.

        Returns
        -------
        list[Chunk]
            The chunks.
        """
        result = get_node_chunks(self.client, node_id)

        body = validate(result)

        chunks = []
        for raw_chunk in body.chunks:
            if raw_chunk.document is None:
                document_id_ = None
            else:
                document_id_ = raw_chunk.document.field_id

            chunks.append(
                Chunk(
                    chunk_id=raw_chunk.field_id,
                    created_at=raw_chunk.created_at,
                    updated_at=raw_chunk.updated_at,
                    document_id=document_id_,
                    workspace_ids=[w.field_id for w in raw_chunk.workspaces],
                    metadata=ChunkMetadata(
                        language=raw_chunk.metadata.language,
                        length=raw_chunk.metadata.length,
                        size=raw_chunk.metadata.size,
                        data_source_type=raw_chunk.metadata.data_source_type,
                        index=raw_chunk.metadata.index,
                        page=raw_chunk.metadata.page,
                        start=raw_chunk.metadata.start,
                        end=raw_chunk.metadata.end,
                    ),
                    content=raw_chunk.content.root,
                    embedding=raw_chunk.embedding,
                    tags=raw_chunk.tags,
                    user_metadata=raw_chunk.user_metadata,
                )
            )

        return chunks


class AsyncNodesResource(AsyncResource):
    """Nodes resource."""

    async def get(self, node_id: str) -> Node:
        """Get a nodes.

        Parameters
        ----------
        node_id : str
            The node ID.

        Returns
        -------
        Node
            The node.
        """
        result = await aget_node(self.client, node_id)
        body = validate(result)

        node = Node(
            node_id=body.nodes[0].field_id,
            created_at=body.nodes[0].created_at,
            updated_at=body.nodes[0].updated_at,
            name=body.nodes[0].name,
            label=body.nodes[0].type,
            properties=body.nodes[0].properties,
            graph_id=body.nodes[0].graph,
            chunk_ids=body.nodes[0].chunks,
        )

        return node

    async def get_all(
        self,
        limit: int = 10,
        name: str | None = None,
        type: str | None = None,
        workspace_name: str | None = None,
        workspace_id: str | None = None,
        graph_name: str | None = None,
        graph_id: str | None = None,
        chunk_ids: list[str] | None = None,
    ) -> AsyncIterator[Node]:
        """Iterate over all nodes.

        Parameters
        ----------
        limit : int, optional
            The maximum number of nodes to fetch in each request.
        name : str, optional
            The name of the node to filter by.
        type : str, optional
            The type of the node to filter by.
        workspace_name : str, optional
            The name of the workspace to filter by.
        workspace_id : str, optional
            The ID of the workspace to filter by.
        graph_name : str, optional
            The name of the graph to filter by.
        graph_id : str, optional
            The ID of the graph to filter by.
        chunk_ids : list[str], optional
            The IDs of the chunks to filter by.

        Yields
        ------
        Node
            A node.

        """
        skip = 0
        while True:
            result = await aget_all_nodes(
                self.client,
                limit=limit,
                skip=skip,
                name=name,
                type=type,
                workspace_name=workspace_name,
                workspace_id=workspace_id,
                graph_name=graph_name,
                graph_id=graph_id,
                chunk_ids=chunk_ids,
            )
            body = validate(result)

            for node in body.nodes:
                skip += 1
                yield Node(
                    node_id=node.field_id,
                    created_at=node.created_at,
                    updated_at=node.updated_at,
                    name=node.name,
                    label=node.type,
                    properties=node.properties,
                    graph_id=node.graph,
                    chunk_ids=node.chunks,
                )

            if len(body.nodes) < limit:
                break

    async def create(
        self,
        name: str,
        type: str,
        graph_id: str,
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
    ) -> Node:
        """Create a mode.

        Parameters
        ----------
        name : str
            The name of the mode.
        type : str
            The type of the mode.
        graph_id : str
            The graph ID.
        properties : dict[str, str | int | bool | float | list[str | int | bool | float | None] | None], optional
            The properties of the node.
        chunks : list[str], optional
            The IDs of the chunks.
        strict_mode : bool, optional
            Whether to use strict mode.

        Returns
        -------
        Node
            The created node.
        """
        result = await acreate_node(
            self.client, name, type, graph_id, properties, chunks, strict_mode
        )
        body = validate(result)

        node = Node(
            node_id=body.nodes[0].field_id,
            created_at=body.nodes[0].created_at,
            updated_at=body.nodes[0].updated_at,
            name=body.nodes[0].name,
            label=body.nodes[0].type,
            properties=body.nodes[0].properties,
            graph_id=body.nodes[0].graph,
            chunk_ids=body.nodes[0].chunks,
        )

        return node

    async def update(
        self,
        node_id: str,
        name: str | None = None,
        type: str | None = None,
        graph_id: str | None = None,
        properties: dict[str, Any] | None = None,
        chunks: list[str] | None = None,
    ) -> Node:
        """Update a node.

        Parameters
        ----------
        node_id : str
            The node ID.
        name : str, optional
            The new name for the node.
        type : str, optional
            The new type for the node.
        graph_id : str, optional
            The new graph ID for the node.
        properties : dict[str, Any], optional
            The new properties for the node.
        chunks : list[str], optional
            The new chunks for the node.

        Returns
        -------
        Node
            The updated node.
        """
        result = await aupdate_node(
            self.client, node_id, name, type, graph_id, properties, chunks
        )
        body = validate(result)

        node = Node(
            node_id=body.nodes[0].field_id,
            created_at=body.nodes[0].created_at,
            updated_at=body.nodes[0].updated_at,
            name=body.nodes[0].name,
            label=body.nodes[0].type,
            properties=body.nodes[0].properties,
            graph_id=body.nodes[0].graph,
            chunk_ids=body.nodes[0].chunks,
        )

        return node

    async def delete(self, node_id: str) -> Node:
        """Delete a node.

        Parameters
        ----------
        node_id : str
            The node ID.
        """
        result = await adelete_node(self.client, node_id)
        body = validate(result)

        node = Node(
            node_id=body.nodes[0].field_id,
            created_at=body.nodes[0].created_at,
            updated_at=body.nodes[0].updated_at,
            name=body.nodes[0].name,
            label=body.nodes[0].type,
            properties=body.nodes[0].properties,
            graph_id=body.nodes[0].graph,
            chunk_ids=body.nodes[0].chunks,
        )

        return node

    async def get_chunks(self, node_id: str) -> list[Chunk]:
        """Get the chunks of a node.

        Parameters
        ----------
        node_id : str
            The node ID.

        Returns
        -------
        list[Chunk]
            The chunks.
        """
        result = await aget_node_chunks(self.client, node_id)

        body = validate(result)

        chunks = []
        for raw_chunk in body.chunks:
            if raw_chunk.document is None:
                document_id_ = None
            else:
                document_id_ = raw_chunk.document.field_id

            chunks.append(
                Chunk(
                    chunk_id=raw_chunk.field_id,
                    created_at=raw_chunk.created_at,
                    updated_at=raw_chunk.updated_at,
                    document_id=document_id_,
                    workspace_ids=[w.field_id for w in raw_chunk.workspaces],
                    metadata=ChunkMetadata(
                        language=raw_chunk.metadata.language,
                        length=raw_chunk.metadata.length,
                        size=raw_chunk.metadata.size,
                        data_source_type=raw_chunk.metadata.data_source_type,
                        index=raw_chunk.metadata.index,
                        page=raw_chunk.metadata.page,
                        start=raw_chunk.metadata.start,
                        end=raw_chunk.metadata.end,
                    ),
                    content=raw_chunk.content.root,
                    embedding=raw_chunk.embedding,
                    tags=raw_chunk.tags,
                    user_metadata=raw_chunk.user_metadata,
                )
            )

        return chunks
