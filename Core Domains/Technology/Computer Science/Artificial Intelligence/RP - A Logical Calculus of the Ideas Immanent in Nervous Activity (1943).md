# A Logical Calculus of the Ideas Immanent in Nervous Activity

**Paper link:** https://doi.org/10.1007/BF02478259

---

## **Paper metadata**

**Authors / collaborators:**  
- Warren S. McCulloch
- Walter Pitts

**Organizations / companies / institutions involved:**  
- Department of Psychiatry, Illinois Neuropsychiatric Institute, College of Medicine, University of Illinois
- The University of Chicago

**Publication date:**  
December 1943

**Venue / source:**  
The Bulletin of Mathematical Biophysics, Vol. 5, No. 4

**Research paper type / category:**  
- Foundational / landmark paper
- Theoretical paper
- Interdisciplinary paper

**Primary field / topic area:**  
Computational neuroscience, mathematical logic, and the early theory of computation

**Keywords:**  
- McCulloch-Pitts neuron
- nervous nets
- threshold logic
- temporal propositional expressions
- recurrent circuits

---

## **Opening perspective**

This paper is one of the earliest places where the brain is treated not just as tissue but as something that can be described with logic. McCulloch and Pitts begin from a deliberately simplified picture of neurons: they either fire or do not fire, synapses can excite or inhibit, delays matter, and enough concurrent excitation can trigger an impulse. From those assumptions they make a bold claim: because nervous activity is "all-or-none," the activity of neurons can be represented propositionally, and whole nervous nets can be analyzed as logical structures.

That is why the paper matters far beyond its biological realism. It is not a learning paper, not an experiment paper, and not a modern neural-network architecture paper. It is a foundational attempt to show that neural activity, logic, memory, and computation can be brought into one formal framework. In one stroke it helps create the formal neuron, gives a constructive account of logic gates built from neurons, and points toward the idea that recurrent nets can embody memory and general computation.

---

## **Full walkthrough and explanation**

**Starting from neurophysiology, but choosing assumptions for calculability**

The paper opens with a long neurophysiological preface, and that beginning matters. McCulloch and Pitts are not saying that real neurons are nothing but logic switches. They start from what they call the cardinal assumptions of theoretical neurophysiology: neurons have somata and axons, synapses connect axons to somata, neurons have thresholds, impulses propagate, synaptic delay is significant, excitation can sum, and inhibition can block or prevent activity. They review latent addition, refractoriness, inhibition, and the fact that what matters about an impulse is mainly its time and place rather than some richer intrinsic code.

At the same time, they make a methodological decision that shapes the whole paper: when several physiological descriptions are possible, they choose the one most convenient for the calculus, provided that alternative descriptions are equivalent in behavior. They say explicitly that the formal equivalence is not itself a factual explanation of facilitation, extinction, or learning. The point is narrower and more powerful. If very different physiological stories produce the same network behavior, then the logical analysis can track what is invariant across those stories.

Afferent activity -> synaptic interaction and delay -> threshold and inhibition test -> neuron either fires or does not fire

This is the first big idea of the paper. The nervous system is being abstracted to a network whose behavior is preserved at the level of logical relations even if some biological implementation details vary.

**Turning neuron activity into propositions**

The decisive move comes next. Because nervous activity is all-or-none, the firing of a neuron can be represented by a proposition. If neuron `c_i` fires at time `t`, measured in synaptic delays from an origin, that event is written as `N_i(t)`. The paper then distinguishes **peripheral afferents**, which receive no synapses from other neurons in the net, from the rest of the network. The central formal problem becomes:

- Given a net, what logical sentences describe its behavior?
- Given a logical sentence, can one build a net that realizes it?

The authors call a set of such descriptive sentences a **solution** of the net. A predicate is **realizable** when there exists some nervous net whose behavior makes the predicate true. They also distinguish realizability in a narrow sense from realizability in an extended sense. The extended sense allows timing shifts or replacement by equivalent nets under different neurophysiological assumptions. That distinction is easy to miss, but it is crucial. They care less about exact micro-timing than about what network behavior survives across equivalent implementations.

They also introduce the idea of a **cyclic** net and define the **order** of a net in terms of how many neurons have to be removed to eliminate circles. Nets of order zero, meaning nets without circles, are the simple case. Those are treated first.

