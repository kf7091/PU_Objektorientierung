import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from tinydb import TinyDB

class EKGdata:

    def __init__(self, ekg_id:int):
        ekg_table = TinyDB("data/person_db.json").table("ekg_tests")
        self.id = ekg_table.get(doc_id=ekg_id).doc_id
        self.date = datetime.strptime(ekg_table.get(doc_id=ekg_id)["date"], "%d.%m.%Y")
        self.data_link = ekg_table.get(doc_id=ekg_id)["result_link"]
        self.df = pd.read_csv(self.data_link, sep='\t', header=None, names=['EKG in mV','Time in ms',])

    
    def find_peaks(self, threshold:float, respacing_factor:int=5):
        """
        A function to find the peaks in a series
        ### Parameters
        - Args:
            - threshold (`float`): The threshold for the peaks
            - respacing_factor (`int`): The factor to respace the series
        - Returns:
            - self.peaks (`list`): A list of the indices of the peaks
        """
        
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
    
    def estimate_hr(self):
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
            for i in range(1, len(self.peaks)):
                # Calculate the time delta between two peaks in ms (for better readability)
                time_delta_ms = self.df['Time in ms'].iloc[self.peaks[i]] - self.df['Time in ms'].iloc[self.peaks[i-1]]
                # Calculate the heart rate in bpm and append it to the list
                hr_list.append(60000/time_delta_ms)

            # Create a pandas series with the heart rate values
            self.hr_pds = pd.Series(hr_list, name="HR", index=self.peaks[1:])
            return self.hr_pds

        
    def plot_time_series(self):
        ''' Plot the EKG data with the peaks found
            ### Parameters
            - Args:
            - Returns:
                - self.time_series (`plotly.graph_objects.Figure`): A plotly figure with the EKG data
        '''
        # create a plotly figure with the raw EKG data and time in seconds
        self.time_series = go.Figure(data=go.Scatter(x=self.df["Time in ms"]/1000, y=self.df["EKG in mV"]))
        # create a scatter plot with the R-peaks and add it to the figure
        r_peaks = go.Scatter(x=self.df["Time in ms"].iloc[self.peaks]/1000, y=self.df["EKG in mV"].iloc[self.peaks], mode='markers', marker=dict(color='red', size=8))
        self.time_series.add_trace(r_peaks)
        return self.time_series
    
    def

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
    def get_ekgids_by_personid(ekg_table:TinyDB.table_class, person_id:int):
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
        for document in ekg_table:
            if document["person_id"] == person_id:
                ekg_ids.append(document.doc_id)
        return ekg_ids
    
    @staticmethod
    def load_ekg_table():
        """A Function that knows where the person Database is and returns a TinyDB-Table with the EKGs
        ### Parameters
        - Args:
        - Returns:
            - (`TinyDB.Table`): A table with all EKGs"""
        return TinyDB("data/person_db.json").table("ekg_tests")



if __name__ == "__main__":
    
    print("This is a module with some functions to read the EKG data")

    print('create EKGdata object')
    ekg = EKGdata(3)
    print(ekg.__dict__)
    '''print(ekg.df.head())
    print(type(ekg))


    print('find peaks')
    ekg.find_peaks(340, 4)
    print(ekg.peaks[:10])

    print('estimate hr')
    print(ekg.estimate_hr()[:10])

    print('plot')
    ekg.plot_time_series().show()'''

    #fig_hr = go.Figure(data=go.Scatter(x=ekg.hr_pds.index, y=ekg.hr_pds))
    #fig_hr.show()