# metermetrics

`metermetrics` is for meter reading metric computing.

Given `pred` and `true`, you could get:

- mae
- mse
- rmse
- acc
- sacc

For more details, you could find them in [HRC-mCNNs: A Hybrid Regression and Classification Multibranch CNNs for Automatic Meter Reading With Smart Shell](https://ieeexplore.ieee.org/document/9854084/).

## Install

`pip install metermetrics`

## Usage

```python
# create counter
from metermetrics.counter import Counter
c = Counter(epoch=50) # epoch nums. NOT EPOCH NO.
c.add_val(pred, true) # your values

c.get_mse()
```