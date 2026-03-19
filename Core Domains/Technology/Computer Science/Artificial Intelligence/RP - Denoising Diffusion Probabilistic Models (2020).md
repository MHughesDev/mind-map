# Denoising Diffusion Probabilistic Models

**Paper link:** https://arxiv.org/pdf/2006.11239.pdf

---

## **Paper metadata**

**Authors / collaborators:**
- Jonathan Ho
- Ajay Jain
- Pieter Abbeel

**Organizations / companies / institutions involved:**
- University of California, Berkeley

**Publication date:**
19 June 2020 (arXiv preprint); later published at NeurIPS 2020

**Venue / source:**
NeurIPS 2020 / arXiv

**Research paper type / category:**
- Foundational / landmark paper
- Method / model paper
- Experimental / empirical paper

**Primary field / topic area:**
Generative modeling, diffusion-based image synthesis, and likelihood-based probabilistic modeling

**Keywords:**
- diffusion probabilistic models
- denoising score matching
- Langevin dynamics
- variational inference
- image generation

---

## **Opening perspective**

This paper sits at a turning point in generative modeling. Before it, diffusion models already existed in a serious probabilistic form, especially through the 2015 work of Sohl-Dickstein and colleagues, but they were not yet the model family people pointed to when they wanted top-tier image samples. The main conversation in practice was split across GANs for visual sharpness, autoregressive models for exact likelihoods, flows for tractable densities, and VAEs for latent-variable structure. Ho, Jain, and Abbeel take a model class that looked elegant but peripheral and show that, with the right parameterization and objective, it can generate images good enough to compete with the strongest generators of the time.

What makes the paper important is not only the headline FID score. It also reorganizes several lines of thought that had been developing somewhat separately: diffusion, denoising autoencoders, score matching, annealed Langevin dynamics, variational inference, and progressive lossy compression. The paper teaches you to think of generation not as one giant leap from latent code to image, but as a long chain of small denoising decisions. That change in viewpoint is why DDPM became the conceptual starting point for the later diffusion era, even though many later systems changed the sampler, training target, and conditioning mechanisms.

---

## **Full walkthrough and explanation**

**What kind of generative model this is**

A diffusion probabilistic model is a latent-variable model in which the latent variables are not a single compressed code but an entire sequence of progressively corrupted versions of the data. If the clean image is `x_0`, then the model introduces `x_1, x_2, ..., x_T`, where every `x_t` has the same dimensionality as the image. The forward chain is fixed and slowly destroys information; the reverse chain is learned and slowly reconstructs it.

The overall pipeline is:

Clean image `x_0` -> repeated Gaussian corruption -> nearly pure noise `x_T` -> learned reverse denoising steps -> generated image `x_0`

That decomposition is the heart of the method. Instead of demanding that a model learn a direct jump from a latent vector to a full image, the paper turns generation into a sequence of easier local problems. The network only needs to answer questions of the form: "given an image corrupted to a known noise level, what should one reverse step look like?" Much of the method's strength comes from that inductive bias.

It is also important to state a historical correction early: this paper did not invent diffusion models from nothing. The basic diffusion-model framework comes from Sohl-Dickstein et al. (2015). What DDPM contributes is the parameterization and training recipe that made the family empirically competitive and conceptually central.

**The forward process: how the image is destroyed**

The forward process, written `q(x_{1:T} | x_0)`, is a fixed Markov chain that adds Gaussian noise in small increments:

$$
q(x_{1:T} | x_0) = \prod_{t=1}^T q(x_t | x_{t-1}), \quad
q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1-\beta_t} x_{t-1}, \beta_t I)
$$

The symbols matter:
- `x_0` is the clean image from the data distribution.
- `x_t` is the partially corrupted image after `t` noising steps.
- `T` is the total number of diffusion steps.
- `\beta_t` is the variance schedule that controls how much noise is added at step `t`.
- `I` is the identity covariance, so the added noise is isotropic Gaussian noise.

The authors use `T = 1000` and a linearly increasing variance schedule from `\beta_1 = 10^{-4}` to `\beta_T = 0.02`. The choice is deliberately conservative: the noise increments are small enough that the reverse process can also be modeled well by Gaussians.

Because this chain is linear Gaussian, the paper can jump directly from `x_0` to any `x_t` without simulating every intermediate step. Defining `\alpha_t := 1 - \beta_t` and `\bar{\alpha}_t := \prod_{s=1}^t \alpha_s`, they get

