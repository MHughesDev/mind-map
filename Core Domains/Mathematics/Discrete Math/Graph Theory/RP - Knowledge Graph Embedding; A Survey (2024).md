# Knowledge Graph Embedding: A Survey from the Perspective of Representation Spaces

**Paper link:** https://doi.org/10.1145/3643806

---

## **Paper metadata**

**Authors / collaborators:**  
- Jiahang Cao
- Jinyuan Fang
- Zaiqiao Meng
- Shangsong Liang

**Organizations / companies / institutions involved:**  
- Sun Yat-sen University
- University of Glasgow
- Mohamed bin Zayed University of Artificial Intelligence

**Publication date:**  
March 13, 2024

**Venue / source:**  
ACM Computing Surveys, 56(6), 1-42

**Research paper type / category:**  
- Survey / review paper
- Tutorial / pedagogical paper

**Primary field / topic area:**  
Knowledge graph embedding, representation learning, and mathematical modeling of relational graphs

**Keywords:**  
- knowledge graph embedding
- representation spaces
- link prediction
- hyperbolic geometry
- relational pattern inference

---

## **Opening perspective**

This survey is best understood as an attempt to clean up a field that had become too dependent on model names, score tables, and isolated tricks. Knowledge graph embedding papers are often introduced as if they were separate inventions, but the authors argue that the deeper question is always the same: what kind of mathematical space are entities and relations being placed into, and what structures does that space naturally preserve? Once you look at the literature that way, TransE, ComplEx, RotatE, hyperbolic models, Gaussian models, and mixed-curvature systems stop looking like unrelated acronyms. They become different answers to the same design problem.

That reframing is why the paper matters. It gives the KGE field a conceptual map instead of a leaderboard. If you care about link prediction, hierarchy-heavy knowledge graphs, cyclic structure, relation-pattern inference, uncertainty, or the later problem of combining knowledge graphs with large language models, the survey gives you a way to reason about why a family of models works rather than just memorizing which one happened to win on a benchmark.

---

## **Full walkthrough and explanation**

**Why the survey reorganizes the KGE field**

The paper begins from the standard object of the field: a knowledge graph is a set of entities, relations, and triples, usually written as
$$
\mathcal{G} = \{\mathcal{E}, \mathcal{R}, \mathcal{T}\},
$$
where each factual edge is a triple
$$
(h, r, t),
$$
with head entity $h$, relation $r$, and tail entity $t$. The practical motivation is familiar. Large knowledge graphs such as YAGO, Wikidata, Freebase, and DBpedia store huge amounts of factual structure, but that structure is difficult to manipulate directly because the graph is large, sparse, multi-relational, and full of patterns like chains, rings, and hierarchies. Knowledge graph embedding tries to compress this symbolic graph into a low-dimensional space where entities and relations can be scored, compared, and completed efficiently.

The survey insists that this compression process always has three major components: embedding mapping, score function, and representation training. The first chooses how entities and relations are represented. The second measures how plausible a triple is. The third learns parameters from observed and corrupted triples. The authors keep returning to this pipeline because it is where mathematical space actually matters.

Observed triples -> embedding mapping -> score function -> negative sampling -> loss minimization -> learned entity and relation embeddings -> downstream tasks

That pipeline is not just engineering detail. It is the bridge between abstract space and empirical performance. A very simple example is TransE, whose score in Euclidean space is
$$
s(\mathbf{h}, \mathbf{r}, \mathbf{t}) = -\|\mathbf{h} + \mathbf{r} - \mathbf{t}\|_{1/2}.
$$
Here $\mathbf{h}$, $\mathbf{r}$, and $\mathbf{t}$ are the embeddings of the head, relation, and tail. The score is high when the translated head $\mathbf{h} + \mathbf{r}$ lands close to the tail $\mathbf{t}$. That already shows the paper's core point: a model is not just a formula. It is a formula made possible by a space with certain operations, distances, and geometric interpretations.

