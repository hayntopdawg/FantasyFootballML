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


def add_player(pp, year, week):
    """
    Create a player with stats set to zero
    """
    global players

    players[str(pp.player)] = {'name': pp.player.full_name}
    players[str(pp.player)][str(year)] = {}
    players[str(pp.player)][str(year)][str(week)] = {'team': '',  # need to add method
                                                     'opponent': '',  # need to add method
                                                     'home': '',  # need to add method (True or False)
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


def get_rec_stats(pp, season, week):
    global players
    player = players[str(pp.player)][str(season)][str(week)]

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
    player = players[str(pp.player)][str(season)][str(week)]

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
    player = players[str(pp.player)][str(season)][str(week)]

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
    player = players[str(pp.player)][str(season)][str(week)]

    player['fumbles_lost'] += pp.fumbles_lost
    player['fumbles_rec_tds'] += pp.fumbles_rec_tds
    player['kickret_tds'] += pp.kickret_tds
    player['puntret_tds'] += pp.puntret_tds


def get_wr_stats(pp, season, week):
    # Receiving stats
    get_rec_stats(pp, season, week)

    # Rushing stats
    get_rush_stats(pp, season, week)

    # Passing stats
    get_pass_stats(pp, season, week)

    # Misc stats
    get_misc_stats(pp, season, week)


def get_fp(name, season, week):
    global players
    player = players[name][str(season)][str(week)]

    player['fp'] = scoring.calc_off_fp(player)


def main():
    global players

    # Connect to database
    db = nfldb.connect()
    # Conduct a query
    q = nfldb.Query(db)

    seasons = range(2014, 2015)
    weeks = range(1, 2)

    players = {}

    for season in seasons:
        for week in weeks:
            # q = nfldb.Query(db)
            games = q.game(season_year=season, season_type='Regular', week=week).as_games()

            for game in games:
                for pp in game.play_players:
                    # If player is a WR/TE or guess_position == WR
                    if is_WR(pp):
                        try:
                            get_wr_stats(pp, season, week)
                        except KeyError:
                            add_player(pp, season, week)
                            get_wr_stats(pp, season, week)
            for player in players:
                get_fp(player, season, week)


if __name__ == '__main__':
    main()
    # print players
    # i = 0
    for player in players:
        # if i > 25: break
        print player, players[player]['2014']['1']['fp']
        # i += 1