$$
q(x_t | x_0) = \mathcal{N}(x_t; \sqrt{\bar{\alpha}_t} x_0, (1 - \bar{\alpha}_t) I)
$$

This equation is one of the practical keys to diffusion training. If `\epsilon ~ \mathcal{N}(0, I)`, then a noisy sample at any timestep can be written directly as

$$
x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon
$$

So the training pipeline becomes:

Sample clean image `x_0` -> sample timestep `t` -> sample Gaussian noise `\epsilon` -> construct `x_t` in closed form -> train the network at that noise scale

That is why diffusion models remain trainable even when the generative chain is very long. You do not need to simulate the entire forward process during training.

**The reverse process: how generation is defined**

The learned model runs a reverse Markov chain from noise back to data:

$$
p_\theta(x_{0:T}) = p(x_T) \prod_{t=1}^T p_\theta(x_{t-1} | x_t), \quad
p_\theta(x_{t-1} | x_t) = \mathcal{N}(x_{t-1}; \mu_\theta(x_t, t), \Sigma_\theta(x_t, t))
$$

The chain starts at `p(x_T) = \mathcal{N}(0, I)` because after enough forward noising the data is nearly standard Gaussian. Sampling then means repeatedly applying learned reverse transitions:

`x_T ~ N(0, I)` -> predict reverse-step statistics at time `T` -> sample `x_{T-1}` -> predict reverse-step statistics at time `T-1` -> ... -> produce `x_0`

At first glance this looks like a standard latent-variable model with many latents, but the fixed forward process gives it unusual structure. The paper can derive the exact forward posterior

$$
q(x_{t-1} | x_t, x_0) = \mathcal{N}(x_{t-1}; \tilde{\mu}_t(x_t, x_0), \tilde{\beta}_t I)
$$

Because the posterior is tractable, each reverse step can be trained by matching a learned Gaussian to a known Gaussian target. That turns the overall learning problem into a sequence of local distribution-matching problems instead of a vague end-to-end "make samples look real" objective.

The authors also make an important simplifying choice: rather than learning a full reverse covariance, they set `\Sigma_\theta(x_t, t) = \sigma_t^2 I` to fixed time-dependent constants. They report that fixed variances are simpler and give better behavior than learned diagonal variances in the settings they test. This is one of the paper's recurring themes: restrained parameterization beats unnecessary flexibility.

**The variational bound and why denoising becomes the learning problem**

Training begins from the standard variational upper bound on negative log-likelihood. After rearrangement, the objective decomposes into a sum of terms comparing the learned reverse process to the tractable forward posterior at every timestep. In other words, the model learns by becoming good at each local reverse move.

This is the point where the paper stops being merely a probabilistic model definition and becomes an actual practical training recipe. The reverse process is not learned as a mysterious black box. It is trained through a ladder of KL terms, each one asking whether the reverse transition at noise level `t` behaves like the correct posterior transition implied by the forward process.

The paper also fixes the forward variances `\beta_t` rather than learning them. Once that choice is made, the `L_T` term in the bound becomes constant during training and can be ignored. That removes complexity without materially hurting the main result.

**Why predicting noise is the decisive parameterization**

A naive reading of the variational objective suggests predicting the posterior mean `\tilde{\mu}_t(x_t, x_0)` directly. The paper shows that a better parameterization is to predict the Gaussian noise `\epsilon` used to create `x_t`. Using the reparameterization above, the reverse mean can be written as

$$
\mu_\theta(x_t, t) =
\frac{1}{\sqrt{\alpha_t}}
\left(
x_t -
\frac{\beta_t}{\sqrt{1-\bar{\alpha}_t}}
\epsilon_\theta(x_t, t)
\right)
$$

Here `\epsilon_\theta(x_t, t)` is the neural network's prediction of the noise component inside `x_t`. The practical meaning is simple: the model looks at a noisy image and tries to infer what random noise was added to it. Once it knows that, it can estimate the clean direction hidden inside the noisy observation.

That parameterization is not just cosmetic. It turns the reverse-step objective into something that resembles denoising score matching:

$$
\mathbb{E}_{x_0, \epsilon}
\left[
\frac{\beta_t^2}{2 \sigma_t^2 \alpha_t (1-\bar{\alpha}_t)}
\|
\epsilon - \epsilon_\theta(x_t, t)
\|^2
\right]
$$

