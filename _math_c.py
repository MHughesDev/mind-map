# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, r"C:\Users\Mason\mind-map")
from _gen_lib import *
MATH = os.path.join(CORE, "Mathematics")

def build_subject(node, keep=()):
    d = os.path.join(MATH, node["name"])
    if os.path.isdir(d): clean_stubs(d, keep=keep)
    generate(node, MATH, "Mathematics", "Mathematics")
    prune_empty(d)
    n = sum(1 for dp,_,fn in os.walk(d) for f in fn if f.endswith(".md"))
    print(f"  {node['name']}: {n} md")

PS = F("Probability & Statistics", "The mathematics of uncertainty, randomness, and inference from data.", [
 F("Probability Theory", "The axiomatic theory of randomness.", [
   L("Sample Spaces & Events", "The foundations of probability.", ["**Sample spaces and events** — outcomes.", "**Axioms of probability** — Kolmogorov.", "**Counting and probability** — combinatorial."]),
   L("Conditional Probability", "Updating probability with information.", ["**Conditional probability** — definition.", "**Independence** — and its meaning.", "**Bayes' rule** — inverting conditionals."]),
   L("Random Variables", "Numerical outcomes of randomness.", ["**Discrete and continuous** — random variables.", "**Distribution and density functions** — describing them.", "**Functions of random variables** — transformations."]),
   L("Distributions", "The common probability distributions.", ["**Discrete distributions** — binomial, Poisson.", "**Continuous distributions** — normal, exponential.", "**Properties** — and relationships."]),
   L("Expectation & Variance", "Summarizing random variables.", ["**Expectation** — the mean.", "**Variance and moments** — spread.", "**Generating functions** — moments and more."]),
   L("Limit Theorems", "The behavior of many random variables.", ["**Laws of large numbers** — averages converge.", "**The central limit theorem** — universality of the normal.", "**Convergence concepts** — in probability and distribution."]),
 ]),
 F("Mathematical Statistics", "Drawing conclusions about populations from data.", [
   L("Estimation", "Inferring parameters from samples.", ["**Estimators** — and their properties.", "**Bias and consistency** — quality.", "**Sufficiency** — and information."]),
   L("Maximum Likelihood", "The dominant estimation method.", ["**The likelihood function** — definition.", "**MLE** — finding estimates.", "**Properties** — asymptotic optimality."]),
   L("Confidence Intervals", "Interval estimates of parameters.", ["**Confidence intervals** — interpretation.", "**Construction** — pivotal quantities.", "**Common intervals** — means and proportions."]),
   L("Hypothesis Testing", "Deciding between competing claims.", ["**Tests and errors** — type I and II.", "**p-values and power** — interpretation.", "**Common tests** — t, chi-square, F."]),
   L("Regression", "Modeling relationships between variables.", ["**Linear regression** — least squares.", "**Inference** — and diagnostics.", "**Multiple regression** — many predictors."]),
   L("Nonparametric Methods", "Inference without distributional assumptions.", ["**Rank-based tests** — distribution-free.", "**Density estimation** — kernels.", "**The bootstrap** — resampling."]),
 ]),
 F("Bayesian Statistics", "Inference treating parameters as random and updating beliefs.", [
   L("Bayes' Theorem", "The engine of Bayesian inference.", ["**Priors, likelihoods, posteriors** — the framework.", "**Updating beliefs** — with data.", "**Bayesian vs frequentist** — perspectives."]),
   L("Priors & Posteriors", "Encoding and updating beliefs.", ["**Choosing priors** — informative and not.", "**Posterior computation** — the basics.", "**Credible intervals** — interpretation."]),
   L("Conjugate Priors", "Priors that make updating easy.", ["**Conjugacy** — definition.", "**Common conjugate families** — examples.", "**Closed-form posteriors** — convenience."]),
   L("Markov Chain Monte Carlo", "Sampling from complex posteriors.", ["**Why sampling** — intractable posteriors.", "**Metropolis-Hastings and Gibbs** — algorithms.", "**Diagnostics** — convergence."]),
   L("Hierarchical Models", "Multi-level Bayesian models.", ["**Hierarchical structure** — and partial pooling.", "**Shrinkage** — borrowing strength.", "**Applications** — grouped data."]),
 ]),
 K("Stochastic Processes"),
])

