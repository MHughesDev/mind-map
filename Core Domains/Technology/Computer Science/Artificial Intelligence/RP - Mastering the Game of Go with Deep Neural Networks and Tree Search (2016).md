# Mastering the Game of Go with Deep Neural Networks and Tree Search

**Paper link:** https://storage.googleapis.com/deepmind-media/alphago/AlphaGoNaturePaper.pdf

---

## **Paper metadata**

**Authors / collaborators:**
- David Silver
- Aja Huang
- Chris J. Maddison
- Arthur Guez
- Laurent Sifre
- George van den Driessche
- Julian Schrittwieser
- Ioannis Antonoglou
- Veda Panneershelvam
- Marc Lanctot
- Sander Dieleman
- Dominik Grewe
- John Nham
- Nal Kalchbrenner
- Ilya Sutskever
- Timothy Lillicrap
- Madeleine Leach
- Koray Kavukcuoglu
- Thore Graepel
- Demis Hassabis

**Organizations / companies / institutions involved:**
- Google DeepMind
- Google

**Publication date:**
27 January 2016; issue dated 28 January 2016

**Venue / source:**
Nature, Volume 529, pages 484-489

**Research paper type / category:**
- Foundational / landmark paper
- Method / model paper
- Experimental / empirical paper
- Systems / engineering paper

**Primary field / topic area:**
Computer Go, reinforcement learning, search, and planning with deep neural networks

**Keywords:**
- AlphaGo
- Go
- policy network
- value network
- Monte Carlo tree search
- self-play reinforcement learning

---

## **Opening perspective**

This paper sits at the intersection of game-playing AI, reinforcement learning, and search, but the cleanest way to read it is as a paper about how to make search selective in a domain where brute force fails. Go had resisted classical game AI for decades because both of the usual shortcuts were weak: searching deep was too expensive, and evaluating unfinished positions was too unreliable. Chess-style alpha-beta search plus handcrafted evaluation had produced superhuman play in other games, but Go's branching factor and positional subtlety made that recipe break down.

What made this paper historic is that it did not merely add a neural network to an existing Go engine. It reorganized the whole system around two learned objects: a policy for saying which moves deserve attention, and a value function for saying what unfinished positions are worth. Those learned components were then embedded inside Monte Carlo tree search rather than treated as standalone replacements for search. That hybridization is the paper's real contribution. People often remember AlphaGo as "deep reinforcement learning beat Go," but the paper is more interesting than that slogan. It is a carefully staged fusion of imitation learning, self-play improvement, value learning, and large-scale search engineering.

---

## **Full walkthrough and explanation**

**Why Go was such a hard target**

The paper opens from the language of perfect-information games. In principle, games like chess or Go have an optimal value function `v*(s)` that tells you whether a position `s` is winning or losing under perfect play. In small games one can compute that value by searching the game tree. But the tree size grows roughly like `b^d`, where `b` is branching factor and `d` is depth, and for Go those numbers are enormous: the paper gives rough figures of `b ~= 250` and `d ~= 150`. That means exhaustive search is hopeless.

Historically there were two general ways to cope. One is to reduce depth by evaluating positions before the end of the game with an approximate value function `v(s)`. The other is to reduce breadth by using a policy `p(a|s)` that prioritizes promising actions. Chess and checkers had done well with powerful search plus strong evaluation. Go had not. Before AlphaGo, the strongest Go systems were mostly Monte Carlo tree search programs. MCTS helped because it replaced exhaustive search with selective sampling, but it still depended on rollout policies and lightweight heuristics that were much weaker than a real understanding of the board.

So the paper's central idea is easy to state even if it is difficult to make work: learn a strong policy to cut search breadth, learn a strong value function to cut search depth, and then combine both inside MCTS.

The system-wide pipeline is:

Human expert positions -> supervised policy network `p_sigma`

Human positions with cheap pattern features -> fast rollout policy `p_pi`

