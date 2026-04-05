# Simplicial Neural Networks

**Paper link:** https://openreview.net/forum?id=nPCt39DVIfk

---

## **Paper metadata**

**Authors / collaborators:**  
- Stefania Ebli
- Michaël Defferrard
- Gard Spreemann

**Organizations / companies / institutions involved:**  
- EPFL

**Publication date:**  
2020

**Venue / source:**  
NeurIPS Workshop on Topological Data Analysis and Beyond

**Research paper type / category:**  
- Method / model paper
- Theoretical paper
- Experimental / empirical paper

**Primary field / topic area:**  
Simplicial deep learning and higher-order representation learning

**Keywords:**  
- simplicial neural networks
- Hodge theory
- higher-order learning
- simplicial complexes
- convolution

---

## **Opening perspective**

This paper is part of the first serious wave of work trying to push graph neural networks beyond pairwise structure. Graphs are often enough when all the information lives on nodes and edges, but not when the data themselves are flows, co-boundaries, or genuinely higher-order relations. Simplicial neural networks are the answer proposed here: take the convolutional logic of graph learning, rebuild it on simplicial complexes, and let the model operate directly on higher-order domains.

The paper matters because it is not satisfied with saying "use a bigger hypergraph." It makes a principled case that Hodge-theoretic structure should shape the neural operator. That gives the model access to gradient, curl, and harmonic behavior in a way ordinary GNNs do not naturally express.

---

## **Full walkthrough and explanation**

**What problem the paper is solving**

A standard GNN assumes the relevant information is organized through pairwise adjacency. That is a good fit for many tasks, but not for data such as edge flows, coauthorship simplices, or interactions among groups larger than two. If the learning problem depends on triangles or higher-order cells, flattening everything to a graph can destroy important structure. This paper starts from that mismatch.

Simplicial complex + signals on simplices -> Hodge-inspired convolution operator -> layered neural updates -> task-specific prediction or imputation

The paper builds its neural operator from simplicial analogues of graph convolutions. Instead of one adjacency relation, a simplex can interact through lower adjacency and upper adjacency. For an edge, lower adjacency comes from shared vertices; upper adjacency comes from shared higher-order simplices such as triangles. That split is conceptually important because it distinguishes two genuinely different ways simplices can be related.

**Why Hodge theory is the right language here**

The model uses the Hodge Laplacian as the main operator guiding convolution. This is the natural higher-order counterpart of the graph Laplacian. The reason this matters is not only spectral elegance. The Hodge decomposition says that edge-space signals can be decomposed into gradient, curl, and harmonic parts. A learning rule built from this structure can respond differently to potential-driven flow, local circulation, and global topological residues.

That is the real advance over a naive extension of GNNs. The paper is not simply adding more adjacency matrices. It is making the operator respect the topology of the underlying complex.

**How the neural computation works**

The paper defines convolutions that act on signals attached to simplices of a chosen order. Those convolutions can be expressed through filters of the corresponding Hodge Laplacian. As in graph spectral learning, this gives a notion of locality when the filters are polynomial or otherwise structured to avoid dense global transforms.

Input simplicial signal -> Hodge-based filtering across upper and lower neighborhoods -> nonlinear transformation -> stacked simplicial layers -> output estimate

In practice, the paper studies missing-data imputation on coauthorship complexes. This is a sensible first test because it is a task where higher-order interactions are not an afterthought. The empirical section is therefore less about benchmark domination and more about showing that the architecture can exploit topology-aware structure in a concrete setting.

**What is easy to misunderstand**

It is easy to think this paper proves simplicial neural networks should replace graph neural networks in general. It does not. The stronger and better-supported claim is narrower: when the data or task naturally live on a simplicial complex, especially with important higher-order couplings, a simplicial operator can preserve information that graph reductions may blur or discard.

The paper is also early-stage. Workshop papers often establish a compelling formulation before the ecosystem of architectures, datasets, and ablations is mature. That is exactly how this work should be read. It is a principled opening move in a new design space, not the final best architecture for higher-order learning.

---

## **Subtle points, clarifications, and limits**

- A simplicial neural network is not just a graph neural network on a denser graph. The operator is structured by lower and upper adjacency and by Hodge-theoretic decomposition.
- The benefits appear most clearly when the signal itself is higher-order, not when a plain node-classification problem is artificially lifted into a simplicial complex.
- Because the paper is early and workshop-based, the experimental scope is narrower than the conceptual scope.

---

## **Closing perspective**

This paper is still worth understanding because it helped establish a credible neural learning path for simplicial complexes. It earned respect in higher-order learning and applied topology circles by showing that Hodge-based structure can be used not only for analysis but for trainable representation learning. Later simplicial and cell-complex neural architectures are easier to interpret once you see this paper as one of the field's formative attempts to make topology computationally native inside a neural model.

---

## **Personal comprehension notes**

The way to think about this paper is: if GNNs are neural filters on graphs, SNNs are neural filters on simplicial complexes. The extra power comes from the fact that an edge or triangle can participate in structured higher-order relations that ordinary graphs do not represent faithfully.

The memory hook is "lower adjacency, upper adjacency, Hodge decomposition." Those three ideas explain why the model is more than just a graph network with extra bookkeeping.

---

## **Compact retention notes**

- **Paper type:** Early higher-order deep learning architecture paper
- **Core idea:** Generalize graph neural networks to simplicial complexes using Hodge-inspired convolutions.
- **Main mechanism:** Apply learnable filters built from Hodge Laplacians so signals on simplices can propagate through lower and upper adjacencies.
- **Key result:** Demonstrates that topology-aware neural operators can model higher-order signals more naturally than graph-only reductions.
- **Main limitation:** The paper is an early workshop contribution, so empirical validation is narrower than the conceptual ambition.

---

## **Citations used in the paper**

- Antonio Ortega et al., *Graph Signal Processing: Overview, Challenges, and Applications*, 2018 - graph-spectral background that simplicial learning extends.
- Sergio Barbarossa and Stefania Sardellitti, *Topological Signal Processing over Simplicial Complexes*, 2020 - closely related higher-order signal-processing foundation.
- Stefania Ebli, Michaël Defferrard, and Gard Spreemann, *Simplicial Neural Networks*, 2020 - the paper's own core formulation connecting Hodge theory and neural convolution.
