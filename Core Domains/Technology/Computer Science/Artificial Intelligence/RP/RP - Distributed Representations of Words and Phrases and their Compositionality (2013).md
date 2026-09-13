# Distributed Representations of Words and Phrases and their Compositionality

**Paper link:** https://arxiv.org/pdf/1310.4546

---

## **Paper metadata**

**Authors / collaborators:**  
- Tomas Mikolov
- Ilya Sutskever
- Kai Chen
- Greg Corrado
- Jeffrey Dean

**Organizations / companies / institutions involved:**  
- Google Inc.

**Publication date:**  
16 October 2013 (arXiv preprint); later presented at NeurIPS 2013

**Venue / source:**  
NeurIPS 2013 / arXiv

**Research paper type / category:**  
- Foundational / landmark paper
- Method / model paper
- Experimental / empirical paper

**Primary field / topic area:**  
Natural language processing, distributional semantics, and representation learning

**Keywords:**  
- skip-gram
- word2vec
- negative sampling
- phrase embeddings
- analogical reasoning
- subsampling

---

## **Opening perspective**

This paper sits in the part of NLP where people stopped treating words mainly as sparse symbols and started treating them as points in a learned geometric space. That shift had already begun before this paper, but Mikolov and colleagues made it much more operational. They took the earlier skip-gram word2vec idea and pushed on the two questions that really determine whether such a model becomes historically important: can it be trained at enormous scale, and do the resulting vectors actually preserve useful semantic and syntactic structure?

What makes the paper worth serious attention is that it is not only a "better embedding" paper. It is a paper about how to make representation learning computationally cheap enough that corpus scale itself becomes a decisive source of quality. Negative sampling, subsampling of frequent words, and phrase mining are all presented as simple engineering decisions, but together they changed how a large part of NLP thought about lexical meaning. The paper gave the field a practical recipe for turning raw co-occurrence structure into dense vectors that could be reused almost everywhere.

---

## **Full walkthrough and explanation**

**What the paper is extending**

The paper starts from the skip-gram model introduced in the earlier word2vec work. The basic idea is simple: if a word is represented well, its vector should help predict the nearby words that tend to appear around it. That already puts the paper inside the distributional tradition, where meaning is inferred from usage patterns rather than from hand-built symbolic definitions. But this paper is not content with the original form of skip-gram. It wants a version that trains faster, yields better vectors, and can move from isolated words to short phrases.

The overall pipeline the paper is building looks like this:

Raw text -> center word and surrounding context pairs -> skip-gram objective -> efficient training approximation -> learned word vectors -> phrase detection -> retraining with phrase tokens -> word and phrase analogy evaluation

That pipeline matters because the paper is not just introducing one trick. It is presenting a compact ecosystem of tricks that work together.

**The basic skip-gram objective**

In skip-gram, each training position provides a center word and several surrounding context words. If the corpus is

$$
w_1, w_2, \ldots, w_T
$$

then the model tries to maximize the average log probability of the nearby words around each center token. The core conditional distribution is written as:

$$
p(w_O \mid w_I) = \frac{\exp({v'_{w_O}}^{T} v_{w_I})}{\sum_{w=1}^{W} \exp({v'_w}^{T} v_{w_I})}
$$

Here `w_I` is the input or center word, `w_O` is an observed context word, `v_{w_I}` is the input embedding of the center word, `v'_{w_O}` is the output embedding of the context word, and `W` is the vocabulary size. The dot product says how compatible the center and context words are. After exponentiation and normalization, that compatibility becomes a probability distribution over the whole vocabulary.

The problem is obvious once the formula is written down: the denominator sums over every vocabulary item. If the vocabulary is hundreds of thousands or millions of tokens, doing that for every training pair is expensive. So the main technical question becomes how to approximate this objective without destroying the quality of the learned geometry.

**Hierarchical softmax as the starting approximation**

Before introducing its new method, the paper reviews hierarchical softmax, which had already been used in earlier neural language models and in the previous skip-gram work. Instead of normalizing over all words directly, hierarchical softmax places words at the leaves of a binary tree and computes the probability of a word by multiplying the probabilities of the branching decisions along its path from the root to the leaf. That reduces cost from something proportional to vocabulary size to something closer to the depth of the tree, roughly `log W` on average.

The paper uses a Huffman tree so that frequent words get shorter codes. That makes training faster, because common words are reached through fewer decisions. Hierarchical softmax is therefore the baseline approximation against which the paper measures its new proposal.

**Why negative sampling is such a big deal**

