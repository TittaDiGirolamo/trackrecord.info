#!/usr/bin/env python3
<<<<<<< HEAD
"""
Trackrecord Scoring Application Script v2.0
Applies the tiered partial_accuracy scoring to resolved match predictions.

Usage:
    python apply_partial_scoring.py predictions.jsonl output.jsonl

Requirements: Python 3.6+
"""

=======
>>>>>>> 3819b78 (Add apply_partial_scoring.py v2.0 script)
import json
import sys
import re
from typing import Dict, Any, Tuple

def parse_score(score_str: str) -> Tuple[int, int]:
<<<<<<< HEAD
    """Parse a score string like '2-1' or '1-1' into (home, away) tuple."""
=======
>>>>>>> 3819b78 (Add apply_partial_scoring.py v2.0 script)
    if not score_str:
        return (None, None)
    match = re.match(r'(\d+)-(\d+)', score_str.strip())
    if match:
        return (int(match.group(1)), int(match.group(2)))
    return (None, None)

def calculate_partial_accuracy(predicted_score: str, actual_score: str) -> Dict[str, Any]:
<<<<<<< HEAD
    """
    Calculate partial_accuracy dict based on tiered rules (v2.0).
    Returns dict with winner_correct, goal_difference_correct, exact_score_correct,
    weighted_score, tier, notes.
    """
=======
>>>>>>> 3819b78 (Add apply_partial_scoring.py v2.0 script)
    pred_home, pred_away = parse_score(predicted_score)
    act_home, act_away = parse_score(actual_score)

    if pred_home is None or act_home is None:
        return {
            "winner_correct": None,
            "goal_difference_correct": None,
            "exact_score_correct": None,
            "weighted_score": 0.0,
            "tier": "none",
            "notes": "Unable to parse scores"
        }

    pred_gd = pred_home - pred_away
    act_gd = act_home - act_away

<<<<<<< HEAD
    # Determine winner (or draw)
=======
>>>>>>> 3819b78 (Add apply_partial_scoring.py v2.0 script)
    if pred_home > pred_away:
        pred_winner = "home"
    elif pred_home < pred_away:
        pred_winner = "away"
    else:
        pred_winner = "draw"

    if act_home > act_away:
        act_winner = "home"
    elif act_home < act_away:
        act_winner = "away"
    else:
        act_winner = "draw"

    winner_correct = (pred_winner == act_winner)
    gd_correct = (pred_gd == act_gd)
    exact_correct = (pred_home == act_home and pred_away == act_away)

<<<<<<< HEAD
    # Apply tiered scoring
=======
>>>>>>> 3819b78 (Add apply_partial_scoring.py v2.0 script)
    if exact_correct:
        weighted = 1.0
        tier = "exact"
        notes = "Exact score match"
    elif winner_correct and gd_correct:
        weighted = 0.4
        tier = "winner_gd"
        notes = "Correct winner and goal difference"
    elif winner_correct:
        weighted = 0.2
        tier = "winner_only"
        notes = f"Correct winner only (GD off by {abs(pred_gd - act_gd)})"
    elif gd_correct:
        weighted = 0.1
        tier = "gd_only"
        notes = "Correct GD but wrong winner (rare)"
    else:
        weighted = 0.0
        tier = "none"
        notes = "Incorrect winner"

    return {
        "winner_correct": winner_correct,
        "goal_difference_correct": gd_correct,
        "exact_score_correct": exact_correct,
        "weighted_score": weighted,
        "tier": tier,
        "notes": notes
    }

def process_predictions(input_path: str, output_path: str):
<<<<<<< HEAD
    """Process the JSONL file and add partial_accuracy where applicable."""
=======
>>>>>>> 3819b78 (Add apply_partial_scoring.py v2.0 script)
    updated_lines = []
    count = 0
    match_count = 0

    with open(input_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
<<<<<<< HEAD
                print(f"Warning: Skipping invalid JSON line")
                updated_lines.append(line)
                continue

            # Only process resolved match predictions that have outcome_proof with actual score
            if (data.get("outcome") is not None and 
                "Group Stage - Match Result" in data.get("statement_topic", "") and
                "outcome_proof" in data and data["outcome_proof"]):

                # Extract actual score from proof if possible (simple heuristic)
                proof = data["outcome_proof"]
                actual_match = re.search(r'Actual:\s*([A-Za-z\s]+)?\s*(\d+-\d+)', proof)
                if actual_match:
                    actual_score = actual_match.group(2)
                    # Try to find predicted score from original_statement or context
                    # For simplicity, we assume the prediction is in the statement or we use a placeholder
                    # In real use, user should provide predicted_score explicitly or parse from context
                    predicted_score = None
                    # Heuristic: look for score in original_statement
=======
                updated_lines.append(line)
                continue

            if (data.get("outcome") is not None and 
                "Match Result" in data.get("statement_topic", "") and
                "outcome_proof" in data):

                proof = data["outcome_proof"]
                actual_match = re.search(r'Actual:.*?(\d+-\d+)', proof)
                if actual_match:
                    actual_score = actual_match.group(1)
>>>>>>> 3819b78 (Add apply_partial_scoring.py v2.0 script)
                    stmt = data.get("original_statement", "")
                    pred_match = re.search(r'(\d+-\d+)', stmt)
                    if pred_match:
                        predicted_score = pred_match.group(1)
<<<<<<< HEAD

                    if predicted_score and actual_score:
=======
>>>>>>> 3819b78 (Add apply_partial_scoring.py v2.0 script)
                        partial = calculate_partial_accuracy(predicted_score, actual_score)
                        data["partial_accuracy"] = partial
                        data["scoring_version"] = "2.0"
                        match_count += 1

                count += 1

            updated_lines.append(json.dumps(data, ensure_ascii=False))

    with open(output_path, 'w', encoding='utf-8') as outfile:
        for line in updated_lines:
            outfile.write(line + '\n')

    print(f"Processed {count} resolved entries.")
    print(f"Applied partial scoring to {match_count} match predictions.")
    print(f"Output written to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
<<<<<<< HEAD
        print("Usage: python apply_partial_scoring.py <input.jsonl> <output.jsonl>")
        sys.exit(1)
    process_predictions(sys.argv[1], sys.argv[2])
=======
        print("Usage: python3 apply_partial_scoring.py <input.jsonl> <output.jsonl>")
        sys.exit(1)
    process_predictions(sys.argv[1], sys.argv[2])
>>>>>>> 3819b78 (Add apply_partial_scoring.py v2.0 script)
