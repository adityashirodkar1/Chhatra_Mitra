import database as dbs

user = []
for i in dbs.users.find({}):
    user.append(i['_id'])

class Graph:
    def __init__(self):
        self.vertices = {}

    def get_node(self,vertex):
        return self.vertices[vertex]
        
    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices[vertex] = set()
            
    def add_edge(self, vertex1, vertex2 = "only one"):
        self.add_vertex(vertex1)
        if vertex2 != "only one":
            self.add_vertex(vertex2)
            self.vertices[vertex1].add(vertex2)
            self.vertices[vertex2].add(vertex1)

    def __str__(self):
        result = []
        for vertex in self.vertices:
            adjacent_vertices = ', '.join(self.vertices[vertex])
            result.append(f"{vertex}: {adjacent_vertices}")
        return '\n'.join(result)

graph = Graph()

if __name__ == "__main__":
    graph.add_edge(str(user[0]), str(user[1]))
    graph.add_edge(str(user[0]), str(user[2]))
    print(graph)
    print(type(graph))
    print(graph.get_node('6444ea701fd6e9522c2ee6d0'))


