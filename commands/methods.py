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


