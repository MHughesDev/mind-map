# ReAct: Synergizing Reasoning and Acting in Language Models (2022)

**Paper link:** https://arxiv.org/abs/2210.03629

---

## **Paper metadata**

**Authors / collaborators:**  
- Shunyu Yao  
- Jeffrey Zhao  
- Dian Yu  
- Nan Du  
- Izhak Shafran  
- Thomas L. Griffiths  
- Yuan Cao  
- Karthik Narasimhan

**Organizations / companies / institutions involved:**  
- Princeton University  
- Google Research

**Publication date:**  
October 2022 (arXiv), later presented at ICLR 2023

**Venue / source:**  
arXiv preprint / ICLR 2023

**Research paper type / category:**  
- Method / model paper  
- Experimental / empirical paper  
- Systems / engineering paper

**Primary field / topic area:**  
Language-model agents, reasoning traces, tool use, interactive decision-making

**Keywords:**  
- ReAct  
- chain-of-thought prompting  
- action-observation loop  
- Wikipedia API interaction  
- embodied and web-based agent tasks

---

## **Opening perspective**

This paper appears at a moment when large language models were already good at producing fluent reasoning traces, but those traces often floated free from reality. A model could "reason" for many lines and still anchor itself on a wrong fact. In parallel, action-only prompting patterns could call tools or take environment actions, but without clear internal planning they were brittle and myopic. ReAct is important because it connects those two partially successful worlds into one control loop: deliberate reasoning steps and concrete environment interactions become mutually corrective rather than separate paradigms.

For anyone serious about modern AI agents, this paper is a foundational bridge. It does not offer a new trained architecture; instead it gives an interaction protocol that turned out to be widely reusable: think, act, observe, revise, repeat. That protocol became one of the conceptual seeds for later agent frameworks, tool-use systems, and planning-plus-execution designs.

---

## **Full walkthrough and explanation**

**Why the authors combine reasoning and acting**

The central claim is not that reasoning alone is bad, or that acting alone is bad. The claim is that each covers the other's blind spots. Pure chain-of-thought prompting can decompose problems but cannot fetch missing external facts by itself. Pure action trajectories can gather evidence but may choose poor next actions without a running internal model of the problem state. ReAct treats these as complementary signals inside one trajectory.

Pipeline: Prompt + task instance -> Thought -> Action -> Observation -> Thought -> ... -> Final answer or terminal action.

In this pipeline, "Thought" tokens are free-form reasoning traces that do planning, hypothesis testing, and error checking. "Action" tokens are structured commands constrained by the current environment (for example, searching Wikipedia, looking up passages, or choosing interactive actions in game-like settings). "Observation" tokens are environment returns that become new evidence. The next thought is conditioned on those observations, so the model can revise prior assumptions rather than merely extending a static plan.

**Prompting format and trajectory design**

ReAct is implemented through few-shot prompting, where exemplars are complete trajectories rather than one-shot input-output examples. Each demonstration includes interleaved Thought/Action/Observation blocks until completion. This matters because the model learns not only what an answer looks like, but what a productive process looks like under uncertainty.

The mechanism can be read as policy shaping through text. The prompt implicitly defines:

1. Which action vocabulary is legal in a task environment.  
2. When to stop thinking and execute an action.  
3. How to consume observations and update beliefs.  
4. When sufficient evidence has been gathered to commit to an answer.

Unlike learned reinforcement-learning policies, this policy is induced at inference time via exemplars and instruction style. That is both a strength (cheap adaptation, no retraining) and a limitation (sensitivity to prompt quality and model scale).

**Knowledge-intensive QA: grounding chain-of-thought with retrieval**

In question answering settings such as HotpotQA and FEVER, the model cannot rely on parametric memory alone. ReAct gives it a controlled way to consult external evidence during inference. A typical loop is:

Question -> Thought (what to verify first?) -> Search action -> Observation (retrieved snippets) -> Thought (update hypothesis) -> Lookup action -> Observation -> ... -> Answer.

This is where ReAct differs from many earlier prompting recipes. The reasoning trace is not just explanatory text generated after deciding. It actively drives information acquisition. If an observation contradicts a tentative hypothesis, the next thought can branch to a different retrieval strategy. In principle this improves factuality because claims are tied to retrieved evidence.

The paper reports stronger performance than reasoning-only and acting-only baselines in these knowledge tasks, and a qualitative gain in interpretability: a reviewer can inspect where each factual step came from. That said, interpretability here is "auditable trajectory," not guaranteed truth. A plausible trajectory can still land on wrong evidence or over-trust noisy retrieval.

**Decision-making tasks: planning under partial observability**

ReAct is also evaluated in interactive environments like ALFWorld and WebShop, where each action changes the state and observations are partial. Here the Thought step serves as a short-horizon planner and memory consolidator:

Current observation -> Thought (goal progress + next subgoal) -> Action -> New observation -> Thought (re-plan).

