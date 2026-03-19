
[Spectral graph theory - Wikipedia](https://en.wikipedia.org/wiki/Spectral_graph_theory)

---

# Spectral Graph Theory

## Overview

**Spectral graph theory** studies the structure and properties of graphs using **linear algebra**, particularly the **eigenvalues and eigenvectors of matrices associated with the graph**.

Instead of analyzing a graph purely through combinatorics (nodes and edges), spectral graph theory converts the graph into a **matrix representation** and studies its **spectrum** (its eigenvalues and eigenvectors).

**Key idea**

> The eigenvalues and eigenvectors of graph matrices reveal hidden structural properties of the graph.

These properties include:

- connectivity
    
- clustering
    
- bottlenecks
    
- graph partitions
    
- diffusion behavior on graphs
    

---

# Graph Foundations

A **graph** consists of:

- **Nodes (vertices)**
    
- **Edges (connections between nodes)**
    

Example graph used throughout this note:

```
    1
   / \
  2---3---4
```

Edges:

```
(1,2)
(1,3)
(2,3)
(3,4)
```

This graph contains:

- a triangle between nodes **1,2,3**
    
- a **tail node (4)** attached to node **3**
    

---

# Node Ordering

To convert a graph into a matrix, we assign each node an index.

For this example:

```
Node ordering = (1,2,3,4)
```

This means:

- Row 1 / Column 1 → Node 1
    
- Row 2 / Column 2 → Node 2
    
- Row 3 / Column 3 → Node 3
    
- Row 4 / Column 4 → Node 4
    

The ordering must remain consistent for all matrices.

---

# Adjacency Matrix

The **adjacency matrix** describes **direct connections between nodes**.

Definition:

```
A[i,j] = 1 if node i is connected to node j
A[i,j] = 0 otherwise
```

For our graph:

```
A =

[0 1 1 0
 1 0 1 0
 1 1 0 1
 0 0 1 0]
```

Interpretation example:

```
A[1,2] = 1 → node 1 connected to node 2
A[1,4] = 0 → node 1 not connected to node 4
```

The adjacency matrix represents **local connectivity** of the graph.

---

# Node Degree

The **degree of a node** is the number of edges connected to it.

For our graph:

```
deg(1) = 2
deg(2) = 2
deg(3) = 3
deg(4) = 1
```

---

# Degree Matrix

The **degree matrix** is a diagonal matrix containing node degrees.

```
D =

[2 0 0 0
 0 2 0 0
 0 0 3 0
 0 0 0 1]
```

Only the diagonal contains values.

---

# Graph Laplacian

The **graph Laplacian** is the most important matrix in spectral graph theory.

Definition:

```
L = D - A
```

For our example:

```
L =

[ 2 -1 -1  0
 -1  2 -1  0
 -1 -1  3 -1
  0  0 -1  1]
```

Interpretation:

- diagonal entries → node degree
    
- off-diagonal entries → negative edge connections
    

Example:

Row for node 3:

```
[-1 -1 3 -1]
```

Meaning:

- node 3 connects to nodes **1,2,4**
    
- degree = **3**
    

---

# Eigenvalues and Eigenvectors

Spectral graph theory studies the **eigenvalue problem**:

```
L v = λ v
```

Where:

- **L** = Laplacian matrix
    
- **v** = eigenvector
    
- **λ** = eigenvalue
    

Interpretation:

Applying matrix **L** to vector **v** only **scales the vector**, without changing its direction.

---

# Characteristic Equation

Eigenvalues are found by solving:

```
det(L - λI) = 0
```

This equation is called the **characteristic polynomial**.

---

# Eigenvalues of the Example Graph

For the example graph, the Laplacian eigenvalues are:

```
0, 1, 3, 4
```

They are usually ordered:

```
λ1 ≤ λ2 ≤ λ3 ≤ λ4
```

So:

```
λ1 = 0
λ2 = 1
λ3 = 3
λ4 = 4
```

---

# Important Laplacian Property

The vector of all ones is always an eigenvector of the Laplacian.

```
v =

[1
 1
 1
 1]
```

with eigenvalue:

```
λ = 0
```

This corresponds to **uniform structure across the graph**.

---

# Connected Components

A key theorem:

```
Number of zero eigenvalues
=
Number of connected components
```

Since our graph has only one zero eigenvalue:

```
The graph is connected.
```

---

# The Fiedler Value

The **second-smallest eigenvalue** is called:

```
Algebraic connectivity
or
Fiedler value
```

For our graph:

```
λ2 = 1
```

Interpretation:

- small values → graph weakly connected
    
- large values → graph strongly connected
    

Our graph is weakly connected because node **4** attaches via only one edge.

---

# The Fiedler Vector

The eigenvector corresponding to λ₂ is called the **Fiedler vector**.

One valid Fiedler vector is:

```
v =

[-1
 -1
  0
  2]
```

This vector reveals **graph clustering structure**.

---

# Interpreting the Fiedler Vector

Node values:

|Node|Value|
|---|---|
|1|-1|
|2|-1|
|3|0|
|4|2|

Interpretation:

Nodes with similar values behave similarly in the graph.

This reveals three structural regions:

```
{1,2}   similar values
3       intermediate bridge node
4       strongly separated
```

A natural clustering is:

```
Cluster A: {1,2,3}
Cluster B: {4}
```

---

# Spectral Clustering Idea

Spectral clustering works as follows:

1. Compute graph Laplacian
    
2. Compute eigenvectors
    
3. Use Fiedler vector values to group nodes
    

A simple rule:

```
negative values → one cluster
positive values → another cluster
```

Nodes near **0** lie near the **boundary between clusters**.

---

# Graph Energy Interpretation

The Fiedler vector minimizes the **graph smoothness energy**:

```
Σ(i,j in edges) (v_i - v_j)^2
```

This means:

- connected nodes prefer similar values
    
- weak connections create large differences
    

This reveals **weak edges or bottlenecks** in the graph.

---

# Geometric Interpretation

You can imagine the Fiedler vector assigning **heights to nodes**.

Example heights:

```
node 1 = -1
node 2 = -1
node 3 = 0
node 4 = 2
```

The graph bends upward toward node **4**, indicating that node **4** forms a separate region.

---

# What Spectral Graph Theory Reveals

Using eigenvalues and eigenvectors, we can detect:

- graph connectivity
    
- clusters
    
- bottlenecks
    
- symmetric nodes
    
- bridge nodes
    
- diffusion behavior
    
- community structure
    

---

# Normalized Laplacian

Another important variant is the **normalized Laplacian**:

```
L_norm = I - D^(-1/2) A D^(-1/2)
```

This removes bias from nodes with very high degree.

Normalized Laplacians are widely used in:

- machine learning
    
- graph clustering
    
- network analysis
    

---

# Spectral Embedding

Instead of using one eigenvector, we can use several.

Example:

```
(v2, v3)
```

Each node becomes a point in Euclidean space:

```
node_i → (v2(i), v3(i))
```

Clustering then becomes a **geometric clustering problem**.

This idea powers:

- spectral clustering
    
- manifold learning
    
- graph embeddings
    
- graph neural networks
    

---

# Key Insight

Spectral graph theory converts graphs into **linear algebra problems**.

Instead of directly analyzing nodes and edges, we analyze:

```
eigenvalues
eigenvectors
matrix structure
```

These reveal the **hidden geometry of the graph**.

---

# Summary

Process of spectral graph analysis:

```
Graph
   ↓
Adjacency Matrix
   ↓
Degree Matrix
   ↓
Laplacian Matrix
   ↓
Eigenvalues & Eigenvectors
   ↓
Structural Insights
```

This allows us to uncover:

- connectivity
    
- clusters
    
- bottlenecks
    
- global graph structure
    

using linear algebra.

---

If you'd like, I can also give you the **next Obsidian note you should create**:

**Spectral Clustering**

It builds directly on this and is where spectral graph theory becomes extremely useful in **AI and machine learning systems**.