# Going Deeper with Convolutions

**Paper link:** https://arxiv.org/pdf/1409.4842.pdf

---

## **Paper metadata**

**Authors / collaborators:**  
- Christian Szegedy
- Wei Liu
- Yangqing Jia
- Pierre Sermanet
- Scott Reed
- Dragomir Anguelov
- Dumitru Erhan
- Vincent Vanhoucke
- Andrew Rabinovich

**Organizations / companies / institutions involved:**  
- Google Inc.
- University of North Carolina at Chapel Hill
- University of Michigan at Ann Arbor
- Magic Leap Inc.

**Publication date:**  
17 September 2014 as an arXiv preprint; later published in June 2015 at CVPR

**Venue / source:**  
CVPR 2015 / arXiv preprint

**Research paper type / category:**  
- Foundational / landmark paper
- Method / model paper
- Experimental / empirical paper
- Systems / engineering paper

**Primary field / topic area:**  
Computer vision, convolutional neural network architecture design, and compute-efficient deep learning

**Keywords:**  
- Inception
- GoogLeNet
- convolutional neural networks
- multi-scale processing
- 1x1 convolutions
- ImageNet
- object detection

---

## **Opening perspective**

This paper comes from the period when modern computer vision was being transformed by deep convolutional networks, but the field still mostly knew one reliable move: make the network bigger. More layers, more filters, more parameters, more compute. "Going Deeper with Convolutions" matters because it pushes against that brute-force instinct. Its real contribution is not just another winning ImageNet model. It is a new design philosophy for how to spend computation inside a network so that depth and width increase in a more structured, more efficient way.

That is why the paper still feels important even though later architectures would outperform it. It introduced the Inception idea: at a given stage of a vision model, different spatial scales may all matter, so the network should examine them in parallel rather than committing to one filter size everywhere. But the paper is equally about engineering reality. The authors are trying to approximate the benefits of sparse, multi-scale structure while still using the dense convolution operations that existing hardware and software libraries could execute efficiently. That combination of architectural imagination and computational pragmatism is what made GoogLeNet historically decisive.

---

## **Full walkthrough and explanation**

**What problem the paper is actually reacting to**

The paper opens from the observation that recent progress in object classification and detection had come from better ideas and better architectures, not merely from larger datasets or stronger hardware. AlexNet had already shown that large CNNs could dominate ImageNet, and subsequent systems kept pushing scale upward. But scaling everything uniformly creates two related problems. First, more parameters increase overfitting risk, especially when strong labels are expensive to collect for fine-grained categories. Second, computation grows very quickly, and in convolutional stacks it can grow almost quadratically when adjacent layers are both widened.

The authors are especially explicit that accuracy is not their only objective. They repeatedly frame the network as something that should remain usable under a finite compute budget rather than as an academic monster optimized only for leaderboard prestige. For most experiments they target about `1.5 billion` multiply-add operations at inference time. That detail is central to understanding the paper. Inception is not simply "deeper is better." It is "deeper and wider can be better if compute is allocated more intelligently."

**The sparse-theory intuition behind the architecture**

The motivating story is unusual and worth understanding carefully. The authors point to the work of Arora et al. on learning deep sparse representations and connect it to the Hebbian slogan "neurons that fire together, wire together." The idea is that if activations from the previous layer reveal clusters of highly correlated units, then an ideal next layer would connect more densely within those correlated groups and more sparsely elsewhere. In lower layers those groups should be spatially local; higher in the hierarchy they can spread over larger regions.

That logic leads naturally to the thought that a good vision network should mix information at multiple spatial scales. Some patterns may be captured by small local filters, others by broader receptive fields, and pooling still contributes a useful summary path. But it is important not to overread the paper here. It does not prove that Inception is the optimal topology, and it does not actually build a truly sparse network from data-driven clustering. The sparse-theory argument is a motivating intuition, not a derivation. The actual architecture is a hand-designed dense approximation of what such sparse structure might look like.

**The first Inception idea: multi-scale branches in parallel**

