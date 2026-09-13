# Training Language Models to Follow Instructions with Human Feedback (2022)

**Paper link:** https://arxiv.org/abs/2203.02155

---

## **Paper metadata**

**Authors / collaborators:**  
- Long Ouyang  
- Jeffrey Wu  
- Xu Jiang  
- Diogo Almeida  
- Carroll L. Wainwright  
- Pamela Mishkin  
- Chong Zhang  
- Sandhini Agarwal  
- Katarina Slama  
- Alex Ray  
- John Schulman  
- Jacob Hilton  
- Fraser Kelton  
- Luke Miller  
- Maddie Simens  
- Amanda Askell  
- Peter Welinder  
- Paul Christiano  
- Jan Leike  
- Ryan Lowe

**Organizations / companies / institutions involved:**  
- OpenAI

**Publication date:**  
March 2022 (arXiv), NeurIPS 2022

**Venue / source:**  
arXiv preprint and NeurIPS 2022

**Research paper type / category:**  
- Foundational / landmark paper  
- Method / model paper  
- Experimental / empirical paper

**Primary field / topic area:**  
Alignment-oriented post-training for large language models (instruction following, preference optimization, RLHF)

**Keywords:**  
- InstructGPT  
- Reinforcement Learning from Human Feedback (RLHF)  
- Preference modeling  
- Instruction tuning  
- PPO with KL regularization  
- Helpful-Honest-Harmless behavior shaping

---

## **Opening perspective**

This paper sits at the transition point between "language models that can continue text" and "assistant-like models that try to follow user intent." Before this work, the dominant pattern was to make base models bigger and hope desired behavior would emerge from scale plus prompting. What InstructGPT demonstrated is that there is a separate optimization problem after pretraining: you can keep raw linguistic competence from next-token learning, then explicitly train behavior using human demonstrations and human preference judgments.

The important shift is not only technical but conceptual. The paper treats alignment with user instructions as something measurable and trainable, even when there is no single ground-truth answer token. That framing made post-training pipelines central to modern LLM development and changed how practitioners think about quality: not just perplexity or benchmark scores, but whether outputs are actually preferred by people for helpfulness, clarity, and safety-relevant behavior.

---

## **Full walkthrough and explanation**

**From next-token prediction to instruction-following behavior**

The base model in this paper is GPT-3 style pretraining, which gives broad world knowledge and generation ability but also leaves several practical problems for assistant use: models may ignore intent, ramble, fabricate, produce unsafe content, or optimize for plausible text continuation instead of user utility. The paper's response is to split training into behavior-shaping stages with explicit human signal.

Pipeline 1 (high level):  
Pretrained LM -> Supervised Fine-Tuning (SFT) on demonstrations -> Reward Model (RM) from rankings -> PPO optimization against RM with KL control -> InstructGPT policy

That pipeline became the canonical RLHF recipe used across many later systems.

**Stage 1: Supervised Fine-Tuning creates an instruction-conditioned policy**

The team collects prompts from two main sources: real prompts submitted to the OpenAI API (with privacy filtering and screening procedures) and prompts written by labelers. Human trainers then write high-quality responses. The model is fine-tuned on this demonstration set, producing an SFT model that is already much better at direct instruction adherence than the raw base model.

Conceptually, SFT does two things at once:
1. It teaches the model a style prior for assistant answers (concise, relevant, cooperative).
2. It gives RLHF a stable initialization so policy optimization does not start from arbitrary behavior.

Without this warm start, later reinforcement learning would be much less sample-efficient and less stable.

**Stage 2: Preference data turns subjective quality into a trainable reward**

Now the paper addresses the core challenge: many instruction tasks do not have a unique "correct" text target, but humans can often say which of two outputs is better. For each prompt, labelers rank multiple candidate responses sampled from model policies. Those pairwise rankings train a reward model that predicts human preference.

The standard preference-learning form is:

$$
P(y_w \succ y_l \mid x) = \sigma\left(r_\theta(x, y_w) - r_\theta(x, y_l)\right)
$$

where:
- \(x\) is the prompt,
- \(y_w\) is the preferred response,
- \(y_l\) is the less preferred response,
- \(r_\theta\) is the learned reward score,
- \(\sigma\) is the logistic function.

The reward model is optimized with a log-loss over these pairwise comparisons. In effect, the paper builds a "human preference proxy" that can be queried cheaply during RL, instead of asking humans at every policy update.

**Stage 3: PPO optimizes behavior while constraining drift**

After reward modeling, the policy is optimized with reinforcement learning. Crucially, this is not unconstrained reward maximization. The objective includes a KL penalty that keeps the updated policy near a reference policy (typically the SFT model), so the model cannot drift too far into degenerate high-reward artifacts.

Pipeline 2 (policy update view):  
Prompt -> Sample response from current policy -> Score with RM -> Apply PPO update with KL penalty to reference model -> Updated policy

A common abstract objective is:

$$
\max_{\pi} \ \mathbb{E}_{x, y \sim \pi(\cdot|x)}\left[r_\theta(x,y)\right] - \beta \, \mathrm{KL}\!\left(\pi(\cdot|x) \,\|\, \pi_{\text{ref}}(\cdot|x)\right)
$$

where:
- \(\pi\) is the current policy,
- \(\pi_{\text{ref}}\) is the reference policy (anchoring behavior),
- \(\beta\) controls the helpfulness-vs-drift tradeoff.

