#!/usr/bin/python
# Copyright (c) 2008, Matt Sparks
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY MATT SPARKS ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL MATT SPARKS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""Graph RFCs (Request for Comments) and their relationships

For usage, see: ./rfcgraph.py -h
"""
import optparse
import os
import re
import sys
from xml.dom import minidom

import pydot

__author__ = "Matt Sparks"
__license__ = "BSD"


def _extract_ids(element):
  values = []
  if element is None:
    return values
  elements = element.getElementsByTagName("doc-id")
  for id_elem in elements:
    values.append(id_elem.firstChild.nodeValue)
  return values


def _extract_and_filter(rfc, element_name):
  element_list = rfc.getElementsByTagName(element_name)
  if not element_list:
    return []
  return filter(lambda x: x.startswith("RFC"), _extract_ids(element_list[0]))


def extract_metadata(index_file):
  """Parse the given XML file and generate RFC relationships.

  Args:
    index_file: RFC index XML file (http://www.rfc-editor.org)

  Returns:
    dictionary of dictionaries, keyed by RFC ID (RFC####)
  """
  dom1 = minidom.parse(index_file)
  rfcs = dom1.getElementsByTagName("rfc-entry")
  metadata = {}
  for rfc in rfcs:
    id = _extract_ids(rfc)[0]
    title = rfc.getElementsByTagName("title")[0].firstChild.nodeValue
    obsoleted_by = _extract_and_filter(rfc, "obsoleted-by")
    updated_by = _extract_and_filter(rfc, "updated-by")

    metadata[id] = {"title": title,
                    "obsoleted_by": obsoleted_by,
                    "updated_by": updated_by}

  return metadata


def _make_nodes(metadata):
  nodes = {}
  ids = metadata.keys()
  ids.sort()
  for id in ids:
    url = "http://www.ietf.org/rfc/%s.txt" % id.lower()
    node = pydot.Node(id, href=url)
    nodes[id] = node
  return nodes


def _add_node(graph, nodes, id):
  if graph.get_node(id):
    return
  graph.add_node(nodes[id])


def _add_nodes(metadata, graph, nodes):
  for id in metadata.keys():
    ob_by = metadata[id]["obsoleted_by"]
    up_by = metadata[id]["updated_by"]
    if not ob_by and not up_by:
      continue  # ignore isolated rfcs for now

    _add_node(graph, nodes, id)
    for ob in ob_by:
      _add_node(graph, nodes, ob)
      graph.add_edge(pydot.Edge(id, ob, color="red"))
    for up in up_by:
      _add_node(graph, nodes, up)
      graph.add_edge(pydot.Edge(id, up, color="green"))


def create_graph(metadata, output_file, format):
  """Create the RFC relationship graph from metadata.

  Args:
    metadata: metadata in the format from extract_metadata()
    output_file: file to write
    format: format to use for writing
  """
  graph = pydot.Dot(graph_name="RFCs", type="digraph")
  nodes = _make_nodes(metadata)
  _add_nodes(metadata, graph, nodes)
  graph.set("overlap", "false")
  graph.set("href", "http://quadpoint.org")
  graph.write(output_file, format=format, prog="neato")


def main():
  parser = optparse.OptionParser()
  parser.add_option("-i", "--file", dest="index_file",
                    help="RFC index (.xml) (default: rfc-index.xml)",
                    metavar="FILE", default="rfc-index.xml")
  parser.add_option("-o", "--output_file", dest="output_file",
                    help="Output filename (default: rfcs.ps)",
                    metavar="FILE", default="rfcs.ps")
  parser.add_option("-f", "--format", dest="format",
                    help="Output file format (ps2, png, ...) (default: ps2)",
                    metavar="FORMAT", default="ps2")
  (options, args) = parser.parse_args()

  index_file = options.index_file
  output_file = options.output_file
  format = options.format

  print "Reading XML..."
  metadata = extract_metadata(index_file)
  print "Creating graph..."
  create_graph(metadata, output_file, format)


if __name__ == "__main__":
  main()
