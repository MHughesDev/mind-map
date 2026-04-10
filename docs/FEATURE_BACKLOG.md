# Feature backlog

Prioritized ideas and scoped work items. This is not a commitment order; reorder as needed.

| Priority | Item | Notes |
|----------|------|--------|
| P1 | **TFT-only forecasting pipeline** | Refocus the trading / market stack so the forecasting path is **only** the Temporal Fusion Transformer (TFT) module and its documented interfaces (feature builder → latent encoder → regime → TFT → quantiles → ensemble). No parallel forecaster families in the same pipeline until explicitly re-scoped. Full spec: [human_provided_spec/TFT_Forecasting_Pipeline_Spec.md](human_provided_spec/TFT_Forecasting_Pipeline_Spec.md). |
