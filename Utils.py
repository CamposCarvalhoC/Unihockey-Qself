import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sn
import csv

class Utils:

    LABELS = ['idk','Shoot','Pass']

    @staticmethod
    def read_data_csv(filename):
        data = pd.read_csv(f"data/{filename}",sep=";")
        data.index = data["Phone timestamp"]
        data =data.drop(columns=["Phone timestamp","sensor timestamp [ns]"])
        data.index = pd.to_datetime(data.index)
        return data

    @staticmethod
    def read_markers(filename):
        df_markers = pd.read_csv(f'data/{filename}', sep=';', header=0, names=['timestamp', 'mark'], index_col=0, parse_dates=True)
        markers = []
        for i in range(0,len(df_markers)-1,2):
            markers.append((df_markers.index[i],df_markers.index[i+1]))
        return markers

    @staticmethod
    def plot_with_markers(data,markers):
        fig, ax = plt.subplots(figsize=(20,7))
        for col in data.columns:
            ax.plot(data[col],label=col)
        for i,(start,end) in enumerate(markers):
            ax.axvspan(start,end,color='r',alpha=0.2,label="Marker" if i == 0 else "")
        
        ax.legend()
        plt.show()

    @staticmethod
    def add_column_classification(data,markers):
        y = np.zeros(len(data))
        for (start,end,label) in markers:
            y[np.argwhere((data.index > start) & (data.index < end))] = label
        return y

    @staticmethod
    def concatenate_data(data_tir,data_passe,markers_tir,markers_passe):
        first_pass_timestamp = data_passe.index[0]
        last_shoot_timestamp = data_tir.index[-1]

        data_passe.index -= first_pass_timestamp
        data_passe.index += last_shoot_timestamp
        data = pd.concat((data_tir,data_passe))
        markers = []
        
        for (start,end) in markers_tir:
            markers.append((start,end,1))

        for (start,end) in markers_passe:
            start -= first_pass_timestamp
            start += last_shoot_timestamp
            end -= first_pass_timestamp
            end += last_shoot_timestamp
            markers.append((start,end,2))

        return data, markers
    
    @staticmethod
    def concatenate_data_bis(data1,data2,markers1,markers2):
        first_timestamp = data2.index[0]
        last_timestamp = data1.index[-1]

        data2.index -= first_timestamp
        data2.index += last_timestamp
        data = pd.concat((data1,data2))

        markers = markers1.copy()

        for (start,end,label) in markers2:
            start -= first_timestamp
            start += last_timestamp
            end -= first_timestamp
            end += last_timestamp
            markers.append((start,end,label))

        return data, markers

    @staticmethod
    def plot_with_markers_label(data,markers):
        fig, ax = plt.subplots(figsize=(20,7))
        for col in data.columns:
            ax.plot(data[col],label=col)
        for i,(start,end,label) in enumerate(markers):
            ax.axvspan(start,end,color='r'if label==1 else 'g',alpha=0.2)
        
        ax.legend()
        plt.show()

    @staticmethod
    def get_label(y):
        uniques,counts = np.unique(y,return_counts=True)
        return uniques[np.argmax(counts)]
    

    @staticmethod
    def plot_confusion_matrix(y_true,y_pred,title='Confusion Matrix'):
        fig, ax = plt.subplots()
        ax.set_title(title)
        ax.set_ylabel('True label')
        ax.set_xlabel('Pred label')
        cm = confusion_matrix(y_true, y_pred)
        sn.heatmap(cm,ax=ax, annot=True,xticklabels=Utils.LABELS,yticklabels=Utils.LABELS)

    @staticmethod
    def create_results_csv(y,name_file):
        unique, counts = np.unique(y, return_counts=True)
        res = {Utils.LABELS[u]:c for u,c in zip(unique,counts) if u!=0}

        with open(name_file,'w',newline='') as f:
            writer = csv.writer(f)
            for k,v in res.items():
                writer.writerow([k,v])

        return res

    @staticmethod
    def create_csv_with_timeseries(y,timeseries,name_file):
        unique, counts = np.unique(y, return_counts=True)
        res = {Utils.LABELS[u]:c for u,c in zip(unique,counts) if u!=0}

        timeseries['Type'] = np.nan
        timeseries['Amount'] = np.nan

        timeseries.loc[:2,'Type']= list(res.keys())
        timeseries.loc[:2,'Amount']= list(res.values())  

        timeseries.to_csv(name_file)
        return res