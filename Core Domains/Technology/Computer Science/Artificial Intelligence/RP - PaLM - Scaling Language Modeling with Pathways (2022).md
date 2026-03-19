# PaLM: Scaling Language Modeling with Pathways

**Paper link:** https://arxiv.org/pdf/2204.02311.pdf

---

## **Paper metadata**

**Authors / collaborators:**  
- Lead authors: Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann
- Additional collaborators: Parker Schuh, Kensen Shi, Sasha Tsvyashchenko, Joshua Maynez, Abhishek Rao, Parker Barnes, Yi Tay, Noam Shazeer, Vinodkumar Prabhakaran, Emily Reif, Nan Du, Ben Hutchinson, Reiner Pope, James Bradbury, Jacob Austin, Michael Isard, Guy Gur-Ari, Pengcheng Yin, Toju Duke, Anselm Levskaya, Sanjay Ghemawat, Sunipa Dev, Henryk Michalewski, Xavier Garcia, Vedant Misra, Kevin Robinson, Liam Fedus, Denny Zhou, Daphne Ippolito, David Luan, Hyeontaek Lim, Barret Zoph, Alexander Spiridonov, Ryan Sepassi, David Dohan, Shivani Agrawal, Mark Omernick, Andrew M. Dai, Thanumalayan Sankaranarayana Pillai, Marie Pellat, Aitor Lewkowycz, Erica Moreira, Rewon Child, Oleksandr Polozov, Katherine Lee, Zongwei Zhou, Xuezhi Wang, Brennan Saeta, Mark Diaz, Orhan Firat, Michele Catasta, Jason Wei, Kathy Meier-Hellstern, Douglas Eck, Jeff Dean, Slav Petrov, Noah Fiedel

**Organizations / companies / institutions involved:**  
- Google Research
- Google Pathways
- Google AI infrastructure and tooling teams behind TPU v4, JAX, T5X, XLA, and large-scale distributed training

**Publication date:**  
5 April 2022 initial arXiv submission; revised 5 October 2022

**Venue / source:**  
arXiv preprint (`cs.CL`)

**Research paper type / category:**  
- Foundational / landmark paper
- Method / model paper
- Systems / engineering paper
- Experimental / empirical paper

**Primary field / topic area:**  
Large language modeling, scaling, and distributed training infrastructure

**Keywords:**  
- PaLM
- Pathways
- large language models
- few-shot learning
- chain-of-thought prompting
- multilingual NLP
- code generation

---

## **Opening perspective**

This is one of the papers that turned large language models from an impressive trend into an infrastructural program. On the surface it is about a 540B-parameter decoder-only Transformer. At a deeper level it is about what has to line up for a model of that size to exist at all: architecture choices that are stable enough to scale, a training corpus broad enough to support generality, and a distributed system that can keep thousands of accelerators busy without wasting most of the compute budget.

What made PaLM especially consequential is that it did not just report better benchmark numbers. It tied together three ideas that became central to the next phase of AI research. First, scaling still had not obviously saturated. Second, prompting could reveal behaviors that standard evaluation styles understated. Third, the infrastructure stack was not a side detail but part of the scientific contribution. That combination is why the paper still matters even though later work changed the compute tradeoffs, training ratios, and deployment story.

---

## **Full walkthrough and explanation**

**The question the paper is really asking**

By early 2022, papers like GPT-3, Gopher, GLaM, and LaMDA had already shown that large autoregressive language models could do surprisingly well in few-shot settings. PaLM asks a sharper question: if you keep the recipe mostly familiar and simply push scale much harder, does performance keep improving in ways that matter, and can a new training system make that scale practical? That is why this is both a model paper and a systems paper. The model is the visible object, but the real experiment is the entire stack.

One subtle but very important point appears right at the start. Even though the title foregrounds Pathways, PaLM itself is not a sparse, modular, mixture-of-experts realization of the full Pathways vision. It is a dense decoder-only Transformer. That choice is deliberate. The authors wanted a comparatively well-understood architecture so that the observed gains could be attributed to scale, data, and training infrastructure rather than to a radically new model family. In other words, PaLM is a clean scaling probe, not an exotic architectural bet.

