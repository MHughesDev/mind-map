# LLaMA: Open and Efficient Foundation Language Models

**Paper link:** https://arxiv.org/abs/2302.13971

---

## **Paper metadata**

**Authors / collaborators:**
- Hugo Touvron
- Thibaut Lavril
- Gautier Izacard
- Xavier Martinet
- Marie-Anne Lachaux
- Timothee Lacroix
- Baptiste Roziere
- Naman Goyal
- Eric Hambro
- Faisal Azhar
- Aurelien Rodriguez
- Armand Joulin
- Edouard Grave
- Guillaume Lample

**Organizations / companies / institutions involved:**
- Meta AI

**Publication date:**
27 February 2023 (arXiv v1)

**Venue / source:**
arXiv preprint (`cs.CL`)

**Research paper type / category:**
- Foundational / landmark paper
- Method / model paper
- Systems / engineering paper
- Experimental / empirical paper

**Primary field / topic area:**
Large language models, autoregressive transformers, and efficient foundation-model scaling

**Keywords:**
- LLaMA
- scaling laws
- public-data pretraining
- autoregressive transformer
- inference efficiency
- RoPE
- RMSNorm
- SwiGLU

---

## **Opening perspective**

LLaMA arrived at a moment when frontier language modeling was starting to look like a contest of sheer size, private data, and closed access. GPT-3, Gopher, Chinchilla, and PaLM had made it seem as if serious progress required either very large parameter counts, proprietary corpora, or both. What this paper changes is the optimization target. Instead of asking only, "What model is best for a fixed training-compute budget?", it asks, "What model is best for a given inference budget if we are willing to train it longer?" That sounds like a small shift, but it has major consequences: a smaller model that keeps improving over far more tokens can be cheaper to serve while still landing near the frontier.

That is why the paper mattered far beyond its benchmark tables. It made the field take seriously the possibility that strong foundation models could be built from a disciplined recipe rather than from maximal scale alone. It also helped trigger the open-model wave of 2023, not because it solved language modeling theoretically, but because it showed that a carefully trained 7B-65B family could be both scientifically useful and practically deployable. The paper is best read as a systems-and-scaling landmark: a recipe paper, an infrastructure paper, and a statement about where the performance frontier really was.

---

## **Full walkthrough and explanation**

**The scaling question the paper is really about**

The paper opens in direct conversation with the first generation of very large few-shot models. GPT-3 made emergent in-context behavior hard to ignore, and PaLM and Gopher pushed the "bigger is better" story even further. But LLaMA treats Hoffmann et al.'s Chinchilla scaling laws as the more immediate backdrop. Chinchilla argues that for a fixed training compute budget, many language models had been undertrained: they were too large for the amount of data they saw. LLaMA accepts that point, but then changes the objective. If a model is going to be served heavily, inference cost matters as much as training cost. In that setting, it can make sense to train a smaller model for longer if that buys you comparable quality with cheaper deployment.

That is the core mental move of the paper. It is not anti-scaling. It is anti-scaling-naively-by-parameters alone. The authors explicitly note that a 7B model kept improving even after 1T tokens, which is far beyond the token budget one would have expected from an older compute-optimal reading. So the claim is not "small beats large." The claim is "there is a better tradeoff frontier if you are willing to spend more training tokens on a smaller architecture." Everything else in the paper sits underneath that thesis.

The high-level pipeline is:

Public text/code/science corpora -> SentencePiece BPE tokenization -> decoder-only transformer pretraining -> zero-shot/few-shot evaluation -> brief instruction finetuning experiment

**What "open and efficient" means in this paper**

The title uses two loaded words, and both need to be read carefully. "Efficient" does not mean the models are cheap in an absolute sense. The 65B model still requires a major training run on 2048 A100-80GB GPUs for about 21 days over 1.4T tokens. What it means is efficient relative to capability: better performance per parameter, and therefore better performance per unit of inference budget, than one would expect from just chasing giant parameter counts.