Training then usually compares positive triples with corrupted negative ones. The paper highlights the standard margin-ranking objective:
$$
\mathcal{L}_{margin}
=
\sum_{(h,r,t)\in\mathcal{T}}
\sum_{(h',r,t')\in\mathcal{T}^{-}}
\max\left(0, \gamma - s(\mathbf{h}, \mathbf{r}, \mathbf{t}) + s(\mathbf{h}', \mathbf{r}, \mathbf{t}')\right),
$$
where $\mathcal{T}$ is the observed triple set, $\mathcal{T}^{-}$ is a set of corrupted triples, and $\gamma$ is the required margin. The logic is simple: valid triples should score higher than corrupted ones. But the survey's larger lesson is that the meaning of "score higher" depends on the structure of the space in which that score is defined.

**Why the authors spend time on basic mathematics**

One of the most distinctive features of the paper is that it does not rush straight to model taxonomy. Before discussing KGE families, it introduces topological space, vector space, normed space, inner product space, Euclidean space, and manifold. That can look excessive at first, but it is actually central to the paper's teaching strategy. The authors want the reader to understand that different model families are not merely different parameterizations. They inherit different capabilities from the spaces they live in.

A key inclusion relation in the paper is:

Inner product space -> normed space -> metric space -> topological space

The meaning is that inner products induce norms, norms induce distances, and distances induce topology. Going from left to right, the space retains fewer directly usable structures. That matters because KGE models live off those structures. Some rely on addition and scalar multiplication, some on angles, some on curvature, some on distance growth, some on probability measures, and some on continuous trajectories. The paper's mathematical preliminaries are therefore not decorative. They are the vocabulary that makes later model comparison precise.

This is also where the authors start motivating their three-way classification. They argue that most KGE models can be understood from three mathematical perspectives: algebraic structure, geometric structure, and analytical structure. Those perspectives are not rivals. They are complementary ways of asking what a representation space lets a model do.

**Algebraic structure: relations as operations**

The algebraic part of the survey is really about what operations a model gives to relations. The authors begin with vector spaces because they dominate KGE history. In real vector space, TransE is the canonical starting point: a relation acts like a translation, so a plausible triple satisfies $\mathbf{h} + \mathbf{r} \approx \mathbf{t}$. This is elegant, cheap, and highly influential. But the paper carefully explains why it breaks down on 1-to-N, N-to-1, and N-to-N relations. If the same head and relation point to many tails, a pure translation can collapse distinct tail entities toward the same location.

That is why later real-space models introduce projections and richer linear structure. TransH projects entities into a relation-specific hyperplane before applying translation, so an entity can behave differently under different relations. TransR separates entity space from relation space and uses a relation-specific mapping matrix to move entities into the relevant relation space. RESCAL and related bilinear models go in a different direction: instead of interpreting a relation as a translation vector, they interpret it as a matrix or operator that mediates semantic interaction between head and tail embeddings. In this family, the relation is not "move here" so much as "interact with these dimensions in this structured way."

The survey then moves into complex vector space, and here the algebraic story changes from translation to rotation and conjugation. ComplEx is important because it uses complex embeddings and a conjugate-based score to escape the symmetry restriction that hurts DistMult. In ordinary real bilinear form, swapping head and tail can make the score too symmetric. ComplEx fixes that by using complex conjugation, so the order of entities matters. RotatE pushes this even further by interpreting each relation as an element-wise rotation in complex space:
$$
\mathbf{t} = \mathbf{h} \circ \mathbf{r},
$$
where $\circ$ is the Hadamard product. The paper treats this as more than a clever trick. Rotation gives a geometric-algebraic explanation for why RotatE can capture symmetry, antisymmetry, inversion, and composition. A relation can be an identity rotation, an inverse rotation, or part of a composed chain of rotations.

Once that logic is in place, the survey naturally expands to quaternion, biquaternion, and dual-quaternion models such as QuatE, BiQUE, and DualE. The point is not that higher-dimensional number systems are automatically better. The point is that richer algebraic systems create richer interaction rules between entities and relations. Quaternion multiplication, for example, gives more expressive rotational behavior than ordinary complex multiplication. Dual quaternion models can combine translation and rotation in one algebraic object.

