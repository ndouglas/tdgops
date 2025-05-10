# tdgops
A proof-of-concept of a type-directed, goal-oriented programming system.

As usual for me, this is a pretty simple idea but I think it's interesting: a declarative programming system that uses an expressive type-and-constraint system to compile high-level problem descriptions into a Pareto frontier of implementation strategies. It searches a graph of typed transformations—like those found in LeetCode-style algorithm problems—to generate candidate solutions optimized along dimensions like time, space, and purity. The system can either select the best path at compile time or defer the tradeoff to runtime based on context.

