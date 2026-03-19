# Graph Learning: A Survey

**Paper link:** [https://doi.org/10.1109/TAI.2021.3076021](https://doi.org/10.1109/TAI.2021.3076021)

---

## **Paper metadata**

**Authors / collaborators:**  

- Feng Xia
- Ke Sun
- Shuo Yu
- Abdul Aziz
- Liangtian Wan
- Shirui Pan
- Huan Liu

**Organizations / companies / institutions involved:**  

- Federation University Australia
- Dalian University of Technology
- Monash University
- Arizona State University

**Publication date:**  
March 2021

**Venue / source:**  
IEEE Transactions on Artificial Intelligence, 2(2), 109-127

**Research paper type / category:**  

- Survey / review paper
- Tutorial / pedagogical paper
- Interdisciplinary paper

**Primary field / topic area:**  
Graph learning, graph representation learning, and machine learning on relational / non-Euclidean data

**Keywords:**  

- graph learning
- graph signal processing
- network representation learning
- graph neural networks
- knowledge graph embedding

---

## **Opening perspective**

This survey is best read as an attempt to make graph learning look like a real field rather than a pile of unrelated techniques. By the time the paper appeared, there were already spectral methods, graph embedding methods, random-walk models, graph neural networks, knowledge graph methods, and domain-specific systems, but they were often discussed in separate literatures. The paper's central move is to gather them under one larger question: how do you learn useful representations and make useful predictions when the data are defined by relationships, not just by isolated feature vectors?

That matters because graphs break many comfortable assumptions inherited from ordinary machine learning. Images, audio, and time series come with regular coordinates. Graphs do not. Their geometry is irregular, their entities influence one another through edges, and scale quickly becomes a practical problem. So the survey is not merely cataloguing models. It is teaching the reader to see relational structure itself as a first-class source of information, and then showing the four main technical traditions that had emerged to exploit it by 2021.

---

## **Full walkthrough and explanation**

**What the paper means by graph learning**

The paper starts from a very broad definition: graph learning is essentially machine learning on graphs. Graphs appear everywhere the world has entities plus relations, including social systems, ecosystems, biological networks, citation networks, traffic systems, knowledge graphs, and information systems. In that sense, the paper is not talking about one narrow model family. It is talking about a problem setting in which data points are linked, and where the links themselves often carry as much meaning as the attributes of the nodes.

The authors are also trying to solve a representational problem. Traditional graph analysis often leans heavily on adjacency matrices and hand-built structural descriptors, but the paper argues that these are not enough for many modern tasks. Large, irregular networks are too complex to treat as simple tables. So graph learning becomes the process of extracting features that preserve graph structure, vertex information, or both, in a form that downstream learning systems can actually use.

Graph entities and relations -> structure-aware representation or model -> downstream task such as classification, link prediction, recommendation, matching, or graph-level inference

The paper repeatedly emphasizes that graph learning is useful because many important tasks are relational by nature. Some are **vertex-based**, such as node classification, clustering, or risk identification. Some are **edge-based**, such as link prediction, recommendation, or knowledge reasoning. Some are **subgraph-based**, such as motif analysis, graph classification, or structured pattern recognition. That task framing matters because the survey is not looking for one universal method. It is mapping a family of methods that preserve different kinds of structural information for different goals.

**Why graphs are technically difficult**

The survey then explains why this whole area is harder than simply applying standard machine learning to adjacency features. It gives three recurring challenges. First, graphs live in an **irregular domain** rather than a Euclidean grid, so ideas like locality, distance, convolution, and sampling cannot simply be borrowed unchanged from images or time series. Second, many real graphs are **heterogeneous**, with multiple node types, edge types, semantic relations, and attribute modalities, so the simplifications that work in homogeneous networks often discard important information. Third, large real-world networks demand **distributed or scalable algorithms**, because centralized processing becomes prohibitive when graphs have millions of vertices and edges.

This is the paper's deeper background claim: graph learning exists because structure is not a nuisance variable to be engineered away. It is the thing the model must learn from. That is why the survey positions representation learning, topology inference, sampling, and neural message passing as parts of one broader landscape.

**The survey's four-part taxonomy**

The central organizing decision of the paper is its taxonomy. The authors sort graph learning into four broad categories:

- graph signal processing
- matrix factorization
- random walk
- deep learning

This classification is important because the paper is not saying all graph learning methods work the same way. It is saying they answer the graph-learning problem from different theoretical angles. Graph signal processing asks how to generalize signal-processing concepts to irregular structures. Matrix factorization asks how to preserve graph relationships in lower-dimensional representations. Random-walk methods ask how to turn local network exploration into learning signals. Deep learning methods ask how to learn graph representations end to end through trainable architectures.

The paper also stresses that this is broader than previous surveys. Earlier overviews had focused on graph embedding, deep graph models, knowledge extraction, or graph signal processing separately. The authors want a more comprehensive umbrella view, and they specifically treat graph signal processing as part of graph learning rather than as a separate neighboring field.

**Graph signal processing as the spectral foundation**

The first major family is graph signal processing, or GSP. This section is trying to teach the reader to see a graph not just as a combinatorial object but as a domain on which signals live. If each node carries a value, then the graph becomes an irregular signal domain, and familiar operations from classical signal processing such as filtering, Fourier analysis, and sampling need graph-specific redefinitions.

The paper introduces the standard objects:

$$
L = D - W, \qquad L_{norm} = D^{-1/2} L D^{-1/2}
$$

Here `W` is the adjacency matrix and `D` is the diagonal degree matrix. The Laplacian is central because it gives a way to talk about variation relative to neighboring nodes. A smooth signal on a graph changes slowly across connected vertices; a high-frequency signal changes sharply across edges. That is why the Laplacian becomes the backbone for spectral methods.

The survey distinguishes two main GSP models: **adjacency-matrix-based GSP** and **Laplacian-based GSP**. The first grows out of algebraic signal processing and uses the adjacency matrix as a graph shift operator. The second grows out of spectral graph theory and is especially natural for undirected graphs with symmetric, non-negative edge weights. In either case, the point is to define graph analogs of shift, filter, Fourier transform, and frequency.

$$
\mathbf{s}*{out} = \mathbf{H}\mathbf{s}*{in}
$$

That equation is the paper's compact way of saying that filtering on graphs is still a linear transformation, but now the transformation has to respect graph structure. The survey explains shift invariance through commutation with the graph shift operator and connects eigendecomposition of the shift matrix to graph Fourier ideas. Once that picture is in place, the reader can understand why low-frequency components capture broad structural regularities while higher-frequency components capture sharper local variation.

The GSP section then branches in two directions. One is **sampling and recovery**. Here the survey adapts the classical logic of Nyquist-Shannon to graphs: observe signals on a subset of vertices, then reconstruct the original graph signal as well as possible. It discusses band-limited graph signals, cut-off frequencies, selecting sampling versus aggregation sampling, least-squares reconstruction, probabilistic recovery with Gaussian random fields, adaptive and distributed recovery, kernel regression, and compressed-sensing-inspired variants. The basic pattern is:

Graph signal -> choose informative sampled vertices -> reconstruct the full signal under smoothness or band-limited assumptions

The other branch is **learning topology structure from data**. This is an important transition, because now the graph itself may be only partially known or entirely latent. If topology is partly known, one can infer the missing structure from the known part. If topology is unknown but signals on the graph are observed, the task becomes blind topology inference or graph topology learning. The survey emphasizes smoothness-based methods, Gauss-Markov random field formulations, diffusion models, and time-series-based graph estimation. In other words, GSP is not only about analyzing a fixed graph. It can also be about inferring the graph that best explains observed signals.

The paper's own verdict on GSP is cautiously respectful. It presents GSP as conceptually powerful and foundational, but also as relatively restrictive in practice. These methods often assume access to the whole graph, can be computationally expensive, and scale poorly compared with lighter-weight embedding or neural approaches.

**Matrix factorization and proximity-preserving embeddings**

The next family is matrix factorization. This part of the survey captures an earlier and still influential style of graph learning: represent graph structure through matrices, then compress those matrices into lower-dimensional representations that preserve important relationships. The resulting embeddings can be fed into ordinary machine learning models.

The survey divides this family into **graph Laplacian matrix factorization** and **vertex proximity matrix factorization**. In the first case, the goal is to preserve geometry encoded by a graph or neighborhood graph. The paper discusses transductive versus inductive settings, metric multidimensional scaling, `k`-nearest-neighbor graph construction, locality-preserving projection, anchor-based improvements, local-and-global regressive mapping, and methods that add label or feedback graphs so the learned representation preserves more than bare adjacency.

What ties these methods together is the attempt to preserve pairwise similarity or local manifold structure when moving into a lower-dimensional space. The graph is doing regularization work here: it says which points ought to remain close or structurally related after dimension reduction.

The second branch, vertex proximity matrix factorization, factorizes a proximity matrix more directly. The survey mentions singular value decomposition, regularized Gaussian matrix factorization, and low-rank factorization approaches. This is a more direct "compress the relation matrix" view of graph learning. Instead of building a rich graph neural architecture, it tries to preserve useful structural proximity in an efficient latent space.

These approaches were historically important because they made network representation learning concrete before the deep-learning wave took over. But the paper is also clear about their limitations. Large factorization problems can be memory-hungry, and matrix factorization is not naturally aligned with end-to-end supervised or semi-supervised training in the way later graph neural methods are.

**Random walks as sequence generators for graph representation**

The random-walk section is one of the clearest examples of graph learning borrowing ideas from another mature field, in this case language modeling. The key idea is simple but powerful: if you wander through a graph, the resulting sequences of nodes encode structural neighborhoods. Those sequences can then be treated analogously to sentences, and representation learning methods like Word2vec can be used to learn node embeddings.

Graph -> random walks -> node sequences -> skip-gram-like objective -> embeddings -> downstream graph task

This is the logic behind **DeepWalk** and **node2vec**, which the survey presents as representative methods for structure-based random walks. DeepWalk uses random walks plus a word-embedding objective to capture network neighborhoods. node2vec extends this by biasing the walk so it can interpolate between breadth-first and depth-first exploration. That matters because different tasks want different notions of similarity: community-style proximity is not the same as structural-role similarity.

The survey then expands the story beyond pure topology. Some networks also contain rich node information such as text, labels, or other attributes, and the random-walk literature responded by mixing structural and vertex information. The paper discusses **TADW**, **MMDW**, **Planetoid**, and **Struc2vec**, among others. Each makes a slightly different claim about what should be preserved: textual content, label information, structural identity, or a joint representation of graph structure and node attributes.

An important detail is that the random-walk worldview scales from nodes to larger objects. The paper mentions **Sub2Vec** for subgraphs and **graph2vec** for whole-graph representations. So the point is not merely "walk the graph." It is that random walks create flexible training signals for multiple granularity levels.

The survey also moves into more specialized network settings. In **heterogeneous networks**, random walks need to respect multiple node and edge types. This is especially important for knowledge graphs and social networks. The paper discusses relational-path approaches such as the path ranking algorithm, improvements to path-based inference, and knowledge-graph settings where relational semantics matter as much as raw proximity. It then turns to meta-path-based models such as **HIN2Vec** and **metapath2vec**, plus random-walk approaches that try to reduce dependence on hand-designed meta-paths.

The time dimension complicates the picture even further. In **time-varying networks**, old edges may disappear, new vertices may arrive, and paths need temporal consistency. The survey mentions methods like **CTDNE** and **HTNE**, which inject chronological or Hawkes-process structure into the embedding process. It also references **GraphSAGE** in the context of handling unseen vertices through neighborhood aggregation, showing that the boundaries between random-walk and neural methods are already becoming blurry by this point in the literature.

The authors end this section with a practical warning. Random walks are powerful because they are easy to sample and adapt, but their stochastic nature introduces uncertainty. Better coverage often requires many samples, and good performance can depend heavily on how the walk bias is tuned.

**Deep learning on graphs**

The deep-learning section is where the survey most clearly shows the field shifting from hand-engineered representations to trainable relational computation. The section begins with early graph neural network work and then divides the area into several major model families.

The first is **graph convolutional networks**, and here the survey distinguishes **spectral / time-domain methods** from **spatial / space-domain methods**. In the spectral line, the core question is how to generalize convolution to graphs through the Laplacian or related operators. The paper walks through the development from spectral graph CNNs to parameter-reduced kernels, Chebyshev approximations for localized filtering, and then the highly influential GCN of Kipf and Welling, which uses a simple first-order spectral approximation and a layer-wise propagation rule. The high-level pipeline is:

Node features + graph operator -> neighborhood aggregation / convolution -> updated node representations -> prediction

The spatial line takes a less explicitly spectral route. Instead of defining convolution through Fourier-style graph operators, these models define it directly in terms of local neighborhoods, ordered patches, diffusion processes, or message-passing structures in the graph itself. The survey mentions PATCHY-SAN, Neural Fingerprints, diffusion-convolutional networks, message-passing formulations, code-graph applications, dual GCNs, learnable large-scale GCNs, graph smoothing splines, and dynamic graph convolution variants. The point is that graph deep learning is not one architecture. It is a design space for learning on irregular local neighborhoods.

The next family is **graph attention networks**. Attention allows the model to weight neighbors unequally rather than aggregating them through fixed or symmetric rules. The paper discusses GAT, GAAN, GAM, and attention-based random-walk hybrids. What matters conceptually is that the graph neighborhood is no longer treated as a bag of equally informative neighbors. The model learns which neighbors matter more for a given task.

Then come **graph auto-encoders**. These are reconstruction-oriented models that learn latent graph representations and decode them back into edge statistics, neighborhood structure, or link probabilities. The survey includes approaches such as DNGR, SDNE, DRNE, variational graph auto-encoders, and adversarially regularized variants. This section shows a different use of graph learning: not directly classifying nodes, but learning a latent space good enough to reconstruct graph relations.

The survey also covers **graph generative networks**, where the model is trained to generate graphs or graph-like structures. Here the paper mentions systems such as MolGAN and DGMG and also connects generative thinking to knowledge-graph and zero-shot settings. The conceptual shift is from encoding or classifying a graph to modeling how a graph could have been produced.

Finally, the section turns to **graph spatial-temporal networks**, which try to model both graph structure and temporal evolution at the same time. Traffic forecasting is the clearest example in the paper. Each sensor is a node, the road network provides the edges, and the node values evolve over time. Methods like DCRNN and STGCN therefore combine graph convolution with recurrent or temporal components. This is one of the places where the survey shows graph learning growing beyond static network analysis into predictive systems.

The paper's own caution here is very brief but revealing: deep graph models inherit the optimization risks of deep learning more generally, including sensitivity to gradient-based training, local optima, and vanishing-gradient-style issues. The section is enthusiastic, but it does not pretend that neural graph models are effortless.

**Applications, datasets, and software ecosystem**

After the method taxonomy, the survey turns outward and asks where these approaches are actually used. It groups applications into structural scenarios, non-structural scenarios, and other scenarios. Structural scenarios are cases where relations are explicit, such as molecular systems, physical systems, and knowledge graphs. Non-structural scenarios are cases like text and images where graph structure is imposed or induced rather than given directly. Other scenarios include broader integration problems and combinatorial optimization.

The applications section begins with **datasets and open-source libraries**, which is more important than it may first appear. This is the paper acknowledging that graph learning had become an ecosystem, not just a set of papers. Datasets like Cora, PubMed, BlogCatalog, Wikipedia, and PPI provide standard benchmarks. Libraries like **OpenKE** and **CogDL** make the methods reusable enough to become research infrastructure.

In **text**, the survey shows how graph models can represent syntactic, semantic, or document-level relationships. GCNs, GATs, Text GCN, sentence-level graph models, syntactic GCNs, and gated graph neural networks appear in tasks such as text classification, sequence labeling, text generation, machine translation, and relation extraction. The broader lesson is that language can be turned into graph structure whenever token dependencies, sentence relations, or knowledge links matter.

In **images**, graph learning appears in social relationship understanding, image classification, visual question answering, object detection, region classification, and semantic segmentation. Here the graph is often a constructed object: regions, objects, people, or scene entities become nodes, and semantic or spatial relations become edges. This is the survey's way of showing that graph learning is not confined to naturally graph-shaped data.

In **science**, the paper highlights physical reasoning, chemistry, biology, and biomedical engineering. Interaction Networks and Visual Interaction Networks are used to reason about objects and physical systems. Molecular fingerprints can be learned with graph models. Protein interaction networks and biomedical relation graphs show up in biological and medical prediction problems. This section is important because it makes the relational bias of graph learning feel natural rather than artificial: many scientific systems really are networks of interacting entities.

In **knowledge graphs**, the survey distinguishes translational-distance models from semantic-matching models. The TransE family interprets relations as geometric translations in embedding space, while models like RESCAL, DistMult, and ANALOGY score plausibility through learned semantic interactions. The paper also discusses knowledge base completion, out-of-knowledge-base entities, cross-lingual alignment, and reinforcement-learning-style path finding such as DeepPath. This is one of the clearest cases where graph learning blends symbolic structure with continuous representation.

In **combinatorial optimization**, graph learning becomes a decision-making tool. Problems like the traveling salesman problem, minimum spanning tree, graph matching, and assignment problems can be attacked with neural architectures that exploit graph structure. The survey points to pointer-network-based reinforcement learning, GNN embeddings combined with Q-learning, and graph matching models that use learned vertex representations plus attention. This section broadens the paper's message: graph learning is not only for representation or prediction, but also for structured search and optimization.

**The paper's forward-looking questions**

The open-issues section is short, but it tells you what the authors thought the field still lacked in 2021. Four themes appear. **Dynamic graph learning** matters because many networks change over time and cannot be handled as fixed adjacency structures. **Generative graph learning** matters because learning to generate or evolve graphs could unify discriminative and generative perspectives. **Fair graph learning** matters because graph representations can encode and amplify sensitive or biased structural information. **Interpretability** matters because graph models are often effective while still behaving like black boxes.

What is notable here is that the paper's future-facing concerns are not only about accuracy. They are about temporal realism, modeling flexibility, social consequences, and scientific intelligibility. That is a sign that the survey sees graph learning as maturing from a method-centric topic into a wider research program.

---

## **Subtle points, clarifications, and limits**

- The paper uses `graph learning` very broadly, and at several points it slides toward `network representation learning` or `graph embedding`. That is not fatal, but it does mean the field boundary is intentionally loose rather than mathematically sharp.
- The survey is much broader than a GNN survey. One of its most important claims is that graph signal processing, factorization, random walks, and deep learning all belong in the same conceptual map.
- The taxonomy mixes theoretical lenses with algorithm families. That is why some boundaries blur in practice: hybrid models combine walks with GANs, deep models borrow spectral ideas, and inductive neighborhood methods spill across categories.
- The paper is strongest as a map of the field, not as a deep technical treatment of every subarea. Some sections, especially the application and open-issues discussions, are necessarily compressed relative to the size of the literature.
- The discussion of limitations is real but brief. Scalability, stochastic instability, memory cost, bias, and interpretability are mentioned, but the survey remains more synthetic than critical.

---

## **Closing perspective**

This paper is still worth understanding because it captures graph learning at the moment it had become too large to be treated as one niche technique and not yet so specialized that its internal connections were invisible. Its lasting value is not that it gives the final word on any single method family. Its value is that it teaches a clean mental picture: once data live on irregular relational structure, you can approach the problem spectrally, algebraically, probabilistically, sequentially, or neurally, but all of those approaches are responding to the same underlying fact that relations change what learning has to mean.

That is why the survey remains useful even after many individual model classes have advanced beyond it. It gives you the field's backbone. If you know the four categories, the recurring tasks, the major application zones, and the open issues around dynamics, fairness, generation, and interpretability, later work becomes much easier to place.

---

## **Personal comprehension notes**

The easiest way to remember this paper is: graph learning is what machine learning becomes when data points are connected and those connections are informative. In ordinary ML, rows are mostly treated as separate examples. In graph learning, each example partly gets its meaning from its neighborhood.

The four main families are really four different mental models:

- **Graph signal processing:** treat node values like signals laid over a network and ask how to filter, sample, reconstruct, or infer the graph.
- **Matrix factorization:** compress graph relationships into a lower-dimensional latent space while preserving neighborhood or proximity structure.
- **Random walks:** explore the graph to generate sequences, then learn embeddings from co-occurrence patterns the way language models learn from word contexts.
- **Deep learning on graphs:** let the model repeatedly aggregate or transform neighborhood information and learn the representation end to end.

Two memory hooks help:

- **Why the field exists:** irregular domain + heterogeneous structure + scale
- **How the field is organized:** signals, factorization, walks, neural models

Another helpful way to think about the paper is that it moves from "what makes graphs special?" to "what methods exploit that specialness?" to "where does that matter in practice?" That is the whole survey in one sentence.

---

## **Compact retention notes**

- **Paper type:** Broad survey and teaching-oriented field map
- **Core idea:** Unify graph learning as machine learning on relational, non-Euclidean data and organize the area into four major methodological families.
- **Main mechanism:** A taxonomy of GSP, matrix factorization, random walks, and deep graph models, followed by applications and open research directions.
- **Key result:** The paper gives a coherent conceptual map showing how graph structure can be represented, sampled, embedded, and learned across many tasks and domains.
- **Main limitation:** Breadth comes before depth; category boundaries blur, and the survey cannot fully analyze every fast-moving subliterature it includes.

---

## **Citations used in the paper**

- David I. Shuman, Sunil K. Narang, Pascal Frossard, Antonio Ortega, and Pierre Vandergheynst, *The Emerging Field of Signal Processing on Graphs: Extending High-Dimensional Data Analysis to Networks and Other Irregular Domains*, 2013 - foundational spectral framing for the survey's graph-signal-processing perspective.
- Antonio Ortega, Pascal Frossard, Jelena Kovacevic, Jose M. F. Moura, and Pierre Vandergheynst, *Graph Signal Processing: Overview, Challenges, and Applications*, 2018 - a major GSP overview that anchors the survey's treatment of graph signals, filtering, sampling, and applications.
- Bryan Perozzi, Rami Al-Rfou, and Steven Skiena, *DeepWalk: Online Learning of Social Representations*, 2014 - canonical example of random-walk-based node embedding through language-model-style training.
- Aditya Grover and Jure Leskovec, *node2vec: Scalable Feature Learning for Networks*, 2016 - extends walk-based embedding with biased exploration that trades off local homophily and structural-role similarity.
- Joan Bruna, Wojciech Zaremba, Arthur Szlam, and Yann LeCun, *Spectral Networks and Locally Connected Networks on Graphs*, 2013 - early deep-learning-on-graphs work that motivates graph convolution through spectral methods.
- Thomas N. Kipf and Max Welling, *Semi-Supervised Classification with Graph Convolutional Networks*, 2017 - one of the survey's central references for simple and influential graph convolution.
- Petar Velickovic, Guillem Cucurull, Arantxa Casanova, Adriana Romero, Pietro Lio, and Yoshua Bengio, *Graph Attention Networks*, 2018 - key reference for attention-weighted neighborhood aggregation.
- Will Hamilton, Zhitao Ying, and Jure Leskovec, *Inductive Representation Learning on Large Graphs*, 2017 - important for the survey's discussion of scalable, inductive graph representation learning for unseen nodes.
- Antoine Bordes, Nicolas Usunier, Alberto Garcia-Duran, Jason Weston, and Oksana Yakhnenko, *Translating Embeddings for Modeling Multi-Relational Data*, 2013 - cornerstone translational model in the survey's knowledge-graph section.
- Peter W. Battaglia, Razvan Pascanu, Matthew Lai, and Danilo Jimenez Rezende, *Interaction Networks for Learning about Objects, Relations and Physics*, 2016 - a representative science application showing graph learning as relational reasoning over physical systems.
- Irwan Bello, Hieu Pham, Quoc V. Le, Mohammad Norouzi, and Samy Bengio, *Neural Combinatorial Optimization with Reinforcement Learning*, 2017 - a representative citation for the survey's claim that graph learning reaches structured search and optimization problems.

---

