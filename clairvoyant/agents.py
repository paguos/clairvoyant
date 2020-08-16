import copy
import pandas as pd

from datetime import datetime
from fbprophet.plot import add_changepoints_to_plot
import matplotlib.pyplot as plt
from fbprophet import Prophet

from clairvoyant.utils import suppress_stdout_stderr


class ClairvoyantAgent:
    pass


class ProphetAgent(ClairvoyantAgent):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def set_arg(self, key, value):
        self.kwargs[key] = value

    def predict(self, data: dict, forecast_length: int, plot=False):

        df = pd.DataFrame.from_dict(data)
        if "cap" in self.kwargs:
            df["cap"] = self.kwargs["cap"]

        if "floor" in self.kwargs:
            df["floor"] = self.kwargs["floor"]

        model = Prophet(**self._clean_args())
        with suppress_stdout_stderr():
            model.fit(df)
            future = model.make_future_dataframe(periods=forecast_length)

        if "cap" in self.kwargs:
            future["cap"] = self.kwargs["cap"]

        if "floor" in self.kwargs:
            future["floor"] = self.kwargs["floor"]
        forecast = model.predict(future)

        prediction = {
            "trend": forecast["trend"].values.tolist()[-forecast_length:],
            "ds": self.format_dates(forecast["ds"])[-forecast_length:]
        }

        return prediction

    @staticmethod
    def format_dates(dates_df):
        dates = pd.to_datetime(dates_df).apply(lambda x: x.date())
        return [
            date.strftime("%Y-%m-%d") for date in dates
        ]

    def _clean_args(self):
        cleaned_args = copy.deepcopy(self.kwargs)
        if "cap" in self.kwargs:
            del cleaned_args["cap"]
        if "floor" in self.kwargs:
            del cleaned_args["floor"]
        return cleaned_args