The high-level pipeline is:

Training corpus -> lossless tokenization -> dense decoder-only Transformer pretraining -> prompted evaluation across language, reasoning, multilingual, code, and safety tasks

That looks simple, but almost every piece of that pipeline is doing important work.

**How the model is built**

Architecturally, PaLM is a standard autoregressive Transformer only in the broadest sense. The paper keeps the decoder-only setup, where each position can attend only to itself and earlier positions, but it makes a set of scaling-oriented design choices that are easy to miss if you only remember "540B dense model."

The model uses SwiGLU activations in the MLP blocks rather than a more standard ReLU or GeLU-style feed-forward stack. It uses a parallel Transformer block formulation, where the attention path and the MLP path both branch off the same normalized input and are added back together, instead of serializing attention first and the MLP second. The reason is not aesthetic. The paper reports roughly 15% faster training at large scale because the relevant matrix multiplications can be fused more effectively. It also uses multi-query attention, where keys and values are shared across heads, which keeps training quality roughly neutral while making autoregressive decoding cheaper. Rotary position embeddings replace absolute or relative position embeddings, shared input-output embeddings reduce redundancy, and biases are removed from dense kernels and layer norms because the authors found this improved stability at large scale.

The vocabulary design also matters more than it may first appear. PaLM uses a 256k-token SentencePiece vocabulary generated from the training data itself. It is designed to be lossless and reversible, which means whitespace is preserved exactly, out-of-vocabulary Unicode characters can fall back to UTF-8 bytes, and numbers are split into individual digit tokens. That sounds like tokenization bookkeeping, but it has direct implications for multilingual handling, exact text reconstruction, and code modeling.

At the largest scale, the model has 118 decoder layers, 48 attention heads, and model width `d_model = 18432`, with feed-forward width always set to `4 x d_model` and head size fixed at 256. The paper also trains 8B and 62B versions using the same data and vocabulary. That controlled family is one of the strongest parts of the paper because it makes the scaling comparisons much cleaner than comparing unrelated frontier models trained with different recipes.

The core computation pipeline is:

Text or code -> 256k lossless SentencePiece tokens -> shared embeddings + RoPE -> 118 decoder blocks with parallel attention and MLP paths -> next-token distribution

An important interpretive point here is that the paper is not mainly claiming a brand-new architecture. It is claiming that a carefully assembled set of mostly known ingredients can still yield qualitatively new behavior when scaled far enough and trained efficiently enough.

**The training data and what the data mixture is doing**

The pretraining dataset contains 780 billion tokens seen for exactly one epoch. The paper presents this as a high-quality mixture meant to span many real language use cases rather than a single genre of text. The proportions are explicit: 50% social media conversations, 27% filtered multilingual webpages, 13% English books, 5% GitHub code, 4% multilingual Wikipedia, and 1% English news. The multilingual portions cover more than 100 languages. The code component is filtered to permissive-license repositories, restricted to 24 common programming languages, and deduplicated because raw code corpora contain a great deal of repetition.

That mixture helps explain several of the paper's results. PaLM is not only strong on classic English NLP tasks, but also on multilingual benchmarks, translation, and code. The breadth of the corpus is part of the argument. The authors are not merely showing that a huge model can memorize more internet text; they are showing that broad pretraining can support surprisingly wide transfer when the model is large enough.

There is also an important correction that later work makes easier to see. PaLM is trained on 780B tokens, which felt enormous at the time, but by the compute-optimal perspective popularized shortly afterward by Chinchilla, a 540B dense model is undertrained relative to its size. So PaLM should not be read as the final answer to "how should we allocate compute between parameters and data?" It is better read as proof that capability gains from scale were still available, not proof that this particular parameter-to-token ratio was optimal.

**Why Pathways is central instead of incidental**