`p_sigma` -> self-play policy-gradient improvement -> reinforcement learning policy `p_rho`

Self-play with `p_rho` -> sampled positions and outcomes -> value network `v_theta`

`p_sigma` + `p_pi` + `v_theta` + Monte Carlo tree search -> AlphaGo move selection

That layered pipeline matters because AlphaGo does not rely on one model doing everything. Different learned components do different jobs at different speeds.

**The paper's basic decomposition: policy for breadth, value for depth**

The paper uses "policy network" and "value network" in a very literal sense. A policy network outputs a probability distribution over legal moves. A value network outputs a scalar estimating the eventual winner from a given board state. Those are conceptually distinct objects, and AlphaGo actually uses several policies:

- `p_sigma`, the supervised learning policy network trained to imitate expert moves
- `p_rho`, the stronger reinforcement learning policy network trained by self-play to maximize winning
- `p_pi`, a fast rollout policy based on local pattern features
- `p_tau`, a tree policy used as a temporary placeholder for priors at newly expanded nodes

This is one of the first places readers can get confused. "The policy network" is not a single thing in the final system. There is a slow, high-quality policy for strong priors, a stronger self-play policy used for value-learning targets, and a cheap rollout policy used because deep networks are too slow to evaluate at every rollout step.

**Supervised policy learning: first learn to see plausible moves**

The first stage is imitation learning from human expert play. The supervised policy network `p_sigma(a|s)` is a deep convolutional network that takes a board position and predicts the expert move played there. The input is not raw pixels in the casual sense people often imagine. The board is encoded as a stack of `19 x 19` feature planes representing things like stone colors, liberties, captures, self-atari, move legality, move history, ladder features, and related state information. That is already an important truth-checking point: the system is deeply learned, but it is not domain-agnostic or feature-free.

Architecturally, the match-time policy network is a 13-layer convolutional network. The first hidden layer uses `5 x 5` filters, the later hidden layers use `3 x 3` filters, and the final layer produces a softmax distribution over board locations. In the Fan Hui match version, the network used `k = 192` filters per convolutional layer. The team also experimented with larger networks and explicit symmetry ensembles, which gave higher predictive accuracy but cost too much latency for search.

The training data came from about 29.4 million positions from 160,000 KGS games played by human experts in the 6-dan to 9-dan range, with symmetry augmentation over the eight rotations and reflections of the board. The paper reports held-out prediction accuracy up to `57.0%` with full input features, compared to a previous state of the art of `44.4%`. That is a very large jump for move prediction in Go, and the paper emphasizes that small accuracy gains translated into surprisingly large strength gains. The learned policy is not just copying humans; it is learning a representation of local and global board structure that makes high-level move selection much stronger than earlier shallow predictors.

The supervised stage is the easiest to understand but also the easiest to misread. Predicting human moves is not the same as maximizing win probability. A system trained only to imitate experts may reproduce strong style without discovering better-than-human deviations or learning which human conventions are merely conventional. The paper knows this, which is why supervised learning is only the first stage.

At the same time, the paper trains a much faster rollout policy `p_pi`. This policy is not a deep network. It is a linear softmax over local pattern features built around response and non-response motifs near the previous move and the current candidate move, plus a few handcrafted Go-specific features. It reached only `24.2%` prediction accuracy, but it could choose moves in about `2 microseconds`, versus about `3 milliseconds` for the deep policy network. That speed difference is decisive inside rollouts. AlphaGo therefore keeps the cheap policy for simulation and the expensive policy for guidance.

**Reinforcement learning: move from imitation to winning**

The second stage takes the supervised policy network and improves it by self-play. The reinforcement learning policy `p_rho` has the same architecture as `p_sigma`, and is initialized with the supervised weights. It is then optimized with policy gradient reinforcement learning so that it wins more games rather than merely matching expert choices.

