# Learning Representations by Back-Propagating Errors

**Paper link:** https://doi.org/10.1038/323533a0

---

## **Paper metadata**

**Authors / collaborators:**  
- David E. Rumelhart
- Geoffrey E. Hinton
- Ronald J. Williams

**Organizations / companies / institutions involved:**  
- Institute for Cognitive Science, University of California, San Diego
- Department of Computer Science, Carnegie Mellon University

**Publication date:**  
9 October 1986

**Venue / source:**  
Nature, Vol. 323, pp. 533-536

**Research paper type / category:**  
- Foundational / landmark paper
- Method / model paper
- Experimental / empirical paper

**Primary field / topic area:**  
Neural network learning, representation learning, and multilayer connectionist models

**Keywords:**  
- back-propagation
- hidden units
- generalized delta rule
- gradient descent
- distributed representations

---

## **Opening perspective**

This paper sits at the point where neural networks stopped being mostly a story about fixed feature detectors and started becoming a story about learned internal structure. Before this work, people already knew how to train simple networks that connected inputs directly to outputs, but the moment a model contained genuinely hidden units, the learning problem became much harder. The target outputs tell you what the network should say, but they do not tell you what the intermediate units should mean. Rumelhart, Hinton, and Williams show how to solve exactly that problem.

That is why the paper matters so much historically. Its deepest contribution is not merely "use calculus on a network." It is the claim that a general-purpose learning rule can force hidden units to invent useful features for a task domain. The paper is also more careful than its later reputation sometimes suggests. It gives a concrete feedforward procedure, derives the relevant gradients, shows how the same idea extends to iterative networks, and then demonstrates that the learned hidden representations are structurally meaningful rather than arbitrary. In that sense it is one of the founding documents of representation learning.

---

## **Full walkthrough and explanation**

**The problem the paper is trying to solve**

The paper begins from the goal of building self-organizing neural networks. A task is specified by giving desired output patterns for input patterns, and the hope is that synaptic modifications will make the network acquire an internal organization suited to that task. For networks with only direct input-to-output connections, learning rules already existed. Those systems can progressively reduce output error by adjusting weights on visible connections. The hard case begins when hidden units are inserted between input and output.

That hidden-layer case is the real conceptual target of the paper. A hidden unit is not directly supervised. The training data never says "this intermediate unit should be active for this case and inactive for that one." The learning procedure therefore has to decide for itself what hidden units should represent. The authors explicitly contrast this with earlier perceptron-style systems that used hand-built feature analyzers. Those intermediate features were not truly learned; their incoming connections were fixed by design. Here the ambition is stronger: let the network discover internal features that make the task solvable.

The overall learning story of the paper is:

Input pattern -> forward computation of hidden and output activations -> compare actual output with desired output -> propagate error derivatives backward -> update all relevant weights -> repeat over many cases

That pipeline sounds standard now, but in 1986 it was the key move that made multilayer learning practically legible.

**The kind of network they study first**

The simplest version of the procedure is presented for layered feedforward networks. The input units sit at the bottom, the output units at the top, and there may be any number of hidden layers in between. Connections are not allowed within a layer or from higher layers down to lower ones, though skip connections that jump over intermediate layers are allowed. Once an input vector is clamped onto the input layer, each higher layer is computed from the one below it, with all units in the same layer updating in parallel and layers themselves being evaluated sequentially from bottom to top.

For a unit `j`, the total input is a weighted sum of lower-layer outputs:

$$
x_j = \sum_i y_i w_{ji}
$$

The paper then gives each unit a nonlinear activation function so that the unit output is:

$$
y_j = \frac{1}{1 + e^{-x_j}}
$$

This is the logistic sigmoid. The choice matters. A hidden layer with purely linear units would collapse into another linear mapping and would not buy expressive power. A hard threshold unit, on the other hand, is not differentiable in the right way for the derivation. The paper therefore works with smooth nonlinear units whose derivatives are bounded. Biases are handled elegantly by imagining an extra input that is always `1`; the weight on that always-on input functions as a learnable bias.

So the forward-pass computation is:

Inputs -> weighted sums + biases -> sigmoid hidden activations -> more weighted sums + biases -> sigmoid outputs

**How the paper defines error**

Once the network produces an output vector, the authors compare it to the desired output vector using a sum-of-squared-errors objective over all training cases:

$$
E = \frac{1}{2} \sum_c \sum_j (y_{j,c} - d_{j,c})^2
$$

Here `c` indexes input-output cases, `j` indexes output units, `y` is the network's actual output, and `d` is the desired output. The task is then to change every weight in the network so that `E` decreases. This is framed as gradient descent in weight space. The paper does not use second-order optimization or anything especially elaborate. Its point is that first-order updates are simple, local, parallelizable, and sufficient to train multilayer systems.

