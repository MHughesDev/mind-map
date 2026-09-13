# Deep Residual Learning for Image Recognition

**Paper link:** https://openaccess.thecvf.com/content_cvpr_2016/papers/He_Deep_Residual_Learning_CVPR_2016_paper.pdf

---

## **Paper metadata**

**Authors / collaborators:**  
- Kaiming He
- Xiangyu Zhang
- Shaoqing Ren
- Jian Sun

**Organizations / companies / institutions involved:**  
- Microsoft Research

**Publication date:**  
10 December 2015 (arXiv preprint); published at CVPR 2016

**Venue / source:**  
arXiv / Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2016)

**Research paper type / category:**  
- Foundational / landmark paper
- Method / model paper
- Experimental / empirical paper

**Primary field / topic area:**  
Deep convolutional neural networks for computer vision and representation learning

**Keywords:**  
- residual learning
- identity shortcuts
- ResNet
- degradation problem
- bottleneck blocks
- ImageNet

---

## **Opening perspective**

This paper sits at the moment when deep vision models had already proved that depth matters, but the field had run into a stubborn practical ceiling: making convolutional networks deeper did not reliably make them better. The surprise was not just that optimization got harder in some vague way. The surprise was that deeper models could perform worse even on the training set, which means the problem was not ordinary overfitting. That made depth look simultaneously valuable and unreliable.

The paper's contribution is conceptually simple but architecturally decisive. Instead of asking each stack of layers to learn a full transformation from scratch, it asks the stack to learn a residual correction relative to its input, while an identity shortcut carries the input forward unchanged. That shift sounds small, but it changed how very deep networks could be trained. ResNet turned depth from something brittle into something scalable, and the idea spread far beyond image classification into detection, segmentation, transformers, diffusion U-Nets, and many other architectures.

---

## **Full walkthrough and explanation**

**The problem the paper is actually reacting to**

The starting point is the success of deep convolutional models such as AlexNet, VGG, and GoogLeNet. By 2015, it was already clear that deeper hierarchies often produced better visual features. But the paper argues that "just add layers" had stopped being a dependable recipe. Vanishing and exploding gradients had been partially tamed by better initialization and batch normalization, so the usual old story was no longer sufficient. The paper shows a different failure mode: degradation. As depth increases, training accuracy saturates and then gets worse. On CIFAR-10, their plain 56-layer network has higher training and test error than a plain 20-layer network. On ImageNet, a plain 34-layer net also underperforms a plain 18-layer net.

That point matters because, in principle, a deeper model should not be worse than a shallower one if the extra layers can simply learn identity mappings. The authors make this constructive argument explicitly: take a trained shallow network, copy its weights into the corresponding layers of a deeper network, and let the added layers be identity. That deeper network should match the shallow solution. If optimization still fails to find a solution at least that good, then the issue is not lack of representational capacity. It is that the solver is struggling to reach an easy-to-describe solution.

**Residual reformulation and the core block**

The paper's answer is to recast the target mapping. Suppose a few stacked layers are trying to learn an underlying function `H(x)`. Instead of directly fitting `H(x)`, the paper tells the layers to fit a residual function `F(x) := H(x) - x`, so the block outputs `F(x) + x`. The central equations are:

$$
y = F(x, \{W_i\}) + x
$$

and, when dimensions do not match,

$$
y = F(x, \{W_i\}) + W_s x
$$

Here `x` is the block input, `F(x, {W_i})` is the residual mapping produced by the stacked convolutional layers, `y` is the block output, and `W_s` is a projection used only when the shortcut has to change dimension. In the paper's simple two-layer example, the residual branch is essentially two weight layers with a ReLU between them, and the shortcut branch is parameter-free identity whenever possible.

The key intuition is not that identity is always the correct answer. It is that many useful transformations may be easier to learn as deviations from identity than as entirely new mappings. If the best behavior of a block is close to "pass most of the signal through and modify only part of it," then forcing the block to relearn that pass-through behavior from scratch is wasteful. Residual learning makes the easy part explicit.

The block-level pipeline is:

Input `x` -> stacked convolutions compute `F(x)` -> shortcut carries `x` or `W_s x` -> element-wise addition -> ReLU -> output

This is an important historical detail: in this original paper, the addition is followed by a nonlinearity. Later ResNet variants, especially pre-activation ResNets, reorganize normalization and activation for better optimization. So when people say "ResNet block," they often mean a family of descendants, not this exact 2015 arrangement.

**Why the shortcut matters, and how this differs from earlier shortcut ideas**

The shortcut connection is deliberately minimal. Identity shortcuts add neither parameters nor meaningful computation. That matters because the authors want a fair comparison between plain networks and residual networks with essentially the same depth, width, and FLOP budget. If residual nets train better under that constraint, the gain cannot be dismissed as "they just added more capacity."