**Nets without circles: the logic of feedforward structure**

For the calculus itself, the paper fixes five assumptions:

1. The structure of the net does not change with time.
2. Inhibitory synapses absolutely prevent excitation at that time.
3. The only significant delay is synaptic delay.
4. A fixed number of excited synapses within the period of latent addition is required to fire a neuron.
5. Neuronal activity is all-or-none.

With these assumptions, the action of a neuron can be written as a logical condition on earlier activity. In ordinary language, a neuron fires now if no inhibitory neuron aimed at it fired at the previous relevant moment and if enough of the appropriate excitatory neurons did fire. The exact formula in the paper is written in Carnap-style notation, but conceptually it is a delayed threshold rule with inhibition. This is the origin of the idealized threshold neuron later associated with their names.

To express such nets, McCulloch and Pitts define **temporal propositional expressions** or TPEs. These are built recursively from predicates of time, the predecessor or delay operator `S`, and propositional operations such as disjunction, conjunction, and conjoined negation. The crucial fact is that these operations are exactly the ones needed to describe what order-zero nets do.

Peripheral afferents over time -> apply delays with `S` -> compose with OR, AND, and AND-NOT -> realize internal neuron activity -> realize the whole acyclic net

This leads to the paper's first pair of central theorems. **Theorem I** says every net of order zero can be solved in terms of temporal propositional expressions. Because the net has no circles, one can recursively replace each internal neuron's firing condition by the TPE that defines it until everything is expressed solely in terms of peripheral afferents. **Theorem II** proves the converse: every TPE can be realized by a net of order zero. The figures in the paper construct the primitive components for one-step delay, disjunction, conjunction, and conjoined negation, and then larger nets can be built compositionally from these pieces.

That constructive aspect matters a lot. The paper is not only saying that nervous nets can be *described* by logic. It is also saying that logic can be *implemented* by nervous nets. Description and construction go both ways.

**What kinds of formulas can these acyclic nets realize?**

Theorem III sharpens the picture by asking which ordinary propositional formulas count as TPEs. The answer is more specific than "all formulas." In effect, the formulas realized by order-zero nets are those that can still be false when all their elementary constituents are false. The paper gives equivalent characterizations in terms of the truth table and Hilbert disjunctive normal form. Intuitively, a net without circles and without spontaneous activity cannot generate truth out of total inactivity. So although it handles conjunction, disjunction, delay, and a constrained form of negation, it does not realize arbitrary negation in the unrestricted modern sense.

This is one of the most subtle points in the paper. The model is logically rich, but its richness is shaped by the physiology-inspired constraints. It is not "Boolean logic in general" dropped into neurons without remainder. It is a specific temporal logic matched to a specific firing model.

**A worked example: the heat sensation caused by transient cooling**

The authors then give a concrete example involving cutaneous sensation. Let `N1` be the action of a heat receptor, `N2` the action of a cold receptor, and let `N3` and `N4` correspond to neurons whose firing implies sensations of heat and cold. They propose conditions of the form:

- `N3(t) = N1(t-1) OR [N2(t-3) AND NOT N2(t-2)]`
- `N4(t) = N2(t-2) AND N2(t-1)`

The point is not just to display a toy circuit. The example shows how structural properties of the net mediate perception. The same external stimulation does not map transparently into sensation. A transient cold stimulus can produce a heat sensation because of the temporal organization of the intervening net. This is one of the first places in the paper where the logic machinery is turned back toward a psychological phenomenon.

**Equivalence theorems: changing physiology without changing logical power**

After the basic feedforward theory, the paper proves a sequence of equivalence theorems. These are among the deepest conceptual parts of the paper because they separate the abstract behavior of a net from particular physiological assumptions.

**Theorem IV** says relative inhibition and absolute inhibition are equivalent in the extended sense. Under relative inhibition, inhibitory input raises the threshold instead of absolutely blocking excitation. McCulloch and Pitts show that the same behavior can be recovered by a different net under the absolute-inhibition assumption.

**Theorem V** says extinction is equivalent to absolute inhibition. Extinction here means that after firing, a neuron's threshold changes for some finite period. They show that this effect can be reproduced by circuits feeding back inhibitory influence with appropriate delays.

