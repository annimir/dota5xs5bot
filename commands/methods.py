from itertools import combinations

import numpy as np

from messages.messagePath import herald, guardian, crusader, archon, legend, ancient, divine, titan
from messages.messages import message


def getRank(language: str, rank_tier: int, leaderboard_rank: int) -> str:
    if rank_tier // 10 == 1:
        return message(language, herald, 'rank', rank_tier % 10)
    elif rank_tier // 10 == 2:
        return message(language, guardian, 'rank', rank_tier % 10)
    elif rank_tier // 10 == 3:
        return message(language, crusader, 'rank', rank_tier % 10)
    elif rank_tier // 10 == 4:
        return message(language, archon, 'rank', rank_tier % 10)
    elif rank_tier // 10 == 5:
        return message(language, legend, 'rank', rank_tier % 10)
    elif rank_tier // 10 == 6:
        return message(language, ancient, 'rank', rank_tier % 10)
    elif rank_tier // 10 == 7:
        return message(language, divine, 'rank', rank_tier % 10)
    elif leaderboard_rank != 0:
        return message(language, titan, 'rank', leaderboard_rank)
    else:
        return message(language, titan, 'rank', '')


def getMmr(rank_tier: int) -> int:
    return ((rank_tier // 10 - 1) * 5 + rank_tier % 10) * 150


def getRatingFromPosition(position, min_rating=7800, max_rating=14500, min_rank=5000, max_rank=1):
    if position == 0:
        return f'5700 — {min_rating}'

    rating = min_rating + (max_rating - min_rating) * (min_rank - position) / (min_rank - max_rank)
    return round(rating)


def isAllNumbersInRoles(lst: []):
    return all(isinstance(x, int) and 1 <= x <= 5 for x in lst)


def convertStrRoletToIntRole(args: []):
    new_list = []
    for arg in args:
        if len(arg) == 1 and arg.isdigit():
            digit = int(arg)
            if 1 <= digit <= 5:
                new_list.append(digit)
            else:
                new_list.append(arg)
        else:
            new_list.append(arg)
    return new_list


def balance_teams(accepted_users):
    ratings = np.array([user['mmr'] for user in accepted_users])

    def team_difference(indices):
        team1 = ratings[indices]
        team2 = ratings[~indices]
        return abs(np.mean(team1) - np.mean(team2))

    best_difference = float('inf')
    best_team = None
    for indices in combinations(range(10), 5):
        indices = np.array(indices)
        difference = team_difference(indices)
        if difference < best_difference:
            best_difference = difference
            best_team = indices

    team1_ids = [accepted_users[i] for i in best_team]
    team2_ids = [accepted_users[i] for i in range(10) if i not in best_team]
    return team1_ids, team2_ids
