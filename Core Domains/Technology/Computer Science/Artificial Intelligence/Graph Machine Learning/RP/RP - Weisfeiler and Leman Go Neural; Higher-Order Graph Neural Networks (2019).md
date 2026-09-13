# Weisfeiler and Leman Go Neural: Higher-Order Graph Neural Networks

**Paper link:** https://arxiv.org/abs/1810.02244

---

## **Paper metadata**

**Authors / collaborators:**  
- Christopher Morris
- Martin Ritzert
- Matthias Fey
- William L. Hamilton
- Jan Eric Lenssen
- Gaurav Rattan
- Martin Grohe

**Organizations / companies / institutions involved:**  
- TU Dortmund University
- University of Amsterdam
- Stanford University
- RWTH Aachen University

**Publication date:**  
2019

**Venue / source:**  
AAAI 2019

**Research paper type / category:**  
- Theoretical paper
- Method / model paper
- Experimental / empirical paper

**Primary field / topic area:**  
Expressive power of graph neural networks and higher-order GNNs

**Keywords:**  
- Weisfeiler-Leman
- higher-order GNN
- expressiveness
- graph isomorphism
- graph classification

---

## **Opening perspective**

This paper matters because it made a hidden limitation of standard GNNs explicit. Many graph networks look different at the implementation level, but their expressive ceiling is often much closer than it appears. The paper shows that common message-passing GNNs are closely tied to the `1`-dimensional Weisfeiler-Leman graph isomorphism test, which means they inherit both its strengths and its blind spots.

That insight changed how the field thought about architecture design. After this paper, expressiveness was no longer just an informal claim about "capturing structure better." It became something researchers could compare against a known combinatorial test.

---

## **Full walkthrough and explanation**

The paper starts by analyzing standard neighborhood-aggregation GNNs. These models update each node by mixing information from its neighbors and itself. The authors show that, under fairly broad conditions, such models are at most as discriminative as `1`-WL for distinguishing non-isomorphic graphs.

Graph -> iterative color/refinement style neighborhood aggregation -> node/graph embeddings -> discrimination power bounded by 1-WL

This is important because `1`-WL is already known to fail on certain structurally distinct graphs. So the result is not just abstract theory. It says that if a task depends on distinctions `1`-WL cannot see, many standard GNNs will fail too no matter how well they are optimized.

The constructive response is to define `k`-order GNNs that operate on tuples or higher-order structures rather than only individual nodes. That raises expressive power, bringing the neural model closer to higher-order Weisfeiler-Leman tests. The cost, of course, is combinatorial growth in computation and memory. The paper is therefore not pretending higher-order expressiveness is free.

The experiments support the theory by showing that higher-order information improves graph classification and regression on tasks where local message passing is insufficient. The broader lesson is that graph-learning power is shaped not just by depth or parameter count, but by what structural comparisons the architecture is even capable of representing.

---

## **Subtle points, clarifications, and limits**

- The paper does not claim that every useful graph task needs higher-order GNNs. It shows that some distinctions are invisible to standard message passing.
- Higher-order power brings heavy computational cost, so the theory creates a trade-off rather than a universal prescription.
- The `1`-WL comparison is a ceiling on a large model family, not a statement that all implementations behave identically in practice.

---

## **Closing perspective**

This paper earned respect because it gave graph deep learning a theory milestone. It connected neural architecture design to a classical graph-isomorphism procedure and thereby made expressiveness measurable in a meaningful way. Many later papers on invariant GNNs, subgraph methods, and higher-order structure are easier to understand once this WL lens is in place.

---

## **Personal comprehension notes**

The easiest way to remember this paper is: standard GNNs mostly "see" graphs the way `1`-WL sees them. If `1`-WL misses a difference, the GNN often misses it too.

The higher-order part then becomes obvious: give the model richer objects than single nodes, and it can represent richer structure, but at a steep computational price.

---

## **Compact retention notes**

- **Paper type:** Foundational theory-meets-architecture paper for GNN expressiveness
- **Core idea:** Standard message-passing GNNs are bounded by the expressive power of `1`-WL, so higher-order neural graph models are needed for richer discrimination.
- **Main mechanism:** Compare aggregation-based GNNs to WL refinement and construct higher-order GNN variants.
- **Key result:** Establishes a clean expressiveness theory and shows higher-order structure can improve downstream performance.
- **Main limitation:** The more expressive models are much more computationally expensive.

---

## **Citations used in the paper**

- Franco Scarselli et al., *The Graph Neural Network Model*, 2009 - early neural computation on graphs.
- Thomas N. Kipf and Max Welling, *Semi-Supervised Classification with Graph Convolutional Networks*, 2017 - representative neighborhood-aggregation GNN baseline.
- Christopher Morris et al., *Weisfeiler and Leman Go Neural: Higher-Order Graph Neural Networks*, 2019 - the core expressiveness result and higher-order construction.
