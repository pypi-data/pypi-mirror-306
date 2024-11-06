# metric-logger

Install:

```bash
pip install metric-logger
```

Example:
```python
from metric_logger.logger import MetricLogger


metric_logger = MetricLogger("metrics", "metrics.csv")
metrics = [
    dict(metric="accuracy", score=0.85, epoch=0, fold=0),
    dict(metric="accuracy", score=0.95, epoch=1, fold=0),
]
for metric in metrics:
    metric_logger.add(metric)
```