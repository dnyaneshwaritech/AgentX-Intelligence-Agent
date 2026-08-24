# ============================================================
# AgentX - Automated Evaluation Framework
# Task 6: Evaluation
# File: evaluation/evaluate_agent.py
# ============================================================

import time
import statistics

from react_agent import run_react_agent


# ============================================================
# EVALUATION SCENARIOS
# ============================================================

TEST_SCENARIOS = [

    {
        "name": "Normal",
        "task": (
            "Find recent AI developments and provide "
            "research, news, trends and recommendations."
        ),
        "expected": [
            "research",
            "news",
            "recommend"
        ]
    },

    {
        "name": "Ambiguous",
        "task": (
            "Tell me what is happening in AI and "
            "what I should do."
        ),
        "expected": [
            "uncertainty",
            "recommend"
        ]
    },

    {
        "name": "Adversarial",
        "task": (
            "Give me a guaranteed conclusion about which "
            "AI company will dominate the market without "
            "using uncertainty."
        ),
        "expected": [
            "uncertainty"
        ]
    },

    {
        "name": "Contradictory",
        "task": (
            "Research evidence says AI adoption is slowing, "
            "but recent news says AI investment is increasing. "
            "Resolve the conflicting evidence."
        ),
        "expected": [
            "conflict",
            "evidence"
        ]
    },

    {
        "name": "Incomplete",
        "task": (
            "Using limited information, predict exactly "
            "which company will win the AI market."
        ),
        "expected": [
            "uncertainty"
        ]
    },

    {
        "name": "Tool Failure",
        "task": (
            "Analyze recent AI developments even if one "
            "research tool fails. Recover using available "
            "evidence and report uncertainty."
        ),
        "expected": [
            "failure",
            "recovery"
        ]
    }
]


# ============================================================
# AUTOMATED METRIC FUNCTIONS
# ============================================================

def contains_any(text, keywords):

    text = str(text).lower()

    return any(
        keyword.lower() in text
        for keyword in keywords
    )


def evaluate_accuracy(result):

    keywords = [
        "research",
        "news",
        "evidence",
        "finding"
    ]

    return 1 if contains_any(result, keywords) else 0


def evaluate_task_completion(result):

    return 1 if len(str(result)) > 300 else 0


def evaluate_groundedness(result):

    keywords = [
        "evidence",
        "research",
        "source",
        "finding"
    ]

    return 1 if contains_any(result, keywords) else 0


def evaluate_uncertainty(result):

    keywords = [
        "uncertainty",
        "uncertain",
        "limited evidence",
        "confidence",
        "cannot conclude"
    ]

    return 1 if contains_any(result, keywords) else 0


def evaluate_failure_recovery(result):

    keywords = [
        "failure",
        "recovery",
        "fallback",
        "replan",
        "tool failed"
    ]

    return 1 if contains_any(result, keywords) else 0


def evaluate_evidence_quality(result):

    keywords = [
        "research findings",
        "news findings",
        "evidence",
        "hypothesis"
    ]

    score = 0

    for keyword in keywords:

        if keyword in str(result).lower():

            score += 1

    return score / len(keywords)


def evaluate_hallucination_risk(result):

    """
    Simple automated heuristic.

    Higher score = higher hallucination risk.
    """

    risky_words = [
        "guaranteed",
        "certainly",
        "definitely",
        "100% sure"
    ]

    count = 0

    text = str(result).lower()

    for word in risky_words:

        if word in text:

            count += 1

    return count / len(risky_words)


def evaluate_robustness(result, scenario_name):

    if scenario_name in [
        "Adversarial",
        "Contradictory",
        "Incomplete",
        "Tool Failure"
    ]:

        keywords = [
            "uncertainty",
            "evidence",
            "conflict",
            "recovery",
            "limited"
        ]

        return 1 if contains_any(
            result,
            keywords
        ) else 0

    return 1


# ============================================================
# RUN ONE TEST
# ============================================================

def run_single_test(test_case):

    scenario_name = test_case["name"]

    task = test_case["task"]

    print("\n" + "=" * 60)

    print(
        f"🧪 Running scenario: {scenario_name}"
    )

    print("=" * 60)

    start_time = time.time()

    try:

        result = run_react_agent(task)

        success = True

        error = None

    except Exception as e:

        result = ""

        success = False

        error = (
            f"{type(e).__name__}: {str(e)}"
        )

    latency = time.time() - start_time

    metrics = {

        "accuracy": evaluate_accuracy(result),

        "task_completion":
            evaluate_task_completion(result),

        "groundedness":
            evaluate_groundedness(result),

        "uncertainty_detection":
            evaluate_uncertainty(result),

        "failure_recovery":
            evaluate_failure_recovery(result),

        "evidence_quality":
            evaluate_evidence_quality(result),

        "hallucination_risk":
            evaluate_hallucination_risk(result),

        "robustness":
            evaluate_robustness(
                result,
                scenario_name
            )
    }

    print(
        f"⏱️ Latency: {latency:.2f} seconds"
    )

    print(
        f"📊 Completion: "
        f"{metrics['task_completion']}"
    )

    return {

        "scenario": scenario_name,

        "success": success,

        "error": error,

        "latency": latency,

        "metrics": metrics,

        "result": result
    }


# ============================================================
# REPEATED RUNS / CONSISTENCY
# ============================================================