The training setup is subtle. The current policy does not always play against its latest self. Instead, it plays against previous versions sampled from an opponent pool. That stabilizes learning by preventing the policy from overfitting to a single currently favored opponent behavior. The reward is simple: `+1` for a win and `-1` for a loss at the end of the game, with no intermediate reward shaping. Conceptually, this stage says: imitation gives you a good prior over sensible play, but self-play should push the system toward whatever actually wins.

This policy-improved network is already very strong even without search. The paper reports that the raw RL policy network won more than `80%` of games against the supervised policy network and `85%` of games against Pachi, a strong MCTS-based open-source Go program that executed `100,000` simulations per move. That result is one of the paper's most striking facts. Before tree search even enters, the learned policy alone is already competitive with top Go engines.

But the paper also makes a counterintuitive observation: the final AlphaGo search uses the supervised policy network `p_sigma` as its main tree prior, not the stronger RL policy `p_rho`. The reason is not that `p_rho` is weaker overall. It is that search wants a broad, calibrated prior over several plausible moves, while the RL policy is optimized to pick a single best move and tends to be too concentrated. Human expert play gives a more diverse beam of promising candidates, which is more useful for guiding search expansion. This is a subtle but very important distinction between "best raw policy" and "best policy prior for tree search."

**Value learning: stop searching every line to the end**

The policy network reduces breadth, but Go is still too deep to search to terminal states everywhere. The paper therefore learns a value network `v_theta(s)` that predicts the expected outcome from a position. This is the depth-reduction half of the design.

The value network has an architecture similar to the policy network but ends in a scalar `tanh` output rather than a distribution over moves. It takes nearly the same feature planes, with one additional plane encoding the current color to play. The match-time value network has one extra convolutional layer compared with the policy network, plus a fully connected hidden layer with `256` rectifier units before the scalar output.

What the paper discovered here is that naive training on expert games overfits badly. If you take every position from a game and label it with the game's final outcome, then adjacent positions are almost identical yet share the same target. The network can memorize game trajectories instead of learning generalizable position evaluation. The paper reports this failure directly: when trained that way on KGS data, the value network got a minimum mean squared error of `0.19` on training data but `0.37` on test data, a clear overfitting gap.

To fix this, the authors generate a new self-play data set of over 30 million distinct positions, each taken from a different game. The data-generation procedure is worth understanding because it is not just "self-play and save everything." For each game, they sample a random time `U`, play the early moves using the supervised policy, force one random legal move to diversify the position distribution, then play the rest of the game using the reinforcement learning policy. From each such game they keep only one training example, namely a single state and the final outcome. That makes the targets much less correlated and produces a broader spread of positions.

This stage has its own pipeline:

Early game moves from `p_sigma` -> one random legal move -> rest of game from `p_rho` -> final win/loss outcome -> single sampled training position -> regression target for `v_theta`

The trained value network substantially outperforms plain Monte Carlo rollouts with weak policies. The paper reports train and test mean squared errors of `0.226` and `0.234`, indicating far less overfitting, and shows that a single forward pass of the value network is consistently more accurate than rollouts using the fast rollout policy. It also approaches the accuracy of rollouts using the much stronger RL policy while using roughly `15,000` times less computation. That is exactly the kind of compression of search effort the paper needed.

There is also a conceptual caveat here that matters. The value network is not learning the true perfect-play value `v*(s)`. It is approximating the expected outcome of games played according to AlphaGo's learned self-play policy. That is still extremely useful, but it is not the same as proving optimality. The paper sometimes speaks in ways that brush close to the idealized optimal-value language from game theory; the actual learned object is a practical approximation tied to the distribution induced by AlphaGo's own policy.

**How AlphaGo searches**

Once the policy and value networks exist, AlphaGo combines them in an asynchronous policy-and-value Monte Carlo tree search algorithm, or APV-MCTS. Each edge `(s, a)` in the search tree stores three essential statistics:

- `P(s, a)`: a prior probability for taking action `a` in state `s`
- `N(s, a)`: the visit count
- `Q(s, a)`: the current action-value estimate

