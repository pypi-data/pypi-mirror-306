# coding: utf-8
"""
评价标准

"""

import numpy as np


def transfer_to_normal(res: np.array):
    """
    one-hot 数据转换
    :param res:
    :return:
    """
    assert res.shape[0] > 10, "size of dataset must bigger than 10"
    final = np.ones((res.shape[0], 6))
    for i in range(res.shape[0]):
        final[i] = np.argmax(res[i], axis=1)

    return final


def equal(pred, true, strict):
    """
    正常数据，最后一位误差不算作误差.
    <= 1, equal
    <= 10 and not strict, equal

    :param pred:
    :param true:
    :param strict: 最后一位误差如何判断
    :return:
    """

    # 008511 without point
    if abs(err(pred, true)) <= 0.1:
        return True
    if abs(err(pred, true)) < 1 and not strict:
        return True

    return False


def data_uniform(pred):
    """
    trans all kinds of data to int
    :param pred:
    :return:
    """
    if isinstance(pred, str):
        pred = int(pred)
    elif isinstance(pred, np.ndarray):
        if len(pred.shape) > 1:
            pred = pred.reshape(-1)
        if (
            pred.dtype == "float32"
            or pred.dtype == np.ndarray
            or pred.dtype == "float64"
        ):
            pred = np.around(pred)
            pred = pred.astype("int")

        pred = int("".join(pred.astype("str")))
    elif isinstance(pred, float):
        pred = int(pred * 10)
    return pred


def err(pred, true):
    """
    data must be:

    - 008101
    - 0, 0, 8, 1, 0, 0
    - 810.1

    :param pred:
    :param true:
    :return:
    """
    assert type(pred) == type(true)

    pred = data_uniform(pred)
    true = data_uniform(true)

    return (pred - true) / 10


def is_equal_combine(pred, true, strict=False):
    e1 = equal(pred[:-1], true[:-1], strict)
    e2 = equal(pred[-1], true[-1], strict)

    return e1 and e2


def mae_combine(pred, true):
    def mae(pred, true):
        """
        计算误差 MAE

        :param pred:
        :param true:
        :return:
        """

        assert pred.shape[0] == 6

        cnt = 5
        delta = 0

        # pred.shape = (6, )
        for i, j in zip(pred, true):
            assert cnt >= 0
            delta += int((i - j) * (10**cnt))
            cnt -= 1

        return abs(delta)

    return mae(pred[:-1], true[:-1])


def useFileName(cdf_filename):
    def get_filename(epoch):
        filename = cdf_filename % epoch
        return filename

    return get_filename
