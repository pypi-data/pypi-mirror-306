import unittest

from metermetrics.counter import Counter, cal_acc


class CounterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.c = Counter(0)

    def test_counter(self):
        pred_list = [1, 1, 1, 1, 1, 1, 1]
        true_list = [1, 1, 1, 1, 1, 1, 1]
        c = Counter(0)

        for pred, true in zip(pred_list, true_list):
            c.add_val(pred, true)

        assert c.get_mae() == 0
        assert c.get_mse() == 0
        assert c.get_rmse() == 0
        assert c.get_max_error() == 0

    def test_cur_equal(self):
        c = Counter(0)
        c.add_val(2.0, 1.0)
        assert not c.is_cur_equal(strict=0)

        c.add_val(1.0, 1.0)
        assert c.is_cur_equal(1)

        c.add_val(1.1, 1.0)
        assert c.is_cur_equal(1)

        c.add_val(1.2, 1.0)
        assert not c.is_cur_equal(1)

    def test_max_error_and_max_abs_error(self):
        pred_list = [4, 1, 2, 2, 2, 1, 1]
        true_list = [1, 4, 1, 8, 3, 1, 1]

        c = Counter(0)
        for pred, true in zip(pred_list, true_list):
            c.add_val(pred, true)

        assert c.get_max_error() == 0.3, c.get_max_error()
        assert c.get_max_abs_err() == 0.6, c.get_max_error()

        pred_list = [4.0, 1.0, 2.0, 2.0, 2.0, 1.0, 1.0]
        true_list = [1.0, 4.0, 1.0, 8.0, 3.0, 1.0, 1.0]

        c = Counter(0)
        for pred, true in zip(pred_list, true_list):
            c.add_val(pred, true)

        assert c.get_max_error() == 3.0, c.get_max_error()
        assert c.get_max_abs_err() == 6.0, c.get_max_error()

    def test_last_err(self):
        self.c.add_val(1.0, 2.0)
        assert self.c.get_last_err(is_abs=1) == 1.0
        assert self.c.get_last_err(is_abs=0) == -1.0

        self.c.add_val(1.1, 2.0)
        assert self.c.get_last_err(is_abs=1) == 0.9
        assert self.c.get_last_err(is_abs=0) == -0.9

        self.c = Counter(0)
        self.c.add_val(1, 2)
        assert self.c.get_last_err(is_abs=1) == 0.1, self.c.get_last_err(is_abs=1)
        assert self.c.get_last_err(is_abs=0) == -0.1, self.c.get_last_err(is_abs=0)

    @unittest.skip
    def test_get_acc(self):
        """
        TODO: need this.
        :return:
        """
        pass

    def test_to_dict(self):
        pred_list = [1, 1, 1, 1, 1, 1, 1]
        true_list = [1, 1, 1, 1, 1, 1, 1]
        c = Counter(0)

        for pred, true in zip(pred_list, true_list):
            c.add_val(pred, true)

        mdict = c.metrics_to_dict()
        keys = ["epoch", "normal_acc", "strict_acc", "MSE", "MAE", "RMSE", "MAX"]
        for key in mdict.keys():
            assert key in keys


class CalTest(unittest.TestCase):
    def test_cal_acc(self):
        res = cal_acc([0.1, 0.1, 0.1, 0, 0], strict=1)
        assert res == 1.0, res

        res = cal_acc([0.1, 0.1, 0.1, 0, 0], strict=0)
        assert res == 1.0, res

        res = cal_acc([0.2, 0.1, 0.1, 0, 0], strict=0)
        assert res == 1.0

        res = cal_acc([0.2, 0.1, 0.1, 0, 0], strict=1)
        assert res == 0.8

        res = cal_acc([1.2, 0.1, 0.1, 0, 0], strict=0)
        assert res == 0.8

        res = cal_acc([1.2, 0.1, 0.1, 0, 0], strict=1)
        assert res == 0.8

        res = cal_acc([-1.2, 0.1, -0.1, 0, 0], strict=1)
        assert res == 0.8
