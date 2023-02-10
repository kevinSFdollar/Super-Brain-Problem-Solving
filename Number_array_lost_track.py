from collections import defaultdict
from math import gcd


class Vertex:
    def __init__(self, val, id):
        self.val = val
        self.id = id
        self.degree = 0

class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    
    def set_score(self, graph):
        self.score = graph.vertex_set[self.v1].degree + graph.vertex_set[self.v2].degree

class Graph:
    def __init__(self, grid):
        self.n = len(grid)
        self.grid = grid
        self.vertex_set = {}
        self.edge_set = []
        self.edge_is_remove = []
        self.edge_visited = []
    
    def convert_edge_set(self):
        self.adj_map = defaultdict(list)
        for i in range(self.edge_num):
            if self.edge_is_remove[i] == 0:
                edge = self.edge_set[i]
                v1 = edge.v1
                v2 = edge.v2
                self.adj_map[v1].append(v2)
                self.adj_map[v2].append(v1)
    
    def query_linked(self, i, j, d=0):
        v1 = self.get_vertex_id(i, j)
        if d==0:
            v2 = self.get_vertex_id(i, j+1)
        else:
            v2 = self.get_vertex_id(i+1, j)
        return v2 in self.adj_map[v1]

    def get_vertex_id(self, i, j):
        id = i * self.n + j
        return id

    def build_graph(self):
        for i in range(self.n):
            for j in range(self.n):
                v1 = self.get_vertex_id(i, j)
                if v1 in self.vertex_set:
                    ver1 = self.vertex_set[v1]
                else:
                    ver1 = Vertex(self.grid[i][j], v1)
                    self.vertex_set[v1] = ver1
                if j != self.n - 1:
                    v2 = self.get_vertex_id(i, j+1)
                    if v2 in self.vertex_set:
                        ver2 = self.vertex_set[v2]
                    else:
                        ver2 = Vertex(self.grid[i][j+1], v2)
                        self.vertex_set[v2] = ver2
                    if gcd(ver1.val, ver2.val) > 1:
                        e = Edge(v1, v2)
                        self.edge_set.append(e)
                        ver1.degree += 1
                        ver2.degree += 1
                if i != self.n - 1:
                    v2 = self.get_vertex_id(i+1, j)
                    if v2 in self.vertex_set:
                        ver2 = self.vertex_set[v2]
                    else:
                        ver2 = Vertex(self.grid[i+1][j], v2)
                        self.vertex_set[v2] = ver2
                    if gcd(ver1.val, ver2.val) > 1:
                        e = Edge(v1, v2)
                        self.edge_set.append(e)
                        ver1.degree += 1
                        ver2.degree += 1
    
    def rank_edge(self):
        for e in self.edge_set:
            e.set_score(self)
        self.edge_set.sort(key=lambda e: e.score)

    def dfs(self):
        self.rank_edge()
        self.edge_num = len(self.edge_set)
        self.edge_is_remove = [0 for i in range(self.edge_num)]
        self.current_degree = [0, 0, 0, 0, 0]
        for ver in self.vertex_set.values():
            d = ver.degree
            self.current_degree[d] += 1
        self.solve(0)
    
    def remove_edge(self, e):
        ver1, ver2 = self.vertex_set[e.v1], self.vertex_set[e.v2]
        self.current_degree[ver1.degree] -= 1
        self.current_degree[ver2.degree] -= 1
        self.current_degree[ver1.degree - 1] += 1
        self.current_degree[ver2.degree - 1] += 1
        ver1.degree -= 1
        ver2.degree -= 1
    
    def add_edge(self, e):
        ver1, ver2 = self.vertex_set[e.v1], self.vertex_set[e.v2]
        self.current_degree[ver1.degree] -= 1
        self.current_degree[ver2.degree] -= 1
        self.current_degree[ver1.degree + 1] += 1
        self.current_degree[ver2.degree + 1] += 1
        ver1.degree += 1
        ver2.degree += 1
    
    def is_connet(self):
        father = [i for i in range(self.n*self.n)]
        size = [1 for i in range(self.n*self.n)]
        def find(x):
            if father[x] != x:
                father[x] = find(father[x])
            return father[x]
        def union(v_1, v_2):
            f_v1 = find(v_1)
            f_v2 = find(v_2)
            if f_v1 != f_v2:
                if size[f_v1] >= size[f_v2]:
                    father[f_v2] = f_v1
                    size[f_v1] += size[f_v2]
                else:
                    father[f_v1] = f_v2
                    size[f_v2] += size[f_v1]
        for i in range(self.edge_num):
            if self.edge_is_remove[i] == 0:
                edge = self.edge_set[i]
                v1 = edge.v1
                v2 = edge.v2
                union(v1, v2)
        for i in range(self.n*self.n):
            if find(i) != father[0]:
                return False
        return True
    
    def solve(self, index):
        if self.current_degree[1] == 2 and self.current_degree[2] == self.n*self.n-2 and self.is_connet():
            return True
        if index == self.edge_num or self.current_degree[0] > 0 or self.current_degree[1] > 2:
            return False
        self.edge_is_remove[index] = 1
        self.remove_edge(self.edge_set[index])
        if self.solve(index + 1):
            return True
        self.edge_is_remove[index] = 0
        self.add_edge(self.edge_set[index])
        return self.solve(index + 1)
    

class Matrix:
    def __init__(self, grid):
        self.n = len(grid)
        self.grid = grid
        self.graph = Graph(grid)
    
    def run_model(self):
        self.graph.build_graph()
        self.graph.dfs()
        self.graph.convert_edge_set()
    
    def __str__(self):
        s = []
        for i in range(self.n - 1):
            s_t_1 = ""
            s_t_2 = ""
            for j in range(self.n - 1):
                s_t_1 += "{:>03}".format(self.grid[i][j])
                if self.graph.query_linked(i, j, 0):
                    s_t_1 += "——"
                else:
                    s_t_1 += "  "
                if self.graph.query_linked(i, j, 1):
                    s_t_2 += "{:<5}".format(" |")
                else:
                    s_t_2 += "{:<5}".format("")
            if self.graph.query_linked(i, self.n - 1, 1):
                    s_t_2 += "{:<5}".format(" |")
            s_t_1 += "{:>03}".format(self.grid[i][self.n - 1])
            s.append(s_t_1)
            s.append(s_t_2)
        s_t = ""
        for j in range(self.n - 1):
            s_t += "{:>03}".format(self.grid[self.n - 1][j])
            if self.graph.query_linked(self.n - 1, j, 0):
                s_t += "——"
            else:
                s_t += "  "
        s_t += "{:>03}".format(self.grid[self.n - 1][self.n - 1])
        s.append(s_t)
        res = "\n".join(s)
        return res

grid = [[118,106,148,16,22], [177,159,111,188,24],\
[21,42,171,133,10], [12,18,74,14,4],[26,54,57,66,8]]

m = Matrix(grid)
m.run_model()
print(m)
