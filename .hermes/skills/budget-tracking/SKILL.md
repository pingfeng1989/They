---
name: budget-tracking
description: "Create and track budgets by category and period."
version: 0.1.0
author: They, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Budget, Money, Spending, Personal-Finance]
    category: productivity
    related_skills: [expense-tracking, shopping-comparison, lifestyle-reminder]
    config:
      - key: budgeting.enabled
        description: "Enable budget tracking (default: true)"
        type: bool
        default: true
---

# Budget Tracking

Create and track spending budgets by category and period (weekly/monthly/yearly). Helps you
understand where your money goes and stay within the limits you set. Designed for personal use,
not accounting-grade precision.

## When to Use

- "Set a $500 monthly budget for groceries."
- "How much do I have left in my dining budget?"
- "Am I over budget this month?"
- "Show me my budget status."
- "Create a weekly budget for transportation."

Don't use for: expense categorization (`expense-tracking` owns that), or one-off purchase
lookups (`shopping-comparison` owns that).

## Prerequisites

- `budgeting.enabled` config set to `true` (default).
- No external API keys required — budgets are stored locally under `~/.hermes/budgets/`.

## How to Run

1. **Create a budget** — say the category, amount, and period.
2. **Check status** — ask how much is left or whether you are over budget.
3. **Track spending** — every recorded expense reduces the matching budget's remaining balance.
4. **Review** — get a summary of all budgets and their status.

## Quick Reference

```
create budget:   category=string, amount=float, period=weekly|monthly|yearly
check budget:    category=string -> {remaining, status, percent_used}
list budgets:    -> [{category, amount, remaining, period, status}]
```

## Procedure

### 1. Create a budget

Record the category, amount, and period. Default period is `monthly`. Store the contract in
`~/.hermes/budgets/<category>.json`:

```json
{
  "category": "groceries",
  "amount": 500.0,
  "period": "monthly",
  "remaining": 500.0,
  "created_at": "2026-11-13T08:00:00Z",
  "spent_this_period": 0.0
}
```

Done when the file exists and the agent confirms creation.

### 2. Check budget status

Read the budget file, compute `remaining = amount - spent_this_period`, and classify:

- `ok` — remaining > 20% of amount
- `low` — remaining ≤ 20% of amount
- `exceeded` — remaining ≤ 0

Report the status, remaining amount, and percent used. Done when the status is deterministic
against the stored values.

### 3. Track spending

When `expense-tracking` records an expense, subtract it from the matching category's
`spent_this_period` and recompute `remaining`. Reset `spent_this_period` to 0 at the start of
each period. Done when the budget file reflects the latest expense.

### 4. Review

Summarize all budgets: total budgeted, total remaining, categories over budget, categories under
budget. Done when every budget has a status and the totals reconcile.

## Pitfalls

- **Budgets are advisory, not enforced.** The agent never blocks a purchase — it only reports.
- **Period boundaries.** Monthly budgets reset on the 1st; weekly on Monday; yearly on Jan 1.
  Use the system clock, not the budget file, to decide when to reset.
- **Missing category.** If an expense has no matching budget, record it but flag it as
  "no budget set" rather than silently ignoring.
- **Overlapping categories.** "Groceries" and "Food" are different budgets. Ask the user to
  disambiguate rather than guessing.

## Verification

Run the test suite:

```bash
scripts/run_tests.sh tests/skills/test_budget_tracking_skill.py -q
```

Test cases:
- Create a budget → file exists with correct values.
- Record an expense → remaining decreases by the expense amount.
- Check status → returns `ok` / `low` / `exceeded` correctly.
- Period reset → spent_this_period resets to 0 at period boundary.