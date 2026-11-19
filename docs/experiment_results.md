# Experiment validation results

## Evaluation type

This run is a reproducible data-integrity and dashboard task-answer check. No human participants were recruited. Therefore, it reports no user completion times, usability ratings, or interview feedback. The task answers below are computed from the prepared dataset and spot-checked against the open Power BI report; they are not evidence of user-perceived usability.

## Dataset

- Prepared file: `data/processed/team_games_2022_23.csv` (local, excluded from Git)
- Scope: NBA 2022–23 regular season
- Rows: 2,460 team-game records
- Games: 1,230
- Teams: 30
- Dates: 2022-10-18 through 2023-04-09
- Required fields checked for nulls: game ID/date, team/opponent, venue, result, and both scores; none found.

## Data validation

The dataset was checked for duplicate game/team rows, two team records per game, one home and one away record per game, a W and L per game, and reciprocal score reconciliation between opponents. These checks passed.

## Predefined task answers

| Task | Computed answer | Result |
|---|---|---|
| Select Lakers (`LAL`) and find the season record | 82 games; 43 wins, 39 losses | Pass |
| Find Lakers' average points and win rate | 117.17 points/game; 52.4% | Pass |
| Find Lakers' highest-scoring game | 2022-11-26 at San Antonio Spurs; 143–138, win | Pass |
| Change team filter to Boston (`BOS`) | 82 games; 57 wins | Pass |
| Compare Lakers home and away records | Home: 23–18; Away: 20–21 | Pass |

## Power BI spot check

With `LAL` selected in the report, Power BI showed 82 Games Played, 43 Wins, Average Points 117.17, and Win Rate 0.52. The table total showed 9,608 Lakers points. These match the prepared CSV after rounding. The win-rate card is currently displayed as a decimal; format the measure as Percentage with one decimal place to show 52.4%.

## Limitations and interpretation

- The checks establish consistency within the prepared CSV, not independent correctness against a second official source.
- Task answers were calculated from the CSV; no real participant comparison or measured task time was conducted.
- The prototype evaluates team-game data only and does not test player-level box-score analytics.
- A favorable answer to a data query does not show that BI improves basketball outcomes.

## Reproduce

From the repository root, after installing `requirements.txt`:

```powershell
.\.venv\Scripts\python.exe src\validate_experiment.py
```

To validate another prepared CSV:

```powershell
.\.venv\Scripts\python.exe src\validate_experiment.py --input path\to\team_games.csv
```
