# AutoGPT and Agent Frameworks

**Paper link:** https://arxiv.org/abs/2308.11432

---

## **Paper metadata**

**Authors / collaborators:**  
- Lei Wang
- Chen Ma
- Xueyang Feng
- Zeyu Zhang
- Hao Yang
- Jingsen Zhang
- Zhiyuan Chen
- Jiakai Tang
- Xu Chen
- Yankai Lin
- Wayne Xin Zhao
- Zhewei Wei
- Ji-Rong Wen

**Organizations / companies / institutions involved:**  
- Gaoling School of Artificial Intelligence, Renmin University of China
- Renmin University of China

**Publication date:**  
August 2023 (original arXiv release; later revised and journal-published)

**Venue / source:**  
arXiv preprint, *A Survey on Large Language Model based Autonomous Agents*; later published in *Frontiers of Computer Science*

**Research paper type / category:**  
- Survey / review paper
- Tutorial / pedagogical paper
- Interdisciplinary paper

**Primary field / topic area:**  
LLM-based autonomous agents, agent architectures, and agent evaluation

**Keywords:**  
- AutoGPT
- LLM-based autonomous agents
- memory and planning
- tool-using agents
- agent evaluation

---

## **Opening perspective**

If you want a serious research anchor for the 2023 AutoGPT wave, this survey is much more useful than the AutoGPT repository itself. The repository showed the public what an "agent loop" looked like, but this paper tries to explain what that loop is made of, how researchers were already building related systems, where the main application areas were appearing, and how one should evaluate all of it without getting carried away by demos.

That is why this note is best read as a map of the early agent-framework boom rather than as the story of one product. The authors are trying to turn a rapidly exploding ecosystem into an intelligible field. Their central move is to say: if you look across these systems carefully, most of them can be discussed in terms of profiling, memory, planning, and action, and then further compared by how they gain capability, what they are used for, and how they are evaluated.

---

## **Full walkthrough and explanation**

**Why this paper became the academic anchor for "AutoGPT-style" systems**

The paper opens from a classical autonomous-agent definition and then places LLM agents against older reinforcement-learning-style agents that were trained in narrow, isolated environments. The authors think LLMs changed the situation because pretrained language models arrive with broad linguistic competence, broad world knowledge, and a natural-language interface. That made it possible to use them as central controllers inside more elaborate loops.

That framing is historically important, but it should be read with one correction in mind. The paper sometimes talks as though broad pretraining pushes us close to "human-level intelligence." That is too strong. What LLMs actually supplied was a flexible prior over language, tasks, and world descriptions, which made agent scaffolds much easier to build. They did not, by themselves, solve robustness, grounding, long-horizon control, or reliable reasoning. In fact, the later sections on hallucination, prompt fragility, and evaluation quietly show that the gap remains large.

The real contribution of the paper is therefore taxonomic, not algorithmic. It does not introduce a new canonical agent architecture that everyone then adopted. It gives a vocabulary for describing a whole family of systems that were emerging at once. That is exactly why it works so well as the best research note for "AutoGPT and agent frameworks." AutoGPT is only one visible node in a larger design pattern.

**The unified architecture is the paper's backbone**

The survey's central pipeline is:

Role or profile -> memory state -> planning -> action -> environmental or model feedback -> memory update -> next step

This should not be mistaken for a law of nature. It is a descriptive framework the authors use to organize prior work. Real systems often blur these boundaries. Some collapse memory and planning into one prompt. Some use no explicit profile. Some replace part of the planning problem with a tool call or external search procedure. Still, the framework is useful because it separates four recurring design questions: who the agent is supposed to be, what it can remember, how it decides what to do next, and how it turns that decision into an actual effect.

### **Profiling as role-conditioning**

The profiling module is the answer to the question "what kind of agent is this supposed to be?" In many LLM agents, that information is injected directly into the prompt as role description, persona, responsibility, demographic information, or social relationship information. The authors treat this as foundational because the role specification shapes downstream memory use, planning behavior, and action style.

They identify three main profiling strategies. The first is **handcrafting**, where a designer explicitly writes the role: teacher, programmer, critic, extrovert, introvert, judge, and so on. This is the most obvious strategy and still the default in many agent demos because it is flexible and cheap to prototype. The second is **LLM-generated profiling**, where a small seed set of profiles or generation rules is given and the model expands them into a larger synthetic population. The third is **dataset alignment**, where real demographic or behavioral data are converted into prompts so the agent population reflects a real observed distribution rather than an invented one.