The basic Inception module is the paper's conceptual center. Instead of choosing one convolution size for a whole stage, the module runs several transforms in parallel and concatenates their outputs along the channel dimension. The naive version contains `1x1`, `3x3`, and `5x5` convolutions together with a pooling branch.

The module-level pipeline is:

Input feature map -> parallel `1x1`, `3x3`, `5x5`, and pooling branches -> concatenate branch outputs -> feed combined representation to the next stage

This design reflects the paper's multi-scale thesis. Small filters capture fine local structure. Larger filters reach more spatial context. Pooling preserves the useful tradition of local summarization and invariance-building. The paper also notes that the restriction to `1x1`, `3x3`, and `5x5` filters is mainly a matter of convenience and implementation sanity, especially to avoid patch-alignment complications. So even the famous branch sizes should be read as a practical discretization of a broader idea rather than as sacred architecture law.

**Why the naive module is too expensive**

Once the paper introduces the naive Inception block, it immediately runs into the problem that makes the paper necessary in the first place: computation blows up. A moderate number of `5x5` convolutions on a tensor with many channels is expensive, and if each branch emits many channels, the concatenated output makes the next stage even more expensive. Adding pooling branches without controlling dimensionality makes that channel growth worse, not better.

This is the key engineering pressure in the paper. The architecture the authors conceptually want, namely one that approximates a richer sparse topology, becomes impractical if implemented naively with dense operators. The rest of the paper is essentially the story of how they prevent that computational explosion without giving up the multi-scale idea.

**Why `1x1` convolutions are the hidden key**

The decisive move is to insert `1x1` convolutions before the expensive `3x3` and `5x5` branches, using them as dimension-reduction layers. This idea borrows from the Network in Network paper, but here it becomes more operationally important. The `1x1` layers shrink the number of input channels before the costly spatial convolutions are applied, which makes the entire module far cheaper. Because these `1x1` layers are followed by ReLU, they are not merely linear compression gadgets; they are also additional learned nonlinear transformations over channels.

The compute-aware branch pipeline becomes:

Input -> `1x1` reductions on expensive branches -> `3x3` and `5x5` convolutions on compressed representations -> pooling branch with projection -> concatenate outputs

This is the real heart of Inception. The paper is often remembered for "parallel branches," but the resource-management trick is what makes those branches viable. Without the `1x1` reductions, the architecture is mostly a nice idea. With them, the model can become both wider and deeper while remaining trainable and deployable.

The authors also suggest that as one moves upward through the network and features become more abstract and less spatially concentrated, the relative importance of broader filters should increase. That gives Inception a stage-wise interpretive logic: lower layers can stay fairly conventional, while higher layers are where multi-scale branching pays off more heavily.

**How GoogLeNet instantiates the architecture**

GoogLeNet is the specific network used in the ILSVRC 2014 submission, not a synonym for the entire Inception idea. Its input is a `224x224` RGB image with zero mean. The front of the network still looks fairly classical: a `7x7/2` convolution, max pooling, local response normalization, a `1x1` convolution, a `3x3` convolution, another normalization, and another max pool. Only after that stem do the repeated Inception modules take over.

The high-level network pipeline is:

`224x224` image -> early convolutional stem -> Inception `3a`, `3b` -> max pool -> Inception `4a`, `4b`, `4c`, `4d`, `4e` -> max pool -> Inception `5a`, `5b` -> global average pool -> dropout -> linear classifier -> softmax

The paper's Table 1 makes clear that each module has its own branch widths and reduction sizes, so the network is not mechanically repeating one identical block. It is a carefully tuned stack of related blocks. The paper counts GoogLeNet as `22` layers deep when counting only layers with parameters, or `27` if pooling layers are included. It also remarks that the total number of independent building blocks is closer to `100`, depending on the counting convention. That is a good reminder that "depth" is not a trivial statistic once networks become modular.

Another crucial design choice is the use of global average pooling before the final classifier instead of large fully connected layers. This follows the spirit of Network in Network and helps keep parameters under control. The authors report that switching from fully connected layers to average pooling improved top-1 accuracy by about `0.6%`, though dropout still remained important even after the fully connected stack was removed. Combined with the overall architecture, the resulting system uses dramatically fewer parameters than the 2012 AlexNet-style winner while achieving much better accuracy.

