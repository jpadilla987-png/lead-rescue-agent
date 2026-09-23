from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    id: str
    kind: str
    label: str


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    relation: str


class EvidenceGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge] = []

    def add_node(self, node: Node) -> None:
        if node.id in self.nodes:
            raise ValueError(f"duplicate node: {node.id}")
        self.nodes[node.id] = node

    def link(self, edge: Edge) -> None:
        if edge.source not in self.nodes or edge.target not in self.nodes:
            raise ValueError("both edge endpoints must exist")
        self.edges.append(edge)

    def outgoing(self, node_id: str) -> list[Node]:
        targets = [edge.target for edge in self.edges if edge.source == node_id]
        return [self.nodes[target] for target in targets]