"Open" also needs qualification. The paper's strongest open claim is about the training recipe and data provenance: unlike GPT-3, PaLM, or Chinchilla, the authors emphasize that they use publicly available datasets rather than opaque proprietary corpora. That mattered enormously for reproducibility and for the broader open-model ecosystem. But it should not be read as unrestricted open-source release in the later licensing sense. The initial 2023 LLaMA release was provided under a noncommercial, case-by-case research-access regime rather than as weights anyone could use without restriction. So historically the paper is a major step toward open-weight research, but not a clean example of fully unrestricted openness.

There is a second subtlety here. The paper sometimes moves quickly from "publicly available" to "compatible with open-sourcing." Those are not identical ideas. Public availability is about access; clean licensing and consent are harder questions. So the paper's openness claim is best understood as a contrast with proprietary undisclosed datasets, not as proof that large-scale data curation problems had been solved.

**The data mixture and why the authors cared about it**

One of the paper's most important contributions is not architectural at all. It is the corpus design. The pretraining mixture is dominated by English CommonCrawl processed through CCNet, which makes up 67% of the sample. C4 adds another 15%. Then come GitHub at 4.5%, Wikipedia at 4.5%, Gutenberg plus Books3 at 4.5%, ArXiv at 2.5%, and Stack Exchange at 2%. That is a deliberately mixed corpus: web text for scale, code for procedural structure, Wikipedia for cleaner reference text, books for longer-form prose, ArXiv for technical language, and Stack Exchange for question-answer format.

The preprocessing story matters because LLaMA is not claiming that "more raw internet text" is enough. CommonCrawl is deduplicated at line level, filtered for English with fastText, and passed through quality filtering. GitHub is license-filtered to Apache, BSD, and MIT projects, then heuristically cleaned and deduplicated at file level. Wikipedia has boilerplate removed. Books are deduplicated at book level. ArXiv LaTeX is stripped of front matter, bibliography, comments, and user-defined macros. Stack Exchange answers are ordered by score. This is recipe work, and the paper treats it as first-class rather than as invisible plumbing.

After tokenization, the full corpus is about 1.4T tokens. The tokenizer is SentencePiece BPE, with two nice practical details: all numbers are split into individual digits, and unknown UTF-8 characters fall back to bytes. Most data is seen only once; Wikipedia and books are revisited for roughly two epochs. The smaller models, 7B and 13B, are trained on 1T tokens, while 33B and 65B go to 1.4T. That means the paper is not just scaling model size. It is scaling model size together with a very deliberate token budget.

The dataset is also more English-heavy than one might assume from the presence of 20-language Wikipedia dumps. The overall mixture is still overwhelmingly web-English, with some multilingual support coming from Wikipedia languages using Latin or Cyrillic scripts. So this is not a strongly multilingual model paper. It is an English-dominant foundation-model paper with some broader textual coverage.

**The architecture is conservative, but the recipe is not**

LLaMA does not win by inventing a new transformer family. It stays within the now-familiar decoder-only autoregressive transformer line. The novelty lies in which post-2017 improvements it adopts, how it combines them, and how long it trains. The four released model sizes are roughly 6.7B, 13.0B, 32.5B, and 65.2B parameters. Their widths, head counts, and depths grow in the expected way: from 32 layers and 32 heads at 7B up to 80 layers and 64 heads at 65B.

The architectural changes relative to the original Transformer are straightforward but consequential. First, LLaMA uses pre-normalization rather than post-normalization. More specifically, it applies RMSNorm to the input of each sublayer, which stabilizes very deep training better than the original 2017 post-norm layout. Second, it replaces ReLU feed-forward blocks with SwiGLU, following the now common view that gated activations give better performance. Third, it removes absolute positional embeddings and instead uses rotary positional embeddings, or RoPE, at every layer. So the representation path looks like:

Tokens -> embeddings -> repeated masked self-attention + feed-forward blocks with RMSNorm and SwiGLU -> next-token logits

