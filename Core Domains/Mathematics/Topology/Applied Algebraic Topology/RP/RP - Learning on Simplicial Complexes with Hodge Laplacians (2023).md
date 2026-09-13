# Learning on Simplicial Complexes with Hodge Laplacians

**Paper link:** https://arxiv.org/abs/2301.11163

---

## **Paper metadata**

**Authors / collaborators:**  
- Luana Ruiz Yang
- Elvin Isufi

**Organizations / companies / institutions involved:**  
- Delft University of Technology

**Publication date:**  
2023

**Venue / source:**  
arXiv / Hodge-aware simplicial convolution line

**Research paper type / category:**  
- Method / model paper
- Theoretical paper

**Primary field / topic area:**  
Simplicial learning with Hodge-Laplacian operators

**Keywords:**  
- Hodge Laplacian
- simplicial complexes
- higher-order learning
- convolution
- topology

---

## **Opening perspective**

This paper belongs to the line of work asking how to learn directly on simplicial complexes rather than reducing everything to a graph. Its defining claim is that Hodge Laplacians are not just mathematically elegant; they are the right operators for building convolution-like learning rules on higher-order relational domains.

## **Full walkthrough and explanation**

The model treats simplices of different orders as distinct but coupled signal domains. Lower and upper adjacency both matter, and the Hodge-Laplacian structure helps keep those interactions organized. The resulting learning rule looks like a higher-order generalization of graph convolution, but the geometry is richer because simplices can interact through shared boundaries and cofaces.

Simplicial complex -> order-specific Hodge operators -> higher-order convolution/filtering -> learned simplicial representations -> prediction

The paper is important because it makes the Hodge-Laplacian viewpoint operational for learning. Instead of using topology only for analysis after the fact, it builds the topological operator into the model itself.

## **Subtle points, clarifications, and limits**

- This direction is most natural when the data are genuinely higher-order, not when a graph problem is artificially lifted into a simplicial complex.
- The main burden remains model construction: choosing the simplicial complex well.

## **Closing perspective**

This paper is part of the effort that turned simplicial learning from an abstract topological idea into a practical operator-design problem. It matters most as a bridge between Hodge theory and trainable higher-order neural models.

## **Personal comprehension notes**

Think of this as "GCN logic, but on simplices with Hodge structure instead of only on nodes with graph adjacency."

## **Compact retention notes**

- **Paper type:** Higher-order learning method paper
- **Core idea:** Use Hodge Laplacians as the main convolutional operators for simplicial learning.
- **Main mechanism:** Build filters from lower and upper simplicial interactions.
- **Key result:** Shows that Hodge-aware operators provide a principled route to learning on simplicial complexes.
- **Main limitation:** Gains depend on the task really containing meaningful higher-order structure.

## **Citations used in the paper**

- Sergio Barbarossa and Stefania Sardellitti, *Topological Signal Processing over Simplicial Complexes*, 2020.
- Stefania Ebli et al., *Simplicial Neural Networks*, 2020.
