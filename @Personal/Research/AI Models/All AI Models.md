---
tags:
  - AI
  - machine-learning
  - reference
  - MOC
aliases:
  - AI Model Types
  - Machine Learning Models
created: 2026-05-16
type: MOC
---

# All AI Models

A taxonomy of AI model architectures. Organized by architectural family as the primary axis. Training paradigms, deployment patterns, and modalities are **orthogonal modifiers** — not model types in themselves.

---

## 1. Classical & Statistical

| # | Architecture | Examples / Notes |
|---|---|---|
| 1 | Linear models | Linear/logistic regression, ridge, lasso, elastic net, GLMs, GAMs |
| 2 | Decision trees | CART, ID3, C4.5 |
| 3 | Ensemble tree models | Random forests, extra trees, bagging |
| 4 | Gradient boosted trees | XGBoost, LightGBM, CatBoost, AdaBoost variants |
| 5 | Kernel machines | SVMs, kernel regression, one-class SVM |
| 6 | k-nearest neighbor models | Instance-based, lazy learning |
| 7 | Naive Bayes models | Gaussian, multinomial, Bernoulli variants |
| 8 | Gaussian process models | Non-parametric Bayesian regression and classification |
| 9 | Bayesian network models | Directed probabilistic graphical models |
| 10 | Hidden Markov models | Sequence labeling, generative sequences |
| 11 | Conditional random field models | Discriminative sequence labeling |
| 12 | Gaussian mixture models | Soft clustering, density estimation |
| 13 | Clustering models | k-means, hierarchical, DBSCAN, HDBSCAN, spectral, mean-shift |
| 14 | Linear dimensionality reduction | PCA, ICA, NMF, factor analysis |
| 15 | Manifold learning models | t-SNE, UMAP |
| 16 | Classical anomaly detection | Isolation forest, LOF, robust covariance |
| 17 | Survival analysis models | Cox proportional hazards, accelerated failure time |
| 18 | Causal inference models | Propensity score, uplift, do-calculus models |

---

## 2. Core Deep Learning

| # | Architecture | Examples / Notes |
|---|---|---|
| 19 | Multilayer perceptron | Feedforward networks, wide networks |
| 20 | Convolutional neural networks | CNN, ConvNeXt, U-Net, ResNet-style |
| 21 | Recurrent neural networks | RNN, LSTM, GRU |
| 22 | Transformer (encoder) | BERT-style bidirectional, e.g. RoBERTa |
| 23 | Transformer (decoder) | GPT-style autoregressive, causal LM |
| 24 | Transformer (encoder–decoder) | T5, BART, machine translation style |
| 25 | Vision Transformer | ViT, DeiT, Swin Transformer |
| 26 | Mixture-of-experts models | MoE layers, sparse gating |
| 27 | Graph neural networks | GCN, GAT, GraphSAGE, GIN, MPNN |
| 28 | Autoencoders | Reconstruction-based representation learning |
| 29 | Variational autoencoders | VAE, β-VAE, VQ-VAE |
| 30 | Generative adversarial networks | GAN, StyleGAN, CycleGAN, conditional GAN |
| 31 | Diffusion models | DDPM, score-based, latent diffusion, classifier-free guidance |
| 32 | Flow matching models | Continuous normalizing flows, OT-CFM |
| 33 | Normalizing flow models | RealNVP, Glow, NICE |
| 34 | Energy-based models | EBM, contrastive divergence training |
| 35 | State-space models | S4, Mamba, RWKV, linear RNN |
| 36 | Hybrid Transformer–SSM models | Jamba, Zamba, Hymba |
| 37 | Neural ODE models | Neural ordinary/stochastic differential equations |
| 38 | Memory networks / NTM | Neural Turing machines, Differentiable Neural Computers |
| 39 | Capsule networks | CapsNet, dynamic routing |
| 40 | Hypernetworks | Networks that generate weights for another network |
| 41 | Hopfield / Modern Hopfield networks | Associative memory; attention as Hopfield retrieval |
| 42 | Restricted Boltzmann machines | RBM, deep Boltzmann machines |
| 43 | Radial basis function networks | RBF networks |
| 44 | Mixture density networks | MDN — outputs a mixture of Gaussians |
| 45 | Kolmogorov-Arnold Networks | KANs — learnable activation functions on edges |
| 46 | Spiking neural networks | Neuromorphic / event-driven computation |

---

## 3. Retrieval & Search

| # | Architecture | Examples / Notes |
|---|---|---|
| 47 | Sparse retrieval models | BM25, TF-IDF, SPLADE, learned sparse |
| 48 | Dense retrieval models | Bi-encoder, DPR, embedding-based retrieval |
| 49 | Cross-encoder / reranker models | Full attention over query + document pair |
| 50 | Two-tower retrieval models | Separate query and item encoders |
| 51 | Hybrid retrieval models | Sparse + dense combined |

---

## 4. Self-Supervised & Representation

