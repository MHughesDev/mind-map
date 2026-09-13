# Language Models are Few-Shot Learners

**Paper link:** https://proceedings.neurips.cc/paper_files/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf

---

## **Paper metadata**

**Authors / collaborators:**  
- Tom B. Brown
- Benjamin Mann
- Nick Ryder
- Melanie Subbiah
- Jared D. Kaplan
- Prafulla Dhariwal
- Arvind Neelakantan
- Pranav Shyam
- Girish Sastry
- Amanda Askell
- Sandhini Agarwal
- Ariel Herbert-Voss
- Gretchen Krueger
- Tom Henighan
- Rewon Child
- Aditya Ramesh
- Daniel M. Ziegler
- Jeffrey Wu
- Clemens Winter
- Christopher Hesse
- Mark Chen
- Eric Sigler
- Mateusz Litwin
- Scott Gray
- Benjamin Chess
- Jack Clark
- Christopher Berner
- Sam McCandlish
- Alec Radford
- Ilya Sutskever
- Dario Amodei

**Organizations / companies / institutions involved:**  
- OpenAI

**Publication date:**  
28 May 2020 (arXiv); published at NeurIPS 2020

**Venue / source:**  
NeurIPS 2020 / arXiv preprint

**Research paper type / category:**  
- Foundational / landmark paper
- Method / model paper
- Experimental / empirical paper
- Systems / engineering paper

**Primary field / topic area:**  
Large language models, scaling, and in-context learning

**Keywords:**  
- GPT-3
- in-context learning
- few-shot learning
- prompting
- scaling laws
- autoregressive transformers

---

## **Opening perspective**

This paper sits at the hinge between two eras of NLP. Before it, the dominant pattern was to pretrain a model and then fine-tune it separately for each task. After it, the field increasingly treated the prompt itself as the interface to a general model. The striking thing is that the paper does not get there by inventing a radically new architecture. Instead, it asks whether scaling a familiar autoregressive transformer far enough will let it perform new tasks from instructions and examples placed directly in context, without gradient updates at all.

That question ended up mattering more than almost any single benchmark number in the paper. GPT-3 did not prove that language modeling had solved intelligence, reasoning, or truthfulness. It did show something historically decisive: a sufficiently large decoder-only model can often use task descriptions and demonstrations as temporary conditioning rather than needing task-specific weight changes. That made in-context learning, prompting, and model scale into central research objects, and much of the later LLM ecosystem can be read as either extending this result or trying to repair its weaknesses.

---

## **Full walkthrough and explanation**

**The shift from fine-tuning to in-context learning**

The paper begins from a contrast that now feels obvious but was still live in 2020. The usual recipe for strong NLP performance was: pretrain on a giant corpus, then fine-tune on thousands or tens of thousands of labeled examples for the target task. The architecture might be task-agnostic, but the workflow was not. Humans, by contrast, can often do a new language task from a short explanation or a few examples. The paper asks whether scale can push language models in that direction.

The key pipeline is:

Internet-scale pretraining -> natural-language task description and optional demonstrations in the prompt -> next-token continuation as the task answer

That means the paper is not mainly about fine-tuning GPT-3 well. In fact, it deliberately avoids fine-tuning in order to study task-agnostic behavior. The authors define four settings along a spectrum of task-specific supervision:

- Fine-tuning: update weights on a supervised dataset for the task.
- Few-shot: give the model many demonstrations in context, but do not update weights.
- One-shot: give one demonstration plus an instruction.
- Zero-shot: give only an instruction.

The conceptual move is subtle but profound. Task adaptation is no longer located in parameter updates between training runs. It is relocated into the model's forward pass, with the prompt acting as a temporary task specification. That is why the paper became so important. It made "what can the model infer from context alone?" into a serious empirical question.

**The model is mostly familiar; the regime is new**

A common misunderstanding is that GPT-3 introduced a radically different transformer. It did not. The model is basically GPT-2 scaled up aggressively, with the same autoregressive objective and broadly the same architectural style, including the GPT-2 tokenization and training conventions. The one notable architectural change the paper emphasizes is the use of alternating dense and locally banded sparse attention patterns, inspired by Sparse Transformer. The paper's main novelty is therefore not a new block or objective. It is a new scale regime and a new evaluation lens.

