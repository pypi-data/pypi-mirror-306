# tests/test_gcair.py



import unittest
from gcair.gc_air import GCAir


class TestGCAir(unittest.TestCase):

    def setUp(self):
        """在每个测试方法前创建 Calculator 实例"""
        self.calc = GCAir()

if __name__ == "__main__":
    unittest.main()