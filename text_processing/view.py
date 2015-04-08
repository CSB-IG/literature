import networkx as nx
from nodebox.graphics import *
from nodebox.graphics.physics import Node, Edge, Graph
import argparse

parser = argparse.ArgumentParser(description='Interactive view of network')
parser.add_argument('--pickle', type=argparse.FileType('r'), required=True )
args   = parser.parse_args()

h = nx.read_gpickle( args.pickle )

g = Graph()

for e in h.edges():
    g.add_edge(e[0], e[1], 
               length = 0.2, 
               weight = 0.2, 
               stroke = color(.5,.5,.6))


g.distance         = 22   # Overall spacing between nodes.
g.layout.force     = 0.0009 # Strength of the attractive & repulsive force.
g.layout.repulsion = 12   # Repulsion radius.

dragged = None
def draw(canvas):
    
    canvas.clear()
    background(color(0.35,.35,.45))
    translate(250, 250)
    
    # With directed=True, edges have an arrowhead indicating the direction of the connection.
    # With weighted=True, Node.centrality is indicated by a shadow under high-traffic nodes.
    # With weighted=0.0-1.0, indicates nodes whose centrality > the given threshold.
    # This requires some extra calculations.
    g.draw(weighted=True, directed=False)
    g.update(iterations=3)
    
    # Make it interactive!
    # When the mouse is pressed, remember on which node.
    # Drag this node around when the mouse is moved.
    dx = canvas.mouse.x - 250 # Undo translate().
    dy = canvas.mouse.y - 250
    global dragged
    if canvas.mouse.pressed and not dragged:
        dragged = g.node_at(dx, dy)
    if not canvas.mouse.pressed:
        dragged = None
    if dragged:
        dragged.x = dx
        dragged.y = dy
        
canvas.size = 1280, 800
canvas.run(draw)
