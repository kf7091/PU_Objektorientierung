import json
import pandas as pd
import plotly.graph_objects as go

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
            - peaks (list): A list of the indices of the peaks
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

            if last < current and current > next and current > threshold:
                self.peaks.append(index-respacing_factor)

        return self.peaks
    
    def estimate_hr(self):
        ''' Estimate the heart rate from the peaks found in the EKG data'''
        if not hasattr(self, 'peaks'):
            raise ValueError("No peaks found - please run find_peaks() first")
        else:
            print(self.peaks[:1])
            hr = pd.Series("HR", name="HR", index=self.peaks)
            for i in range(1, len(self.peaks)):
                hr.at[i, 'HR'] = 1/((self.peaks[i] - self.peaks[i-1])/60000)
        return hr

        
    def plot_time_series():
        pass


if __name__ == "__main__":
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
    ekg.find_peaks(250)
    print(ekg.peaks[:10])

    print('estimate hr')
    print(ekg.estimate_hr()[:10])

    fig = go.Figure(data=go.Scatter(x=ekg.df["Time in ms"], y=ekg.df["EKG in mV"]))
    #add_trace = go.Scatter(x=ekg.df["Time in ms"].iloc[ekg.peaks], y=ekg.df["EKG in mV"].iloc[ekg.peaks], mode='markers', marker=dict(color='red', size=8))
    #fig.add_trace(add_trace)
    fig.show()