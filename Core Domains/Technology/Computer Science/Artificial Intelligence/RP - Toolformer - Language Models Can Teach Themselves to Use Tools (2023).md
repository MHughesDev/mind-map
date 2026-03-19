# Toolformer: Language Models Can Teach Themselves to Use Tools (2023)

**Paper link:** https://arxiv.org/abs/2302.04761

---

## **Paper metadata**

**Authors / collaborators:**  
- Timo Schick  
- Jane Dwivedi-Yu  
- Roberto Dessi  
- Roberta Raileanu  
- Maria Lomeli  
- Luke Zettlemoyer  
- Nicola Cancedda  
- Thomas Scialom

**Organizations / companies / institutions involved:**  
- Meta AI

**Publication date:**  
- February 2023 (arXiv preprint)  
- Presented at NeurIPS 2023 (Oral)

**Venue / source:**  
- arXiv (cs.CL)  
- Neural Information Processing Systems (NeurIPS 2023)

**Research paper type / category:**  
- Method / model paper  
- Experimental / empirical paper  
- Systems / engineering paper

**Primary field / topic area:**  
Tool-augmented language modeling and inference-time API use

**Keywords:**  
- tool-using language models  
- self-supervised data construction  
- API call insertion  
- retrieval and external computation  
- zero-shot generalization

---

## **Opening perspective**

Toolformer lands in a very specific tension in language modeling: large LMs can do impressive in-context adaptation, yet they remain fragile at things that are trivial for external systems, such as arithmetic, date handling, and factual lookup. The paper's main move is to treat tool use not as hand-built orchestration around a frozen model, but as a behavior that can itself be learned inside the language modeling objective.

What makes this contribution important is the framing. Instead of collecting a large supervised dataset of "when to call tools," the authors show how to bootstrap such data from the model's own generations plus a filtering signal based on next-token likelihood improvement. In other words, they use the LM's native training criterion to decide whether a tool call was useful. That becomes the bridge between raw text modeling and practical external capability.

---

## **Full walkthrough and explanation**

**Core idea: make tool use endogenous to token prediction**  
Toolformer starts from a pretrained causal LM and asks it to interleave ordinary text with API call strings. Each call has two pieces: the textual trigger plus arguments, and the returned result. If tool output helps predict subsequent tokens, then the inserted call-result pair is kept as training signal.

The key pipeline is:

Raw text + few API demonstrations -> sample candidate call positions -> generate API arguments -> execute APIs -> insert returned values -> score with LM loss reduction -> keep useful augmentations -> fine-tune LM -> inference with optional API calls

That "loss reduction" filter is the paper's central mechanism. A candidate call is not accepted just because it is syntactically plausible; it must improve predictive quality in context.

**How data generation works in detail**  
The authors provide only a handful of demonstrations per API to teach the model the textual calling format. Then, over unlabeled text, the model samples potential insertion points where an API call could appear. For each candidate:

1. The model proposes an API call (including arguments).  
2. The call is executed using the external tool.  
3. The output is written back into the sequence.  
4. The model compares predictive loss with and without that augmentation over downstream tokens.

A simple way to represent the acceptance criterion is:

$$
\Delta \mathcal{L} = \mathcal{L}_{\text{without tool}} - \mathcal{L}_{\text{with tool}}
$$

When \(\Delta \mathcal{L}\) is sufficiently positive, the example is retained. The paper does not claim this is a perfect causal estimate of utility; it is a practical proxy for "does this API usage help language modeling in this context?"

**What tools are integrated**  
Toolformer includes a heterogeneous set of APIs so the behavior is not tied to a single domain:

- calculator  
- question-answering system  
- two search engines  
- machine translation system  
- calendar

This matters because the model must learn a mixed policy over different tool affordances: when to compute, when to retrieve, when to translate, and when to stay purely internal.

**What is being learned, exactly**  
The model is jointly learning four linked decisions:

Text context -> should I call? -> which API? -> which arguments? -> how should returned text condition next-token prediction?

Most prior systems at the time either (a) kept this policy outside the LM, or (b) required stronger supervision. Toolformer's novelty is that these decisions become trainable from self-generated candidates plus filtering.

**Evaluation logic and claims**  
The paper evaluates zero-shot performance on tasks where external tools should help, and reports substantial gains while preserving general language-model behavior. The strongest claim is not "Toolformer is the best universal model"; it is that a relatively modest base LM with learned tool-use behavior can become competitive with larger plain LMs on tool-relevant tasks.