The authors train eight dense models ranging from 125 million parameters to 175 billion. The largest model, the one they call GPT-3, has 96 layers, model width 12,288, 96 attention heads, head dimension 128, and a context window of 2048 tokens. All eight models are trained for 300 billion tokens. That last detail matters because the paper is operating in the scaling-laws mindset: not simply "make the model as large as possible," but choose model size, batch size, and learning rate in a way that tracks compute-efficient scaling behavior.

So the model ladder is doing two jobs at once. It gives them the headline 175B system, and it also lets them study whether improvements are smooth with size rather than being a one-off lucky jump. Much of the paper's argument depends on that second point.

**Training data and why the corpus design matters**

The training corpus is large, messy, and highly consequential to the paper's later strengths and weaknesses. The authors rely heavily on filtered Common Crawl, but they do not simply dump raw web text into the model. They describe three major quality-control steps: filtering Common Crawl against higher-quality reference corpora, fuzzy deduplication within and across datasets, and adding curated datasets to improve quality and diversity.

The resulting training mixture is:

Filtered Common Crawl -> 410B tokens -> 60% of training examples  
WebText2 -> 19B tokens -> 22%  
Books1 -> 12B tokens -> 8%  
Books2 -> 55B tokens -> 8%  
Wikipedia -> 3B tokens -> 3%

Those percentages are not proportional to raw size. Higher-quality datasets are intentionally oversampled, so some corpora are seen multiple times while filtered Common Crawl and Books2 are seen less than once over 300 billion training tokens. That is an important design choice. GPT-3 is not just "the internet poured into a transformer." It is the internet after quality filtering, deduplication, and deliberate reweighting.

The corpus is still overwhelmingly English, about 93% by word count, with only about 7% in other languages. This becomes crucial later when the paper evaluates translation. GPT-3 has multilingual capability, but it is not a balanced multilingual model.

The training setup is also a systems paper in practice. The larger models are trained on Microsoft-provided V100 GPU clusters using both model parallelism within matrix multiplies and model parallelism across layers. That engineering story is not just infrastructure trivia. The paper's claim that scale changes behavior depends on making this training actually possible.

**How evaluation turns prompting into adaptation**

Once GPT-3 is trained, the paper turns task evaluation into prompt design. For few-shot learning, each evaluation example is paired with K task demonstrations sampled from the training split, all packed into the 2048-token context window. K is usually in the range of about 10 to 100 examples, depending on how much fits. On multiple-choice tasks, the model compares likelihoods of candidate completions. On free-form generation tasks, the authors use beam search. Natural-language task descriptions are sometimes added as instructions.

This is easy to understate because today prompt engineering is familiar. In 2020 this was a major reframing. The prompt is not just a convenient input format. It is the mechanism by which the model is told what kind of continuation counts as success. On LAMBADA, for instance, the few-shot framing turns the problem into an explicit fill-in-the-blank format, which helps the model infer that a single-word answer is wanted. The paper is therefore one of the first major demonstrations that formatting and examples can expose capabilities that would be much less visible under raw zero-shot prompting.

It is also worth noting what this setup is not. This is not instruction tuning, RLHF, chat-style post-training, or tool use. GPT-3 here is a raw pretrained model evaluated through prompt conditioning alone. That makes the results historically cleaner, but it also explains some of its brittleness.

**What the scaling curves say before the benchmarks**

Before getting into individual tasks, the paper makes a broader claim about scale. Validation loss continues the smooth power-law behavior highlighted in the earlier scaling-laws work. More importantly, many downstream tasks also improve fairly smoothly with model size. The paper repeatedly emphasizes that zero-shot, one-shot, and few-shot performance all generally rise with scale.

One of the most interesting observed patterns is that the gap between zero-shot and few-shot performance often grows with model size. The larger models do not just know more facts. They also seem increasingly able to make use of demonstrations in context. The authors cautiously suggest that larger models may be better meta-learners. That is directionally right, though later work made clear that "meta-learning" here should be understood carefully. Some tasks likely involve genuine adaptation to the prompt, others are probably better seen as task recognition or pattern completion based on structures learned during pretraining.

Still, the broad empirical message is clear: scale does not merely reduce perplexity. It changes what kinds of task behavior become available through prompting.

**Language modeling and cloze tasks: where the prompt starts to look powerful**