This is one of the paper's main conceptual contributions. It shows that variational inference for a finite-time diffusion model can be rewritten in a form that closely resembles multi-noise-level denoising score matching, while the reverse sampling procedure resembles annealed Langevin dynamics. That bridge between traditions is why DDPM sits so naturally between probabilistic modeling and score-based generative modeling.

The corresponding reverse update becomes

$$
x_{t-1} =
\frac{1}{\sqrt{\alpha_t}}
\left(
x_t -
\frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}}
\epsilon_\theta(x_t, t)
\right)
+ \sigma_t z
$$

with `z ~ \mathcal{N}(0, I)` for `t > 1`. In words: estimate the noise in `x_t`, subtract the appropriate amount, then inject the amount of randomness required by the reverse conditional. This is what makes DDPM sampling look like iterative denoising guided by a learned score-like field.

**Why the simplified objective produces the best samples**

After deriving the weighted form above, the paper makes another crucial move: it drops the timestep-dependent weighting and trains with the simpler objective

$$
L_{\text{simple}}(\theta) =
\mathbb{E}_{t, x_0, \epsilon}
\left[
\|
\epsilon - \epsilon_\theta(\sqrt{\bar{\alpha}_t} x_0 + \sqrt{1-\bar{\alpha}_t} \epsilon, t)
\|^2
\right]
$$

This yields the training loop shown in the paper:

Sample `x_0` -> sample `t` uniformly from `{1, ..., T}` -> sample `\epsilon ~ N(0, I)` -> build `x_t` -> predict `\epsilon` -> minimize mean squared error

This objective is simpler than the literal variational bound, and in the paper it gives substantially better sample quality. That tradeoff is extremely important. DDPM is not claiming that the cleanest theoretical objective is automatically the best engineering objective. In fact, the paper explicitly reports that training on the true variational bound yields better codelengths, while `L_simple` yields the best images.

The authors' explanation is intuitive and important: the simplified objective effectively down-weights very small-noise denoising tasks, which are easy and otherwise consume too much attention. That lets the model spend more learning capacity on harder, higher-noise denoising problems that matter more for perceptual sample quality.

**Discrete data, decoder design, and what likelihood means here**

The paper works with image data whose integer pixel values are scaled linearly to `[-1, 1]`. To obtain a true discrete log-likelihood rather than an informal continuous density, the final reverse step uses a discrete decoder derived from a Gaussian around `\mu_\theta(x_1, 1)`. This is a subtle but meaningful modeling choice. It means the paper is not only saying "look at these samples." It is defining a proper generative model of discrete images and evaluating bits per dimension.

At the same time, the authors are unusually clear about the limitations of those likelihood results. Their diffusion models do not have competitive log-likelihoods compared with the best likelihood-based image models of that period. That is not a minor footnote. It is central to how the paper should be understood. DDPM achieves strong perceptual generation not because it is the best lossless compressor, but because its inductive bias allocates modeling power toward visually meaningful structure.

This is why the paper later interprets the method through rate-distortion language. A large fraction of the lossless codelength is spent on details humans barely notice. So diffusion can be weak as a lossless code yet excellent as a lossy compressor and sample generator.

**Architecture and training recipe**

The reverse model is a U-Net-like convolutional network, described as similar to an unmasked PixelCNN++ backbone, with group normalization throughout. Parameters are shared across timesteps, and the timestep information is injected via sinusoidal embeddings of the kind popularized by the Transformer literature. The model also uses self-attention at the `16 x 16` feature-map resolution.

The architecture pipeline is roughly:

Noisy image `x_t` + sinusoidal time embedding -> U-Net-style convolutional denoiser -> self-attention at `16 x 16` resolution -> predicted noise `\epsilon_\theta(x_t, t)`

This detail matters historically because the paper's breakthrough is not "a new image backbone." The backbone is practical and strong, but the real innovation is the noise-conditioned reverse process plus the objective that trains it.

The main settings are part of the result:
- `T = 1000`
- linear `\beta_t` schedule from `10^{-4}` to `0.02`
- fixed reverse variances
- time-conditioned shared network across all timesteps
- image values scaled to `[-1, 1]`

Those choices also reveal one of the paper's biggest practical limitations: sampling is slow, because generating one image requires roughly one network evaluation per reverse step.

**What the experiments actually show**

