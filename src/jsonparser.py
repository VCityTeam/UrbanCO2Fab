# Currently this code is taken from https://github.com/MEPP-team/py3dtiles/blob/Tiler/Tilers/CityTiler/CityTemporalTiler.py
# TODO Need to integrate this code directly in py3dtiles (in long term)

import json
import argparse
import numpy as np
import json
import sys
from enum import Enum, unique

from pprint import pprint

class Node(object):
    @unique
    class Status(Enum):
        """
        Historical status of the node (mainly used on documentation/debug
        purposes) indicating the nature of the node in its relationship
        with past and future nodes
        """
        unknown = 1
        # Appears isolated at a single time stamp (neither ancestors nor
        # descendants)
        hapax = 2
        # Beginning of a lineage of nodes (no ancestors)
        start = 3
        # Termination of a lineage of nodes (no descendants)
        end = 4
        # Historical link/connection between the past nodes and future nodes
        # (has both ancestors and descendants)
        link = 5

    def __init__(self, **kwargs):
        # Attributes that will be dynamically added by the Json parsing
        # An integer used as Node identifier (local to a single Graph file)
        self.id = None
        # A string used as (global) Node identifier i.e. valid across a
        # set of Graph files
        self.globalid = None
        self.__dict__ = kwargs

        # When blending various graphs (respectively loaded from different
        # graph files), the nodes shared among such graphs (as designated
        # with their globalid) need to be reconciled. For some nodes (
        # (e.g. for nodes that are loaded when a previous node with
        # the same globalid already existed) the self.id (relative to a
        # file) will thus be lost. In order to help traceability (read
        # debugging) of the nodes, we keep the original file identifiers
        # in the following attribute:
        self.file_ids = ''

        self.creation_date = None
        self.deletion_date = None

        # Design note: we had the choice to either store the ancestor nodes
        # or to store the "ancestor edges" (that is edges that have this
        # node as target). Both choices have their respective drawbacks.
        # When storing the nodes and we need the information attached to
        # the edges we need to retrieve those edges (and the cost of retrieving
        # an edge out of its adjacent vertices is not constant in graph size).
        # And when storing the edges, retrieving the ancestors requires a
        # (constant time) walk on those edges.
        # Note that storing both is always risky because we must keep them
        # "aligned" (in sync).
        # We chose to store edges to keep the computation complexity constant.
        # The list of edges that have this node as target:
        self.ancestor_edges = list()

        # A list of edges which have this node a source. The targets of those
        # edges are thus nodes that come after in time which make them
        # descendants:
        self.descendant_edges = list()

        self.status = Node.Status.unknown
        self.set_hapax(self.get_time_stamp())

    def __str__(self):
        ret_str = f'Node: {self.globalid} (id: {self.id})\n'
        ret_str += f'  Creation date: {self.creation_date} \n'
        ret_str += f'  Deletion date: {self.deletion_date} \n'
        ret_str += f'  Status: {self.status} \n'
        if self.ancestor_edges:
            ret_str += f'  Ancestors: '
            for ancestor in self.get_ancestors():
                ret_str += ancestor.globalid + ', '
            ret_str += '\n'
        if self.descendant_edges:
            ret_str += f'  Descendants: '
            for descendant in self.get_descendants():
                ret_str += descendant.globalid + ', '
            ret_str += '\n'
        if self.file_ids != '':
            ret_str += f'  file_ids: {self.file_ids}\n'
        return ret_str

    def is_unknown(self):
        if self.status == Node.Status.unknown:
            return True
        return False

    def is_hapax(self):
        if self.status == Node.Status.hapax:
            return True
        return False

    def is_start(self):
        if self.status == Node.Status.start:
            return True
        return False

    def is_end(self):
        if self.status == Node.Status.end:
            return True
        return False

    def is_link(self):
        if self.status == Node.Status.link:
            return True
        return False

    def assert_status_coherence(self):
        ancestors = self.get_ancestors()
        descendants = self.get_descendants()
        if not ancestors and not descendants:
            if self.is_unknown():
                # No information and nothing to assert
                return
            if self.is_hapax():
                # A hapax indeed has not ancestors nor descendants
                return
            else:
                print("Only a hapax has neither ancestors nor descendants.")
                sys.exit(1)
        if ancestors and not descendants:
            if self.is_unknown():
                print("Should have been an end prior to having ancestors.")
                sys.exit(1)
            return
        if not ancestors and descendants:
            if self.is_unknown():
                print("Should have been a start prior to having descendants.")
                sys.exit(1)
            return
        # The Node has both ancestors and descendants:
        if self.is_unknown():
            print("Should have been a hapax, a start or end prior to having")
            print("both ancestors and descendants.")
            sys.exit(1)
        if not self.is_link():
            print("This node has both ancestors and descendants but is not")
            print("a link but a: ", self.status)
            sys.exit(1)

    def are_all_ancestor_edges_fusion_typed(self):
        """
        :return: True when they are at least two ancestor edges and all
                 ancestor edges are fusion edges. False otherwise.
        """
        ancestor_edges = self.get_ancestor_edges()
        if len(ancestor_edges) < 2:
            # We need at least two edges for them to be the same
            return False
        for edge in ancestor_edges:
            if not edge.is_fusion():
                return False
        return True

    def are_all_descendant_edges_subdivision_typed(self):
        """
        :return: True when they are at least two descendant edges and all
                 descendant edges are subdivision edges. False otherwise.
        """
        descendant_edges = self.get_descendant_edges()
        if len(descendant_edges) < 2:
            # We need at least two edges for them to be the same
            return False
        for edge in descendant_edges:
            if not edge.is_subdivided():
                return False
        return True

    def do_all_ancestor_nodes_share_same_date(self):
        """
        :return: True when they are at least two ancestor nodes and all
                 such ancestor nodes have exactly the same creation and
                 deletiondates. False otherwise.
        """
        ancestors = self.get_ancestors()
        if len(ancestors) < 2:
            # We need at least two ancestors for them to have matching dates
            return False
        creation_date = ancestors[0].creation_date
        deletion_date = ancestors[0].deletion_date
        for ancestor in ancestors[1:]:
            if not ancestor.creation_date == creation_date:
                return False
            if not ancestor.deletion_date == deletion_date:
                return False
        return True

    def do_all_descendant_nodes_share_same_date(self):
        """
        :return: True when they are at least two descendant nodes and all
                 such descendant nodes have exactly the same creation and
                 deletiondates. False otherwise.
        """
        descendants = self.get_descendants()
        if len(descendants) < 2:
            # We need at least two descendants for them to have matching dates
            return False
        creation_date = descendants[0].creation_date
        deletion_date = descendants[0].deletion_date
        for descendant in descendants[1:]:
            if not descendant.creation_date == creation_date:
                return False
            if not descendant.deletion_date == deletion_date:
                return False
        return True

    def get_time_stamp(self):
        return int(self.globalid.split('::')[0])

    def get_deletion_date(self):
        return self.deletion_date

    def set_deletion_date(self, time_stamp):
        self.deletion_date = time_stamp

    def get_creation_date(self):
        return self.creation_date

    def set_creation_date(self, time_stamp):
        self.creation_date = time_stamp

    def set_creation_date_if_earlier(self, time_stamp):
        """
        When the given time_stamp is earlier than the current value of
        the node creation_date then set the creation_date with that value
        :param time_stamp: the time stamp that should be set when it is earlier
        :return: None
        """
        if not self.creation_date:
            self.creation_date = time_stamp
            return
        if time_stamp < self.creation_date:
            self.creation_date = time_stamp

    def set_creation_date_recursive(self, time_stamp):
        self.set_creation_date_if_earlier(time_stamp)
        for descendant in self.get_descendants():
            descendant.set_creation_date_recursive(time_stamp)

    def set_deletion_date_if_later(self, time_stamp):
        if not self.deletion_date:
            self.deletion_date = time_stamp
            return
        if time_stamp > self.deletion_date:
            self.deletion_date = time_stamp

    def get_ancestors(self):
        return [edge.ancestor for edge in self.ancestor_edges]

    def add_ancestor_edge(self, ancestor_edge):
        if not ancestor_edge:
            return
        self.ancestor_edges.append(ancestor_edge)
        if self.is_hapax():
            self.set_end()
        elif self.is_start():
            self.set_link()

    def add_ancestor_edges(self, ancestor_edges_list):
        for edge in ancestor_edges_list:
            self.add_ancestor_edge(edge)

    def get_ancestor_edges(self):
        return self.ancestor_edges

    def get_descendants(self):
        """
        :return: the list of the direct descendants (no recursion done)
        """
        return [edge.descendant for edge in self.descendant_edges]

    def add_descendant_edge(self, descendant_edge, debug_mode=False):
        if not descendant_edge:
            return
        if debug_mode and descendant_edge in self.descendant_edges:
            print("The following edge: ")
            pprint(vars(descendant_edge))
            print("is already part of the descendant edges of this node: ")
            pprint(vars(self))
            print('Exiting.')
            sys.exit(1)
        self.descendant_edges.append(descendant_edge)
        if self.is_hapax():
            self.set_start()
        elif self.is_end():
            self.set_link()

    def add_descendant_edges(self, descendant_edge_list):
        for edge in descendant_edge_list:
            self.add_descendant_edge(edge)

    def get_descendant_edges(self):
        return self.descendant_edges

    def reset_descendant_edges(self):
        self.descendant_edges = list()

    def disconnect_adjacent_edges(self):
        self.ancestor_edges = list()
        self.reset_descendant_edges()

    def set_hapax(self, time_stamp):
        if not self.is_unknown():
            print("Failing to promote as hapax from status: ", self.status)
            sys.exit(1)
        self.status = Node.Status.hapax
        if self.creation_date:
            print("This newly converted hapax already had a creation_date.")
            sys.exit(1)
        self.creation_date = time_stamp
        if self.deletion_date:
            print("This newly converted hapax already had a deletion_date.")
            sys.exit(1)
        self.deletion_date = time_stamp
        self.assert_status_coherence()

    def set_start(self, time_stamp=None):
        if not self.is_unknown() and not self.is_hapax():
            print("Failed to define as start.")
            sys.exit(1)
        if self.is_end():
            print("Failed to convert an end into being a start.")
            sys.exit(1)
        if self.is_link():
            print("Failed to convert a link into being a start.")
            sys.exit(1)
        self.status = Node.Status.start
        if time_stamp:
            if self.creation_date:
                print("Warning: overwriting a creation_date of a new start.")
            self.creation_date = time_stamp
        self.assert_status_coherence()

    def set_end(self, time_stamp=None):
        if not self.is_unknown() and not self.is_hapax():
            print("Failed to define as end.")
            sys.exit(1)
        if self.is_start():
            print("Failed to convert a start into being a end.")
            sys.exit(1)
        if self.is_link():
            print("Failed to convert a link into being an end.")
            sys.exit(1)
        self.status = Node.Status.end
        if time_stamp:
            if self.deletion_date:
                print("Warning: overwriting a creation_date of a new end.")
            self.deletion_date = time_stamp
        self.assert_status_coherence()

    def set_link(self):
        if self.is_unknown():
            print("An unknown node should not be converted to being an link.")
            sys.exit(1)
        if self.is_hapax():
            print("An hapax node should not be converted to being an link.")
            sys.exit(1)
        self.status = Node.Status.link


