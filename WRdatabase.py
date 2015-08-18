import nfldb
import scoring

__author__ = 'hayntopdawg'


def is_WR(pp):
    if str(pp.player.position) == 'WR':
        return True
    elif str(pp.player.position) == 'TE':
        return True
    elif str(pp.player.position) == 'UNK' and str(pp.guess_position) == 'WR':
        return True
    else:
        return False


def add_player(pp):
    """
    Add player to players dictionary
    """
    global players

    players[pp.player_id] = {'name': pp.player.full_name,
                             'height': pp.player.height,
                             'weight': pp.player.weight,
                             'dob': pp.player.birthdate,
                             'seasons': {}}


def add_player_year(pp, season):
    """
    Add player's season to players dictionary
    """
    global players

    years_pro = pp.player.years_pro
    if years_pro is None:
        years_pro = 0
    players[pp.player_id]['seasons'][str(season)] = {'age': 0,  # need to add method
                                                     'years_pro': years_pro,  # need to add method
                                                     'weeks': {}}


def calc_age(pp, season, db):
    pass


# Assumes database is pulled up to current date
def calc_years_pro(pp, season, game, db):
    # global players
    # if pp.player.years_pro is None:
    # print 'pp.player:', pp.player, len(players[pp.player_id])-4
    # years_pro = len(players[pp.player_id])-4
    #     print 'years_pro', len(players[pp.player_id])-4
    #     print 'pp.player:', pp.player
    #     print 'pp.player.years_pro:', pp.player.years_pro
    #     print 'nfldb.current(db)[1]:', nfldb.current(db)[1]
    #     print 'game.season_year:', game.season_year
    # elif pp.player.years_pro - (nfldb.current(db)[1] - game.season_year) < 0:
    #     print 'pp.player:', pp.player.full_name
    #     print 'pp.player.years_pro:', pp.player.years_pro
    #     print 'nfldb.current(db)[1]:', nfldb.current(db)[1]
    #     print 'game.season_year:', game.season_year
    # else:
    #     print "Last season played:",
    #     years_pro = pp.player.years_pro
    # years_pro = pp.player.years_pro - (nfldb.current(db)[1] - game.season_year)
    # players[pp.player_id]['seasons'][str(season)]['years_pro'] = years_pro

    # If pp.player.years_pro is None
    #     Player should only have 1 season under seasons
    #     Years pro = 0 for 1 Rookie season

    # If pp.player.status == 'Active'
    #     If nfldb.current(db)[1] != max(season) in seasons
    #          Years pro for max(season) in seasons = pp.player.years_pro - 1
    #          Years pro - 1 for each season after
    #     Else
    #          Years pro for max(season) in seasons = pp.player.years_pro
    #          Years pro - 1 for each season after

    # If pp.player.status != 'Active'
    #     Years pro for max(season) in seasons = pp.player.years_pro
    #     Years pro - 1 for each season after

    pass


def add_player_week(pp, season, week):
    """
    Add player's week to players dictionary
    """
    players[pp.player_id]['seasons'][str(season)]['weeks'][str(week)] = {'team': '',
                                                                         'opponent': '',
                                                                         'at_home': '',  # boolean
                                                                         'receiving_tar': 0,
                                                                         'receiving_rec': 0,
                                                                         'receiving_yds': 0,
                                                                         'receiving_tds': 0,
                                                                         'receiving_tds_bonus': 0,
                                                                         'receiving_twopta': 0,
                                                                         'receiving_twoptm': 0,
                                                                         'rushing_att': 0,
                                                                         'rushing_yds': 0,
                                                                         'rushing_tds': 0,
                                                                         'rushing_tds_bonus': 0,
                                                                         'rushing_twopta': 0,
                                                                         'rushing_twoptm': 0,
                                                                         'passing_att': 0,
                                                                         'passing_cmp': 0,
                                                                         'passing_int': 0,
                                                                         'passing_tds': 0,
                                                                         'passing_tds_bonus': 0,
                                                                         'passing_twopta': 0,
                                                                         'passing_twoptm': 0,
                                                                         'fumbles_lost': 0,
                                                                         'fumbles_rec_tds': 0,
                                                                         'kickret_tds': 0,
                                                                         'puntret_tds': 0,
                                                                         'fp': 0}


def get_game_info(pp, season, week, game):
    global players
    player = players[pp.player_id]['seasons'][str(season)]['weeks'][str(week)]

    team = pp.team
    home = game.home_team
    away = game.away_team

    player['team'] = team
    if team == home:
        player['opponent'] = away
        player['at_home'] = True
    else:
        player['opponent'] = home
        player['at_home'] = False