This KL-controlled PPO design is one of the most influential implementation choices in the paper. It operationalizes a practical compromise: improve preference alignment without catastrophically rewriting the model's language competence.

**What was actually compared in experiments**

The paper evaluates model variants around GPT-3 family scales (including 1.3B, 6B, and 175B baselines), with InstructGPT policies trained by the above pipeline. Human raters compare outputs on held-out prompts. The headline result is behaviorally striking: a much smaller RLHF-tuned model can be preferred over a much larger plain GPT-3 model on instruction-following quality. That directly challenges "bigger is always better" for user-facing usefulness.

The authors also report improvements on helpfulness-oriented judgments and reductions in some undesirable behaviors (for example, toxic or untruthful tendencies in certain evaluations), while acknowledging remaining failure modes.

**Why this result is technically significant**

The key insight is objective mismatch:
- Pretraining objective: predict likely next text.
- Assistant objective: satisfy user intent under social and safety constraints.

RLHF supplies a bridge between these objectives by learning from comparative human judgments. This made post-training a first-class part of LLM systems engineering.

**Important distinctions often missed**

One subtle point is that "human preference" is not identical to "truth." A response can sound better and still be wrong. The paper discusses truthfulness and toxicity evaluations, but the reward model still reflects annotator judgments under specific instructions and distributions. That means improvements are real but distribution-bound.

Another commonly missed detail is that RLHF is highly data-pipeline dependent. Prompt mix, annotator guidelines, rater expertise, and comparison sampling strategy all shape what the policy learns. So the method is less like a universal plug-in and more like a socio-technical training stack.

**Where the paper is directionally right but incomplete**

The paper's framing around helpful-honest-harmless behavior is historically important, but it does not fully solve robustness under adversarial prompting, strategic deception, or long-horizon autonomy concerns. Also, reward models can be exploited ("reward hacking"): if policy optimization finds textual quirks that score well without real quality, performance may look good on proxy reward while degrading on true user value.

The KL term and held-out human evals mitigate this but do not eliminate it. Later work on stronger evaluators, constitutional constraints, direct preference optimization variants, and process supervision can be read as attempts to improve this same core alignment loop.

**How this paper connects to adjacent work**

InstructGPT builds directly on prior preference-learning and RL-from-feedback lines, including reward learning from comparisons and earlier text-generation RLHF experiments. Its distinctive contribution is scale plus operational clarity: it turns a promising idea into a reproducible production-style pipeline for large language models.

The broader trajectory can be read as:
Pretraining scaling laws -> Prompting/in-context learning -> Instruction tuning -> RLHF post-training -> Modern chat assistants

That historical sequence is why this paper is frequently treated as a bridge document between GPT-3-era capability demonstrations and assistant-era deployment practices.

---

## **Subtle points, clarifications, and limits**

- The main achievement is better alignment to rater preferences on targeted prompt distributions, not a proof of general alignment.
- "Preferred by labelers" does not imply unbiased, globally correct, or universally acceptable behavior.
- Safety improvements are partial and evaluation-contingent; harmful or deceptive outputs can still occur.
- Reward model overoptimization remains a real risk even with PPO and KL regularization.
- Some benchmark regressions can appear when optimizing for conversational quality, because objectives are different.

---

## **Closing perspective**

This paper earned unusually high practical respect because it changed how frontier language models are trained in the final mile before deployment. It did not replace pretraining, but it redefined what comes after pretraining. The field largely accepted the lesson that behavior quality requires dedicated alignment objectives and human-centered evaluation, not just larger parameter counts. In that sense, InstructGPT is both a technical method paper and a turning point in research culture: it made post-training a core discipline in LLM engineering.

---

## **Personal comprehension notes**

The way to think about this paper is: pretraining gives a powerful "language engine," but that engine has no built-in notion of what users mean by a good answer. RLHF adds a steering system. Demonstrations show examples of desired driving; preference comparisons teach relative quality; PPO updates the steering policy while KL keeps the car from becoming a different machine altogether.

Another useful mental model is objective layering:
- Layer 1: "Can the model generate plausible text?" (pretraining)
- Layer 2: "Can the model follow instructions in expected style?" (SFT)
- Layer 3: "Given multiple plausible answers, does it choose the one humans prefer?" (RM + RL)

The conceptual win is not that RLHF is perfect. It is that alignment can be turned into an iterative optimization loop with measurable progress.

---

## **Compact retention notes**

- **Paper type:** Foundational method + empirical alignment paper
- **Core idea:** Train assistant behavior with human demonstrations and preference comparisons after pretraining
- **Main mechanism:** SFT -> reward model from ranked outputs -> PPO with KL penalty to reference policy
- **Key result:** Smaller RLHF-tuned model outputs are often preferred over much larger untuned GPT-3 outputs
- **Main limitation:** Preference optimization is a proxy that can encode bias and be gamed; it does not guarantee truth or full safety

---

## **Citations used in the paper**

- Brown et al., *Language Models are Few-Shot Learners*, 2020  
- Christiano et al., *Deep Reinforcement Learning from Human Preferences*, 2017  
- Schulman et al., *Proximal Policy Optimization Algorithms*, 2017  
- Ziegler et al., *Fine-Tuning Language Models from Human Preferences*, 2019  
- Stiennon et al., *Learning to Summarize with Human Feedback*, 2020  
- Askell et al., *A General Language Assistant as a Laboratory for Alignment*, 2021 (alignment framing context)

---
