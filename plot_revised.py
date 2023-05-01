import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

# Function to find the partition position
def partition(frequencies, keys, low, high):
 
    # choose the rightmost element as pivot
    pivot = frequencies[high]
 
    # pointer for greater element
    i = low - 1
 
    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if frequencies[j] <= pivot:
 
            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1
 
            # Swapping element at i with element at j
            (frequencies[i], frequencies[j]) = (frequencies[j], frequencies[i])
            (keys[i], keys[j]) = (keys[j], keys[i])
 
    # Swap the pivot element with the greater element specified by i
    (frequencies[i + 1], frequencies[high]) = (frequencies[high], frequencies[i + 1])
    (keys[i + 1], keys[high]) = (keys[high], keys[i + 1])
 
    # Return the position from where partition is done
    return i + 1


# Function to perform quicksort
def quickSort(frequencies, keys, low, high):
    if low < high:
 
        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = partition(frequencies, keys, low, high)
 
        # Recursive call on the left of pivot
        quickSort(frequencies, keys, low, pi - 1)
 
        # Recursive call on the right of pivot
        quickSort(frequencies, keys, pi + 1, high)

## using temporary data

# Fall 2019
#study = pd.read_excel(r'Fall 2019 Event Info (Data Project).xlsx', sheet_name = '(12.11.19) Study pectacular')
#study_attended = study[["Attended", "Major", "Classification"]].dropna()


def get_frequency(data, x = 'event'):
    colname = ''
    if (x.lower() == 'major'):
        colname = 'major'
    elif (x.lower() == 'class'):
        colname = 'classification_category'
    elif (x.lower() == 'semester'):
        colname = 'semester'
    elif (x.lower() == 'event'):
        colname = 'undated_event'

    data_cols = data[colname].tolist()
    data_cols_unique = list(set(data_cols))
    freq = {key: 0 for key in data_cols_unique}
    for col in freq:
        filtered = data.loc[data[colname] == col]
        #cols_freq = filtered['Attended'].sum()
        cols_freq = len(filtered)
        freq[col] += cols_freq
    
    return freq


def plot(freq_dict, title, x_lab, asc = False):
    # set width of bars
    barWidth = 0.25

    # set y-values
    y = list(freq_dict.values())

    # set x-values
    x = list(freq_dict.keys())

    quickSort(y, x, 0, len(x) - 1)
    if not asc:
        y.reverse()
        x.reverse()

    # Create axis
    fig, axs = plt.subplots(nrows = 2, ncols = 1, figsize = (20,20))
    
    # Bar chart
    # make plot
    axs[0].bar(x, y, width = barWidth, color = 'blue') 

    # add title, xticks, and labels
    axs[0].set_title(title)
    axs[0].set_xlabel(x_lab) 
    axs[0].set_ylabel('Attendence')
    axs[0].set_xticks(x, x, rotation=45, ha='right')

    # Pie chart
    pie_dict = {}
    for key in freq_dict:
        if freq_dict[key] != 0:
            pie_dict[key] = freq_dict[key]
    axs[1].pie(pie_dict.values(), labels = pie_dict.keys())


    plt.tight_layout()
    st.pyplot(fig)


# major_freq = get_frequency(study_attended, 'Major')
# major_plot = plot(major_freq, 'Attendence by Major', 'Majors')
# class_freq = get_frequency(study_attended, 'Class')
# class_plot = plot(class_freq, 'Attendence by Class', 'Classes')

