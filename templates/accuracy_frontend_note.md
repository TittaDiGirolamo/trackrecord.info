# Accuracy is a frontend-only presentation

The backend scoring pipeline **never** computes, stores, or ranks by any “accuracy” number.

All numbers that leave the canonical function are pure Brier scores (mean of (p − o)²).

If the UI wants a higher-is-better or percentage-style number, derive it **client-side** (or in the template) from the Brier value that was already emitted. Example:

```js
function accuracyFromBrier(brier) {
  if (brier == null) return null;
  // Example map: Brier 0 → 100 %, Brier 0.25 → 0 %
  return Math.max(0, Math.min(100, (1 - brier / 0.25) * 100));
}
