from .helper import equal, err


class Counter:
    def __init__(self, epoch):
        self.epoch = epoch
        self.pred_list = []
        self.true_list = []
        self.err_list = []
        self.cnt = 0

    def add_val(self, pred, true):
        self.pred_list.append(pred)
        self.true_list.append(true)
        self.err_list.append(err(pred, true))
        self.cnt += 1

    def get_last_err(self, is_abs):
        if is_abs:
            return abs(self.err_list[-1])
        else:
            return self.err_list[-1]

    def is_cur_equal(self, strict):
        pred = self.pred_list[-1]
        true = self.true_list[-1]
        return equal(pred, true, strict)

    def get_mae(self):
        err_list = [abs(val) for val in self.err_list]
        sums = sum(err_list)
        if not err_list:
            return 0
        assert self.cnt == len(self.pred_list)
        return sums / self.cnt

    def get_mse(self):
        sums = 0

        for err_val in self.err_list:
            sums += err_val**2

        if sums == 0:
            return 0
        return sums / self.cnt

    def get_rmse(self):
        return self.get_mse() ** 0.5

    def get_max_error(self):
        err_list = [val for val in self.err_list]
        return max(err_list)

    def get_max_abs_err(self):
        if not self.err_list:
            return -1
        err_list = [abs(val) for val in self.err_list]
        return max(err_list)

    def get_strict_acc(self):
        return cal_acc(self.err_list, strict=1)

    def get_acc(self):
        return cal_acc(self.err_list, strict=0)

    def metrics_to_dict(self):
        row = dict(
            epoch=self.epoch,
            normal_acc=self.get_acc(),
            strict_acc=self.get_strict_acc(),
            MSE=self.get_mse(),
            MAE=self.get_mae(),
            RMSE=self.get_rmse(),
            MAX=self.get_max_abs_err(),
        )
        return row


def cal_acc(err_list: list, strict: bool):
    cnt = 0
    for val in err_list:
        if abs(val) <= 0.1:
            cnt += 1
        elif abs(val) < 1.0 and not strict:
            cnt += 1

    if cnt == 0:
        return 0
    return cnt / len(err_list)