**Auxiliary classifiers and how the paper thinks about optimization**

Because the network is relatively deep, the authors worried about gradient propagation through all layers. Their answer was to attach auxiliary classifiers to intermediate points in the network, specifically after Inception `4a` and `4d`. These side heads are small classifiers built from average pooling, a `1x1` convolution for dimension reduction, a fully connected layer with `1024` units, heavy dropout, and a softmax prediction over the same `1000` classes. During training, their losses are added to the main loss with weight `0.3`; at inference time, they are discarded.

The auxiliary-head pipeline is:

Intermediate feature map -> average pool -> `1x1` conv -> fully connected layer -> dropout -> softmax loss

This is a historically important detail because many people remember the auxiliary heads as a major breakthrough against vanishing gradients. The paper itself is more restrained than that memory. It later reports control experiments suggesting their effect is relatively minor, around `0.5%`, and that one auxiliary classifier would have been enough to get essentially the same benefit. So even inside the paper, this idea is presented and then partially deflated by follow-up experimentation.

**How the model was trained**

Training is described in a notably practical, slightly messy way, which fits the competition context. The network was trained in Google's DistBelief system with modest model and data parallelism. The implementation used CPUs, not a GPU-centric training stack, though the authors estimate that a few high-end GPUs could likely train it within a week if memory were handled well. Optimization used asynchronous SGD with `0.9` momentum, a fixed learning-rate schedule that decayed by `4%` every `8` epochs, and Polyak averaging for the final inference model.

The data pipeline also matters. Over time the team changed image sampling methods and sometimes continued training already-converged models under different settings, which means the paper is honest that there is no perfectly clean single recipe to extract. One prescription that worked well after the competition sampled patches covering anywhere from `8%` to `100%` of the image area, with aspect ratio restricted to `[3/4, 4/3]`. The authors also found Andrew Howard's photometric distortions useful against overfitting to the imaging conditions of the training data.

**What the ImageNet classification result really consists of**

The classification task is standard ILSVRC: `1,000` categories, roughly `1.2 million` training images, `50,000` validation images, and `100,000` test images. Performance is ranked by top-5 error. GoogLeNet wins the 2014 challenge with `6.67%` top-5 error on both validation and test, which is a large relative improvement over earlier systems. The paper emphasizes a `56.5%` relative reduction compared with the 2012 SuperVision result and about a `40%` relative reduction compared with the previous year's best Clarifai system.

But the paper is also clear that this headline number is a whole-system result, not the score of one naked model evaluated with one center crop. The team trained `7` versions of GoogLeNet, including one wider variant, and used ensemble prediction. At test time they also used an aggressive multi-crop evaluation scheme: `4` image scales, `3` spatial positions per scale, `6` crops per square including corners and center plus one resized whole-square crop, and mirrored versions, giving `144` crops per image. The final probabilities are obtained by averaging over crops and models.

The performance breakdown is revealing:

One model + one crop -> `10.07%` top-5 error  
One model + `10` crops -> `9.15%`  
One model + `144` crops -> `7.89%`  
Seven models + one crop -> `8.09%`  
Seven models + `144` crops -> `6.67%`

This is important for honest interpretation. The architecture itself is strong, but the challenge-winning number also depends substantially on test-time augmentation and ensembling. The paper is not hiding that; it documents it. So the correct lesson is not "a single GoogLeNet forward pass suddenly solved ImageNet." The correct lesson is that the Inception design produced a very strong base model whose gains compounded well with a serious competition inference protocol.

**Why the detection results matter**

The paper does not stop at classification. It also evaluates GoogLeNet in the ILSVRC 2014 detection challenge, where the task is to place class-labeled bounding boxes around objects from `200` categories and performance is measured by mean average precision. Here the authors use a pipeline similar in spirit to R-CNN, but with the Inception model as the region classifier.

The detection pipeline is:

Image -> region proposals from selective search plus Multibox -> crop proposed regions -> classify regions with GoogLeNet -> combine detections into final boxes

