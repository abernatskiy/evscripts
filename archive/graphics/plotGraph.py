#!/usr/bin/python2

annTopology = [4,-2,2]
inputAnnotations = ['<p<SUB>l</SUB>>', '<p<SUB>r</SUB>>', '<l<SUB>l</SUB>>', '<l<SUB>r</SUB>>']
outputAnnotations = ['m0', 'm1']

import pydot

graph = pydot.Dot(graph_type='digraph')

for iInNode in xrange(annTopology[0]):
	graph.add_node(pydot.Node('i'+str(iInNode), label=inputAnnotations[iInNode], shape='circle')) # http://www.graphviz.org/doc/info/attrs.html

graph.write_png('gr.png')
#graph.add_edge(pydot.Edge(node_a, node_b))
#graph.add_edge(pydot.Edge(node_b, node_c))
#graph.add_edge(pydot.Edge(node_c, node_d))
#graph.add_edge(pydot.Edge(node_d, node_a, label="and back we go again", labelfontcolor="#009933", fontsize="10.0", color="blue"))