The implementation also stores separate rollout and value accumulators so that these two evaluation sources can be mixed cleanly.

Every simulation proceeds through the now-familiar four phases of tree search:

Selection -> Expansion -> Evaluation -> Backup

During selection, AlphaGo chooses actions according to a rule of the form

$$
a_t = \arg\max_a \left[ Q(s_t, a) + u(s_t, a) \right]
$$

where `u(s_t, a)` is an exploration bonus that grows with prior probability and shrinks as the action is visited more often. In the Methods section this is given as a variant of what later became widely recognized as PUCT. Intuitively, the search prefers actions that look promising either because they have already performed well or because the policy prior says they deserve more investigation.

When a leaf is reached, AlphaGo does not immediately expand every possible child. Expansion occurs only once a threshold is crossed, specifically when a visit count exceeds `n_thr = 40`. Newly expanded nodes first get temporary priors from the tree policy `p_tau`, and then the supervised policy network `p_sigma` evaluates the leaf on GPU and replaces those placeholders with stronger priors. This detail matters because the whole system is asynchronous: CPUs handle search threads and rollouts, GPUs evaluate the expensive neural networks, and the queues between them are part of the algorithm rather than just implementation noise.

Leaf evaluation mixes two different estimators:

$$
V(s_L) = (1 - \lambda) v_{\theta}(s_L) + \lambda z_L
$$

Here `v_theta(s_L)` is the value network's estimate of the leaf position, `z_L` is the outcome of a rollout from that leaf to the end of the game using the fast rollout policy, and `lambda = 0.5` in the match version. This is another place where popular memory oversimplifies the system. AlphaGo's strongest version in this paper is not "the value network replaced rollouts." The value network and rollouts are complementary, and the mixed version performed best.

The paper explains why the combination helps. The value network approximates the outcome of play under the strong but slow RL policy, while rollouts score complete continuations under the weak but fast rollout policy. Those are noisy in different ways. Mixing them gives more robust search estimates than either alone.

At backup time, AlphaGo updates the statistics of every traversed edge. The value and rollout information are accumulated separately and then combined into `Q(s, a)`. Once the allotted search time ends, AlphaGo does not play the move with highest action value. It plays the move with highest visit count at the root. The paper notes that this is less sensitive to outliers. The search tree is then reused for the next move by keeping the chosen child as the new root and discarding the irrelevant branches.

This entire search engine is engineered for scale. The single-machine match version used `40` search threads, `48` CPUs, and `8` GPUs. The distributed version used `40` search threads, `1,202` CPUs, and `176` GPUs. The paper also notes that the match version continues searching during the opponent's turn, uses virtual loss to reduce thread collisions, chooses mini-batch size `1` for network evaluations to minimize latency, and shapes time use toward the middle game. These details are not decorative. They are part of why the system actually reached professional strength.

**Representation and domain knowledge**

One of the most important ways to read this paper honestly is to notice what is learned and what is engineered. The learned part is substantial: deep convolutional policies, a learned value function, policy-gradient self-play, and search statistics informed by those networks. But the paper is not trying to be a pure end-to-end "just give it raw boards and everything emerges" story.

The feature representation is Go-specific. The rollout policy is built from local patterns and a few handcrafted common-sense Go features. The input planes include liberties, capture counts, self-atari, ladder information, and sensibleness. The system uses an expansion threshold, a specific search-control rule, virtual losses, search-tree reuse, time management, and a resignation heuristic. None of this makes the paper less impressive. It just means the correct lesson is not "generic deep learning alone solved Go." The correct lesson is that learned policy and value functions became strong enough to serve as the main intelligence inside a very carefully designed search system.

The symmetry discussion is a nice example. Earlier Go work sometimes tried to bake rotational and reflectional symmetry directly into network filters. AlphaGo found that such hard constraints hurt performance in larger networks because intermediate filters need freedom to learn asymmetric patterns. Instead, the system uses symmetry at run time by evaluating randomly transformed boards during search or by averaging over multiple symmetries in explicit ensembles. That is a practical scientific choice, not mere implementation clutter.

