import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

class DataBunch():
    def __init__(self, path, file_name, quat, d_type=None):
        self.path = Path(path)
        self.file_name = file_name
        self.quat = quat
        self.d_type = d_type
        
    def data_to_series(self):
        data = pd.read_csv(self.path/self.file_name, header=None)
        year, month, day, _ = list(data.iloc[0,:])
        
        start = pd.to_datetime(f'{int(year)}-{int(month)}-{int(day)}')
        end = start + timedelta(days=data.shape[0]-1)
        date_range = pd.date_range(start=start, end=end)
        
        series = pd.Series(index=date_range, data=data.iloc[:,3].values).astype(float)
        
        return series[series > 0]
    
    def yearly_mean(self, save=False):
        series = self.data_to_series()
        resampled = series.resample('Y').mean()
        df = pd.DataFrame({'Quat':self.quat,
                           'Year':resampled.index.year, 
                           f'{self.d_type}':resampled.values
                          })
        
        if save:
            df.to_csv(self.path/f'{self.d_type}_year.csv', index=False)
        else:
            return df
        
    
    def monthly_mean(self, save=False):
        series = self.data_to_series()
        resampled = series.groupby(series.index.month).mean()
        df = pd.DataFrame({'Quat':self.quat,
                           'Month':resampled.index, 
                           f'{self.d_type}':resampled.values
                          })
        
        if save:
            df.to_csv(self.path/f'{self.d_type}_month.csv', index=False)
        else:
            return df