The most famous contribution of the paper is negative sampling. The authors start from the idea of Noise Contrastive Estimation, but they deliberately simplify it because their goal is not to build the best normalized language model. Their goal is to learn high-quality vector representations. Negative sampling says: instead of computing a full normalized probability for every target word, train the model to distinguish real center-context pairs from randomly sampled fake ones.

The paper writes the objective for one observed pair as:

$$
\log \sigma({v'_{w_O}}^{T} v_{w_I}) + \sum_{i=1}^{k} \mathbb{E}_{w_i \sim P_n(w)} \left[ \log \sigma(-{v'_{w_i}}^{T} v_{w_I}) \right]
$$

This deserves to be unpacked carefully. The first term rewards the model for giving a high score to the real observed context word `w_O` around center word `w_I`. The second term samples `k` noise words from a noise distribution `P_n(w)` and rewards the model for pushing those fake words away. The sigmoid `sigma` turns dot products into logistic yes/no judgments. So training becomes a sequence of tiny classification problems:

Real pair -> push score up  
Sampled noise pair -> push score down

That is why the method is fast. Each training event touches only the true pair plus a small number of sampled negatives instead of touching the entire output layer. The authors report that for small datasets, `k = 5` to `20` negatives works well, while for very large datasets `k = 2` to `5` can already be enough.

There is also an important conceptual point here. Negative sampling is not pretending to be the exact softmax objective. The paper explicitly treats that as acceptable. If the vectors are what we care about, then a simpler objective that produces better vectors is preferable to a more principled objective that wastes computation. That pragmatic stance is a big part of the paper's influence.

The choice of noise distribution matters. The paper tests several options and finds that sampling from the unigram distribution raised to the `3/4` power works better than sampling from the raw unigram distribution or from a uniform distribution. Intuitively, this downweights the extremely frequent words without flattening the distribution completely. That turns out to be one of those small implementation details that survived into standard practice because it works reliably.

**Why subsampling frequent words helps both speed and quality**

Another key contribution is subsampling of frequent words. The authors point out that very common tokens such as "the", "in", and "a" appear so often that they dominate training, but each additional occurrence adds relatively little information. Seeing "France" next to "the" again is not nearly as informative as seeing "France" next to "Paris". So the paper discards very frequent words probabilistically during training.

The discard probability is given by:

$$
P(w_i) = 1 - \sqrt{\frac{t}{f(w_i)}}
$$

where `f(w_i)` is the corpus frequency of word `w_i` and `t` is a threshold, typically around `1e-5`. This means that once a word becomes much more frequent than the threshold, many of its occurrences are dropped. The paper emphasizes two effects: training gets much faster, and the remaining training signal becomes more informative, especially for rarer content words.

This is not presented as a theorem-backed derivation. It is a heuristic. But it is a very effective heuristic. The paper reports speedups around `2x` to `10x`, which is enormous when the entire point is to exploit huge corpora.

**What the word-level experiments actually show**

The first empirical section evaluates different training objectives on the standard analogy task introduced in the earlier Mikolov work. The analogy format is the now-famous pattern:

`Germany : Berlin :: France : ?`

which is solved by searching for the vector closest to:

$$
\text{vec}(\text{Berlin}) - \text{vec}(\text{Germany}) + \text{vec}(\text{France})
$$

The dataset contains both semantic analogies, such as country-capital relations, and syntactic analogies, such as adjective-adverb or verb tense transformations. For these word experiments, the paper trains on an internal Google news corpus of about one billion words, drops words occurring fewer than five times, and ends up with a vocabulary of about `692K` tokens. The reported models use `300` dimensions.

The results are important for two reasons. First, negative sampling beats hierarchical softmax on the word analogy task. With no subsampling, `NEG-15` reaches `61%` total accuracy versus `47%` for Huffman hierarchical softmax. Second, subsampling improves both quality and speed. For example, `NEG-5` drops from `38` minutes to `14` minutes while improving total accuracy from `59%` to `60%`. Hierarchical softmax also benefits substantially once frequent tokens are downsampled.

What this means is not that analogy accuracy is a complete measure of meaning. It is not. Analogy tasks strongly reward linear relational structure of a particular sort. But the paper does show something real: these vectors are organizing semantic and syntactic regularities in a way that can be probed with simple algebraic operations, and the proposed training changes improve that organization.

**Why phrases are treated as a separate problem**

The paper then turns to a limitation of ordinary word vectors: they ignore word order and they cannot reliably represent idiomatic or named multiword expressions. "Air Canada", "Boston Globe", and "New York Times" are not just arbitrary sums of their component words. If the model only learns vectors for individual tokens, it misses a lot of practically important lexical units.