class Edge(object):

    def __init__(self, **kwargs):
        # Attributes that will be dynamically added by the Json parsing
        # An integer used as Node identifier (local to a single Graph file)
        self.id = None
        # An integer index designating the source Node
        self.source = None
        # An integer index designating the target Node
        self.target = None
        # A string among 'replace', 'create' and 'delete'
        self.type = None
        # A string that, when type is 'replace', is among 'fused', 'modified',
        # 're-ided', 'subdivided' and 'unchanged'.
        self.tags = None
        self.__dict__ = kwargs

        # Refer to Node.file_ids eponymous attribute for comments:
        self.file_ids = ''
        # The Node with self.source as identifier
        self.ancestor = None
        # The Node with self.target as identifier
        self.descendant = None

    def set_ancestor(self, ancestor_node):
        self.ancestor = ancestor_node
        if ancestor_node:
            ancestor_node.add_descendant_edge(self)

    def get_ancestor(self):
        return self.ancestor

    def set_descendant(self, descendant_node):
        self.descendant = descendant_node
        if descendant_node:
            descendant_node.add_ancestor_edge(self)

    def get_descendant(self):
        return self.descendant

    def is_replace(self):
        if self.type == 'replace':
            return True
        return False

    def is_unchanged(self):
        if self.is_replace() and self.tags == 'unchanged':
            return True
        return False

    def is_subdivided(self):
        if self.is_replace() and self.tags == 'subdivided':
            return True
        return False

    def is_re_ided(self):
        if self.is_replace() and self.tags == 're-ided':
            return True
        return False

    def is_modified(self):
        if self.is_replace() and self.tags == 'modified':
            return True
        return False

    def set_modified(self):
        self.type = 'replace'
        self.tags = 'modified'

    def is_fusion(self):
        if not self.is_replace():
            return False
        if self.tags == 'fused':
            return True
        return False

    def are_adjecent_nodes_one_to_one(self):
        """
        :return: True iif the ancestor node only has a single descendant edge
                (that has to be this one) AND the descendant node only has a
                single ancestor edge (that must also be this one). False
                otherwise.
        """
        if len(self.ancestor.get_descendant_edges()) != 1:
            return False
        if len(self.descendant.get_ancestor_edges()) != 1:
            return False
        return True


