class NumericAccuracy(object):
    def __init__(self, epoch):
        self.epoch = epoch
        self.pred_list = []
        self.true_list = []
        self.err_list = []
        self.cnt = 0

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
