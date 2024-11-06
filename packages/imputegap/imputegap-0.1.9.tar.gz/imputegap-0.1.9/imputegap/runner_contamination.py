from imputegap.recovery.manager import TimeSeries
from imputegap.tools import utils

# 1. initiate the TimeSeries() object that will stay with you throughout the analysis
ts_1 = TimeSeries()

# 2. load the timeseries from file or from the code
ts_1.load_timeseries(data=utils.search_path("eeg-alcohol"), max_series=100, max_values=1000, header=False)
ts_1.normalize(normalizer="min_max")

# [OPTIONAL] you can plot your raw data / print the information
ts_1.print(view_by_series=True)
ts_1.plot(raw_data=ts_1.data, title="EEG - Raw Data", max_series=3)

# 3. contamination of the data with MCAR scenario
infected_matrix = ts_1.Contaminate.missing_percentage(ts=ts_1.data, series_impacted=0.4, missing_rate=0.4)

# [OPTIONAL] you can plot your raw data / print the contamination
ts_1.print(limit=10)
ts_1.plot(ts_1.data, infected_matrix, title="EEG - MCAR Contamination", max_series=1, save_path="./assets")