The paper also situates itself relative to earlier uses of residual ideas and skip connections. It mentions residual encodings in VLAD and Fisher vectors, multigrid-style residual correction in numerical methods, and shortcut-based mechanisms in older neural networks. The most immediate comparison is to highway networks. Highway nets use gated shortcuts, where the gate can close and the layer can revert to a standard nonlinear transform. ResNet's shortcut is different in spirit: the identity path is always open, parameter-free, and always carries information forward. The claim is not merely "skip connections are useful." It is that an always-available identity reference point makes deep optimization easier.

**From plain VGG-style stacks to residual networks**

To make the comparison concrete, the paper builds plain ImageNet baselines that follow VGG-style design rules: mostly `3 x 3` convolutions, same number of filters within a stage, doubled channel count when spatial resolution halves, downsampling by stride-2 convolutions, global average pooling near the end, and a 1000-way fully connected classifier. Their 34-layer plain network has 3.6 billion FLOPs, only about 18% of VGG-19's 19.6 billion FLOPs, so the baseline is already comparatively economical.

The full ImageNet pipeline is:

Image -> `7 x 7` conv, 64, stride 2 -> max pool -> residual stage `conv2_x` -> `conv3_x` -> `conv4_x` -> `conv5_x` -> global average pool -> 1000-way fully connected layer -> class probabilities

For the 18-layer and 34-layer networks, the residual branch uses the simpler two-layer block with two `3 x 3` convolutions. The stage depths are the familiar ResNet counts: `2, 2, 2, 2` blocks for ResNet-18 and `3, 4, 6, 3` blocks for ResNet-34. So the paper is not just inventing a new training trick; it is showing how to retrofit a very standard CNN backbone with shortcut-based residual blocks.

**What happens when dimensions change**

A residual addition requires compatible shapes, so the paper studies three strategies when feature dimensions change between stages.

1. `Option A`: keep the shortcut as identity and use zero-padding to expand dimensions.
2. `Option B`: use projection shortcuts only when dimensions increase.
3. `Option C`: use projection shortcuts for every shortcut.

This comparison is more subtle than many people remember. The main win does not depend on aggressive projection everywhere. All three residual options beat the plain network by a large margin. `Option B` is slightly better than `Option A`, presumably because zero-padded channels in `A` do not receive residual correction, and `Option C` is only marginally better than `B` despite adding more parameters. The paper therefore adopts `B` for deeper ImageNet models, because it captures most of the benefit without needless cost.

That is one of the paper's quiet but important messages: the identity shortcut is not just an aesthetic choice. It is part of the efficiency story.

**Why the paper introduces bottleneck blocks**

For deeper networks such as ResNet-50, ResNet-101, and ResNet-152, the paper switches from the two-layer block to a three-layer bottleneck block:

`1 x 1` reduce dimensions -> `3 x 3` process -> `1 x 1` restore dimensions -> add shortcut -> ReLU

The `1 x 1` convolutions shrink and then expand channel dimension so the expensive `3 x 3` work happens in a narrower space. This is a practical engineering move, not the paper's central conceptual claim. The authors say explicitly that deeper non-bottleneck ResNets also gain from depth, as CIFAR-10 later shows, but bottlenecks make very deep ImageNet models affordable.

The canonical stage layouts are:

- `ResNet-50`: bottleneck blocks arranged as `3, 4, 6, 3`
- `ResNet-101`: bottleneck blocks arranged as `3, 4, 23, 3`
- `ResNet-152`: bottleneck blocks arranged as `3, 8, 36, 3`

Those models have about `3.8`, `7.6`, and `11.3` billion FLOPs respectively. The striking comparison is that ResNet-152 is about eight times deeper than VGG while still having lower complexity than VGG-16 or VGG-19. That is why the paper matters as both an optimization paper and a systems paper: it makes greater depth useful without exploding computation in the same way earlier very deep stacks did.

**Training recipe and what is easy to miss**

The implementation details are not incidental. On ImageNet, the paper follows common large-scale CNN practice: scale augmentation by resizing the shorter side into `[256, 480]`, random `224 x 224` crops and horizontal flips, standard color augmentation, batch normalization after every convolution and before activation, SGD with mini-batch size `256`, momentum `0.9`, weight decay `0.0001`, an initial learning rate of `0.1`, and learning-rate drops by a factor of 10 when error plateaus. The models are trained up to `60 x 10^4` iterations. They do not use dropout, following the batch-normalized Inception-style recipe.

At test time, the comparison studies use standard 10-crop evaluation, while their best results use the fully convolutional test-time form and average predictions across multiple image scales. So the famous leaderboard numbers are not the performance of a bare architectural diagram alone; they are the output of a full training-and-evaluation recipe.

