import pytest

from lottery import run_lottery


def test_run_lottery_returns_all_four_teams_in_some_order() -> None:
    teams = ["Alpha", "Bravo", "Charlie", "Delta"]
    result = run_lottery(teams)
    assert len(result) == 4
    assert set(result) == set(teams)


def test_run_lottery_rejects_wrong_team_count() -> None:
    with pytest.raises(ValueError, match="Exactly four"):
        run_lottery(["A", "B", "C"])


def test_run_lottery_rejects_duplicate_names() -> None:
    with pytest.raises(ValueError, match="unique"):
        run_lottery(["A", "A", "B", "C"])


def test_run_lottery_rejects_empty_name() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        run_lottery(["A", "B", "C", "   "])
