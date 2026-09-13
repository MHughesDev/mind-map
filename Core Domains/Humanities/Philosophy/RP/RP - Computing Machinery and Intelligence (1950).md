# Computing Machinery and Intelligence

**Paper link:** https://doi.org/10.1093/mind/LIX.236.433

---

## **Paper metadata**

**Authors / collaborators:**  
- Alan M. Turing

**Organizations / companies / institutions involved:**  
- University of Manchester

**Publication date:**  
October 1950

**Venue / source:**  
Mind, Vol. LIX, Issue 236

**Research paper type / category:**  
- Foundational / landmark paper
- Theoretical paper
- Position / perspective paper
- Interdisciplinary paper

**Primary field / topic area:**  
Philosophy of artificial intelligence, philosophy of mind, and theory of computation

**Keywords:**  
- imitation game
- digital computer
- machine intelligence
- learning machine
- philosophy of mind

---

## **Opening perspective**

This paper became famous for the question it refuses to handle in the usual way. Turing begins with "Can machines think?" and then immediately notices that the argument is likely to collapse into a dispute over the meanings of "machine" and "think." Instead of pretending those words can be cleaned up once and for all, he performs a much more important move: he replaces the original question with one that can actually be examined. That replacement is the imitation game, and the real achievement of the paper is not just that it proposes a test, but that it shows how to convert a philosophical deadlock into a researchable problem.

That is why the paper still matters. It sits at the intersection of philosophy, logic, early computing, psychology, and what later became AI. It is not an experiment paper and not a mathematical proof in the narrow sense. It is a disciplined argument about what counts as evidence for intelligence, what kinds of objections deserve to be taken seriously, and what kind of machine one would actually have to build if one wanted machine intelligence to become more than speculation.

---

## **Full walkthrough and explanation**

**Replacing a vague question with an operational one**

Turing opens by saying that if we try to answer "Can machines think?" by defining the words in their ordinary sense, we end up in something close to a sociological survey of language usage, which he treats as absurd. That opening matters because it shows his strategy from the beginning: he is not merely offering a new example or a clever metaphor, he is changing the form of the problem. The paper should therefore be read as a methodological intervention before it is read as a prediction about future computers.

Vague question about thinking -> replace slippery terms with a game -> compare hidden performances through text -> ask whether the machine can do as well as a human

The imitation game itself begins as a three-person party game involving a man, a woman, and an interrogator who has to decide which is which through written exchange alone. Turing then modifies the setup by asking what happens when a machine takes the deceptive role. The key issue becomes whether the interrogator will make the wrong identification as often in the machine case as in the original human case. This is already more precise than "Can machines think?" because it turns the issue into observable conversational performance under controlled conditions.

The text-only structure is not incidental. Turing deliberately strips away voice, appearance, physical strength, and bodily resemblance so that the evaluation tracks intellectual performance rather than theatrical resemblance. He even notes that there is no point in penalizing a machine for losing a beauty contest or a footrace. That is one of the strongest parts of the paper: he separates the question of human likeness from the question of intelligence. If the issue is intelligence, then the test should isolate the relevant capacities rather than smuggling in irrelevant ones.

It is also important that Turing does not say conversation exhausts the whole of mind. His narrower claim is that if a machine can sustain human-level conversational performance under interrogation, then many of the standard anti-machine objections lose much of their force. This is a criterion of evidence, not a complete metaphysics of thought.

**Why Turing narrows the problem to digital computers**

Once the new question is in place, Turing asks what kind of machine the paper is even talking about. He briefly considers broader possibilities but rejects the idea that every conceivable engineering method needs to count. A biologically constructed human duplicate would not be interesting here, even if artificially produced, because it would evade rather than clarify the issue. So he restricts the discussion to digital computers, the class of machines that had already become central to contemporary discussions of "thinking machinery."

