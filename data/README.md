# Dataset instructions

Place a locally obtained `game.csv` in `data/raw/`, or pass its path directly to `src/prepare_data.py`. Raw and generated CSV files are excluded from Git by `.gitignore`.

Before submitting, record the dataset's provider, dataset name/version, download or access date, URL, and license/terms here. The user's local folder name is not sufficient source attribution. Do not redistribute data unless its terms allow it. The `play_by_play.csv` file in the supplied collection is very large and is not needed for this team-game prototype.

## Files used

- Required: `game.csv` (one row per game with home and away team statistics).
- Optional future extensions: `line_score.csv` for quarter scoring; `other_stats.csv` for additional team statistics. These are not required by the current preparation script.

## Data handling

Keep an untouched copy of the source data. The preparation script writes a separate normalized output. Missing historical statistics remain blank; they are not silently replaced with zero.