class Graph(object):

    def __init__(self, nodes=None, edges=None):
        if not nodes:
            self.nodes = list()
        else:
            self.nodes = nodes
        if not edges:
            self.edges = list()
        else:
            self.edges = edges

    def extend_with_subgraph(self, sub_graph):
        # Concerning the nodes of sub_graph we have two possibilities
        # - the node with corresponding globalid already exists in this
        #   graph in which case we need the edges to point to it
        # - the nodes is new (i.e. the node does not correspond to and existing
        #   node with the same globalid within this graph) and we need to
        #   pour/add in this graph

        # The dictionary having the sub_graph node index as key and this
        # graph node as value
        for node in sub_graph.nodes:
            existing_node = self.find_node(node.globalid)
            if existing_node:
                # We need to rewire the edges to the already existing node
                ancestor_edges = node.get_ancestor_edges()
                if ancestor_edges:
                    for edge in ancestor_edges:
                        edge.set_descendant(existing_node)

                descendant_edges = node.get_descendant_edges()
                if descendant_edges:
                    for edge in descendant_edges:
                        edge.set_ancestor(existing_node)

                # Keep a trace of the identification of the nodes
                existing_node.file_ids += f'{node.id}, '
            else:
                # No edge rewiring required. We simply need to add the
                # new sub-graph node to the this graph and change its
                # id to avoid id collisions:
                node.file_ids += f'{node.id}, '
                node.id = len(self.nodes) + 1
                self.nodes.append(node)

        # All sub-graph edges (rewired or not) must be kept and thus get
        # poured/blended within this graph:
        for new_edge in sub_graph.edges:
            new_edge.file_ids += f'{new_edge.id}, '
            new_edge.id = len(self.edges) + 1
            self.edges.append(new_edge)

    def add_node(self, new_node):
        self.nodes.append(new_node)

    def find_node(self, globalid):
        """
        Retrieve, when it exists, the node with the given globalid
        :param globalid: the global id that is looked for
        :return: the node with globalid when found, None otherwise
        """
        encountered = [node for node in self.nodes if node.globalid == globalid]
        if len(encountered) == 0:
            return None
        elif len(encountered) == 1:
            return encountered[0]
        else:
            print(f'Many nodes with same globalid: {globalid}')
            pprint(vars(encountered))
            sys.exit()

    def delete_node(self, node, deep_assert=False):
        """
        Assert this node has no adjacent edge that it knows about and delete
        it from the graph.
        :param node: the node to be removed
        :param deep_assert: when true, assert that no other edge of the graph
                            (that the node wouldn't know about) is pointing to
                            the argument node
        :return: True when properly deleted, sys.exit() otherwiwe
        """
        if node.get_ancestors() or node.get_descendants():
            print('Cannot delete following node with ancestors or descendants')
            pprint(vars(node))
            sys.exit()
        if deep_assert:
            for edge in self.edges:
                if edge.get_ancestor() == node or edge.get_descendant() == node:
                    print('Cannot delete following node:')
                    pprint(vars(node))
                    print('   because it is refered by following edge:')
                    pprint(vars(edge))
                    sys.exit()
        if node not in self.nodes:
            print('Cannot delete following node:')
            pprint(vars(node))
            print('   because it is not in the graph nodes.')
            sys.exit()
        self.nodes.remove(node)
        return True

    def disconnect_edge(self, edge):
        """
        Isolate this edge from its adjacent nodes and tell those adjacent
        nodes to forget about the existence of this edge. This method
        is usually called prior to delete_edge.
        :param edge: the edge to be disconnected.
        """
        # Clean up the ancestor and descendant nodes:
        if not edge.ancestor:
            print('The following edge has no ancestor:')
            pprint(vars(edge))
            print('Exiting.')
            sys.exit(1)
        descendant_edges = edge.ancestor.get_descendant_edges()
        if edge in descendant_edges:
            descendant_edges.remove(edge)

        if not edge.descendant:
            print('The following edge has no ancestor:')
            pprint(vars(edge))
            print('Exiting.')
            sys.exit(1)
        ancestor_edges = edge.descendant.get_ancestor_edges()
        if edge in ancestor_edges:
            ancestor_edges.remove(edge)

        # We finish will un-connecting the edge per-se
        edge.set_ancestor(None)
        edge.set_descendant(None)

    def delete_edge(self, edge, deep_assert=False):
        """
        Assert this edge has no adjacent nodes (that it knows about) and delete
        it from the graph.
        :param edge: the edge to be removed
        :param deep_assert: when true, assert that no other node of the graph
                            (that the edge wouldn't know about) is pointing to
                            the argument edge
        :return: True when properly deleted, sys.exit() otherwiwe
        """
        if edge.get_ancestor() or edge.get_descendant():
            print('Cannot delete following edge with an ancestor or descendant')
            pprint(vars(edge))
            sys.exit()
        if deep_assert:
            for node in self.nodes:
                if edge in node.get_ancestor_edges():
                    print('Cannot delete following edge:')
                    pprint(vars(edge))
                    print('   because it is an ancestor edge of following node:')
                    pprint(vars(node))
                    sys.exit()
                if edge in node.get_descendant_edges():
                    print('Cannot delete following edge:')
                    pprint(vars(edge))
                    print('   because it is a descendant edge of following node:')
                    pprint(vars(node))
                    sys.exit()
        self.edges.remove(edge)
        return True

    def collapse_edge_and_remove_ancestor(self, edge, debug_mode=False):
        """
        Collapse the given edge that is
         - take all the ancestor edges of the ancestor of the argument edge
           and make them ancestor edges of the descendant of that argument edge
         - remove the argument edge from the list of ancestor_edges
         - remove the argument edge from the graph
         - set the start date of the descendant of the argument edge as being
           the start date of the ancestor of the argument edge
        :param edge: the edge that should be removed
        :param debug_mode: when True assume something is wrong and realize
                           additional sanity checks
        :return: True when edge removed, sys.exit() otherwise
        """
        ancestor = edge.get_ancestor()
        descendant = edge.get_descendant()
        ancestor_edges = ancestor.get_ancestor_edges()

        # Rewire the ancestor_edges to the descendant
        if ancestor_edges:
            for ancestor_edge in ancestor_edges:
                ancestor_edge.set_descendant(descendant)
            # Conversely, let the descendant know about its new ancestor edges
            descendant.add_ancestor_edges(ancestor_edges)

        # Disconnect the ancestor node from all its adjacent edges
        ancestor.disconnect_adjacent_edges()

        # We must now proceed with isolating/un-connecting the edge
        self.disconnect_edge(edge)

        # Both the ancestor node and the edge to be collapsed are now isolated
        # from the graph. We can proceed with their removal:
        self.delete_node(ancestor, debug_mode)
        self.delete_edge(edge, debug_mode)

        return True

    def split_edge_and_remove_descendant(self, edge, debug_mode=False):
        """
        Split the given edge that is
         - take all the descendant edges of the descendant of the argument edge
           and make them descendant edges of the ancestor of that argument edge
         - remove the argument edge from the list of descendant_edges (of
           the ancestor for the argument edge)
         - remove the argument edge from the graph
         - set the start date of the descendants of the descendant of argument
           edge as being the start date of the descendant of the argument edge
        :param edge: the edge that should split (and technically removed)
        :param debug_mode: when True assume something is wrong and realize
                           additional sanity checks
        :return: True when edge removed, sys.exit() otherwise
        """

        ancestor = edge.get_ancestor()
        descendant = edge.get_descendant()
        descendant_edges = descendant.get_descendant_edges()

        # Rewire the ancestor of descendant_edges (of the descendant) to
        # being the ancestor
        if descendant_edges:
            for descendant_edge in descendant_edges:
                descendant_edge.set_ancestor(ancestor)
            # Conversely, let the ancestor node know it has new descendant
            # edges (acting as the split versions of the argument edge)
            ancestor.add_descendant_edge(descendant_edge)

        # Disconnect the descendant node from all its adjacent edges
        descendant.disconnect_adjacent_edges()

        # We must now proceed with isolating/un-connecting the edge
        self.disconnect_edge(edge)

        # Both the descendant node and the edge to be collapsed are now isolated
        # from the graph. We can proceed with their removal:
        self.delete_node(descendant, debug_mode)
        self.delete_edge(edge, debug_mode)

        return True

    def display_characteristics(self, indent=''):
        print(indent, "Nodes: total number", len(self.nodes))
        edges_number = len(self.edges)
        modified_edges_number = \
            len([e for e in self.edges if e.is_modified()])
        re_ided_edges_number = \
            len([e for e in self.edges if e.is_re_ided()])
        subdivision_edges_number = \
            len([e for e in self.edges if e.is_subdivided()])
        fusion_edges_number = \
            len([e for e in self.edges if e.is_fusion()])
        unchanged_edges_number = \
             len([e for e in self.edges if e.is_unchanged()])
        replacement_edges_number = modified_edges_number \
                                   + re_ided_edges_number \
                                   + subdivision_edges_number \
                                   + fusion_edges_number \
                                   + unchanged_edges_number

        print(indent, "Edges: total number", edges_number)
        print(indent, "  - modified edges: ",    modified_edges_number)
        print(indent, "  - re-ided edges: ",     re_ided_edges_number)
        print(indent, "  - subdivision edges: ", subdivision_edges_number)
        print(indent, "  - fusion edges: ",      fusion_edges_number)
        print(indent, "  - unchanged edges: ",   unchanged_edges_number)
        print(indent, "  - replace edges total", replacement_edges_number)
        if edges_number != replacement_edges_number:
            print(indent, "WARNING: missmatching number of edges")


class GraphMLDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, dct):
        if 'id' in dct and 'globalid' in dct:
            return Node(**dct)
        if      'id'     in dct \
            and 'source' in dct \
            and 'target' in dct \
            and 'type'   in dct \
            and 'tags'   in dct:
            return Edge(**dct)
        return dct


def reconstruct_graph_connectivity(cli_args):
    graph = None
    print("Reconstructing graph: ")
    print("   Loading nodes and edges of files: ")
    # Deserialize the temporal (sub) graphs to constitute the general graph
    for temporal_graph_filename in cli_args:
        with open(temporal_graph_filename, 'r') as temporal_graph_file:
            temporal_graph = json.loads(temporal_graph_file.read(),
                                        cls=GraphMLDecoder)

        current_nodes = temporal_graph['nodes']
        # Because the Json GraphML we parse is produced with boost::ptree's
        # write_json method that is well known for not conforming to Json
        # (integers are serialized as strings i.e. enclosed with double quotes)
        # we need to "fix" things after the Json parser is run
        for node in current_nodes:
            if isinstance(node.id, str):
                node.id = int(node.id)

        current_edges = temporal_graph['edges']
        # Edges id must also be type fixed (refer above to current_nodes)
        for edge in current_edges:
            if isinstance(edge.id, str):
                edge.id = int(edge.id)

        # Additionally we need to replace the node indexes (integer) loaded
        # as source and target (with the Json type fix) to their corresponding
        # references (as python objects):
        for edge in current_edges:
            if isinstance(edge.source, str):
                edge.set_ancestor(current_nodes[int(edge.source)])
            if isinstance(edge.target, str):
                edge.set_descendant(current_nodes[int(edge.target)])

        # Eventually we can pour/blend the current graph with the central
        # graph
        new_sub_graph = Graph(current_nodes, current_edges)
        if not graph:
            graph = new_sub_graph
        else:
            graph.extend_with_subgraph(new_sub_graph)
        print("   ", temporal_graph_filename, ": done.")
    print("  Loading of files: done.")
    print("Graph reconstruction: done.")
    return graph