The paper also includes neural network models such as ConvE, R-GCN, KG-BERT, and Knowformer under the vector-space umbrella. That is a useful reminder that even when a model looks architectural rather than algebraic, it still ultimately lives in a representational space with particular operators. The survey admits that neural models are harder to interpret mathematically, but because they still produce vectorial embeddings, they remain part of the same broad story.

The algebraic discussion then widens beyond vector spaces. Group-based models such as TorusE, DihEdral, DensE, NagE, and ModulE are appealing because group structure naturally matches relations like identity, inverse, and composition. TorusE is especially important in the survey because it uses a compact Lie group to avoid the divergence problems that force explicit regularization in many Euclidean models. Ring-based models, especially MobiusE, take this a step further by defining embeddings on a Mobius ring. The authors emphasize the unusual non-oriented surface of the Mobius band, which they suggest may be useful for orientation-related relational phenomena.

A large part of the later pattern-inference section makes more sense once this algebraic groundwork is in place. The survey's basic conclusion is that the operator often determines the patterns a model can capture. Addition-based models are simple and powerful but limited. Product-based models, especially Hadamard and Hamilton-style products, often capture richer relation patterns more naturally.

**Geometric structure: matching graph shape to space shape**

If the algebraic section asks what operations relations perform, the geometric section asks what global shape the embedding space has. The authors divide this into Euclidean geometry, hyperbolic geometry, and spherical geometry.

Euclidean geometry is the most familiar setting, and the survey treats it as the home of straightforward geometric transformations. Translation, rotation, reflection, and scaling are all easy to visualize and compute there. In Cartesian coordinates, models such as TransE, RotatE, PairRE, TripleRE, TranS, HousE, and CompoundE can all be read as using different Euclidean transformations to move one entity toward another. This is why Euclidean KGE is so intuitive: the relation really can look like a movement or transformation in a flat space.

The survey is especially good at explaining that Euclidean geometry is not exhausted by ordinary Cartesian translation. HAKE, for example, moves to a polar coordinate system because hierarchy is awkward to express in plain flat Cartesian terms. In HAKE, the radial coordinate models level or depth in a hierarchy, while the angular coordinate separates entities within the same level. That is a very important design move. The paper is showing that sometimes a better coordinate system inside the same broad geometric family gives the model the inductive bias it needs. It also notes related models such as H2E and HBE that combine polar intuitions with hyperbolic structure.

The hyperbolic section is one of the most important parts of the paper because it gives the standard argument for why hyperbolic embeddings became so attractive in knowledge graphs. In hyperbolic space, area and volume grow rapidly with radius, which makes the space naturally good at representing tree-like and hierarchical structures. That is why models such as MuRP, ATTH, HBE, HyperKA, HypHKGE, and UltraE show strong performance on hierarchy-heavy graphs. The authors repeatedly connect this geometry to the actual structure of datasets like WN18RR.

ATTH is especially illustrative because it does more than place embeddings in a hyperbolic manifold. It learns trainable curvatures and uses hyperbolic isometries so that relations can capture logical patterns and hierarchies at the same time. The survey likes models of this kind because they make the relation between geometry and task explicit: hyperbolic curvature is not just mathematically exotic, it is there because low-dimensional flat spaces distort hierarchies too easily.

At the same time, the paper does not romanticize hyperbolic geometry. It explicitly raises the question of whether hyperbolic space is always worth its added computational cost. Models such as RotL are presented as attempts to simplify hyperbolic operations while retaining some of the low-dimensional benefits. This is typical of the survey's tone. It is interested in advantages, but also in when those advantages are actually worth paying for.

The spherical section makes another important distinction. The authors separate spherical coordinate systems from spherical geometry proper. A spherical coordinate system is just a way of describing positions; spherical geometry is a space with its own lines, distances, and curvature. That distinction matters because some models merely use spherical coordinates, while others truly exploit spherical geometry. TransC, for example, represents concepts as spheres and instances as points, which is useful for modeling concept-subconcept and instance-concept relations. HypersphereE extends the same intuition to hyperspheres in order to capture uncertainty more flexibly. ManifoldE expands entities from points to manifolds, especially spheres and hyperplanes, so that link prediction does not have to force all true facts through a single pointwise constraint.

