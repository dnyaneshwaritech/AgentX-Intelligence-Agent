# ============================================================
# AgentX - Human Evaluation Rubric
# Task 6: Human Evaluation
# File: evaluation/human_evaluation.py
# ============================================================

EVALUATION_CRITERIA = {

    "accuracy": {
        "name": "Accuracy",
        "question": (
            "Are the conclusions factually reasonable "
            "and relevant to the task?"
        )
    },

    "task_completion": {
        "name": "Task Completion",
        "question": (
            "Did the agent successfully complete the "
            "requested objective?"
        )
    },

    "groundedness": {
        "name": "Groundedness",
        "question": (
            "Are conclusions supported by the available "
            "research, news, or evidence?"
        )
    },

    "evidence_quality": {
        "name": "Evidence Quality",
        "question": (
            "Is the evidence relevant, useful, and "
            "appropriately considered?"
        )
    },

    "uncertainty_awareness": {
        "name": "Uncertainty Awareness",
        "question": (
            "Does the agent clearly communicate uncertainty "
            "when evidence is incomplete or conflicting?"
        )
    },

    "unsupported_claim_refusal": {
        "name": "Unsupported Conclusion Refusal",
        "question": (
            "Does the agent avoid making strong conclusions "
            "that are not supported by evidence?"
        )
    },

    "failure_recovery": {
        "name": "Failure Recovery",
        "question": (
            "When a tool fails, does the agent recover using "
            "fallback tools or available evidence?"
        )
    },

    "robustness": {
        "name": "Robustness",
        "question": (
            "Does the agent handle ambiguous, adversarial, "
            "contradictory, and incomplete inputs safely?"
        )
    },

    "overall_quality": {
        "name": "Overall Quality",
        "question": (
            "How useful and trustworthy is the final result?"
        )
    }
}


# ============================================================
# SCORE GUIDE
# ============================================================

SCORE_GUIDE = {

    1: "Poor - Major failure or unreliable behavior",

    2: "Weak - Significant problems",

    3: "Acceptable - Partially successful",

    4: "Good - Strong performance",

    5: "Excellent - Reliable and high quality"
}


# ============================================================
# DISPLAY HUMAN EVALUATION FORM
# ============================================================

def print_human_evaluation_form():

    print("\n")
    print("=" * 70)

    print("🤖 AGENTX HUMAN EVALUATION RUBRIC")

    print("=" * 70)

    print(
        "\nScore each criterion from 1 to 5.\n"
    )

    print("SCORE GUIDE:\n")

    for score, description in SCORE_GUIDE.items():

        print(
            f"{score} = {description}"
        )

    print("\n" + "-" * 70)

    for key, criterion in EVALUATION_CRITERIA.items():

        print(
            f"\n📊 {criterion['name']}"
        )

        print(
            f"Question: {criterion['question']}"
        )

        print(
            "Score (1-5): ______"
        )

        print(
            "Comments: ______________________________"
        )


# ============================================================
# CALCULATE HUMAN EVALUATION SCORE
# ============================================================

def calculate_human_score(scores):

    if not scores:

        return 0

    total = sum(
        scores.values()
    )

    maximum = len(scores) * 5

    percentage = (
        total / maximum
    ) * 100

    return round(
        percentage,
        2
    )


# ============================================================
# EXAMPLE HUMAN EVALUATION
# ============================================================

def example_evaluation():

    # Example scores entered by evaluator
    scores = {

        "accuracy": 4,

        "task_completion": 5,

        "groundedness": 4,

        "evidence_quality": 4,

        "uncertainty_awareness": 5,

        "unsupported_claim_refusal": 5,

        "failure_recovery": 4,

        "robustness": 4,

        "overall_quality": 4
    }

    final_score = calculate_human_score(
        scores
    )

    print("\n")
    print("=" * 70)

    print("📊 EXAMPLE HUMAN EVALUATION RESULT")

    print("=" * 70)

    for criterion, score in scores.items():

        name = EVALUATION_CRITERIA[
            criterion
        ]["name"]

        print(
            f"{name}: {score}/5"
        )

    print(
        f"\nFinal Human Evaluation Score: "
        f"{final_score}%"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print_human_evaluation_form()

    example_evaluation()