**What the experiments actually establish**

The evaluation section is where the paper becomes historic rather than merely elegant. In internal tournaments with `5` seconds per move, single-machine AlphaGo won `494` out of `495` games, or `99.8%`, against other leading Go programs including Crazy Stone, Zen, Pachi, Fuego, and GnuGo. It also won handicap games in which the opponent received four free opening stones, beating Crazy Stone `77%` of the time, Zen `86%`, and Pachi `99%`. The distributed version was stronger still, winning `77%` against the single-machine version and `100%` against all other tested programs.

The ablations are just as important as the headline match. A version using only the value network and no rollouts still outperformed all other Go programs, which showed that value networks were already viable for serious Go search. But the mixed evaluation with `lambda = 0.5` beat both value-only and rollout-only variants. That confirms the paper's main systems claim: the strength comes from integration, not from any one module in isolation.

The match against Fan Hui provides the public milestone. Fan Hui was a professional 2-dan player and the reigning European champion in 2013, 2014, and 2015. The formal five-game match was played from 5-9 October 2015 under Chinese rules with `7.5` komi, `1` hour of main time, and three `30`-second byo-yomi periods. AlphaGo won the formal match `5-0`, and won the five informal shorter-time games `3-2`. The paper is correct to call this the first time a computer program defeated a professional human player in full-sized Go without handicap.

At the same time, the paper's discussion sometimes pushes a little beyond what the evidence in this exact article strictly proves. It says AlphaGo plays "at the level of the strongest human players." The more carefully supported claim is that it overwhelmingly surpassed existing Go programs and defeated a professional human champion in Europe. That is already an enormous achievement. But the top world-title-level human comparison, in the strongest possible sense, was still something readers would naturally want to validate with later events, including the Lee Sedol match and subsequent AlphaGo versions.

**Why the paper changed how people think**

What changed after this paper was not just the benchmark status of Go. The paper altered a design intuition. Before AlphaGo, deep learning and search could be viewed as separate traditions: one learned representations from data, the other reasoned over explicit lookahead trees. AlphaGo showed that strong learned policy and value functions could become the steering intelligence of search itself. That point carried far beyond Go.

The later AlphaGo Zero and AlphaZero systems are often treated as if they made this paper obsolete. In one sense they superseded it. They removed human supervision, simplified the pipeline, discarded rollouts, and learned from self-play more directly. But that only makes this paper more important historically, not less. It is the bridge paper. It is the place where deep policies and values first demonstrated that they could carry a full professional-strength planning system in a domain long thought resistant to exactly that kind of learning.

---

## **Subtle points, clarifications, and limits**

Readers often compress AlphaGo into "policy network plus value network," but the paper actually relies on a four-policy ecology: supervised policy, reinforcement-learning policy, rollout policy, and tree policy. Those roles are not interchangeable, and several of the most interesting results come from the fact that the best component for one role is not the best component for another.

It is also easy to overstate how general or clean the system is. This is not yet AlphaGo Zero. Human expert data, Go-specific feature engineering, pattern-based rollouts, and substantial distributed systems work all matter. The paper's achievement is therefore not that search disappeared, nor that hand design disappeared, but that learned evaluation became powerful enough to reorganize the whole search stack around it.

Finally, the result against Fan Hui should be remembered accurately. It was absolutely historic, but it was a first defeat of a professional human in full 19x19 Go, not yet a proof that the system had already dominated every top world champion. The paper earns its reputation without needing that stronger gloss.

---

## **Closing perspective**

