#!/usr/bin/python3
# -*- coding: utf-8 -*-
import math
import random
from sklearn.metrics.cluster import adjusted_rand_score

#########################################
# Dado de entrada
#########################################
class Objeto():
	def __init__(self, nome, x, y):
		self.nome = nome
		self.x = x
		self.y = y
		self.cluster = -1

	# Retorna a representação do objeto como string
	def __repr__(self):
		return(str(self.nome) + " " + str(self.x) + " " + str(self.y) + " " + str(self.cluster))

	# Retorna a reprentação em string para escrever no arquivo e saida
	def saida(self):
		return(str(self.nome) + " " + str(self.cluster))

	# Retorna a distancia do objeto com outro ponto
	def distancia(self, x, y):
		dx = self.x - x
		dy = self.y - y

		return math.sqrt( dx ** 2 + dy ** 2 )

#########################################
# Lê arquivos de entrada
#########################################
# Realiza a leitura do conjunto de dados do arquivo entrada
def lerConjuntoDeDados(caminho, conjuntoDados):
	with open(caminho) as arq:
		cabecalho = arq.readline()

		for linha in arq:
			valores = linha.split()
			#print(valores)
			conjuntoDados.append( Objeto(valores[0], float(valores[1]), float(valores[2])) )

# Realiza a leitura do arquivo com os valores corretos das classes
def lerConjuntoDadosReal(caminho, conjuntoDadosReal):
	with open(caminho) as arq:

		for linha in arq:
			valores = linha.split()
			#print(valores)
			conjuntoDadosReal.append( (valores[0], float(valores[1]))  )

#########################################
# Escreve arquivo de saida
#########################################
# Escreve os objetos da partão no arquivo de saida
def escreveParticaoArquivo(caminho, conjuntoDadosReal):
	with open(caminho, 'w') as arq:
		for dado in conjuntoDadosReal:
			arq.write(dado.saida() + "\n")


#########################################
# Calcula a distancia entre cada Objeto
#########################################
def calcularDistanciasEntreObjetos(tabela, conjuntoDados):
	for i in range(len(conjuntoDados)):
		for j in range(len(conjuntoDados)-i):
			#print("[{}][{}]".format(i, i+j))

			if i != j:
				distancia = conjuntoDados[i].distancia(conjuntoDados[i+j].x, conjuntoDados[i+j].y)
				tabela[i][i+j] = distancia
				tabela[i+j][i] = distancia


#########################################
# Calcula a distancia entre cada Cluster
# Retorna a menor distancia 
#########################################
def calcularDistanciaEntreClusters(cluster1, cluster2):
	indiceObjetoCluster1 = 0 
	indiceObjetoCluster2 = 0 
	menorDistancia = 9999999999999

	for indice1, objeto1 in enumerate(cluster1):
		for indice2, objeto2 in enumerate(cluster2):
			distancia = objeto1.distancia(objeto2.x, objeto2.y)
			
			if distancia < menorDistancia:
				indiceObjetoCluster1 = indice1
				indiceObjetoCluster2 = indice2
				menorDistancia = distancia

	return menorDistancia


#########################################
# Encontra os clusters mais próximos
# Retorna o indice dos cluster mais 
# próximos
#########################################
def clustersMaisProximos(clusters, tabela):
	cluster1 = 0
	cluster2 = 0
	menorDistancia = 99999999999

	for i in range(len(clusters)):
		for j in range(len(clusters)-i):
			#print("[{}][{}]".format(i, j))

			distancia = calcularDistanciaEntreClusters(clusters[i], clusters[j])
			#print(distancia)
			if i != j:
				if distancia < menorDistancia:
					cluster1 = i
					cluster2 = j
					menorDistancia = distancia

	return cluster1, cluster2, menorDistancia



#########################################
# Lê entrada e executa o agrupamento
#########################################
def main():

	kmin = int(input("Digite o kmin"))
	kmax = int(input("Digite o kmax"))

	conjuntoDadosReal = []
	lerConjuntoDadosReal('../datasets/c2ds1-2spReal.clu', conjuntoDadosReal)

	conjuntoDados = []
	lerConjuntoDeDados('../datasets/c2ds1-2sp.txt', conjuntoDados);
	
	
	conjuntoDados = [
		Objeto("c2sp1s1", 10.5, 9),
		Objeto("c2sp1s2", 10.56717, 9.268445),
		Objeto("c2sp1s3", 8.27532, 11.38221),
		Objeto("c2sp1s4", 8.227458, 11.37764),
		Objeto("c2sp1s5", 8.179511, 11.37211),
		Objeto("c2sp1s6", 8.1315, 11.36561),
		Objeto("c2sp1s7", 8.083443, 11.35814),
		Objeto("c2sp1s8", 8.035361, 11.3497),
		Objeto("c2sp1s9", 7.98727, 11.34027),
		Objeto("c2sp1s10", 7.9392, 11.32987)
	]
	

	# Coloca cada um dos objetos em um partição separada
	clusters = []
	for objeto in conjuntoDados:
		clusters.append([objeto])


	# Criar tabela com distâncias
	tabela = []

	for i in range(len(conjuntoDados)):
		tabela.append([])
		for j in range(len(conjuntoDados)):
			tabela[i].append(0)
	
	calcularDistanciasEntreObjetos(tabela, conjuntoDados)

	# Continua a executar até ter somente duas partições
	while True:

		print(len(clusters))
		if len(clusters) >= kmin and len(clusters) <= kmax:
			for indice, cluster in enumerate(clusters):
				for objeto in cluster:
					objeto.cluster = indice

			escreveParticaoArquivo('c2ds1-2spK' + str(len(clusters)) + '.txt', conjuntoDados)

		# Obtém clusters mais próximos e faz merge deles
		indiceCluster1, indiceCluster2, distancia = clustersMaisProximos(clusters, tabela)
		clusters[indiceCluster1].extend(clusters[indiceCluster2])
		del clusters[indiceCluster2]

		# Quando tiver 2 clusters calcula o indice rand
		if len(clusters) == 2:
			# vetor de resultados para calcula AR
			resultado = []
			for dado in conjuntoDados:
				resultado.append(dado.cluster)

			# vetor com os valores esperados para calcular AR
			esperado = []
			for dado in conjuntoDadosReal:
				esperado.append(int(dado[1]))

			# calcula Ar
			indiceRand = adjusted_rand_score(resultado, esperado)
			print("AR: " + str(indiceRand))
			escreveParticaoArquivo('c2ds1-2spK' + str(len(clusters)) + '.txt', conjuntoDados)
			break

if __name__ == "__main__":
    main()