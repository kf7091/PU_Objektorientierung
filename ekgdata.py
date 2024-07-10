import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from tinydb import TinyDB
from tinydb.table import Table, Document
import os

class EKGdata:

    def __init__(self, ekg_id:int):
        ekg_table = EKGdata.load_ekg_table()
        self.id = ekg_table.get(doc_id=ekg_id).doc_id
        self.date = datetime.strptime(ekg_table.get(doc_id=ekg_id)["date"], "%Y-%m-%d")
        self.data_link = ekg_table.get(doc_id=ekg_id)["result_link"]
        self.df = pd.read_csv(self.data_link, sep='\t', header=None, names=['EKG in mV','Time in ms',])
        self.legnth = self.df['Time in ms'].iloc[-1]-self.df['Time in ms'].iloc[0]

    
    def find_peaks(self, threshold:float, respacing_factor:int=5) -> list:
        '''
        A function to find the peaks in a series
        ### Parameters
        - Args:
            - threshold (`float`): The threshold for the peaks
            - respacing_factor (`int`): The factor to respace the series
        - Returns:
            - self.peaks (`list`): A list of the indices of the peaks
        '''
        
        # Respace the series
        series = self.df["EKG in mV"].iloc[::respacing_factor]
    
        # Filter the series
        series = series[series>threshold]


        self.peaks = []
        last = 0
        current = 0
        next = 0

        for index, row in series.items():
            last = current
            current = next
            next = row

            if last < current and current >= next and current > threshold:
                self.peaks.append(index-respacing_factor)

        return self.peaks
    
    def estimate_hr(self) -> pd.Series:
        ''' 
        Estimate the heart rate from the R-peaks found in the EKG data
        ### Parameters
        - Args:
        - Returns:
            - self.hr_pds (`pd.Series`): A pandas series with the heart rate values
        '''
        # Check if self.peaks exists
        if not hasattr(self, 'peaks'):
            raise ValueError("No peaks found - please run find_peaks() first")
        else:
            hr_list = []
            time_list = []
            for i in range(1, len(self.peaks)):
                # Calculate the time delta between two peaks in ms (for better readability)
                time_delta_ms = self.df['Time in ms'].iloc[self.peaks[i]] - self.df['Time in ms'].iloc[self.peaks[i-1]]
                # Append the time of the peak to the list and start at 0
                time_list.append(self.df['Time in ms'].iloc[self.peaks[i]] - self.df['Time in ms'].iloc[self.peaks[0]])
                # Calculate the heart rate in bpm and append it to the list
                hr_list.append(60000/time_delta_ms)

            # Create a pandas series with the heart rate values and the time of the peaks
            self.hr_pds = pd.Series(hr_list, name="HR", index=time_list)
            return self.hr_pds

        
    def plot_hr_series(self, accuracy:int=25) -> go.Figure:
        '''
        Plot the Heartrate data with the peaks found
        ### Parameters
        - Args:
            - accuracy (`int`): The accuracy of the rolling mean
        - Returns:
            - self.time_series (`plotly.graph_objects.Figure`): A plotly figure with the EKG data
        '''

        # check if self.hr_pds exists
        if not hasattr(self, 'hr_pds'):
            self.estimate_hr(self)
        
        self.hr_plot = go.Figure()

        # create a scatter plot with the heartrate values
        self.hr_plot.add_trace(go.Scatter(
            name="Herzfrequenz",
            x=self.hr_pds.index/1000,
            y=self.hr_pds,
            mode='markers',
            visible='legendonly'
        ))
            
        # create a line plot with the rolling mean of the heartrate values
        avg_hr_pds = self.hr_pds.rolling(window=accuracy, min_periods=1).mean()
        self.hr_plot.add_trace(go.Scatter(
            name="Durchschnittliche Herzfrequenz",
            x=avg_hr_pds.index/1000,
            y=avg_hr_pds,
            mode='lines',
            line_shape='spline'
        ))

        # update the layout of the plot
        self.hr_plot.update_layout(
            title="Herzfrequenz",
            xaxis_title="Zeit in s",
            yaxis_title="Herzfrequenz in bpm",
            xaxis=dict(
                rangeslider=dict(
                visible=True
                ),
                type="linear"
            )
        )
        # move the legend to the top
        self.hr_plot.update_legends(
            orientation="h",
            y=1,
            x=0.5,
            xanchor="center",
            yanchor="bottom"
        )

        return self.hr_plot

        #old code
        '''# create a plotly figure with the raw EKG data and time in seconds
        self.time_series = go.Figure(data=go.Scatter(x=self.df["Time in ms"]/1000, y=self.df["EKG in mV"]))
        # create a scatter plot with the R-peaks and add it to the figure
        r_peaks = go.Scatter(x=self.df["Time in ms"].iloc[self.peaks]/1000, y=self.df["EKG in mV"].iloc[self.peaks], mode='markers', marker=dict(color='red', size=8))
        self.time_series.add_trace(r_peaks)
        return self.time_series'''
    

    '''
    @staticmethod
    def load_by_id(self, person_id:int, ekg_id:int):
        ekg_dict = json.load(open("data/person_db.json"))[person_id-1]["ekg_tests"][ekg_id-1]
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV','Time in ms',])

        return self
    '''

    @staticmethod
    def get_ekgids_by_personid(person_id:int) -> list:
        '''
        Staticmethod which gets all ekg_ids which belong to the given person_id
        ### Parameters
        - Args:
            - ekg_table (`TinyBD.table_class`): Table of all ekgs
            - person_id (`int`): id of the person
        - Returns: 
            - ekg_ids (`list`): list of the coresponding ekgs
        '''
        ekg_ids = []
        for document in EKGdata.load_ekg_table():
            if document["person_id"] == person_id:
                ekg_ids.append(document.doc_id)
        return ekg_ids
    
    @staticmethod
    def load_ekg_table() -> Table:
        '''
        A Function that knows where the person Database is and returns a TinyDB-Table with the EKGs
        ### Parameters
        - Args:
        - Returns:
            - (`TinyDB.Table`): A table with all EKGs
        '''
        return TinyDB("data/person_db.json").table("ekg_tests")

    @staticmethod
    def delete_ekg_file(ekg_id: int):
        """Deletes the EKG file associated with a given ekg_id."""
        ekg_table = EKGdata.load_ekg_table()
        ekg_data = ekg_table.get(doc_id=ekg_id)
        file_path = ekg_data["result_link"]
        os.remove(file_path)


    def max_hr_warning(self, max_hr:int, timeframe:int=10) -> bool:
        '''
        A function to check if the max_hr is exceeded
        ### Parameters
        - Args:
            - max_hr (`int`): The maximum heart rate
            - timeframe (`int`): The timeframe in seconds
        - Returns:
            - bool: True if the max_hr is exceeded in the timeframe
        '''

        hr_timer = 0
        index_old = self.hr_pds.index[0]

        for index in self.hr_pds.index:
            if self.hr_pds[index] > max_hr:
                hr_timer += index-index_old
            else: 
                hr_timer = 0

            index_old = index

            if hr_timer > timeframe*1000:
                return True
            
        return False


if __name__ == "__main__":
    
    print("This is a module with some functions to read the EKG data")

    print('create EKGdata object')
    ekg = EKGdata(3)
    ekg.find_peaks(340, 4)
    ekg.estimate_hr()

    print('plot')
    fig_hr = go.Figure(data=go.Scatter(x=ekg.hr_pds.index, y=ekg.hr_pds))
    fig_hr.show()
    print(EKGdata.max_hr_warning(100, ekg.hr_pds))