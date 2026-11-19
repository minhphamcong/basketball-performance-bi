# Data dictionary

The preparation script creates one record per team per game from the home and away columns in `game.csv`.

| Output field | Meaning |
|---|---|
| `game_id` | Source game identifier |
| `game_date` | Game date parsed as a date/time |
| `season_id` | Source season identifier; filter using the exact value in the CSV |
| `season_type` | Source season type, when present |
| `team_id`, `team_abbreviation`, `team_name` | Team represented by this row |
| `opponent_id`, `opponent_abbreviation`, `opponent_name` | Opposing team |
| `venue` | Home or Away, derived from the source side |
| `result` | Source W/L value, when present |
| `plus_minus` | Source team plus/minus, when present |
| `opponent_points` | Opponent's points in the game |
| `points`, `field_goals_made`, `field_goals_attempted`, `field_goal_pct_source` | Team scoring and field-goal fields |
| `three_pointers_made`, `three_pointers_attempted`, `three_point_pct_source` | Three-point fields |
| `free_throws_made`, `free_throws_attempted`, `free_throw_pct_source` | Free-throw fields |
| `offensive_rebounds`, `defensive_rebounds`, `rebounds`, `assists`, `steals`, `blocks`, `turnovers`, `personal_fouls` | Other source team statistics, when present |

Blank values mean the source did not provide that statistic. Percentage fields ending in `_source` are retained for comparison; derive percentages from makes/attempts for validation and document the zero-attempt handling.
