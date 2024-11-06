from metric_logger.logger import MetricLogger
from metric_logger.utils import init_logger


def test_metric_logger(tmp_path):
    # Arrange
    logger_name = "METRIC_LOGGER"
    init_logger(name=logger_name, path=tmp_path / "metrics.csv")
    metric_logger = MetricLogger(logger_name)

    # Act
    metrics = [
        dict(metric="accuracy", score=0.85, epoch=0, fold=0),
        dict(metric="accuracy", score=0.95, epoch=1, fold=0),
    ]
    for metric in metrics:
        metric_logger.add(metric)

    # Assert
    expected_data = "metric,score,epoch,fold\naccuracy,0.85,0,0\naccuracy,0.95,1,0\n"
    with open(tmp_path / "metrics.csv", "r") as f:
        assert f.read() == expected_data
