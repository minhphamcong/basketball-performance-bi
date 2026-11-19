"""Normalize NBA game.csv home/away columns into one row per team per game."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


STAT_COLUMNS = {
    "points": "pts",
    "field_goals_made": "fgm",
    "field_goals_attempted": "fga",
    "field_goal_pct_source": "fg_pct",
    "three_pointers_made": "fg3m",
    "three_pointers_attempted": "fg3a",
    "three_point_pct_source": "fg3_pct",
    "free_throws_made": "ftm",
    "free_throws_attempted": "fta",
    "free_throw_pct_source": "ft_pct",
    "offensive_rebounds": "oreb",
    "defensive_rebounds": "dreb",
    "rebounds": "reb",
    "assists": "ast",
    "steals": "stl",
    "blocks": "blk",
    "turnovers": "tov",
    "personal_fouls": "pf",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Path to source game.csv")
    parser.add_argument("--output", required=True, type=Path, help="Path for normalized output CSV")
    parser.add_argument("--season-id", help="Optional exact season_id to retain")
    parser.add_argument("--team", help="Optional team abbreviation to retain, e.g. LAL")
    return parser.parse_args()


def normalize_side(frame: pd.DataFrame, side: str) -> pd.DataFrame:
    suffix = f"_{side}"
    required = [f"team_id{suffix}", f"team_abbreviation{suffix}", f"team_name{suffix}", f"pts{suffix}"]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"game.csv is missing required columns: {', '.join(missing)}")

    result = pd.DataFrame(
        {
            "game_id": frame["game_id"].astype("string"),
            "game_date": pd.to_datetime(frame["game_date"], errors="coerce"),
            "season_id": frame["season_id"].astype("string"),
            "season_type": frame.get("season_type", pd.Series(pd.NA, index=frame.index)).astype("string"),
            "team_id": frame[f"team_id{suffix}"].astype("string"),
            "team_abbreviation": frame[f"team_abbreviation{suffix}"].astype("string").str.strip().str.upper(),
            "team_name": frame[f"team_name{suffix}"].astype("string").str.strip(),
            "opponent_id": frame[f"team_id{'_away' if side == 'home' else '_home'}"].astype("string"),
            "opponent_abbreviation": frame[f"team_abbreviation{'_away' if side == 'home' else '_home'}"].astype("string").str.strip().str.upper(),
            "opponent_name": frame[f"team_name{'_away' if side == 'home' else '_home'}"].astype("string").str.strip(),
            "venue": "Home" if side == "home" else "Away",
            "result": frame[f"wl{suffix}"].astype("string").str.strip().str.upper() if f"wl{suffix}" in frame.columns else pd.Series(pd.NA, index=frame.index, dtype="string"),
            "plus_minus": pd.to_numeric(frame[f"plus_minus{suffix}"], errors="coerce") if f"plus_minus{suffix}" in frame.columns else pd.Series(pd.NA, index=frame.index),
        }
    )

    opponent_side = "away" if side == "home" else "home"
    result["opponent_points"] = pd.to_numeric(frame.get(f"pts_{opponent_side}"), errors="coerce")
    for output_name, source_base in STAT_COLUMNS.items():
        source = f"{source_base}{suffix}"
        if source in frame.columns:
            result[output_name] = pd.to_numeric(frame[source], errors="coerce")
    return result


def main() -> None:
    args = parse_args()
    if not args.input.is_file():
        raise FileNotFoundError(f"Input CSV not found: {args.input}")

    games = pd.read_csv(args.input, low_memory=False)
    required = {"game_id", "game_date", "season_id"}
    missing = sorted(required.difference(games.columns))
    if missing:
        raise ValueError(f"game.csv is missing required columns: {', '.join(missing)}")

    team_games = pd.concat([normalize_side(games, "home"), normalize_side(games, "away")], ignore_index=True)
    if args.season_id:
        team_games = team_games[team_games["season_id"] == str(args.season_id)]
    if args.team:
        team_games = team_games[team_games["team_abbreviation"] == args.team.strip().upper()]

    team_games = team_games.sort_values(["game_date", "game_id", "team_abbreviation"], na_position="last")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    team_games.to_csv(args.output, index=False, na_rep="")
    print(f"Wrote {len(team_games):,} team-game rows to {args.output}")


if __name__ == "__main__":
    main()