The first results section covers traditional language modeling, cloze, and completion tasks. On Penn Treebank, GPT-3 achieves zero-shot perplexity 20.5, substantially better than the prior zero-shot SOTA 35.8. That matters less as a practical benchmark and more as evidence that plain next-token modeling continues to improve strongly with scale on a clean old dataset that largely escapes contamination concerns.

The more famous result in this section is LAMBADA. In zero-shot, GPT-3 reaches 76.2% accuracy, already above the previous state of the art. In few-shot, after reframing the task as explicit fill-in-the-blank completion, it reaches 86.4%, a huge jump. This is one of the paper's clearest demonstrations that few-shot prompting is not just about adding examples mechanically. The examples tell the model what kind of completion counts as success, and larger models can exploit that framing much better than smaller ones.

The section is also useful because it already shows the paper's unevenness. GPT-3 is strong but not universally dominant. On HellaSwag it reaches 79.3% few-shot, better than some earlier language-model baselines but still below the overall SOTA of 85.6. On StoryCloze it reaches 87.7% few-shot, still behind the best fine-tuned BERT-style system. So even in this early section, the paper is not saying "few-shot prompting beats fine-tuning everywhere." It is saying that the gap has narrowed dramatically on many tasks, enough that the old workflow can no longer be treated as obviously necessary.

**Closed-book question answering: knowledge stored in the weights**

The closed-book QA section is where GPT-3 most clearly looks like a model that has absorbed a lot of world knowledge into parameters. Unlike open-domain QA systems that retrieve relevant documents at test time, GPT-3 has to answer from what is already in its weights and from the prompt format alone.

On TriviaQA, GPT-3 gets 64.3% zero-shot, 68.0% one-shot, and 71.2% few-shot. That few-shot result beats the cited open-domain RAG system at 68.0 and exceeds the fine-tuned closed-book T5-11B numbers by a substantial margin. On WebQuestions, GPT-3 rises from a weak 14.4% zero-shot to 41.5% few-shot, approaching the fine-tuned T5-11B+SSM result of 44.7. On Natural Questions it climbs from 14.6% to 29.9%, still below strong fine-tuned systems but clearly benefiting from in-context examples.

The pattern matters more than any single number. GPT-3 seems to contain a great deal of factual knowledge, but whether that knowledge becomes usable depends strongly on task format and distribution match. TriviaQA is relatively favorable. Natural Questions is harder, possibly because it asks for more fine-grained Wikipedia-style knowledge and answer formatting. So the right interpretation is not "the model just knows everything." It is "the model stores enough broad statistical knowledge that prompting can sometimes turn it into competitive closed-book QA."

**Translation: surprisingly strong, but not symmetrically multilingual**

The translation section is easy to overlook, but it tells you a lot about what GPT-3 is and is not. The model was trained mostly on English, without a translation-specific objective, back-translation pipeline, or supervised bilingual fine-tuning. Even so, it shows meaningful multilingual behavior.

Zero-shot translation underperforms dedicated unsupervised NMT systems. But one-shot and few-shot prompting change the picture sharply. A single demonstration often adds more than 7 BLEU, and few-shot improves further. GPT-3's best few-shot scores are especially strong when translating into English: 39.2 BLEU for French to English, 40.6 for German to English, and 39.5 for Romanian to English. Translation out of English is noticeably weaker, with English to Romanian especially bad at 21.0 BLEU.

That asymmetry is exactly what you would expect from a model whose training corpus is dominated by English and whose tokenizer was inherited from GPT-2's English-heavy setting. The paper explicitly suggests the byte-level BPE tokenizer may be part of the weakness. This is a good example of the paper teaching both capability and limitation at the same time. Yes, GPT-3 can do translation through prompting alone. No, that does not make it a clean replacement for dedicated multilingual translation systems.

It is also important that the paper itself notes these results are not strictly comparable to fully unsupervised translation, because one-shot and few-shot prompting include paired examples in context. The demonstrations are small, but they are still task-specific bilingual supervision at inference time.

**Reasoning-style benchmarks reveal both strength and fragility**

The middle of the paper is where GPT-3 starts to look both impressive and obviously incomplete. On the original Winograd schemas, GPT-3 is strong in all settings, reaching 89.7% one-shot and 88.6% few-shot, close to fine-tuned systems. On Winogrande, the harder adversarial version, it reaches 77.7% few-shot, competitive but below the 84.6 SOTA. On PIQA, GPT-3 reaches 82.8% few-shot and even exceeds the cited prior SOTA, though that result is later marked with an asterisk because contamination or statistical bias may be helping.