**Theorem VI** says facilitation and temporal summation can be replaced by spatial summation. In practical terms, if one wants temporally separated impulses to add up, one can reproduce that effect by inserting chains of delaying neurons so that the inputs arrive together spatially at the target neuron.

**Theorem VII** says alterable synapses can be replaced by circles. This is especially important. The paper considers a simple learning-like mechanism in which previously ineffective axonal terminations can become effective if co-active with the target neuron's firing. McCulloch and Pitts show that recurrent circuitry can reproduce the same functional effect.

The pattern across these theorems is consistent: different physiological stories can be transformed into equivalent nets that preserve the relevant logical behavior, perhaps with timing differences. This is an early and very strong statement of what later philosophy would call multiple realizability. The logical role of a component matters more, for the purposes of the calculus, than the exact physical story used to realize it.

**Nets with circles: memory and indefinite reference to the past**

The second half of the paper is harder and more ambitious. Once circles are allowed, activity can reverberate indefinitely. A neuron in a recurrent circuit may fire now because of an event that happened an arbitrarily long time ago. That means the simple TPE account for order-zero nets is no longer enough.

The authors handle this by identifying a **cyclic set** of neurons whose removal would leave the net without circles. Every noncyclic neuron's activity can still be expressed as a TPE in terms of the cyclic set and the peripheral afferents. The real difficulty is to characterize the cyclic set itself. To do this, the paper introduces more elaborate formulas that quantify over possible histories and possible state assignments to the cyclic neurons.

The notational burden becomes heavy here, but the conceptual point is clear. A recurrent net is not merely computing a formula of the current inputs plus a bounded window of delays. It can embody a state that carries forward information about the indefinite past.

Present afferents + current cyclic state -> recurrent update -> possible reverberation over time -> future activity depends on remote past

**Theorem VIII** states that these richer expressions, together with TPEs for the noncyclic neurons, constitute a solution for nets with circles. The paper then moves to the realizability question in this recurrent setting. It introduces the idea of **prehensible classes** and proves **Theorem IX**, which characterizes when certain classes are realizable in terms of closure properties under logical and temporal operations.

This part is historically important even if it is not the easiest part to learn from directly. The authors are trying to generalize beyond feedforward logic into a theory of memory-bearing recurrent organization. They themselves admit that the treatment is sketchy because of space limitations, and later readers found this section obscure. But the ambition is unmistakable: circles are not an annoying complication added after the fact. They are the mechanism by which the theory reaches beyond momentary reaction and into memory, persistence, and history-sensitive behavior.

**A simpler sufficient condition and the bridge to computability**

Because the full recurrent characterization is difficult to use, the paper offers **Theorem X** as an easier sufficient condition for realizability. It defines a class `K` recursively. Roughly speaking, one starts with TPEs, then allows bounded universal and existential constructions over time and modular predicates like being congruent to `m mod n`. The theorem says every member of this class is realizable.

That move is significant because it shows how recurrent nets can represent patterns like:

- there exists some earlier time with a certain property,
- for all earlier times up to some bound a property holds,
- periodic or cyclical conditions hold.

So the paper is not only about static logical gates. It is about using recurrence and temporal structure to represent memory-like logical universals over past activity.

The closing computability claim is one of the paper's most famous long-range contributions. McCulloch and Pitts say that if a net is furnished with a tape, scanners attached to afferents, and suitable effectors, then it can compute exactly the numbers a Turing machine can compute, and conversely. Nets with circles, even without that full external machinery, can compute some of those numbers, but not all. This is an extraordinary claim for 1943. It places nervous nets directly in relation to the emerging theory of effective computability and suggests a deep alignment between brain-like networks and formal machines.

**The philosophical consequences are not incidental**

The final section, "Consequences," pushes well beyond narrow technical modeling. The authors argue that because a full state description plus net structure determines the future, but not uniquely the whole past or the exact afferent causes, our knowledge is incomplete in space and indefinite in time. They then say that every idea and sensation is realized by activity in the nervous net, and they introduce the language of **psychons**, treating the activity of a single neuron as the smallest relevant psychological event.

