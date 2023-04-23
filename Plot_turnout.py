import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)
"""
# Reading data
f19_df = pd.read_excel(r'Fall 2019 Event Info (Data Project).xlsx')
f20_df = pd.read_excel(r'Fall 2020 Event Info (Data Project).xlsx')
s21_df = pd.read_excel(r'Spring 2021 Event Info (Data Project).xlsx')
f21_df = pd.read_excel(r'Fall 2021 Event Info (Data Project).xlsx')
s22_df = pd.read_excel(r'Spring 2022 Event Info (Data Project).xlsx')
f22_df = pd.read_excel(r'Fall 2022 Event Info (Data Project).xlsx')

# Selecting only attended and registered columns
f19_att_reg = f19_df[['Attended', 'Registered']]
f20_att_reg = f20_df[['Attended', 'Registered']]
s21_att_reg = s21_df[['Attended', 'Registered']]
f21_att_reg = f21_df[['Attended', 'Registered']]
s22_att_reg = s22_df[['Attended', 'Registered']]
f22_att_reg = f22_df[['Attended', 'Registered']]

# Get count of attended and registered values for each event
f19_counts = f19_att_reg.apply(pd.Series.value_counts)
f20_counts = f20_att_reg.apply(pd.Series.value_counts)
s21_counts = s21_att_reg.apply(pd.Series.value_counts)
f21_counts = f21_att_reg.apply(pd.Series.value_counts)
s22_counts = s22_att_reg.apply(pd.Series.value_counts)
f22_counts = f22_att_reg.apply(pd.Series.value_counts)

# Extract attended and registered counts as separate lists
f19_att = f19_counts.loc[1].tolist()
f19_reg = f19_counts.loc[0].tolist()

f20_att = f20_counts.loc[1].tolist()
f20_reg = f20_counts.loc[0].tolist()

s21_att = s21_counts.loc[1].tolist()
s21_reg = s21_counts.loc[0].tolist()

f21_att = f21_counts.loc[1].tolist()
f21_reg = f21_counts.loc[0].tolist()

s22_att = s22_counts.loc[1].tolist()
s22_reg = s22_counts.loc[0].tolist()

f22_att = f22_counts.loc[1].tolist()
f22_reg = f22_counts.loc[0].tolist()

# Grouped Bar Chart

# Set width of bars
barWidth = 0.25

# Set heights of bars
attended = [f19_att[0], f20_att[0], s21_att[0], f21_att[0], s22_att[0], f22_att[0]]
registered = [f19_reg[0], f20_reg[0], s21_reg[0], f21_reg[0], s22_reg[0], f22_reg[0]]
"""


import plot_revised