The paper's solution is not a deep compositional model. It is much simpler and much more opportunistic. First, scan the corpus for adjacent words that occur together much more often than expected from their individual frequencies. Then merge those high-scoring pairs into phrase tokens and retrain the embedding model over the modified corpus. In effect, some recurrent local strings get promoted to atomic vocabulary items.

The phrase discovery pipeline is:

Corpus -> count unigrams and bigrams -> score adjacent pairs -> merge pairs above threshold into single tokens -> repeat with lower thresholds -> train skip-gram on words plus phrase tokens

The phrase score is based on how often a bigram occurs compared with the separate frequencies of its component words, with a discount term `delta` that suppresses accidental low-count combinations. The paper runs `2` to `4` passes with decreasing thresholds so that longer phrases can emerge from earlier merged bigrams. This is how constructions such as `New_York_Times` can be built incrementally instead of requiring the system to spot every long phrase in one shot.

This is a very practical idea, but it is also clearly heuristic. It is good at catching frequent collocations and named entities in a large news corpus. It is not a full theory of phrase meaning, syntax, or compositional semantics. The authors are not claiming otherwise. They are simply showing that this lightweight phrase-mining step makes skip-gram substantially more expressive at low computational cost.

**How the phrase evaluation works**

To test phrase vectors, the paper introduces a new analogy dataset for phrases. Instead of only asking for word relations such as capital cities, it asks for relations like:

`Montreal : Montreal Canadiens :: Toronto : ?`

where the expected answer is `Toronto Maple Leafs`. The full phrase analogy test set contains `3218` examples across categories such as newspapers, NHL teams, NBA teams, airlines, and company executives.

On the one-billion-word news corpus with `300` dimensions and context size `5`, the performance is mixed but informative. `NEG-15` with subsampling reaches `42%`, while hierarchical softmax with subsampling reaches `47%`. So the best method for word analogies is not automatically the best method for phrase analogies. That is one of the paper's more careful observations: optimal training choices depend on the downstream structure being evaluated.

To maximize phrase performance, the authors scale up much more aggressively. Using about `33B` words, `1000` dimensions, hierarchical softmax, and effectively whole-sentence context, they reach `72%` phrase analogy accuracy. When the training corpus is reduced to `6B` words, accuracy falls to `66%`. That supports one of the paper's central messages: scale is not a minor implementation detail here. The ability to train cheaply on much more data is itself part of the scientific contribution.

**What additive compositionality is claiming, and what it is not**

Another memorable part of the paper is the observation that vector addition can sometimes yield useful phrase-like meanings. The examples include things like `Russia + river` being close to `Volga River`, or `Germany + capital` being close to `Berlin`. The authors explain this through the skip-gram objective itself. Since vectors are trained to predict contexts, a vector can be interpreted as a compact encoding of the contexts in which a word tends to appear. Adding two vectors roughly combines those contextual tendencies.

The paper's intuition is that addition behaves somewhat like an AND operation over contexts: words that are compatible with both component contexts remain prominent. That is why the sum of two vectors can land near an entity or phrase that naturally lives in the intersection of the two contextual neighborhoods.

This is an insightful observation, but it should not be overread. Vector addition is not a general semantic calculus. It works well for some relations and some lexicalized combinations, and poorly for many others. The paper is strongest when it treats these results as evidence of useful linear structure, not as proof that meaning in general is literally additive.

**Comparison to earlier published embeddings**

The paper also compares its learned vectors to earlier published word representations from Collobert and Weston, Turian et al., and Mnih and Hinton by looking at nearest neighbors of relatively rare words and phrases. The comparison is qualitative rather than benchmark-style, but the pattern supports the paper's main story: when skip-gram is trained at much larger scale, especially with phrase tokens, the neighborhoods of rare entities become noticeably more coherent.

That matters because it shows where the gain is really coming from. The paper is not claiming that a shallow model is intrinsically superior in all respects to deeper or more complex neural language models. It is showing that an extremely efficient shallow architecture can be trained on far more data than previous methods, and that this scale changes the quality regime of the learned representations.

**How to read the paper historically**

Historically, the paper is easy to misremember as "the negative sampling paper" or "the word2vec phrase paper." Both are true, but they are too narrow. The deeper contribution is that it turns lexical representation learning into something cheap, scalable, and reusable. It gives the field a recipe in which the objective is simple, the approximations are deliberately practical, and the output vectors are good enough to become infrastructure for a large range of downstream NLP tasks.

That is why this paper became more influential than many more theoretically polished papers. It showed a way to get useful semantic geometry at industrial scale, and it did so with enough simplicity that the method could be reimplemented, adapted, and deployed almost immediately.

---

## **Subtle points, clarifications, and limits**

