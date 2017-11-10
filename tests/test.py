import unittest
import os
import mock
import shutil
from tig.tig import *
from tig.utils import *

class TestTig(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(ROOT):
            os.mkdir(ROOT)


    def tearDown(self):
        if os.path.exists(ROOT):
            shutil.rmtree(ROOT)


    def test_repo_exists(self):
        
        self.assertTrue(repo_exists())

    def test_repo_not_exists(self):
    
        shutil.rmtree(ROOT)
        self.assertFalse(repo_exists())

    @mock.patch('tig.tig.repo_exists', return_value=True)
    def test_init_ko(self, repo_exists_function):
        self.assertFalse(init())

    @mock.patch('tig.tig.repo_exists', return_value=False)
    def test_init_ok(self, repo_exists_function):
        shutil.rmtree(ROOT)
        self.assertTrue(init())
        self.assertTrue(os.path.exists(ROOT))
        self.assertTrue(os.path.exists(BRANCHES_FOLDER))
        self.assertTrue(os.path.exists(os.path.join(BRANCHES_FOLDER, DEFAULT_BRANCH)))
        self.assertTrue(os.path.exists(TMP_FOLDER))


    def test_get_current_branch(self):
        self.test_init_ok()
        self.assertEqual(get_current_branch(), DEFAULT_BRANCH)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTig)
    unittest.TextTestRunner(verbosity=2).run(suite)