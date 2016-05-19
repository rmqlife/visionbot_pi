class Graph:
    def __init__(self):
        self.nodes = set()
        # dict https://docs.python.org/2/library/collections.html#collections.defaultdict
        self.edges = defaultdict(list)
        self.distances = {}
        
    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance
    
def distance(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1]) **2) **0.5

def gen_nodes(hlist,vlist):
    ps = set()
    for h in hlist:
        for v in vlist:
            p = (h,v)
            ps.add(p)
    return ps
    
def nearest(target_node,nodes):
    nearest_node = None
    min_dist = 10000
    for node in nodes:
        d = distance(node,target_node)
        if d<min_dist:
            min_dist = d
            nearest_node = node
    return nearest_node

def greedy_path(start,nodes):
    path = list()
    path.append(start)
    while len(nodes)>0 :
        nearest_node = nearest(start, nodes)
        path.append(nearest_node)
        nodes.remove(nearest_node)
        start = nearest_node    
    return path

if __name__ == "__main__":
    nodes = gen_nodes(range(0,180,20),range(90,180,20))
    path = greedy_path((90,90),nodes)
    print path
