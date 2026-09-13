# Neural Machine Translation by Jointly Learning to Align and Translate

**Paper link:** https://arxiv.org/abs/1409.0473

---

## **Paper metadata**

**Authors / collaborators:**  
- Dzmitry Bahdanau
- Kyunghyun Cho
- Yoshua Bengio

**Organizations / companies / institutions involved:**  
- Jacobs University Bremen
- Universite de Montreal
- CIFAR

**Publication date:**  
1 September 2014 as an arXiv preprint; later presented at ICLR 2015

**Venue / source:**  
arXiv / ICLR 2015

**Research paper type / category:**  
- Foundational / landmark paper
- Method / model paper
- Experimental / empirical paper

**Primary field / topic area:**  
Neural machine translation, sequence-to-sequence learning, and attention mechanisms

**Keywords:**  
- neural machine translation
- attention
- alignment
- encoder-decoder
- bidirectional RNN

---

## **Opening perspective**

This paper sits at the moment when neural machine translation was starting to look plausible but still carried an obvious weakness: the model had to read an entire source sentence, compress everything into one fixed-size vector, and then somehow decode a full translation from that bottleneck. That worked surprisingly well on shorter sentences, but it was also visibly brittle. Bahdanau, Cho, and Bengio do not throw away the encoder-decoder idea. Instead, they make a subtler and more important move: they let the decoder revisit the source sentence while generating each target word.

That sounds like a modest architectural tweak, but it changed the field's mental model. Translation no longer had to mean "encode once, then decode from memory." It could mean "build a distributed memory over the source sentence, then learn where to look at each decoding step." This paper matters because it turns alignment from an external statistical object into a differentiable, trainable part of the model itself, and in doing so it establishes the core intuition behind modern attention.

---

## **Full walkthrough and explanation**

**The bottleneck the paper is reacting against**

The paper starts from the encoder-decoder view of translation. A source sentence `x = (x_1, ..., x_{T_x})` is read by an encoder RNN, producing hidden states that are then collapsed into a context vector `c`. A decoder RNN uses that context together with previously generated target words to model the target sentence `y = (y_1, ..., y_{T_y})`. In the basic formulation, the decoder assigns probability by factorizing translation word by word:

$$
p(\mathbf{y}) = \prod_{t=1}^{T_y} p(y_t \mid y_{<t}, c)
$$

The key concern is not that this formulation is mathematically invalid. It is that the whole source sentence, regardless of length or complexity, has to be squeezed into the same fixed-length representation `c`. The paper treats this as a capacity bottleneck, and it argues, correctly, that the bottleneck becomes most painful on longer sentences. This is one of the most important framing moves in the paper, because it shifts the question from "can encoder-decoder work at all?" to "what information access pattern should a decoder have while translating?"

**How the new architecture changes the translation pipeline**

The proposed pipeline is:

Source sentence -> bidirectional encoder annotations `h_j` -> alignment scores `e_{ij}` -> attention weights `alpha_{ij}` -> context vector `c_i` for target step `i` -> decoder state update `s_i` -> deep output layer -> next target word

What changes here is that the model no longer uses one global context vector for the whole target sentence. It computes a distinct context vector `c_i` for each target word `y_i`. So instead of saying "here is the entire source sentence in one vector; now decode everything from it," the model says "for the next output word, form a context that emphasizes whichever source positions are most relevant right now."

This is the conceptual birth of attention in mainstream sequence modeling. The decoder is no longer forced to remember the entire source perfectly at all times. It can query a structured representation of the source as generation unfolds.

**What the encoder actually produces**

The encoder is not a plain left-to-right RNN. It is a bidirectional RNN. For each source position `j`, the model computes a forward hidden state and a backward hidden state, then concatenates them into an annotation:

$$
h_j = [\overrightarrow{h}_j^\top ; \overleftarrow{h}_j^\top]^\top
$$

This matters because an annotation is not meant to represent only the current source word in isolation. It is meant to represent that word together with left and right context. The paper emphasizes that each annotation contains information about the whole sentence with strong focus around position `j`. In practical terms, `h_j` becomes a context-aware memory slot for source token `x_j`.

That design choice is easy to overlook historically because later attention models often operate over transformer states rather than bidirectional RNN annotations. But in this paper the bidirectional encoder is doing essential work. It makes the attention mechanism more useful because the model attends to context-rich source representations, not bare word embeddings.

**The alignment mechanism is the real innovation**

For each target step `i`, the model computes a context vector as a weighted sum of source annotations:

$$
c_i = \sum_{j=1}^{T_x} \alpha_{ij} h_j
$$

The weights are normalized scores:

$$
\alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k=1}^{T_x}\exp(e_{ik})}
$$

where

$$
e_{ij} = a(s_{i-1}, h_j)
$$

