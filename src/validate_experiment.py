"""Run reproducible data-integrity and task-answer checks on team-game CSV."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


KEY_COLUMNS = [
    "game_id",
    "game_date",
    "team_abbreviation",
    "opponent_abbreviation",
    "venue",
    "result",
    "points",
    "opponent_points",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/processed/team_games_2022_23.csv"),
        help="Normalized team-game CSV (default: %(default)s)",
    )
    args = parser.parse_args()

    data = pd.read_csv(args.input, low_memory=False)
    missing_columns = sorted(set(KEY_COLUMNS).difference(data.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    errors: list[str] = []
    nulls = data[KEY_COLUMNS].isna().sum()
    if nulls.any():
        errors.append(f"Required-field nulls: {nulls[nulls > 0].to_dict()}")
    if data.duplicated(["game_id", "team_abbreviation"]).any():
        errors.append("Duplicate game_id + team_abbreviation rows found")

    teams_per_game = data.groupby("game_id")["team_abbreviation"].nunique()
    venues_per_game = data.groupby("game_id")["venue"].nunique()
    if not teams_per_game.eq(2).all():
        errors.append("At least one game does not have exactly two teams")
    if not venues_per_game.eq(2).all():
        errors.append("At least one game does not have one home and one away row")

    # Each team's points must equal the opponent row's opponent_points, and each
    # game must contain one W and one L.
    for game_id, game in data.groupby("game_id"):
        if len(game) != 2:
            errors.append(f"Game {game_id} has {len(game)} rows instead of 2")
            continue
        rows = game.to_dict("records")
        if sorted(row["result"] for row in rows) != ["L", "W"]:
            errors.append(f"Game {game_id} does not contain one W and one L")
        for row in rows:
            other = next((item for item in rows if item["team_abbreviation"] != row["team_abbreviation"]), None)
            if other and row["points"] != other["opponent_points"]:
                errors.append(f"Points do not reconcile for game {game_id}")
                break

    lakers = data[data["team_abbreviation"].eq("LAL")]
    celtics = data[data["team_abbreviation"].eq("BOS")]
    if lakers["game_id"].nunique() != 82:
        errors.append("LAL expected 82 games")
    if (lakers["result"] == "W").sum() != 43 or (lakers["result"] == "L").sum() != 39:
        errors.append("LAL expected record 43 wins and 39 losses")
    if celtics["game_id"].nunique() != 82 or (celtics["result"] == "W").sum() != 57:
        errors.append("BOS expected 82 games and 57 wins")
    lakers_by_venue = lakers.groupby("venue")["result"].agg(
        games="count", wins=lambda values: (values == "W").sum()
    )
    expected_venue = {"Home": (41, 23), "Away": (41, 20)}
    for venue, (expected_games, expected_wins) in expected_venue.items():
        actual = lakers_by_venue.loc[venue] if venue in lakers_by_venue.index else None
        if actual is None or actual["games"] != expected_games or actual["wins"] != expected_wins:
            errors.append(f"LAL {venue.lower()} expected {expected_games} games and {expected_wins} wins")

    print(f"Rows: {len(data):,}; games: {data['game_id'].nunique():,}; teams: {data['team_abbreviation'].nunique()}")
    print(f"Date range: {data['game_date'].min()} to {data['game_date'].max()}")
    print(
        "LAL: "
        f"{lakers['game_id'].nunique()} games, "
        f"{(lakers['result'] == 'W').sum()} W / {(lakers['result'] == 'L').sum()} L, "
        f"{lakers['points'].sum():.0f} points, "
        f"{lakers['points'].mean():.2f} points/game, "
        f"{(lakers['result'] == 'W').mean():.1%} win rate"
    )
    highest = lakers.loc[lakers["points"].idxmax()]
    print(
        "LAL highest-scoring game: "
        f"{highest['game_date']} vs {highest['opponent_name']} ({highest['venue']}), "
        f"{highest['points']:.0f}-{highest['opponent_points']:.0f}, {highest['result']}"
    )
    print(f"BOS filter check: {celtics['game_id'].nunique()} games, {(celtics['result'] == 'W').sum()} wins")
    print(
        "LAL venue check: "
        f"Home {lakers_by_venue.loc['Home', 'wins']}-{lakers_by_venue.loc['Home', 'games'] - lakers_by_venue.loc['Home', 'wins']}; "
        f"Away {lakers_by_venue.loc['Away', 'wins']}-{lakers_by_venue.loc['Away', 'games'] - lakers_by_venue.loc['Away', 'wins']}"
    )

    if errors:
        print("VALIDATION FAILED:")
        for error in sorted(set(errors)):
            print(f"- {error}")
        raise SystemExit(1)
    print("VALIDATION PASSED")


if __name__ == "__main__":
    main()
