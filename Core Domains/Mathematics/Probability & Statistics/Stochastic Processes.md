---
title: Stochastic Processes
type: learning-topic
domain: Mathematics
subdomain: Probability & Statistics
status: in-progress
tags: [mathematics, probability]
---

## Big Picture

A **stochastic process** is a random system that changes over time.

The word **stochastic** means random or probabilistic. The word **process** means something that evolves, develops, or changes. So when we put them together, a stochastic process is any system where the state changes through time and randomness is involved.

At the highest level, this subject is about answering questions like:

- What can happen next?
    
- How likely is each future outcome?
    
- Does the future depend only on the present?
    
- Does the past still matter?
    
- Can we simulate this system?
    
- Can we predict its average behavior?
    
- Can we model risk?
    

A stochastic process is one of the most important ideas in probability because it lets us model real systems that are not perfectly predictable.

Examples include:

- Stock prices moving through time
    
- Weather changing from day to day
    
- Customers arriving at a store
    
- Orders arriving at an exchange
    
- Network packets arriving at a server
    
- A robot moving through uncertain terrain
    
- A queue growing and shrinking
    
- A machine failing randomly
    
- A population growing with random births and deaths
    
- A gambling account going up and down
    

A single random variable describes uncertainty at one moment. A stochastic process describes uncertainty across many moments.

---

# High-Level Hierarchy

```text
Mathematics
│
└── Probability Theory
    │
    ├── Random Variables
    │
    ├── Probability Distributions
    │
    ├── Conditional Probability
    │
    ├── Expected Value
    │
    └── Stochastic Processes
        │
        ├── Markov Processes
        │   │
        │   ├── Markov Chains
        │   ├── Brownian Motion
        │   ├── Hidden Markov Models
        │   └── Diffusion Processes
        │
        ├── Poisson Processes
        │
        ├── Random Walks
        │
        ├── Martingales
        │
        ├── Time Series Processes
        │
        └── Non-Markov Processes
```

The further down the hierarchy you go, the more specific the process becomes.

The most general idea is:

```text
Stochastic Process = Randomness evolving through time
```

A Markov process adds a restriction:

```text
Future depends only on the present state
```

A Markov chain adds another restriction:

```text
Future depends only on the present state, and the state space is discrete
```

Brownian motion is also Markov, but it is not a Markov chain because its state space is continuous.

---

# Random Variables

## What Is a Random Variable?

A **random variable** is a value whose outcome is uncertain.

It is called a variable because it can take different values. It is called random because we do not know which value it will take before the outcome happens.

Examples:

```text
Coin Flip:

X = Heads or Tails
```

```text
Die Roll:

X = 1, 2, 3, 4, 5, or 6
```

```text
Daily Stock Return:

X = -2.4%, 0.3%, 1.7%, etc.
```

```text
Number of Customers in One Hour:

X = 0, 1, 2, 3, 4, ...
```

A random variable describes uncertainty at a single point.

For example, if we ask:

```text
What will tomorrow's stock return be?
```

that is one random variable.

But if we ask:

```text
What will the stock price be every day for the next year?
```

now we are dealing with a stochastic process.

---

# From Random Variables to Stochastic Processes

A single random variable might be written as:

```text
X
```

A stochastic process is a whole sequence or family of random variables:

```text
X₀, X₁, X₂, X₃, ...
```

or:

```text
X(t)
```

where `t` represents time.

For example:

```text
X₀ = today's price
X₁ = tomorrow's price
X₂ = price two days from now
X₃ = price three days from now
```

Each value is random because the future is uncertain.

The process is the entire evolving system.

---

# Definition of a Stochastic Process

A **stochastic process** is a collection of random variables indexed by time.

Written formally:

```text
{X(t) : t ∈ T}
```

or:

```text
{X_t}
```

where:

```text
t = time
X_t = the random state of the system at time t
```

In plain English:

> A stochastic process is a random path through time.

---

# Intuitive Examples

## Example 1: Coin Flips Over Time

A single coin flip is a random variable.

A sequence of coin flips is a stochastic process.

```text
Time:    1   2   3   4   5   6
Result:  H   T   H   H   T   T
```

Each time step has a random outcome.

The process is the full sequence.

---

## Example 2: A Gambler's Wealth

Suppose you start with $10.

Each round:

- Win: gain $1
    
- Lose: lose $1
    

Possible path:

```text
Time:    0   1   2   3   4   5
Money:  10  11  10   9  10  11
```

This is a stochastic process because your wealth evolves through time and each round is random.

---

## Example 3: Stock Price

A stock price changes every second, minute, hour, or day.

```text
Time:   Mon   Tue   Wed   Thu   Fri
Price:  100   101    99   103   102
```

The future price is uncertain, but we can model probabilities.

This is one reason stochastic processes are central to quantitative finance.

---

## Example 4: Customers Arriving at a Store

Suppose customers arrive randomly.

```text
Minute:      1   2   3   4   5
Arrivals:    0   2   1   0   3
```

The number of arrivals each minute is random.

The process tracks arrivals through time.

This type of example leads naturally into Poisson processes and queueing theory.

---

## Example 5: Network Packets

A server receives packets at random times.

```text
Time 0.001s: packet arrives
Time 0.004s: packet arrives
Time 0.011s: packet arrives
Time 0.020s: no packet
```

This is important in networking, distributed systems, exchange connectivity, and low-latency systems.

---

## Example 6: Orders Arriving on an Exchange

A trading venue receives random buy orders, sell orders, cancellations, and modifications.

```text
10:30:00.001 - Buy order arrives
10:30:00.002 - Cancel order arrives
10:30:00.004 - Sell order arrives
10:30:00.006 - Trade occurs
```

The order book is a stochastic system because it changes through time under random order flow.

This is directly connected to market microstructure and trading system simulation.

---

# Discrete Time vs Continuous Time

One way to classify stochastic processes is by how time is measured.

## Discrete-Time Process

Time moves in steps.

Examples:

```text
t = 0, 1, 2, 3, 4, ...
```

This is useful for:

- Daily stock prices
    
- Monthly sales
    
- Yearly population counts
    
- Turn-based games
    
- Discrete simulations
    
- Bar data in trading
    

Example:

```text
Day 0: $100
Day 1: $102
Day 2: $101
Day 3: $105
```

A discrete-time process only updates at specific time steps.

---

## Continuous-Time Process

Time flows continuously.

Examples:

```text
t = 0.001
t = 0.002
t = 0.002348
t = 0.002349
```

This is useful for:

- Physics
    
- Brownian motion
    
- Network events
    
- Exchange order flow
    
- Real-time trading
    
- Sensor data
    
- Queueing systems
    

Example:

```text
10:30:00.000001
10:30:00.000002
10:30:00.000003
```

In continuous time, events can happen at any moment.

---

# Discrete State vs Continuous State

Another classification is the type of values the process can take.

## Discrete State Space

The state can only be one of a countable set of values.

Examples:

```text
Sunny
Rainy
Cloudy
```

```text
Bull Market
Bear Market
Sideways Market
```

```text
0 customers
1 customer
2 customers
3 customers
```

Discrete states are like labeled boxes.

The process jumps from one box to another.

---

## Continuous State Space

The state can be any real number within some range.

Examples:

```text
Temperature = 72.348 degrees
```

```text
Stock price = 103.48291
```

```text
Position = -0.38173
```

Continuous states are not limited to distinct categories.

The process can move through infinitely many possible values.

---

# Four Major Types

Combining time and state gives four broad categories:

```text
1. Discrete Time, Discrete State

Example:
Markov chain for weather.

2. Discrete Time, Continuous State

Example:
Daily stock returns.

3. Continuous Time, Discrete State

Example:
Number of people in a queue.

4. Continuous Time, Continuous State

Example:
Brownian motion.
```

This classification helps you understand where different stochastic models fit.

---

# The Markov Property

The **Markov property** is one of the most important ideas in stochastic processes.

A process has the Markov property if:

```text
P(Future | Present, Past) = P(Future | Present)
```

In plain English:

> Once you know the current state, the past does not provide any additional information about the future.

That does not mean the past never mattered. It means the past has already been summarized into the current state.

---

# Intuitive Explanation of Markov

Imagine a board game.

You are on square 10.

The next move depends only on:

```text
Current square = 10
Next dice roll
```

It does not matter how you got to square 10.

You could have arrived from square 8, square 9, or square 4. Once you are on square 10, the rules for the next step are the same.

That is Markov.

---

# Non-Markov Example

Now imagine a game where your next move depends on how many times you have visited the square before.

If you are on square 10, but the rules depend on whether this is your first, second, or tenth time on square 10, then the past matters.