This section matters because it makes a subtle point that later agent discourse often blurred: role-playing is not the same thing as competence. A model can be convincingly prompted as a chemist, a judge, or a product manager without actually having reliable domain-level reasoning. The paper does not fully emphasize that distinction, but it becomes essential whenever agent systems are deployed in higher-stakes settings.

### **Memory as context, storage, and abstraction**

The memory module is where the survey becomes much more concrete. The authors argue that agents need memory because they operate in dynamic environments and long-horizon tasks. Without some way to carry information across steps, each action is basically a fresh isolated completion rather than part of a coherent process.

They divide memory structure into **unified memory** and **hybrid memory**. Unified memory is effectively short-term memory only: relevant observations, plans, and recent context are kept directly in the prompt or context window. Hybrid memory adds a longer-term store, usually external to the immediate prompt, that the agent can query when needed. This is the structure most people now associate with agent systems: local context plus retrieval or persistent storage.

The paper then makes a second distinction by memory format. Memory can be stored as raw natural language, as embeddings, as database entries, or as more structured lists and trees. This is a useful engineering observation. Natural language is flexible and semantically rich; embeddings support retrieval; databases support precise manipulation; structured lists make plans and subgoals explicit. Many systems combine these rather than choosing only one.

What really makes this section strong is that it does not stop at storage. It explains memory as a set of operations: reading, writing, and reflection.

When the agent reads memory, the paper summarizes the common retrieval logic with:

$$
m^* = \arg\max_{m \in M} \left(\alpha s^{rec}(q,m) + \beta s^{rel}(q,m) + \gamma s^{imp}(m)\right)
$$

Here `q` is the current query or task context, `M` is the memory store, `s^{rec}` scores recency, `s^{rel}` scores relevance, and `s^{imp}` scores importance. The balancing weights `\alpha`, `\beta`, and `\gamma` let a designer decide what sort of retrieval behavior matters most. This is a simple but clarifying abstraction: agent memory is not just "store everything." It is "decide what can still guide action now."

Memory writing introduces other problems. Similar memories may pile up redundantly. Storage may overflow. Systems therefore need compression, merging, deletion, or replacement rules. This is where many real agent systems become messier than their demos suggest, because bad memory hygiene quickly produces drift, contradiction, and useless prompt bloat.

The most interesting operation is **memory reflection**. Instead of merely storing past observations, the agent summarizes them into higher-level insights. The survey uses work like Generative Agents and GITM to show how many low-level events can be condensed into a more general pattern. That matters because intelligent behavior often depends less on remembering every fact than on forming reusable abstractions from experience.

This is one of the survey's best ideas, but it also needs a reality check. The analogy to human memory is productive, yet loose. A vector database plus prompt summaries is not literally human memory, and current agents often "reflect" in a far shallower way than the word suggests. Even so, the paper is right that memory design is one of the core differentiators between toy loops and systems that can sustain longer tasks.

### **Planning as decomposition, search, and replanning**

If memory manages the past, the planning module manages the future. The authors divide planning into two major regimes: planning **without feedback** and planning **with feedback**.

In the first regime, the system tries to decompose a task up front. The simplest case is **single-path reasoning**, where one chain of intermediate steps leads to the answer or action sequence. Chain-of-thought prompting and zero-shot "think step by step" prompting belong here. More elaborate versions, like ReWOO or HuggingGPT, still keep the basic idea that a plan can be laid out before or alongside execution.

The next step is **multi-path reasoning**, where the system explores multiple possible branches. Self-consistency, Tree of Thoughts, Graph of Thoughts, and related work fit this pattern. The paper's organizing intuition is that the planner should not commit too early if several plausible next moves exist. Once you see this, it becomes easier to interpret later agent work as a tradeoff between search quality and cost.

The third branch is **external planning**, where the LLM does not shoulder the whole planning burden alone. Instead, it translates the problem into a more formal planner-friendly representation and lets a separate planning system compute part of the solution. This is important because it shows the field learning, even in 2023, that LLM planning is not universally reliable and that specialized planners still matter.

But the deeper move comes when the authors switch to planning with feedback. This is where agent systems start to look distinctly different from one-shot prompt engineering. The key idea is:

Goal -> provisional plan -> action -> feedback from world, human, or model -> revised plan -> next action

