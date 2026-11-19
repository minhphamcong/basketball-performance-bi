# Basketball Performance BI

Project-management and BI prototype for analyzing basketball team performance from game-level statistics.

## Project scope

The first reproducible version analyzes team performance by game using the NBA `game.csv` table. It converts home/away columns into one row per team per game, then filters a selected season and team. The available files do not include a player-by-game box-score table, so player-level performance is outside this prototype's current data scope.

## Repository contents

- `src/prepare_data.py`: creates a normalized team-game CSV from `game.csv`.
- `data/`: instructions and a location for local data; raw and processed data are not committed.
- `powerbi/`: instructions for building the report in Power BI Desktop.
- `docs/`: data dictionary, methodology, and experiment plan.

## Requirements

- Python 3.10 or newer
- Python package in `requirements.txt`
- Power BI Desktop (optional, for the dashboard)
- The source basketball dataset, obtained from its original provider under its applicable license

## Reproduce the data preparation (Windows PowerShell)

From the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

Keep the original CSV outside Git, or place it locally at `data/raw/game.csv`. Then run either:

```powershell
py src/prepare_data.py --input data/raw/game.csv --output data/processed/team_game_stats.csv
```

Or provide the path to your existing dataset:

```powershell
py src/prepare_data.py --input "E:\tri tue kinh doanh\archive\csv\game.csv" --output data/processed/team_game_stats.csv
```

To focus on one season and one team, pass the exact `season_id` and team abbreviation found in the CSV, for example:

```powershell
py src/prepare_data.py --input "E:\tri tue kinh doanh\archive\csv\game.csv" --output data/processed/lal_team_games.csv --season-id 22023 --team LAL
```

The season example is illustrative: inspect your CSV first and use a season ID and abbreviation that exist in your data. The output is a local file and is intentionally ignored by Git.

## Build the dashboard

Open Power BI Desktop, import the generated CSV from `data/processed/`, and create visuals described in [`powerbi/README.md`](powerbi/README.md). Save the `.pbix` locally. Before sharing it, check whether it embeds source data and whether your dataset license allows redistribution.

## Data and limitations

Document the dataset's actual source, version, access date, and license in [`data/README.md`](data/README.md). Do not upload the multi-gigabyte play-by-play file or any source data unless its license and repository size permit it. The current pipeline supports team-game analysis only; it does not derive player box scores from play-by-play events.

## Experiment

The proposed evaluation compares a small set of predefined information-finding tasks using a spreadsheet and the BI dashboard. Record task completion, correctness, time, and participant feedback. This prototype can evaluate data preparation and dashboard usability; it cannot establish that the system improves win rates.