The crucial challenge is that for a weight leading into a hidden unit, the error is not directly observable. The paper's answer is repeated application of the chain rule.

**The core derivation: why errors can be sent backward**

For an output unit, the first easy derivative is:

$$
\frac{\partial E}{\partial y_j} = y_j - d_j
$$

Because the sigmoid output depends on the unit input `x_j`, the paper then uses:

$$
\frac{\partial E}{\partial x_j} = \frac{\partial E}{\partial y_j} \cdot \frac{dy_j}{dx_j}
$$

and since the derivative of the sigmoid is:

$$
\frac{dy_j}{dx_j} = y_j(1-y_j)
$$

the local error term for an output unit becomes proportional to the output mismatch multiplied by the sigmoid slope. Once that quantity is known, the derivative with respect to a weight `w_{ji}` feeding into that unit is:

$$
\frac{\partial E}{\partial w_{ji}} = \frac{\partial E}{\partial x_j} \cdot y_i
$$

This already gives the update for output-layer weights. The deeper step is that the same idea lets the network compute how much a hidden unit contributed to the final error. Since a hidden unit affects many later units, its influence is the weighted sum of the downstream error signals:

$$
\frac{\partial E}{\partial y_i} = \sum_j \frac{\partial E}{\partial x_j} w_{ji}
$$

That quantity is then turned into a hidden-unit input derivative by multiplying by the derivative of the activation function at that hidden unit. In modern notation people often compress this into a `delta` term, but the conceptual content is exactly what the paper emphasizes: each hidden unit receives a blame signal formed by looking at the error signals of units it influences, weighted by the strengths of those influences.

The backward-pass pipeline is therefore:

Output mismatch -> output derivatives -> hidden-layer derivatives from downstream weighted sums -> earlier hidden-layer derivatives -> weight gradients everywhere

This is why the method is called back-propagation. What propagates backward is not the target itself, but partial derivatives of the error with respect to internal states.

**What the weight update rule looks like in practice**

Once the partial derivatives are known, the simplest update is ordinary gradient descent:

$$
\Delta w = - \varepsilon \frac{\partial E}{\partial w}
$$

where `epsilon` is the learning rate. The paper also uses an acceleration term that later became standard momentum:

$$
\Delta w(t) = - \varepsilon \frac{\partial E}{\partial w}(t) + \alpha \Delta w(t-1)
$$

The idea is that one should not just move according to the current gradient, but also retain some velocity from recent weight updates. The authors explain this geometrically: ravines in the error surface can cause oscillation across a steep direction and slow progress along a shallow one, while momentum damps the high-curvature oscillation and lets learning move faster in the useful direction.

The paper also notes an implementation choice that is easy to miss. One can update after every training case, or one can accumulate gradients over the whole set of cases and then update. The reported experiments use accumulated gradients across a sweep of the training set before adjusting the weights.

**Why random initialization matters**

The procedure has a symmetry problem if all weights start identical. If hidden units begin in perfectly symmetric states, they receive identical error signals and therefore remain identical forever. The network would fail to differentiate their functions. The remedy is simple but essential: start with small random weights. This is one of those details that looks minor but is foundational. Without symmetry breaking, the theory would be correct and the actual system would still fail to learn useful differentiated hidden features.

**What the paper means by learned representations**

The paper's title matters. It is not just about optimizing an output function. It is about learning representations. A hidden unit is useful when its pattern of activity captures a regularity that is not explicit in the raw input coding but helps organize the mapping from inputs to outputs. The authors are therefore interested not only in whether the network reaches the right answers, but in what kind of internal coding it discovers on the way there.

That emphasis is one reason the paper remained so influential. It argues that hidden layers can become meaningful computational objects rather than mysterious intermediate numbers.

**The mirror-symmetry experiment**

The first demonstration task is mirror symmetry detection in a one-dimensional binary input array. This is a good example because no single input bit, considered by itself, tells you whether the whole pattern is symmetric. Simply summing local evidence is not enough. The property to be detected is relational and global, so the network needs intermediate units that compare structure across positions.

The paper reports that the learning procedure discovers an elegant solution using only two hidden units. The learned network has a striking structure: for a given hidden unit, weights on positions symmetric around the center are equal in magnitude and opposite in sign. That means a perfectly symmetric pattern sends cancelling contributions into that hidden unit, producing a net input of zero. Because the hidden units carry negative biases, they stay off when symmetry is present. The output unit has a positive bias, so with both hidden units off it turns on and signals symmetry.

For a non-symmetric pattern, the cancellation fails. At least one hidden unit receives a nonzero activation, turns on, and suppresses the output. The paper points out an especially clever detail in the learned solution: the weights on one side of the midpoint occur in the ratio `1:2:4`, which makes each half-pattern generate a unique sum. That ensures that the only lower-half pattern capable of exactly cancelling the upper-half sum is the true mirror image. This is a beautiful example of the network inventing a compact coding scheme that no one explicitly programmed into it.

