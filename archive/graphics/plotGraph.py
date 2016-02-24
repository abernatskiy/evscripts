#!/usr/bin/python2

annTopology = [4,-2,2]
inputAnnotations = ['<p<SUB>l</SUB>>', '<p<SUB>r</SUB>>', '<l<SUB>l</SUB>>', '<l<SUB>r</SUB>>']
outputAnnotations = ['<m<SUB>0</SUB>>', '<m<SUB>1</SUB>>']

import numpy as np
import pydot

def getNumLinks(topology):
	if topology != []:
		acc = 0
		for iLayer in range(len(topology)-1):
			acc += abs(topology[iLayer])*abs(topology[iLayer+1])
			if topology[iLayer+1] < 0:
				acc += abs(topology[iLayer+1])*abs(topology[iLayer+1])
		return acc
	else:
		return None

def getWeights(netdesc, topol):
	links = []
	curpos = 0
	for iLayer in range(len(topol)-1):
		inNeu = abs(topol[iLayer])
		outNeu = abs(topol[iLayer+1])
		curordinary = np.array(netdesc[curpos:(curpos+inNeu*outNeu)])
		curordinary = curordinary.reshape(inNeu, outNeu)
		curpos += inNeu*outNeu
		if topol[iLayer+1] < 0:
			curhidden = np.array(netdesc[curpos:(curpos+outNeu*outNeu)])
			curhidden = curhidden.reshape(outNeu, outNeu)
			curpos += outNeu*outNeu
		else:
			curhidden = None
		links.append((curordinary, curhidden))
	return links

def printWeights(nwWeights):
	counter = 0
	for wgts, hwgts in nwWeights:
		counter += 1
		print('Layer %02d' % counter + ':')
		print('\n' + repr(wgts))
		print('\n' + repr(hwgts))
	print('')

import sys
numLinks = getNumLinks(annTopology)
while True:
	mline = sys.stdin.readline()
	if not mline:
		break
	if mline[0] == '#':
		continue

	fields = mline.split()
	nwDesc = map(float, fields[-1*numLinks:])
	nwID = int(fields[-1*(numLinks+1)])
	nwMetadata = fields[:-1*(numLinks+1)]

	nwWeights = getWeights(nwDesc, annTopology)

	print('ID' + str(nwID))
	printWeights(nwWeights)

	graph = pydot.Dot(graph_type='digraph')

	for iInNode in range(annTopology[0]):
		graph.add_node(pydot.Node('i'+str(iInNode), label=inputAnnotations[iInNode], shape='circle')) # http://www.graphviz.org/doc/info/attrs.html

	for iLayer in range(1, len(annTopology)-1):
		for iNode in range(annTopology[iLayer]):
			graph.add_node(pydot.Node('h'+str(iNode)+'_'+str(iLayer), shape='circle'))
			for iUpperNode in range(annTopology[iLayer-1]):
				graph.add_edge(pydot.Edge())

			graph.add_node(pydot.Node('i'+str(iNode), shape='circle')) # http://www.graphviz.org/doc/info/attrs.html

graph.write_png('gr.png')
'''

#graph.add_edge(pydot.Edge(node_a, node_b))
#graph.add_edge(pydot.Edge(node_b, node_c))
#graph.add_edge(pydot.Edge(node_c, node_d))
#graph.add_edge(pydot.Edge(node_d, node_a, label="and back we go again", labelfontcolor="#009933", fontsize="10.0", color="blue"))

