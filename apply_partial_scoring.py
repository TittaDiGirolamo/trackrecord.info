#!/usr/bin/env python3
"""
Trackrecord Scoring Application Script v2.0
Applies the tiered partial_accuracy scoring to resolved match predictions.

Usage:
    python apply_partial_scoring.py predictions.jsonl predictions_v2.jsonl

Requirements: Python 3.6+
"""

import json
import sys
import re
from typing import Dict, Any, Tuple


def parse_score(score_str: str) -> Tuple[int, int]:
    """Parse a score string like '2-1' or '1-1' into (home, away) tuple."""
    if not score_str:
        return (None, None)
    match = re.match(r'(\d+)-(\d+)', score_str.strip())
    if match:
        return (int(match.group(1)), int(match.group(2)))
    return (None, None)


def calculate_partial_accuracy(predicted_score: str, actual_score: str) -> Dict[str, Any]:
    """
    Calculate partial_accuracy dict based on tiered rules (v2.0).
    Returns dict with winner_correct, goal_difference_correct, exact_score_correct,
    weighted_score, tier, notes.
    """
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

    # Determine winner (or draw)
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

    # Apply tiered scoring
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
    """Process the JSONL file and add partial_accuracy where applicable."""
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
                print(f"Warning: Skipping invalid JSON line")
                updated_lines.append(line)
                continue

            # BROAD FILTER: Any resolved entry with outcome_proof
            if data.get("outcome") is not None and "outcome_proof" in data and data["outcome_proof"]:
                if "Sutton" in str(data.get("author", "")):
                    print(f"DEBUG: Processing Sutton resolved entry: {data.get('statement_id')} topic={data.get('statement_topic')}")

                proof = data["outcome_proof"]
                print(f"DEBUG: Proof for {data.get('statement_id')}: {proof[:150]}...")

                # Broader regex to extract actual score
                actual_match = re.search(r'Actual:?\s*.*?(\d+-\d+)', proof, re.IGNORECASE) or \
                               re.search(r'(\d+-\d+)', proof)
                if actual_match:
                    actual_score = actual_match.group(1)
                    print(f"DEBUG: Extracted actual_score: {actual_score}")

                    stmt = data.get("original_statement", "")
                    pred_match = re.search(r'(\d+-\d+)', stmt)
                    if pred_match:
                        predicted_score = pred_match.group(1)
                        partial = calculate_partial_accuracy(predicted_score, actual_score)
                        data["partial_accuracy"] = partial
                        data["scoring_version"] = "2.0"
                        match_count += 1
                        print(f"Applied scoring to {data.get('statement_id')} -> tier={partial.get('tier')}, weighted_score={partial.get('weighted_score')}")
                    else:
                        print("No predicted score found in statement")
                else:
                    print("No actual score parsed from proof")

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
        print("Usage: python apply_partial_scoring.py <input.jsonl> <output.jsonl>")
        sys.exit(1)
    process_predictions(sys.argv[1], sys.argv[2])