The reported training details also matter historically. Learning required `1,425` sweeps through the full set of `64` possible input vectors, using `epsilon = 0.1`, `alpha = 0.9`, and random initial weights drawn uniformly from `-0.3` to `0.3`. Those details show that the paper was not just presenting an abstract theorem. It was demonstrating an operational training recipe.

**The family-tree experiment and what hidden units actually encode**

The second major example is much richer and arguably more revealing. The network is trained on two isomorphic family trees. Knowledge is represented as triples of the form:

`<person 1> + <relationship> -> <person 2>`

where relationships include roles such as father, mother, husband, wife, son, daughter, uncle, aunt, brother, sister, nephew, and niece. The network receives a person and a relationship as input and must activate the correct output person or persons. Because some relations have multiple correct answers, the system may need to activate more than one output unit.

The architecture is a five-layer network. One group of input units represents the first person, another group represents the relationship, and each of those groups first projects into its own small hidden representation. Those representations are then combined through deeper hidden layers before driving the output units representing possible second persons.

The important result is not merely that the network memorizes examples. It learns an internal code that reflects real latent structure in the domain. After training on `100` of the `104` possible triples, the network generalizes correctly to the remaining four. When the authors inspect the learned hidden units, they find features that were never explicitly given in the one-hot input coding. One hidden unit primarily distinguishes the English family from the isomorphic Italian family. Another tracks generation. Another captures branch structure within the family. Because the network has discovered the isomorphism between the two trees, it can share structure across them and generalize sensibly.

This is a central conceptual point. The learned internal representation is not a copy of the input coding. It is a restructuring of the domain into dimensions that help solve the relational task. Modern readers would call this latent factor discovery or distributed representation learning. In 1986 the paper is already showing that hidden units can learn abstractions like nationality, generation, and branch even when the data is presented as isolated symbolic identities.

The family-tree experiment also contains several practically interesting details. The authors introduce a small weight decay after each update so that after long training the magnitude of a weight reflects how useful it is in reducing error. They also treat the error as effectively zero when desired-on outputs exceed `0.8` and desired-off outputs fall below `0.2`, because finite sigmoid networks do not naturally hit exact `0` and `1` without driving weights toward infinity. That is an early sign of the authors understanding the numerical behavior of sigmoidal networks rather than treating the math as purely idealized.

**The recurrent-network extension**

The paper does not stop at simple feedforward stacks. It argues that a recurrent network run for several time steps can be viewed as equivalent to a deeper layered network in which each time step becomes another layer. Once you see the model that way, the same differentiation logic applies. The catch is that two extra bookkeeping requirements appear. First, one must store the history of activations from the forward process because the backward process needs them later. Second, weights that are conceptually the same across time-unrolled copies must be kept tied, which means their gradients need to be averaged before updating them.

This section is short, but historically it is very important. It contains the core unrolling idea that later becomes backpropagation through time. The paper is not yet giving the modern recurrent-neural-network toolkit, but it clearly shows that the gradient-based logic is not confined to shallow static mappings.

**What the paper says about local minima and where that judgment was right or incomplete**

The authors openly acknowledge the standard objection to gradient descent: the error surface may contain local minima, so the procedure is not guaranteed to find the global optimum. Their empirical judgment, based on the tasks they studied, is that poor local minima are rare and especially associated with networks that have just barely enough connections to solve the task. Adding extra connections creates more directions in weight space and can provide routes around bad traps.

That claim was directionally important but not universally sufficient. For the relatively small networks and tasks in the paper, this optimism was often justified. For later deep networks, optimization turned out to be much more delicate because of vanishing gradients, saturation, initialization issues, data scale, and architectural choices. So the paper was right that local minima were not the fatal objection many people assumed, but it would be too strong to read it as having solved all future optimization problems. Its real victory was showing that useful multilayer learning was possible at all.

**How to read the paper historically**

The paper presents back-propagation as a new learning procedure, and in the context of mainstream neural-network practice that framing made sense. But historically the chain-rule idea did not originate from nowhere in October 1986. Related derivations and precursor ideas existed, and the paper itself explicitly notes roughly similar variants by David Parker and Yann Le Cun. So the fairest historical reading is not "this paper invented the very first gradient-based multilayer training idea." The fairer reading is that it made the method clear, general, convincing, and experimentally compelling enough to transform the field.

That distinction matters because it clarifies what kind of landmark this is. It is a breakthrough paper in the sense that it changed what researchers believed was trainable and worthwhile, not in the simplistic sense of being the first human thought ever to involve the chain rule.

