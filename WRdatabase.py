import nfldb

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
    global players

    players[str(pp.player)] = {'receiving_tar': 0,
                               'receiving_rec': 0,
                               'receiving_yds': 0,
                               'receiving_tds': 0,
                               'receiving_tds_bonus': 0,
                               'receiving_twoptm': 0,
                               'rushing_att': 0,
                               'rushing_yds': 0,
                               'rushing_tds': 0,
                               'rushing_tds_bonus': 0,
                               'rushing_twoptm': 0,
                               'passing_att': 0,
                               'passing_cmp': 0,
                               'passing_int': 0,
                               'passing_tds': 0,
                               'passing_tds_bonus': 0,
                               'passing_twoptm': 0,
                               'fumbles_lost': 0,
                               'fumbles_rec_tds': 0,
                               'kickret_tds': 0,
                               'puntret_tds': 0}


def get_wr_stats(pp):
    global players
    name = str(pp.player)

    # Receiving stats
    players[name]['receiving_tar'] += pp.receiving_tar
    players[name]['receiving_rec'] += pp.receiving_rec
    players[name]['receiving_yds'] += pp.receiving_yds
    players[name]['receiving_twoptm'] += pp.receiving_twoptm

    if pp.receiving_tds:
        # >= 50 yards
        if pp.receiving_yds >= 50:
            players[name]['receiving_tds_bonus'] += pp.receiving_tds
        # < 50 yards
        else:
            players[name]['receiving_tds'] += pp.receiving_tds

    # Rushing stats
    players[name]['rushing_att'] += pp.rushing_att
    players[name]['rushing_yds'] += pp.rushing_yds
    players[name]['rushing_twoptm'] += pp.rushing_twoptm

    if pp.rushing_tds:
        # >= 50 yards
        if pp.rushing_yds >= 50:
            players[name]['rushing_tds_bonus'] += pp.rushing_tds
        # < 50 yards
        else:
            players[name]['rushing_tds'] += pp.rushing_tds

    # Passing stats
    players[name]['passing_att'] += pp.passing_att
    players[name]['passing_cmp'] += pp.passing_cmp
    players[name]['passing_int'] += pp.passing_int
    players[name]['passing_twoptm'] += pp.passing_twoptm

    if pp.passing_tds:
        # > 50 yards
        if pp.passing_yds >= 50:
            players[name]['passing_tds_bonus'] += pp.passing_tds
        else:
            players[name]['passing_tds'] += pp.passing_tds

    # Misc stats
    players[name]['fumbles_lost'] += pp.fumbles_lost
    players[name]['fumbles_rec_tds'] += pp.fumbles_rec_tds
    players[name]['kickret_tds'] += pp.kickret_tds
    players[name]['puntret_tds'] += pp.puntret_tds


def main():
    global players

    # Connect to database
    db = nfldb.connect()
    # Conduct a query
    q = nfldb.Query(db)

    weeks = range(1, 2)

    players = {}

    for week in weeks:
        # q = nfldb.Query(db)
        games = q.game(season_year=2014, season_type='Regular', week=week).as_games()

        for game in games:
            for pp in game.play_players:
                # If player is a WR/TE or guess_position == WR
                if is_WR(pp):
                    try:
                        get_wr_stats(pp)
                    except KeyError:
                        add_player(pp)
                        get_wr_stats(pp)


    for player in players:
        print player, players[player]


if __name__ == '__main__':
    main()