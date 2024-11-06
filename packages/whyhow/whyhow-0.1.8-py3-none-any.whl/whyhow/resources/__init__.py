"""Collection of route specific resources."""

from whyhow.resources.chunks import AsyncChunksResource, ChunksResource
from whyhow.resources.documents import (
    AsyncDocumentsResource,
    DocumentsResource,
)
from whyhow.resources.graphs import AsyncGraphsResource, GraphsResource
from whyhow.resources.nodes import AsyncNodesResource, NodesResource
from whyhow.resources.schemas import AsyncSchemasResource, SchemasResource
from whyhow.resources.workspaces import (
    AsyncWorkspacesResource,
    WorkspacesResource,
)

__all__ = [
    "AsyncChunksResource",
    "AsyncDocumentsResource",
    "AsyncGraphsResource",
    "AsyncNodesResource",
    "AsyncSchemasResource",
    "AsyncWorkspacesResource",
    "ChunksResource",
    "DocumentsResource",
    "GraphsResource",
    "NodesResource",
    "SchemasResource",
    "WorkspacesResource",
]
