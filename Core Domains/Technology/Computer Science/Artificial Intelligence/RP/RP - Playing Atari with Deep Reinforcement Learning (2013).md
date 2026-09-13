# Playing Atari with Deep Reinforcement Learning

**Paper link:** https://arxiv.org/pdf/1312.5602.pdf

---

## **Paper metadata**

**Authors / collaborators:**  
- Volodymyr Mnih
- Koray Kavukcuoglu
- David Silver
- Alex Graves
- Ioannis Antonoglou
- Daan Wierstra
- Martin Riedmiller

**Organizations / companies / institutions involved:**  
- DeepMind Technologies

**Publication date:**  
19 December 2013

**Venue / source:**  
NIPS 2013 Deep Learning Workshop / arXiv preprint

**Research paper type / category:**  
- Foundational / landmark paper
- Method / model paper
- Experimental / empirical paper

**Primary field / topic area:**  
Deep reinforcement learning, value-based control from visual input

**Keywords:**  
- deep Q-network
- Atari 2600
- Q-learning
- experience replay
- convolutional neural network

---

## **Opening perspective**

This paper is one of the places where modern deep reinforcement learning becomes visible as a real program rather than a vague ambition. Reinforcement learning had long been able to solve certain structured control problems, and deep learning had begun to dominate perception, but joining the two was widely seen as unstable, data-hungry, and difficult to make work from raw sensory input. What this paper contributes is not just a better Atari agent. It shows that a single neural network architecture can look at game pixels, estimate action values, and learn competent control behavior across multiple games without hand-designed features for each one.

Why serious people still care about this paper is that it establishes a reusable recipe. The paper takes Q-learning, combines it with a convolutional network and experience replay, and demonstrates that the combination can train directly from visual input. Later deep RL systems became much larger, more stable, and more sophisticated than what appears here, but the central bridge between representation learning and control is already in place. This is why the paper is historically larger than its seven-game benchmark might suggest.

---

## **Full walkthrough and explanation**

**The problem the paper is trying to crack open**

The paper begins from a long-standing reinforcement learning problem: an agent should choose actions from high-dimensional sensory input, not from a neat hand-built state vector. Earlier RL systems that worked well in visually rich domains usually depended on carefully engineered features or narrow task structure. Deep learning, meanwhile, had started to prove that large neural networks could learn powerful representations from raw images and speech. So the natural question was whether the same representational strength could be attached to a control algorithm and used end to end.

The paper is unusually clear about why that is hard. Reinforcement learning does not give you stable labeled examples in the way supervised learning does. The reward signal is sparse, noisy, and often delayed by many time-steps. The data is highly correlated because consecutive frames come from the same unfolding trajectory. Worse, the data distribution keeps changing because the current policy changes what the agent will experience next. Those are exactly the conditions under which large nonlinear function approximators were widely feared to become unstable.

This is the setting in which the paper makes its claim: if those instabilities can be managed well enough, then a convolutional network should be able to learn a useful control policy straight from pixels.

**From Atari interaction to action values**

The environment is the Atari 2600 emulator. At each time-step the agent selects an action `a_t` from the set of legal actions `A`, observes an image `x_t` of the current screen, and receives a reward `r_t` corresponding to the change in game score. The screen image is high-dimensional, and a single frame is not enough to fully identify the true game state. Motion direction, hidden timers, and other latent aspects of the game are not always recoverable from one image. So the paper treats the problem as partially observed and defines the state as a sequence of observations and actions rather than a single frame.

In theory the state history is the whole sequence up to time `t`, written as `s_t = x_1, a_1, x_2, ..., a_{t-1}, x_t`. The objective is to maximize future discounted return:

$$
R_t = \sum_{t' = t}^{T} \gamma^{t' - t} r_{t'}
$$

Here `T` is the end of the episode and `gamma` discounts later rewards. The key object is the optimal action-value function `Q^*(s, a)`, which tells you how much future discounted reward you can expect if you see state history `s`, take action `a`, and then behave optimally afterward. It obeys the Bellman equation:

$$
Q^*(s, a) = \mathbb{E}_{s' \sim E}[r + \gamma \max_{a'} Q^*(s', a') \mid s, a]
$$

This equation is central. `r` is the immediate reward for the current action, `s'` is the next state history, and the `max` over `a'` says that after the current step the agent is assumed to act optimally. So the value of the current decision is immediate payoff plus the best discounted continuation.

