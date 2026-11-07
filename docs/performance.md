# Performance envelope

SparkPrompt accepts at most 200 domain characters, 1,000 skill-description characters, and 8,000 characters each for a learner prompt or generated exercise. Provider calls have 60-second client timeouts, 4,096 output-token caps, and 32,000 response-character caps.

Each exercise uses one provider call; evaluation and refinement use two sequential calls. Release measurements record provider fake-client overhead separately from live-provider latency. No release may claim a live latency guarantee because model, region, quota, and account tier are outside the application boundary. A release is blocked by removal of enforced limits, unbounded retries, or a 2× local fake-client regression without explanation.
