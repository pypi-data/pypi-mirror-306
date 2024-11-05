from picologger.logger import MetricLogger
from picologger.utils import init_logger


def test_metric_logger(tmp_path):
    # Arrange
    logger_name = "METRIC_LOGGER"
    init_logger(name=logger_name, path=tmp_path / "metrics.csv")
    metric_logger = MetricLogger(logger_name)

    # Act
    metric_logger.add({
        "metric": "accuracy",
        "score": 0.85,
    })
    metric_logger.add({
        "score": 0.95,
        "metric": "accuracy",
    })

    # Assert
    expected_file = "metric,score\naccuracy,0.85\naccuracy,0.95\n"
    with open(tmp_path / "metrics.csv", "r") as f:
        assert f.read() == expected_file