def get_rec_stats(pp, season, week):
    global players
    player = players[pp.player_id]['seasons'][str(season)]['weeks'][str(week)]

    player['receiving_tar'] += pp.receiving_tar
    player['receiving_rec'] += pp.receiving_rec
    player['receiving_yds'] += pp.receiving_yds
    player['receiving_twopta'] += pp.receiving_twopta
    player['receiving_twoptm'] += pp.receiving_twoptm

    if pp.receiving_tds:
        # >= 50 yards
        if pp.receiving_yds >= 50:
            player['receiving_tds_bonus'] += pp.receiving_tds
        # < 50 yards
        else:
            player['receiving_tds'] += pp.receiving_tds


def get_rush_stats(pp, season, week):
    global players
    player = players[pp.player_id]['seasons'][str(season)]['weeks'][str(week)]

    player['rushing_att'] += pp.rushing_att
    player['rushing_yds'] += pp.rushing_yds
    player['rushing_twopta'] += pp.rushing_twopta
    player['rushing_twoptm'] += pp.rushing_twoptm

    if pp.rushing_tds:
        # >= 50 yards
        if pp.rushing_yds >= 50:
            player['rushing_tds_bonus'] += pp.rushing_tds
        # < 50 yards
        else:
            player['rushing_tds'] += pp.rushing_tds


def get_pass_stats(pp, season, week):
    global players
    player = players[pp.player_id]['seasons'][str(season)]['weeks'][str(week)]

    player['passing_att'] += pp.passing_att
    player['passing_cmp'] += pp.passing_cmp
    player['passing_int'] += pp.passing_int
    player['passing_twopta'] += pp.passing_twopta
    player['passing_twoptm'] += pp.passing_twoptm

    if pp.passing_tds:
        # > 50 yards
        if pp.passing_yds >= 50:
            player['passing_tds_bonus'] += pp.passing_tds
        else:
            player['passing_tds'] += pp.passing_tds


def get_misc_stats(pp, season, week):
    global players
    player = players[pp.player_id]['seasons'][str(season)]['weeks'][str(week)]

    player['fumbles_lost'] += pp.fumbles_lost
    player['fumbles_rec_tds'] += pp.fumbles_rec_tds
    player['kickret_tds'] += pp.kickret_tds
    player['puntret_tds'] += pp.puntret_tds


def get_wr_stats(pp, season, week):
    get_rec_stats(pp, season, week)  # Receiving stats
    get_rush_stats(pp, season, week)  # Rushing stats
    get_pass_stats(pp, season, week)  # Passing stats
    get_misc_stats(pp, season, week)  # Misc stats


def get_fp(name, season, week):
    global players
    player = players[name]['seasons'][str(season)]['weeks'][str(week)]
    player['fp'] = scoring.calc_off_fp(player)


def create_wr_db(seasons, weeks=range(1, 18)):
    global players
    players = {}

    # Connect to database
    db = nfldb.connect()

    for season in seasons:
        for week in weeks:
            # Conduct a query
            q = nfldb.Query(db)
            games = q.game(season_year=season, season_type='Regular', week=week).as_games()

            for game in games:
                for pp in game.play_players:
                    # If player is a WR/TE or guess_position == WR
                    if is_WR(pp):
                        if pp.player_id not in players:
                            add_player(pp)
                        if str(season) not in players[pp.player_id]['seasons']:
                            add_player_year(pp, season)
                            # add calc_age
                        if str(week) not in players[pp.player_id]['seasons'][str(season)]['weeks']:
                            add_player_week(pp, season, week)
                            get_game_info(pp, season, week, game)
                        get_wr_stats(pp, season, week)

    for player in players:
        for season in players[player]['seasons']:
            # calc years pro
            for week in players[player]['seasons'][season]['weeks']:
                get_fp(player, season, week)

    return players


if __name__ == '__main__':
    seasons = range(2013, 2015)
    weeks = range(1, 18)
    players = create_wr_db(seasons, weeks)
    i = 0
    for player in players:
        # print players[player]
        # break
        if i > 5: break
        print player, players[player]
        # print players[player]['name'], players[player]['seasons']['2014']['weeks']['1']['fp']
        i += 1
    # for season in players[player]['seasons']:
    #     print season
    #     print type(season)
    #     break
    # break

    # for player in players:
    #     for season in players[player]['seasons']:
    #         for week in players[player]['seasons'][season]:
    #             p = players[player]['seasons'][season][week]
    #             print p
    #             print type(p)
    #             print p['fp']
    #             break
    #         break
    #     break