The infrastructure story is not packaging around the model. It is one of the main results. PaLM 540B is trained using JAX and T5X on two TPU v4 Pods, each containing 3072 chips, for a total of 6144 TPU v4 chips. Within a pod, the training uses 12-way model parallelism together with 256-way fully sharded data parallelism. Across the two pods, Pathways provides pod-level two-way data parallelism. Each pod runs forward and backward passes on half the batch, gradients are exchanged across pods, and both sides apply the same update so the parameters remain bitwise identical.

The systems pipeline is:

Batch split across two pods -> within-pod forward and backward computation -> cross-pod gradient exchange -> synchronized optimizer update on both pods

The paper emphasizes that this works without pipeline parallelism. That matters because pipeline parallelism often introduces bubble overhead, memory-bandwidth costs, and extra software complexity. Pathways lets the authors avoid that route and still scale training efficiently across pods. They report 1.95x throughput relative to a single pod, which is about 97% of ideal weak scaling in that setup, despite the burden of large cross-pod gradient transfers.

The efficiency claims are also unusually explicit. PaLM 540B reaches 238.3K tokens per second at batch size 2048, 46.2% model FLOPs utilization, and 57.8% hardware FLOPs utilization. The distinction between the two is important: the paper argues that model FLOPs utilization is the cleaner metric because it factors out implementation-specific rematerialization choices. This section is one reason the paper remained important to systems researchers, not just language model researchers.

**What the broad language benchmarks actually show**

On the standard English few-shot benchmark suite inherited from the GPT-3 and GLaM comparison tradition, PaLM 540B is very strong. Across 29 tasks covering closed-book question answering, cloze and completion, Winograd-style tasks, commonsense reasoning, reading comprehension, SuperGLUE tasks, and natural language inference, it beats prior large-language-model state of the art on 24 of 29 tasks in the 1-shot setting and 28 of 29 tasks in the few-shot setting. Its average 1-shot scores are 63.9 on the generation-oriented subset and 74.7 on the understanding-oriented subset. On MMLU it reaches 69.3 in the 5-shot setting, surpassing Chinchilla's reported average.

These results matter for two reasons. First, they show that scale is still buying more than small benchmark polishing. Second, PaLM beats a similarly large model such as Megatron-Turing NLG across the benchmark suite, which suggests that architecture size alone is not the whole story. Training data, training duration, optimization choices, and infrastructure all influence the final capability profile.

At the same time, this section should be read with some care. The paper mostly compares against other pretrained large language models in few-shot or zero-shot setups, not against the very best task-specific supervised systems on every benchmark. And when the authors do finetune PaLM on SuperGLUE, the result is excellent and competitive, but still naturally shaped by the fact that decoder-only autoregressive models are not always the ideal architecture for classification-style fine-tuning. So the right conclusion is not "PaLM solves language understanding." The right conclusion is that general-purpose pretrained models had become startlingly strong across a very broad surface area.

**BIG-bench and the language of emergent behavior**

One of the paper's most historically influential sections is the BIG-bench analysis. On the shared subset of 58 textual BIG-bench tasks used for direct comparison, PaLM 540B 5-shot beats prior state of the art on 44 tasks and, in aggregate, scores above average human performance. On the larger set of 150 textual tasks, the paper argues that performance still follows a roughly log-linear trend overall, but with many task-specific exceptions where the jump from 62B to 540B is much larger than the jump from 8B to 62B.

This is where the paper gave many readers the language of discontinuous improvement. The authors define discontinuity relative to the log-linear projection from smaller models. On tasks like `english_proverbs` or `logical_sequence`, PaLM 540B jumps much more than that simple projection would have suggested. The paper reports that across all 150 BIG-bench tasks, 25% show discontinuity greater than +10 points and 15% show discontinuity greater than +20 points.

Historically, this mattered because it supported the intuition that some capabilities do not look impressive at intermediate scale and then suddenly become usable at larger scale. But this claim should be interpreted carefully. The discontinuity measure depends on a particular extrapolation scheme from only two smaller models, and BIG-bench itself contains very heterogeneous tasks. The result is still meaningful, but it is better thought of as strong evidence that scaling curves can be uneven rather than as a complete theory of emergence.

