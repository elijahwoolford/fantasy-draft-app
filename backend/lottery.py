"""Draft lottery logic (ported from Streamlit prototype)."""

from __future__ import annotations

import random
from typing import Dict, List

# Team 1 = 37%, Team 2 = 28%, Team 3 = 20%, Team 4 = 15%
HARDCODED_ODDS = [37, 28, 20, 15]

TOTAL_NUMBERS = 10000


def assign_numbers(teams: Dict[str, float]) -> Dict[str, List[int]]:
    assigned_numbers: Dict[str, List[int]] = {}
    remaining_numbers = list(range(TOTAL_NUMBERS))

    for team, odds in teams.items():
        num_numbers = int(TOTAL_NUMBERS * (odds / 100))
        assigned = random.sample(remaining_numbers, num_numbers)
        assigned_numbers[team] = assigned
        remaining_numbers = [num for num in remaining_numbers if num not in assigned]

    return assigned_numbers


def lottery_draw(assigned_numbers: Dict[str, List[int]]) -> tuple[List[int], List[str]]:
    draft_order: List[str] = []
    all_numbers = sum(assigned_numbers.values(), [])
    drawn_numbers: List[int] = []

    while len(draft_order) < len(assigned_numbers):
        drawn_number = random.choice(all_numbers)
        drawn_numbers.append(drawn_number)

        for team, numbers in assigned_numbers.items():
            if drawn_number in numbers:
                if team not in draft_order:
                    draft_order.append(team)
                all_numbers = [num for num in all_numbers if num not in numbers]
                break

    return drawn_numbers, draft_order


def run_lottery(team_names: List[str]) -> List[str]:
    """
    Returns draft order: index 0 = #1 overall pick, index 3 = #4 pick.
    """
    if len(team_names) != 4:
        raise ValueError("Exactly four team names are required.")
    stripped = [n.strip() for n in team_names]
    if any(not n for n in stripped):
        raise ValueError("Team names must be non-empty.")
    if len(set(stripped)) != 4:
        raise ValueError("Team names must be unique.")

    teams = {name: float(odds) for name, odds in zip(stripped, HARDCODED_ODDS)}
    assigned = assign_numbers(teams)
    _, draft_order = lottery_draw(assigned)
    return draft_order