This is also where one should resist a common oversimplification. The paper does not show that residual connections magically solve every optimization problem. It shows that under a concrete modern CNN training pipeline, residual reformulation removes a specific degradation barrier that plain deep networks still suffer from.

**What the ImageNet experiments actually prove**

The ImageNet results are organized to make the causal argument readable. First, plain networks demonstrate the problem. The plain 18-layer model gets `27.94%` top-1 error on the validation set, while the plain 34-layer model gets worse at `28.54%`. That is the degradation effect.

Then the paper applies residual learning to the same baselines. ResNet-18 gets `27.88%` top-1 validation error, similar to the plain 18-layer model, but ResNet-34 improves sharply to `25.03%`. Just as important, the 34-layer ResNet has lower training error than the 18-layer ResNet, reversing the bad pattern seen in the plain networks. The paper treats this as the core evidence that residual learning makes added depth optimizable rather than merely expressive.

The shortcut comparison on the 34-layer model is also revealing. ResNet-34 `A` reaches `25.03 / 7.76` top-1 / top-5 error, `B` reaches `24.52 / 7.46`, and `C` reaches `24.19 / 7.40`. The differences exist, but they are small compared with the jump from the plain network, which is why the paper insists that parameter-heavy projections are not the essence of the result.

Once the authors move to bottleneck models, the gains keep compounding. On the validation set, ResNet-50 gets `22.85 / 6.71`, ResNet-101 gets `21.75 / 6.05`, and ResNet-152 gets `21.43 / 5.71` under 10-crop evaluation. In the stronger single-model comparison, ResNet-152 reaches `19.38%` top-1 and `4.49%` top-5 validation error. That single model already beats the previous ensemble results the paper compares against. Their six-model ensemble reaches `3.57%` top-5 error on the ImageNet test set and wins ILSVRC 2015 classification.

Historically, that last number is easy to quote but slightly distorting if taken alone. The deeper point is not just that a particular ensemble won a benchmark. The deeper point is that residual architecture made it routine to benefit from depths that plain convolutional stacks could not use effectively.

**What CIFAR-10 adds to the argument**

The CIFAR-10 section matters because it shows the phenomenon is not a quirk of one large-scale benchmark. Here the paper uses very simple networks of depth `6n + 2`, with only `3 x 3` convolutions over feature-map sizes `32`, `16`, and `8`, filter counts `16`, `32`, and `64`, and identity shortcuts throughout. This stripped-down setting makes the optimization story cleaner.

As depth increases, plain networks again get worse, while residual networks continue improving. The reported test errors go from `8.75%` at 20 layers to `6.43%` at 110 layers. The 110-layer ResNet is especially important because it shows that the method scales even in deliberately thin networks with far fewer parameters than some competing deep models.

The paper also explores a 1202-layer ResNet. This model has no obvious optimization failure and drives training error below `0.1%`, which is exactly the kind of outcome the paper wants to make possible. But its test error, `7.93%`, is worse than the 110-layer model. The authors interpret this as overfitting on a small dataset, not as a return of the degradation problem. That distinction is important. Residual learning helps train extremely deep networks; it does not guarantee that every additional layer helps generalization.

There is a further analytical claim in this section. The paper measures the standard deviations of layer responses and finds that residual networks tend to have smaller response magnitudes than plain networks, with deeper ResNets often modifying the signal less at each layer. This supports the intuition that residual functions are often closer to zero than full non-residual mappings. But it should be read as suggestive evidence rather than a settled proof of why ResNets work. Later theory and later ResNet variants show that the full explanation is richer than one simple "closer to zero" story.

**Why the paper immediately mattered beyond classification**

The paper does not stop at ImageNet classification. It swaps VGG-16 for ResNet-101 inside Faster R-CNN and reports better detection on both PASCAL VOC and MS COCO using otherwise comparable detection machinery. On VOC 2007 and 2012 test sets, the baseline mAP rises from `73.2 / 70.4` with VGG-16 to `76.4 / 73.8` with ResNet-101. On COCO validation, the standard `mAP@[.5, .95]` metric rises from `21.2` to `27.2`, which the paper describes as a `28%` relative improvement.

This is the section that proves the representation itself is what matters. The architecture was not merely an ImageNet leaderboard trick. The learned features transferred strongly to detection and segmentation, which is one reason ResNet became the default backbone for so many vision systems over the next several years.

**How to read the paper today**

Read carefully, this is both a concrete engineering paper and a conceptual reframing of deep learning. The engineering part is the exact architecture, training schedule, shortcut variants, bottleneck design, and benchmark tables. The conceptual part is the idea that very deep networks can be made trainable by anchoring transformations around identity and learning corrections instead of whole mappings.