The paper is also careful enough to mention a fact that many simplified retellings drop: even though PaLM exceeds average human performance in the aggregate, average humans still outperform it on 35% of individual BIG-bench tasks. So this is not broad human equivalence. It is benchmark-specific evidence that the model has crossed some striking thresholds.

**Reasoning, chain-of-thought, and why this paper changed prompting**

The most famous scientific result in the paper is not actually the raw parameter count. It is the interaction between scale and chain-of-thought prompting. The authors evaluate arithmetic reasoning datasets such as GSM8K, SVAMP, MAWPS, and AQuA, along with commonsense reasoning datasets such as CommonsenseQA and StrategyQA. They use 8-shot chain-of-thought exemplars following the now-canonical prompting format in which the model is shown worked intermediate reasoning steps rather than only final answers.

The GSM8K numbers show the point clearly. PaLM 540B gets 17% without chain-of-thought, 54% with chain-of-thought alone, and 58% with chain-of-thought plus an external calculator. The 62B model with chain-of-thought reaches only 33%, which means the improvement is not coming from the prompt format alone. The prompt and the model scale interact. Across seven reasoning datasets, PaLM 540B with chain-of-thought achieves new state of the art on four and comes close on the others, despite competing against systems that often rely on task-specific fine-tuning, task-specific architectures, or verifier pipelines.

This result changed the field because it reframed language generation itself as part of the computation. The model is not merely asked to output an answer. It is asked to write an intermediate reasoning trace, and that trace improves the answer. That made prompting feel less like user-interface wording and more like a way of recruiting internal competence.

Still, this section also needs sober reading. The paper does not prove that PaLM has human-like reasoning in a deep or robust sense. The gains are benchmark- and prompt-sensitive. GSM8K's best headline number also uses an external calculator. And chain-of-thought is partly a formatting intervention: it can reveal competence, but it can also scaffold brittle behavior that does not generalize cleanly outside the benchmark setup. Even with those caveats, the paper genuinely marks a turning point in how researchers thought about reasoning prompts.

**Multilingual behavior and translation**

PaLM is also a multilingual transfer paper, even though that is not the part most people remember first. Because large portions of the training mixture are multilingual webpages, conversations, and Wikipedia, the model is evaluated on translation and other multilingual tasks without being trained as a specialized translation system. On traditional WMT language pairs, PaLM 540B beats prior zero-shot and few-shot language-model baselines by large margins. For example, it reaches 44.0 BLEU on English-to-French in few-shot mode and 47.5 BLEU on German-to-English, even exceeding some older supervised baselines in the latter direction.

The translation results are interesting because they show a familiar asymmetry that later multilingual models continue to exhibit: translating into English is easier than translating out of English. The paper also shows that PaLM can do direct non-English pair translation such as French-to-German reasonably well, but performance drops more sharply on genuinely hard low-resource settings like English-Kazakh. That is a useful corrective. The paper is not saying generalist language models eliminate the need for specialist machine translation. It is saying that the generalist baseline had become unexpectedly strong.

**Code as a test of whether the model is really general**

The code section is another major reason the paper mattered. PaLM is trained on 39B code tokens total, only about 2.7B of them Python, yet it performs strongly on HumanEval, MBPP, TransCoder, GSM8K-Python, and DeepFix. The pretraining-only PaLM 540B reaches 26.2 pass@1 on HumanEval and 76.2 pass@100, broadly comparable to early Codex results despite using far less Python-specific training data. The authors interpret this as evidence that very large models can become more sample efficient and can transfer from natural language and from other programming languages into code generation.

The paper then goes a step further with PaLM-Coder, a code-finetuned variant. That model reaches 88.4 pass@100 on HumanEval and 82.1% compile rate on DeepFix. Even though that code-finetuned model is no longer the same as the pretraining-only PaLM model, the overall argument is clear: scale made it plausible to have one model family that is simultaneously strong on language and code instead of maintaining totally separate specialist systems.

