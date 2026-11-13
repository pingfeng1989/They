---
name: shopping-comparison
description: "Track product prices across stores and alert on drops or thresholds."
version: 0.1.0
author: They, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Shopping, Prices, Comparison, Alerts, Personal-Finance]
    category: productivity
    related_skills: [expense-tracking, budget-tracking]
    config:
      - key: shopping_comparison.enabled
        description: "Enable price tracking (default: true)"
        type: bool
        default: true
---

# Shopping Comparison

Track product prices across stores and alert on price drops, availability changes, or custom
thresholds. Records a price, compares it against history, and triggers a notification when the
condition you set is met.

## When to Use

- "Alert me when this laptop drops below $1,000."
- "Track the price of this item across stores."
- "Did this price change since last week?"
- "Compare prices for the same product."
- "Notify me if this item comes back in stock."

Don't use for: general expense logging (`expense-tracking` owns that), or budget limits
(`budget-tracking` owns that).

## Prerequisites

- `shopping_comparison.enabled` config set to `true` (default).
- Optional: `web_extract` for live price checks.
- No external API keys required for basic tracking.

## How to Run

1. **Add a product to watch** — product name, store, current price, optional URL.
2. **Record a price check** — update the price, record the observation.
3. **Set an alert** — threshold, cooldown, notification destination.
4. **List watches** — show all tracked products and their current state.
5. **Run a check** — fetch the latest price, compare, decide whether to alert.

## Quick Reference

```
watch product:   product=string, store=string, price=float, url=string?
set alert:       product=string, condition=below|above|available, threshold=float, cooldown=hours
list watches:    -> [{product, store, current_price, last_checked, condition}]
check now:       product=string -> {price, changed, alerted}
```

## Procedure

### 1. Add a product to watch

Record the product name, store, current price, and optional URL. Store the watch contract in
`~/.hermes/price-watches/<watch-slug>.json`:

```json
{
  "id": "watch_20261113_abc123",
  "product": "laptop x",
  "store": "amazon",
  "url": "https://example.com",
  "current_price": 999.0,
  "baseline_price": 999.0,
  "condition": "below",
  "threshold": 900.0,
  "cooldown_hours": 24,
  "last_checked": "2026-11-13T08:00:00Z",
  "last_alert": null,
  "observation_history": []
}
```

Done when the file exists and the agent confirms the watch is active.

### 2. Record a price check

Fetch the current price (via `web_extract` if URL is provided, or ask the user). Record the
observation: timestamp, price, availability. Append to `observation_history`. Update
`current_price` and `last_checked`. Done when the observation is comparable to the baseline.

### 3. Set an alert

Define the alert condition:

- `below` — price drops below `threshold`
- `above` — price rises above `threshold`
- `available` — item is in stock / available

Store the condition, threshold, cooldown, and notification destination. Done when the condition
is deterministic against stored state.

### 4. Run a check

Compare the current price against the baseline and condition:

- If condition met and no alert sent in `cooldown_hours` → trigger notification, update
  `last_alert`.
- If condition not met → record observation, no alert.
- If price unavailable → report unknown state, do not overwrite the last good observation.

Done when the alert decision is deterministic and the observation is recorded.

### 5. List watches

Summarize all active watches: product, store, current price, last checked, condition, whether
an alert is due. Done when every watch has a status.

## Pitfalls

- **Stale prices.** Never overwrite a good observation with an error page. Report unknown state
  instead.
- **Duplicate alerts.** Replaying the same price must not send a second alert. Respect the
  cooldown.
- **Currency.** Assume the user's local currency. Convert only when explicitly asked.
- **Availability.** "In stock" and "out of stock" are distinct from price — record them separately.

## Verification

Run the test suite:

```bash
scripts/run_tests.sh tests/skills/test_shopping_comparison_skill.py -q
```

Test cases:
- Add a watch → file exists with correct fields.
- Record a price → observation appended, current_price updated.
- Set an alert → condition stored, deterministic against state.
- Check → alert fires only when condition met and cooldown respected.
- Stale price → reported as unknown, not overwritten.