#! python2

# import nflgame
from __future__ import division

__author__ = 'hayntopdawg'

# R-Unit Fantasy Point Values
# Passing
PASSING_YDS_FP = 1 / 50  # Every 50 passing yards
PASSING_TD_FP = 4
PASSING_TD_BONUS_FP = 4 + PASSING_TD_FP  # 50+ yard TD pass bonus
PASSING_TWOPT_FP = 2
PASSING_INT_FP = -2

# Rushing
RUSHING_YDS_FP = 1 / 20  # Every 20 rushing yards
RUSHING_TD_FP = 6
RUSHING_TD_BONUS_FP = 6 + RUSHING_TD_FP  # 50+ yard TD rush bonus
RUSHING_TWOPT_FP = 2

# Receiving
RECEIVING_YDS_FP = 1 / 20  # Every 20 rushing yards
RECEIVING_TD_FP = 6
RECEIVING_TD_BONUS_FP = 6 + RECEIVING_TD_FP  # 50+ yard TD rush bonus
RECEIVING_TWOPT_FP = 2

# Misc
FUM_LOST_FP = -2

# Kicking
LONG_FG_MADE_FP = 6  # 50+ yard field goal
FG_MADE_FP = 3  # 0-49 yard field goal
PAT_MADE_FP = 1

# D/ST
INT_RET_TD_FP = 6
FUM_RET_TD_FP = 6
KICK_RET_TD_FP = 12
PUNT_RET_TD_FP = 12
BLOCK_KICK_RET_TD_FP = 6
DEF_INT_FP = 2
FUM_REC_FP = 2
SAFETY_FP = 2
ALLOW_0_FP = 10
ALLOW_6_FP = 6  # 1-6 points allowed
ALLOW_13_FP = 4  # 7-13 points allowed
ALLOW_17_FP = 2  # 14-17 points allowed
ALLOW_21_FP = 1  # 18-21 points allowed


def calc_off_fp(player, game):
    points = 0

    # Passing points
    try:
        points += player.passing_tds * PASSING_TD_FP
        points += player.passing_yds / 25 * PASSING_YDS_FP
        points += player.passing_twoptm * RECEIVING_TWOPT_FP
        points += player.passing_ints * PASSING_INT_FP
    except:
        pass

    # Rushing points
    try:
        points += player.rushing_tds * RUSHING_TD_FP
        points += player.rushing_yds / 10 * RUSHING_YDS_FP
        points += player.rushing_twoptm * RUSHING_TWOPT_FP
    except:
        pass

    # Receiving points
    try:
        points += player.receiving_tds * RECEIVING_TD_FP
        points += player.receiving_yds / 10 * RECEIVING_YDS_FP
        points += player.receiving_twoptm * RECEIVING_TWOPT_FP
    except:
        pass

    # Misc Offense
    try:
        points += player.fumbles_lost * FUM_LOST_FP
    except:
        pass

    # Kicking
    if 'kicking_fgm' in player._stats:
        points += calc_fg_pts(player, game)
    try:
        points += player.kicking_xpmade
    except:
        pass

    return points


def cal_pass_fp(player):
    points = 0
    try:
        points += int(player['passing_tds'] * PASSING_TD_FP)
    except KeyError:
        pass

    try:
        points += int(player['passing_tds_bonus'] * PASSING_TD_BONUS_FP)
    except KeyError:
        pass

    try:
        points += int(player['passing_yds'] * PASSING_YDS_FP)
    except KeyError:
        pass

    try:
        points += int(player['passing_twoptm'] * PASSING_TWOPT_FP)
    except KeyError:
        pass

    try:
        points += int(player['passing_int'] * PASSING_INT_FP)
    except KeyError:
        pass


    return points


def cal_rush_fp(player):
    points = 0
    try:
        points += int(player['rushing_tds'] * RUSHING_TD_FP)
    except KeyError:
        pass

    try:
        points += int(player['rushing_tds_bonus'] * RUSHING_TD_BONUS_FP)
    except KeyError:
        pass

    try:
        points += int(player['rushing_yds'] * RUSHING_YDS_FP)
    except KeyError:
        pass

    try:
        points += int(player['rushing_twoptm'] * RUSHING_TWOPT_FP)
    except KeyError:
        pass

    return points


def cal_rec_fp(player):
    points = 0
    try:
        points += int(player['receiving_tds'] * RECEIVING_TD_FP)
    except KeyError:
        pass

    try:
        points += int(player['receiving_tds_bonus'] * RECEIVING_TD_BONUS_FP)
    except KeyError:
        pass

    try:
        points += int(player['receiving_yds'] * RECEIVING_YDS_FP)
    except KeyError:
        pass

    try:
        points += int(player['receiving_twoptm'] * RECEIVING_TWOPT_FP)
    except KeyError:
        pass

    return points


def calc_fg_pts(player, game):
    plays = game.drives.plays()
    pts = 0
    fgm = find_num_kicks(plays, 'kicking_fgm', kicking_fgm__ge=1, kicking_fgm_yds__lt=50)
    fgm_long = find_num_kicks(plays, 'kicking_fgm', kicking_fgm__ge=1, kicking_fgm_yds__ge=50)

    pts += (fgm * FG_MADE_FP if fgm else 0)
    pts += (fgm_long * LONG_FG_MADE_FP if fgm_long else 0)

    return pts


def find_num_kicks(plays, stat, **kwargs):
    for player in plays.filter(**kwargs).players():
        return getattr(player, stat)

        # season2014week1 = nflgame.games(2014, week=1)
        #
        # # One way to calculate all of the fantasy points for the week may be to find all of the fantasy scoring stats per player
        # # then calculate the points
        #
        # for n, game in enumerate(season2014week1):
        # # if n > 0: break
        #     for num, p in enumerate(game.players):
        #         # if num > 0: break
        #         if 'defense_tkl' in p._stats: continue # no defensive players will be on a roster
        #         pts = calc_off_fp(p, game)
        #         print "{} {} ({}, {}) scored {} pts".format(p.player.first_name, p.player.last_name, p.player.position, p.team, str(pts))
        #         # print "\t{}".format(p.formatted_stats())
        #
        #         # print p.__dict__
        #         # print p.player.__dict__
        #         # print p, p._stats
        #         # print p.name
        #         # print p.player
        #         # calc_fg_pts(p, game)