The current state alone is not enough.

That is non-Markov unless you expand the state to include visit count.

For example:

```text
State = current square
```

might be non-Markov.

But:

```text
State = current square + number of previous visits
```

could become Markov.

This is a very important idea.

A process can sometimes be made Markov by defining the state more completely.

---

# State Design

The phrase:

```text
The future depends only on the present
```

can be misleading.

A better version is:

```text
The future depends only on the present state, if the present state contains all relevant information.
```

For example, in trading, if your state is only:

```text
State = current price
```

that may not be enough.

But if your state is:

```text
State =
- Current price
- Current spread
- Order book imbalance
- Volatility estimate
- Recent trade flow
- Current inventory
```

then the state contains much more information.

This expanded state may make the system closer to Markov.

This same idea appears in:

- Reinforcement learning
    
- Robotics
    
- Control systems
    
- Trading systems
    
- Forecasting
    
- Hidden Markov models
    
- State-space models
    

---

# Markov Processes

A **Markov process** is a stochastic process that satisfies the Markov property.

All Markov processes are stochastic processes.

But not all stochastic processes are Markov processes.

```text
Stochastic Process
│
└── Markov Process
```

A Markov process says:

```text
Present state contains all relevant information for predicting the future.
```

Examples:

- Markov chains
    
- Brownian motion
    
- Certain diffusion processes
    
- Some queueing models
    
- Some state-space models
    

---

# Markov Chains

A **Markov chain** is a Markov process with a discrete state space.

It moves between distinct states.

Example states:

```text
Sunny
Rainy
Cloudy
```

or:

```text
Bull
Bear
Sideways
```

or:

```text
0 customers
1 customer
2 customers
3 customers
```

The process moves from one state to another according to probabilities.

---

# Weather Markov Chain Example

Suppose the weather can be:

```text
Sunny
Rainy
Cloudy
```

If today is sunny:

```text
70% chance tomorrow is sunny
20% chance tomorrow is cloudy
10% chance tomorrow is rainy
```

If today is rainy:

```text
40% chance tomorrow is rainy
40% chance tomorrow is cloudy
20% chance tomorrow is sunny
```

If today is cloudy:

```text
40% chance tomorrow is cloudy
30% chance tomorrow is sunny
30% chance tomorrow is rainy
```

This is Markov if tomorrow's weather depends only on today's weather.

---

# Transition Matrix

A Markov chain is often represented using a transition matrix.

```text
             Tomorrow
          Sunny Cloudy Rainy
Today
Sunny      0.70   0.20  0.10
Cloudy     0.30   0.40  0.30
Rainy      0.20   0.40  0.40
```

Each row sums to 1.

That is because if you are currently in one state, the process must go somewhere next.

---

# Market Regime Markov Chain Example

In finance, you might model the market as being in one of three states:

```text
Bull Market
Bear Market
Sideways Market
```

Example transition matrix:

```text
                    Tomorrow
              Bull   Bear   Sideways
Today
Bull          0.85   0.05     0.10
Bear          0.10   0.80     0.10
Sideways      0.25   0.15     0.60
```

This model says if the market is currently bullish, it is likely to remain bullish tomorrow. If it is bearish, it is likely to remain bearish.

This kind of model is simple, but it introduces a powerful idea:

```text
Markets can move between regimes.
```

---

# Random Walks

A **random walk** is one of the simplest stochastic processes.

Start at 0.

At each step:

```text
50% chance of +1
50% chance of -1
```

Example path:

```text
Time:      0   1   2   3   4   5   6
Position:  0   1   2   1   0  -1   0
```

Another possible path:

```text
Time:      0   1   2   3   4   5   6
Position:  0  -1  -2  -1  -2  -3  -2
```

The rules are the same, but the realized path is different each time.

---

# Why Random Walks Matter

Random walks matter because they are the foundation for many more advanced models.

If the steps get smaller and happen more frequently, a random walk begins to resemble Brownian motion.

Random walks also appear in:

- Gambling
    
- Stock price modeling
    
- Physics
    
- Search algorithms
    
- Diffusion
    
- Genetics
    
- Queueing
    
- Monte Carlo simulation
    

In finance, a basic random walk idea says:

```text
Tomorrow's price change is random.
```

This is not a complete model of markets, but it is a useful starting point.

---

# Brownian Motion