The survey also argues that spherical spaces are especially natural for cyclic or ring-like structures, because spherical embedding fields have a kind of circularity that aligns with those patterns. This is part of the paper's broader thesis: different graph structures want different curvature. Hierarchies tend to like hyperbolic space, cyclic structures tend to like spherical structure, and flat relational transformations often fit Euclidean space. Once that clicks, the field starts looking like geometry matching rather than mere model proliferation.

**Analytical structure: uncertainty, continuity, and stability**

The analytical perspective is the least familiar part of the survey, but it is one of the most interesting. Here the authors are asking whether the space supports things like probability measures, continuity, differential structure, and other properties relevant to optimization and robustness.

The probability-space models are the clearest example. KG2E represents entities and relations not as single vectors but as Gaussian distributions. The mean vector indicates location, while the covariance carries uncertainty. That is a major conceptual shift. Instead of saying "this entity is exactly here in space," the model says "this entity occupies a region with a certain uncertainty profile." That is especially helpful when the graph is noisy or when a relation has ambiguous semantics. TransG pushes this idea further by using an infinite mixture model so that one relation can have multiple semantic components rather than a single translation vector. DiriE uses Dirichlet distributions, GaussianPath reasons through Gaussian uncertainty in multi-hop settings, and ItoE treats relation dynamics as stochastic processes. The survey groups all of this under analytical structure because these models use probability and stochasticity as core representational ingredients, not as afterthoughts.

The other analytical branch focuses on continuity and dynamics in Euclidean space. FieldE is the main example. Instead of thinking of a relation as a static vector or matrix, it treats a relation as a vector field and models entity transitions through an ordinary differential equation:
$$
\frac{d\mathbf{e}(t)}{dt} = f_{\theta_r}(\mathbf{e}(t)).
$$
This means the relation defines a continuous trajectory through space rather than a one-step jump. TANGO applies a similar neural-ODE idea to temporal knowledge graphs. The survey uses these models to argue that analytical properties such as continuity, stability, convergence, and differentiability deserve much more attention in KGE than they usually get. In other words, the field has focused heavily on what space looks like and too little on how dynamics unfold inside that space.

A useful way to read this section is that analytical structure does not usually replace algebraic or geometric structure. It supplements them. The authors themselves say this perspective is underexplored and often auxiliary, but they clearly think it will matter more in future models.

**What the empirical sections are really trying to teach**

After building the taxonomy, the paper turns to downstream tasks. The first is link prediction, the canonical KGE evaluation problem. Given a partial triple such as $(h, r, ?)$ or $(?, r, t)$, the model scores candidate entities and ranks them. The paper explains that this is where the score function becomes operational: a translation score, rotation score, or hyperbolic distance is not just a theoretical object anymore. It is the quantity used to decide which missing entity is most plausible.

The most important empirical discussion is the hierarchy-acquisition analysis. The authors compare Euclidean, hyperbolic, spherical, and mixed-curvature models on hierarchy-containing datasets such as WN18RR and FB15K-237. Their main conclusion is nuanced. In low dimensions, non-Euclidean models, especially hyperbolic ones, usually do better on hierarchical structure because the geometry fits tree-like growth more naturally. Spherical models can also help when cyclic or ring-like structure matters. But in higher dimensions, the gap between Euclidean and non-Euclidean spaces narrows because high-dimensional Euclidean space can also absorb complicated structure. That is an important restraint on the usual hype. Hyperbolic space is not presented as universally superior. It is presented as especially helpful when dimensionality is tight and hierarchy is strong.

The survey also finds that mixed or hybrid models often do especially well. That fits the authors' broader view that real knowledge graphs are structurally heterogeneous. A single curvature or a single operator may be too blunt if the graph contains both tree-like and cyclic patterns, or both simple and highly compositional relations.

The pattern-inference section is another major contribution. The paper formalizes four important relation patterns: symmetry, antisymmetry, inversion, and composition. It then compares model families by whether they can capture them. This is where the algebraic story becomes empirical. TransE's addition operator is elegant and can capture antisymmetry, inversion, and composition, but not symmetry. DistMult's inner-product structure handles symmetry well but fails on antisymmetry. ComplEx improves that by using complex conjugation, and RotatE improves it further by using rotations that naturally encode all four patterns. PairRE, BiQUE, DualE, ATTH, DihEdral, and UltraE are also highlighted as models that can capture the full set. The authors' practical conclusion is that product-like operations are often a better route than pure addition if the task demands rich relation-pattern inference.

