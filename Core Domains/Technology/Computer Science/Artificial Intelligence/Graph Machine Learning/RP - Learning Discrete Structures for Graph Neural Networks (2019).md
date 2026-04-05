# Learning Discrete Structures for Graph Neural Networks

**Paper link:** https://proceedings.mlr.press/v97/franceschi19a.html

---

## **Paper metadata**

**Authors / collaborators:**  
- Luca Franceschi
- Mathias Niepert
- Massimiliano Pontil
- Xiao He

**Organizations / companies / institutions involved:**  
- USI Lugano
- NEC Laboratories Europe
- University College London

**Publication date:**  
2019

**Venue / source:**  
ICML 2019

**Research paper type / category:**  
- Method / model paper
- Experimental / empirical paper

**Primary field / topic area:**  
Structure learning for graph neural networks

**Keywords:**  
- structure learning
- bilevel optimization
- graph learning
- GNN
- discrete edges

---

## **Opening perspective**

This paper attacks a hidden assumption in graph neural networks: that the graph is already given and correct. In many real problems the graph is noisy, incomplete, or missing, so the paper proposes learning the discrete graph structure jointly with the GNN parameters.

## **Full walkthrough and explanation**

The method treats edge probabilities as learnable hyperparameters inside a bilevel optimization problem. The inner problem trains the GNN on a sampled or induced graph, and the outer problem adjusts the graph distribution so the learned model performs better.

Features -> probabilistic edge model -> sampled/learned graph -> GNN training -> bilevel update of graph structure

The key contribution is conceptual as much as technical: graph construction itself becomes part of the learning loop rather than a frozen preprocessing choice.

## **Subtle points, clarifications, and limits**

- The method is powerful when graph structure is uncertain, but bilevel optimization is expensive.
- The learned graph is task-dependent, which can be a strength or a limitation depending on the use case.

## **Closing perspective**

This paper mattered because it helped normalize the idea that graph learning is not only about learning on graphs but also about learning the graphs themselves.

## **Personal comprehension notes**

Think of it as "do not assume the graph; optimize it."

## **Compact retention notes**

- **Paper type:** Graph structure-learning paper
- **Core idea:** Jointly learn the graph and the GNN.
- **Main mechanism:** Bilevel optimization over discrete edge probabilities.
- **Key result:** Shows that task-aware graph structure learning can outperform fixed-graph baselines.
- **Main limitation:** Optimization is substantially harder than ordinary GNN training.

## **Citations used in the paper**

- Thomas N. Kipf and Max Welling, *Semi-Supervised Classification with Graph Convolutional Networks*, 2017.
- Luca Franceschi et al., *Learning Discrete Structures for Graph Neural Networks*, 2019.
