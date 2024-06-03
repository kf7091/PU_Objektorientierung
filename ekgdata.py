import json
import pandas as pd

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV','Time in ms',])

    def load_by_id(self, id):
        return {'id': id, 'date': self.date, 'result_link': self.data}

    def find_peaks(self, threshold:float, respacing_factor:int=5):
        """
        A function to find the peaks in a series
        Args:
            - threshold (float): The threshold for the peaks
            - respacing_factor (int): The factor to respace the series
        Returns:
            - self.peaks (list): A list of the indices of the peaks
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
        ''' Estimate the heart rate from the peaks found in the EKG data
            Args:
            Returns:
                - self.hr_pds (pd.Series): A pandas series with the heart rate values
        '''
        # Check if self.peaks exists
        if not hasattr(self, 'peaks'):
            raise ValueError("No peaks found - please run find_peaks() first")
        
        else:
            hr_list = []
            for i in range(1, len(self.peaks)):
                time_delta_ms = self.df['Time in ms'].iloc[self.peaks[i]] - self.df['Time in ms'].iloc[self.peaks[i-1]]
                hr_list.append(60000/time_delta_ms)

            self.hr_pds = pd.Series(hr_list, name="HR", index=self.peaks[1:])
            return self.hr_pds

        
    def plot_time_series(self):
        self.time_series = go.Figure(data=go.Scatter(x=self.df["Time in ms"], y=self.df["EKG in mV"]))
        r_peaks = go.Scatter(x=self.df["Time in ms"].iloc[self.peaks], y=self.df["EKG in mV"].iloc[self.peaks], mode='markers', marker=dict(color='red', size=8))
        self.time_series.add_trace(r_peaks)
        return self.time_series






if __name__ == "__main__":
    import plotly.graph_objects as go
    print("This is a module with some functions to read the EKG data")

    print('Loading Data')
    file = open("data/person_db.json")
    person_data = json.load(file)

    print('convert to dict')
    ekg_dict = person_data[0]["ekg_tests"][0]
    print(ekg_dict)

    print('create EKGdata object')
    ekg = EKGdata(ekg_dict)
    print(ekg.df.head())
    print(type(ekg))
    print(type(ekg_dict))

    print('find peaks')
    ekg.find_peaks(340, 4)
    print(ekg.peaks[:10])

    print('estimate hr')
    print(ekg.estimate_hr()[:10])

    print('plot')
    ekg.plot_time_series().show()

    #fig_hr = go.Figure(data=go.Scatter(x=ekg.hr_pds.index, y=ekg.hr_pds))
    #fig_hr.show()