def simplify_graph(graph, debug_mode=False):
    print("Simplifying the graph:")
    # At this point we have lineage information at hand in the form of the
    # reconstructed graph. We still have to simplify that graph in order
    # to re-interpret the available lineages at the level of the objects
    # (the buildings in this application). For example if the building B_1 is
    # present for year Y1, Y2 and Y3 and the land-print (geometry) of the
    # building remains unchanged during those years (same geometry) then
    # we can abstract such a situation by stating (in a 3DTiles temporal
    # framework) that building B_1 has a creation date of Y1 and a deletion
    # date of Y3. In other terms we simplified the sub-graph
    #                 unchanged               unchanged
    #     [B_1, Y1] ------------> [B_1, Y2] -------------> [B_1, Y3]
    # to be reduced to a single node/vertex
    #                           [B_1, Y1-Y3]
    # For more complicated cases (e.g. when the geometry gets modified), the
    # simplified graph will still posses edges that will need to be
    # represented (within the resulting tileset) as (3DTiles) temporal
    # transactions.
    #
    # In the following simplification process note that we iterate over
    # the time stamps in order to apply some graph simplification (empirical)
    # rules. When doing so we start from the past (oldest time stamps) and
    # proceed towards the future (the most recent time stamps). The reason
    # for this past to future time oriented sweeping process (as opposed to
    # random order or from future to past) is to obtain a simplified graph
    # that keeps the most recent building geometries (and removes the oldest
    # nodes i.e. the most ancient building geometries). The assumption behind
    # such time stamp sweeping strategy is that most recent city descriptions
    # are also the most detailed.

    # Retrieve, out of the node's global identifier, an ordered (from oldest
    # to most recent) list of time stamps (where the oldest time stamp is
    # weeded out):
    time_stamps_set = set()
    for node in graph.nodes:
        time_stamps_set.add(node.get_time_stamp())
    time_stamps = list(time_stamps_set)
    time_stamps.sort()

    # Note that the relative order of application of the following
    # simplification strategies (labeled as stages) does matter. In particular
    #  - collapsing unchanged/re-ided 1 to 1 edges should NOT be realized
    #    prior to collapsing fusion edges, but
    #  - collapsing unchanged/re-ided 1 to 1 edges MUST be realized prior to
    #    collapsing subdivision edges
    # The above constraints on relative order leave a single ordering
    # possibility that is thus used below.



    print("  Stage 0: collapsing unchanged/re-ided 1 to 1 edges.")
    initial_number_one_to_one_edges = \
        len([ e for e in graph.edges if e.are_adjecent_nodes_one_to_one() \
                               and (e.is_unchanged() or e.is_re_ided())])
    number_deleted_edges = 0
    one_to_one_number = 0
    to_remove = graph.edges.copy()
    for edge in to_remove:
        if not edge.are_adjecent_nodes_one_to_one():
            continue
        if edge.is_unchanged() or edge.is_re_ided():
            graph.collapse_edge_and_remove_ancestor(edge, debug_mode)
            one_to_one_number +=1
            print(f'    Number of collapsed edges: {one_to_one_number} / {initial_number_one_to_one_edges} ',
                  end='\r')
    print(f'    Number of collapsed edges: {one_to_one_number} / {initial_number_one_to_one_edges}')
    graph.display_characteristics('    ')

    print("  Stage 1: collapsing fusion edges.")
    print("    Initial number of fusion edges: ",
          len([ e for e in graph.edges if e.is_fusion()]))
    for time_stamp in time_stamps:
        current_nodes = [n for n in graph.nodes
                        if n.get_time_stamp() == time_stamp]
        for node in current_nodes:
            if not node.are_all_ancestor_edges_fusion_typed():
                continue
            if not node.do_all_ancestor_nodes_share_same_date():
                continue
            # We can proceed with the collapsal of all fusion edges
            node.set_creation_date(node.get_ancestors()[0].get_creation_date())
            # We need to freeze the list of edges to be dealt with (as opposed
            # to using e.g. "for ancestor_edge in node.get_ancestor_edges()")
            # because the operator used within the loop possibly modifies
            # that list by adding new edges (that we don't want to delete)
            # on the fly:
            ancestor_edges = node.get_ancestor_edges().copy()
            for ancestor_edge in ancestor_edges:
                graph.collapse_edge_and_remove_ancestor(ancestor_edge,
                                                        debug_mode)
    number_fusion_edges_left = len([ e for e in graph.edges if e.is_fusion()])
    if number_fusion_edges_left:
        print("    Remaining number of (un-removed) fusion edges : ",
              number_fusion_edges_left)
    else:
        print("    All removed.")

    print("  Stage 2: collapsing subdivision edges.")
    initial_number_fusion_edges = \
        len([ e for e in graph.edges if e.is_subdivided()])
    number_deleted_edges = 0
    print( f'   Deleted subdivision edges {number_deleted_edges} / {initial_number_fusion_edges}',
           end='\r')
    for time_stamp in time_stamps:
        current_nodes = [n for n in graph.nodes
                        if n.get_time_stamp() == time_stamp]
        for node in current_nodes:
            if not node.are_all_descendant_edges_subdivision_typed():
                continue
            if not node.do_all_descendant_nodes_share_same_date():
                continue
            ancestor_edges = node.get_ancestor_edges()
            if len(ancestor_edges) > 1:
                # The proper/clean way of dealing with a subdivided node that
                # has more thatn one ancestors is not yet established. For
                # the time being we thus leave such a situation untouched.
                continue

            # Whether the is no ancestor at all or only one we shall proceed
            # with the "split" of all subdivision edges. For both cases we
            # shall propagate the creation date:
            for descendant_node in node.get_descendants():
                descendant_node.set_creation_date(node.get_creation_date())

            if len(ancestor_edges) == 0:
                # Because we already propagated the creation date of the node
                # (to its descendants), the set of the descendants capture all
                # the geometry for the current time stamp. We can thus get
                # git of the present node and all the sub-division edges
                # without loss of information (in fact this sub-division was
                # not a geometrical one but a logical one).
                for descendant_edge in node.get_descendant_edges().copy():
                    graph.disconnect_edge(descendant_edge)
                    graph.delete_edge(descendant_edge, True)
                    number_deleted_edges +=1
                    print(f'   Deleted subdivision edges {number_deleted_edges} / {initial_number_fusion_edges}',
                        end='\r')

                # We can proceed with the removal of the node:
                graph.delete_node(node, debug_mode)

            else:   # This means there is a single ancestor edge
                # We shall re-label all the sub-divided edges that we deal
                # with (below) as 'modified' so when we build the corresponding
                # transaction we have a trace that this was a sub-division case
                # with modification:
                for descendant_edge in node.get_descendant_edges():
                    descendant_edge.set_modified()
                ancestor_edge = ancestor_edges[0]
                if not ancestor_edge.is_modified():
                    print("All non modified edges should have been collapsed.")
                    print("Yet, the following edge is not:")
                    pprint(vars(ancestor_edge))
                    print("Exiting")
                    sys.exit(1)
                graph.split_edge_and_remove_descendant(ancestor_edge,
                                                       debug_mode)
                number_deleted_edges += 1
                print(f'   Deleted subdivision edges {number_deleted_edges} / {initial_number_fusion_edges}',
                      end='\r')

    number_edges_left = len([ e for e in graph.edges if e.is_subdivided()])
    if number_edges_left:
        print("    Remaining number of (un-removed) subdivision edges : ",
              number_edges_left)
    else:
        print("    All removed.")

    print("Simplifying the graph: done.")

def process_temporal_data(cli_args):
    #FIXME: this variable shadows the global one. Consider using only
    #       the global one since the following local one is to transmitted
    #       to methods like Node::add_descendant_edge()
    debug_mode = True
    graph = reconstruct_graph_connectivity(cli_args)
    graph.display_characteristics()
    simplify_graph(graph, debug_mode)
    graph.display_characteristics()

    if not debug_mode:
        for node in graph.nodes:
            if node.is_unknown():
                print("A node with unknown status was found:")
                pprint(vars(node))
                sys.exit(1)
            print(node)

        for edge in graph.edges:
            pprint(vars(edge))


def handleGraph(): 
  with open('DifferencesAsGraph.json', 'r') as handle:
      parsed = json.load(handle)
      nodeDict = dict()
      for node in parsed["nodes"]:
        nodeDict[node["id"]] = node["globalid"]
      edgeDict = dict()
      for node in parsed["edges"]:
         if (nodeDict[node["source"]] not in edgeDict):
            edgeDict[nodeDict[node["source"]]] = [] 
         edgeDict[nodeDict[node["source"]]].append(nodeDict[node["target"]])
         print(edgeDict[nodeDict[node["source"]]])
 
process_temporal_data(['../DifferencesAsGraph.json']) 