| # | Architecture | Examples / Notes |
|---|---|---|
| 52 | Contrastive learning models | SimCLR, MoCo, BYOL, CLIP, SigLIP |
| 53 | Masked language models | BERT, RoBERTa, ELECTRA — predict masked tokens |
| 54 | Masked image modeling | MAE, BEiT, SimMIM — predict masked patches |
| 55 | Word embedding models | Word2Vec, GloVe, FastText — static embeddings |
| 56 | Meta-learning models | MAML, Prototypical Networks, few-shot learning |
| 57 | Neural process models | Conditional/attentive neural processes |

---

## 5. Sequence & Language

| # | Architecture | Examples / Notes |
|---|---|---|
| 58 | n-gram / bag-of-words models | Classical count-based language models |
| 59 | Large language models | Scaled decoder Transformers, 1B+ parameters |
| 60 | Reasoning models | Chain-of-thought, process reward models, o1-style |
| 61 | Diffusion language models | Masked diffusion, absorbing-state diffusion over tokens |
| 62 | Sequence-to-sequence models | Encoder-decoder for translation, summarization |

---

## 6. Scientific & Physics-Based

| # | Architecture | Examples / Notes |
|---|---|---|
| 63 | Physics-informed neural networks | PINNs — embed PDEs as loss constraints |
| 64 | Neural operators | FNO, DeepONet, GNO — learn mappings between function spaces |
| 65 | Surrogate / emulator models | Replacing expensive simulations with learned approximations |
| 66 | Protein language models | ESM, Progen, Evo — sequence-based protein models |
| 67 | Molecular graph models | MPNN, SchNet, DimeNet for atoms and bonds |
| 68 | Bayesian optimization models | GP-based or neural acquisition function models |

---

## 7. 3D & Spatial

| # | Architecture | Examples / Notes |
|---|---|---|
| 69 | Neural radiance fields | NeRF and variants — implicit volumetric scene representation |
| 70 | Gaussian splatting models | 3DGS — explicit point-based scene representation |
| 71 | Point cloud models | PointNet, PointNet++, Point Transformer |
| 72 | Implicit neural representations | SDF, occupancy networks, coordinate networks |
| 73 | Voxel models | 3D grid-based spatial representations |
| 74 | Mesh generation models | Direct surface mesh output |

---

## 8. Reinforcement Learning

| # | Architecture | Examples / Notes |
|---|---|---|
| 75 | Value-based RL models | Q-learning, DQN, Double DQN, Dueling DQN, Rainbow |
| 76 | Policy gradient models | REINFORCE, VPG |
| 77 | Actor-critic models | A2C, A3C, PPO, SAC, TD3, DDPG |
| 78 | Model-based RL / world models | Dreamer, MuZero — learn environment dynamics |
| 79 | Monte Carlo tree search models | MCTS, AlphaZero, MuZero planning |
| 80 | Offline RL models | Conservative Q-learning, TD3+BC, IQL |
| 81 | Inverse RL / imitation learning | IRL, behavior cloning, GAIL |
| 82 | Multi-agent RL models | MADDPG, QMIX, cooperative and competitive settings |
| 83 | Hierarchical RL models | Options framework, goal-conditioned policies |
| 84 | Bandit models | Multi-armed bandits, contextual bandits, Thompson sampling |

---

## 9. Reasoning & Symbolic

| # | Architecture | Examples / Notes |
|---|---|---|
| 85 | Neuro-symbolic models | Neural networks + logic rules, constraint satisfaction, ILP |
| 86 | Automated theorem-proving models | Formal proof search, tactic suggestion |
| 87 | Causal graph models | Structural causal models, do-calculus networks |
| 88 | Knowledge graph embedding models | TransE, DistMult, ComplEx, RotatE |

---

## Orthogonal Modifiers

These are **not** model types. They are properties that can be applied to any architecture above.

### Training Paradigm
- Supervised
- Unsupervised
- Self-supervised
- Semi-supervised
- Weakly supervised
- Reinforcement learning
- Multi-task learning
- Transfer learning
- Few-shot / meta-learning
- Zero-shot
- Federated learning
- Online / continual learning
- Knowledge distillation
- Fine-tuning
- Instruction tuning
- Preference tuning (RLHF / DPO)

### Scale & Deployment Pattern
- Foundation model (large-scale pretrain)
- Distilled / compressed
- Quantized
- Edge / on-device
- Ensemble
- Mixture-of-experts (deployment)

### System Pattern
- Retrieval-augmented generation (RAG)
- Agentic / tool-using
- Multi-agent system
- Human-in-the-loop

### Data Modality
- Text
- Image
- Video
- Audio / speech
- Code
- Tabular / structured
- Time series
- Graph / network
- 3D / spatial
- Molecular / protein sequence
- Multimodal

---

## Mental Map

> **Input data type → task type → architecture family → deployment constraint**

| Goal | Start here |
|---|---|
| Predict a number, class, or score | Classical & Statistical, Core Deep Learning |
| Generate new content | Diffusion, GAN, VAE, Autoregressive (LLM) |
| Turn data into embeddings | Contrastive, Masked LM, Masked Image |
| Find relevant information | Retrieval & Search |
| Order results by usefulness | Cross-encoder / reranker |
| Choose actions over time | Reinforcement Learning |
| Solve multi-step problems | Reasoning models, Neuro-symbolic |
| Work on 3D or physical space | 3D & Spatial |
| Work on molecules or physics | Scientific & Physics-Based |
