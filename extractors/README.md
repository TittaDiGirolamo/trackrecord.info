# Probability Extraction (Upstream of Scoring)

Rule-based is the primary / default method for Phase 1.
LLM-style is an optional secondary method with its own method ID.

Never mix the two under the same method ID.
When you change a rule table or a prompt, bump the version in the method ID.