def plot(att_freq_dict_old, reg_freq_dict_old, x_axis, x_lab, title1, title2):

    att_freq_dict = {}
    reg_freq_dict = {}
    
    all_x_vals = []
    for x in att_freq_dict_old:
        all_x_vals.append(x)
    for x in reg_freq_dict_old:
        if not x in att_freq_dict_old:
            all_x_vals.append(x)
    
    for x in all_x_vals:
        if x in att_freq_dict_old:
            att_freq_dict[x] = att_freq_dict_old[x]
        else:
            att_freq_dict[x] = 0
        if x in reg_freq_dict_old:
            reg_freq_dict[x] = reg_freq_dict_old[x]
        else:
            reg_freq_dict[x] = 0
    
    print(len(all_x_vals))
    print(len(att_freq_dict))
    
    indices = np.arange(len(all_x_vals))
    
    # Make plot
    fig, axs = plt.subplots(nrows = 2, ncols = 1, figsize = (20,20))
    barWidth = .25
    
    # Bar chart
    axs[0].bar(indices, att_freq_dict.values(), width=barWidth, color='green', label='Attended')
    axs[0].bar(indices + barWidth, reg_freq_dict.values(), width=barWidth, color='red', label='Registered')
    
    # Add xticks, labels, and legend
    axs[0].set_xlabel(x_lab)
    axs[0].set_ylabel('Number of Students')
    axs[0].set_title(title1)
    axs[0].set_xticks(indices, list(att_freq_dict.keys()), rotation=45)
    
    
    for i in range(len(att_freq_dict)):  
        
        a = list(att_freq_dict.values())[i]
        r = list(reg_freq_dict.values())[i]
        #v = a + r
        axs[0].text(i - 0.12, a + 4, str(a), color='black', fontweight='bold')
        #v = a + r
        axs[0].text(i + 0.16, r + 3, str(r), color='black', fontweight='bold')
    #plt.xticks(x1 + barWidth/2, ['Fall 2019', 'Fall 2020', 'Spring 2021', 'Fall 2021', 'Spring 2022', 'Fall 2022'])
    axs[0].legend()
    
    
    # Calculate maximum y-axis value
    labels = axs[0].get_yticks()
    interval = labels[1] - labels[0]
    max_freq = max(max(att_freq_dict.values()), max(reg_freq_dict.values()))
    axs[0].set_ylim([0, max_freq + interval])
    
    # Create a list of turnout percentages for each event
    turnout_pct = {}
    for key in att_freq_dict:
        if reg_freq_dict[key] != 0:
            turnout = att_freq_dict[key] / reg_freq_dict[key] * 100
        else:
            turnout = att_freq_dict[key] / 1 * 100
        turnout_pct[key] = turnout
    
    
    # Make line plot of turnout percentages
    axs[1].plot(turnout_pct.keys(), turnout_pct.values() ,marker='o')
    axs[1].set_xlabel(x_lab)
    axs[1].set_ylabel('Turnout Percentage')
    axs[1].set_title(title2)
    #plt.xticks(rotation=45)
    
    
    plt.tight_layout()
    st.pyplot(fig)
    #plt.show()


"""
study = pd.read_excel(r'Fall 2019 Event Info (Data Project).xlsx', sheet_name= "(12.11.19) Study pectacular")
study_attended = study[["Registered", "Major", "Classification"]].dropna()
study_registered = study[["Attended", "Major.1", "Classification.1"]].dropna()
study_registered = study_registered.rename(columns={"Attended": "Attended", "Major.1": "Major", "Classification.1": "Classification"})

print(study_registered.columns)
x_axis = "Major"
x_lab = "Events"
title1 = "Attendance and Registration by Event"
title2 = "Turnout Percentage by Event"
att_freq_dict_old = plot_revised.get_frequency(study_attended, x_axis)
reg_freq_dict_old = plot_revised.get_frequency(study_registered, x_axis)


plot(att_freq_dict_old, reg_freq_dict_old, x_axis, x_lab, title1, title2)
"""


"""


# Set position of bar on x-axis
x1 = np.arange(6)
x2 = [x + barWidth for x in x1]

# Make plot
fig, ax = plt.subplots()
ax.bar(x1, attended, width=barWidth, color='green', label='Attended')
ax.bar(x2, registered, width=barWidth, color='red', label='Registered')


# Add xticks, labels, and legend
ax.set_xlabel('Events')
ax.set_xticks(x1, ['Fall 2019', 'Fall 2020', 'Spring 2021', 'Fall 2021', 'Spring 2022', 'Fall 2022'])
ax.set_ylabel('Number of Attendees')
ax.set_title('Attendance and Registration by Event')

for i, a in enumerate(attended):  
    #v = a + r
    ax.text(i - 0.15, a + 4, str(a), color='black', fontweight='bold')
for i, r in enumerate(registered):
    #v = a + r
    ax.text(i + 0.13, r + 3, str(r), color='black', fontweight='bold')
plt.xticks(x1 + barWidth/2, ['Fall 2019', 'Fall 2020', 'Spring 2021', 'Fall 2021', 'Spring 2022', 'Fall 2022'])
ax.legend()

labels = ax.get_yticks()
#print(locs)
print(labels)

interval = labels[1] - labels[0]
ax.set_ylim([0, maxfreq + interval])



plt.show()

"""