Nothing in that list is revolutionary on its own. That is precisely why the paper is important. It shows how much performance can come from choosing the right already-known ingredients and training them at the right scale. LLaMA is a recipe paper in the strongest sense: it does not discover a new primitive so much as show the power of a disciplined assembly of existing ones.

**Optimization and systems engineering are a hidden part of the contribution**

The optimization setup is more serious than people often remember when they summarize the paper as "small models trained longer." The authors use AdamW with `beta1 = 0.9`, `beta2 = 0.95`, weight decay `0.1`, gradient clipping `1.0`, 2,000 warmup steps, and a cosine learning-rate schedule that ends at 10% of the peak rate. All models use a global batch size of 4M tokens, while the peak learning rate varies by model size. That is already enough to show that this is not a casual scaling experiment.

The systems side is equally important. They use memory-efficient causal attention in `xformers`, avoid storing masked attention weights, manually implement backward passes for transformer layers to reduce wasteful activation recomputation, and combine model parallelism with sequence parallelism while overlapping communication and computation. Those choices are the difference between a nice scaling idea and an actually executable 65B training run. When the paper reports around 380 tokens/sec/GPU on 2048 A100-80GB GPUs, that is not a side detail. It is part of the scientific contribution because the whole thesis depends on making long-duration training economically plausible.

A useful way to read the paper is that it has three stacked arguments:

Data argument -> careful public-data mixture can support frontier-quality training  
Model argument -> a mid-sized decoder-only transformer can stay competitive if trained much longer  
Systems argument -> the training stack must be efficient enough that this tradeoff can actually be realized

If any one of those layers failed, the headline story would collapse.

**What the benchmark section is really saying**

The evaluation is broad rather than narrow. The authors run zero-shot and few-shot tests over 20 benchmarks covering common-sense reasoning, closed-book question answering, reading comprehension, mathematical reasoning, code generation, and MMLU. For multiple-choice tasks they do not simply generate free-form answers and hope for the best; they rank candidate continuations by normalized likelihood, with some task-specific adjustments for datasets like BoolQ and OpenBookQA. That matters because the results are not just casual prompt demos.

The paper's most repeated comparison is that LLaMA-13B beats GPT-3 175B on most reported benchmarks, despite being over 10 times smaller in parameter count. The 65B model often competes with or surpasses Chinchilla-70B and even PaLM-540B on common-sense reasoning, closed-book QA, code, and some math tasks. On TriviaQA, for example, the 65B model reaches 73.0 exact match in the 64-shot setting. On HumanEval it gets 23.7 pass@1, and on MBPP it reaches 37.7 pass@1, outperforming PaLM 62B and LaMDA 137B as a general model without code-specific finetuning. On GSM8K, the 65B model even edges past Minerva 62B despite not being finetuned on mathematical data. The authors also emphasize that the 13B model is competitive on closed-book QA while being small enough to run on a single V100 GPU at inference time.

That is the paper's good news. The important thing is that the authors do not claim uniform dominance. MMLU is the clearest counterexample. LLaMA-65B reaches 63.4 five-shot average accuracy, which is strong but still behind Chinchilla-70B at 67.5 and PaLM-540B at 69.3. The authors suggest that their relatively small amount of book and academic-paper data may explain part of this. Whether that explanation is fully sufficient is less important than the broader lesson: LLaMA is not magically best at everything. Its strengths cluster where the paper's data mixture and scaling choices pay off most directly.

The training-curve analysis makes a similar point. Performance generally tracks training perplexity and improves steadily as tokens accumulate, which supports the paper's long-training thesis. But SIQA shows high variance, and WinoGrande does not track perplexity cleanly. The authors interpret this as possible benchmark unreliability or mismatch. That is a healthy detail. It keeps the paper from pretending that all evaluation noise disappears once a model gets big enough.

**The instruction-finetuning section is small, but historically revealing**

