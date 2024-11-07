from os.path import abspath, dirname, join

import seq_dbutils

DATA_DIR = join(dirname(abspath(__file__)), 'data')

seq_dbutils.decrypt.BIN_FILE = join(DATA_DIR, 'test_decrypt.bin')


def test_initialize():
    key = '-zITTaJ8LJ_JFjsa6EG3ASlL-yZsxEYRmCX_wjaW34I='
    result = seq_dbutils.Decrypt.initialize(key)
    assert result == 'password'