The vectors in this paper are still static type-level embeddings. A word gets one vector regardless of context, so polysemous words are forced into a single compromise representation. Later contextual models such as ELMo, BERT, and GPT solve a different problem by letting a token's representation vary with surrounding text. That later shift does not invalidate this paper, but it does clarify what this method can and cannot express.

It is also worth keeping separate three different ideas that people often blur together: analogy offsets, phrase tokens, and additive composition. The paper studies all three, but they are not the same phenomenon. Analogy offsets show linear relational structure, phrase tokens create new atomic vocabulary items for recurring multiword expressions, and additive composition tries to combine existing vectors without introducing a new token. Those mechanisms are related, but they are not interchangeable.

---

## **Closing perspective**

This paper has foundational status because it made dense lexical representation learning feel like a standard tool rather than an expensive research curiosity. Negative sampling and subsampling became canonical engineering ideas, and the broader word2vec program helped normalize the view that semantic structure can emerge from predictive training over raw text. It is still respected across NLP, representation learning, and modern deep learning because it marks a real transition point: from sparse symbolic features and small neural language models to scalable learned vector spaces that later systems, including contextual language models, would build on and eventually surpass.

---

## **Personal comprehension notes**

The easiest way to think about this paper is: it teaches each word vector to become a compact summary of the kinds of neighborhoods that word lives in. A good vector is one that makes true nearby words easy to recognize. Negative sampling makes that training cheap by replacing "compare against the whole vocabulary" with "separate the real neighbors from a handful of impostors."

Another useful mental model is that the paper wins by reallocating compute, not by inventing a deep semantic theory. It spends less computation per training event, then cashes in that savings by training on much more text. That is why the paper feels so practical. The scientific claim and the engineering claim are basically the same claim: if you can afford enough real text, simple predictive geometry becomes surprisingly powerful.

For phrases, the mental model is: the method promotes certain recurring word sequences into vocabulary items. Instead of forcing `New`, `York`, and `Times` to compose on the fly every time, it decides that `New_York_Times` deserves its own point in space. That is crude compared with later contextual composition, but it is often exactly the right crude move for large corpora full of named entities and idioms.

---

## **Compact retention notes**

- **Paper type:** Foundational method paper in NLP representation learning
- **Core idea:** Train skip-gram embeddings much more efficiently with negative sampling and subsampling, then extend the same framework to phrase tokens.
- **Main mechanism:** Predict surrounding words from a center word, replace full softmax with sampled real-vs-noise updates, drop many high-frequency tokens, and mine frequent collocations as phrases.
- **Key result:** Simple shallow models trained on very large corpora learn word and phrase vectors with strong analogy performance and surprisingly coherent semantic structure.
- **Main limitation:** The embeddings are static, corpus-dependent, and only capture phrase meaning through heuristics or linear approximations rather than true context-sensitive composition.

---

## **Citations used in the paper**

- Yoshua Bengio, Rejean Ducharme, Pascal Vincent, Christian Janvin, *A Neural Probabilistic Language Model*, 2003
- Ronan Collobert, Jason Weston, *A Unified Architecture for Natural Language Processing: Deep Neural Networks with Multitask Learning*, 2008
- Michael U. Gutmann, Aapo Hyvarinen, *Noise-Contrastive Estimation of Unnormalized Statistical Models, with Applications to Natural Image Statistics*, 2012
- Andriy Mnih, Geoffrey E. Hinton, *A Scalable Hierarchical Distributed Language Model*, 2009
- Andriy Mnih, Yee Whye Teh, *A Fast and Simple Algorithm for Training Neural Probabilistic Language Models*, 2012
- Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean, *Efficient Estimation of Word Representations in Vector Space*, 2013
- Tomas Mikolov, Wen-tau Yih, Geoffrey Zweig, *Linguistic Regularities in Continuous Space Word Representations*, 2013
- Frederic Morin, Yoshua Bengio, *Hierarchical Probabilistic Neural Network Language Model*, 2005
- David E. Rumelhart, Geoffrey E. Hinton, Ronald J. Williams, *Learning Representations by Back-Propagating Errors*, 1986
- Holger Schwenk, *Continuous Space Language Models*, 2007
- Richard Socher, Cliff C. Lin, Andrew Y. Ng, Christopher D. Manning, *Parsing Natural Scenes and Natural Language with Recursive Neural Networks*, 2011
- Richard Socher, Brody Huval, Christopher D. Manning, Andrew Y. Ng, *Semantic Compositionality Through Recursive Matrix-Vector Spaces*, 2012
- Peter D. Turney, Patrick Pantel, *From Frequency to Meaning: Vector Space Models of Semantics*, 2010
