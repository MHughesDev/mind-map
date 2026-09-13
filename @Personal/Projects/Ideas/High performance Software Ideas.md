Here's a list of HPC-oriented software project ideas that build on your trading platform experience while pushing you deeper into big data, high-throughput parallelism, and low-latency systems.

**1. Distributed Real-Time Analytics Engine** A system that ingests high-volume event streams (IoT sensors, clickstreams, telemetry) and computes rolling aggregations, percentiles, and anomaly scores in sub-millisecond windows. You'd build a sharded ingestion layer, a parallel compute tier using something like a partitioned actor model, and a REST API exposing query endpoints and dashboards. The front end would show live-updating charts via Server-Sent Events or WebSockets layered over the REST core. This is the closest analog to your trading work but generalizes the aggregation/low-latency muscles.

**2. Parallel Backtesting / Simulation Grid** A compute grid that runs thousands of independent simulations (Monte Carlo, parameter sweeps, agent-based models) across a worker pool. The REST layer accepts job submissions, partitions the parameter space, dispatches to workers, and streams results back. You'd learn work-stealing schedulers, result reduction, and fault-tolerant job recovery. A UI lets users define parameter ranges and visualize the result surface. Directly leverages your trading domain since backtesting is a natural fit.

**3. Time-Series Database with a Query API** Build a columnar, append-optimized store tuned for ingesting millions of timestamped points per second, with downsampling, retention policies, and parallel range scans. REST endpoints handle writes and PromQL-style queries. This teaches memory-mapped I/O, lock-free ring buffers, compression (delta-of-delta, Gorilla), and cache-friendly data layout—core low-latency skills.

**4. Stream Processing Framework (mini-Flink)** A framework where users define directed acyclic graphs of operators (map, filter, window, join) that execute in parallel across partitions with exactly-once semantics and checkpointing. The REST API submits topologies and reports operator-level metrics. This is the deepest parallelism project—you'll wrestle with backpressure, state management, and watermarks.

**5. Distributed In-Memory Cache / KV Store** A sharded, replicated key-value store with consistent hashing, configurable consistency levels, and a binary protocol fronted by a REST admin/query API. You'll implement replication, failure detection (gossip), and tail-latency optimization. Great for learning the networking and concurrency primitives underneath everything else.

**6. Order Book Matching Engine as a Service** A standalone, ultra-low-latency matching engine exposing REST for order entry and a streaming feed for market data—essentially extracting and hardening the hottest path of a trading platform into a benchmarkable, lock-free component. You'd focus on single-threaded hot loops, NUMA awareness, and microbenchmarking. Highest overlap with what you've already built, but pushes latency rigor much further.

**7. Parallel Log/Data Pipeline (ETL at Scale)** A high-throughput ingestion and transformation pipeline that reads from sources (Kafka, files, sockets), applies parallel transforms, and sinks to storage, with a REST control plane for pipeline config and monitoring. Teaches batching, partitioning strategies, and throughput tuning.

A few notes on sequencing and stack choices, since they matter for skill growth:

If your trading platform was in a managed language, consider doing one of these (the matching engine or time-series DB) in Rust or C++ to confront low-latency realities directly—allocation control, cache lines, lock-free structures. The analytics engine and stream framework are better in a managed language first so you can focus on distributed-systems concepts rather than fighting memory.

For ordering, I'd suggest: start with the time-series DB or in-memory KV store (foundational storage/concurrency), then the analytics engine or backtesting grid (distributed compute on top), then the stream framework (the capstone that combines everything).

Want me to go deeper on any one of these—sketch out an architecture, suggest a concrete tech stack, or define a phased milestone plan? I can also tailor recommendations if you tell me what language your trading platform used and which dimension (latency vs. throughput vs. parallelism) you most want to stretch.