From there they make their strongest philosophical extrapolation: because single-neuron activity is propositional and all-or-none, the fundamental relations among psychons are those of two-valued logic. This is not just a side comment. It shows that the paper is simultaneously trying to reshape neurophysiology, psychology, and epistemology. It is one of the earliest explicit attempts to say that mental events may be understood through formal network organization without appealing to a separate nonformal domain.

That ending should be read carefully. It is not a proved reduction of mind to logic in any modern strict sense. It is the authors' philosophical interpretation of what follows if their calculus captures the relevant organization of nervous activity. But it reveals the full scope of the project: not merely to model spikes, but to give a formal bridge from neural events to ideas, memory, purposive behavior, and computation.

---

## **Subtle points, clarifications, and limits**

- This is **not** a modern neural-network training paper. There is no gradient descent, statistical fitting, loss minimization, or benchmark evaluation.
- The original formal neuron is more austere than the usual modern textbook summary. It works with all-or-none firing, synaptic delay, fixed thresholds, excitatory and inhibitory synapses, and temporal structure rather than a generic real-valued weighted-sum story alone.
- The order-zero results do **not** give arbitrary propositional logic. The allowable expressions are constrained by the firing assumptions, especially the fact that total inactivity cannot by itself realize an always-true negated condition.
- The recurrent part of the paper is important but much harder than the gate-construction section. The authors explicitly present it in compressed form, and later readers often found it obscure.
- The claims about psychons, psychology, and the "thing in itself" are philosophical extensions of the formal work. They show the paper's ambition, but they should not be mistaken for narrow mathematical theorems.

---

## **Closing perspective**

What this paper changed was the level at which nervous activity could be discussed. After McCulloch and Pitts, one could say something much sharper than "brains somehow process information." One could ask what logical forms a network realizes, what network realizes a desired logical form, what kinds of memory require circles, and how different physiological mechanisms collapse into equivalent functional organizations. Even though later neuroscience and AI departed from many of the paper's biological assumptions, the core wager endured: networks of simple elements can implement rich computation.

That is why the paper still matters. It is not important because its neuron model is a faithful portrait of the brain. It is important because it is one of the earliest rigorous demonstrations that logic, memory, and computation can be embedded in networked units whose behavior unfolds in time. Much of later AI, automata theory, and computational neuroscience grows out of that possibility.

---

## **Personal comprehension notes**

The easiest way to remember this paper is: each neuron is treated like a tiny yes-or-no statement about whether its adequate conditions are present. Once that move is made, a nervous net becomes a logical machine spread out over time.

The cleanest mental split is:

- **Nets without circles:** basically delayed logical formulas built from input activity.
- **Nets with circles:** formulas are no longer enough by themselves because the net now carries state and can depend on the indefinite past.

The equivalence theorems are the other memory hook. They say that a lot of what looks physiologically different can still be functionally the same at the level of logical behavior. So one deep lesson of the paper is not just "neurons can compute," but "computation can survive across multiple physiological implementations."

Two short ways to retain it:

- **Neuron -> proposition:** firing is treated as truth of a time-indexed proposition.
- **Circle -> memory:** recurrence is what lets the net carry the past forward.

---

## **Compact retention notes**

- **Paper type:** Foundational theoretical paper linking neurophysiology, logic, and computation
- **Core idea:** Because neural activity is all-or-none, nervous nets can be described and constructed using propositional logic extended over time.
- **Main mechanism:** Threshold neurons with excitatory and inhibitory synapses, synaptic delays, feedforward logical constructions, and recurrent circles for memory-like behavior.
- **Key result:** Order-zero nets realize temporal propositional expressions, recurrent nets extend that logical power to history-dependent behavior, and suitably equipped nets align with Turing computability.
- **Main limitation:** The model is highly idealized biologically, the recurrent section is compressed and difficult, and the philosophical conclusions go well beyond what the formal theorems strictly prove.

---

## **Citations used in the paper**

- Rudolf Carnap, *The Logical Syntax of Language*, 1938 - provides the formal language, especially "Language II," in which the calculus is expressed.
- Bertrand Russell and Alfred North Whitehead, *Principia Mathematica*, 1925 - supplies logical notation and background conventions used in the paper's symbolic treatment.
- David Hilbert and Wilhelm Ackermann, *Grundzuge der Theoretischen Logik*, 1927 - part of the logical background behind the theorem machinery and formal treatment of expressions.

---