On unconditional CIFAR-10, the best model trained with `L_simple` reaches an Inception Score of `9.46` and an FID of `3.17`, which the paper presents as state of the art for unconditional CIFAR-10 at the time. The paper also notes that the test-set FID is `5.24`, still strong but worse than the training-set FID used in most literature comparisons. That detail matters because FID reporting conventions are often slippery.

The ablation results are especially revealing. The paper compares:
- predicting `\tilde{\mu}` versus predicting `\epsilon`
- fixed isotropic reverse variance versus learned diagonal variance
- true variational-bound training versus the simplified MSE objective

The winning recipe is not "anything diffusion-like." The best samples come from `\epsilon`-prediction with fixed variances and the simplified objective. Learned reverse variances are unstable in their experiments, and direct `\tilde{\mu}` prediction is not as effective under the simple loss. This is why the DDPM recipe looks the way it does.

On `256 x 256` LSUN Church and Bedroom, the paper reports image quality comparable to ProgressiveGAN, with figure captions giving FIDs of `7.89` for Church and `4.90` for Bedroom. That matters because it shows the method is not only a CIFAR-10 toy success.

The paper also highlights a split between sample quality and codelength quality. Models trained on the true variational bound achieve better NLL than those trained on `L_simple`, but they do not produce the best-looking samples. This is already a preview of a theme that continued throughout later diffusion work: the best perceptual generator is not always the model that most tightly optimizes exact likelihood.

**Progressive coding, reconstruction, and generalized autoregressive thinking**

One of the most original parts of the paper is its interpretation of the diffusion chain as a progressive lossy code. Because the variational objective decomposes over timesteps, the model can be read as revealing information gradually. If a receiver has access to `x_t`, the paper gives a natural estimate of the clean image:

$$
\hat{x}_0 =
\frac{x_t - \sqrt{1-\bar{\alpha}_t}\,\epsilon_\theta(x_t, t)}{\sqrt{\bar{\alpha}_t}}
$$

This reconstruction pipeline is:

Partial noisy state `x_t` -> predict noise content -> estimate clean image `\hat{x}_0`

As reverse diffusion proceeds, large-scale structure emerges first and fine detail arrives later. That is why progressive DDPM generations look coarse-to-fine rather than all-at-once. The paper interprets this through rate-distortion analysis and shows that much of the transmitted information goes toward details that are visually minor.

The paper also makes a clever conceptual argument that diffusion can be interpreted as a generalized form of autoregressive decoding. If one designs a very particular diffusion that masks coordinates one by one, the variational objective reduces to autoregressive prediction. The Gaussian diffusion used in DDPM is not ordinary autoregression, but it can be seen as an information-revealing process with a much richer ordering than a fixed pixel sequence. That is an interpretation, not a proof that diffusion dominates autoregressive models on every axis, but it is a powerful lens for understanding why the method refines global structure before local detail.

**Interpolation and latent structure**

The interpolation experiments are not just decorative figures. The paper encodes two source images into noisy latents at the same timestep, linearly interpolates between those latents, and then decodes with the reverse process. At around `t = 500`, this yields reconstructions and smooth semantic interpolations in CelebA-HQ across pose, skin tone, hairstyle, expression, and background, with larger `t` values producing coarser, more varied interpolations.

The important conceptual point is that high-noise latents preserve large-scale attributes while discarding fine details. Samples generated from the same latent `x_t` can share high-level structure such as pose or eyewear. This suggests that the diffusion latents are not merely arbitrary corruptions; they organize semantic information by scale.

**How to read the paper from today's perspective**

From today's standpoint, DDPM is both narrower and more foundational than people sometimes remember. It is narrower because it is about unconditional image generation with a slow 1000-step Gaussian reverse chain and a U-Net-style denoiser. It does not yet include classifier guidance, text conditioning, latent diffusion, distillation, or the later SDE and probability-flow reformulations that unified many score-based methods.

But it is foundational because the central decomposition survives nearly all later developments: start from data, corrupt it gradually, train a model that knows how to denoise at many scales, and sample by walking backward through those scales. The paper also gets something deep and still relevant exactly right: diffusion's strength is not simply "better likelihood" or "more realistic samples" in isolation. Its strength is an inductive bias that reconstructs perceptually meaningful structure in a staged, stable, and controllable way.

---

## **Subtle points, clarifications, and limits**