To make that restriction intelligible, he gives a compact explanation of how digital computers work by comparing them to a human computer following rules. A human computer, in the old sense, performs calculations by following explicit procedures. The digital computer mechanizes that kind of rule-following. Turing breaks it into three main parts: the **store**, which holds information; the **executive unit**, which performs operations; and the **control**, which ensures that the instructions are carried out in the right order. This is one of the places where the paper quietly links philosophy to computer architecture.

Question or input -> control reads instruction table -> executive unit performs operations -> store is updated -> typed reply is produced

Turing also explains the importance of conditional instructions and repetition. A machine is not just a passive calculator executing one straight list of steps. It can branch, loop, and continue until some condition is met. That detail matters because it gives the machine something more like flexible procedure rather than mere linear arithmetic. He also mentions digital computers with a random element, which matters later when he discusses learning and search.

Another subtle move appears here: Turing says the paper is not asking whether every existing digital computer could already do well in the game, nor whether all digital computers would do well. The real question is whether there are imaginable digital computers that could do so. That protects the argument from trivial dismissal based on the weakness of contemporary hardware.

**Discrete-state machines and the universality argument**

The next major conceptual step is the move to discrete-state machines and universality. Turing notes that digital computers belong to a class of systems whose states change in distinct steps rather than continuously. He then argues that a sufficiently capable digital computer can mimic the behavior of any other discrete-state machine, provided it has enough storage, enough speed, and the right program. This is the universality claim, and it is one of the deepest parts of the paper.

Any discrete-state machine -> describable transitions -> simulable by a universal digital computer -> imitation game can be played by the simulator as well

This changes the stakes of the entire debate. If some machine architecture could in principle display the relevant intelligent behavior, then one does not need a special mystical material in order to achieve it. One sufficiently general digital computer could be adapted to do the job. Turing eventually compresses the issue into a very concrete question: fix a particular digital computer `C`; if we enlarge its storage, improve its speed, and provide a suitable program, can it play the imitation game satisfactorily? That formulation is important because it pushes the conversation away from essence and toward capability.

The discussion of discrete-state machinery also prepares Turing's response to later objections. If intelligence-relevant behavior can be generated by state transitions that are sufficiently rich and sufficiently well organized, then appeals to superficial differences in substance or medium become much less decisive.

**Turing states his wager plainly**

Before turning to the objections, Turing gives his own view with unusual directness. He predicts that in about fifty years it will be possible to program computers with a storage capacity of about `10^9` to play the imitation game so well that an average interrogator will have no more than a 70 percent chance of making the right identification after five minutes of questioning. He also says that by the end of the century the phrase "machines think" will be used without provoking contradiction.

This is not presented as a proved theorem. Turing is explicit that it is a conjecture. But he insists that conjectures matter because they guide research. That too is part of the paper's style: it is not pretending that hard proof is available where only disciplined foresight is possible.

**The objections are the real argumentative center of the paper**

Many people remember the paper only for the imitation game, but most of its substance is actually in the long sequence of replies to opposing views. Turing's list is worth retaining because later debates in AI keep rediscovering the same structure:

- The theological objection
- The "heads in the sand" objection
- The mathematical objection
- The argument from consciousness
- Arguments from various disabilities
- Lady Lovelace's objection
- The argument from continuity in the nervous system
- The argument from informality of behavior
- The argument from extra-sensory perception

### **Objections grounded in dignity, soul, or inward certainty**

The theological objection claims that thinking depends on an immortal soul granted to human beings but not to machines. Turing does not try to defeat this by irreligion. Instead, he replies on the objection's own terms and points out that such a view places a curious restriction on divine omnipotence. If one allows that God could confer a soul where He wished, then the objection stops being decisive. Turing is not trying to prove that machines have souls; he is showing that this line of argument does not settle the matter.

The "heads in the sand" objection is psychologically revealing rather than analytically powerful. It says, in effect, that the consequences of machines thinking would be too dreadful, so we had better hope they cannot. Turing treats this as an expression of fear, not a real argument. That remains relevant today because many disputes about AI are still partly arguments about human status disguised as arguments about logic.