The paper then zooms out to other uses of KGE: question answering, knowledge reasoning, recommendation systems, information retrieval, cybersecurity, biomedicine, and increasingly the integration of knowledge graphs with large language models. This last point is especially interesting because the survey explicitly places KGs and KGEs in the LLM era. The authors argue that knowledge graphs can help with hallucination, domain-specific grounding, and explainability, while LLMs can in turn help extract, enrich, or interact with KG knowledge. So the survey is not treating KGE as an isolated subfield. It is positioning it as infrastructure for broader AI systems.

The complexity analysis adds one more layer. Vector-based models such as TransE, ComplEx, and UltraE tend to be relatively efficient, often with time and space complexity that scale linearly in embedding dimension. Matrix-heavy models such as RESCAL or TransR are more expensive. Hyperbolic models do not necessarily explode in asymptotic order, but their operations are often slower in practice. The survey's implicit advice is that representation space is never just an expressiveness choice. It is also a compute-budget choice.

**Where the paper thinks the field should go next**

The future-directions section distills the paper's argument into a research agenda. On the algebraic side, the authors want more powerful and possibly unified operations that can capture complex relation types without giving up interpretability. On the geometric side, they want models that can handle mixed structures better and do so with lower computational cost, since single-geometry assumptions are often too rigid for real graphs. On the analytical side, they want much more work on stability, convergence, derivability, and optimization, because those properties shape whether a theoretically attractive space is actually trainable and robust.

One of the paper's most important final claims is that algebraic, geometric, and analytical perspectives should not be treated as separate tribes. The most promising systems may be the ones that mix them. A model might use a hyperbolic manifold for hierarchy, product-based algebra for relation patterns, and differential or probabilistic machinery for continuity and uncertainty. In that sense, the survey is not just classifying the old literature. It is trying to define a more mature design language for future KGE work.

By the end of the paper, the field looks very different from how it looked at the start. Instead of a zoo of named embeddings, you see a structured design space: choose operations for relation logic, choose geometry for graph shape, choose analytical machinery for uncertainty and dynamics, and then accept the matching trade-offs in complexity and performance. That is the survey's real teaching achievement.

---

## **Subtle points, clarifications, and limits**

- The paper does **not** present a single new state-of-the-art KGE model. Its main contribution is a mathematical classification framework, an empirical synthesis, and guidance for choosing spaces.
- "Representation space" here means much more than embedding dimension. It includes algebraic operations, distance functions, curvature, topology, probability measures, and optimization behavior.
- The paper does **not** say non-Euclidean geometry always wins. Its actual claim is narrower: hyperbolic and spherical spaces are often especially useful in low-dimensional settings when the graph structure matches their geometry.
- Spherical coordinate systems and spherical geometry are **not** the same thing in the survey. The authors explicitly distinguish using spherical coordinates as a descriptive tool from embedding in a genuinely spherical manifold.
- Analytical structure is presented as important but underdeveloped. The survey treats uncertainty, continuity, convergence, and stochastic dynamics as promising directions, not as the dominant source of current benchmark wins.
- Several models naturally appear from more than one perspective. RotatE, for example, can be read algebraically as a product-based complex-vector model and geometrically as a rotation-based transformation model.
- The survey's LLM discussion is not a side note. It signals that the authors see knowledge graphs as complementary to language models, especially for factual grounding, domain specificity, and explainability.

---

## **Closing perspective**

This paper matters because it changes the level at which the KGE field can be discussed. Instead of asking which named model is best in the abstract, it asks what kind of space a task actually needs, what operations that space permits, what structures it can preserve with low distortion, and what computational price comes with those choices. That makes the literature much more intelligible.

It is also a useful reminder that representation learning is never just about fitting vectors. It is about choosing the mathematics that will make certain relational facts easy to express and others hard. By giving the field a language of algebraic operators, geometric curvature, and analytical behavior, the survey turns knowledge graph embedding from a collection of recipes into a coherent design discipline.

