import json
import os
import pathlib

import numpy as np
import seaborn as sns
from pylab import exp, plot, show

# from pkg.recorder.db.relation.helper import save_epoch_data
from .helper import get_filename


class PredictResults:
    def __init__(self, parent_dir, prefix, run_name):
        self.cdf = list()
        self.ids = list()
        self.pred_list = list()
        self.true_list = list()

        self.run_name = run_name
        self.parent_dir = pathlib.Path(parent_dir)

        self.update_results_dir(prefix)
        self._create_dirs()

    def update_results_dir(self, prefix):
        self.cdf_dir = self.parent_dir / 'cdf' / prefix

    def _create_dirs(self):
        os.makedirs(self.parent_dir / "cdf", exist_ok=True)
        os.makedirs(self.cdf_dir, exist_ok=True)

    def insert(self, err_val, cur_id, pred, true, epoch):
        self.cdf.append(err_val)
        self.ids.append(str(cur_id))
        self.pred_list.append(str(pred))
        self.true_list.append(str(true))
        self._save2db(epoch, pred, true, err_val, cur_id)

    def _save_graph(self, epoch):
        """
        draw cdf graph.
        :param epoch:
        :return:
        """
        sns.set(color_codes=True)
        sns_plot = sns.distplot(
            tuple(self.cdf),
            bins=20,
            hist_kws=dict(cumulative=True),
            kde_kws=dict(cumulative=True),
        )
        fig = sns_plot.get_figure()
        fig.savefig(self.cdf_dir / (get_filename(epoch=epoch) + ".png"))

    def _save2db(self, epoch, pred, true, cdf, img_id):
        data = dict(
            run_name=self.run_name,
            epoch=epoch,
            pred=pred,
            true=true,
            cdf=cdf,
            img_id=img_id,
        )
        # save_epoch_data(data)

    def _save_data_json(self, epoch):
        """
        save to output dir, with json.
        :param epoch:
        :return:
        """
        filename = get_filename(epoch=epoch)
        data = dict(
            cdf=self.cdf, ids=self.ids, pred=self.pred_list, true=self.true_list
        )
        with open(self.cdf_dir / filename, "w") as outfile:
            json.dump(data, outfile)

    def save(self, epoch):
        self._save_data_json(epoch=epoch)
        self._save_graph(epoch=epoch)


def draw_cdf():
    dx = 0.01
    X = np.arange(-2, 2, dx)
    Y = exp(-X ** 2)

    # Normalize the data to a proper PDF
    Y /= (dx * Y).sum()

    # Compute the CDF
    CY = np.cumsum(Y * dx)

    plot(X, Y)
    plot(X, CY, "r--")

    show()