Then the cracks become more visible. On ARC Challenge, GPT-3 hovers around the low 50s, far below the best specialized systems. On OpenBookQA it improves from 57.6 zero-shot to 65.4 few-shot, but still trails the top models by a wide margin. On reading comprehension the picture is mixed: GPT-3 is fairly strong on CoQA at 85.0 F1 and improves substantially on SQuAD 2.0 to 69.8 F1 in few-shot mode, yet it remains weak on QuAC, DROP, and especially RACE.

SuperGLUE makes the unevenness even clearer. GPT-3's few-shot average is 71.8. That is respectable, and on some tasks it is genuinely strong: COPA is 92.0, ReCoRD is 90.2 accuracy / 91.1 F1, and WSC is solid. But WiC sits at 49.4%, essentially chance. The paper flags a pattern that later readers should take seriously: GPT-3 seems weak on several tasks that require comparing two pieces of text carefully, such as sentence-pair inference or word-sense comparison. The ANLI and RTE results reinforce this. In other words, scaling a decoder-only language model gives broad transfer, but it does not automatically produce robust sentence-pair reasoning or careful bidirectional comparison.

This part of the paper is often flattened in popular memory. GPT-3 did not simply dominate NLP benchmarks. It mixed near-breakthrough behavior on some task families with near-random weakness on others.

**Synthetic and qualitative tasks: the most forward-looking part of the paper**

The benchmark tables established that GPT-3 can often compete without fine-tuning. The synthetic and qualitative tasks are what made many readers feel that something more general was happening. Here the authors stop relying only on standard benchmarks and instead ask whether GPT-3 can adapt to prompt-defined tasks that are unlikely to have been seen in exactly that form during training.

Arithmetic is the cleanest example. In few-shot mode, GPT-3 gets 100.0% on two-digit addition, 98.9% on two-digit subtraction, 80.4% on three-digit addition, 94.2% on three-digit subtraction, 29.2% on two-digit multiplication, and 21.3% on simple composite expressions. Those are not the numbers of a model with general mathematical reliability, but they are high enough to show that prompt-conditioned computation is happening to some extent. The authors even spot-check the training data and find very few exact arithmetic overlaps, with many wrong answers looking like imperfect algorithmic attempts rather than memorized lookup failures.

The word-scrambling tasks push this further. These tasks are artificial, character-level, and awkward for a BPE-based language model, yet the largest model can learn some of them from examples in context. SAT analogies are another striking result: GPT-3 reaches 65.2% few-shot, above the cited average student score of 57%. The paper also shows plausible few-shot use of novel words in sentences and few-shot grammar correction.

The news-generation study is the most socially loaded of these qualitative sections. Human raters asked to distinguish real short news articles from GPT-3 outputs are only about 52% accurate on the 175B model, barely above chance. This result is not a proof of truthfulness or deep understanding. In fact the paper notes factual inaccuracies, repetition, and subtle incoherence. But it is a powerful demonstration that GPT-3 can generate fluent genre-conforming text good enough to worry seriously about misuse.

Taken together, these sections are why the paper felt bigger than a benchmark paper. It suggested that the prompt could be used to define tasks on the fly, and that scaling unlocks a broader behavioral repertoire than many researchers expected.

**The contamination analysis is unusually important**

Because GPT-3 is trained on internet-scale data, the paper spends serious effort on benchmark contamination. This matters because a model trained on massive web corpora can easily encounter test-set material or closely overlapping text during pretraining. The authors actually tried to remove overlaps before training, but a bug caused only partial removal. Since retraining was too expensive, they performed a post hoc contamination analysis.

Their method is intentionally conservative: build cleaned benchmark subsets by removing examples with 13-gram overlaps to pretraining data, then compare scores on the clean subset versus the full benchmark. The broad result is more nuanced than casual summaries suggest. Contamination appears frequent, but in most cases the score changes are small. The paper concludes either that the conservative analysis overestimates contamination or that contamination often has limited effect.

Still, there are real caveats. PIQA is marked because the clean subset causes a noticeable drop and the data collection process may have exposed some relevant source material. Winograd is marked because many schemas were indeed found in the training data. LAMBADA appears genuinely contaminated to some degree, although the performance shift on the clean subset is small. And several classic language modeling benchmarks derived from Wikipedia are omitted entirely because they are too contaminated to trust. This part of the paper deserves respect. It does not solve the contamination problem, but it is much more careful about it than people often remember.

