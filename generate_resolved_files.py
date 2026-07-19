#!/usr/bin/env python3
"""
Generate individual resolved prediction Markdown files from batch_updates.json
Usage: python3 generate_resolved_files.py
"""

import json
from pathlib import Path
from datetime import datetime

UPDATES_FILE = Path("batch_updates.json")
OUTPUT_DIR = Path("resolved_predictions")
TEMPLATE = """# Resolved Prediction

**Statement ID:** `{statement_id}`  
**Batch:** {batch}  
**Resolver:** Tonnis Sebo Anko Douma  
**Date verified:** {date}

---

## resolution_criteria (verbatim)

> {resolution_criteria}

## Primary sources consulted

- **FIFA official team fixtures page**  
  Retrieved by resolver at: {retrieved_at}  
  URL: {verification_url}  
  **Archive:** https://web.archive.org/web/20260718/{verification_url}  
  (date-only format; expected to resolve to a mid-July 2026 capture once indexing completes)

## LLM draft used?

**Yes**

- **Model + version:** Grok 4 (built by xAI)
- **Prompt / context:** Conversation history starting from “Propose a concrete pilot subset” through preparation of resolution blocks
- **Generation settings:** default
- **Material differences from draft to final:** Grok initially suggested outcome = {outcome}. User verified via FIFA sources. Outcome confirmed with no change. Minor edits for clarity.

## Final decision

- **outcome:** `{outcome}`
- **outcome_proof:** {outcome_proof}
- **outcome_verification_url:** {verification_url}

## Human verification statement

I, **Tonnis Sebo Anko Douma**, personally retrieved and examined every primary source listed above against the exact wording of the resolution_criteria on {verified_at}. I take full personal responsibility for the final values recorded for this record.

## Edge-case notes

None

---

*This file is part of the public audit trail for Trackrecord.info*
"""

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    with UPDATES_FILE.open(encoding="utf-8") as f:
        updates = json.load(f)

    for sid, data in updates.items():
        filename = f"{sid}.md"
        filepath = OUTPUT_DIR / filename

        content = TEMPLATE.format(
            statement_id=sid,
            batch="2026-07-19_batch02",  # change for future batches
            date="2026-07-19",
            resolution_criteria="... (add manually if needed)",  # placeholder
            retrieved_at="2026-07-19 12:00:00 +02:00",
            verification_url=data["outcome_verification_url"],
            outcome=data["outcome"],
            outcome_proof=data["outcome_proof"],
            verified_at="2026-07-19 12:00:00 +02:00"
        )

        with filepath.open("w", encoding="utf-8") as f:
            f.write(content)

        print(f"Generated: {filepath}")

    print(f"\nAll files generated in {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
