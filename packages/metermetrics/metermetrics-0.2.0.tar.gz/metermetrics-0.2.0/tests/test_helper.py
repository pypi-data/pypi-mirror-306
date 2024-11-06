import unittest

import numpy as np

from metermetrics import helper


class HelperTest(unittest.TestCase):
    def test_mae(self):
        pred = np.array([1, 2, 3, 4, 5, 6])
        true = np.array([0, 2, 3, 4, 5, 6])

    def test_err(self):
        pred = 810.1
        true = 810.0
        assert helper.err(pred, true) == 0.1

        pred = np.array([0, 0, 1, 1, 1, 1])
        true = np.array([[0], [0], [1], [1], [1], [1]])
        assert helper.err(pred, true) == 0

        pred = np.array([0, 0, 1, 1, 1, 1])
        true = np.array([0, 0, 1, 1, 1, 1])
        assert helper.err(pred, true) == 0

        pred = np.array([0, 0, 1, 1, 0, 1])
        true = np.array([0, 0, 1, 1, 1, 1])
        assert helper.err(pred, true) == -1, helper.err(pred, true)

        pred = np.array([0, 0, 1, 1, 2, 1])
        true = np.array([0, 0, 1, 1, 1, 1])
        assert helper.err(pred, true) == 1, helper.err(pred, true)

        pred = 1
        true = 2
        assert helper.err(pred, true) == -0.1, helper.err(pred, true)

        # 003370, 004370
        pred = np.array([0.0, 0.0, 3.212705, 2.7218645, 7.1418715, 0.0])
        true = np.array([0.0, 0.0, 4.0, 3.0, 7.0, 0.0])
        assert helper.err(pred, true) == -100.0, helper.err(pred, true)

    def test_equal(self):
        pred, true = 1.0, 2.0

        assert not helper.equal(pred, true, strict=1)
        assert not helper.equal(pred, true, strict=0)

        pred, true = 1.0, 0.1
        assert not helper.equal(pred, true, strict=1)
        assert helper.equal(pred, true, strict=0)

        pred, true = 1.0, 1.1
        assert helper.equal(pred, true, strict=1)
        assert helper.equal(pred, true, strict=0)

        pred, true = 1.1, 1.1
        assert helper.equal(pred, true, strict=1)
        assert helper.equal(pred, true, strict=0)

        pred = np.array([1, 2, 3, 4, 5, 6])
        true = np.array([0, 2, 3, 4, 5, 6])
        assert not helper.equal(pred, true, strict=1)
        assert not helper.equal(pred, true, strict=0)

        pred = np.array([1, 2, 4, 4, 5, 5])
        true = np.array([1, 2, 4, 4, 5, 6])
        assert helper.equal(pred, true, strict=1)
        assert helper.equal(pred, true, strict=0)

        pred = np.array([1, 2, 4, 4, 6, 5])
        true = np.array([1, 2, 4, 4, 5, 6])
        assert not helper.equal(pred, true, strict=1)
        assert helper.equal(pred, true, strict=0)

        pred = np.array([0.0, 0.0, 3.212705, 2.7218645, 7.1418715, 0.0])
        true = np.array([0.0, 0.0, 4.0, 3.0, 7.0, 0.0])
        assert not helper.equal(pred, true, strict=0)

    def test_data_uniform(self):
        p = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        p = helper.data_uniform(p)
        assert p == 0

        p = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype="float32")
        p = helper.data_uniform(p)
        assert p == 0

        pred = np.array([0.0, 0.0, 3.212705, 2.7218645, 7.1418715, 0.0])
        p = helper.data_uniform(pred)
        assert p == 3370, p

    def test_transfer_to_normal(self):
        a = np.array(
            [
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        a = np.concatenate([a.copy().reshape(1, 6, -1) for i in range(11)])
        self.assertEqual(a.shape, (11, 6, 10))

        res = helper.transfer_to_normal(a)
        self.assertEqual(res.shape, (11, 6))
