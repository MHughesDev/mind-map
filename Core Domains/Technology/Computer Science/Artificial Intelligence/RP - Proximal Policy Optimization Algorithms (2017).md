# Proximal Policy Optimization Algorithms

**Paper link:** https://arxiv.org/abs/1707.06347

---

## **Paper metadata**

**Authors / collaborators:**  
- John Schulman  
- Filip Wolski  
- Prafulla Dhariwal  
- Alec Radford  
- Oleg Klimov

**Organizations / companies / institutions involved:**  
- OpenAI

**Publication date:**  
2017 (arXiv preprint posted July 2017)

**Venue / source:**  
arXiv (cs.LG)

**Research paper type / category:**  
- Method / model paper  
- Experimental / empirical paper  
- Systems / engineering paper

**Primary field / topic area:**  
Deep reinforcement learning, on-policy policy optimization

**Keywords:**  
- proximal policy optimization (PPO)  
- clipped surrogate objective  
- trust-region methods  
- policy gradient  
- generalized advantage estimation (GAE)

---

## **Opening perspective**

By 2017, deep reinforcement learning already had two competing realities: we had policy-gradient methods that were elegant but fragile, and we had trust-region methods like TRPO that were substantially more stable but operationally awkward. PPO lands exactly in that gap. It takes the core trust-region intuition ("do not move the policy too far in one update") and turns it into an optimization objective that can be run with ordinary first-order tools and minibatch SGD. That one design decision is why PPO became a workhorse: it trades some of TRPO's theoretical strictness for dramatically better day-to-day usability without collapsing performance.

---

## **Full walkthrough and explanation**

**Why TRPO created pressure for a simpler method**

The immediate ancestor of PPO is TRPO. TRPO frames policy improvement as a constrained optimization problem: improve expected return, but keep the KL divergence between old and new policy below a bound. This gives a monotonic improvement argument under assumptions, and in practice it often stabilizes training compared with naive policy gradient updates. The problem is that implementing TRPO means dealing with conjugate-gradient style machinery, Hessian-vector products, and line-search logic. For many practitioners this increased complexity became a practical bottleneck.

PPO starts from a pragmatic premise: keep the "small, conservative update" behavior, but encode it in an objective that works with simple gradient ascent on minibatches. That is a change in engineering philosophy as much as a change in math.

**Core object: the probability ratio**

PPO uses the policy ratio

$$
r_t(\theta) = \frac{\pi_{\theta}(a_t \mid s_t)}{\pi_{\theta_{\text{old}}}(a_t \mid s_t)}.
$$

This ratio says how much more or less likely the new policy makes the sampled action compared with the old policy at timestep \(t\). If \(r_t(\theta) > 1\), the new policy increases that action's probability; if \(r_t(\theta) < 1\), it decreases it.

The policy-gradient style surrogate is then built around \(r_t(\theta)\hat{A}_t\), where \(\hat{A}_t\) is the estimated advantage. Positive advantage means "increase this action probability"; negative advantage means "decrease it."

**Clipped surrogate: the central PPO idea**

The clipped PPO objective is:

$$
L^{\text{CLIP}}(\theta) =
\hat{\mathbb{E}}_t\left[
\min\left(
r_t(\theta)\hat{A}_t,\;
\text{clip}\big(r_t(\theta), 1-\epsilon, 1+\epsilon\big)\hat{A}_t
\right)
\right].
$$

What this does is subtle and important. The unclipped term tries to improve the policy as usual. The clipped term cuts off the incentive once \(r_t(\theta)\) moves outside \([1-\epsilon, 1+\epsilon]\). The min operator chooses the pessimistic bound so optimization cannot gain extra objective value by pushing the ratio too far beyond the trust region proxy.

Intuition by sign:
- If \(\hat{A}_t > 0\), increasing \(r_t\) is good only until approximately \(1+\epsilon\); after that, extra increase is not rewarded.
- If \(\hat{A}_t < 0\), decreasing \(r_t\) is good only until approximately \(1-\epsilon\); after that, extra decrease is not rewarded.

So PPO does not hard-constrain KL the way TRPO does, but it makes large policy changes locally unattractive in the objective itself. This is why people often call it a "soft trust-region-like" method.

**Alternative PPO variant: KL penalty**

The paper also discusses a KL-penalty form where the objective includes a KL divergence penalty with an adaptive coefficient:

Policy surrogate \(\rightarrow\) subtract \(\beta \cdot \text{KL}(\pi_{\theta_{\text{old}}}, \pi_\theta)\),

and \(\beta\) is adjusted depending on whether observed KL is above or below a target. This variant is conceptually closer to TRPO's KL control, but in practice the clipped objective became the dominant form because it was simpler and often more robust to tuning in common implementations.

**How the full PPO training loop actually runs**

The operational pipeline is:

Environment interaction under \(\pi_{\theta_{\text{old}}}\) -> trajectory batch collection -> compute returns and advantages (often GAE) -> optimize clipped surrogate for multiple epochs over minibatches -> update value function (and often entropy bonus term) -> set \(\theta_{\text{old}} \leftarrow \theta\) -> repeat

Two details are central to why PPO works in practice:
1. **Multiple epochs on the same on-policy batch.** Vanilla policy gradient often uses each sample once; PPO reuses samples several times with clipping as a guardrail.
2. **Joint actor-critic training setup.** Most implementations optimize a combined loss with policy objective, value loss, and entropy regularization, even if the paper presents components separately.

