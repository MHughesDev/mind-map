# Towards a Science of Human-AI Decision Making: A Survey of Empirical Studies

**Paper link:** https://arxiv.org/abs/2112.11471

---

## **Paper metadata**

**Authors / collaborators:**  
- Vivian Lai  
- Chacha Chen  
- Q. Vera Liao  
- Alison Smith-Renner  
- Chenhao Tan

**Organizations / companies / institutions involved:**  
- University of Chicago  
- Microsoft Research  
- University of Colorado Boulder  
- Dataminr

**Publication date:**  
2021

**Venue / source:**  
arXiv (cross-community survey spanning HCI and AI venues)

**Research paper type / category:**  
- Survey / review paper  
- Position / perspective paper  
- Experimental / empirical synthesis paper  
- Interdisciplinary paper

**Primary field / topic area:**  
Human-AI decision making (HCI + ML + sociotechnical evaluation)

**Keywords:**  
- human-AI decision making  
- decision support systems  
- trust and reliance calibration  
- explainable AI (XAI)  
- empirical human-subject studies  
- evaluation design

---

## **Opening perspective**

This paper appears at a moment when AI models were improving quickly, but practical deployment in high-stakes domains still depended on humans making the final call. That creates a basic tension: model quality can improve, while real-world decisions can still degrade because people interact with predictions, confidence signals, explanations, and interfaces in ways that are not automatically aligned with model quality. The paper matters because it reframes the scientific target from "Is the model accurate?" to "Does the human-AI system produce better decisions under realistic constraints?" If you care about responsible AI, decision support, or real deployment in medicine, law, finance, or public services, this is one of the surveys that forces the field to adopt that systems-level lens.

---

## **Full walkthrough and explanation**

**The core reframing: decision science, not model benchmarking**

The survey starts from a practical deployment reality: in many domains, full automation is unsafe, unacceptable, or legally constrained, while fully manual workflows are often noisy, slow, or inconsistent. So the real object of study is a hybrid team. The paper's canonical flow is:

Human task context -> AI output and assistance -> human interpretation -> reliance/override behavior -> final decision -> downstream outcome.

That pipeline is not just illustrative; it carries the paper's thesis. Once this is the unit of analysis, model-level metrics are necessary but insufficient. The same model can help, harm, or do nothing depending on task design, user expertise, interface timing, and evaluation choices. The survey therefore treats human-AI decision making as an empirical science problem with design variables, confounders, and measurement validity concerns.

**How the authors define scope and build the corpus**

A strong feature of the paper is explicit inclusion criteria. The surveyed works must include human-subject evaluation, involve decision tasks, and center decision makers rather than pure model engineering. This excludes many classic AI papers and keeps focus on studies where human behavior is actually measured. They gather papers across major HCI and AI-adjacent venues (especially 2018-2021), then code them through iterative consensus around three design axes:

1. Decision tasks  
2. AI models and assistance elements  
3. Evaluation metrics

This coding strategy is one of the paper's key contributions: it does not only summarize findings, it proposes a way to make findings comparable across a fragmented literature.

**Decision tasks: diversity without shared characterization**

The paper shows wide task diversity across law, medicine, finance, education, leisure, professional, artificial, and generic settings. The useful move is that domain labels alone are treated as weak abstractions for generalization. Instead, the survey argues that studies should characterize tasks along deeper dimensions:

- risk/stakes,  
- required expertise,  
- subjectivity of judgment,  
- and AI-for-emulation vs AI-for-discovery.

That last distinction is especially important. In emulation tasks, AI mimics judgments humans already perform well. In discovery tasks, AI seeks patterns in outcomes grounded in external processes (social/biological dynamics) where humans may be weaker or biased. This distinction changes what "good assistance" means and whether results transfer across tasks.

The paper also flags a structural problem: task choice is often dataset-driven, not question-driven. For example, overuse of recidivism benchmarks may reflect data availability more than scientific priority. This can create a false sense of maturity while leaving major applied contexts under-studied.

**AI assistance elements: from "show prediction" to full design space**

A second major contribution is a taxonomy of assistance elements. The paper separates:

- model predictions,  
- information about predictions (uncertainty, local explanations, counterfactuals, examples),  
- information about models/data (global performance, documentation, training-data context),  
- and workflow/agency elements (timing, user control, feedback loops, machine agency levels).

This is a strong corrective to explanation-centric thinking. The field had often acted as if "better explanation" was the main lever. The survey shows that assistance quality is broader: ordering of interaction, opportunity for user input, and control over model behavior can matter as much as explanation form.

Pipeline examples from the paper's framing:

- Baseline support: Input case -> model prediction -> human accept/reject -> final decision  
- Explanation-enhanced support: Input case -> prediction + uncertainty/explanation -> human mental model update -> calibrated reliance -> final decision  
- Agency-aware support: Human pre-judgment -> model suggestion -> editable controls/feedback -> revised decision

The paper also documents model diversity in studies: deep models, shallow models, and many Wizard-of-Oz simulations. A subtle but important caution appears here: WoZ can help isolate variables, but unrealistic simulation of model behavior can weaken ecological validity and distort conclusions.

**Evaluation metrics: what is measured shapes what is learned**

The third pillar is evaluation design. The survey distinguishes evaluation with respect to:

