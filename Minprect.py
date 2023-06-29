#include <cmath>
#include <iostream>

import pandas as pd
import math
import matplotlib.pyplot as plt
import time
from matplotlib.patches import Rectangle, Circle

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node:
    def __init__(self, pos: Point, data, poblacion: float):
        self.pos = pos
        self.data = data
        self.poblacion = poblacion

class Quad:
    def __init__(self, topLeft: Point, botRight: Point):
        self.topLeft = topLeft
        self.botRight = botRight
        self.n = None
        self.topLeftTree = None
        self.topRightTree = None
        self.botLeftTree = None
        self.botRightTree = None

    def insert(self, node: Node):
        if node is None:
            return 

        if not self.inBoundary(node.pos):
            return 

        if abs(self.topLeft.x - self.botRight.x) <= 1 and abs(self.topLeft.y - self.botRight.y) <= 1:
            if self.n is None:
                self.n = node
            return

        if (self.topLeft.x + self.botRight.x) / 2 >= node.pos.x:
            if (self.topLeft.y + self.botRight.y) / 2 >= node.pos.y:
                if self.topLeftTree is None:
                    self.topLeftTree = Quad(self.topLeft, Point((self.topLeft.x + self.botRight.x) / 2, (self.topLeft.y + self.botRight.y) / 2))
                self.topLeftTree.insert(node)
            else:
                if self.botLeftTree is None:
                    self.botLeftTree = Quad(Point(self.topLeft.x, (self.topLeft.y + self.botRight.y) / 2), Point((self.topLeft.x + self.botRight.x) / 2, self.botRight.y))
                self.botLeftTree.insert(node)
        else:
            if (self.topLeft.y + self.botRight.y) / 2 >= node.pos.y:
                if self.topRightTree is None:
                    self.topRightTree = Quad(Point((self.topLeft.x + self.botRight.x) / 2, self.topLeft.y), Point(self.botRight.x, (self.topLeft.y + self.botRight.y) / 2))
                self.topRightTree.insert(node)
            else:
                if self.botRightTree is None:
                    self.botRightTree = Quad(Point((self.topLeft.x + self.botRight.x) / 2, (self.topLeft.y + self.botRight.y) / 2), self.botRight)
                self.botRightTree.insert(node)

    def search(self, p: Point):
        if not self.inBoundary(p):
            return None
        if self.n is not None:
            return self.n.data
        if (self.topLeft.x + self.botRight.x) / 2 >= p.x:
            if (self.topLeft.y + self.botRight.y) / 2 >= p.y:
                if self.topLeftTree is None:
                    return None
                return self.topLeftTree.search(p)
            else:
                if self.botLeftTree is None:
                    return None
                return self.botLeftTree.search(p)
        else:
            if (self.topLeft.y + self.botRight.y) / 2 >= p.y:
                if self.topRightTree is None:
                    return None
                return self.topRightTree.search(p)
            else:
                if self.botRightTree is None:
                    return None
                return self.botRightTree.search(p)

    def inBoundary(self, p: Point):
        return p.x >= self.topLeft.x and p.x <= self.botRight.x and p.y >= self.topLeft.y and p.y <= self.botRight.y
    
    def totalPoints(self):
        count = 0
        if self.n is not None:
            count += 1
        if self.topLeftTree is not None:
            count+= self.topLeftTree.totalPoints()
        if self.topRightTree is not None:
            count+= self.topRightTree.totalPoints()
        if self.botLeftTree is not None:
            count+= self.botLeftTree.totalPoints()
        if self.botRightTree is not None:
            count+= self.botRightTree.totalPoints()

        return count
    
    def totalNodes(self):
        countnod = 1  # Inicializar con 1 para contar el nodo actual

        if self.topLeftTree is not None:
            countnod += self.topLeftTree.totalNodes()
        if self.topRightTree is not None:
            countnod += self.topRightTree.totalNodes()
        if self.botLeftTree is not None:
            countnod += self.botLeftTree.totalNodes()
        if self.botRightTree is not None:
            countnod += self.botRightTree.totalNodes()

        return countnod

    def inRegion(self, p: Point, d: int) -> bool:
        # Calcula los límites de la región
        minX = p.x - d
        maxX = p.x + d
        minY = p.y - d
        maxY = p.y + d

        # Comprueba si los límites de la región intersectan con los límites del nodo actual
        return not (minX > self.botRight.x or maxX < self.topLeft.x or minY > self.botRight.y or maxY < self.topLeft.y)

    def countRegion(self, p: Point, d: int) -> int:
        countreg = 0
        
        # Verificar si el nodo actual está dentro de la región
        if self.inRegion(p, d):
            if self.n is not None:
                countreg += 1
    
            # Contar los puntos en los subárboles recursivamente
            if self.topLeftTree is not None:
                countreg += self.topLeftTree.countRegion(p, d)
            if self.topRightTree is not None:
                countreg += self.topRightTree.countRegion(p, d)
            if self.botLeftTree is not None:
                countreg += self.botLeftTree.countRegion(p, d)
            if self.botRightTree is not None:
                countreg += self.botRightTree.countRegion(p, d)
        
        return countreg
    
    def AggregateRegion(self, p: Point, d: int):
        population = 0
        
        # Verificar si el nodo actual está dentro de la región
        if self.inRegion(p, d):
            if self.n is not None:
                population += self.n.poblacion  # Agregar la poblacion acumulada en el nodo actual

            # Sumar la poblacion en los subárboles recursivamente
            if self.topLeftTree is not None:
                population += self.topLeftTree.AggregateRegion(p, d)
            if self.topRightTree is not None:
                population += self.topRightTree.AggregateRegion(p, d)
            if self.botLeftTree is not None:
                population += self.botLeftTree.AggregateRegion(p, d)
            if self.botRightTree is not None:
                population += self.botRightTree.AggregateRegion(p, d)
        
        return population
    def inorder(self):
        point_list = []

        if self.topLeftTree is not None:
            point_list.extend(self.topLeftTree.inorder())
        if self.n is not None:
            point_list.append((self.n.pos.x, self.n.pos.y, self.n.data, self.n.poblacion))
        if self.topRightTree is not None:
            point_list.extend(self.topRightTree.inorder())
        if self.botLeftTree is not None:
            point_list.extend(self.botLeftTree.inorder())
        if self.botRightTree is not None:
            point_list.extend(self.botRightTree.inorder())

        return point_list
    
    def list(self):
        point_list = quadtree.inorder()
        print("Puntos almacenados en el Quadtree:")
        for point in point_list:
            print("Coordenadas:", point[0], ",", point[1])
            print("Valor asociado:", point[2])
            print("Población:", point[3])
            print()

    class Rectangle:
        def __init__(self, topLeft: Point, botRight: Point):
            self.topLeft = topLeft
            self.botRight = botRight
    
