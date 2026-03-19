# Attention Is All You Need

**Paper link:** https://arxiv.org/pdf/1706.03762.pdf

---

## **Paper metadata**

**Authors / collaborators:**
- Ashish Vaswani
- Noam Shazeer
- Niki Parmar
- Jakob Uszkoreit
- Llion Jones
- Aidan N. Gomez
- Lukasz Kaiser
- Illia Polosukhin

**Organizations / companies / institutions involved:**
- Google Brain
- Google Research
- University of Toronto

**Publication date:**
12 June 2017 (arXiv preprint); later published at NeurIPS 2017

**Venue / source:**
NeurIPS 2017 / arXiv

**Research paper type / category:**
- Foundational / landmark paper
- Method / model paper
- Experimental / empirical paper

**Primary field / topic area:**
Sequence modeling, neural machine translation, and transformer architectures

**Keywords:**
- transformer
- self-attention
- sequence transduction
- positional encoding
- neural machine translation

---

## **Opening perspective**

This paper belongs to sequence modeling, but its real significance is architectural rather than task-specific. It is framed around machine translation, yet what it actually contributes is a new way to organize computation over sequences. Instead of treating recurrence as the default mechanism for handling ordered data, the paper asks whether attention alone can carry the full burden of representation building and generation. That sounds modest when stated abstractly, but it turned out to be a structural break with the dominant design language of the field.

Why the paper matters is that it does two hard things at once. It offers a concrete model, with enough detail to be trained and benchmarked, and it also changes the mental model of what a sequence model can be. If recurrence had been the standard answer to "how do we process tokens in order?", this paper replaces that answer with content-based interaction among all positions, plus an explicit mechanism for injecting position information. That is why it became the seed of the transformer era rather than merely a strong translation paper.

---

## **Full walkthrough and explanation**

**The problem the paper is reacting against**

Before the Transformer, the strongest sequence transduction systems were usually encoder-decoder models built around recurrent neural networks, especially LSTMs and GRUs, sometimes augmented by convolution and almost always improved by attention. Attention was already known to help. The deeper issue was that recurrence still imposed a sequential dependency in computation: the representation at position `t` depends on the one from position `t-1`, so training and inference carry an unavoidable left-to-right chain. That hurts parallelization and makes long-range dependency learning harder because signals must travel through many sequential steps.

The paper contrasts this with convolutional alternatives such as ByteNet and ConvS2S. Convolutions allow more parallel computation than RNNs, but distant positions still require multiple layers to communicate, so the path length between two far-apart tokens grows with distance or with the stack depth needed to bridge that distance. The Transformer is presented as a cleaner answer: let every position directly attend to every other relevant position, and let that be the core computation rather than an auxiliary mechanism.

The overall sequence pipeline is:

Input tokens -> embeddings + positional encodings -> encoder stack -> encoder representations -> decoder stack with masked self-attention + encoder-decoder attention -> linear projection + softmax -> next-token prediction

That pipeline is still encoder-decoder sequence transduction in the familiar sense. What changes is the internal machinery used to build and connect those representations.

**The high-level architecture**

The Transformer keeps the standard encoder-decoder form. The encoder maps an input sequence `(x1, ..., xn)` to contextual representations `(z1, ..., zn)`. The decoder then generates output tokens `(y1, ..., ym)` autoregressively, meaning each new token prediction depends on previously generated output tokens and on the encoder output. So the paper is not discarding sequence-to-sequence modeling. It is replacing the recurrent engine inside it.

The encoder consists of `N = 6` identical layers. Each layer contains two sublayers: a multi-head self-attention mechanism and a position-wise fully connected feed-forward network. Each sublayer is wrapped with a residual connection and followed by layer normalization. The paper writes this pattern as:

`LayerNorm(x + Sublayer(x))`

This is important because the Transformer is not just "attention plus softmax." It is a carefully composed stack in which attention and feed-forward transformations alternate, while residual connections and normalization stabilize optimization. The base configuration described through most of the paper uses `d_model = 512`, `d_ff = 2048`, and `h = 8` heads. The later big model mostly widens these dimensions rather than changing the core logic of the stack.