The score `e_{ij}` tells the model how relevant source position `j` is when predicting target word `i`, given the decoder's previous hidden state `s_{i-1}`. In the appendix the alignment model is parameterized as a small feedforward network:

$$
a(s_{i-1}, h_j) = v_a^\top \tanh(W_a s_{i-1} + U_a h_j)
$$

This is the classic additive attention form that later literature often calls Bahdanau attention. It is not self-attention and it is not dot-product attention. It is a learned compatibility function between a decoder-side state and an encoder-side annotation.

The paper gives a particularly good intuition for the weighted sum. It says `c_i` can be interpreted as an expected annotation under a distribution over possible alignments. That is a clean way to understand the difference between older hard-alignment thinking and this new soft alignment. Instead of choosing one source position discretely, the model forms a differentiable probability distribution over all source positions. That is why the whole mechanism can be trained jointly with backpropagation.

This is a major departure from classical statistical machine translation. Alignment is no longer a separately estimated latent structure that sits outside the translation model. It becomes an internal computation that exists only insofar as it helps prediction.

**Why soft alignment helps translation**

The paper repeatedly uses the word "soft-search," and that wording is revealing. The model is not cutting the source sentence into explicit segments or committing to a single source word for each target word. It is softly consulting many positions with different strengths. That matters because translation often depends on local combinations rather than one-to-one word correspondences.

