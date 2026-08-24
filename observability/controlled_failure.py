# ============================================================
# AgentX - Controlled Failure Test
# Task 7
# ============================================================

import os
from react_agent import run_react_agent


def run_controlled_failure_test():

    print("\n")
    print("=" * 70)
    print("🔥 AGENTX CONTROLLED FAILURE TEST")
    print("=" * 70)

    # Enable simulated failure
    os.environ["FORCE_TOOL_FAILURE"] = "1"

    task = (
        "Find recent AI industry developments and identify "
        "important opportunities and risks."
    )

    print("\n🔴 Controlled failure enabled")
    print("🎯 Task:", task)

    try:

        result = run_react_agent(
            task,
            adversarial=True
        )

        print("\n")
        print("=" * 70)
        print("📊 CONTROLLED FAILURE TEST RESULT")
        print("=" * 70)

        print(result)

    except Exception as e:

        print("\n❌ Test execution failed")
        print(
            type(e).__name__,
            ":",
            str(e)
        )

    finally:

        # Disable simulated failure
        os.environ.pop(
            "FORCE_TOOL_FAILURE",
            None
        )

        print("\n🟢 Controlled failure disabled")


if __name__ == "__main__":

    run_controlled_failure_test()