They modify the proposal stage by doubling the superpixel size, which halves the number of selective-search proposals, then add back `200` Multibox proposals. This reduces the proposal count to about `60%` of what R-CNN used while slightly increasing proposal coverage from `92%` to `93%`. The paper reports about a `1%` mAP gain in the single-model case from that change alone. With a `6`-model ensemble, the detection system reaches `43.9%` mAP and wins the challenge. Even the single-model version reaches `38.02%` mAP without contextual modeling or bounding-box regression, which the authors did not implement in time. That matters because it shows the architecture is not just a classifier trick; it transfers into a broader visual recognition system.

**What the paper actually established**

Taken as a whole, the paper establishes that dense modules can be arranged to approximate some of the benefits people hoped sparse, multi-scale visual computation would provide. It shows that you do not have to choose between accuracy and efficiency in a simplistic way. With the right module design, you can increase representational richness while still respecting a compute budget.

It also marks a shift in architectural thinking. Earlier CNN success stories were often narrated mostly in terms of depth, filter counts, and regularization. This paper starts talking more explicitly about branch structure, dimensionality reduction, module composition, inference cost, and system-level resource allocation. That way of thinking became one of the major pathways by which deep learning architecture design matured.

---

## **Subtle points, clarifications, and limits**

One subtlety that is easy to miss is that `Inception` and `GoogLeNet` are not identical terms. Inception is the broader architectural idea of multi-branch, multi-scale modules with dimensionality control. GoogLeNet is one specific `22`-layer incarnation used in the 2014 competition system. Another subtlety is that the paper's sparse-network story is motivational rather than demonstrated. The model never becomes truly sparse in the computational sense; it remains a dense network whose structure is chosen to mimic where sparsity might have been useful.

It is also worth remembering that the famous top-5 error of `6.67%` is a full competition recipe, not a plain single-model benchmark. And historically, not every piece of the paper aged equally. The auxiliary classifiers mattered less than expected, later Inception variants changed the branch design substantially, and later families like ResNets often offered a simpler path to very strong performance. What endured most was not every exact branch width in Table 1, but the design principle that computation can be split across scales and controlled through cheap projections.

---

## **Closing perspective**

This paper has canonical status in the history of computer vision. It is respected not just because GoogLeNet won ImageNet and detection benchmarks, but because it made architectural resource allocation a first-class scientific and engineering concern. In the lineage of influential vision papers, it sits alongside AlexNet, VGG, and ResNet as one of the landmarks that changed how people thought about deep networks rather than merely improving a score.

Its long-term influence is slightly different from those other papers. Many practitioners no longer deploy the original GoogLeNet block exactly as written, but the underlying lessons spread widely: multi-scale processing matters, `1x1` convolutions can be strategically transformative, large fully connected tails are often wasteful, and system-level compute efficiency belongs inside architecture design rather than after it. That is why the paper still carries serious respect from the computer vision and deep learning communities. It is both a historical milestone and a genuinely instructive piece of design thinking.

---

## **Personal comprehension notes**

The easiest way to remember Inception is: each spatial location gets several different "looks" at the same feature map, and the network keeps all of them. One branch asks, "is a tiny local pattern enough?" Another asks, "do I need a medium-sized neighborhood?" Another asks, "do I need even more context?" Pooling adds a summary view. Then the model stacks all those answers together and lets the next stage decide what to use.

The `1x1` convolutions are the paper's budget managers. They do not look glamorous, but they are what makes the whole design economically viable. A good mental model is that the network first compresses or remixes channels into a cheaper internal code, then spends the expensive `3x3` and `5x5` operations only where that spending is justified. So Inception is really a story about selective spending, not just multi-branch cleverness.

Another good way to think about GoogLeNet is as a bridge between two eras. Earlier CNNs mostly felt like stronger or weaker versions of the same stack. After this paper, architecture starts to feel modular and strategic. You are no longer just asking how many layers to add. You are asking what kinds of computation should happen in parallel, where to compress, where to widen, and how to keep the overall system within budget.

---