**What the paper ultimately establishes**

By the end, the paper has done three things at once. It has given a clean learning rule for multilayer differentiable networks. It has shown, through concrete examples, that hidden units can discover structurally meaningful features instead of merely memorizing training cases. And it has argued that the method extends beyond static feedforward nets to iterative systems. The broad claim is that gradient descent in weight space can construct interesting internal representations, even if the resulting learning rule is not biologically realistic in its present form.

That final caveat is important. The authors explicitly say the procedure is not a plausible model of brain learning. Their point is more restrained and more durable: if gradient information can create useful internal representations in artificial networks, then it is worth looking for ways brains might approximate something functionally similar.

---

## **Subtle points, clarifications, and limits**

- The paper is about **learning hidden representations**, not just minimizing output error. The examples are chosen to show that the hidden units discover latent structure such as symmetry constraints, family generation, and family branch.
- Back-propagation does **not** tell a hidden unit what symbolic concept it should represent. It sends derivatives backward so the hidden unit changes in whatever way most reduces downstream error.
- The procedure depends on **differentiable nonlinearities**. Hard threshold units, which were central to older perceptron thinking, do not fit the derivation in the needed way.
- The paper's optimism about optimization should be read in context. It correctly rebutted the idea that multilayer learning was hopeless, but later deep learning still needed better initialization, architectures, nonlinearities, regularization, data, and hardware before large-scale success arrived.
- Historically, this paper is best understood as the work that **popularized and crystallized** practical back-propagation for multilayer networks, not as the sole absolute origin of every precursor idea.

---

## **Closing perspective**

This paper became canonical because it changed the research attitude toward neural networks. After Minsky and Papert, many people treated hidden-unit networks as conceptually interesting but procedurally awkward. Rumelhart, Hinton, and Williams turned them into trainable systems and, more importantly, into systems whose hidden layers could be interpreted as learned structure rather than as unexplained mathematical residue. That is why the paper still carries very high status across connectionist history, deep learning textbooks, and the work of later neural-network researchers. It marks the moment when "learn the features" became a credible technical program instead of a wish.

---

## **Personal comprehension notes**

The cleanest way to think about the paper is that the network first makes a guess, then asks every weight how much it helped create the mistake. The forward pass answers "what does the network currently believe?" The backward pass answers "how should each connection change so this belief becomes less wrong next time?" Hidden units are not hand-written concepts. They are whatever intermediate features make that correction process efficient.

The mirror-symmetry example is a very good memory hook because it shows what hidden units are doing. They are not storing the answer "symmetric" directly. They are building detectors whose activations cancel when the mirrored halves match and fail to cancel when they do not. That is representation learning in miniature.

The family-tree example is the stronger memory hook for abstraction. The way to think about it is:

- The inputs name particular people and relationships.
- The hidden layers quietly rediscover deeper axes such as family, generation, and branch.
- Those hidden axes make it possible to answer unseen relational queries correctly.

So the intuitive slogan for the paper is:

Observed cases -> learned hidden structure -> better generalization

Two compact ways to remember the paper:

- **Backprop as credit assignment:** send error derivatives backward so hidden units know how they contributed to the final mistake.
- **Representation learning before the phrase was fashionable:** the network is useful because it invents internal features that were not explicitly encoded in the inputs.

---

## **Compact retention notes**

- **Paper type:** Foundational method paper with experimental demonstrations
- **Core idea:** Use gradient descent with a backward pass of error derivatives to train multilayer networks so hidden units learn task-appropriate internal representations.
- **Main mechanism:** Forward pass computes activations, backward pass applies the chain rule to propagate error terms through hidden layers, and weights are updated with learning rate plus optional momentum.
- **Key result:** The method learns nontrivial hidden features, such as symmetry-sensitive codes and family-structure abstractions, and generalizes beyond the seen training cases.
- **Main limitation:** It requires differentiable units, is not biologically plausible in its presented form, and does not guarantee globally optimal solutions.

---

## **Citations used in the paper**

- Frank Rosenblatt, *Principles of Neurodynamics*, 1961 - background on perceptrons and earlier neural learning rules for systems without learned hidden representations.
- Marvin L. Minsky and Seymour Papert, *Perceptrons*, 1969 - classic analysis of the limitations of simple perceptrons that motivates the need for intermediate learned structure.
- Yann Le Cun, *Proc. Cognitiva 85*, 1985 - early related work on gradient-based learning in multilayer systems, acknowledged by the authors as a similar scheme.
- David E. Rumelhart, Geoffrey E. Hinton, and Ronald J. Williams, *Parallel Distributed Processing: Explorations in the Microstructure of Cognition, Vol. 1: Foundations*, 1986 - expanded treatment by the same authors, showing the broader connectionist context around the Nature paper.

---