The benefit is especially visible when tasks require multi-step dependencies. Instead of selecting actions greedily from the latest observation, the model keeps an explicit textual plan and checks whether new evidence confirms or invalidates it. The paper shows this helps compared to simple action-only prompting.

A subtle but important point: ReAct's "reasoning" in these settings often includes operational memory ("I already searched X," "I still need Y") rather than abstract logic. That memory role is one reason interleaving can outperform a single long initial plan.

**Interpretability and human correction**

Because trajectories are explicit, a human can inspect and edit intermediate thoughts or actions. The authors show that this can rescue failed trajectories more directly than black-box output correction. Conceptually, ReAct reframes LM inference as a controllable process with intervention points, not a one-shot monologue.

This is directionally powerful, but the paper's experiments do not prove broad human-in-the-loop scalability. Manual trajectory correction is useful for analysis and targeted debugging, yet expensive at scale unless paired with automated policy improvement loops.

**What the paper gets right, and where claims must be bounded**

The strongest contribution is the interaction protocol itself. ReAct demonstrates that structured alternation between internal reasoning and external action can improve success and error recovery across multiple task types without task-specific finetuning.

However, some modern readers overextend the result into "ReAct solves hallucination." It does not. ReAct reduces certain failure modes by forcing evidence-seeking behavior, but hallucinations can still occur in at least three places: in thought (bad hypothesis), in action selection (wrong query/tool call), and in observation interpretation (misreading returned evidence). The protocol creates opportunities to self-correct; it does not guarantee correction.

Another potential overreach is to equate trajectory transparency with faithful reasoning. A readable thought trace helps debugging, but it may still be a post-hoc rationalization in some cases. So the right claim is pragmatic: ReAct gives a better interface for control and audit than opaque single-shot outputs, not a perfect window into cognition.

**Historical connection to later agent systems**

Many later agent stacks instantiate a close variant of this loop, even when they add memory buffers, tool routers, reflection modules, or verification calls. ReAct's core pattern can be recognized in modern "planner-executor" systems:

State + objective -> deliberation text -> tool action -> tool result -> revised deliberation -> next action.

What changed later is mostly the surrounding infrastructure (tool abstractions, retry logic, safety guards, long-horizon memory), not the fundamental insight that reasoning should stay coupled to environment feedback.

---

## **Subtle points, clarifications, and limits**

ReAct is a prompting framework, not a trained architecture, so performance depends heavily on model capability, prompt demonstrations, and environment design. It is most reliable when action spaces are constrained and observations are informative. In weakly structured environments, trajectories can drift, loop, or accumulate mistaken assumptions. It also inherits context-window limitations: long trajectories can crowd out crucial earlier observations unless external memory or summarization is added.

---

## **Closing perspective**

ReAct earned durable respect because it gave the field a simple, transferable control principle at exactly the right time: language models should not just narrate solutions, they should gather evidence and adapt plans while acting. Historically, this helped shift practical work from static prompting toward interactive agents. Technically, it clarified that better behavior often comes from better inference protocols, not only bigger models. It is still worth understanding because many current agent systems are, at core, elaborations of this same reasoning-action-observation loop.

---

## **Personal comprehension notes**

The most useful mental model for me is: ReAct turns an LM from "essay writer" into "investigator." In essay mode, it tries to finish the whole answer from prior beliefs. In investigator mode, it writes a short hypothesis, runs a test action, reads evidence, and updates its belief state. So instead of one long brittle chain-of-thought, you get repeated mini-cycles of hypothesis -> experiment -> revision.

Another memory anchor: chain-of-thought by itself is like thinking with your eyes closed; tool use by itself is like moving without a map. ReAct is opening your eyes while you move. That framing helps explain why it generalizes across both QA and interactive tasks.

---

## **Compact retention notes**

- **Paper type:** Prompting method + empirical evaluation for LM agents  
- **Core idea:** Interleave explicit reasoning traces with environment actions in one trajectory  
- **Main mechanism:** Thought -> Action -> Observation loops using few-shot trajectory prompts  
- **Key result:** Better task success and more debuggable behavior than reasoning-only or acting-only prompting on QA and interactive benchmarks  
- **Main limitation:** Prompt-sensitive, no guarantee of factual correctness, and can still fail through bad action choices or observation misinterpretation

---

## **Citations used in the paper**

- Wei et al., *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*, 2022  
- Yang et al., *HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering*, 2018  
- Thorne et al., *FEVER: a Large-scale Dataset for Fact Extraction and VERification*, 2018  
- Shridhar et al., *ALFWorld: Aligning Text and Embodied Environments for Interactive Learning*, 2020  
- Yao et al., *WebShop: Towards Scalable Real-World Web Interaction with Grounded Language Agents*, 2022  
- Kojima et al., *Large Language Models are Zero-Shot Reasoners*, 2022  
- Nye et al., *Show Your Work: Scratchpads for Intermediate Computation with Language Models*, 2021

---