The paper is easy to overread as proving that diffusion models are generally superior to GANs or to all other likelihood-based models. It does not do that. Its strongest demonstration is that diffusion models can produce excellent image samples with stable training and a principled probabilistic story. Its own lossless likelihood results are explicitly not competitive with the best likelihood-based generators of that moment.

It is also easy to mistake `\epsilon`-prediction for the one true diffusion target. In this paper it is the most effective parameterization they found, not a universal law. Later work explores `x_0`-prediction, `v`-prediction, learned variances, different schedules, and far faster samplers. The durable contribution is the denoising-chain viewpoint and the bridge to score-based modeling, not a frozen 2020 implementation checklist.

---

## **Closing perspective**

This paper changed generative modeling by taking a once-niche probabilistic construction and turning it into a practical, high-performance design pattern. DDPM made iterative denoising feel concrete, trainable, and empirically serious. It connected diffusion models to score matching, Langevin-like sampling, progressive compression, and a generalized autoregressive interpretation, while producing image quality strong enough to force the field to pay attention. That is why the paper now carries landmark status: much of modern image generation, and a large share of later score-based generative modeling, is either a direct extension of this paper or a response to its limitations.

---

## **Personal comprehension notes**

The best memory hook is: "hide the image under noise slowly, then learn the exact style of undoing that hiding." The model is not trying to imagine a whole image in one shot. It is trying to become very good at a narrower skill: given a noisy image and a timestamp, tell me what noise is inside it. If you can do that at every scale, then generation is just repeated cleanup from pure noise back to structure.

Another useful mental model is coarse-to-fine restoration. High noise levels preserve only big visual facts, so early reverse steps recover layout, pose, broad color regions, and global composition. Later steps fill in hair strands, edges, textures, and small details. That is why diffusion samples often feel like an image gradually coming into focus rather than a latent code suddenly unfolding.

A third way to remember the paper is as a bridge between research traditions. It keeps the formal language of latent-variable modeling and variational bounds, but the practical training rule looks like denoising score matching. So DDPM is not just a good generative model. It is a translation layer between probabilistic modeling, energy-based intuition, and modern image synthesis practice.

---

## **Compact retention notes**

- **Paper type:** Foundational method paper in generative modeling
- **Core idea:** Learn to reverse a fixed Gaussian noising process by predicting the noise present at many timesteps.
- **Main mechanism:** Sample a noisy `x_t`, predict `\epsilon`, convert that prediction into the reverse Gaussian mean, and iterate from `x_T ~ N(0, I)` back to `x_0`.
- **Key result:** DDPM reaches state-of-the-art unconditional CIFAR-10 FID (`3.17`) and strong `256 x 256` LSUN results while tying diffusion to score matching and progressive compression.
- **Main limitation:** Sampling is slow because it requires many reverse steps, and the best sample-quality objective is not the best likelihood objective.

---

## **Citations used in the paper**

- Jascha Sohl-Dickstein, Eric Weiss, Niru Maheswaranathan, Surya Ganguli, *Deep Unsupervised Learning Using Nonequilibrium Thermodynamics*, 2015
- Yang Song, Stefano Ermon, *Generative Modeling by Estimating Gradients of the Data Distribution*, 2019
- Yang Song, Stefano Ermon, *Improved Techniques for Training Score-Based Generative Models*, 2020
- Pascal Vincent, *A Connection Between Score Matching and Denoising Autoencoders*, 2011
- Tim Salimans, Andrej Karpathy, Xi Chen, Diederik P. Kingma, *PixelCNN++: Improving the PixelCNN with Discretized Logistic Mixture Likelihood and Other Modifications*, 2017
- Olaf Ronneberger, Philipp Fischer, Thomas Brox, *U-Net: Convolutional Networks for Biomedical Image Segmentation*, 2015
- Yuxin Wu, Kaiming He, *Group Normalization*, 2018
- Ashish Vaswani et al., *Attention Is All You Need*, 2017 - used for the sinusoidal timestep embedding
- Karol Gregor et al., *Towards Conceptual Compression*, 2016 - relevant to the paper's progressive lossy compression perspective
- Andrew Brock, Jeff Donahue, Karen Simonyan, *Large Scale GAN Training for High Fidelity Natural Image Synthesis*, 2019
- Tero Karras et al., *Training Generative Adversarial Networks with Limited Data*, 2020
- Yilun Du, Igor Mordatch, *Implicit Generation and Modeling with Energy Based Models*, 2019