**What the paper itself says about its limits, and what later history makes clearer**

The limitations section is one of the most revealing parts of the paper. GPT-3, despite its fluency, still repeats itself, loses coherence over long passages, contradicts itself, and sometimes drifts into non sequiturs. On discrete tasks it has glaring weak spots, especially common-sense physics questions, sentence-comparison tasks like WiC and ANLI, and parts of reading comprehension. The authors suggest that some of these weaknesses may reflect the limitations of pure autoregressive modeling relative to bidirectional or denoising objectives.

They also make a deeper point that is easy to miss: next-token prediction may itself become a bottleneck. It weights every token equally, it does not directly optimize what humans most care about, and it leaves the model ungrounded in modalities like action, vision, and physical experience. They explicitly raise future directions such as learning objectives from humans, reinforcement learning, multimodal grounding, and distillation.

This is where later history sharpens the interpretation of GPT-3. The paper was right that scale unlocks broad in-context behavior. But later systems became substantially more useful not just by getting larger, but by adding post-training, better instruction following, RLHF-style alignment, retrieval, tools, longer context windows, and stronger steering. So the paper should not be read as proving that scale alone is sufficient for reliable language intelligence. It should be read as proving that scale is a major ingredient and that prompt-conditioned transfer is real.

**Broader impacts are part of the main argument, not an afterthought**

The paper's broader-impacts section is also integral to understanding why GPT-3 mattered. The authors do not just mention misuse in passing. They connect the model's news-generation ability to concrete concerns about spam, phishing, misinformation, and social engineering. They also analyze bias along gender, race, and religion, concluding that internet-trained models inherit internet-scale biases. Occupation prompts skew male, racial sentiment is uneven, and some religious associations are clearly problematic. The paper further acknowledges the energy cost of training a model at this scale.

This section does not resolve those issues, and some of its analyses are preliminary by the authors' own admission. But it matters historically because the paper is not merely triumphalist. It presents GPT-3 as both a capability milestone and a source of real deployment risk.

**How to read the paper historically**

The deepest legacy of the paper is not any single dataset result. It is the change in interface it made plausible. Before GPT-3, the natural question was often "how do we fine-tune for this task?" After GPT-3, a new question became unavoidable: "can the prompt specify the task well enough that the base model already knows how to do it?" That is the real historical break.

The paper also gave the field a new decomposition of language-model progress. Instead of thinking only about parameter counts or perplexity, it encouraged researchers to track zero-shot, one-shot, and few-shot behavior separately and to study how scale changes the ability to use context. That is why the work is canonical in the scaling literature, in the history of prompting, and in the origin story of modern LLM product interfaces.

At the same time, the paper remains worth reading because it preserves the original ambiguity. GPT-3 is broad but brittle, fluent but unreliable, adaptable but ungrounded, and impressive without being close to general intelligence. Later LLM development makes much more sense when you see that those tensions were already visible here.

---

## **Subtle points, clarifications, and limits**

Few-shot learning here does not mean the model updates its weights during inference. All of the adaptation is happening through context conditioning inside a fixed pretrained model. That sounds obvious now, but it is essential to keep separate from both fine-tuning and later instruction-tuned chat behavior. GPT-3 in this paper is a raw autoregressive model, and many of its best results depend on careful prompt format choices and on selecting how many demonstrations fit inside a 2048-token context window.

It is also easy to overread "few-shot" as if it meant robust human-like abstraction. The paper does not justify that conclusion. Some tasks really do look like rapid adaptation to a new format, especially the synthetic ones. Others may be closer to task recognition using patterns already distributed through pretraining. The paper itself raises that ambiguity, and later work only made it more important.

Finally, the paper's strongest claim is uneven capability emergence, not universal competence. GPT-3 is excellent on some tasks, mediocre on others, and near chance on a few. That unevenness is not an embarrassing side note. It is one of the main truths the paper teaches.

---

## **Closing perspective**

This paper earned unusual status because it changed what researchers thought a language model interface could be. It showed that a single large autoregressive model could often be steered into translation, question answering, cloze completion, analogy solving, arithmetic, and free-form generation by examples and instructions alone. That did not solve reliability, truthfulness, bias, or reasoning, and the paper is explicit about those shortcomings. But it made prompting and in-context learning impossible to dismiss as curiosities.

