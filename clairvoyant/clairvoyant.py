
import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime
from pathlib import Path

from loguru import logger
from sklearn.metrics import mean_squared_error

from clairvoyant.agents import ClairvoyantAgent


class Clairvoyant:

    def __init__(self, data: dict, training_ratio: float):
        self.data = self._validate_data(data)
        self.training_ratio = self._validate_training_ratio(training_ratio)
        self.time_range = data["ds"]

        data_size = len(list(self.data.values())[0])
        self.training_size = int(data_size * self.training_ratio)
        self.test_size = data_size - self.training_size

        self.training_data = {}
        self.test_data = {}

        for k, v in self.data.items():
            self.training_data[k] = v[:self.training_size]
            self.test_data[k] = v[self.training_size:]

    def set_agent(self, agent: ClairvoyantAgent):
        self.agent = agent
        Path(
            f"logs/{type(self.agent).__name__}").mkdir(parents=True, exist_ok=True)

    def train(self, arg, start, end, interval, plot=True):
        value = start
        logger.info(f"Training '{arg}' in '{type(self.agent).__name__}' ...")
        training_results = []

        while value <= end:
            logger.info(f"Training with {arg} -> {value} ...")
            forecast, error = self._run_agent(arg, value)

            training_results.append(
                {
                    "error": error,
                    "forecast": forecast,
                    "value": value
                }
            )
            logger.info(f"Training with {arg} -> {value}: error -> {error}")
            value += interval

        if plot:
            plt.figure(f"train_err_{arg}")

            x = np.array([r["value"] for r in training_results])
            y = np.array([r["error"] for r in training_results])
            plt.plot(x, y, label="error")
            plt.legend(loc="upper left")
            plt.savefig(
                f"logs/{type(self.agent).__name__}/train_err_{arg}.png"
            )

        optimal_experiment = min(training_results, key=lambda k: k["error"])
        self.plot(optimal_experiment["forecast"], arg)
        self.agent.kwargs[arg] = optimal_experiment["value"]
        logger.info(f"Optimal value for {arg}: {optimal_experiment['value']}")
        logger.info(
            f"Training '{arg}' in '{type(self.agent).__name__}' ... done!"
        )

    def predict(self, periods):

        plt.figure(f"prediction_{periods}")

        forecast = self.agent.predict(
            self.data, periods, plot=True
        )

        self._plot_set(self.data, "data")
        self._plot_set(forecast, "forecast")

        plt.legend(loc="upper left")
        plt.savefig(
            f"logs/{type(self.agent).__name__}/prediction_{periods}.png"
        )
        return forecast

    def _run_agent(self, arg, value):
        self.agent.kwargs[arg] = value
        forecast = self.agent.predict(
            self.training_data, self.test_size
        )

        y_true = self.test_data["y"]
        y_pred = forecast["trend"]
        error = mean_squared_error(y_true, y_pred)
        return forecast, error

    def plot(self, forecast, arg):
        plt.figure(f"train_{arg}")
        self._plot_set(self.training_data, label="training")
        self._plot_set(self.test_data, label="test")
        self._plot_set(forecast, label="forecast")
        plt.legend(loc="upper left")
        plt.savefig(f"logs/{type(self.agent).__name__}/train_{arg}.png")

    @staticmethod
    def _plot_set(dataset, label):
        dates = [
            datetime.strptime(d, "%Y-%m-%d")
            for d in np.array(dataset["ds"])
        ]
        for k in dataset.keys():
            if k != "ds":
                y = np.array(dataset[k])
                plt.plot_date(
                    dates, y,
                    label=label,
                    linestyle='solid',
                    marker='None'
                )

    @staticmethod
    def _validate_data(data) -> dict:
        if "ds" not in data:
            raise ValueError("Dataset has not 'ds' key!")
        if len(data.keys()) < 2:
            raise ValueError("Dataset must have at least 2 keys!")

        values_lengths = [len(v) for v in list(data.values())]
        if len(set(values_lengths)) > 1:
            raise ValueError("All columns/values need the same length!")
        return data

    @staticmethod
    def _validate_training_ratio(training_ratio) -> float:
        if training_ratio < 0 or training_ratio > 1:
            raise ValueError("Training ratio must be between 0 and 1!")
        return training_ratio