**Brownian motion** is a continuous-time, continuous-state stochastic process.

It can be thought of as the limiting version of a random walk where:

- Time steps become extremely small
    
- Movement steps become extremely small
    
- The process becomes continuous
    

Brownian motion produces paths that look jagged and random, but still continuous.

It is one of the central models in:

- Physics
    
- Probability theory
    
- Quantitative finance
    
- Stochastic calculus
    
- Option pricing
    

---

# Brownian Motion Is Markov

Brownian motion is a Markov process.

That means:

```text
P(Future | Present, Past) = P(Future | Present)
```

If Brownian motion is currently at position 10, then to describe its future distribution, you only need to know that current position.

The path it took to reach 10 does not matter.

---

# Brownian Motion Is Not a Markov Chain

Brownian motion is not a Markov chain.

Why?

Because a Markov chain has a discrete state space.

Brownian motion has a continuous state space.

A Markov chain might have states like:

```text
Bull
Bear
Sideways
```

Brownian motion has states like:

```text
1.38291
1.38292
1.38293
```

It can take any real-valued position.

So:

```text
Brownian Motion = Markov Process
Brownian Motion ≠ Markov Chain
```

---

# Geometric Brownian Motion

Brownian motion can go negative because it moves on the real number line.

But stock prices cannot go below zero.

So in finance, a common model is **geometric Brownian motion**.

The rough idea is:

```text
Price changes by random percentages, not random dollar amounts.
```

Instead of:

```text
Price = Price + Random Change
```

we use:

```text
Price = Price × Random Factor
```

This keeps prices positive.

Geometric Brownian motion is used in the Black-Scholes model and many basic financial models.

It is not a perfect model of markets, but it is historically important.

---

# Poisson Processes

A **Poisson process** models random event arrivals through time.

It answers questions like:

```text
How many events happen during a time interval?
```

Examples:

- Customers arriving at a store
    
- Cars arriving at a toll booth
    
- Packets arriving at a server
    
- Orders arriving at an exchange
    
- Calls arriving at a call center
    
- Machine failures
    
- Radioactive decay events
    

---

# Store Arrival Example

Suppose a store receives an average of 12 customers per hour.

That does not mean exactly one customer arrives every 5 minutes.

The actual arrivals are random.

One hour might look like:

```text
Minute 1: 0 customers
Minute 2: 1 customer
Minute 3: 0 customers
Minute 4: 3 customers
Minute 5: 0 customers
```

The average rate is stable, but the exact timing is random.

That is what a Poisson process models.

---

# Exchange Order Arrival Example

Suppose an exchange receives an average of 1,000 orders per second.

The exact arrival times are not evenly spaced.

Some microseconds may have many orders.

Some may have none.

A simple first approximation might use a Poisson process to model:

- Buy order arrivals
    
- Sell order arrivals
    
- Cancellation arrivals
    
- Market order arrivals
    

Real markets are more complex than a basic Poisson process, but the Poisson process is a useful starting model.

---

# Queueing Example

Imagine a coffee shop.

Customers arrive randomly.

Workers serve customers.

The line length changes through time.

```text
Line Length(t)
```

is a stochastic process.

It increases when customers arrive.

It decreases when customers are served.

This connects stochastic processes to queueing theory.

Queueing theory matters in:

- Retail
    
- Manufacturing
    
- Cloud computing
    
- Networking
    
- Operating systems
    
- Trading infrastructure
    

---

# Martingales

A **martingale** is a stochastic process where your best prediction of the future value is the current value.

In simple terms:

```text
No expected edge.
```

Example:

You are playing a fair betting game.

You start with $100.

Each round:

- 50% chance you win $1
    
- 50% chance you lose $1
    

Your wealth moves randomly.

But your expected wealth after the next round is still $100.

That is a martingale.

---

# Martingale Intuition

A martingale does not mean the value cannot move.

It can move a lot.

It means the expected future value, given what you know now, equals the current value.

So:

```text
Expected Tomorrow Value = Today's Value
```

This is important in finance because many no-arbitrage pricing ideas are connected to martingales.

If a price process were predictably biased in a risk-free way, traders could exploit it.

---

# Hidden Markov Models

A **Hidden Markov Model**, or HMM, is a model where the true state is hidden, but it produces observable outputs.

The hidden state follows a Markov chain.

The observed data is noisy evidence of the hidden state.

