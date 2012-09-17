import unittest

import trending

class Trending_Tests(unittest.TestCase):
    
    def setUp(self):
                
        self.trend = trending.trending
        
        self.u   = [10, 11, 12, 13, 14, 15]
        self.d   = [15, 14, 13, 12, 11, 10]
        self.ud  = [10, 11, 12, 13, 12, 11]
        self.du  = [15, 14, 13, 12, 13, 14]
        self.udu = [10, 11, 12, 13, 12, 11, 12, 13]
        self.dud = [13, 12, 11, 12, 13, 12, 11, 10]
        
    def test_setUp(self):
        pass
        
    def test_trending_up(self):
        self.assertEqual(self.trend(self.u, 1), [True, True, True, True, True, True])
        
    def test_trending_down(self):
        self.assertEqual(self.trend(self.d, 1), [False, False, False, False, False, False])
        
    def test_trending_up_down(self):
        self.assertEqual(self.trend(self.ud, 1), [True, True, True, True, False, False])

    def test_trending_down_up(self):
        self.assertEqual(self.trend(self.du, 1), [False, False, False, False, True, True])
        
    def test_trending_up_down_larger_r(self):
        self.assertEqual(self.trend(self.ud, 1.01), [True, True, True, True, True, False])

    def test_trending_down_up_larger_r(self):
        self.assertEqual(self.trend(self.du, 1.01), [False, False, False, False, False, True])

    def test_trending_up_down_smaller_r(self):
        self.assertEqual(self.trend(self.ud, .99), [True, True, True, True, False, False])
        
    def test_trending_down_up_smaller_r(self):
        self.assertEqual(self.trend(self.du, .99), [False, False, False, False, True, True])
        
    def test_trending_up_down_up(self):
        self.assertEqual(self.trend(self.udu, 1), [True, True, True, True, False, False, True, True])
        
    def test_trending_down_up_down(self):
        self.assertEqual(self.trend(self.dud, 1), [False, False, False, True, True, False, False, False])

    def test_trending_up_down_up_larger_r(self):
        self.assertEqual(self.trend(self.udu, 1.01), [True, True, True, True, True, False, False, True])

    def test_trending_down_up_down_larger_r(self):
        self.assertEqual(self.trend(self.dud, 1.01), [False, False, False, False, True, True, False, False])

    def test_trending_up_down_up_smaller_r(self):
        self.assertEqual(self.trend(self.udu, .99), [True, True, True, True, False, False, True, True])

    def test_trending_down_up_down_smaller_r(self):
        self.assertEqual(self.trend(self.dud, .99), [False, False, False, True, True, False, False, False])

if __name__ == "__main__":
    
    unittest.main()
