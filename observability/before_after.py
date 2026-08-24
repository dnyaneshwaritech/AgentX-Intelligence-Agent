# ============================================================
# AgentX - Before vs After Observability Metrics
# Task 7
# File: observability/before_after.py
# ============================================================

import json
from pathlib import Path


# ============================================================
# TRACE DIRECTORY
# ============================================================

TRACE_DIR = Path("observability/traces")


# ============================================================
# LOAD TRACE
# ============================================================

def load_trace(trace_path):

    with open(
        trace_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# EXTRACT METRICS
# ============================================================

def extract_metrics(trace):

    summary = trace.get(
        "summary",
        {}
    )

    status = trace.get(
        "status",
        "unknown"
    )

    return {

        "trace_id":
            trace.get(
                "trace_id",
                "unknown"
            ),

        "status":
            status,

        "latency":
            float(
                summary.get(
                    "total_latency_seconds",
                    0
                )
            ),

        "tool_calls":
            int(
                summary.get(
                    "tool_calls",
                    0
                )
            ),

        "errors":
            int(
                summary.get(
                    "error_count",
                    0
                )
            ),

        "estimated_tokens":
            int(
                summary.get(
                    "estimated_tokens",
                    0
                )
            ),

        "success":
            1 if status == "success" else 0
    }


# ============================================================
# CALCULATE PERCENTAGE CHANGE
# ============================================================

def percentage_improvement(
    before,
    after,
    lower_is_better=True
):

    if before == 0:

        return 0.0

    if lower_is_better:

        change = (
            (before - after)
            / before
        ) * 100

    else:

        change = (
            (after - before)
            / before
        ) * 100

    return round(
        change,
        2
    )


# ============================================================
# COMPARE TWO TRACES
# ============================================================

def compare_traces(
    before_trace,
    after_trace
):

    before = extract_metrics(
        before_trace
    )

    after = extract_metrics(
        after_trace
    )

    comparison = {

        "before": before,

        "after": after,

        "improvements": {

            "latency_percent":
                percentage_improvement(
                    before["latency"],
                    after["latency"],
                    lower_is_better=True
                ),

            "tool_calls_percent":
                percentage_improvement(
                    before["tool_calls"],
                    after["tool_calls"],
                    lower_is_better=True
                ),

            "errors_percent":
                percentage_improvement(
                    before["errors"],
                    after["errors"],
                    lower_is_better=True
                ),

            "token_efficiency_percent":
                percentage_improvement(
                    before["estimated_tokens"],
                    after["estimated_tokens"],
                    lower_is_better=True
                )
        }
    }

    return comparison


# ============================================================
# PRINT COMPARISON
# ============================================================

def print_comparison(comparison):

    before = comparison["before"]
    after = comparison["after"]
    improvements = comparison["improvements"]

    print("\n")
    print("=" * 70)

    print(
        "📊 AGENTX BEFORE vs AFTER COMPARISON"
    )

    print("=" * 70)

    print("\nBEFORE:")

    print(
        f"Trace ID: {before['trace_id']}"
    )

    print(
        f"Status: {before['status']}"
    )

    print(
        f"Latency: "
        f"{before['latency']:.2f} seconds"
    )

    print(
        f"Tool Calls: "
        f"{before['tool_calls']}"
    )

    print(
        f"Errors: "
        f"{before['errors']}"
    )

    print(
        f"Estimated Tokens: "
        f"{before['estimated_tokens']}"
    )

    print("\nAFTER:")

    print(
        f"Trace ID: {after['trace_id']}"
    )

    print(
        f"Status: {after['status']}"
    )

    print(
        f"Latency: "
        f"{after['latency']:.2f} seconds"
    )

    print(
        f"Tool Calls: "
        f"{after['tool_calls']}"
    )

    print(
        f"Errors: "
        f"{after['errors']}"
    )

    print(
        f"Estimated Tokens: "
        f"{after['estimated_tokens']}"
    )

    print("\n📈 MEASURABLE CHANGE:")

    print(
        f"Latency Improvement: "
        f"{improvements['latency_percent']}%"
    )

    print(
        f"Tool Call Reduction: "
        f"{improvements['tool_calls_percent']}%"
    )

    print(
        f"Error Reduction: "
        f"{improvements['errors_percent']}%"
    )

    print(
        f"Token Efficiency Improvement: "
        f"{improvements['token_efficiency_percent']}%"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    trace_files = list(
        TRACE_DIR.glob(
            "trace_*.json"
        )
    )

    if len(trace_files) < 2:

        print(
            "❌ At least two trace files are required."
        )

        print(
            "Run AgentX once before optimization "
            "and once after optimization."
        )

    else:

        # Sort traces by creation time
        trace_files.sort(
            key=lambda path:
                path.stat().st_mtime
        )

        # First trace = BEFORE
        before_path = trace_files[-2]

        # Latest trace = AFTER
        after_path = trace_files[-1]

        print(
            f"\n📡 BEFORE TRACE:\n"
            f"{before_path}"
        )

        print(
            f"\n📡 AFTER TRACE:\n"
            f"{after_path}"
        )

        before_trace = load_trace(
            before_path
        )

        after_trace = load_trace(
            after_path
        )

        comparison = compare_traces(
            before_trace,
            after_trace
        )

        print_comparison(
            comparison
        )