This part of the paper also benefits from a cautionary reading. Good benchmark performance on code does not mean safe or trustworthy software generation. The authors themselves note that functional correctness estimates are limited by benchmark test suites and that compiled code is not necessarily secure, robust, or semantically ideal. In that sense, the paper is impressively strong but already aware of the deployment gap.

**Bias, toxicity, memorization, and the paper's attempt at realism**

Unlike some scaling papers that stop at leaderboard wins, PaLM also includes a substantial responsible-AI and memorization analysis. On Winogender, PaLM 540B achieves new state of the art among large language models in 1-shot and few-shot settings, but the details matter. The paper distinguishes multiple-choice scoring from stricter generative scoring and shows that multiple-choice evaluation can flatter performance. Under stricter generative scoring, the 540B model reaches 69.7% in 1-shot and 84.7% in 4-shot settings, still below human performance and still worse on stereotype-violating "gotcha" examples, especially for female pronouns.

The co-occurrence and toxicity analyses are even more revealing. Prompted with identity terms, the model produces associations that clearly reflect harmful stereotypes, including anti-Muslim associations such as "terrorist," "violent," and "radical." On RealToxicityPrompts, toxicity in the continuation rises with toxicity in the prompt, and the 62B and 540B models have quite similar toxicity profiles. That suggests that simply scaling from large to larger does not solve this class of problem.

The paper is also admirably explicit about methodological limits here. The evaluations are English-only, they rely in part on Perspective API scores, and template-based prompt analyses can be brittle to small phrasing changes. So the lesson is not that the paper has solved bias measurement. The lesson is that the authors understood these risks were central enough to include in the main scientific story.

The memorization analysis makes a similar move toward realism. The authors prompt the model with the first 50 tokens of sampled training sequences and ask whether it reproduces the next 50 exactly. The 8B model exactly matches 1.6% of these continuations, while the 540B model matches 2.4%. For examples seen exactly once in training, the memorization rate for the largest model is only 0.75%, but for examples duplicated more than 500 times it rises above 40%. That tells you two things at once: larger models do memorize more, and duplication structure in the data matters enormously.

Even this likely understates the broader problem, because exact-match continuation recovery is only one form of memorization. Approximate reproduction, paraphrastic leakage, and extraction under longer or more targeted prompts are not fully captured by this measurement. The paper more or less recognizes that and frames memorization risk as a function of model size, dataset content, and the downstream application context.

**How to interpret the paper historically**

PaLM sits at a very particular moment in the history of large models. It is late enough that the basic autoregressive Transformer recipe is already established, but early enough that scaling, prompting, and systems efficiency still feel like open scientific frontiers rather than settled industrial practice. It helped cement the idea that dense models still had room to improve, that benchmark behavior could change qualitatively with scale, and that prompting style was not superficial. At almost the same time, later work would shift the conversation toward compute-optimal training, stronger alignment methods, retrieval, tool use, and productization. PaLM therefore reads best as a milestone in the transition from "large language models are interesting" to "large language models are a platform."

---

## **Subtle points, clarifications, and limits**

The word "Pathways" in the title can be misleading if read too quickly. The broader Pathways vision is about modular, general systems that can route computation efficiently across tasks and modalities. PaLM is not that full vision realized. It is a dense language model trained on Pathways infrastructure. That does not diminish the result, but it does clarify what exactly the paper proved.

The paper is also famous for results that are easy to overstate in retelling. "Above average human on BIG-bench" does not mean human-level general intelligence. "Chain-of-thought reasoning" does not mean robust abstract reasoning in the strong philosophical sense. "Memorization is low" does not mean leakage is solved. The paper's actual claims are more careful than many of the summaries built on top of it, and reading it well means preserving that care.

---

## **Closing perspective**

