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


    def test_get_current_branch(self):
        self.test_init_ok()
        self.assertEqual(get_current_branch(), 'master')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTig)
    unittest.TextTestRunner(verbosity=2).run(suite)