Historically, the paper now has canonical status across several communities at once: frontier-model researchers, scaling-law researchers, prompt-engineering practitioners, and people trying to understand why modern LLM systems look the way they do. It is still worth studying closely because later progress did not replace its core insight. It mostly built a larger stack around it.

---

## **Personal comprehension notes**

The easiest way to think about GPT-3 is: pretraining packs a huge library of patterns, facts, genres, and task formats into the weights, and the prompt acts like a temporary program that selects which part of that library should activate. The model is not literally "learning a new task" in the same way a person might, but it is often doing something more interesting than rote recall. It is inferring the intended continuation game from the examples.

Another good memory hook is:

Pretrain on text -> hide many tasks inside next-token prediction -> reveal a task by formatting the prompt correctly

That is why this paper made prompts so important. A prompt is not just a question. It is a miniature environment that tells the model what kind of behavior is being requested.

One more useful intuition is that GPT-3's capabilities are broad because language contains traces of many tasks, but its failures are broad for the same reason. If everything is learned indirectly through text prediction, then factual knowledge, genre imitation, weak reasoning strategies, stereotypes, and brittle shortcuts all get loaded together. Scale amplifies the useful regularities, but it also amplifies the system's reach and its failure surface.

---

## **Compact retention notes**

- **Paper type:** Landmark scaling and in-context learning paper
- **Core idea:** A sufficiently large decoder-only language model can perform many tasks from instructions and examples in context instead of task-specific fine-tuning.
- **Main mechanism:** Train a 175B GPT-style autoregressive transformer on a filtered web/books/Wikipedia mixture, then evaluate it in zero-shot, one-shot, and few-shot settings by prompt conditioning alone.
- **Key result:** GPT-3 shows strong few-shot performance on many benchmarks, especially LAMBADA, closed-book QA, translation into English, and several prompt-defined synthetic tasks, while producing short news text that humans struggle to distinguish from real articles.
- **Main limitation:** The behavior is highly uneven and brittle, with major weaknesses on sentence-comparison tasks, some reasoning and reading-comprehension benchmarks, plus contamination, bias, cost, and reliability concerns.

---

## **Citations used in the paper**

- Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, *Language Models are Unsupervised Multitask Learners*, 2019
- Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, Dario Amodei, *Scaling Laws for Neural Language Models*, 2020
- Rewon Child, Scott Gray, Alec Radford, Ilya Sutskever, *Generating Long Sequences with Sparse Transformers*, 2019
- Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova, *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*, 2018
- Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, Peter J. Liu, *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer*, 2020
- Patrick Lewis, Ethan Perez, Aleksandara Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Kuhn, Barlas Oguz, Gabriel Ilharco, Wen-tau Yih, Sebastian Riedel, Douwe Kiela, *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, 2020
- Alexis Conneau, Guillaume Lample, *Cross-lingual Language Model Pretraining*, 2019
- Kaitao Song, Xu Tan, Tao Qin, Jianfeng Lu, Tie-Yan Liu, *MASS: Masked Sequence to Sequence Pre-training for Language Generation*, 2019
- Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, Veselin Stoyanov, *RoBERTa: A Robustly Optimized BERT Pretraining Approach*, 2019
- Rowan Zellers, Ari Holtzman, Yonatan Bisk, Ali Farhadi, Yejin Choi, *HellaSwag: Can a Machine Really Finish Your Sentence?*, 2019
- Yonatan Bisk, Rowan Zellers, Ronan Le Bras, Jianfeng Gao, Yejin Choi, *PIQA: Reasoning about Physical Commonsense in Natural Language*, 2019
- Adina Williams, Nikita Nangia, Angeliki Lazaridou, *SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems*, 2019
- Yixin Nie, Adina Williams, Emily Dinan, Mohit Bansal, Jason Weston, Douwe Kiela, *Adversarial NLI: A New Benchmark for Natural Language Understanding*, 2019
- Yonatan Bisk, Ari Holtzman, Jesse Thomason, Jacob Andreas, Yoshua Bengio, Joyce Chai, Mirella Lapata, Angeliki Lazaridou, Jonathan May, Aleksandr Nisnevich, Nicolas Pinto, Joseph Turian, *Experience Grounds Language*, 2020