- task outcomes (efficacy, efficiency, demand/satisfaction), and  
- AI-focused constructs (understanding, trust/reliance, fairness, usability).

Each can be objective or subjective. The paper repeatedly warns that these are not interchangeable. For example:

- self-reported understanding can diverge from objective forward simulation ability,  
- trust attitude differs from reliance behavior,  
- and reliance can be influenced by factors beyond trust (time pressure, workload, self-confidence, incentives).

This is where the paper is strongest methodologically. It asks researchers to improve construct validity and content validity rather than mixing metrics casually. It also highlights reproducibility barriers: many studies use home-grown survey items and do not publish instruments, making cross-study synthesis weaker than it should be.

**Main empirical pattern the paper surfaces**

Across all three axes, the paper converges on one broad finding: the field had many isolated studies but limited cumulative science. Results vary because tasks, assistance designs, participants, and metrics vary in ways that are often under-specified. The paper is not claiming there are no robust effects; it is claiming that robust effects are hard to identify without shared frameworks and better reporting discipline.

**Where the paper is right, incomplete, or historically bounded**

The paper is right to reject a model-only framing and to insist on alignment between research question, task properties, assistance design, and metric choices. It is also right that explanation-centric work alone cannot solve decision support.

A limitation, acknowledged implicitly, is that the synthesis heavily reflects 2018-2021 work and therefore underrepresents later developments in foundation models, conversational interfaces, and interactive copilots. Another bounded assumption is that many evaluated tasks are trial-like and short horizon; real deployments involve organizational incentives, accountability structures, and longitudinal adaptation effects that are harder to study in controlled experiments.

Still, these are less failures than historical boundaries. The paper's framework remains useful precisely because it can absorb newer modalities and longer-term workflows.

---

## **Subtle points, clarifications, and limits**

One easy misread is to treat this as a ranking paper for explanation methods. It is not. It is a design-and-methodology paper that asks what kinds of assistance should exist, for whom, in which task conditions, and measured how. Another subtle point is that "better calibration" does not mean "less reliance"; it means reliance shifts toward conditions where model help is actually warranted. Finally, while the paper calls for common frameworks, it does not deliver a complete theory of transfer across domains; it gives a principled scaffold and concrete recommendations, not a closed-form science.

---

## **Closing perspective**

This paper earned durable respect as an agenda-setting bridge between HCI and AI because it changed the default question from component quality to joint performance under human constraints. It helped legitimize the view that decision support quality is co-produced by models, interfaces, workflows, users, and institutions. In terms of standing, it is widely treated as a serious synthesis in human-centered AI and explainable-AI-adjacent communities, especially among researchers working on trust calibration, evaluation methodology, and sociotechnical deployment. It is worth studying not because it "settles" the field, but because it gives a rigorous way to do better work next.

---

## **Personal comprehension notes**

The best mental model for this paper is: **it is a map of experimental levers and measurement traps**.  
If you only optimize model AUC, you are optimizing one component inside a longer behavioral system. The final decision outcome depends on whether the human interpreted assistance correctly, whether the workflow forced reflective thinking or encouraged lazy acceptance, and whether your metric actually measured what you claim.

Another memory anchor: **task characteristics are hidden moderators**. If risk, expertise, and subjectivity differ, you should expect effect sizes and even effect directions to move. That is why two papers about "explanations" can disagree without either being wrong.

And one more: **trust is not reliance**. Trust is an attitude; reliance is behavior under constraints. Treating them as identical leads to false conclusions and bad design decisions.

---

## **Compact retention notes**

- **Paper type:** Survey + research agenda paper (empirical literature synthesis)  
- **Core idea:** Evaluate human-AI decision making as a joint system, not model-in-isolation.  
- **Main mechanism:** Organize the field by task design, assistance-element design, and metric design.  
- **Key result:** Existing studies are fragmented; stronger common frameworks and measurement practices are needed for cumulative science.  
- **Main limitation:** Corpus and conclusions are historically bounded (mostly pre-2022 paradigms and short-horizon study setups).

---

## **Citations used in the paper**

- Lai, Chen, Liao, Smith-Renner, Tan, *Towards a Science of Human-AI Decision Making: A Survey of Empirical Studies*, 2021  
- Kulesza et al., *Too Much, Too Little, or Just Right? Ways Explanations Impact End Users' Mental Models*, 2013  
- Yin, Vaughan, Wallach, *Understanding the Effect of Accuracy on Trust in Machine Learning Models*, CHI 2019  
- Zhang, Liao, Bellamy, *Effect of Confidence and Explanation on Accuracy and Trust Calibration in AI-Assisted Decision Making*, 2020  
- Wang and Yin, *Are Explanations Helpful? A Comparative Study of the Effects of Explanations in AI-Assisted Decision-Making*, IUI 2021  
- Buçinca, Malaya, Gajos, *To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI*, 2021  
- Green and Chen, *The Principles and Limits of Algorithm-in-the-Loop Decision Making*, CSCW 2019  
- Sperrle et al., *A Survey of Human-Centered Evaluations in Human-Centered Machine Learning*, 2021  
- Lee and See, *Trust in Automation: Designing for Appropriate Reliance*, 2004  
- Mitchell et al., *Model Cards for Model Reporting*, FAT* 2019

---