AM = F("Applied Mathematics", "Mathematics deployed to model, analyze, and optimize real-world systems.", [
 F("Numerical Analysis", "Algorithms for approximating continuous mathematics.", [
   L("Error & Floating Point", "The limits of numerical computation.", ["**Floating-point representation** — and precision.", "**Sources of error** — round-off and truncation.", "**Conditioning and stability** — sensitivity."]),
   L("Root Finding", "Solving nonlinear equations numerically.", ["**Bisection** — bracketing.", "**Newton's method** — and convergence.", "**Fixed-point iteration** — and secant."]),
   L("Interpolation", "Fitting functions through data.", ["**Polynomial interpolation** — Lagrange and Newton.", "**Spline interpolation** — piecewise.", "**Error analysis** — accuracy."]),
   L("Numerical Integration", "Approximating integrals.", ["**Newton-Cotes rules** — trapezoid, Simpson.", "**Gaussian quadrature** — optimal points.", "**Adaptive methods** — error control."]),
   L("Numerical Linear Algebra", "Solving systems and eigenproblems numerically.", ["**Direct solvers** — LU and pivoting.", "**Iterative methods** — and convergence.", "**Eigenvalue algorithms** — QR and power."]),
   L("Numerical ODEs", "Integrating differential equations.", ["**Euler methods** — explicit and implicit.", "**Runge-Kutta methods** — higher order.", "**Stability and stiffness** — challenges."]),
 ]),
 F("Optimization", "Finding the best solution subject to constraints.", [
   L("Linear Programming", "Optimizing linear objectives.", ["**LP formulation** — and geometry.", "**The simplex method** — solving.", "**Duality** — the dual problem."]),
   L("Convex Optimization", "The tractable frontier of optimization.", ["**Convex sets and functions** — basics.", "**Convex problems** — and properties.", "**Algorithms** — interior point."]),
   L("Gradient Methods", "First-order optimization.", ["**Gradient descent** — and step sizes.", "**Stochastic gradient descent** — large scale.", "**Acceleration** — momentum methods."]),
   L("Constrained Optimization", "Optimizing under constraints.", ["**Lagrange multipliers** — equality constraints.", "**KKT conditions** — inequality constraints.", "**Penalty methods** — and barriers."]),
   L("Integer Programming", "Optimization with discrete variables.", ["**Integer programs** — formulation.", "**Branch and bound** — solving.", "**Relaxations** — and bounds."]),
 ]),
 F("Dynamical Systems & Chaos", "How systems evolve and the emergence of unpredictability.", [
   L("Flows & Maps", "Continuous and discrete dynamics.", ["**Flows** — continuous-time systems.", "**Maps** — discrete-time systems.", "**Phase space** — and trajectories."]),
   L("Fixed Points & Stability", "Equilibria and their behavior.", ["**Fixed points** — and equilibria.", "**Linearization** — and stability.", "**Lyapunov functions** — stability proofs."]),
   L("Bifurcations", "Qualitative changes in dynamics.", ["**Bifurcation types** — saddle-node, Hopf.", "**Bifurcation diagrams** — visualizing.", "**Applications** — onset of oscillation."]),
   L("Chaos", "Deterministic unpredictability.", ["**Sensitive dependence** — the butterfly effect.", "**Strange attractors** — and examples.", "**Routes to chaos** — period doubling."]),
   L("Fractals", "Self-similar geometric structure.", ["**Fractal dimension** — measuring roughness.", "**Famous fractals** — Mandelbrot and Julia.", "**Connections** — to dynamics."]),
 ]),
 F("Control Theory", "Designing inputs to make systems behave as desired.", [
   L("State-Space Models", "Describing dynamical systems.", ["**State-space representation** — and form.", "**Linear systems** — and solutions.", "**Transfer functions** — input-output."]),
   L("Controllability & Observability", "Structural properties of systems.", ["**Controllability** — reaching states.", "**Observability** — inferring states.", "**Canonical forms** — and tests."]),
   L("Feedback Control", "Using output to drive input.", ["**Feedback** — and stabilization.", "**PID control** — the workhorse.", "**Pole placement** — design."]),
   L("Optimal Control", "Controlling at minimum cost.", ["**The cost functional** — objectives.", "**Pontryagin's principle** — necessary conditions.", "**LQR** — linear-quadratic regulator."]),
 ]),
 F("Game Theory", "The mathematics of strategic interaction.", [
   L("Normal-Form Games", "Simultaneous strategic decisions.", ["**Players, strategies, payoffs** — the model.", "**Dominance** — and rationalizability.", "**Examples** — prisoner's dilemma."]),
   L("Nash Equilibrium", "Stable strategy profiles.", ["**Nash equilibrium** — definition.", "**Mixed strategies** — randomization.", "**Existence** — Nash's theorem."]),
   L("Extensive-Form Games", "Sequential strategic interaction.", ["**Game trees** — and information.", "**Subgame perfection** — refinement.", "**Backward induction** — solving."]),
   L("Cooperative Game Theory", "Coalitions and fair division.", ["**Coalitions and the core** — stability.", "**The Shapley value** — fair allocation.", "**Bargaining** — and solutions."]),
   L("Mechanism Design", "Designing games for desired outcomes.", ["**Incentive compatibility** — truthfulness.", "**Auctions** — and revenue.", "**The revelation principle** — simplification."]),
 ]),
 F("Information Theory", "Quantifying information, compression, and communication.", [
   L("Entropy", "Measuring uncertainty.", ["**Shannon entropy** — definition.", "**Joint and conditional entropy** — and chain rule.", "**Properties** — and intuition."]),
   L("Mutual Information", "Shared information between variables.", ["**Mutual information** — definition.", "**Relative entropy** — KL divergence.", "**Applications** — feature selection."]),
   L("Source Coding", "The limits of data compression.", ["**The source coding theorem** — entropy limit.", "**Huffman coding** — optimal codes.", "**Arithmetic coding** — and beyond."]),
   L("Channel Capacity", "The limits of reliable communication.", ["**Channel models** — and capacity.", "**The noisy-channel theorem** — Shannon's result.", "**Error-correcting codes** — achieving capacity."]),
 ]),
 F("Mathematical Physics", "The mathematical structures underlying physical theories.", [
   L("Vector & Tensor Calculus", "The language of fields.", ["**Vector calculus** — grad, div, curl.", "**Tensors** — and index notation.", "**Curvilinear coordinates** — and transformations."]),
   L("Variational Principles", "Physics from optimization.", ["**The calculus of variations** — Euler-Lagrange.", "**The principle of least action** — mechanics.", "**Noether's theorem** — symmetry and conservation."]),
   L("PDEs of Physics", "The equations governing nature.", ["**Wave and heat equations** — and solutions.", "**The Schrodinger equation** — quantum mechanics.", "**Special functions** — Bessel, Legendre."]),
   L("Group Theory in Physics", "Symmetry as a physical principle.", ["**Symmetry groups** — and representations.", "**Lie groups and algebras** — continuous symmetry.", "**Applications** — particle physics."]),
 ]),
])