The argument from consciousness is more serious. Turing quotes Geoffrey Jefferson's demand that a machine would need not only to produce a sonnet or concerto, but to do so from felt thought and emotion, knowing that it had done so. Turing's reply is subtle. If one insists that the only way to know a being thinks is to be that being, then one collapses into a kind of solipsism. In practice, human life works by a more modest convention: we infer mentality from sustained, meaningful behavior. Turing then strengthens the point by giving a viva voce style exchange in which a machine capable of answering follow-up questions about poetry would look much less like a hollow trick. His aim is not to eliminate the mystery of consciousness, but to deny that the mystery blocks all judgment about intelligence.

### **Objections grounded in logic, mechanism, and physical form**

The mathematical objection draws on limits discovered by Godel, Church, Kleene, Rosser, and Turing himself. The claim is that machines, as formal systems, will run into questions they cannot answer, whereas human minds somehow transcend those limits. Turing's reply is carefully restrained. He grants that any particular machine has limits. What he denies is that anyone has shown humans to be free of comparable limits. More importantly, even if one machine fails on some question, it does not follow that every possible machine fails in exactly the same way, nor that human superiority has been established in any broad sense. The argument gives people a feeling of superiority over a given machine, but not over machinery as such.

The objection from continuity in the nervous system says that brains are not discrete-state systems, so digital computers cannot genuinely mimic them. Turing's response is that the imitation game does not require exact internal identity. It requires behavior that cannot be discriminated in the test situation. He uses the example of a continuous machine such as a differential analyzer and notes that a digital computer could still produce appropriately similar answers. The point is crucial: exact material duplication is not necessary for functional indistinguishability.

The objection from informality of behavior argues that no finite set of rules can specify what a human being should do in every imaginable circumstance. Turing agrees with the first half and rejects the conclusion. He distinguishes **rules of conduct** from **laws of behavior**. Human beings may not carry explicit rulebooks for every case, but it does not follow that their behavior is lawless or unmechanizable. This distinction is easy to miss and extremely important. Turing is saying that "not consciously following a complete rule list" does not imply "not being a machine."

### **Objections grounded in familiar stereotypes about machines**

The "various disabilities" objection comes in the familiar form: a machine will never do X. Turing lists a whole cluster of such claims, including being kind, resourceful, beautiful, friendly, humorous, morally aware, in love, self-reflective, diverse in behavior, or capable of genuinely new action. His response is that these assertions are usually unsupported extrapolations from the very limited machines people already know. They are products of shallow induction from weak examples.

Several important clarifications appear inside this section. One is Turing's distinction between **errors of functioning** and **errors of conclusion**. An abstract machine, considered as an idealized mechanism, may not malfunction. But that does not mean it cannot produce false or misguided outputs once its symbols are given meaning. So the claim that "machines cannot make mistakes" depends on confusing physical malfunction with wrong inference or false belief-like output. Another is his remark that a machine can, in a real sense, be the subject matter of its own operations: it can help revise its own programs or predict the consequences of changes to itself.

Lady Lovelace's objection is one of the most famous. Her claim about the Analytical Engine is that it has no pretensions to originate anything and can only do what we know how to order it to perform. Turing partly agrees and partly dissolves the force of the objection. A machine may be built by us, programmed by us, and still produce results that surprise us. He rejects the popular variant that a machine can never do anything really new, and he spends time on the closely related claim that machines cannot surprise us. His answer is almost disarmingly practical: machines surprise him frequently, often because the consequences of a setup outrun what he bothered to calculate in advance. The real issue is not whether causes exist, but whether the resulting behavior can exceed our immediate foresight.

### **The strange but revealing ESP section**

The final objection is about extra-sensory perception, especially telepathy. To modern readers this section feels bizarre, but it is historically revealing. Turing treats ESP more seriously than most contemporary readers would, largely because some statistical evidence at the time seemed persuasive to him. The point for the paper is not that telepathy is central to intelligence. The point is that if telepathic leakage were real, it could contaminate the imitation game, so the test conditions would need to be tightened, for example by using a "telepathy-proof room." Even this odd section reinforces the paper's general style: if a test is vulnerable to confounders, refine the test rather than abandon the inquiry.

