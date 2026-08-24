import json
from pathlib import Path


def load_trace(trace_path):

    with open(
        trace_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def detect_root_causes(trace):

    root_causes = []

    errors = trace.get(
        "errors",
        []
    )

    events = trace.get(
        "events",
        []
    )

    summary = trace.get(
        "summary",
        {}
    )

    metrics = {}

    for event in events:

        if event.get("event_type") == "metric":

            name = event.get(
                "name",
                ""
            )

            value = event.get(
                "data",
                {}
            ).get(
                "value",
                0
            )

            metrics[name] = value

    # Explicit errors
    for error in errors:

        root_causes.append({

            "cause": "Execution Error",

            "component": error.get(
                "component",
                "Unknown"
            ),

            "details": error.get(
                "message",
                str(error)
            ),

            "severity": "high"
        })

    # Tool failures
    failure_count = metrics.get(
        "failure_count",
        0
    )

    if failure_count > 0:

        root_causes.append({

            "cause": "Tool Failure Detected",

            "component": "Agent Tool Layer",

            "details":
                f"{failure_count} tool failure(s) "
                "detected during execution.",

            "severity": "high"
        })

    # Evidence conflicts
    conflict_count = metrics.get(
        "conflict_count",
        0
    )

    if conflict_count > 0:

        root_causes.append({

            "cause":
                "Conflicting Evidence Detected",

            "component":
                "Evidence Resolution",

            "details":
                f"{conflict_count} evidence conflict(s) "
                "detected.",

            "severity": "medium"
        })

    # Low confidence
    confidence = metrics.get(
        "final_confidence",
        1.0
    )

    if confidence < 0.5:

        root_causes.append({

            "cause":
                "High Uncertainty / Low Confidence",

            "component":
                "Reasoning Layer",

            "details":
                f"Final confidence was {confidence}.",

            "severity": "medium"
        })

    # High latency
    latency = summary.get(
        "total_latency_seconds",
        0
    )

    if latency > 30:

        root_causes.append({

            "cause":
                "High Execution Latency",

            "component":
                "AgentX",

            "details":
                f"Execution took {latency:.2f} seconds.",

            "severity": "medium"
        })

    # LLM fallback detection
    for event in events:

        data = event.get(
            "data",
            {}
        )

        output_preview = str(
            data.get(
                "output_preview",
                ""
            )
        ).lower()

        if (
            "llm analysis is temporarily unavailable"
            in output_preview
        ):

            root_causes.append({

                "cause":
                    "LLM/API Failure",

                "component":
                    "LLM / OpenRouter",

                "details":
                    "Primary LLM failed and "
                    "fallback was activated.",

                "severity":
                    "high"
            })

            break

    # Failed status
    status = trace.get(
        "status",
        "unknown"
    )

    if status != "success":

        root_causes.append({

            "cause":
                "Task Execution Failed",

            "component":
                "AgentX",

            "details":
                f"Trace status: {status}",

            "severity":
                "high"
        })

    return root_causes


def recommend_improvements(root_causes):

    recommendations = []

    for cause in root_causes:

        cause_name = cause["cause"]

        if cause_name == "Tool Failure Detected":

            recommendations.append(
                "Use fallback tools or alternate data sources."
            )

            recommendations.append(
                "Avoid repeatedly calling a failed tool."
            )

        elif cause_name == "LLM/API Failure":

            recommendations.append(
                "Reduce max_tokens or prompt size."
            )

            recommendations.append(
                "Use a fallback response or alternate model."
            )

        elif cause_name == "Conflicting Evidence Detected":

            recommendations.append(
                "Verify conflicting claims using independent evidence."
            )

        elif cause_name == "High Uncertainty / Low Confidence":

            recommendations.append(
                "Report uncertainty and avoid unsupported conclusions."
            )

        elif cause_name == "High Execution Latency":

            recommendations.append(
                "Run independent tools in parallel."
            )

    return list(dict.fromkeys(recommendations))


def diagnose_trace(trace_path):

    trace = load_trace(trace_path)

    root_causes = detect_root_causes(trace)

    recommendations = recommend_improvements(
        root_causes
    )

    return {

        "trace_id": trace.get(
            "trace_id",
            "unknown"
        ),

        "status": trace.get(
            "status",
            "unknown"
        ),

        "root_causes": root_causes,

        "recommendations": recommendations
    }


def print_diagnosis(diagnosis):

    print("\n")
    print("=" * 70)
    print("🔍 AGENTX AUTOMATIC TRACE DIAGNOSIS")
    print("=" * 70)

    print(
        "\nTrace ID:",
        diagnosis["trace_id"]
    )

    print(
        "Status:",
        diagnosis["status"]
    )

    print("\n🔎 ROOT CAUSES:")

    if diagnosis["root_causes"]:

        for index, cause in enumerate(
            diagnosis["root_causes"],
            start=1
        ):

            print(
                f"\n{index}. {cause['cause']}"
            )

            print(
                "   Component:",
                cause["component"]
            )

            print(
                "   Details:",
                cause["details"]
            )

            print(
                "   Severity:",
                cause["severity"]
            )

    else:

        print(
            "No major root cause detected."
        )

    print("\n🔧 RECOMMENDED IMPROVEMENTS:")

    if diagnosis["recommendations"]:

        for index, recommendation in enumerate(
            diagnosis["recommendations"],
            start=1
        ):

            print(
                f"{index}. {recommendation}"
            )

    else:

        print(
            "No immediate improvement required."
        )


if __name__ == "__main__":

    trace_dir = Path(
        "observability/traces"
    )

    trace_files = list(
        trace_dir.glob(
            "trace_*.json"
        )
    )

    if not trace_files:

        print(
            "❌ No trace files found."
        )

    else:

        latest_trace = max(
            trace_files,
            key=lambda path: path.stat().st_mtime
        )

        print(
            f"📡 Analyzing trace: {latest_trace}"
        )

        diagnosis = diagnose_trace(
            latest_trace
        )

        print_diagnosis(
            diagnosis
        )