Instead of estimating a separate value for every possible state-action pair, the paper uses a neural approximation `Q(s, a; \theta)`, where `\theta` are the network parameters. The training objective is:

$$
L_i(\theta_i) = \mathbb{E}_{s,a \sim \rho(\cdot)}[(y_i - Q(s, a; \theta_i))^2]
$$

with target

$$
y_i = \mathbb{E}_{s' \sim E}[r + \gamma \max_{a'} Q(s', a'; \theta_{i-1}) \mid s, a]
$$

The network is therefore trained to make its current estimate match a one-step bootstrapped target. This is already much less comfortable than ordinary supervised learning, because the target itself depends on another value prediction rather than on a fixed label.

**Why this was not an obvious success case**

The paper spends time reviewing earlier reinforcement learning because the historical context matters. TD-Gammon had already shown that neural networks and temporal-difference learning could work together in a striking domain. But follow-up attempts in games like chess, Go, and checkers had been far less successful, and the community had good reasons to worry about instability. Combining off-policy learning with nonlinear function approximation could make Q-learning diverge, not merely perform badly.

That makes this paper more interesting than a simple architecture note. It is not introducing deep learning into a part of machine learning where everyone expected it to work. It is stepping into a place where many researchers expected serious optimization pathologies. The paper therefore has to do two jobs at once: propose a useful system and explain why the system does not immediately collapse.

It also positions itself relative to neural fitted Q-learning and other earlier methods. NFQ already used a neural network to approximate a Q-function, but it relied on batch optimization whose cost grew with the entire data set. This paper wants something more scalable: lightweight stochastic gradient updates, applied continuously, directly from visual input, and robust enough to handle large replay memories.

**The core move: experience replay**

The main algorithmic move is experience replay. Instead of updating the network only from the latest transition, the agent stores experiences `e_t = (s_t, a_t, r_t, s_{t+1})` in a replay memory `D`. During learning, it samples random minibatches of past transitions from that memory and applies Q-learning updates to those samples.

This does several important things at once. First, it makes better use of data because one experience can influence many gradient updates rather than being used once and then discarded. Second, random sampling breaks the strong short-range temporal correlations in consecutive experience, which makes the optimization problem look more like learning from a shuffled data set. Third, because the memory contains transitions generated by many earlier versions of the policy, the effective training distribution is averaged over many past behaviors rather than being tied only to the current policy's most recent quirks.

That third point is easy to miss but crucial. If you update only on current on-policy experience, the network's current preferences heavily determine what it sees next, which can create bad feedback loops and oscillations. Experience replay partially smooths that problem. The paper is clear, though, that the replay buffer is simple and limited. It stores only the most recent `N` transitions, overwriting older ones, and samples uniformly at random. The authors explicitly note that more sophisticated sampling strategies might learn faster by focusing on especially informative transitions. That later became a major line of work.

**How the agent actually sees the game**

The raw Atari input is a `210 x 160` RGB image at `60 Hz` with a `128`-color palette. Feeding that directly into a learning system would be computationally expensive, so the paper preprocesses each frame. The RGB image is converted to grayscale, down-sampled to `110 x 84`, and then cropped to `84 x 84`. The paper notes that this final crop was partly motivated by the GPU convolution code they used, which expected square inputs.

The function `phi` maps a history into a fixed-size state representation by taking the last four preprocessed frames and stacking them. This gives an `84 x 84 x 4` input tensor. That design is a practical compromise. In the formal RL description the state is the whole observation-action history, but a network cannot easily consume arbitrary-length histories. The four-frame stack is meant to carry enough short-term motion information for the agent to infer velocity and direction in many Atari settings.

The network architecture is modest by later standards but was extremely consequential. The first hidden layer applies `16` convolutional filters of size `8 x 8` with stride `4`, followed by rectified nonlinearities. The second applies `32` filters of size `4 x 4` with stride `2`, again followed by rectifiers. Then comes a fully connected hidden layer with `256` rectified units. The output layer is linear and produces one scalar `Q` value for each valid action in the current game, with the number of legal actions ranging from `4` to `18`.

That output design matters. Some earlier Q-network formulations fed both state and action into the model and needed a separate forward pass for each candidate action. Here the network takes only the state representation as input and emits all action values in one pass. That makes action selection cheap: one evaluation of the network tells the agent which action currently looks best. The paper refers to networks trained this way as Deep Q-Networks, or DQNs.

**The learning loop in concrete terms**

The full pipeline is:

Raw Atari frames -> grayscale / downsample / crop -> stack 4 recent frames -> convolutional network -> `Q` values for all legal actions -> epsilon-greedy action -> reward and next frame -> store transition in replay memory -> sample random minibatch -> temporal-difference update

At decision time the agent follows an epsilon-greedy behavior policy. Most of the time it picks the action with the highest predicted value, but with probability `epsilon` it acts randomly to preserve exploration. After taking an action, it observes the next frame and reward, converts the new recent history into the next representation `phi_{t+1}`, stores the transition, samples a random minibatch from replay memory, and performs a gradient step that nudges `Q(phi_t, a_t)` toward a bootstrapped target built from reward plus the best next-state action value.

For terminal next states the target is just the observed reward. For non-terminal next states it is reward plus discounted future value. Conceptually, the network is always trying to answer the same question: if I press this action now, how much future score is likely to follow? What makes the paper historically important is that this early version gets meaningful results without yet using the separate periodically copied target network that many people now associate with the later 2015 Nature DQN paper. Stability here comes mainly from replay, reward clipping, careful preprocessing, and conservative optimization choices.

**What the training setup really is**

The experiments cover seven Atari games: `Beam Rider`, `Breakout`, `Enduro`, `Pong`, `Q*bert`, `Seaquest`, and `Space Invaders`. A large part of the paper's appeal is that the same architecture and almost the same hyperparameters are used across all seven games. The point is not merely that the system works on one environment. It is that the authors are trying to show a single learning recipe with minimal game-specific customization.

The training recipe is quite concrete. They use RMSProp with minibatches of size `32`, train for `10 million` frames, and keep a replay memory containing the most recent `1 million` frames. Exploration is epsilon-greedy, with `epsilon` annealed linearly from `1.0` to `0.1` over the first million frames and then held at `0.1`. The agent also uses frame skipping: it selects an action every `k` frames and repeats the previous action on skipped frames. They use `k = 4` for all games except `Space Invaders`, where they switch to `k = 3` because with `k = 4` the lasers can blink out and become visually invisible.

One of the most consequential engineering choices is reward clipping. During training, every positive reward is set to `+1`, every negative reward to `-1`, and zero stays zero. This makes the scale of the temporal-difference error more uniform across games and lets one learning rate work across tasks. But it also removes information. The agent can no longer distinguish a very large positive event from a small positive one while learning. That is an important caveat: the method is not being trained on the exact score structure of each game.

The paper also pays attention to how to judge training progress. Average episode reward is noisy in reinforcement learning, because even small policy changes can drastically alter what states the policy visits. So the authors track a second quantity: the average maximum predicted `Q` value on a held-out set of states collected by a random policy before training begins. That curve is much smoother and rises steadily. Together with the absence of observed divergence in their experiments, this is presented as evidence that large neural networks can be trained stably enough for control from raw pixels, at least in this setting.

There is a useful subtlety here. The paper does not prove that the method is stable in general. It shows empirical stability on these tasks under this recipe. That is still a major achievement, but it should be read as a demonstration of viability rather than as a solved theory of deep RL optimization.

**What the experiments actually demonstrate**

The strongest part of the experimental story is that the baselines are not trivial. The compared Sarsa and Contingency agents use linear methods plus hand-engineered visual features, background subtraction, and task-specific prior structure. In contrast, DQN receives only preprocessed screen images and the reward signal. Even so, it outperforms the prior learning methods on all seven tested games.

The per-game average scores in the main table are revealing. DQN scores `4092` on `Beam Rider`, `168` on `Breakout`, `470` on `Enduro`, `20` on `Pong`, `1952` on `Q*bert`, `1705` on `Seaquest`, and `581` on `Space Invaders`. Those numbers substantially exceed the earlier Sarsa and Contingency results across the board. The system also beats the reported expert human median on `Breakout`, `Enduro`, and `Pong`, and comes relatively close on `Beam Rider`. But the table also makes the limitations obvious: human scores on `Q*bert`, `Seaquest`, and `Space Invaders` remain far higher. So the right interpretation is not "general human-level Atari." The right interpretation is "end-to-end control from pixels has suddenly become credible."

The comparison to HNeat is also instructive. HNeat can exploit deterministic Atari sequences and is evaluated by the best-performing episode. DQN, by contrast, is evaluated using an `epsilon = 0.05` policy averaged over a fixed number of steps, so it has to perform reasonably across a variety of perturbed trajectories rather than memorize a single brittle exploit. Even with that tougher interpretation of competence, DQN's average performance beats HNeat on every game except `Space Invaders`.

