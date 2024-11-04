import logging

from .node_group import NodeGroup
from ..node.node_link import NodeLink

logger = logging.getLogger(__name__)


class Pipeline(NodeGroup, NodeLink):
    def __init__(
        self,
        all_nodes,
    ):
        super().__init__(all_nodes=all_nodes)
        self.head = all_nodes[0]
        self.tail = all_nodes[-1]

    def _connect_nodes(self):
        former = None
        for node in self.all_nodes.values():
            if former is None:
                former = node
                continue
            else:
                logger.info(f"connect {former.__name__} to {node.__name__}")
                former.connect(node)
                former = node

    @property
    def src_nodes(self):
        return self.head.src_nodes

    @src_nodes.setter
    def src_nodes(self, value):
        self.head.src_nodes = value

    def set_src_node(self, node):
        return self.head.set_src_node(node)

    @property
    def dst_nodes(self):
        return self.tail.dst_nodes

    @dst_nodes.setter
    def dst_nodes(self, value):
        self.tail.dst_nodes = value

    def set_dst_node(self, node):
        return self.tail.set_dst_node(node)

    def put(self, data):
        self.head.put(data)

    def connect(self, node, criteria=lambda data: True):
        self.tail.set_dst_node(node)
        node.set_src_node(self)
        self.set_dst_criteria(node, criteria)
        
    def set_dst_criteria(self, node, criteria):
        self.tail.set_dst_criteria(node, criteria)