PaLM mattered because it made frontier language modeling legible as a joint phenomenon of model scale, prompt format, and training infrastructure. It showed that a dense Transformer could still unlock striking new behavior if trained at sufficient scale, that reasoning performance could change dramatically when the prompt asked for intermediate thought, and that the systems stack itself had become part of the science. Even if later models improved the data-compute tradeoff and changed the safety and deployment conversation, this paper remains one of the clearest records of the moment when large language models became a full-stack research program.

---

## **Personal comprehension notes**

The easiest way to think about PaLM is as three achievements stacked on top of each other. The first is a broad training corpus that gives the model raw exposure to language, code, and multilingual structure. The second is a giant but still conceptually conservative dense Transformer. The third is the Pathways training substrate that makes the first two tractable at 540B scale. If any of those layers is missing, the paper as we know it does not happen.

Another useful mental model is that PaLM is the paper where prompting stopped being just phrasing and started looking like computation. Chain-of-thought works here because the model is not merely being asked for an answer; it is being induced to generate a temporary reasoning workspace in language. That does not magically turn the model into a perfect reasoner, but it does explain why the paper felt like a conceptual jump rather than just a bigger benchmark table.

A third memory hook is: Pathways is the railway system, PaLM is the train. The title includes both because the train is impressive, but the track is what made this route possible.

---

## **Compact retention notes**

- **Paper type:** Landmark scaling, model, and systems paper
- **Core idea:** Train a very large dense decoder-only Transformer efficiently with Pathways and show that scale still unlocks broad few-shot gains, especially when paired with chain-of-thought prompting.
- **Main mechanism:** 780B-token pretraining + 256k lossless tokenization + 118-layer dense Transformer + Pathways training across 6144 TPU v4 chips + broad evaluation across NLP, BIG-bench, reasoning, translation, code, and safety analyses.
- **Key result:** PaLM 540B sets new few-shot state of the art across much of the benchmark suite, shows striking gains on BIG-bench and reasoning tasks, and helps establish chain-of-thought prompting as a major capability unlock.
- **Main limitation:** The model is extremely compute-intensive, undertrained by later compute-optimal standards, and still inherits serious issues around bias, toxicity, brittleness, and memorization.

---

## **Citations used in the paper**

- Ashish Vaswani et al., *Attention Is All You Need*, 2017
- Tom B. Brown et al., *Language Models are Few-Shot Learners*, 2020
- Nan Du et al., *GLaM: Efficient Scaling of Language Models with Mixture-of-Experts*, 2021
- Romal Thoppilan et al., *LaMDA: Language Models for Dialog Applications*, 2022
- Jack W. Rae et al., *Scaling Language Models: Methods, Analysis and Insights from Training Gopher*, 2021
- Jordan Hoffmann et al., *Training Compute-Optimal Large Language Models*, 2022
- Daniel Isard et al., *Pathways: Asynchronous Distributed Dataflow for ML*, 2022
- Yuanzhong Xu et al., *GSPMD: General and Scalable Parallelization for ML Computation Graphs*, 2021
- Noam Shazeer, *GLU Variants Improve Transformer*, 2020
- Noam Shazeer, *Fast Transformer Decoding: One Write-Head is All You Need*, 2019
- Jianlin Su et al., *RoFormer: Enhanced Transformer with Rotary Position Embedding*, 2021
- Taku Kudo, John Richardson, *SentencePiece: A Simple and Language Independent Subword Tokenizer and Detokenizer for Neural Text Processing*, 2018
- Aarohi Srivastava et al., *Beyond the Imitation Game Benchmark (BIG-bench): How Hard Can It Be?*, 2022
- Jason Wei et al., *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*, 2022
- Karl Cobbe et al., *Training Verifiers to Solve Math Word Problems*, 2021
- Mark Chen et al., *Evaluating Large Language Models Trained on Code*, 2021
- Rachel Rudinger et al., *Gender Bias in Coreference Resolution*, 2018
- Samuel Gehman et al., *RealToxicityPrompts: Evaluating Neural Toxic Degeneration in Language Models*, 2020
- Nicholas Carlini et al., *Quantifying Memorization Across Neural Language Models*, 2022