The paper includes a smaller but revealing analysis of learned values on `Seaquest`. The predicted value rises when an enemy appears, peaks when a torpedo is about to hit, and falls back after the event ends. That does not amount to a full theory of interpretability, but it is a meaningful sanity check. The network's value estimates are tracking game-relevant structure over time rather than only reflecting arbitrary correlations.

The broader claim, then, is not merely that the agent gets decent scores. It is that one convolutional value-learning system, with a largely shared setup, can discover useful object-level and motion-level structure directly from visual experience and turn that structure into control decisions.

**How to read the paper historically**

This paper is often blurred together with the later 2015 Nature DQN paper, but they should be kept distinct. The 2013 workshop/arXiv version already contains the essential bridge: convolutional perception, replay memory, off-policy value learning, and Atari control from pixels. But it is smaller in scope, uses only seven games, and does not yet include the later target-network stabilization that many people now treat as part of "standard DQN." If you read it as the first convincing proof that the bridge can be built at all, its historical role becomes much clearer.

It is also best read as a historically understandable but incomplete success. Atari is rich enough to matter, yet still much simpler than real-world control. The method is sample-inefficient, uses clipped rewards, only approximates state with a four-frame window, and depends on a huge amount of emulator interaction. Even so, the paper changed the field because it showed that learned perception and learned control could live inside the same end-to-end system without task-specific handcrafting. That was the conceptual unlock.

---

## **Subtle points, clarifications, and limits**

The biggest misunderstanding is to act as if this paper already contains the final later DQN recipe. It does not. Experience replay is here, but the separate frozen target network commonly associated with DQN arrives later, and this earlier version is more preliminary and more fragile than many retrospectives imply. Even the "same hyperparameters across games" claim has one stated exception: `Space Invaders` uses a different frame-skip value so the lasers remain visible.

It is also worth not taking every rhetorical flourish too literally. The paper says the agent learns from video input, reward, and terminal signals "just as a human player would" in the sense that it does not use emulator internals or hand-built features. But the analogy is only partial. The agent receives a clean scalar reward channel, trains on millions of frames, and repeatedly reuses old experience through replay memory. Those are powerful learning conditions humans do not have. The central accomplishment here is not human-like learning in a rich sense; it is end-to-end value learning from visual data.

Finally, several of the paper's simplifying choices are double-edged. Reward clipping stabilizes optimization but erases magnitude information. A four-frame state proxy helps recover motion but still leaves long-range partial observability unresolved. Uniform replay is simple and effective but not especially sample-efficient. So this paper should be respected as a breakthrough, not mistaken for a finished solution.

---

## **Closing perspective**

This paper earned lasting respect because it made deep reinforcement learning concrete. After it, the idea that a single network could look at pixels, estimate future reward, and learn control across multiple tasks no longer sounded speculative. Researchers in deep RL, game-playing agents, and later large-scale control systems all inherit part of their lineage from this result. It is still worth understanding because many later improvements, from target networks and prioritized replay to dueling heads and distributional methods, make the most sense when you see the exact instability and ingenuity of this starting point.

---

## **Personal comprehension notes**

The easiest way to think about this paper is: take the old Q-table idea, replace the table with a convolutional vision model, and then use replay memory to make the stream of reinforcement-learning experience look just stable enough for gradient descent to cope with. The network is not predicting labels in the supervised-learning sense. It is predicting, for every legal action at once, "if I do this now, how much future score do I expect?"

A good memory pipeline is:

4 recent grayscale frames -> CNN -> one value per joystick action -> epsilon-greedy move -> store transition -> sample random old transitions -> temporal-difference correction

Replay memory is the conceptual hinge. It turns a purely online control problem into something a little more like learning from a shuffled data set, without giving up interaction with the environment. That is why this paper feels like deep learning and reinforcement learning meeting halfway.

Another useful memory aid is to keep the historical distinction clear: 2013 DQN means "the bridge from pixels to Q-values works"; later DQN work means "now we know more tricks for making that bridge stronger, stabler, and broader." If you remember that, the paper sits in the right place in the development of modern RL.

---

## **Compact retention notes**

