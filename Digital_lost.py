class Matrix:
    def __init__(self, grid):
        self.n = len(grid)
        self.grid = grid
        self.visited = [[0 for j in range(self.n)] for i in range(self.n)]
        self.number = {}
        self.candi = set()
    
    def build(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j]!=0:
                    self.number[self.grid[i][j]] = (i, j)
                    self.visited[i][j] = 1
        for num in self.number:
            if num - 1 not in self.number and num!=1:
                self.candi.add(num-1)
            if num + 1 not in self.number and num!=self.n*self.n:
                self.candi.add(num+1)
        self.opts = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)]
    
    def run_model(self):
        self.build()
        f = self.solve()
        for i in range(1, self.n*self.n+1):
            x, y = self.number[i]
            self.grid[x][y] = i
    
    def get_candi_position(self, key):
        res = set()
        x, y = self.number[key]
        for op in self.opts:
            nx ,ny = x+op[0], y+op[1]
            if nx>=0 and nx<self.n and ny>=0 and ny<self.n and self.visited[nx][ny]==0:
                res.add((nx, ny))
        return res
    
    def solve(self):
        if not self.candi:
            return True
        item = list(self.candi)[-1]
        self.candi.remove(item)
        adj_position = set()
        nei1 = set()
        nei2 = set()
        if item + 1 in self.number:
            nei1 = self.get_candi_position(item+1)
        if item - 1 in self.number:
            nei2 = self.get_candi_position(item-1)
        if item + 1 in self.number and item - 1 in self.number:
            adj_position = nei1.intersection(nei2)
        elif item + 1 in self.number:
            adj_position = nei1
        elif item - 1 in self.number:
            adj_position = nei2
        for x, y in adj_position:
            self.number[item] = (x, y)
            self.visited[x][y] = 1
            n1 = False
            n2 = False
            if item + 1 not in self.number and item+1<=self.n*self.n:
                if item+1 not in self.candi:
                    self.candi.add(item+1)
                    n1 = True
            if item - 1 not in self.number and item-1>=1:
                if item-1 not in self.candi:
                    self.candi.add(item-1)
                    n2 = True
            if self.solve():
                return True
            del self.number[item]
            self.visited[x][y] = 0
            if n1:
                self.candi.remove(item+1)
            if n2:
                self.candi.remove(item-1)
        self.candi.add(item)
        return False

    def __str__(self):
        s = []
        for i in range(self.n):
            s_t = ""
            for j in range(self.n):
                s_t += "{:<5}".format(self.grid[i][j])
            s_t += "\n"
            s.append(s_t)
        return "\n".join(s)

grid = [[37,0,41,0,0,0,49],[0,0,40,0,44,0,0],[35,33,0,0,0,8,0],[0,0,0,1,0,9,0],[30,25,4,0,0,0,0],[0,0,0,0,16,0,13],[0,27,0,22,0,0,14]]
m = Matrix(grid)
m.run_model()
print(m)