It is also worth noticing that this original formulation is what later literature calls post-norm: normalization happens after the residual addition. Many later large transformers switch to pre-norm for optimization stability, so the enduring transformer idea should not be confused with every exact implementation detail from the 2017 recipe.

The decoder also uses `N = 6` identical layers, but each decoder layer has three sublayers rather than two:

Masked decoder self-attention -> encoder-decoder attention -> position-wise feed-forward network

The masking in decoder self-attention is essential. The decoder is autoregressive, so when predicting position `i`, it must not look at tokens to the right. The paper enforces this by masking illegal future positions before the softmax, effectively setting their logits to negative infinity so they receive zero probability.

**Attention as the central primitive**

The paper defines attention as a function that takes a query together with key-value pairs and returns a weighted sum of values. The weights come from a compatibility function between the query and each key. In the Transformer, queries, keys, and values are all vectors, and in practice entire sets of them are packed into matrices `Q`, `K`, and `V`.

The core equation is:

$$
\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

This is scaled dot-product attention. Each row of `QK^T` measures how compatible a query is with every key. Dividing by `sqrt(d_k)` is not a cosmetic trick. The paper explains that when the key/query dimension `d_k` is large, raw dot products can become large in magnitude, pushing the softmax into regions with very small gradients. Scaling stabilizes optimization by keeping those values in a better numerical range.

So the attention pipeline is:

Queries + Keys -> dot products -> scale by `1 / sqrt(d_k)` -> softmax over keys -> weights over values -> weighted sum output

The paper compares this to additive attention and standard dot-product attention. Additive attention and dot-product attention can be similar in theoretical expressive power, but dot-product attention is faster and more space-efficient in practice because it maps well onto optimized matrix multiplication hardware. The scaling factor lets the model keep that efficiency while avoiding the optimization problems of unscaled large dot products.

**Why multi-head attention exists**

If one attention operation is useful, why not just make it larger? The paper's answer is multi-head attention. Instead of applying one attention function in the full model dimension, the model learns separate linear projections of queries, keys, and values multiple times and runs attention in parallel across those lower-dimensional projections.

The paper defines:

$$
\mathrm{MultiHead}(Q, K, V) = \mathrm{Concat}(head_1, ..., head_h)W^O
$$

where

$$
head_i = \mathrm{Attention}(QW_i^Q, KW_i^K, VW_i^V)
$$

Here `W_i^Q`, `W_i^K`, and `W_i^V` are learned projection matrices for head `i`, and `W^O` maps the concatenated head outputs back into model space. In the original model, the paper uses `h = 8` heads with `d_model = 512`, so each head uses `d_k = d_v = 64`.

The reason this matters is representational diversity. A single head has to compress all relational structure into one compatibility pattern. Multiple heads let the model attend to different types of relationships in parallel, across different representation subspaces and positions. The paper explicitly says that a single head can suffer from averaging effects that hide structure. Multi-head attention reduces that problem.

This yields three distinct uses of attention inside the model:

Encoder self-attention -> each input position attends to all input positions  
Decoder self-attention -> each output position attends to earlier output positions only  
Encoder-decoder attention -> each decoder position attends to all encoder positions

Those three uses are easy to blur together, but the distinction is critical. Encoder self-attention builds contextualized representations of the source sentence. Decoder self-attention models already generated target-side context. Encoder-decoder attention is the bridge that lets target generation condition on the source.

**The feed-forward sublayer and what attention does not do**

Each encoder and decoder layer also contains a position-wise feed-forward network:

$$
\mathrm{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2
$$

This network is applied independently to each position. The same feed-forward transformation is reused across positions within a layer, but each layer has its own parameters. The paper notes that this is equivalent to two `1 x 1` convolutions with a ReLU in between. In the base model, input/output dimension is `d_model = 512`, and the hidden dimension is `d_ff = 2048`.

This sublayer matters because attention is doing token-to-token communication, but the model still needs learned nonlinear transformation at each position after information has been mixed. The Transformer is therefore not "only attention" in the literal sense of every operation. The phrase means that recurrence and convolution are removed as sequence-processing primitives. The architecture still uses feed-forward layers, embeddings, residual connections, normalization, and output projection.

**Embeddings, weight tying, and autoregressive generation**

Input tokens and output tokens are mapped into vectors of dimension `d_model` through learned embeddings. The paper also shares the same weight matrix across the two embedding layers and the linear transformation before the softmax. That matters because the reported gains are not coming from an unnecessarily bloated parameterization; the authors are already using parameter-sharing tricks that had proven useful in related sequence models. The embeddings are multiplied by `sqrt(d_model)` before being combined with positional encodings.

On the decoder side, prediction is autoregressive:

Previous target tokens -> target embeddings + positional encodings -> masked decoder stack -> vocabulary logits -> softmax -> next-token probabilities

The "shifted right" target input is important. During training, the decoder receives the gold target sequence offset by one position, so prediction at position `i` only conditions on positions `< i`. The masking makes that causal structure explicit.

**How the model handles order without recurrence**

Because the architecture removes recurrence and convolution, it loses any built-in notion of token order. The paper solves this by adding positional encodings to the token embeddings at the bottoms of the encoder and decoder stacks. Since positional encoding vectors have the same dimensionality as token embeddings, they can be added directly.

The paper experiments with learned and fixed positional encodings and reports similar results. It chooses sinusoidal positional encodings:

$$
PE_{(pos, 2i)} = \sin(pos / 10000^{2i/d_{model}})
$$

$$
PE_{(pos, 2i+1)} = \cos(pos / 10000^{2i/d_{model}})
$$

Here `pos` is the token position and `i` indexes dimensions. Even dimensions use sine, odd dimensions use cosine, and the wavelengths form a geometric progression. The motivation is subtle and important: for a fixed offset `k`, `PE_{pos+k}` can be represented as a linear function of `PE_pos`, which may make relative-position reasoning easier to learn. The paper also suggests sinusoidal encodings may extrapolate better to longer sequence lengths than purely learned positional embeddings.

So the ordering pipeline is:

Token embedding -> add position signal -> contextual mixing through attention -> deeper contextual representations

This is one of the paper's deepest conceptual moves. Sequence order is no longer hardwired through recurrence. It becomes explicit information injected into a model whose main interaction rule is attention.

**Why self-attention is worth preferring**

The paper does not just introduce self-attention and assume it is good. It gives a comparative argument along three dimensions: per-layer computational complexity, amount of sequential computation, and maximum path length between distant positions. Path length matters because if two tokens need many processing steps to influence one another, learning long-range dependencies becomes harder.

The key comparison in the paper is:

Self-attention -> `O(1)` sequential operations -> `O(1)` maximum path length between positions  
Recurrence -> `O(n)` sequential operations -> `O(n)` path length  
Convolution -> parallelizable but requires deeper stacks to connect distant positions

There is an important qualification. Full self-attention has `O(n^2 * d)` complexity per layer because every position attends to every other position. For sentence-level machine translation, where sequence lengths are often smaller than representation dimensionality, this tradeoff is favorable. For very long sequences, the quadratic cost becomes a real limitation. The paper briefly mentions restricted self-attention over neighborhoods of size `r` as a possible future direction, which later became a major line of efficiency research.

The paper also notes that self-attention may be more interpretable, because one can inspect attention distributions and see some heads apparently specializing in syntactic or positional behavior. That claim should not be overstated, but it helps explain why the architecture became attractive scientifically as well as computationally.

**Training data, optimization, and regularization**

The training recipe is more specific than people often remember. For WMT 2014 English-to-German, the paper uses about 4.5 million sentence pairs and a shared source-target byte-pair vocabulary of about 37,000 tokens. For WMT 2014 English-to-French, it uses 36 million sentence pairs and a 32,000 word-piece vocabulary. Batches are grouped by approximate sequence length and contain about 25,000 source tokens and 25,000 target tokens. That matters because the paper's efficiency argument is tied to sentence-level machine translation with subword tokenization, not to arbitrarily long-context modeling.

The optimizer is Adam with `beta1 = 0.9`, `beta2 = 0.98`, and `epsilon = 1e-9`, together with a custom learning-rate schedule:

$$
lrate = d_{model}^{-0.5} \cdot \min(step\_num^{-0.5}, step\_num \cdot warmup\_steps^{-1.5})
$$

This schedule does two things. During the warmup phase, the learning rate increases with step number. After warmup, it decays proportionally to the inverse square root of the step. Scaling by `d_model^{-0.5}` adjusts the schedule to the representation size, and the paper sets `warmup_steps = 4000`. This "warmup then inverse-square-root decay" pattern became one of the most copied details from the paper.

Hardware and runtime are also part of the claim. The base model trains for `100,000` steps, about 12 hours on 8 NVIDIA P100 GPUs, while the big model trains for `300,000` steps, about 3.5 days. That is why the paper keeps emphasizing not just accuracy but quality per training cost.

The model also uses dropout in multiple places, including on sublayer outputs, on attention weights, and on the sums of embeddings plus positional encodings. For the base model, `Pdrop = 0.1`. It also applies label smoothing with `epsilon_ls = 0.1` during training. Label smoothing slightly relaxes the target distribution away from a hard one-hot target, which hurts perplexity but often improves accuracy and BLEU. These are not cosmetic training details; they are part of how the reported results were made to work reliably.

**What the experiments actually show**

The paper evaluates the Transformer primarily on machine translation. On WMT 2014 English-to-German, the base Transformer reaches 27.3 BLEU and the big Transformer reaches 28.4 BLEU, surpassing previous best results including ensembles. On WMT 2014 English-to-French, the big model reaches 41.8 BLEU as a single model after 3.5 days of training on eight GPUs, which the paper emphasizes is only a fraction of the training cost of earlier best systems.

These numbers matter, but the deeper empirical claim is about the combination of quality and efficiency. The paper is not saying "attention can work too." It is saying that an attention-only architecture can outperform strong recurrent and convolutional baselines while also being substantially more parallelizable.

The inference recipe behind those BLEU scores is easy to miss. For base models, the authors average the last 5 checkpoints saved at 10-minute intervals; for big models, they average the last 20. Decoding uses beam search with beam size 4 and length penalty `alpha = 0.6`, and output length is capped at input length + 50 with early stopping when possible. So the headline result is the performance of the full recipe, not merely of the bare architecture in isolation.

The paper also includes ablations and variations that clarify what is doing the work. Single-head attention is about 0.9 BLEU worse than the best multi-head setting, too many heads under fixed compute also hurt, reducing the key dimension damages quality, bigger models help, and dropout is important for avoiding overfitting. One especially useful observation is that learned positional embeddings and sinusoidal encodings perform nearly identically in the reported setup. That tells you the main gain is not coming from one magical positional trick; it is coming from the broader attention-centered architecture.

An often-overlooked part of the paper is the constituency parsing experiment. The authors use the Transformer successfully on English constituency parsing with both large and limited training data, which broadens the paper's claim beyond "good translation system." Even though parsing is not the main focus of the paper, its inclusion helps show that the architecture is not being sold as a translation-specific hack.

**How to interpret the paper historically**

Read carefully, the paper is both narrow and enormous. Narrow because it is solving sequence transduction with a specific encoder-decoder model on specific benchmarks. Enormous because the design principle underneath it is broader: representation building can be organized around pairwise token interaction rather than recurrent state propagation. The paper does not present the giant language-model ecosystem people now associate with transformers. But it introduces the primitive that made those later systems natural.

Its importance also comes from the way the pieces fit together. Self-attention alone would not have been enough. The paper combines scaled dot-product attention, multi-head factorization, residual connections, layer normalization, feed-forward sublayers, tied embeddings, positional encoding, masking, and a stable training schedule into one coherent architecture. That coherence is why the model could be adopted and extended so quickly.

---

## **Subtle points, clarifications, and limits**

The title is easy to overread. The paper does not mean that every useful operation in the model is attention; feed-forward layers, embeddings, normalization, residual paths, masking, and output projection are all essential. It also does not prove that attention has no scaling problems. The original model has quadratic cost in sequence length, which later became one of the central engineering pressures in transformer research. And while attention maps are often visually appealing, the paper's comments about interpretability should be taken as suggestive rather than as a full theory of what attention weights mean.

It is also important to remember that the original Transformer here is the post-norm version, uses fixed sinusoidal positional encodings, and assumes full quadratic self-attention over sentence-length inputs. Later transformer practice often changes each of those details while preserving the central insight. So the enduring contribution is the attention-first computational pattern, not a frozen checklist of 2017 hyperparameters.

---

## **Closing perspective**

This paper changed the field because it replaced a default assumption. After it, recurrence was no longer the obvious backbone for sequence models; content-based interaction plus explicit position signals became the new center of gravity. The transformer made sequence processing more parallel, shortened the effective path between distant tokens, and provided a design that later scaled into BERT, GPT-style language models, translation systems, vision transformers, and many multimodal variants. It has rare cross-community status: canonical in NLP, central in modern deep learning, and still worth understanding in detail because so much of current AI is either a direct extension of it or a response to its limitations.

---

## **Personal comprehension notes**

The way to think about the Transformer is: every token gets to look around the whole sentence, decide what matters for its current role, and rebuild itself from those interactions. Instead of passing information along a chain step by step, the model creates a communication pattern over positions and updates all positions in parallel. That is the conceptual jump.

Another useful mental model is that the architecture separates three jobs cleanly. Attention decides who should talk to whom. Feed-forward layers decide how each position should transform what it learned. Positional encodings tell the model where each token sits in the sequence. Once you see those three jobs, the whole design becomes much easier to remember.

A third mental model is to treat each self-attention layer as building a temporary weighted graph over token positions. Each head draws its own graph, the feed-forward network rewrites each node after message passing, and stacking layers repeats that process. Seen that way, the architecture is less mysterious: it is repeated communication plus local rewriting, with position information injected from the start.

---

## **Compact retention notes**

- **Paper type:** Foundational / landmark method paper
- **Core idea:** Replace recurrence and convolution in sequence transduction with attention-based interaction plus explicit position information.
- **Main mechanism:** Scaled dot-product attention, multi-head attention, encoder-decoder stacks, positional encodings, and masked autoregressive decoding.
- **Key result:** The Transformer achieves state-of-the-art translation quality with substantially better parallelization and lower training cost than strong recurrent baselines.
- **Main limitation:** Full self-attention has quadratic cost in sequence length, which becomes a bottleneck for very long contexts.

---

## **Citations used in the paper**

- Jimmy Lei Ba, Jamie Ryan Kiros, Geoffrey E. Hinton, *Layer Normalization*, 2016
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, *Neural Machine Translation by Jointly Learning to Align and Translate*, 2014
- Kyunghyun Cho et al., *Learning Phrase Representations Using RNN Encoder-Decoder for Statistical Machine Translation*, 2014
- Jonas Gehring et al., *Convolutional Sequence to Sequence Learning*, 2017
- Nal Kalchbrenner et al., *Neural Machine Translation in Linear Time*, 2017
- Kaiming He et al., *Deep Residual Learning for Image Recognition*, 2016
- Diederik P. Kingma, Jimmy Ba, *Adam: A Method for Stochastic Optimization*, 2015
- Ofir Press, Lior Wolf, *Using the Output Embedding to Improve Language Models*, 2016
- Rico Sennrich, Barry Haddow, Alexandra Birch, *Neural Machine Translation of Rare Words with Subword Units*, 2015
- Christian Szegedy et al., *Rethinking the Inception Architecture for Computer Vision*, 2015 — source of the label-smoothing idea used in the training recipe
- Ilya Sutskever, Oriol Vinyals, Quoc V. Le, *Sequence to Sequence Learning with Neural Networks*, 2014
- Yonghui Wu et al., *Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation*, 2016
