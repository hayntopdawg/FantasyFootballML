import scoring
from unittest import TestCase

__author__ = 'FujNasty'


class Test_Scoring(TestCase):
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