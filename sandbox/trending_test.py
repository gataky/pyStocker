import unittest

class Trending_Tests(unittest.TestCase):

    def setUp(self):

        import trending

        self.trender = trending.Trending

        self.u   = [10, 11, 12, 13, 14, 15]
        self.d   = [15, 14, 13, 12, 11, 10]
        self.ud  = [10, 11, 12, 13, 12, 11]
        self.du  = [15, 14, 13, 12, 13, 14]
        self.udu = [10, 11, 12, 13, 12, 11, 12, 13]
        self.dud = [13, 12, 11, 12, 13, 12, 11, 10]

    def test_setUp(self):
        pass

    def test_strings(self):
        self.assertEqual(self.trender(["0", "1", "2"], 1).getTrend(), [True, True, True])


    def test_init_trending(self):
        self.assertEqual(self.trender(self.u, 1)._initialize_trend(), (True, [True, True]))
        self.assertEqual(self.trender(self.d, 1)._initialize_trend(), (False, [False, False]))


    def test_getTrend_up(self):
        self.assertEqual(self.trender(self.u, 1).getTrend(), [True, True, True, True, True, True])

    def test_getTrend_down(self):
        self.assertEqual(self.trender(self.d, 1).getTrend(), [False, False, False, False, False, False])

    def test_trending_up_down(self):
        self.assertEqual(self.trender(self.ud, 1).getTrend(), [True, True, True, True, False, False])

    def test_trending_down_up(self):
        self.assertEqual(self.trender(self.du, 1).getTrend(), [False, False, False, False, True, True])

    def test_getTrend_up_down_up(self):
        self.assertEqual(self.trender(self.udu, 1).getTrend(), [True, True, True, True, False, False, True, True])

    def test_getTrend_down_up_down(self):
        self.assertEqual(self.trender(self.dud, 1).getTrend(), [False, False, False, True, True, False, False, False])



    def test_trending_up_down_larger_r(self):
        self.assertEqual(self.trender(self.ud, 1.01).getTrend(), [True, True, True, True, True, False])

    def test_trending_down_up_larger_r(self):
        self.assertEqual(self.trender(self.du, 1.01).getTrend(), [False, False, False, False, False, True])

    def test_trending_up_down_up_larger_r(self):
        self.assertEqual(self.trender(self.udu, 1.01).getTrend(), [True, True, True, True, True, False, False, True])

    def test_trending_down_up_down_larger_r(self):
        self.assertEqual(self.trender(self.dud, 1.01).getTrend(), [False, False, False, False, True, True, False, False])



    def test_trending_up_down_smaller_r(self):
        self.assertEqual(self.trender(self.ud, .99).getTrend(), [True, True, True, True, False, False])

    def test_trending_down_up_smaller_r(self):
        self.assertEqual(self.trender(self.du, .99).getTrend(), [False, False, False, False, True, True])

    def test_trending_up_down_up_smaller_r(self):
        self.assertEqual(self.trender(self.udu, .99).getTrend(), [True, True, True, True, False, False, True, True])

    def test_trending_down_up_down_smaller_r(self):
        self.assertEqual(self.trender(self.dud, .99).getTrend(), [False, False, False, True, True, False, False, False])


    def test_data_reversed(self):
        self.assertEqual(self.trender(self.u[::-1], 1, True).getTrend(), [True, True, True, True, True, True])
        self.assertEqual(self.trender(self.u[::-1], 1, False).getTrend(), [False, False, False, False, False, False])


if __name__ == "__main__":

    unittest.main()
