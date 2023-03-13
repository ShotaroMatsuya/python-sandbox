import os
import calculation
import files
import pytest


def test_add_num_and_double():
    cal = calculation.Cal()
    assert cal.add_num_and_double(1, 1) == 4


class TestCal(object):
    @classmethod
    def setup_class(cls):
        print('start')
        cls.cal = calculation.Cal()
        cls.files = files.File()
        cls.test_dir = '/tmp/test_dir'
        cls.test_file_name = 'test.txt'
    
    @classmethod
    def teardown_class(cls):
        print('end')
        del cls.cal
        del cls.files
        import shutil
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)
    
    def setup_method(self, method):
        print('method={}'.format(method.__name__))
        # self.cal = calculation.Cal()
    
    def teardown_method(self, method):
        print('method={}'.format(method.__name__))
        # del self.cal
    
    def test_add_num_and_double(self):
        assert self.cal.add_num_and_double(1, 1) == 4
        
    @pytest.mark.skip(reason='skip!')
    def test_add_num_and_double_raise(self):
        with pytest.raises(ValueError):
            self.cal.add_num_and_double('1', '1')
            
    # pytest pytest_calculation.py  -rs -s --os-name mac
    def test_add_num_and_double_os(self, request):
        os_name = request.config.getoption('--os-name')
        print(os_name)
        if os_name == 'mac':
            print('ls')
        elif os_name == 'windows':
            print('dir')
        assert self.cal.add_num_and_double(1, 1) == 4
            
    def test_save(self, tmpdir):
        self.files.save(tmpdir, self.test_file_name)
        test_file_path = os.path.join(
            tmpdir, self.test_file_name
        )
        assert os.path.exists(test_file_path) is True

    def test_add_num_and_double_fixture(self, csv_file):
        print(csv_file)
        assert self.cal.add_num_and_double(1, 1) == 4

    def test_add_num_and_double_raise_no_skip(self):
        with pytest.raises(ValueError):
            self.cal.add_num_and_double('1', '1')
    
    def test_save_no_dir(self):
        self.files.save(self.test_dir, self.test_file_name)
        test_file_path = os.path.join(
            self.test_dir, self.test_file_name
        )
        assert os.path.exists(test_file_path) is True
    

# coverage check
# pytest pytest_calculation.py --cov=calculation -rs -s
# pytest pytest_calculation.py --cov=files -rs -s
