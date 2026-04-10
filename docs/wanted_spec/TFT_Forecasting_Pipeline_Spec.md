# TFT forecasting pipeline — implementation specification

This document is the **full TFT forecasting spec** for the trading bot, written as an implementation guide rather than a high-level summary.

The design keeps **TFT** as the core forecaster because TFT is built for **multi-horizon forecasting with three input families**—static inputs, known future inputs, and observed historical inputs—and because it includes **variable selection networks, gating, recurrent local processing, and self-attention for longer-range dependencies**. Those are the architectural pieces to preserve. At the same time, recent financial benchmarking suggests that **generic transformer stacks are not automatically the best choice in finance**, and that **richer temporal representations and strong variable-selection hybrids can outperform plain deep baselines**, so this spec adds a latent-state front-end, regime conditioning, and ensembling around TFT rather than using a plain TFT alone. ([Temporal Fusion Transformers (original)](https://arxiv.org/abs/1912.09363))

---

## 1. System objective

The TFT model is the **world model** of the trading system. Its job is not to place trades directly. Its job is to produce a calibrated forecast of the near-future market state from recent data. Concretely, it should output a **probabilistic multi-horizon return forecast** for the next few decision steps, plus uncertainty estimates derived from quantiles. The downstream policy or rules engine will convert that forecast into actions. This separation is deliberate: TFT is used for **prediction**, not for final execution control. TFT’s original design is probabilistic and multi-horizon, and that is the correct mode for this use case. ([Temporal Fusion Transformers (original)](https://arxiv.org/abs/1912.09363))

---

## 2. Trading cadence and horizon definition

The base decision cadence will be either **15 seconds** or **1 minute**. The model should be trained for one base cadence only; higher time horizons should be represented as derived features, not as separate raw candle streams. The forecast horizon should be multi-step. For a 15-second system, a sensible initial horizon is **H = 4 to 8 steps**. For a 1-minute system, a sensible initial horizon is also **H = 4 to 8 steps**. The model therefore predicts a sequence of future returns, not a single next-tick value. This matches TFT’s intended use as a multi-horizon forecaster and keeps the target aligned with trading decisions instead of raw price reconstruction. ([Temporal Fusion Transformers (original)](https://arxiv.org/abs/1912.09363))

---

## 3. Prediction target

The model target will be **future log returns**, not OHLC and not raw price. The target for each future horizon `h` is:

`r_{t+h} = log(close_{t+h} / close_t)`

The model should predict quantiles for each horizon, such as `q10`, `q50`, and `q90`. The median forecast `q50` is the central directional estimate. The interval width `q90 - q10` is the uncertainty estimate. This is preferred over a deterministic regression target because TFT is designed for probabilistic forecasting and is commonly trained with **quantile loss**. Using returns rather than prices improves stationarity and makes the output directly useful for decision logic. ([Temporal Fusion Transformers (original)](https://arxiv.org/abs/1912.09363))

---

## 4. Model architecture overview

The full model stack is:

**market data → feature builder → latent encoder → regime estimator → TFT core → quantile head → ensemble combiner**

This spec intentionally includes the advanced upgrades we discussed:

* latent-state front-end
* regime conditioning
* regime-aware normalization
* probabilistic multi-horizon output
* ensemble inference
* optional expert routing in a later phase

That structure is justified by two lines of evidence: first, TFT’s architecture is well suited to structured multi-input forecasting; second, recent financial benchmarking found that **richer learned temporal representations** and **strong variable-selection hybrids** are especially effective in financial forecasting, which supports augmenting TFT with a representation-learning front-end instead of leaving it “plain.” ([Temporal Fusion Transformers (original)](https://arxiv.org/abs/1912.09363))

---

## 5. Input families

The model uses TFT’s standard three-way split.

### 5.1 Observed historical inputs

These are known only up to the current time and are passed through the encoder portion of the model. They include:

* log returns at the base interval
* rolling volatility estimates
* rolling momentum features
* range and candle-shape features if candles are used
* volume and volume change
* spread and spread change if available
* optional microstructure summaries if available, but not required

These are the core market-state observations. They are the main empirical description of “what the market has been doing.” TFT was designed to handle this observed-past block explicitly. ([Temporal Fusion Transformers (original)](https://arxiv.org/abs/1912.09363))

### 5.2 Known future inputs

These are features known for every forecast horizon at prediction time. In this system they are mainly calendar and cyclic time features:

* `sin(2π * minute / 60)`
* `cos(2π * minute / 60)`
* `sin(2π * hour / 24)`
* `cos(2π * hour / 24)`
* `sin(2π * day_of_week / 7)`
* `cos(2π * day_of_week / 7)`
* optional session flags if relevant to the traded market

These features are simple, but they are correct and standard. They are not the main source of alpha; they tell the model **where it is in time** so it can align behavior with recurring market patterns. TFT explicitly expects and benefits from known-future inputs of this type. ([Temporal Fusion Transformers (original)](https://arxiv.org/abs/1912.09363))

### 5.3 Static or slow-moving inputs

For a single-asset system without cross-asset features, static inputs should still exist, but they are limited:

* asset ID embedding if the system may later support multiple symbols
* exchange ID if multiple exchanges are ever used
* model configuration ID if training across multiple instrument variants
* slow regime summary features if treated as static over the current sample window

Static covariates matter because TFT uses them to condition internal gating and context vectors. Even in a single-asset design, leaving space for static conditioning is useful. ([Temporal Fusion Transformers (original)](https://arxiv.org/abs/1912.09363))

---

## 6. Feature engineering block

The feature builder should produce a clean, layered world state.

### 6.1 Base-frequency observed features

For each bar:

* `log_return_1`
* `abs_return_1`
* `high_low_range / close`
* `close_open_return`
* `volume_z`
* `spread_z` if available

### 6.2 Multi-scale derived features

From the base bars, derive rolling aggregates at larger windows. These are features, not separate raw time streams:

* short window: 4 to 8 base steps
* medium window: 5-minute equivalent and 15-minute equivalent
* long window: 1-hour equivalent and optionally 4-hour equivalent

For each of those windows:

* rolling mean return
* rolling standard deviation
* rolling realized volatility
* momentum
* max drawdown over window
* z-scored deviation from rolling mean

This gives the model short-, medium-, and long-context summaries without breaking the one-base-cadence design. TFT already combines local sequence modeling and longer-range attention; these aggregates make that job easier. ([Temporal Fusion Transformers (original)](https://arxiv.org/abs/1912.09363))

### 6.3 Regime features

A regime subsystem should compute soft regime probabilities at every timestep. Start with four regimes:

* uptrend
* downtrend
* low-volatility chop
* high-volatility chop

A simple first implementation can derive those probabilities from:

* recent trend slope
* realized volatility
* momentum
* autocorrelation
* distance from rolling moving average

Do not hard-assign a single regime initially. Output a soft vector like:
`[p_uptrend, p_downtrend, p_lowvol_chop, p_highvol_chop]`

This is included as part of the observed or slow-moving input block. Adaptive TFT research for crypto reports improvements from **pattern-based categorization and adaptive segmentation**, specifically because plain TFT struggles with non-stationarity in volatile financial series. ([Adaptive TFT for cryptocurrency](https://arxiv.org/abs/2509.10542))

---

## 7. Regime-aware normalization

Every observed feature should be normalized in two ways:

* rolling global normalization
* regime-aware normalization

For a feature `x_t`:

* global version: `(x_t - rolling_mean) / rolling_std`
* regime version: `(x_t - regime_mean) / regime_std`

Feed both versions into the model when practical. Finance is highly non-stationary, and regime adaptation is one of the reasons adaptive TFT variants help. This step is less flashy than architecture changes, but it is critical for keeping feature distributions well-behaved across changing market states. ([Adaptive TFT for cryptocurrency](https://arxiv.org/abs/2509.10542))

---

## 8. Latent-state encoder

Before the TFT core, add a compact front-end encoder that transforms the recent observed sequence into a learned latent state `z_t`. This is the main advanced enhancement for prediction quality.

### 8.1 Purpose

The latent encoder learns nonlinear temporal structure that hand-built features may miss. Recent financial benchmarking found that **models explicitly designed to learn rich temporal representations** outperform generic baselines more consistently than architecture hype alone would suggest. That is the main reason this spec includes a representation-learning front-end. ([Deep learning for financial time series benchmark](https://arxiv.org/abs/2603.01820))

### 8.2 Recommended encoder

Use a **small causal 1D CNN** first. This is preferable to a more complicated variational or generative encoder for the first production version.

Recommended structure:

* input: last `L` encoder steps of observed normalized features
* 2 or 3 causal Conv1D layers
* kernel sizes: 3, 5, and optionally 7
* channel widths: 32 → 64 → 64
* activation: GELU or ReLU
* optional residual connection
* global temporal pooling or final-step extraction
* output latent vector: dimension 16 or 32

This produces `z_t`.

### 8.3 How to use `z_t`

Concatenate `z_t` back into the TFT input path as either:

* an additional observed feature block repeated over the decoder horizon, or
* a static context vector conditioning the TFT

The second option is cleaner. Treat `z_t` as a context summary of recent market state. This does not alter TFT’s core design; it enhances it. Similar hybrid approaches that combine structured feature selection with sequence models have performed very well in recent finance benchmarks. ([Deep learning for financial time series benchmark](https://arxiv.org/abs/2603.01820))

---

## 9. TFT core specification

The TFT core should remain recognizable as TFT.

### 9.1 Main components to keep

* variable selection networks for each input family
* gating layers / GRNs
* recurrent local encoder-decoder path
* interpretable self-attention block
* static covariate encoders
* multi-horizon decoder

These are the exact mechanisms that define TFT and are the reason to use it in the first place. ([Temporal Fusion Transformers (original)](https://arxiv.org/abs/1912.09363))

### 9.2 Suggested base hyperparameters

For a first production build:

* hidden size: 64 or 128
* attention heads: 4
* dropout: 0.1 to 0.2
* encoder length `L`: 64 to 128 timesteps
* decoder length `H`: 4 to 8 timesteps
* latent state size: 16 or 32
* batch size: as large as memory allows while preserving sequence diversity

TFT is a relatively large model for time series, and public implementations also note that it performs better with sufficient data and capacity. ([PyTorch Forecasting — TFT tutorial](https://pytorch-forecasting.readthedocs.io/en/v1.4.0/tutorials/stallion.html))

---

## 10. Quantile output head

The output head predicts quantiles for each horizon. Recommended quantiles:

* 0.1
* 0.5
* 0.9

Optionally expand later to:

* 0.05
* 0.25
* 0.5
* 0.75
* 0.95

Training loss is the sum of **pinball losses** across horizons and quantiles. TFT’s original training setup uses quantile loss; production libraries also treat probabilistic quantile forecasting as the default TFT mode. ([ScienceDirect — TFT](https://www.sciencedirect.com/science/article/pii/S0169207021000637))

---

## 11. Loss function

Primary training objective:

* multi-horizon quantile loss on future log returns

Optional auxiliary terms:

* monotonic quantile crossing penalty
* forecast smoothness regularizer across horizons
* calibration penalty if interval coverage is poor

Do not use plain MSE as the primary objective. Recent 2026 work even highlights failure modes of transformer-based financial forecasting under squared-loss settings, which is another reason not to default to a naive point-forecast objective. ([Forecast collapse under squared loss](https://arxiv.org/abs/2604.00064))

---

## 12. Ensemble design

The model should not be deployed as a single TFT instance. Build a small ensemble.

### 12.1 Ensemble members

Train 3 to 5 TFT variants with:

* different random seeds
* slightly different encoder lengths
* slightly different dropout values
* optionally one variant with a slightly larger latent encoder

### 12.2 Ensemble output

At inference:

* average quantile forecasts, or
* average median forecast and uncertainty widths separately

Ensembling is a robust production tactic because financial models are sensitive to initialization and regime shifts. Recent finance benchmarks explicitly evaluate robustness to random seed selection, which makes seed-based ensembling especially relevant. Broader forecasting literature also supports ensembling as a robustness tool under distributional shifts. ([Deep learning for financial time series benchmark](https://arxiv.org/abs/2603.01820))

---

## 13. Optional second-phase expert routing

This is a phase-two enhancement, not required for v1.

After the soft-regime-conditioned TFT is stable, you may replace the single TFT core with a **small expert family**:

* one TFT expert more specialized for trend
* one TFT expert more specialized for chop
* one generalist TFT

A lightweight gating module uses the regime probabilities and recent latent state to blend expert outputs. This idea is supported directionally by newer time-series MoE work and by adaptive TFT papers that split series into pattern categories, though the exact architecture there is not standard TFT+MoE. Because MoE designs are more complex and easier to overfit, they belong in v2, not v1. ([Adaptive TFT for cryptocurrency](https://arxiv.org/abs/2509.10542))

---

## 14. Dataset construction

Training examples are built as sliding windows.

For each anchor time `t`:

* encoder input = observed history from `t-L+1` to `t`
* known future inputs = calendar/cyclic features from `t+1` to `t+H`
* target = future return sequence from `t+1` to `t+H`

Strictly avoid leakage:

* no future normalization stats
* no future-derived indicators in the encoder block
* no train/validation overlap via sequence bleed across walk-forward splits

This is especially important in finance, where small leakage errors can produce completely misleading results. ([Deep learning for financial time series benchmark](https://arxiv.org/abs/2603.01820))

---

## 15. Walk-forward training protocol

Use **walk-forward retraining**, not one static train/test split.

Recommended protocol:

1. choose a training window
2. train ensemble members on that window
3. validate on the next contiguous validation block
4. test on the next unseen block
5. roll forward
6. repeat

This gives a realistic estimate of stability under regime changes. Recent financial benchmarks emphasize evaluation across multiple market regimes, robustness diagnostics, and transaction-cost-aware analysis rather than one lucky split. ([Deep learning for financial time series benchmark](https://arxiv.org/abs/2603.01820))

---

## 16. Data augmentation and balancing

Do not use aggressive synthetic augmentation in v1. The first priority is clean regime coverage and enough samples across different volatility states.

You may, however:

* oversample rare but important regime windows in training batches
* ensure batch diversity across regimes
* balance high-volatility and low-volatility samples

This is preferable to naive GAN-style augmentation for the initial system. Recent finance augmentation work exists, but it is not necessary for a first production TFT forecaster. ([Financial time series augmentation](https://arxiv.org/abs/2602.17865))

---

## 17. Model diagnostics

The TFT pipeline should expose diagnostics after every retrain:

* quantile coverage error
* directional hit rate by horizon
* calibration of uncertainty width
* feature importance / variable selection weights
* attention maps
* performance broken down by regime
* performance broken down by time-of-day bucket
* ensemble dispersion

Interpretability is one of TFT’s selling points, not a side feature. The original TFT paper explicitly emphasizes variable selection and interpretable temporal dynamics. Use that. ([Temporal Fusion Transformers (original)](https://arxiv.org/abs/1912.09363))

---

## 18. Prediction-to-signal interface

The TFT world model does not directly emit buy/sell. It emits:

* future return quantiles over `H` steps
* uncertainty interval widths
* optional regime-conditioned confidence score

A downstream signal layer converts this into tradable scores. For example:

* expected move score = `q50`
* confidence score = `q50 / (q90 - q10 + ε)`
* trade eligibility requires interval width below a threshold
* signal may also depend on agreement across ensemble members

That keeps forecasting and trading policy decoupled, which is the safer and more modular design. TFT remains the predictive engine only. This is consistent with how forecasting models are typically wrapped in practical trading systems. ([Deep learning for financial time series benchmark](https://arxiv.org/abs/2603.01820))

---

## 19. Live inference pipeline

At runtime, the forecasting service should operate as follows:

1. ingest latest market bar
2. update rolling features
3. update regime probabilities
4. update rolling normalization stats
5. construct encoder window
6. construct known future time features for the forecast horizon
7. run latent encoder
8. run each ensemble TFT
9. aggregate quantile forecasts
10. publish world-model output to the policy layer

Inference should be deterministic given the current state and model snapshot. Online learning is not required at every inference pass. Retraining should happen on a scheduled cadence or when triggered by model drift metrics.

---

## 20. Retraining cadence

Recommended retraining policy:

* light refresh: daily or every few hours, depending on cadence and data volume
* full ensemble refresh: less frequent, such as daily or weekly
* emergency refresh: triggered by sharp degradation in calibration or regime-specific performance

Do not do per-step retraining. That is unnecessary and unstable. The model should infer every step and retrain in controlled batches.

---

## 21. Failure controls

The forecasting service should refuse to produce “high-confidence” outputs when:

* quantile intervals become abnormally wide
* ensemble disagreement exceeds threshold
* current feature values are strongly out-of-distribution relative to training
* market feed is incomplete or missing
* normalization stats are unstable due to insufficient fresh data

This is especially important in finance because model failure often looks like overconfidence, not obvious crashes.

---

## 22. What is explicitly excluded from this spec

The following are intentionally excluded from v1:

* cross-asset features
* text/news fusion
* direct RL inside the TFT training loop
* very large MoE systems
* foundation-model pretraining
* raw OHLC target prediction

Those may be useful later, but this spec is focused on the strongest single-asset TFT build without overcomplicating the system.

---

## 23. Final reference implementation

The recommended v1 system is:

**Base cadence:** 15 seconds or 1 minute  
**Target:** multi-horizon future log-return quantiles  
**Observed features:** returns, vol, momentum, volume, range, optional spread  
**Known future features:** sine/cosine minute, hour, day-of-week, session flags  
**Static/slow features:** asset/exchange ID placeholders, slow regime summary  
**Advanced upgrades:** soft regime conditioning, regime-aware normalization, CNN latent encoder, 3–5 member TFT ensemble  
**Core model:** TFT with VSNs, gating, recurrent local processing, interpretable attention, probabilistic head  
**Training:** walk-forward, quantile loss, no leakage  
**Output:** return quantiles and uncertainty for downstream policy conversion  

That is the cleanest production-ready TFT specification here because it preserves what TFT is good at while adding the advanced mechanisms that are most defensible from current finance and forecasting research: regime adaptation, richer temporal representation, probabilistic calibration, and ensemble robustness. ([Temporal Fusion Transformers (original)](https://arxiv.org/abs/1912.09363))

---

## Next step (engineering)

This can be turned into a code-oriented engineering spec with exact tensor shapes, PyTorch module boundaries, and config fields.

---

## References

1. Lim, B., et al. “Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting.” *arXiv:1912.09363*. https://arxiv.org/abs/1912.09363  
2. “Adaptive Temporal Fusion Transformers for Cryptocurrency Price Prediction.” *arXiv:2509.10542*. https://arxiv.org/abs/2509.10542  
3. “Deep Learning for Financial Time Series: A Large-Scale Benchmark of Risk-Adjusted Performance.” *arXiv:2603.01820*. https://arxiv.org/abs/2603.01820  
4. PyTorch Forecasting. “Demand forecasting with the Temporal Fusion Transformer.” Tutorial (v1.4.0). https://pytorch-forecasting.readthedocs.io/en/v1.4.0/tutorials/stallion.html  
5. *International Journal of Forecasting* / ScienceDirect — TFT interpretable multi-horizon work. https://www.sciencedirect.com/science/article/pii/S0169207021000637  
6. “Forecast collapse of transformer-based models under …” *arXiv:2604.00064*. https://arxiv.org/abs/2604.00064  
7. “Financial time series augmentation using transformer …” *arXiv:2602.17865*. https://arxiv.org/abs/2602.17865  