**The paper's positive program: learning machines**

After dismantling the objections, Turing turns to the most forward-looking part of the paper. He admits that he has no decisive positive proof and even describes some of his suggestive analogies as "recitations tending to produce belief." That phrase matters because it shows intellectual honesty. He knows the positive case is still partly visionary. But the vision is concrete enough to become a research agenda.

One analogy compares minds to atomic piles. Some are "sub-critical": an injected idea causes only a small disturbance that dies away. Others are "super-critical": one idea generates a whole expanding structure of related ideas. Turing asks whether a machine could be made super-critical in the same sense. Another analogy is the "skin of an onion." We strip away one apparently mechanical layer of mind, then another, and keep insisting the real mind must lie deeper. Turing asks whether this process ever reaches some nonmechanical core or whether, after enough stripping, the entire thing proves to be mechanical after all. These are not proofs, but they show the direction of his thinking.

The paper then shifts from argument to engineering. Turing says the real problem is largely one of programming. Instead of trying to simulate a finished adult mind directly, he suggests building a child-machine and educating it. This is one of the most prophetic moments in the paper because it reframes intelligence as something to be developed through training rather than hard-coded in mature form from the outset.

Child-programme -> education -> other experience -> revised behavior -> further selection and improvement -> adult-like competence in the imitation game

This proposal has several layers. First, Turing divides mental development into three components: the initial state at birth, formal education, and other experience. Second, he suggests that the child mind is comparatively simple, something like a notebook with little mechanism and many blank pages, which makes it more plausible as an object of programming. Third, he says the process should be iterative: build a child-machine, teach it, evaluate how well it learns, revise the design, and try again. He explicitly compares this to evolution:

- Structure of the child machine = hereditary material
- Changes of the child machine = mutations
- Judgment of the experimenter = natural selection

That comparison is not ornamental. It tells you how Turing imagines the search space of intelligence. We do not simply derive the adult mind from first principles. We search, vary, test, retain, and improve.

He also discusses the mechanics of teaching. Reward and punishment can shape behavior, but they are too low-bandwidth to support rich education on their own. Turing makes this vivid by joking that a child forced to learn a text purely through reward and punishment would become very sore indeed. So the machine also needs "unemotional" channels of communication through which instruction can be transmitted more directly. This is an early recognition that intelligence training needs both evaluation signals and informative content.

Turing then considers how much innate structure the child-machine should have. One possibility is to make it as simple as possible. Another is to build in a logical inference system containing definitions, propositions with different statuses, and imperatives that trigger action once sufficiently established. His examples here are wonderfully concrete. A teacher's command such as "Do your homework now" might eventually become an imperative inside the machine once supported by other accepted propositions, such as the fact that the teacher's statements are to be treated as true. This is not modern machine learning language, but it is unmistakably an attempt to think about representation, belief status, instruction, and action selection in one system.

Two further ideas make this section feel strikingly modern. One is that the teacher of a learning machine will often be quite ignorant of what is happening internally, even while still being able to judge the machine's outward behavior. Turing contrasts this with ordinary computation, where one wants a clear picture of the machine state at each moment. The other is that randomness may be useful in learning because search over many possible satisfactory behaviors can be more efficient with random exploration than with rigidly systematic trial. Both ideas point toward later work in machine learning, reinforcement learning, and search.

The paper closes this section by asking what intellectual domains machines should attempt first. Turing suggests abstract tasks like chess, but he also considers the alternative of giving machines the best sense organs available and teaching them language the way one teaches a child. He declines to choose decisively between the paths and says both should be tried. That final openness is characteristic of the whole paper. It is bold in direction, but not dogmatic in implementation.

The overall structure of the paper is therefore much richer than the slogan "Turing Test." It goes: replace a bad question, define a workable test, restrict attention to digital computers, defend the possibility in terms of universality, answer objections one by one, and then propose learning as the practical route to success. Once seen that way, the paper is not just a benchmark proposal. It is a conceptual blueprint for AI.

