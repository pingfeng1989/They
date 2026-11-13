---
name: expense-tracking
description: "Record and summarize personal expenses over time."
version: 0.1.0
author: They, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Expenses, Spending, Money, Personal-Finance]
    category: productivity
    related_skills: [budget-tracking, shopping-comparison, lifestyle-reminder]
    config:
      - key: expense_tracking.enabled
        description: "Enable expense tracking (default: true)"
        type: bool
        default: true
---

# Expense Tracking

Record, categorize, and summarize personal expenses. Captures every purchase in one place,
groups it by category, and produces summaries you can act on — daily, weekly, or monthly.

## When to Use

- "I spent $45 on lunch today."
- "Record a $120 Amazon purchase under electronics."
- "What did I spend last week?"
- "Show me my spending by category this month."
- "How much have I spent on coffee this month?"

Don't use for: budget limits (`budget-tracking` owns that), or purchase price comparisons
(`shopping-comparison` owns that).

## Prerequisites

- `expense_tracking.enabled` config set to `true` (default).
- No external API keys required — expenses are stored locally under `~/.hermes/expenses/`.

## How to Run

1. **Record an expense** — amount, category, optional note, optional store.
2. **Summarize** — totals by category, by day, by period.
3. **Export** — produce a CSV or text report for a given period.

## Quick Reference

```
record expense: amount=float, category=string, note=string?, store=string?
summarize:       period=daily|weekly|monthly -> {by_category, total, count}
export:          period=string, format=csv|text -> file path
```

## Procedure

### 1. Record an expense

Capture amount, category, note, and store. Default category is `general`. Store the record in
`~/.hermes/expenses/<timestamp>.json`:

```json
{
  "id": "exp_20261113_080000_abc123",
  "amount": 45.0,
  "category": "food",
  "note": "lunch",
  "store": "local cafe",
  "timestamp": "2026-11-13T08:00:00Z"
}
```

If the category is unknown, ask the user rather than guessing. Done when the file exists and the
agent confirms the amount and category.

### 2. Summarize by period

Read all expense files in the requested period and aggregate:

- `total` — sum of all amounts
- `count` — number of expenses
- `by_category` — `{category: {total, count}}`
- `by_day` — `{day: {total, count}}`
- `largest` — the single largest expense

Done when every expense in the period is accounted for exactly once.

### 3. Export

Produce a report in the requested format:

- `csv` — one row per expense: `id,amount,category,note,store,timestamp`
- `text` — human-readable summary with category breakdown

Write to `~/.hermes/expenses/reports/<period>-<format>.<ext>`. Done when the file exists and
matches the requested format.

## Pitfalls

- **Currency.** Assume the user's local currency. Never convert unless explicitly asked.
- **Duplicates.** If the same expense is recorded twice, ask before deleting — the user may have
  a reason to keep both.
- **Missing category.** Prefer a small set of stable categories (`food`, `transport`,
  `entertainment`, `bills`, `health`, `shopping`, `general`) over freeform strings.
- **Timestamps.** Use the system clock in the user's timezone. Never fabricate a time.

## Verification

Run the test suite:

```bash
scripts/run_tests.sh tests/skills/test_expense_tracking_skill.py -q
```

Test cases:
- Record an expense → file exists with correct fields.
- Summarize → totals reconcile against the recorded expenses.
- Export → file exists and matches the requested format.
- Missing category → agent asks rather than guessing.