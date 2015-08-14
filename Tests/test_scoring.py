import scoring
from unittest import TestCase

__author__ = 'FujNasty'


class Test_Scoring(TestCase):
    # Test Passing
    def test_calc_pass_fp_tds(self):
        player = {'passing_tds': 3}
        self.assertEquals(scoring.cal_pass_fp(player), 12)

    def test_calc_pass_fp_tds_bonus(self):
        player = {'passing_tds_bonus': 2}
        self.assertEquals(scoring.cal_pass_fp(player), 16)

    def test_calc_pass_fp_100_yds(self):
        player = {'passing_yds': 305}
        self.assertEquals(scoring.cal_pass_fp(player), 6)

    def test_calc_pass_fp_twoptm(self):
        player = {'passing_twoptm': 2}
        self.assertEquals(scoring.cal_pass_fp(player), 4)

    def test_calc_pass_fp_int(self):
        player = {'passing_int': 2}
        self.assertEquals(scoring.cal_pass_fp(player), -4)

    def test_calc_pass_fp_all(self):
        player = {'passing_tds': 2, 'passing_tds_bonus': 1, 'passing_yds': 267, 'passing_twoptm': 0, 'passing_int': 3}
        self.assertEquals(scoring.cal_pass_fp(player), 8+8+5+0-6)

    # Test Rushing
    def test_calc_rush_fp_tds(self):
        player = {'rushing_tds': 3}
        self.assertEquals(scoring.cal_rush_fp(player), 18)

    def test_calc_rush_fp_tds_bonus(self):
        player = {'rushing_tds_bonus': 2}
        self.assertEquals(scoring.cal_rush_fp(player), 24)

    def test_calc_rush_fp_100_yds(self):
        player = {'rushing_yds': 221}
        self.assertEquals(scoring.cal_rush_fp(player), 11)

    def test_calc_rush_fp_twoptm(self):
        player = {'rushing_twoptm': 2}
        self.assertEquals(scoring.cal_rush_fp(player), 4)

    def test_calc_rush_fp_all(self):
        player = {'rushing_tds': 1, 'rushing_tds_bonus': 1, 'rushing_yds': 153, 'rushing_twoptm': 1}
        self.assertEquals(scoring.cal_rush_fp(player), 6+12+7+2)

    # Test Receiving
    def test_calc_rec_fp_tds(self):
        player = {'receiving_tds': 2}
        self.assertEquals(scoring.cal_rec_fp(player), 12)

    def test_calc_rec_fp_tds_bonus(self):
        player = {'receiving_tds_bonus': 1}
        self.assertEquals(scoring.cal_rec_fp(player), 12)

    def test_calc_rec_fp_100_yds(self):
        player = {'receiving_yds': 100}
        self.assertEquals(scoring.cal_rec_fp(player), 5)

    def test_calc_rec_fp_twoptm(self):
        player = {'receiving_twoptm': 1}
        self.assertEquals(scoring.cal_rec_fp(player), 2)

    def test_calc_rec_fp_all(self):
        player = {'receiving_tds': 1, 'receiving_tds_bonus': 1, 'receiving_yds': 118, 'receiving_twoptm': 0}
        self.assertEquals(scoring.cal_rec_fp(player), 6+12+5+0)