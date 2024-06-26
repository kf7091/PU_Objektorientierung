import json
import pandas as pd
import plotly.graph_objects as go

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

    def __init__(self, person_id:int, ekg_id:int):
        
        db = json.load(open("data/person_db.json"))
        for p_id in db:
            if p_id['id'] == person_id:
                person = p_id
                break
        print(person)
        for ekg in person['ekg_tests']:
            if ekg['id'] == ekg_id:
                ekg_dict = ekg
                break
        print(ekg_dict)
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV','Time in ms',])

    
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
        ''' 
        Estimate the heart rate from the R-peaks found in the EKG data
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
                # Calculate the time delta between two peaks in ms (for better readability)
                time_delta_ms = self.df['Time in ms'].iloc[self.peaks[i]] - self.df['Time in ms'].iloc[self.peaks[i-1]]
                # Calculate the heart rate in bpm and append it to the list
                hr_list.append(60000/time_delta_ms)

            # Create a pandas series with the heart rate values
            self.hr_pds = pd.Series(hr_list, name="HR", index=self.peaks[1:])
            return self.hr_pds

        
    def plot_time_series(self):
        ''' Plot the EKG data with the peaks found
            Args:
            Returns:
                - self.time_series (plotly.graph_objects.Figure): A plotly figure with the EKG data
        '''
        # create a plotly figure with the raw EKG data and time in seconds
        self.time_series = go.Figure(data=go.Scatter(x=self.df["Time in ms"]/1000, y=self.df["EKG in mV"]))
        # create a scatter plot with the R-peaks and add it to the figure
        r_peaks = go.Scatter(x=self.df["Time in ms"].iloc[self.peaks]/1000, y=self.df["EKG in mV"].iloc[self.peaks], mode='markers', marker=dict(color='red', size=8))
        self.time_series.add_trace(r_peaks)
        return self.time_series

    @staticmethod
    def load_by_id(self, person_id:int, ekg_id:int):
        ekg_dict = json.load(open("data/person_db.json"))[person_id-1]["ekg_tests"][ekg_id-1]
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV','Time in ms',])

        return self




if __name__ == "__main__":
    
    print("This is a module with some functions to read the EKG data")

    print('create EKGdata object')
    ekg = EKGdata(2, 3)
    '''print(ekg.df.head())
    print(type(ekg))


    print('find peaks')
    ekg.find_peaks(340, 4)
    print(ekg.peaks[:10])

    print('estimate hr')
    print(ekg.estimate_hr()[:10])

    print('plot')
    ekg.plot_time_series().show()'''

    fig_hr = go.Figure(data=go.Scatter(x=ekg.hr_pds.index, y=ekg.hr_pds))
    fig_hr.show()