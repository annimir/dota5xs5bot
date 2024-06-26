from messages.messages import message

herald = 'rank.herald'
guardian = 'rank.guardian'
crusader = 'rank.crusader'
archon = 'rank.archon'
legend = 'rank.legend'
ancient = 'rank.ancient'
divine = 'rank.divine'
titan = 'rank.titan'


def getRank(rank_tier: int, leaderboard_rank: int) -> str:
    if rank_tier // 10 == 1:
        return message(herald, 'rank', rank_tier % 10)
    elif rank_tier // 10 == 2:
        return message(guardian, 'rank', rank_tier % 10)
    elif rank_tier // 10 == 3:
        return message(crusader, 'rank', rank_tier % 10)
    elif rank_tier // 10 == 4:
        return message(archon, 'rank', rank_tier % 10)
    elif rank_tier // 10 == 5:
        return message(legend, 'rank', rank_tier % 10)
    elif rank_tier // 10 == 6:
        return message(ancient, 'rank', rank_tier % 10)
    elif rank_tier // 10 == 7:
        return message(divine, 'rank', rank_tier % 10)
    elif leaderboard_rank != 0:
        return message(titan, 'rank', leaderboard_rank)
    else:
        return message(titan, 'rank', '')


def getMmr(rank_tier: int) -> int:
    return ((rank_tier // 10 - 1) * 5 + rank_tier % 10) * 150


def getRatingFromPosition(position, min_rating=7800, max_rating=14500, min_rank=5000, max_rank=1):
    if position == 0:
        return f'5700 — {min_rating}'

    rating = min_rating + (max_rating - min_rating) * (min_rank - position) / (min_rank - max_rank)
    return round(rating)
