# Memory, Cost, and Latency Budget

> Section of **Predictive-Extension Architecture > Memory, Cost, and Latency Budget**
>
> Generated from the Word document -- **do not edit.** Edit the OneDrive `.docx`; this file is rewritten on every snapshot.

---

The four-gigabyte ceiling is respected by construction: data and one model are held in memory at a time, the language model is accessed by API rather than loaded, and intermediate artefacts are released after use. Memory is reported by RSS; cost (API tokens) and latency (wall-clock, including tool round-trips) are tracked as the secondary SRQ4 dimensions. The per-component budget, measured by RSS on the local pipeline over the largest category (CSD), is summarised in  **Table** **6**.
| Component | Peak RAM (RSS) | When |
|---|---|---|
| Python runtime and libraries (numpy, pandas, LightGBM, XGBoost, scikit-learn) | ~194 MB | Always |
| Coordinator state (typed state passed between components) | < 1 MB | Always |
| Nielsen data (per category, largest = CSD) | ~15 MB | Data loading |
| Active model (one at a time; XGBoost ≈15, LightGBM ≈7, Ridge < 1 MB) | ~15 MB | Forecasting |
| Agentic layer (remote API; no weights loaded, network buffer only) | negligible | Synthesis |
| End-to-end peak | ~231 MB | Forecasting |
**Table** **6** - Per-component budget, measured by RSS (psutil), 2026-06-27
The end-to-end peak of approximately 231 MB is about 2.8% of the eight-gigabyte budget. The budget therefore binds the model-selection space (excluding transformer and locally hosted LLM options up front) rather than the final footprint; the realised footprint sits two orders of magnitude below the ceiling because the language model is kept out of process by the remote-API design and only one lightweight model is resident at a time.