Section 4 is easy to overlook because it is not the main contribution, yet it turned out to be historically predictive. The authors take the 65B base model and do a brief instruction-finetuning experiment, producing `LLaMA-I`. Using a protocol similar to Flan-style work, they push MMLU from 63.4 to 68.9. They are explicit that this is not a full instruction-tuning study. It is a single proof-of-possibility experiment.

That modesty matters. Read in 2023 hindsight, this section looks like a trailer for what the community would immediately do with LLaMA: instruction tuning, chat tuning, domain adaptation, low-rank adaptation, safety tuning, and tool-use experiments on top of a strong base model. The paper itself is still a base-model paper, not a chat-assistant paper. But it already shows that the base is unusually fertile for post-training.

**The paper does not hide safety and social problems, but it does not solve them either**

A valuable feature of the paper is that it does not stop at benchmark accuracy. The authors explicitly test the 65B family on bias, toxicity, and misinformation-adjacent benchmarks. On RealToxicityPrompts, average toxicity tends to rise with model size, especially under the "respectful" prompt framing. On CrowS-Pairs, LLaMA-65B is slightly better than GPT-3 and OPT-175B on average, but still shows strong stereotype preferences, especially in religion, age, and gender. On WinoGender, performance drops on gotcha cases where occupation stereotypes conflict with the correct pronoun resolution, which strongly suggests that the model is using social priors instead of the sentence evidence alone.

TruthfulQA shows a different limitation. LLaMA beats GPT-3 on the paper's reported truthfulness metrics, but the absolute scores are still low enough that hallucination and misinformation remain serious risks. This is exactly the sort of result people often miss when they remember only the performance headlines. The paper is saying two things at once: the models are impressively strong, and they still inherit harmful internet biases and truthfulness failures.

The authors are also candid that these benchmarks are incomplete. That is important. A few toxicity or bias probes do not amount to a full safety evaluation. So the responsible way to read this section is not "Meta audited the model and the problem is handled." It is "the paper acknowledges obvious failure modes and shows that the base models still have them."

**Carbon cost and practical efficiency pull in opposite directions**

There is another tension in the paper that is worth understanding clearly. LLaMA is efficient in the sense of performance per parameter and performance per inference budget. It is not environmentally cheap in any everyday sense. Under the paper's standardized assumptions, training the 65B model corresponds to about 449 MWh and 173 tCO2eq. The broader development process for the family is estimated at roughly 2,638 MWh and 1,015 tCO2eq.

That makes the paper a good example of a recurring pattern in modern AI systems. A model can be more efficient along one axis and still be extremely expensive along another. LLaMA made the open-model ecosystem more accessible because 7B and 13B models could run on much smaller hardware than GPT-3-scale systems. But that downstream accessibility sits on top of a very large upstream training effort.

**How to read the paper historically**

Historically, LLaMA is best understood as a turning-point paper in open-model systems research. It did not introduce the transformer, few-shot learning, instruction tuning, or scaling laws. What it did was synthesize them into a particularly effective base-model recipe built from public data and then show that the resulting family remained competitive with the best private-model work. That is why it had so much downstream impact. It changed what researchers thought was possible outside a handful of labs with proprietary data advantages.

It also shifted the center of gravity of the conversation. After LLaMA, it became much harder to argue that only extremely large closed models mattered. A strong mid-sized base model could support a huge amount of scientific work: alignment experiments, finetuning, quantization, retrieval augmentation, domain adaptation, and instruction following. In that sense, the paper is not only about benchmark quality. It is about changing the usable unit of progress in LLM research from "giant closed frontier model" to "strong reusable base model family."

---

## **Subtle points, clarifications, and limits**

The most common overreading is to treat this paper as proof that parameter count stopped mattering. It did not. The actual lesson is narrower: parameter count by itself is a poor guide if token budget, data quality, architectural details, and serving constraints are ignored. Bigger still helps, but bigger-and-undertrained is not the right frontier.