Some of the paper's exact implementation choices are no longer the final word. Later ResNet work changes activation placement, identity mapping treatment, and training recipes. Later architectures also reinterpret skip connections in broader ways. But the paper's central insight survives those changes. Modern deep learning repeatedly returns to the same pattern: preserve a strong signal path, make learned branches refine rather than replace it, and let depth accumulate useful incremental changes rather than full rewrites.

---

## **Subtle points, clarifications, and limits**

The paper is sometimes remembered as proving that residual connections solve vanishing gradients. That is not quite its actual argument. The authors go out of their way to say that batch normalization already keeps signals and gradients in workable ranges, and that the remaining issue is degradation: deeper models getting worse training error despite containing a shallower solution in principle. Residual learning is presented as an optimization reformulation, not as a single-cause gradient fix.

It is also easy to overread the 1202-layer CIFAR result. The paper does show that such depth can be optimized, but it also shows that optimization success and generalization success are different questions. Likewise, the response-magnitude analysis supports the residual-preconditioning intuition, but it does not fully explain all later skip-connected networks. The enduring lesson is architectural: identity-preserving pathways make extreme depth usable. The exact mechanism is richer than one slogan.

---

## **Closing perspective**

This paper changed deep learning because it made depth dependable again. After ResNet, adding layers was no longer mainly a gamble that optimization might collapse. It became possible to build models so deep that the network could keep a stable representational backbone while each block learned only what needed to change. That single idea became foundational in modern vision, influenced sequence models and transformers through their own residual paths, and remains one of the clearest examples of a small architectural reformulation having enormous downstream consequences. It has very high standing across computer vision and deep learning more broadly: it is treated as a canonical landmark paper, routinely taught, cited, and built upon by both researchers and practitioners.

---

## **Personal comprehension notes**

The most useful way to think about ResNet is: each block is allowed to say "keep most of what you already have, and I will only add the correction." That is much easier than asking every block to rebuild the whole representation from zero. The shortcut path is the memory of what is already working; the residual branch is the editor, not the entire author.

Another good mental model is that plain deep nets force information to survive a long obstacle course of nonlinear transforms, while ResNets provide a protected highway running alongside the transforms. The learned branch can still do substantial work, but it no longer has to preserve signal and invent new structure at the same time.

A third way to remember the architecture is by its stage pattern. Spatial resolution keeps shrinking, channel count keeps growing, and each stage is a stack of small corrective blocks. In shallow ResNets those blocks are two `3 x 3` convolutions; in deeper ones they are bottlenecks that squeeze -> process -> expand. But the recurring idea is the same in every case: identity path plus correction path.

---

## **Compact retention notes**

- **Paper type:** Foundational / landmark method paper
- **Core idea:** Recast deep convolutional blocks as residual corrections around identity shortcuts so much deeper networks become trainable and useful.
- **Main mechanism:** Learn `F(x)` on a residual branch, add it to `x` or `W_s x`, and stack those blocks into very deep CNNs, using bottlenecks for efficient 50/101/152-layer models.
- **Key result:** ResNet eliminates the degradation pattern of plain deep CNNs, wins ILSVRC 2015 with `3.57%` top-5 test error as an ensemble, and improves transfer to detection.
- **Main limitation:** Residual connections make depth trainable, but they do not guarantee better generalization at arbitrary depth, as the 1202-layer CIFAR result shows.

---

## **Citations used in the paper**

- Alex Krizhevsky, Ilya Sutskever, Geoffrey Hinton, *ImageNet Classification with Deep Convolutional Neural Networks*, NeurIPS 2012
- Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun, *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification*, ICCV 2015
- Sergey Ioffe, Christian Szegedy, *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift*, ICML 2015
- Karen Simonyan, Andrew Zisserman, *Very Deep Convolutional Networks for Large-Scale Image Recognition*, ICLR 2015
- Christian Szegedy et al., *Going Deeper with Convolutions*, CVPR 2015
- Rupesh Kumar Srivastava, Klaus Greff, Jurgen Schmidhuber, *Highway Networks*, 2015
- Shaoqing Ren, Kaiming He, Ross Girshick, Jian Sun, *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*, NeurIPS 2015
- Olga Russakovsky et al., *ImageNet Large Scale Visual Recognition Challenge*, 2014
- Alex Krizhevsky, *Learning Multiple Layers of Features from Tiny Images*, 2009 - source of the CIFAR-10 dataset used for the depth analysis
- Tsung-Yi Lin et al., *Microsoft COCO: Common Objects in Context*, ECCV 2014
- Marc Everingham et al., *The Pascal Visual Object Classes (VOC) Challenge*, IJCV 2010
- William L. Briggs, Van Emden Henson, Steve McCormick, *A Multigrid Tutorial*, 2000 - cited as an analogy for residual correction in numerical optimization