This gives a high "stability per implementation complexity" ratio, which is arguably PPO's real contribution.

**Where advantage estimation fits**

PPO itself is a policy objective; it still depends heavily on the quality and variance of \(\hat{A}_t\). In the paper and standard practice, \(\hat{A}_t\) is commonly estimated with Generalized Advantage Estimation (GAE), which introduces a bias-variance tradeoff via \(\lambda\). This means PPO's behavior is partly an interaction between clipping and GAE smoothness, not clipping alone.

So when practitioners say "PPO is stable," they are often describing a package:
- clipped policy objective,
- actor-critic baseline,
- GAE advantages,
- normalization/scaling choices,
- and careful batch/epoch/horizon configuration.

**What experiments in the paper show**

The paper evaluates PPO on continuous-control benchmarks (including MuJoCo-style locomotion) and Atari settings. The empirical message is not "PPO strictly dominates every method everywhere." The stronger claim is:
- PPO is competitive with strong baselines (including TRPO variants and A2C/A3C-style methods in relevant setups),
- while being much easier to implement and run.

That framing matters. PPO was not sold as a theoretically perfect replacement; it was sold as the best practical tradeoff for many users.

**Important nuance: what clipping does not guarantee**

A common misunderstanding is that clipping guarantees monotonic policy improvement. It does not. Unlike TRPO's constrained step with supporting theory, PPO's clipped objective is a heuristic lower-bound style stabilizer. It reduces destructive updates but does not fully prevent them. Large performance drops can still happen with poor hyperparameters, bad reward scaling, unstable value targets, or problematic environment stochasticity.

Another frequent overreach is "PPO is sample efficient." Relative to many on-policy alternatives, it can be efficient enough to be practical due to minibatch reuse. But relative to strong off-policy methods (in settings where replay and bootstrapping work well), PPO is often sample-hungry.

**Why this became foundational beyond benchmark RL**

PPO's influence extended into human-feedback training pipelines for language models, where on-policy updates and regularization against over-updating the policy are key concerns. RLHF implementations are not a copy-paste of 2017 PPO, but the clipped-ratio logic and trust-region-like caution are directly in the family. Historically, this paper gave the field a robust "default optimizer mindset" for policy updates.

---

## **Subtle points, clarifications, and limits**

Clipping stabilizes incentives, not dynamics in a strict control-theoretic sense. If value estimates drift, reward scales change sharply, or rollout data are too narrow, optimization can still become erratic even when the clipped loss looks well-behaved. Also, \(\epsilon\) is not universally transferable: larger action spaces, sparse rewards, and different horizon lengths can require materially different clipping and epoch choices. Finally, PPO's broad adoption sometimes hides that many "PPO results" rely on implementation details outside the original core objective, such as observation normalization, reward clipping, advantage normalization, and tuned entropy schedules.

---

## **Closing perspective**

PPO earned durable respect because it converted an important but operationally heavy idea (trust-region caution) into a method most teams could implement quickly and debug reliably. It did not end policy optimization research, and it is not the final word on sample efficiency or theoretical guarantees, but it reset the practical baseline for deep RL and later influenced large-scale preference optimization pipelines. The paper is highly respected in both academic RL and industry engineering circles precisely because it balanced conceptual soundness with real-world usability.

---

## **Personal comprehension notes**

The mental model I keep is: PPO places a "friction band" around policy change. Inside the band, normal policy-gradient pressure pushes probabilities according to advantage. Outside the band, extra pressure mostly stops paying off. So rather than hard-braking each update with constrained optimization, PPO reshapes the reward landscape so over-aggressive updates become less attractive.

Another useful way to think about it: TRPO says "solve a constrained problem correctly"; PPO says "solve an easier unconstrained problem whose objective already encodes caution." This is why PPO became the default in codebases: the second strategy is easier to scale in day-to-day experimentation.

For memory, I compress PPO as:
old policy snapshots + advantage-weighted ratio + clipping guardrail + multiple minibatch epochs on fresh rollouts.

---

## **Compact retention notes**

- **Paper type:** Practical policy optimization method paper (with benchmark evidence)  
- **Core idea:** Use a clipped probability-ratio surrogate to prevent overly large policy updates  
- **Main mechanism:** Maximize \( \min(r_t\hat{A}_t,\text{clip}(r_t,1-\epsilon,1+\epsilon)\hat{A}_t) \) over minibatches and epochs  
- **Key result:** TRPO-level practical stability with much simpler first-order implementation and strong benchmark competitiveness  
- **Main limitation:** Still on-policy and hyperparameter-sensitive; clipping is a heuristic stabilizer, not a strict monotonic-improvement guarantee

---

## **Citations used in the paper**

- Schulman et al., *Trust Region Policy Optimization*, 2015  
- Schulman et al., *High-Dimensional Continuous Control Using Generalized Advantage Estimation*, 2016  
- Mnih et al., *Asynchronous Methods for Deep Reinforcement Learning*, 2016  
- Lillicrap et al., *Continuous Control with Deep Reinforcement Learning*, 2015  
- Kingma and Ba, *Adam: A Method for Stochastic Optimization*, 2014 — optimizer widely used in PPO training setups

---
