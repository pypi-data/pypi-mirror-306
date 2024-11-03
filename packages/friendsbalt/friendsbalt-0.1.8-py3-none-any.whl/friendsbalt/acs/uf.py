class QuickFind:
    def __init__(self, N):
        self.id = list(range(N))

    def connected(self, p, q):
        return self.id[p] == self.id[q]

    def union(self, p, q):
        pid = self.id[p]
        qid = self.id[q]
        for i in range(len(self.id)):
            if self.id[i] == pid:
                self.id[i] = qid

class QuickUnion:
    def __init__(self, N):
        self.id = list(range(N))

    def root(self, i):
        while i != self.id[i]:
            i = self.id[i]
        return i

    def connected(self, p, q):
        return self.root(p) == self.root(q)

    def union(self, p, q):
        i = self.root(p)
        j = self.root(q)
        self.id[i] = j


class WeightedQuickUnion:
    """
    A data structure for union-find with weighted quick union.

    This class implements the union-find algorithm with path compression
    and weighting to ensure efficient union and find operations.

    Attributes:
        id (list): The list to hold the parent of each element.
        sz (list): The list to hold the size of each tree.
        count (int): The number of components.

    Methods:
        __init__(N):
            Initializes the UF object with N elements.
        root(i):
            Finds the root of the element at index i in the Union-Find data structure.
        connected(p, q):
            Determines whether two elements are connected in the union-find data structure.
        union(p, q):
            Unites two elements by connecting their roots.
        size(i):
            Returns the size of the component that the element 'i' belongs to.
        count():
            Returns the number of components in the union-find data structure.
    """
    def __init__(self, N):
        """
        Initializes the UF object with N elements.

        Parameters:
        - N (int): The number of elements in the UF object.

        Returns:
        None
        """
        self.id = list(range(N))
        self.sz = [1] * N
        self.count = N

    def root(self, i):
        """
        Finds the root of the element at index i in the Union-Find data structure.

        Parameters:
        - i: The index of the element.

        Returns:
        - The root of the element at index i.

        Notes:
        - This method uses path compression to optimize the search for the root.
        """
        while i != self.id[i]:
            self.id[i] = self.id[self.id[i]]  # path compression
            i = self.id[i]
        return i

    def connected(self, p, q):
        """
        Determines whether two elements are connected in the union-find data structure.

        Parameters:
            p (int): The first element.
            q (int): The second element.

        Returns:
            bool: True if the elements are connected, False otherwise.
        """
        return self.root(p) == self.root(q)

    def union(self, p, q):
        """
        Unites two elements by connecting their roots.
        Parameters:
        - p: The first element.
        - q: The second element.
        Returns:
        None
        """
        i = self.root(p)
        j = self.root(q)
        if i == j:
            return

        if self.sz[i] < self.sz[j]:
            self.id[i] = j
            self.sz[j] += self.sz[i]
        else:
            self.id[j] = i
            self.sz[i] += self.sz[j]
        
        self.count -= 1
    
    def size(self, i):
        """
        Returns the size of the component that the element 'i' belongs to.

        Parameters:
        - i: The element for which the size of the component is to be determined.

        Returns:
        - The size of the component that the element 'i' belongs to.
        """
        return self.sz[self.root(i)]
    
    def count(self):
        """
        Returns the number of components in the union-find data structure.

        Parameters:
        None

        Returns:
        int: The number of components in the union-find data structure.
        """
        return self.count