## **Compact retention notes**

- **Paper type:** Foundational architecture paper with strong experimental validation
- **Core idea:** Approximate multi-scale sparse visual processing using dense Inception modules that branch across filter sizes while controlling compute with `1x1` reductions.
- **Main mechanism:** Parallel `1x1`, `3x3`, `5x5`, and pooling branches with channel concatenation, stacked into GoogLeNet and combined with global average pooling and auxiliary training heads.
- **Key result:** GoogLeNet won ILSVRC 2014 classification with `6.67%` top-5 error and also led the detection challenge, while using far fewer parameters than earlier giant CNNs.
- **Main limitation:** The sparse-theory motivation is heuristic rather than proven, and the best reported numbers depend on ensembling and heavy test-time cropping rather than a single plain model.

---

## **Citations used in the paper**

- *Know Your Meme: We Need to Go Deeper*, 2014
- Sanjeev Arora, Aditya Bhaskara, Rong Ge, Tengyu Ma, *Provable Bounds for Learning Some Deep Representations*, 2013
- Umit V. Catalyurek, Cevdet Aykanat, Bora Ucar, *On Two-Dimensional Sparse Matrix Partitioning: Models, Methods, and a Recipe*, 2010
- Jeffrey Dean et al., *Large Scale Distributed Deep Networks*, NIPS 2012
- Dumitru Erhan, Christian Szegedy, Alexander Toshev, Dragomir Anguelov, *Scalable Object Detection Using Deep Neural Networks*, CVPR 2014
- Ross B. Girshick, Jeff Donahue, Trevor Darrell, Jitendra Malik, *Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation*, CVPR 2014
- Geoffrey E. Hinton, Nitish Srivastava, Alex Krizhevsky, Ilya Sutskever, Ruslan Salakhutdinov, *Improving Neural Networks by Preventing Co-Adaptation of Feature Detectors*, 2012
- Andrew G. Howard, *Some Improvements on Deep Convolutional Neural Network Based Image Classification*, 2013
- Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton, *ImageNet Classification with Deep Convolutional Neural Networks*, NIPS 2012
- Yann LeCun, Bernhard Boser, John S. Denker, Donnie Henderson, Richard E. Howard, Wayne Hubbard, Lawrence D. Jackel, *Backpropagation Applied to Handwritten Zip Code Recognition*, 1989
- Yann LeCun, Leon Bottou, Yoshua Bengio, Patrick Haffner, *Gradient-Based Learning Applied to Document Recognition*, 1998
- Min Lin, Qiang Chen, Shuicheng Yan, *Network in Network*, 2013
- Boris T. Polyak, Anatoli B. Juditsky, *Acceleration of Stochastic Approximation by Averaging*, 1992
- Pierre Sermanet, David Eigen, Xiang Zhang, Michael Mathieu, Rob Fergus, Yann LeCun, *OverFeat: Integrated Recognition, Localization and Detection Using Convolutional Networks*, 2013
- Thomas Serre, Lior Wolf, Stanley M. Bileschi, Maximilian Riesenhuber, Tomaso Poggio, *Robust Object Recognition with Cortex-Like Mechanisms*, 2007
- Fengguang Song, Jack Dongarra, *Scaling Up Matrix Computations on Shared-Memory Manycore Systems with 1000 CPU Cores*, ICS 2014
- Ilya Sutskever, James Martens, George E. Dahl, Geoffrey E. Hinton, *On the Importance of Initialization and Momentum in Deep Learning*, ICML 2013
- Christian Szegedy, Alexander Toshev, Dumitru Erhan, *Deep Neural Networks for Object Detection*, NIPS 2013
- Alexander Toshev, Christian Szegedy, *DeepPose: Human Pose Estimation via Deep Neural Networks*, 2013
- Koen E. A. van de Sande, Jasper R. R. Uijlings, Theo Gevers, Arnold W. M. Smeulders, *Segmentation as Selective Search for Object Recognition*, ICCV 2011
- Matthew D. Zeiler, Rob Fergus, *Visualizing and Understanding Convolutional Networks*, ECCV 2014