---

# Hidden Markov Model Example

Suppose the true market regime is one of:

```text
Bull
Bear
Sideways
```

But you cannot observe the regime directly.

Instead, you observe:

```text
Price returns
Volume
Volatility
Spread
Trend strength
```

The HMM tries to infer the hidden state from the observed data.

This is useful because the market may behave differently depending on the hidden regime.

---

# Medical Example of HMM

Hidden state:

```text
Healthy
Sick
Recovering
```

Observed symptoms:

```text
Temperature
Cough
Fatigue
Blood test result
```

The doctor cannot directly observe the true internal state, but symptoms provide evidence.

This same logic applies to markets, robots, speech recognition, and sensor systems.

---

# Time Series Processes

A **time series** is data observed over time.

Many time series are stochastic processes.

Examples:

- Daily sales
    
- Monthly revenue
    
- Hourly temperature
    
- Stock returns
    
- CPU usage
    
- Website traffic
    
- Electricity demand
    

Some time series models are Markov.

Some are not.

---

# AR(1) Process

An AR(1) process means the next value depends on the previous value plus noise.

```text
X(t) = aX(t-1) + Noise
```

This is Markov if the current state is just `X(t)`.

Why?

Because the next value only needs the current value.

---

# AR(p) Process

An AR(p) process depends on multiple past values.

Example:

```text
X(t) depends on:
X(t-1)
X(t-2)
X(t-3)
```

If your state is only `X(t-1)`, this is not Markov.

But you can make it Markov by expanding the state:

```text
State(t) =
X(t)
X(t-1)
X(t-2)
```

This is another example of state design.

The process may become Markov if the state includes enough history.

---

# Non-Markov Processes

A non-Markov process is a stochastic process where the current state alone is not enough to predict the future distribution.

Example:

```text
X(t+1) = average of all previous values + noise
```

To predict the future, you need the whole history.

The current value alone does not tell you enough.

---

# Long-Memory Example

Suppose today's market volatility depends on volatility over the last 100 days.

If your state only includes today's volatility, the process may be non-Markov.

But if your state includes:

```text
Current volatility
100-day volatility average
Recent return history
```

then you have packed more past information into the present state.

This is why defining the state correctly is so important.

---

# Stochastic Calculus

Stochastic calculus is an advanced area that studies calculus with random processes, especially Brownian motion.

Normal calculus deals with smooth change.

Stochastic calculus deals with random jagged change.

In normal calculus, you might write:

```text
dx/dt
```

In stochastic calculus, you see expressions involving:

```text
dW
```

where:

```text
W = Brownian motion
```

This is the language behind:

- Black-Scholes
    
- Option pricing
    
- Financial engineering
    
- Diffusion models
    
- Continuous-time stochastic systems
    

---

# Why Stochastic Calculus Is Hard

Brownian motion is continuous, but it is extremely rough.

Its paths are not smooth like normal curves.

That means ordinary calculus does not work cleanly.

Stochastic calculus was created to handle this kind of randomness.

For most practical systems work, you do not need to start here. But for deep quantitative finance, especially derivatives pricing, stochastic calculus becomes important.

---

# How This Applies to Quantitative Finance

Stochastic processes are everywhere in quant finance.

## Price Modeling

Stock prices, interest rates, volatility, and exchange rates can all be modeled as stochastic processes.

Examples:

```text
Stock Price(t)
Interest Rate(t)
Volatility(t)
Spread(t)
```

The purpose is not to perfectly predict the future. The purpose is to describe uncertainty and make better decisions under uncertainty.

---

## Risk Modeling

Risk is fundamentally about future uncertainty.

A portfolio's value tomorrow is random.

A stochastic process lets us model possible future paths.

For example:

```text
Path 1: Portfolio rises 2%
Path 2: Portfolio falls 1%
Path 3: Portfolio falls 8%
Path 4: Portfolio rises 0.5%
```

Risk systems care about the distribution of possible outcomes.

---

## Option Pricing

Options are valuable because the future price of the underlying asset is uncertain.

Stochastic processes model that uncertainty.

This is why Brownian motion and geometric Brownian motion became central to option pricing.

---

## Market Regimes

Markets may switch between regimes:

```text
Low volatility
High volatility
Trending
Mean reverting
Crisis
Normal
```

Markov chains and Hidden Markov Models can be used to model regime changes.

---

## Order Flow