# Driver program

#LaQuadtree = Quad(Point(0, 0), Point(8, 8))
#a = Node( Point(1,1), 5)
#b = Node( Point(2,5), 2)
#c = Node( Point(1,5), 7)
#LaQuadtree.insert(a)
#LaQuadtree.insert(b)
#LaQuadtree.insert(c)
#result = LaQuadtree.search(Point(1,1))
#print("Node a: ", result)
#print("Total de puntos: ", LaQuadtree.totalPoints())
#regionCount = LaQuadtree.countRegion(Point(1, 1), 1)
#print("Cantidad de puntos en la región: ", regionCount)

df = pd.read_csv('E:\Programas_C_C++_java\Laboratorios\Miniproyecto 2\MiniProyecto-2\worldcitiespop_fixed.csv', sep=";")
df['Longitude'] = df['Longitude'].str.replace(',', '.').astype(float)
df['Latitude'] = df['Latitude'].str.replace(',', '.').astype(float)

#Extraer columnas coordenadas
latitudemaxvalue = df['Latitude'].values
longitudemaxvalue = df['Longitude'].values

#Encontrar los valores maximos y minimos de latitude y longitude
min_latitude = min(latitudemaxvalue)
max_latitude = max(latitudemaxvalue)
min_longitude = min(longitudemaxvalue)
max_longitude = max(longitudemaxvalue)

expansion_factor = 1.2

# Calcular el rango ampliado
range_latitude = max_latitude - min_latitude
range_longitude = max_longitude - min_longitude
expanded_range_latitude = range_latitude * expansion_factor
expanded_range_longitude = range_longitude * expansion_factor

# Calcular los límites ampliados del Quadtree
expanded_min_latitude = min_latitude - expanded_range_latitude/2
expanded_max_latitude = max_latitude + expanded_range_latitude/2
expanded_min_longitude = min_longitude - expanded_range_longitude/2
expanded_max_longitude = max_longitude + expanded_range_longitude/2

# Crear el Quadtree con los límites ampliados
quadtree = Quad(topLeft=Point(expanded_min_longitude, expanded_min_latitude), botRight=Point(expanded_max_longitude, expanded_max_latitude))

country_values = df['Country'].values
city_values = df['City'].values
accentcity_values = df["AccentCity"].values
region_values = df['Region'].values
population_values = df['Population'].values
latitude_values = df['Latitude'].values
longitude_values = df['Longitude'].values
geopoint_values = df['geopoint'].values

#quadtree = Quad(topLeft=Point(min_longitude, min_latitude), botRight=Point(max_longitude, max_latitude))

quadtree = Quad(topLeft=Point(expanded_min_longitude, expanded_min_latitude), botRight=Point(expanded_max_longitude, expanded_max_latitude))
#quadtree = Quad(Point(0,0),Point(500,300))
def function():
    pass

start_time = time.time()

for country, city, region, latitude, longitude, geopoint, accentcity, population in zip(country_values, city_values, region_values, latitude_values, longitude_values, geopoint_values, accentcity_values, population_values):
    point = Point(float(longitude), float(latitude))
    poblacion = float(population)
    valores = {
        'Country': country,
        'City': city,
        'AccentCity': accentcity,
        'Region': region,
        'geopoint': geopoint
    }
    node = Node(point, valores, poblacion)
    quadtree.insert(node)

end_time = time.time()


print('Execution time: {} seconds'.format(end_time - start_time ))