The paper then sorts feedback into three types.

**Environmental feedback** comes from the world or simulator. ReAct is the clean example: thought, action, observation, then new thought. Embodied systems like Voyager, Ghost, SayPlan, DEPS, and Inner Monologue expand this further by using execution traces, task failures, scene descriptions, or state changes to revise plans.

**Human feedback** enters when the agent asks for clarification or correction. This is especially important when the world is ambiguous or when the agent needs to align with user preferences rather than merely optimize a simulator-defined objective.

**Model feedback** is the self-critique family: Self-Refine, SelfCheck, InterAct, ChatCoT, Reflexion. Here the agent or an auxiliary model critiques an attempted trajectory and uses that critique to improve later decisions.

This part of the survey is conceptually very strong. It correctly identifies feedback loops as one of the main reasons agent systems looked more powerful than static prompting. But it also points toward the main failure mode of the entire field. Replanning can create the appearance of autonomy while simply propagating earlier mistakes through a longer loop. If the observations are wrong, the memory is noisy, or the critic is unreliable, more steps do not necessarily mean more intelligence. They may just mean more opportunities to drift.

### **Action is where the system finally touches reality**

The action module translates decisions into outcomes. The authors analyze it through four angles: action goal, action production, action space, and action impact.

The **goals** may be task completion, communication, or exploration. This reminds the reader that agents are not only tool-users completing checklists. Some are collaborators, some are simulators, and some are explorers.

The **production** of action can come from memory recollection or from following an explicit plan. This is a useful distinction because some agents behave like retrieval-guided responders while others behave like plan executors.

The **action space** is split between external tools and internal model capabilities. External tools include APIs, databases, knowledge bases, and other models. Internal capabilities include planning, dialogue, and common-sense reasoning already present in the LLM. This division is especially important for understanding the early AutoGPT era. Much of the "agent magic" came not from the LLM alone, but from the combination of LLM plus external affordances.

The **impact** of action can change the environment, change the agent's internal state, or trigger additional actions. That last point matters because one successful action often expands what is now possible. Long-horizon behavior is path-dependent.

Historically, this is also where AutoGPT should be placed. The survey does not treat AutoGPT as the scientific center of the field. It appears as one entry among many in a broader ecosystem, characterized by planning with feedback, some memory structure, and tool use. That is the right way to remember it: not as the definitive agent paper, but as a public-facing instance of a wider architectural pattern.

**Capability acquisition is the survey's second major axis**

After architecture, the paper asks a different question: once you have an agent structure, how does it become good at anything? The authors call architecture the "hardware" and capability acquisition the "software." That is not a perfect metaphor, but it is useful. One question is how the loop is built; the other is how the loop gains useful behaviors.

They divide acquisition into methods **with fine-tuning** and **without fine-tuning**.

With fine-tuning, capability comes from data. The paper describes three data sources: human annotation, LLM-generated data, and real-world datasets. This is straightforward but important because it reminds the reader that not all agent capability gains come from clever prompting. Some come from ordinary supervised adaptation.

Without fine-tuning, the survey distinguishes **prompt engineering** from **mechanism engineering**. Prompt engineering tries to write helpful knowledge or procedures into prompts. Mechanism engineering is more structural: it changes how the agent operates.

The mechanism-engineering section is especially valuable because it names several patterns that showed up repeatedly in 2023:

- trial-and-error with critics or validators
- crowd-sourcing or debate across multiple agents
- experience accumulation in memory or skill libraries
- self-driven evolution through feedback and self-generated goals

This is one of the clearest places where the survey captures what was really happening in the field. Many gains that were publicly described as "the model got smarter" were actually gains from scaffolding, tools, memory, verification, or multi-step control. The paper sees that clearly. What it underplays is how dependent those gains remain on model quality, task framing, and environment design. The mechanism can help, but it cannot reliably rescue a weak base model from poor grounding.

**The application sections show breadth, but also early-stage evidence**

The survey then broadens from architecture to use cases. It organizes applications across **social science**, **natural science**, and **engineering**.

In social science, the paper discusses psychology, political science and economics, social simulation, jurisprudence, and research assistance. The common theme is that LLM agents can simulate people, produce dialogue, or assist with structured knowledge work. This includes both benign assistant roles and more ambitious social simulation settings.

In natural science, the authors focus on documentation, data management, experiment assistance, and education. Here the agent is imagined as a research aide that can search, summarize, plan procedures, and help interpret or teach technical material.