- **Paper type:** Foundational deep reinforcement learning method paper
- **Core idea:** Learn action values directly from raw Atari pixels with a convolutional network trained by Q-learning plus experience replay.
- **Main mechanism:** Stack four preprocessed frames, predict all action values in one CNN forward pass, act epsilon-greedily, and train on random replayed transitions with temporal-difference targets.
- **Key result:** One mostly shared architecture beats prior Atari RL methods on all seven tested games and exceeds reported human expert performance on three of them.
- **Main limitation:** This early DQN is still fragile, sample-inefficient, and far from human level on harder long-horizon games.

---

## **Citations used in the paper**

- Leemon Baird, *Residual algorithms: Reinforcement learning with function approximation*, ICML 1995
- Marc Bellemare, Joel Veness, Michael Bowling, *Sketch-based linear value function approximation*, Advances in Neural Information Processing Systems 25, 2012
- Marc G. Bellemare, Yavar Naddaf, Joel Veness, Michael Bowling, *The Arcade Learning Environment: An Evaluation Platform for General Agents*, Journal of Artificial Intelligence Research, 2013
- Marc G. Bellemare, Joel Veness, Michael Bowling, *Investigating Contingency Awareness using Atari 2600 Games*, AAAI 2012
- Marc G. Bellemare, Joel Veness, Michael Bowling, *Bayesian learning of recursively factored environments*, ICML 2013
- George E. Dahl, Dong Yu, Li Deng, Alex Acero, *Context-dependent pre-trained deep neural networks for large-vocabulary speech recognition*, IEEE Transactions on Audio, Speech, and Language Processing, 2012
- Alex Graves, Abdel-rahman Mohamed, Geoffrey E. Hinton, *Speech recognition with deep recurrent neural networks*, ICASSP 2013
- Matthew Hausknecht, Risto Miikkulainen, Peter Stone, *A neuro-evolution approach to general Atari game playing*, 2013
- Nicolas Heess, David Silver, Yee Whye Teh, *Actor-critic reinforcement learning with energy-based policies*, European Workshop on Reinforcement Learning, 2012
- Kevin Jarrett, Koray Kavukcuoglu, Marc'Aurelio Ranzato, Yann LeCun, *What is the best multi-stage architecture for object recognition?*, CVPR 2009
- Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton, *ImageNet Classification with Deep Convolutional Neural Networks*, Advances in Neural Information Processing Systems 25, 2012
- Sascha Lange, Martin Riedmiller, *Deep auto-encoder neural networks in reinforcement learning*, IJCNN 2010
- Long-Ji Lin, *Reinforcement learning for robots using neural networks*, technical report, 1993
- Hamid Maei, Csaba Szepesvari, Shalabh Bhatnagar, Doina Precup, David Silver, Rich Sutton, *Convergent Temporal-Difference Learning with Arbitrary Smooth Function Approximation*, Advances in Neural Information Processing Systems 22, 2009
- Hamid Maei, Csaba Szepesvari, Shalabh Bhatnagar, Richard S. Sutton, *Toward off-policy learning control with function approximation*, ICML 2010
- Volodymyr Mnih, *Machine Learning for Aerial Image Labeling*, PhD thesis, University of Toronto, 2013
- Andrew Moore, Chris Atkeson, *Prioritized sweeping: Reinforcement learning with less data and less real time*, Machine Learning, 1993
- Vinod Nair, Geoffrey E. Hinton, *Rectified Linear Units Improve Restricted Boltzmann Machines*, ICML 2010
- Jordan B. Pollack, Alan D. Blair, *Why did TD-Gammon work*, Advances in Neural Information Processing Systems 9, 1996
- Martin Riedmiller, *Neural fitted Q iteration - first experiences with a data efficient neural reinforcement learning method*, ECML 2005
- Brian Sallans, Geoffrey E. Hinton, *Reinforcement learning with factored states and actions*, Journal of Machine Learning Research, 2004
- Pierre Sermanet, Koray Kavukcuoglu, Soumith Chintala, Yann LeCun, *Pedestrian detection with unsupervised multi-stage feature learning*, CVPR 2013
- Richard Sutton, Andrew Barto, *Reinforcement Learning: An Introduction*, MIT Press, 1998
- Gerald Tesauro, *Temporal difference learning and TD-Gammon*, Communications of the ACM, 1995
- John N. Tsitsiklis, Benjamin Van Roy, *An analysis of temporal-difference learning with function approximation*, IEEE Transactions on Automatic Control, 1997
- Christopher J. C. H. Watkins, Peter Dayan, *Q-learning*, Machine Learning, 1992