This paper has landmark status because it solved two problems at once: it delivered a visible competitive breakthrough, and it gave the field a reusable conceptual pattern. The breakthrough was AlphaGo's professional-level Go play. The deeper pattern was that policy learning can tell search where to look, value learning can tell search when to stop, and the combination can outperform either brute-force search or raw neural play alone. That insight is respected across reinforcement learning, search and planning, game AI, and the broader history of modern deep learning. Even though later systems simplified and surpassed AlphaGo, this paper remains essential because it is the moment learned intuition and lookahead planning were fused into one coherent high-performance intelligence system.

---

## **Personal comprehension notes**

The most useful mental model for AlphaGo is "intuition plus deliberation, but both are machine learned." The supervised policy is like fast expert pattern recognition: "these moves look plausible." The reinforcement-learned value function is like strategic judgment: "this position is probably winning or losing." Monte Carlo tree search is the deliberate lookahead process that keeps asking, "if I focus on the most promising branches, what actually holds up?" AlphaGo is strong because all three levels cooperate.

Another good way to think about it is that the system attacks the two dimensions of combinatorial explosion separately. Policy narrows width. Value shortens depth. Search then spends its budget only where those learned signals say it matters. If you remember only one equation-level intuition from the paper, it should be that AlphaGo is constantly trading off prior belief, accumulated evidence, and exploration pressure when deciding which branch to examine next.

It also helps to separate this paper from the myth people later tell about it. The myth is "deep RL solved Go." The paper itself is closer to "a staged learning pipeline distilled human and self-play experience into search guidance strong enough to beat professionals." That version is less slogan-ready, but it is more accurate and more instructive.

---

## **Compact retention notes**

- **Paper type:** Landmark hybrid learning-and-search systems paper
- **Core idea:** Learn policy and value functions strong enough to guide Monte Carlo tree search in Go.
- **Main mechanism:** Expert imitation -> self-play policy improvement -> self-play value learning -> APV-MCTS with policy priors and mixed value/rollout evaluation.
- **Key result:** AlphaGo beat prior Go programs by `99.8%` and defeated Fan Hui `5-0` in a formal full-board match.
- **Main limitation:** The system is still heavily Go-specific, multi-stage, compute-intensive, and not yet the cleaner self-play-only design later seen in AlphaGo Zero.

---

## **Citations used in the paper**

- Leslie V. Allis, *Searching for Solutions in Games and Artificial Intelligence*, 1994
- Martin Muller, *Computer Go*, 2002 — classic statement of why Go remained difficult for search-based AI
- Remi Coulom, *Efficient selectivity and backup operators in Monte-Carlo tree search*, 2006
- Levente Kocsis, Csaba Szepesvari, *Bandit Based Monte-Carlo Planning*, 2006 — one of the key MCTS foundations
- Sylvain Gelly, David Silver, *Combining Online and Offline Learning in UCT*, 2007 — earlier learned priors inside Go tree search
- Ilya Sutskever, Volodymyr Nair, *Mimicking Go Experts with Convolutional Neural Networks*, 2008
- Chris J. Maddison, Aja Huang, Ilya Sutskever, David Silver, *Move Evaluation in Go Using Deep Convolutional Neural Networks*, 2015
- Christopher Clark, Amos J. Storkey, *Training Deep Convolutional Neural Networks to Play Go*, 2015
- Ronald J. Williams, *Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning*, 1992 — REINFORCE foundation
- Richard Sutton, David McAllester, Satinder Singh, Yishay Mansour, *Policy Gradient Methods for Reinforcement Learning with Function Approximation*, 2000
- Gerald Tesauro, *TD-Gammon, a Self-Teaching Backgammon Program, Achieves Master-Level Play*, 1994 — earlier value-learning milestone in game AI
- Volodymyr Mnih et al., *Human-level Control through Deep Reinforcement Learning*, 2015 — immediate deep RL context for the paper
- Christopher D. Rosin, *Multi-Armed Bandits with Episode Context*, 2011 — source behind the PUCT-style exploration term
- Jeff Dean et al., *Large Scale Distributed Deep Networks*, 2012 — infrastructure context for large-scale training in DistBelief