In engineering, the paper covers software engineering, industrial automation, robotics, and embodied AI, then closes by discussing open-source libraries such as AutoGPT, LangChain, WorkGPT, GPT-Engineer, AgentVerse, and others. This is the part that most directly connects the survey to the public "agent framework" boom.

The important thing to notice is that the construction section is analytically deep, while the application section is much broader and shallower. That is not a flaw so much as a limitation of surveying a fast-moving field. The breadth is real, but the evidence is uneven. Many examples are proofs of concept, GitHub projects, or early studies rather than settled demonstrations of robust deployment. So this part of the paper should be read partly as a map of ambitions and emerging directions, not just a ledger of mature successes.

**Evaluation is where the paper becomes most sober**

One of the most useful parts of the survey is the evaluation section, because it acknowledges how hard it is to know whether an agent is actually good.

The paper divides evaluation into **subjective** and **objective** forms.

Subjective evaluation includes human annotation and Turing-test-style discrimination. These are useful when the property being measured is difficult to formalize, such as realism, helpfulness, or human-likeness. But they are expensive, slow, and biased by evaluator population.

Objective evaluation is unpacked into three layers: metrics, protocols, and benchmarks.

For **metrics**, the authors highlight task success, human similarity, and efficiency. This is a good triad because it separates "did it finish the task?" from "did it behave plausibly?" and "what did it cost?"

For **protocols**, the survey identifies real-world simulation, social evaluation, multi-task evaluation, and software testing. This is useful because it shows agent evaluation is not one thing. A Minecraft benchmark, a collaborative social-simulation benchmark, and a bug-reproduction benchmark are testing very different abilities.

For **benchmarks**, the paper names environments like ALFWorld, IGLU, Minecraft, AgentBench, ToolBench, WebShop, Mobile-Env, WebArena, SocKET, and others. The field was clearly moving toward more standardized evaluation, but the paper also makes clear that no single benchmark captures the whole phenomenon.

This section indirectly reveals one of the deepest truths about agent frameworks: they are harder to evaluate than ordinary single-turn models because success depends on interaction, tools, long-horizon trajectories, error recovery, and cost over time. The paper does not fully solve that problem, but it sees it. That alone makes it more useful than many purely enthusiastic 2023 agent writeups.

**What the paper adds beyond individual agent papers**

The survey's unique value is not that it proves a single theory of agency. Its value is that it imposes an organized conceptual grid on a field that was at risk of becoming pure demo culture.

Before a paper like this, one might read ReAct, Toolformer, HuggingGPT, Generative Agents, Reflexion, Voyager, AutoGPT, ChatDev, and MetaGPT as unrelated bursts of creativity. The survey shows they can instead be located inside a common design space:

- profile the agent
- give it memory
- give it a planning strategy
- let it act through tools or language
- improve it through data, prompting, or mechanism design
- evaluate it in environments that match the intended use

That is not a final theory of agents, but it is a highly useful field map.

**The challenge section is the paper's own warning label**

The authors close with six major challenges: role-playing capability, generalized human alignment, prompt robustness, hallucination, knowledge boundary, and efficiency.

These are worth pausing on because they show that the paper is not naively celebratory.

**Role-playing capability** matters because many agent systems depend on prompt-defined roles, yet role prompts do not guarantee domain fidelity or psychological realism.

**Generalized human alignment** is an unusually interesting point. The authors argue that if agents are used for social simulation, then always forcing them into one "ideal" alignment may actually be wrong, because simulation sometimes requires representing bad or conflicting human values honestly.

**Prompt robustness** reflects the fact that an agent is not driven by one prompt but by a whole prompt framework. Small wording changes can destabilize the behavior of the overall system.

**Hallucination** becomes more dangerous in agents than in chat because errors can now drive actions, tool use, code generation, or multi-step plans.

**Knowledge boundary** is subtle and important: if an LLM is supposed to simulate an ordinary person, it may know far more than the simulated person should know. That contaminates realism.

**Efficiency** reminds the reader that agent loops are expensive. Every extra memory read, planner call, critic pass, or tool invocation compounds latency and cost.

What is striking is how many of these challenges remained central even after the first agent boom. The paper aged in its benchmark list and in some of its example set, but it did not age badly in its diagnosis of the hard parts.

---

## **Subtle points, clarifications, and limits**