---

## **Subtle points, clarifications, and limits**

- The paper does **not** claim that passing the imitation game proves consciousness. Turing's point is about what counts as public evidence for intelligence, not about solving the hard problem of subjective experience.
- The paper is **not** merely about deception or cheap trickery. The interrogator can ask sustained, adaptive follow-up questions, so success requires flexible competence rather than a single canned stunt.
- The imitation game is only the beginning of the paper. The later discussion of learning machines is essential, because it shows that Turing's real interest is how intelligence might be built, not just how it might be tested.
- Turing's responses often weaken objections rather than annihilate them. That is part of the paper's strength. He is usually shifting the burden of proof, exposing confusions, and showing that many impossibility claims were never well-founded.
- The ESP discussion should be read as a historical artifact and as an example of test design under confounding conditions, not as a core foundation of the paper's argument for machine intelligence.

---

## **Closing perspective**

What this paper changed was not just a vocabulary word or a famous test. It changed the standard for how claims about machine intelligence should be argued. Instead of demanding a final definition of thought before any inquiry can begin, Turing shows how to work with observable performance, conceptual clarity, and progressive refinement of the question itself. That is why the paper still matters. Even now, whenever AI debate gets stuck between grand metaphysics and shallow demo culture, Turing's method remains a model for how to make the conversation sharper without making it smaller.

---

## **Personal comprehension notes**

The easiest way to think about this paper is that Turing is not trying to solve the mystery of mind in one stroke. He is changing the rules of evidence. He notices that people can hide behind vague language forever, so he asks for a setting in which intelligence would have to show up in publicly assessable behavior.

The imitation game is best remembered as a courtroom standard, not as a full theory of mind. The question becomes: what evidence would be enough to stop dismissing the machine? Once framed that way, many anti-machine arguments begin to look weaker than they sound.

The child-machine idea is the other half of the paper. The way to remember it is:

- Do not hand-code a finished adult mind.
- Build something trainable.
- Educate it.
- Revise the design based on how it learns.

That makes the paper feel much closer to modern machine learning than people often realize.

Two memory hooks help:

- **Bad question -> better test:** Turing's deepest move is replacing an unproductive question with an operational one.
- **Test -> learning program:** the paper starts with evaluation but ends with training, adaptation, and search.

---

## **Compact retention notes**

- **Paper type:** Foundational theoretical position paper
- **Core idea:** Replace "Can machines think?" with an operational imitation game based on conversational performance.
- **Main mechanism:** Hidden text-based interrogation plus a universality argument for programmable digital computers and a learning-machine research program.
- **Key result:** The paper reframes machine intelligence as a tractable question of observable behavior and programmable learning rather than metaphysical essence.
- **Main limitation:** It does not prove consciousness, embodiment, or full human cognition; it mainly offers a criterion of evidence and a research direction.

---

## **Citations used in the paper**

- Countess of Lovelace, *Translator's notes to an article on Babbage's Analytical Engine*, 1842 - source of the originality objection that Turing answers directly.
- G. Jefferson, *The Mind of Mechanical Man*, 1949 - source of the consciousness objection and the demand that machines must genuinely feel.
- K. Godel, *Uber formal unentscheidbare Satze der Principia Mathematica und verwandter Systeme, I*, 1931 - central background for the mathematical limitation objection.
- Alonzo Church, *An Unsolvable Problem of Elementary Number Theory*, 1936 - part of the logical and computability background behind claims about machine limits.
- S. C. Kleene, *General Recursive Functions of Natural Numbers*, 1935 - another foundational result in the family of formal limitations Turing discusses.
- D. R. Hartree, *Calculating Instruments and Machines*, 1949 - cited in connection with Lovelace's objection and the possibility of machines that learn.
- A. M. Turing, *On Computable Numbers, with an Application to the Entscheidungsproblem*, 1937 - the deeper theoretical background for universality and digital simulation.
- Samuel Butler, *Erewhon*, 1865 - an early literary treatment of machine-related speculation that sits in the paper's broader cultural background.

---
