#! /usr/bin/python
import math
import sys
import string
import time
import Gnuplot as gp
import random
import numpy

def iniciar_vertices(V,ancho,alto):
	pos = {}
	for v in V:
		pos[v] = (random.random()*ancho,random.random()*alto)
	return pos

def fa(x,k):
	return (x*x)/k
def fr(x,k):
	return (k*k)/x
def cool(t):
	if t > 1:
		return t - 0.2
	elif t > 0:
		return t - 0.1
	else:
		return 0

def modulo_vector(x,y):
	return math.sqrt((x)**2+(y)**2)

def run_layout(grafo,ancho,alto,M):
	(V,E) = grafo
	V = set(V)
	area = ancho*alto
	k = 0.6*math.sqrt(area/len(V))

	t = 50

	disp = {}
	for v in V:
		disp[v] = (0,0)

	pos = iniciar_vertices(V,ancho,alto)

	for i in range(0,M):
		#print "El valor de M es: %s",M
		for v in V:
			disp[v] = (0,0)
			# Fuerza repulsion
			for u in V:
				if (u != v):
					Delta = tuple(numpy.subtract(pos[v],pos[u]))
					x,y = Delta
					Modulo_Delta = modulo_vector(x,y)
					if Modulo_Delta == 0:
						#print "Error en repulsion"
						return(-1)
						
					Delta_sobre_modulo = tuple(d/Modulo_Delta for d in Delta)
					# aux = D/|D| * fr(|D|)
					aux = tuple(q*fr(Modulo_Delta,k) for q in Delta_sobre_modulo)
					# v.disp = v.disp + D/|D| * fr(|D|)
					disp[v] = tuple(numpy.add(disp[v],aux))

		# Fuerza atraccion.
		for (g,h) in E:
			Delta = tuple(numpy.subtract(pos[g],pos[h]))
			
			x,y = Delta
			Modulo_Delta = modulo_vector(x,y)
			
			if Modulo_Delta == 0:
				return(-1)
			Delta_sobre_modulo = tuple(float(d)/float(Modulo_Delta) for d in Delta)
			aux = tuple(p*fa(Modulo_Delta,k) for p in Delta_sobre_modulo)

			disp[g] = tuple(numpy.subtract(disp[g],aux))
			disp[h] = tuple(numpy.add(disp[h],aux))

		# Limitamos desplazamiento.
		for v in V:
			a,b = disp[v]
			displen = modulo_vector(a,b)
			if displen == 0:
				return(-1)
			aux = tuple( (dd/(displen)*t) for dd in disp[v])
			pos[v] = tuple(numpy.add(pos[v],aux))

			a,b = pos[v]

			pos[v] = (min(ancho/2,max(-ancho/2,a)),
				   min(alto/2,max(-alto/2,b)))
			
		t = cool(t)

	graficar(pos,V,E)



dibujar_vertice = 'set object %s circle center %s,%s size 5 fc rgb "black" fs solid border lc rgb "black" '
dibujar_arista = 'set arrow nohead from %s,%s to %s,%s filled back lw 2 lc rgb "black"'

def graficar(pos,V,E):
	g = gp.Gnuplot()
	g('set terminal wxt size 1000,550')
	g('set terminal wxt persist')
	g('set terminal wxt noraise')
	g('set key off')
	g('set terminal wxt background "white"')
#	g('set title "FR"')
	g('unset xtics')
	g('unset ytics')
	g('unset border')
	g('unset key')
	g('set xrange [-100:700]; set yrange [-250:350]')

	# Dibujamos vertices
	id_vertice = 1
	for v in V:
		x,y = pos[v]
		cmd = (dibujar_vertice) % (id_vertice,x,y)
		g(cmd)
		id_vertice += 1
	# Dibujamos aristas
	for ar in E:
		a,b = pos[ar[0]]
		c,d = pos[ar[1]]
		cmd = (dibujar_arista) % (a,b,c,d)
		g(cmd)
	g('plot NaN')

def lee_grafo_archivo(file_path):
	count = 0
	with open(file_path,'r') as f:
		cantidad = int(f.readline())
		
		Vertices = []
		for i in range(0,cantidad):
			elem = f.readline().strip()
			Vertices.append(elem)
		
		Aristas = []
		for line in f:
			elem = line.strip().split()
			Aristas.append(tuple(elem))

	G = (Vertices,Aristas)

	return G

def main():
	if len(sys.argv) < 2:
		print 'Uso: python gg.py <archivo>'
		return

	G = lee_grafo_archivo(sys.argv[1])
	dibujar = run_layout(G,1000,550,250)

	while dibujar == -1:
		dibujar = run_layout(G,1000,550,250)


if __name__ == '__main__':
	main()