Order arrivals, cancellations, and trades are stochastic.

A trading system might model:

```text
Limit order arrivals
Market order arrivals
Cancel events
Fill events
Latency variation
Queue position changes
```

This is where stochastic processes connect directly to market microstructure.

---

# How This Applies to Trading Systems

If you build a trading simulator, backtester, or exchange simulator, stochastic processes become practical engineering tools.

## Market Replay

Historical replay uses real past data.

But if you want synthetic testing, you need stochastic models to create fake-but-realistic market paths.

---

## Fill Simulation

A realistic paper trader must estimate whether your order would have been filled.

That may depend on:

- Queue position
    
- Order flow
    
- Trade arrivals
    
- Cancellations
    
- Latency
    
- Spread changes
    
- Volatility
    

All of those are stochastic.

---

## Latency Modeling

Latency is not perfectly constant.

A system might usually respond in 200 microseconds, but sometimes spike to 2 milliseconds.

That makes latency a stochastic process.

A realistic trading simulator should model latency variation.

---

## Order Book Simulation

An order book changes as orders arrive, cancel, and execute.

The full order book state is a stochastic process.

```text
OrderBook(t)
```

At each time, the book has:

- Bid prices
    
- Ask prices
    
- Bid sizes
    
- Ask sizes
    
- Queue depths
    
- Order priorities
    

The future book depends on random future order flow.

---

# Mental Model

The most useful mental model is:

```text
Random Variable:
One uncertain value.

Stochastic Process:
A timeline of uncertain values.

Markov Process:
A stochastic process where the present state is enough.

Markov Chain:
A Markov process with discrete states.

Brownian Motion:
A Markov process with continuous states.

Poisson Process:
A stochastic process for random event arrivals.

Martingale:
A stochastic process with no expected advantage.

Hidden Markov Model:
A Markov chain where the true state is hidden.
```

---

# Common Confusions

## Confusion 1: Is every stochastic process Markov?

No.

A stochastic process can depend on the entire past.

Markov processes are only one special category.

---

## Confusion 2: Is Brownian motion a Markov chain?

No.

Brownian motion is Markov, but it is not a Markov chain.

It is not a Markov chain because its state space is continuous.

---

## Confusion 3: Does Markov mean the past does not matter?

Not exactly.

It means the past does not matter once the current state is known.

The past may have shaped the current state.

But after the current state is known, the past adds no extra predictive information.

---

## Confusion 4: Can a non-Markov process become Markov?

Sometimes, yes.

If you expand the state to include enough history, a non-Markov-looking process can become Markov.

Example:

```text
Future depends on last 3 values.
```

If the state only includes the current value, it is not Markov.

But if the state includes the last 3 values, it can be Markov.

---

# Final Taxonomy

```text
Stochastic Process
│
├── Markov Processes
│   │
│   ├── Markov Chains
│   │   └── Discrete state space
│   │
│   ├── Brownian Motion
│   │   └── Continuous state space
│   │
│   ├── Hidden Markov Models
│   │   └── Hidden discrete states with noisy observations
│   │
│   └── Diffusion Processes
│       └── Continuous-time random motion
│
├── Poisson Processes
│   └── Random event arrivals
│
├── Martingales
│   └── No expected edge
│
├── Time Series Processes
│   └── Data evolving through time
│
└── Non-Markov Processes
    └── Future depends on more than the current state
```

---

# Key Takeaways

A random variable describes uncertainty at one moment.

A stochastic process describes uncertainty evolving through time.

A stochastic process is a collection of random variables indexed by time.

A stochastic process does not have to be Markov.

A stochastic process may depend on the current state, past states, the entire history, external inputs, or some combination of those.

A Markov process is a stochastic process where the future depends only on the current state.

The Markov property is:

```text
P(Future | Present, Past) = P(Future | Present)
```

A Markov chain is a Markov process with a discrete state space.

Brownian motion is a Markov process with a continuous state space.

Brownian motion is not a Markov chain.

A Poisson process models random event arrivals.

A martingale models a fair process where the expected future value equals the current value.

Hidden Markov Models are useful when the true state is hidden but produces observable signals.

In quantitative finance, stochastic processes are used for prices, volatility, regimes, order flow, risk, and option pricing.

In trading systems, stochastic processes are used for market replay, order book simulation, fill simulation, queue modeling, latency modeling, and risk simulation.