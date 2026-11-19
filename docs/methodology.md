# Experimental methodology

## Research question

Can a BI dashboard help a user answer predefined questions about a team's game-by-game performance accurately and efficiently?

## Scope

Use one season and one team selected from the available `game.csv`. Analyze team-game statistics only. Player-level box-score analysis requires a separate player-game dataset and is not inferred from this source table.

## Preparation

1. Preserve the original source CSV unchanged.
2. Record its provider, version, access date, URL, and license in `data/README.md`.
3. Run `src/prepare_data.py` with an exact season ID and team abbreviation.
4. Check missing values and validate selected rows against the source.
5. Independently recalculate field-goal percentages for sample rows and compare them with source percentages.

## Dashboard questions

- What is the team's win/loss record in the selected scope?
- How do points and point differential vary by game?
- How do shooting, rebounds, assists, and turnovers differ between wins and losses?
- Are home and away results different in this selected sample?

## User evaluation

Give participants the same 3–5 information-finding tasks in a spreadsheet and the dashboard. Record task completion, correctness, completion time, requests for help, and brief usability feedback. Treat a small convenience sample as exploratory, not representative of all teams or coaches.

## Limits

This experiment assesses data preparation and dashboard usability. It cannot demonstrate that the dashboard causes improved team performance or more wins. Interpret comparisons with sample size, season, opponents, and missing source statistics in mind.