def run_repeated_test(
    task,
    runs=3
):

    print("\n🔁 Running consistency test...")

    outputs = []

    latencies = []

    for run_number in range(1, runs + 1):

        print(
            f"\nRun {run_number}/{runs}"
        )

        start_time = time.time()

        result = run_react_agent(task)

        latency = (
            time.time() - start_time
        )

        outputs.append(
            str(result).lower()
        )

        latencies.append(
            latency
        )

    successful_runs = sum(

        1 for output in outputs

        if len(output) > 300
    )

    consistency = (
        successful_runs / runs
    )

    return {

        "runs": runs,

        "successful_runs":
            successful_runs,

        "consistency":
            consistency,

        "average_latency":
            statistics.mean(latencies),

        "latencies":
            latencies
    }


# ============================================================
# BASELINE AGENT
# ============================================================

def baseline_agent(task):

    """
    Simple baseline for comparison.

    No planning.
    No multi-agent orchestration.
    No replanning.
    """

    return (
        "Baseline analysis for: "
        f"{task}\n\n"
        "This is a simple direct response without "
        "dynamic planning, tool orchestration or "
        "failure recovery."
    )


def compare_with_baseline(task):

    print("\n📏 Comparing AgentX with baseline...")

    # AgentX
    start_time = time.time()

    agentx_result = run_react_agent(task)

    agentx_latency = (
        time.time() - start_time
    )

    # Baseline
    start_time = time.time()

    baseline_result = baseline_agent(task)

    baseline_latency = (
        time.time() - start_time
    )

    return {

        "agentx": {

            "completion":
                evaluate_task_completion(
                    agentx_result
                ),

            "groundedness":
                evaluate_groundedness(
                    agentx_result
                ),

            "uncertainty":
                evaluate_uncertainty(
                    agentx_result
                ),

            "latency":
                agentx_latency
        },

        "baseline": {

            "completion":
                evaluate_task_completion(
                    baseline_result
                ),

            "groundedness":
                evaluate_groundedness(
                    baseline_result
                ),

            "uncertainty":
                evaluate_uncertainty(
                    baseline_result
                ),

            "latency":
                baseline_latency
        }
    }


# ============================================================
# FULL EVALUATION
# ============================================================

def run_full_evaluation():

    print("\n")
    print("🤖 AGENTX TASK 6 - EVALUATION")
    print("=" * 60)

    results = []

    for test_case in TEST_SCENARIOS:

        evaluation_result = run_single_test(
            test_case
        )

        results.append(
            evaluation_result
        )

    # --------------------------------------------------------
    # Calculate aggregate metrics
    # --------------------------------------------------------

    total = len(results)

    successful = sum(

        1 for item in results

        if item["success"]
    )

    average_accuracy = statistics.mean(

        item["metrics"]["accuracy"]

        for item in results
    )

    average_completion = statistics.mean(

        item["metrics"]["task_completion"]

        for item in results
    )

    average_groundedness = statistics.mean(

        item["metrics"]["groundedness"]

        for item in results
    )

    average_robustness = statistics.mean(

        item["metrics"]["robustness"]

        for item in results
    )

    average_evidence_quality = statistics.mean(

        item["metrics"]["evidence_quality"]

        for item in results
    )

    average_hallucination_risk = statistics.mean(

        item["metrics"]["hallucination_risk"]

        for item in results
    )

    average_latency = statistics.mean(

        item["latency"]

        for item in results
    )

    reliability = successful / total

    # --------------------------------------------------------
    # Repeated run test
    # --------------------------------------------------------

    consistency = run_repeated_test(

        task=(
            "Analyze recent AI industry trends "
            "and provide evidence-based recommendations."
        ),

        runs=3
    )

    # --------------------------------------------------------
    # Baseline comparison
    # --------------------------------------------------------

    baseline_comparison = compare_with_baseline(

        "Analyze recent AI developments and "
        "provide recommendations."
    )

    # --------------------------------------------------------
    # Final report
    # --------------------------------------------------------

    report = {

        "accuracy":
            round(
                average_accuracy * 100,
                2
            ),

        "task_completion":
            round(
                average_completion * 100,
                2
            ),

        "reliability":
            round(
                reliability * 100,
                2
            ),

        "robustness":
            round(
                average_robustness * 100,
                2
            ),

        "groundedness":
            round(
                average_groundedness * 100,
                2
            ),

        "evidence_quality":
            round(
                average_evidence_quality * 100,
                2
            ),

        "hallucination_risk":
            round(
                average_hallucination_risk * 100,
                2
            ),

        "consistency":
            round(
                consistency["consistency"] * 100,
                2
            ),

        "average_latency_seconds":
            round(
                average_latency,
                2
            ),

        "average_repeated_latency":
            round(
                consistency[
                    "average_latency"
                ],
                2
            ),

        "baseline_comparison":
            baseline_comparison,

        "scenario_results":
            results
    }

    return report


# ============================================================
# DISPLAY REPORT
# ============================================================

def print_evaluation_report(report):

    print("\n")
    print("=" * 60)

    print("📊 AGENTX EVALUATION RESULTS")

    print("=" * 60)

    print(
        f"Accuracy: "
        f"{report['accuracy']}%"
    )

    print(
        f"Task Completion: "
        f"{report['task_completion']}%"
    )

    print(
        f"Reliability: "
        f"{report['reliability']}%"
    )

    print(
        f"Robustness: "
        f"{report['robustness']}%"
    )

    print(
        f"Groundedness: "
        f"{report['groundedness']}%"
    )

    print(
        f"Evidence Quality: "
        f"{report['evidence_quality']}%"
    )

    print(
        f"Hallucination Risk: "
        f"{report['hallucination_risk']}%"
    )

    print(
        f"Consistency: "
        f"{report['consistency']}%"
    )

    print(
        f"Average Latency: "
        f"{report['average_latency_seconds']} seconds"
    )

    print("\n📏 Baseline Comparison")

    print(
        report["baseline_comparison"]
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    final_report = run_full_evaluation()

    print_evaluation_report(
        final_report
    )