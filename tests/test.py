import unittest
import os
import mock
import shutil
from tig.tig import *

class TestTig(unittest.TestCase):

    def setUp(self):
        if not os.path.exists('.tig'):
            os.mkdir('.tig')


    def tearDown(self):
        if os.path.exists('.tig'):
            shutil.rmtree('.tig')


    def test_repo_exists(self):
        
        self.assertTrue(repo_exists())

    def test_repo_not_exists(self):
    
        shutil.rmtree('.tig')
        self.assertFalse(repo_exists())

    @mock.patch('tig.tig.repo_exists', return_value=True)
    def test_init_ko(self, repo_exists_function):
        self.assertFalse(init())

    @mock.patch('tig.tig.repo_exists', return_value=False)
    def test_init_ok(self, repo_exists_function):
        shutil.rmtree('.tig')
        self.assertTrue(init())
        self.assertTrue(os.path.exists('.tig'))
        self.assertTrue(os.path.exists('.tig/branches'))
        self.assertTrue(os.path.exists('.tig/branches/master'))
        self.assertTrue(os.path.exists('.tig/tmp'))


    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTig)
    unittest.TextTestRunner(verbosity=2).run(suite)