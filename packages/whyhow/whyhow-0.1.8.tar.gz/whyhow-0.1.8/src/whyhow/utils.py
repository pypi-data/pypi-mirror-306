"""Internal utility functions."""

import json
from typing import Any

from .schemas import Chunk, Node, Relation, Triple


def _create_graph_from_knowledge_table(
    client: Any, file_path: str, workspace_name: str, graph_name: str
) -> str:
    """
    Create a graph from a knowledge table file.

    This internal function handles the process of creating a graph
    from a knowledge table file, including data loading, structuring,
    and uploading to the specified workspace.

    Parameters
    ----------
    client
        The client object used for API interactions.
    file_path : str
        Path to the knowledge table file.
    workspace_name : str
        Name of the workspace to use or create.
    graph_name : str
        Name for the graph to be created.

    Returns
    -------
    str
        The ID of the created graph.
    """
    print(f"Starting graph creation from knowledge table: {file_path}")

    # 1. Import the file
    with open(file_path, "r") as f:
        data = json.load(f)
    print(f"Loaded data from {file_path}")

    # 2. Structure the chunks and triples
    formatted_chunks = [
        Chunk(
            content=c["content"],
            user_metadata={
                "table_chunk_id": c["chunk_id"],
                "table_triple_id": c["triple_id"],
                "page": c["page"],
            },
        )
        for c in data["chunks"]
    ]
    print(f"Structured {len(formatted_chunks)} chunks")

    workspaces = list(client.workspaces.get_all(name=workspace_name))
    workspace = next(iter(workspaces), None)
    if not workspace:
        workspace = client.workspaces.create(name=workspace_name)
        print(f"Created new workspace: {workspace_name}")
    else:
        print(f"Using existing workspace: {workspace_name}")

    # 3. Upload the chunks to the workspace
    created_chunks = client.chunks.create(
        workspace_id=workspace.workspace_id, chunks=formatted_chunks
    )
    print(f"Uploaded {len(created_chunks)} chunks.")

    # for all chunks, get the triple_id in the user_metadata, then assign that chunk id to the triple
    formatted_triples = []

    for t in data["triples"]:
        chunk_ids = [
            c.chunk_id
            for c in created_chunks
            if "table_triple_id"
            in c.user_metadata.get(workspace.workspace_id, {})
            and c.user_metadata[workspace.workspace_id]["table_triple_id"]
            == t["triple_id"]
        ]
        formatted_triples.append(
            Triple(
                head=Node(
                    label=t["head"]["label"],
                    name=t["head"]["name"].strip("'\""),
                    properties=t["head"].get("properties", {}),
                ),
                tail=Node(
                    label=t["tail"]["label"],
                    name=t["tail"]["name"].strip("'\""),
                    properties=t["tail"].get("properties", {}),
                ),
                relation=Relation(name=t["relation"]["name"]),
                chunk_ids=chunk_ids,
            )
        )

    print(f"Structured {len(formatted_triples)} triples")

    graph = client.graphs.create_graph_from_triples(
        name=graph_name,
        workspace_id=workspace.workspace_id,
        triples=formatted_triples,
    )

    print("Successfully created graph from knowledge table.")
    return graph.graph_id