The paper's own example is helpful: translating English `[the man]` into French `[l' homme]` is not well captured by a rigid alignment that maps `[the]` only to `[l']` and `[man]` only to `[homme]`. The correct French article depends on the noun that follows. Soft alignment lets the model look at both words when generating the article. This is one of the clearest arguments in the paper, because it shows that attention is not merely about locating a single source token; it is about constructing the right local source context for the next target decision.

It also naturally handles source and target phrases of different lengths. Phrase-based SMT needed explicit machinery for null alignments and phrase extraction. Here, the weighted context can spread mass over multiple source positions without introducing separate symbolic alignment bookkeeping.

**What the decoder is doing at each step**

The decoder remains recurrent, and this is important historically. The paper has not abolished recurrence. It has changed what recurrence has access to.

The decoder state is updated by a gated recurrent unit style mechanism:

$$
s_i = (1 - z_i) \circ s_{i-1} + z_i \circ \tilde{s}_i
$$

where the candidate state `\tilde{s}_i` depends on the previous target word embedding, the reset-gated previous hidden state, and the new context vector `c_i`. The update gate `z_i` controls how much of the old state to keep, while the reset gate `r_i` controls how much of the previous state to use when proposing a candidate update. This is early GRU-era recurrent modeling, not LSTM, though the paper explicitly notes that LSTMs could also have been used.

That detail matters for interpretation. The model's improvement does not come from replacing recurrence with something more parallel, as the Transformer later would. It comes from giving the recurrent decoder dynamic access to source-side information at every output step.

The output distribution itself is computed through what the paper calls a deep output with a single maxout hidden layer. This is not the part of the model that became historically famous, but it is part of the real architecture used in the experiments, and it helps explain why the note "attention mechanism" should not be mistaken for the whole system. The paper's practical model is a fairly rich RNN-based translation architecture whose decisive novelty is the alignment-conditioned context.

**Why bidirectionality and per-step attention fit together**

There is a nice architectural symmetry here. The encoder builds one annotation per source position, and each annotation already knows something about both left and right context because of the bidirectional pass. The decoder then decides how much each annotation should matter for the current target step. That means the attention mechanism is not retrieving isolated words but context-shaped source positions.

The flow is therefore:

Source tokens -> forward and backward recurrent summaries -> annotation per source position -> decoder query against all annotations -> weighted source summary for the current target word

Seen this way, the paper is solving a memory-access problem. The source sentence is stored as many contextualized memory cells instead of one compressed vector, and the decoder learns a content-dependent retrieval rule over those cells.

**What the experiments are actually testing**

The experiments are on English-to-French translation using the WMT '14 parallel corpora. The raw pool contains about 850 million words across Europarl, News Commentary, UN, and two crawled corpora. Following earlier work, the authors reduce that to 348 million words using data selection from Axelrod, He, and Gao. The development set is `news-test-2012` plus `news-test-2013`, and the test set is `news-test-2014` with 3003 sentences.

The preprocessing is historically important because it also reveals a limitation. The authors use a shortlist of the 30,000 most frequent words in each language and map everything else to `[UNK]`. They do not use lowercasing, stemming, or subword segmentation. This means the paper's model is fighting two different problems at once: sentence-level compression and rare-word handling. Attention directly addresses the first, but not the second.

The authors train four main neural systems: `RNNencdec-30`, `RNNsearch-30`, `RNNencdec-50`, and `RNNsearch-50`, where the suffix indicates whether the model saw sentences up to length 30 or 50 during training. The encoder and decoder hidden size is `1000`; the embedding size is `620`; the maxout hidden layer size is `500`; and the alignment model hidden size is `1000`. Training uses minibatch SGD with Adadelta, minibatches of `80` sentences, gradient norm clipping, and about five days of training per model. Decoding uses beam search.

These details matter because the paper is not claiming a purely conceptual toy result. It is reporting a serious system comparison under matched training conditions between a basic encoder-decoder and the new attention-based model.

**What the numbers actually show**

The headline quantitative result is that `RNNsearch` dramatically outperforms the basic `RNNencdec` baseline. On the full test set, `RNNencdec-30` gets `13.93` BLEU while `RNNsearch-30` gets `21.50`; `RNNencdec-50` gets `17.82` while `RNNsearch-50` gets `26.75`. A longer-trained version, `RNNsearch-50*`, reaches `28.45`.

That alone is a large jump and strongly supports the paper's bottleneck diagnosis. One especially telling comparison is that `RNNsearch-30` still beats `RNNencdec-50`. In other words, the architectural change is doing more than merely allowing the model to see longer sentences during training.

The comparison with `Moses`, the phrase-based system, needs to be read carefully. On the full test set `Moses` gets `33.30` BLEU, still well above the neural systems. On the subset of sentences without unknown words, however, `RNNsearch-50*` reaches `36.15`, slightly above `Moses` at `35.63`. So the paper's claim of being comparable to phrase-based SMT is directionally right, but only under the known-word condition. Overall performance still lags, and the reason is not mysterious: the fixed shortlist and `[UNK]` handling remain serious weaknesses.

That is an important place to correct an overly celebratory reading. This paper is not yet the moment when neural MT cleanly dominates phrase-based SMT in every practical sense. It is the moment when neural MT becomes clearly credible as a full translation architecture, especially once the fixed-vector bottleneck is removed.

**Why sentence length matters so much**

Figure 2 is central to the paper's argument. The basic encoder-decoder deteriorates sharply as source sentences grow longer, while `RNNsearch` is substantially more robust. `RNNsearch-50` in particular shows little deterioration even for sentences of length 50 or more.

This is exactly what one would expect if the fixed-length context vector were the main failure point. Long sentences contain more clauses, more reorderings, more local dependencies, and more opportunities for the decoder to need information that was not preserved cleanly in one compressed vector. By recomputing `c_i` at each step, attention turns "remember the whole source perfectly" into the easier problem "retrieve the relevant part of the source when needed."

The long-sentence translation examples in the paper make this intuitive. The baseline model begins well and then drifts semantically, effectively losing the sentence. The attention-based model stays anchored to the source meaning for much longer. That pattern is more revealing than the BLEU numbers alone because it shows what kind of failure attention is preventing.

**What the qualitative alignments show and what they do not**

The visualized alignments are one of the most memorable parts of the paper. Many target words put most of their mass near diagonal positions, reflecting the often monotonic nature of English-French translation. But the model also handles non-monotonic cases, such as adjective-noun ordering changes, and the example `[European Economic Area] -> [zone economique europeenne]` is used to show that the decoder can jump to the semantically right region and then continue assembling the phrase.

These plots are scientifically useful, but they should not be romanticized. The attention weights are not gold linguistic alignments, and later work showed that attention distributions are not always faithful explanations of model reasoning. Still, for this paper they serve their purpose well: they demonstrate that the model has learned a plausible soft correspondence structure without explicit alignment supervision.

**What is incomplete, outdated, or limited in the paper**

The paper itself is fairly honest about several limitations. First, the attention mechanism requires scoring every source position for every target position. The authors note that this means the method scales with `T_x x T_y`, which is acceptable for translation sentences of length roughly `15-40` words but may be limiting elsewhere. That observation turned out to be prescient; scaling attention mechanisms became a major research direction later.

Second, the model still has sequential decoding and recurrent state propagation. So although attention relieves the fixed-vector bottleneck, it does not remove the optimization and parallelization limits of RNNs. This paper is historically foundational for attention, but not yet for the much more parallel computation pattern that transformers introduced.

Third, rare and unknown words remain a major weakness. The paper ends by explicitly naming this as future work. In retrospect that is exactly right. Later progress in neural MT depended not just on attention, but also on better tokenization, larger vocabularies or subword units, stronger optimization, and eventually transformer architectures.

**Why this became a foundational paper**

The enduring contribution is not just "attention helps." It is the deeper computational idea that a decoder should have dynamic, differentiable access to a structured source memory while generating output. That is the real shift. Once that idea exists, many later developments become natural: different scoring functions, multi-head variants, self-attention, pointer-like behaviors, and transformer cross-attention.

This paper therefore deserves to be read both as a machine translation paper and as a paper about learnable information access. In translation language, it solves a bottleneck in seq2seq. In broader deep learning language, it introduces a trainable retrieval mechanism over context-indexed representations. That second description is why its influence spread so far beyond MT.

---

## **Subtle points, clarifications, and limits**

This is not the Transformer's notion of attention. The model is still an encoder-decoder with recurrent computation on both sides, and the attention is an additive scoring mechanism from decoder state to encoder annotations. Historically, though, this is one of the clearest ancestors of later cross-attention.

The title phrase "jointly learning to align and translate" can also be misunderstood. The model is not trained with explicit gold alignments. It learns a soft alignment only because those weights help maximize translation probability. That is why the alignments are useful and interpretable, but they are also task-internal model artifacts rather than supervised linguistic annotations.

The paper's strongest comparison to phrase-based SMT also needs to be read with care. The neural model is competitive on the no-UNK subset, but it still trails `Moses` on the full test set, and `Moses` also benefits from additional monolingual data. So the correct historical takeaway is not "attention solved machine translation overnight." It is "attention made standalone neural translation dramatically more viable and exposed a path forward."

---

## **Closing perspective**

This paper is respected at a very high level across NLP and deep learning because it introduced the first widely convincing version of neural attention as a core computation rather than a side trick. In machine translation, it showed that the fixed-vector bottleneck was not a minor nuisance but an architectural mistake worth correcting. In the wider history of AI, it helped establish the idea that models should be allowed to build distributed memories and query them adaptively. That is why people still read it: not only because it improved 2014-era translation, but because it changed how the field thinks about sequence modeling itself.

---

## **Personal comprehension notes**

The easiest way to think about this paper is: the old seq2seq model tried to pour an entire sentence into one bottle and then decode from the bottle. Bahdanau attention replaces the bottle with a shelf of labeled memory slots, one per source position, where each slot already knows something about its local neighborhood. The decoder does not need the whole sentence in one place anymore. It just needs a good rule for looking at the right slots at the right time.

Another useful mental model is that this is "query the source before every word." The previous decoder state is the query, the source annotations are the memory, and the attention weights are the lookup rule. The weighted sum is not choosing one source word so much as building the exact source-side view needed for the next target decision. That is why the model handles articles, reorderings, and long-distance meaning better than the fixed-context baseline.

One more memory hook: if the Transformer later says "make attention the main computation everywhere," this paper says "at least stop making translation depend on one frozen summary vector." It is the bridge between early seq2seq and the full attention era.

---

## **Compact retention notes**

- **Paper type:** Foundational / landmark method paper with empirical validation
- **Core idea:** Replace the single fixed-length source summary with per-target-step soft alignment over bidirectional source annotations.
- **Main mechanism:** Decoder state scores each source annotation, softmax produces attention weights, weighted sum forms a context vector, and the recurrent decoder predicts the next word from that context.
- **Key result:** `RNNsearch` strongly outperforms the basic encoder-decoder, especially on long sentences, and becomes competitive with phrase-based SMT on the no-UNK subset.
- **Main limitation:** The model still suffers from rare-word `[UNK]` problems and keeps recurrent, sequential decoding while scoring all source positions at every target step.

---

## **Citations used in the paper**

- Yoshua Bengio, Rejean Ducharme, Pascal Vincent, Christian Janvin, *A Neural Probabilistic Language Model*, 2003
- Philipp Koehn, Franz Josef Och, Daniel Marcu, *Statistical Phrase-Based Translation*, 2003
- Holger Schwenk, *Continuous Space Translation Models for Phrase-Based Statistical Machine Translation*, 2012
- Alex Graves, *Generating Sequences with Recurrent Neural Networks*, 2013
- Ian Goodfellow et al., *Maxout Networks*, 2013
- Nal Kalchbrenner, Phil Blunsom, *Recurrent Continuous Translation Models*, 2013
- Ilya Sutskever, Oriol Vinyals, Quoc V. Le, *Sequence to Sequence Learning with Neural Networks*, 2014
- Kyunghyun Cho et al., *Learning Phrase Representations Using RNN Encoder-Decoder for Statistical Machine Translation*, 2014
- Kyunghyun Cho et al., *On the Properties of Neural Machine Translation: Encoder-Decoder Approaches*, 2014
- Razvan Pascanu et al., *How to Construct Deep Recurrent Neural Networks*, 2014
- Amittai Axelrod, Xiaodong He, Jianfeng Gao, *Domain Adaptation via Pseudo In-Domain Data Selection*, 2011 — used for corpus selection
- Matthew D. Zeiler, *ADADELTA: An Adaptive Learning Rate Method*, 2012

---
