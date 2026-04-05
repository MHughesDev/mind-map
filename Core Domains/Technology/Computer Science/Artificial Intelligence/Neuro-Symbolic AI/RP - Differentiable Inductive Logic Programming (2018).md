# Differentiable Inductive Logic Programming

**Paper link:** https://deepmind.com/blog/learning-explanatory-rules-noisy-data/

---

## **Paper metadata**

**Authors / collaborators:**  
- Richard Evans
- Edward Grefenstette

**Organizations / companies / institutions involved:**  
- DeepMind

**Publication date:**  
2018

**Venue / source:**  
Journal of Artificial Intelligence Research

**Research paper type / category:**  
- Method / model paper
- Theoretical paper

**Primary field / topic area:**  
Neuro-symbolic learning and inductive logic programming

**Keywords:**  
- dILP
- logic induction
- differentiable reasoning
- rule learning
- interpretability

---

## **Opening perspective**

This paper asks whether logic programs can be learned with gradient descent rather than symbolic search alone. That question is central in neuro-symbolic AI because it targets the classic ILP strengths of data efficiency and interpretability while trying to add robustness to noise and differentiable training.

## **Full walkthrough and explanation**

The system relaxes discrete rule search into differentiable rule-weight learning over a constrained clause space. Instead of outputting only opaque neural embeddings, it aims to learn explicit rules that can still be read by humans.

Examples -> differentiable clause weighting over candidate logic programs -> soft inference -> learned rule set

Its importance lies in showing that symbolic program induction and backpropagation do not have to be treated as enemies. The main weakness is that the original framework had significant expressivity restrictions, which later work tried to relax.

## **Subtle points, clarifications, and limits**

- The original dILP system is historically important but constrained in predicate arity and clause shape.
- Later structured-example extensions are more expressive.

## **Closing perspective**

This paper remains one of the clearest landmarks in neuro-symbolic rule learning because it showed a concrete way to learn interpretable logic-like programs with differentiable machinery.

## **Personal comprehension notes**

The memory hook is: "learn symbolic-looking rules with gradient descent."

## **Compact retention notes**

- **Paper type:** Foundational neuro-symbolic rule-learning paper
- **Core idea:** Make ILP differentiable so rule induction can be optimized with gradient-based methods.
- **Main mechanism:** Softly weight candidate clauses and perform differentiable logical inference.
- **Key result:** Learns interpretable rule structures while handling some noise and ambiguity.
- **Main limitation:** The original framework is quite restricted in what programs it can represent.

## **Citations used in the paper**

- Richard Evans and Edward Grefenstette, *Differentiable Inductive Logic Programming*, JAIR.
- Hikaru Shindo et al., *Differentiable Inductive Logic Programming for Structured Examples*, 2021.