- This is **not** a canonical AutoGPT paper in the narrow sense. It is a broader survey that happens to be one of the best scholarly ways to understand the AutoGPT-style design pattern.
- The four-module architecture is a **taxonomy**, not a mandatory implementation recipe. Real systems often merge or skip modules.
- Many cited systems are early arXiv papers, demos, or GitHub frameworks. The survey is therefore partly documenting a live research frontier rather than a settled body of validated knowledge.
- The paper sometimes uses "human-like" language more freely than the evidence warrants. LLM agents showed flexible orchestration, not robust human-level autonomy.
- Because the arXiv version was revised after 2023, the accessible version now contains later updates than the original early-boom snapshot. That is useful, but it also means the note sits between a 2023 historical moment and a somewhat later polished survey.

---

## **Closing perspective**

What makes this paper worth keeping in memory is that it gave the early agent-framework era a real intellectual skeleton. It did not prove that AutoGPT-style systems were robust, and it did not settle what an autonomous agent fundamentally is. What it did do was far more useful for learning: it showed how to decompose the field into recurring design decisions, how to separate architecture from capability acquisition, how to distinguish application claims from evaluation evidence, and where the hardest unsolved problems actually were.

That is why this note still matters. If you remember only one thing, remember that the 2023 agent boom was not "LLMs suddenly became autonomous." It was "LLMs became the controller inside engineered loops of role, memory, planning, action, and feedback." This survey is one of the clearest documents for understanding that transition.

---

## **Personal comprehension notes**

The simplest mental model is:

LLM agent = language model + operating loop

The operating loop usually has four questions:

- Who am I supposed to be? -> profile
- What do I know right now and from before? -> memory
- What should I do next? -> planning
- How do I actually do it? -> action

Then there are two extra layers on top of that:

- How does the system get better? -> capability acquisition
- How do we know it is actually good? -> evaluation

That is the core idea of the whole survey.

The most useful memory hook for the AutoGPT era is that the visible autonomy mostly came from **scaffolding**, not from one miraculous prompt. Tool access, memory storage, iterative replanning, critics, and retrieval all made the loop look more agent-like. That is why the same period produced so many framework names at once: people were exploring different ways to wrap a powerful language model in control structure.

Another good way to remember the paper is this contrast:

- **Chat model:** answer this request now.
- **Agent framework:** keep acting until the goal state changes or the task is done.

That shift from single response to controlled loop is the real heart of the note.

Two memory hooks:

- **AutoGPT is the brand name; the survey is the map.**
- **The field's real problem is not generating steps, but controlling error across steps.**

---

## **Compact retention notes**

- **Paper type:** Broad survey of LLM-agent architectures, applications, and evaluation
- **Core idea:** Organize early LLM agents into profiling, memory, planning, and action, then compare how they acquire capability and how they should be evaluated.
- **Main mechanism:** Taxonomic synthesis across modules, feedback loops, applications, and benchmarks rather than a single new algorithm.
- **Key result:** The paper turns the early AutoGPT-style boom from a pile of demos and frameworks into a coherent research design space.
- **Main limitation:** It is descriptive rather than causal, includes many immature early systems, and sometimes overstates how close these agents are to human-like autonomy.

---

## **Citations used in the paper**

- Franklin and Graesser, *Is It an Agent, or Just a Program?: A Taxonomy for Autonomous Agents*, 1997 - gives the classical autonomous-agent definition the survey opens from.
- Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models*, 2023 - central example of planning with environmental feedback.
- Park et al., *Generative Agents: Interactive Simulacra of Human Behavior*, 2023 - major source for memory, reflection, and social-simulation design.
- Shinn et al., *Reflexion: Language Agents with Verbal Reinforcement Learning*, 2024 - key example of model-generated feedback and self-improvement.
- Schick et al., *Toolformer: Language Models Can Teach Themselves to Use Tools*, 2024 - important anchor for tool-use as a model capability.
- Shen et al., *HuggingGPT: Solving AI Tasks with ChatGPT and Its Friends in Hugging Face*, 2024 - important example of orchestrating external models and tools.
- Wang et al., *Voyager: An Open-Ended Embodied Agent with Large Language Models*, 2023 - shows experience accumulation, skill libraries, and embodied long-horizon behavior.
- Liu et al., *AgentBench: Evaluating LLMs as Agents*, 2023 - captures the shift from building agents to benchmarking them systematically.

---
