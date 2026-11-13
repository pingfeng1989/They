---
name: lifestyle-reminder
description: "Set reminders, digests, and anomaly alerts."
version: 0.1.0
author: They, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Reminders, Daily-Digest, Anomaly-Alerts, Personal-Management]
    category: productivity
    related_skills: [budget-tracking, expense-tracking, shopping-comparison]
    config:
      - key: lifestyle_reminder.enabled
        description: "Enable lifestyle reminders (default: true)"
        type: bool
        default: true
      - key: lifestyle_reminder.morning_time
        description: "Morning digest time (default: 08:00)"
        type: string
        default: "08:00"
      - key: lifestyle_reminder.evening_time
        description: "Evening digest time (default: 20:00)"
        type: string
        default: "20:00"
---

# Lifestyle Reminder

Schedule reminders, daily digests, and anomaly alerts for everyday life. Supports recurring
schedule triggers, proactive budget/spending anomaly detection, and scheduled digests — without
needing you to ask each time.

## When to Use

- "Remind me to take medication every day at 9am."
- "Give me a morning digest of my budget status."
- "Alert me if I exceed my budget this month."
- "Tell me when my subscriptions are due."
- "Set a one-time reminder to call the bank."

Don't use for: complex calendar management (`google-workspace` owns calendar sync), or
multi-agent task coordination (`delegate_task` owns sub-agents).

## Prerequisites

- `lifestyle_reminder.enabled` config set to `true` (default).
- Uses Hermes cron (`cronjob()`) for scheduled triggers.
- Notification destinations: terminal, gateway channels (Telegram/Slack/etc. if configured),
  or whichever platform the user is chatting on.

## How to Run

1. **Set a one-time reminder** — time, message, optional channel.
2. **Set a recurring reminder** — schedule, message, channel.
3. **Get a daily digest** — morning/evening summary of budget, spending, and reminders.
4. **Run anomaly checks** — budget exceeded, spending spike, upcoming bills.
5. **List active reminders** — show all scheduled reminders with next fire time.

## Quick Reference

```
remind once:     message=string, time=string, channel=string?
remind recurring: message=string, schedule=cron_string, channel=string?
digest:          period=morning|evening -> {budget, spending, upcoming}
anomaly check:   -> [{type, severity, message, action}]
list reminders:  -> [{message, schedule, next_fire, channel}]
```

## Procedure

### 1. Set a one-time reminder

Record the message, time, and channel. Store under `~/.hermes/reminders/one-time/`:

```json
{
  "id": "remind_20261113_abc123",
  "message": "Take medication",
  "time": "2026-11-13T09:00:00Z",
  "channel": "terminal",
  "fired": false
}
```

Done when the reminder exists and fires at the correct time.

### 2. Set a recurring reminder

Record the message, schedule (cron string), and channel. Create a Hermes cron job:

```
cronjob(action="create",
        schedule="0 9 * * *",
        prompt="Run the lifestyle-reminder skill to fire the reminder: 'Take medication'",
        deliver="terminal")
```

Done when the cron job exists and the reminder fires on schedule.

### 3. Get a daily digest

Gather state for morning or evening:

- **Morning**: today's calendar events (if connected), budget status, upcoming reminders.
- **Evening**: today's spending total, budget progress, tomorrow's reminders.

Deliver as a concise message. Done when all sections are populated.

### 4. Run anomaly checks

Scan for conditions that need attention:

- Budget exceeded (`budget-tracking` status `exceeded`)
- Spending spike vs average
- Upcoming bill due dates
- Low budget remaining

Classify severity (`low`, `medium`, `high`) and suggest an action. Done when all anomalies are
detected with a clear next step.

### 5. List reminders

Summarize all active reminders: message, schedule, next fire time, channel. Done when every
reminder has a status.

## Pitfalls

- **Timezone.** Use the user's configured timezone, not server time.
- **Channel.** If no channel is specified, use the current chat channel.
- **Fire once.** One-time reminders should fire exactly once, then be marked as fired.
- **Spam.** Don't remind more frequently than the user requested. Respect cooldowns.
- **Missed fires.** If the agent was offline at fire time, report the missed reminder rather
  than silently skipping it.

## Verification

Run the test suite:

```bash
scripts/run_tests.sh tests/skills/test_lifestyle_reminder_skill.py -q
```

Test cases:
- Set a one-time reminder → fires at the correct time.
- Set a recurring reminder → creates a cron job, fires on schedule.
- Digest → returns budget status and upcoming reminders.
- Anomaly check → detects budget exceeded with severity.
- List reminders → all reminders have status and next fire time.