A useful interpretation is that Toolformer shifts some burden from memorization to interface learning. The model does not need to internalize all arithmetic or current facts if it can reliably invoke a calculator or retrieval tool at the right point.

**Important distinctions from later agent framing**  
It is easy to overread Toolformer through a post-2023 "agent" lens. The paper is not primarily about long-horizon planning, multi-step tool chains, reflective loops, or environment control. It is about local insertion of helpful calls within token-level generation. That narrower framing is a strength: it isolates one capability (tool invocation) and studies how to train it with minimal manual annotation.

**Where the method is strong and where it is brittle**  
The strength is scalability of supervision: once the mechanism is set up, additional training signal can be mined from large unlabeled corpora. The brittleness is that utility is judged through short-horizon loss improvements, which may miss delayed benefits, compositional workflows, or cases where a noisy tool call hurts local likelihood but helps global correctness.

Another limitation is tool interface sensitivity. If an API has unstable outputs, poor formatting, or weak argument constraints, the training signal degrades. So the method partially transfers alignment burden from "labeling tool calls" to "designing robust APIs and post-processing."

**Historical placement**  
Toolformer sits between retrieval-augmented LM work and full agentic systems. It borrows the intuition that external resources can patch LM weaknesses, but contributes a concrete self-supervised training recipe for when/where to call tools. That recipe influenced later work on function calling, planner-executor architectures, and model-native tool policies.

---

## **Subtle points, clarifications, and limits**

Toolformer is often paraphrased as "the model teaches itself to use tools," which is directionally right but incomplete. The model is not learning from pure free-form trial and error; it is constrained by seeded API demonstrations, candidate sampling heuristics, and a specific acceptance signal tied to language-model loss. The system also does not guarantee global factual correctness or robust long multi-step reasoning. It mainly improves local decisions about when external calls are likely to help next-token prediction.

Another subtlety is that reported gains depend heavily on tasks where the chosen APIs are genuinely useful. Performance uplift should not be interpreted as universal improvement over all language tasks.

---

## **Closing perspective**

Toolformer earned respect because it turned tool use from a prompt trick into a trainable model behavior with a simple, reusable objective link: keep calls that improve prediction. That idea helped normalize the view that capable LMs should be interface learners, not just text compressors. Even as newer systems move toward richer agent loops, this paper remains worth studying because it cleanly formulates the "when and how to call tools" problem in a way that scales and can be measured.

---

## **Personal comprehension notes**

The way I remember Toolformer is: "teach the LM a few examples of API syntax, let it over-propose calls, and then trust perplexity improvement as the gatekeeper." So the model is doing a kind of self-curated apprenticeship.

A second mental model: Toolformer is like adding "external function pointers" into a next-token engine. The model keeps its language prior, but learns escape hatches for operations that are easier outside its parameters.

The easiest mistake is to confuse this with autonomous agents. It is closer to disciplined inline function calling than to full decision-making over long trajectories.

---

## **Compact retention notes**

- **Paper type:** Method + empirical paper on self-supervised tool-use training  
- **Core idea:** Train an LM to insert API calls by keeping only self-generated calls that improve token prediction  
- **Main mechanism:** Candidate call generation + API execution + loss-based filtering + fine-tuning on accepted augmentations  
- **Key result:** Stronger zero-shot performance on tool-relevant tasks without losing base LM fluency  
- **Main limitation:** Local loss-based utility and tool-interface quality constrain robustness and long-horizon reasoning

---

## **Citations used in the paper**

- Brown et al., *Language Models are Few-Shot Learners*, NeurIPS 2020  
- Guu et al., *REALM: Retrieval-Augmented Language Model Pre-Training*, ICML 2020  
- Borgeaud et al., *Improving Language Models by Retrieving from Trillions of Tokens*, ICML 2022  
- Gao et al., *PAL: Program-aided Language Models*, ICML 2022  
- Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models*, ICLR 2023  
- Parisi et al., *TALM: Tool Augmented Language Models*, 2022  
- Nakano et al., *WebGPT: Browser-assisted Question-Answering with Human Feedback*, 2021  
- Zhang et al., *OPT: Open Pre-trained Transformer Language Models*, 2022  
- Costa-jussa et al., *No Language Left Behind: Scaling Human-Centered Machine Translation*, 2022  
- Schick et al., *Few-shot Learning with Retrieval Augmented Language Models*, JMLR 2022

---