HP = F("History & Philosophy of Mathematics", "Where mathematics came from and what its objects and truths actually are.", [
 L("Ancient Mathematics", "The origins of mathematical thought.", ["**Babylonian and Egyptian mathematics** — early arithmetic.", "**Greek mathematics** — proof and Euclid.", "**Other traditions** — Indian, Chinese, Islamic."]),
 L("Development of Calculus", "The invention of the calculus and its rigor.", ["**Newton and Leibniz** — the invention.", "**The priority dispute** — history.", "**Rigorization** — Cauchy and Weierstrass."]),
 L("The Foundations Crisis", "When mathematics questioned itself.", ["**Paradoxes** — Russell and others.", "**Responses** — programs to secure foundations.", "**Resolution** — and its limits."]),
 L("Philosophy of Mathematics", "What mathematical objects and truths are.", ["**Platonism** — mathematics as discovery.", "**Formalism and logicism** — mathematics as construction.", "**Intuitionism** — and constructivism."]),
 L("Godel & the Limits of Formalism", "The incompleteness theorems and their meaning.", ["**The incompleteness theorems** — recap.", "**Implications** — for foundations.", "**Philosophical impact** — and debates."]),
])

# History was a root-level leaf file; remove it, then build as a folder
old_hist = os.path.join(MATH, "History & Philosophy of Mathematics.md")
if os.path.isfile(old_hist):
    os.remove(old_hist)

build_subject(PS, keep={"Stochastic Processes.md"})
build_subject(AM)
generate(HP, MATH, "Mathematics", "Mathematics")
print(f"  History & Philosophy: built")

# Rebuild Mathematics root index
subjects = ["Foundations & Logic", "Algebra", "Number Theory", "Combinatorics", "Discrete Math",
            "Analysis", "Geometry", "Topology", "Probability & Statistics", "Applied Mathematics",
            "History & Philosophy of Mathematics"]
_emit_moc(os.path.join(MATH, "Mathematics.md"), "Mathematics", "Mathematics", "Mathematics",
          "The science of structure, quantity, space, and change; the foundational language of all quantitative knowledge.",
          [f"[[{s}]] (folder)" for s in subjects])
print("Math batch C done.")
