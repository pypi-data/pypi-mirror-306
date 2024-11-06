import pandas as pd
from pyPhases.exporter.PickleExporter import PickleExporter
from pyPhases.Data import DataNotFound


class PandasExporter(PickleExporter):
    
    def __init__(self, options=None):
        super().__init__(options)
        self.df = None
        self.dataHandler = True
    
    def checkType(self, type):
        return type in [pd.DataFrame]
    
    def getDataHandler(self, data):
        self.df = data
        return self

    def read(self, dataId, options={}, **kwargs):
        data = super().read(dataId, options)
        df = pd.DataFrame(data)
        self.df = df

        return self
    
    def write(self, dataId, object: pd.DataFrame, options={}, **kwargs):
        # to list
        data = object.to_dict("records")
        super().write(dataId, data, options)


    def get(self, **kwargs):
        """
        Retrieves a single row (as dict) from the DataFrame based on the provided keyword arguments.
        If no keyword arguments are provided, returns the entire DataFrame.
        """
                
        if self.df is None:
            raise DataNotFound("Data was never read")
        
        if kwargs:
            return self.df.loc[(self.df[list(kwargs)] == pd.Series(kwargs)).all(axis=1)].iloc[0].to_dict()

        return self.df