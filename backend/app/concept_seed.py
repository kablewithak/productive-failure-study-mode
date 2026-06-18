from __future__ import annotations

from app.models import ChallengeType, Concept


SEEDED_CONCEPTS: tuple[Concept, ...] = (
    Concept(
        concept_id="python_lists_sliding_window",
        title="Python lists: keeping the most recent readings",
        discipline="Computer Science",
        module_context="Introductory programming",
        learning_outcome=(
            "Use a Python list to store, append, and remove values so that only the most "
            "recent fixed number of readings is retained."
        ),
        prerequisite_knowledge=[
            "variables",
            "while loops",
            "if statements",
            "basic function calls",
        ],
        challenge_type=ChallengeType.DIAGNOSE_ERROR,
        challenge_prompt=(
            "A sensor produces one new heart-rate reading at a time. Without using a full "
            "explanation of lists yet, describe how you would keep only the 10 most recent "
            "readings and discard older readings as new readings arrive."
        ),
        expected_reasoning_steps=[
            "Represent multiple readings as one ordered collection.",
            "Add each new reading to the end of the collection.",
            "Check whether the collection contains more than 10 readings.",
            "Remove the oldest reading when the collection grows beyond 10.",
            "Use the updated collection as the current state.",
        ],
        common_misconceptions=[
            "Storing each reading in a separate variable instead of one collection.",
            "Replacing the whole collection with the newest reading.",
            "Removing the newest reading instead of the oldest reading.",
            "Checking the value of a reading instead of checking the number of readings.",
        ],
        canonical_explanation=(
            "A Python list is an ordered collection that can grow and shrink. For this task, "
            "the useful structure is a sliding window: append the newest reading, then if the "
            "list is longer than 10, remove the first item because it is the oldest reading."
        ),
        retrieval_question_seeds=[
            "Why is a list more suitable than ten separate variables for this task?",
            "What should happen immediately after the eleventh reading is added?",
            "How would the logic change if the system needed the most recent seven readings?",
        ],
    ),
    Concept(
        concept_id="law_offer_acceptance",
        title="Offer and acceptance",
        discipline="Law",
        module_context="Contract Law",
        learning_outcome=(
            "Identify whether a valid offer has been accepted and explain why the facts do "
            "or do not show agreement."
        ),
        prerequisite_knowledge=[
            "basic contract formation",
            "intention to create legal relations",
            "communication between parties",
        ],
        challenge_type=ChallengeType.CASE_APPLICATION,
        challenge_prompt=(
            "A seller emails: 'I can sell you my laptop for R5,000 if you confirm by Friday.' "
            "The buyer replies on Friday: 'Sounds good, but can you include the laptop bag?' "
            "Before receiving any explanation, decide whether the buyer accepted the offer and "
            "explain your reasoning."
        ),
        expected_reasoning_steps=[
            "Identify the seller's statement as a possible offer.",
            "Check whether the buyer's reply matches the terms of the offer.",
            "Distinguish acceptance from a counter-offer or request for changed terms.",
            "Explain whether consensus was reached on the same terms.",
        ],
        common_misconceptions=[
            "Treating any positive-sounding reply as acceptance.",
            "Ignoring changed or added terms.",
            "Confusing negotiation with final agreement.",
            "Assuming agreement exists because both parties are interested.",
        ],
        canonical_explanation=(
            "Acceptance must correspond to the offer's material terms. A response that changes "
            "the terms may be a counter-offer or further negotiation rather than acceptance. "
            "The key question is whether the buyer unequivocally agreed to the same offer."
        ),
        retrieval_question_seeds=[
            "What makes an acceptance different from a counter-offer?",
            "Why does changing a material term matter in contract formation?",
            "Apply the same rule to a rental agreement where the tenant changes the move-in date.",
        ],
    ),
    Concept(
        concept_id="commerce_break_even_analysis",
        title="Break-even analysis",
        discipline="Commerce",
        module_context="Business Accounting and Economics",
        learning_outcome=(
            "Calculate and interpret the break-even point using fixed costs, selling price, "
            "and variable cost per unit."
        ),
        prerequisite_knowledge=[
            "revenue",
            "fixed costs",
            "variable costs",
            "basic algebra",
        ],
        challenge_type=ChallengeType.CALCULATION_ATTEMPT,
        challenge_prompt=(
            "A student business sells study packs for R120 each. Each pack costs R45 to print, "
            "and the business pays R3,000 once-off for design and setup. Before receiving the "
            "formula, estimate how many packs must be sold before the business stops making a "
            "loss. Explain your reasoning."
        ),
        expected_reasoning_steps=[
            "Separate fixed costs from variable costs.",
            "Calculate contribution per unit as selling price minus variable cost.",
            "Divide fixed costs by contribution per unit.",
            "Interpret the result as the number of units needed to cover total fixed costs.",
        ],
        common_misconceptions=[
            "Dividing fixed cost by selling price instead of contribution per unit.",
            "Treating variable cost as if it happens only once.",
            "Calculating profit for one unit but not scaling to total fixed costs.",
            "Giving a number without explaining what it means.",
        ],
        canonical_explanation=(
            "Break-even happens when total revenue equals total cost. Each unit contributes "
            "selling price minus variable cost toward fixed costs. Once total contribution "
            "covers fixed costs, the business reaches break-even."
        ),
        retrieval_question_seeds=[
            "Why does break-even use contribution per unit rather than selling price?",
            "What happens to the break-even point if printing cost increases?",
            "Calculate the break-even point for a product selling at R80 with R30 variable cost and R2,500 fixed cost.",
        ],
    ),
    Concept(
        concept_id="engineering_moments",
        title="Moments: turning effect of a force",
        discipline="Engineering and Physical Sciences",
        module_context="Mechanics",
        learning_outcome=(
            "Explain and calculate the moment produced by a force acting at a distance from "
            "a pivot."
        ),
        prerequisite_knowledge=[
            "force",
            "distance",
            "multiplication",
            "clockwise and anticlockwise rotation",
        ],
        challenge_type=ChallengeType.SHORT_PROBLEM_SOLVING,
        challenge_prompt=(
            "A 20 N force is applied downward at the end of a 0.5 m spanner. Before receiving "
            "the full rule, explain what affects the turning effect around the bolt and estimate "
            "the size of that turning effect."
        ),
        expected_reasoning_steps=[
            "Recognize that a force can rotate an object around a pivot.",
            "Identify the force magnitude.",
            "Identify the perpendicular distance from the pivot.",
            "Multiply force by perpendicular distance.",
            "State the result with an appropriate unit and direction where relevant.",
        ],
        common_misconceptions=[
            "Considering only force and ignoring distance from the pivot.",
            "Considering only distance and ignoring force.",
            "Using mass instead of force.",
            "Forgetting that the perpendicular distance matters.",
        ],
        canonical_explanation=(
            "A moment is the turning effect of a force around a pivot. For a force applied "
            "perpendicular to the lever arm, the moment equals force multiplied by distance "
            "from the pivot. The larger the force or distance, the larger the turning effect."
        ),
        retrieval_question_seeds=[
            "Why does pushing farther from the pivot create a larger moment?",
            "What moment is produced by a 15 N force applied 0.4 m from a pivot?",
            "How would the moment change if the same force were applied closer to the bolt?",
        ],
    ),
)


CONCEPTS_BY_ID: dict[str, Concept] = {concept.concept_id: concept for concept in SEEDED_CONCEPTS}