The word "open" is also easy to overread. LLaMA was a landmark for open-weight research and public-data training recipes, but the original release was gated research access under a noncommercial license, not unrestricted open-source availability. The data story also deserves caution: public availability of training sources is not the same thing as resolving all licensing, consent, or governance concerns around web-scale corpora.

Finally, the paper should be remembered as a base-model paper. The later chat, instruction, and agent ecosystems built on LLaMA are historically downstream of this work, not identical to it. If you read the paper expecting RLHF, dialog alignment, or tool use, you are reading the wrong paper.

---

## **Closing perspective**

LLaMA earned lasting respect because it changed the practical imagination of the field. It showed that the frontier was not owned exclusively by gigantic closed systems trained on opaque data. A well-chosen transformer recipe, trained for a very long time on a carefully assembled public corpus, could get surprisingly close while being far easier to study and reuse. That made the paper important not only to large-model practitioners at frontier labs, but also to the wider open-weight, systems, and alignment communities. It is still worth understanding because so much of the 2023-and-beyond language-model ecosystem was built on top of the shift in assumptions that this paper forced into the open.

---

## **Personal comprehension notes**

The easiest way to remember LLaMA is: "Chinchilla logic, but optimized for serving." Chinchilla says many models were too large for how much data they saw. LLaMA takes that idea and says, "Fine, then let us spend more tokens on smaller models so they stay cheap at inference." That is the paper in one sentence.

A second mental model is to treat LLaMA as a recipe stack rather than a single idea:

Public-data corpus + aggressive token budget + decoder-only transformer + RMSNorm + SwiGLU + RoPE + strong training systems = unusually capable base model family

That is why the paper feels less like a theory breakthrough and more like an engineering synthesis that changed the research landscape.

A third useful way to think about it is that LLaMA made the 7B-65B regime scientifically central. Before this, people often talked as if real capability lived only at the extreme end of scale. After LLaMA, a mid-sized open model became a serious research object in its own right.

---

## **Compact retention notes**

- **Paper type:** Landmark LLM recipe and scaling paper
- **Core idea:** Train smaller decoder-only transformers much longer on a carefully filtered public-data mixture to improve capability per parameter and per inference budget.
- **Main mechanism:** Public-data pretraining at 1T-1.4T tokens plus a modern transformer recipe using RMSNorm, SwiGLU, and RoPE.
- **Key result:** LLaMA-13B beats GPT-3 on most reported benchmarks, and LLaMA-65B is competitive with Chinchilla-70B and PaLM-540B on many tasks.
- **Main limitation:** The models are not uniformly best, are still biased and hallucinatory, and the original release was not fully unrestricted despite the paper's "open" framing.

---

## **Citations used in the paper**

- Tom B. Brown et al., *Language Models are Few-Shot Learners*, 2020
- Jordan Hoffmann et al., *Training Compute-Optimal Large Language Models*, 2022
- Aakanksha Chowdhery et al., *PaLM: Scaling Language Modeling with Pathways*, 2022
- Jack W. Rae et al., *Scaling Language Models: Methods, Analysis & Insights from Training Gopher*, 2021
- Ashish Vaswani et al., *Attention Is All You Need*, 2017
- Biao Zhang, Rico Sennrich, *Root Mean Square Layer Normalization*, 2019
- Noam Shazeer, *GLU Variants Improve Transformer*, 2020
- Jianlin Su et al., *RoFormer: Enhanced Transformer with Rotary Position Embedding*, 2021
- Guillaume Wenzek et al., *CCNet: Extracting High Quality Monolingual Datasets from Web Crawl Data*, 2020
- Leo Gao et al., *The Pile: An 800GB Dataset of Diverse Text for Language Modeling*, 2020
- Hyung Won Chung et al., *Scaling Instruction-Finetuned Language Models*, 2022
- Samuel Gehman et al., *RealToxicityPrompts: Evaluating Neural Toxic Degeneration in Language Models*, 2020
- Stephanie Lin, Jacob Hilton, Owain Evans, *TruthfulQA: Measuring How Models Mimic Human Falsehoods*, 2021