---

## **Personal comprehension notes**

The easiest way to remember this paper is to think of KGE as "putting a graph into a space whose math does part of the reasoning for you." The survey says the crucial question is not just how big the embedding is. The crucial question is what the space lets relations do.

A good mental model is:

Graph structure -> choose a space shape -> choose relation operators -> train scores that respect that structure -> use the resulting geometry/algebra for prediction

If the graph is strongly hierarchical, hyperbolic space is attractive because it expands outward in a tree-friendly way. If the graph has cyclic or ring-like structure, spherical ideas become attractive. If the task depends on symmetry, inversion, and composition, product-based algebra tends to help more than plain translation. If uncertainty or temporal evolution matters, probabilistic or ODE-based models become more natural.

The way I would compress the survey for memory is:

- **Space choice answers "what kind of structure can I represent naturally?"**
- **Operator choice answers "what kind of relation logic can I model?"**
- **Analytical choice answers "how stable, uncertain, or dynamic can the representation be?"**

Two memory hooks help:

- **Model zoo -> design space:** the paper's deepest move is turning a long list of named models into a structured set of mathematical choices.
- **Leaderboard -> fit between graph and space:** the right question is not "Which KGE is best?" but "Which space matches the structure and constraints of this graph?"

---

## **Compact retention notes**

- **Paper type:** Mathematical survey and tutorial on knowledge graph embedding
- **Core idea:** Reorganize KGE models by the properties of their representation spaces rather than by model name or benchmark ranking.
- **Main mechanism:** Classify KGE methods through three perspectives: algebraic structure, geometric structure, and analytical structure, then compare how those spaces affect pattern modeling, hierarchy capture, uncertainty, and downstream results.
- **Key result:** The paper shows that many empirical differences between KGE families make sense once you ask what operations, curvature, and analytical behavior their spaces provide.
- **Main limitation:** It gives a strong conceptual map, but it is still a survey; it does not settle model choice automatically, and many real systems need mixed spaces plus task-specific engineering.

---

## **Citations used in the paper**

- Antoine Bordes, Nicolas Usunier, Alberto Garcia-Duran, Jason Weston, and Oksana Yakhnenko, *Translating embeddings for modeling multi-relational data*, 2013 - the canonical translation-based baseline and the paper's main reference point for addition-based KGE.
- Theo Trouillon, Johannes Welbl, Sebastian Riedel, Eric Gaussier, and Guillaume Bouchard, *Complex embeddings for simple link prediction*, 2016 - the key complex-vector model used to explain asymmetry and richer semantic matching.
- Zhiqing Sun, Zhi-Hong Deng, Jian-Yun Nie, and Jian Tang, *RotatE: Knowledge graph embedding by relational rotation in complex space*, 2019 - the survey's central example of rotation-based modeling of symmetry, antisymmetry, inversion, and composition.
- Ines Chami, Adva Wolf, Da-Cheng Juan, Frederic Sala, Sujith Ravi, and Christopher Re, *Low-dimensional hyperbolic knowledge graph embeddings*, 2020 - the core hyperbolic reference for low-dimensional hierarchy capture.
- Shizhu He, Kang Liu, Gaowei Ji, and Jun Zhao, *Learning to represent knowledge graphs with Gaussian embedding*, 2015 - the foundational probability-space reference for modeling uncertainty in KGE.
- Maximillian Nickel and Douwe Kiela, *Poincare embeddings for learning hierarchical representations*, 2017 - a major geometric background reference for why hyperbolic space is useful on hierarchical data.
- Quan Wang, Zhendong Mao, Bin Wang, and Li Guo, *Knowledge graph embedding: A survey of approaches and applications*, 2017 - an earlier survey that the authors explicitly position themselves against by shifting from encoding categories to representation spaces.
- Shirui Pan, Linhao Luo, Yufei Wang, Chen Chen, Jiapu Wang, and Xindong Wu, *Unifying large language models and knowledge graphs: A roadmap*, 2023 - part of the paper's broader context for KG and LLM integration.

---
