'''
7. An Advertisement agency develops new ads for various clients (like Jewellery shops, Textile shops). 
The Agency wants to assess their performance, for which they want to know the number of ads they developed in each quarter for different shop category.
Help them to visualize data using radar/spider charts.
Shop Category           Quarter 1     Quarter 2     Quarter 3   Quarter 4 
Textile                 10              6           8           13 
Jewellery               5               5           2           4 
Cleaning Essentials     15              20          16          15 
Cosmetics               14              10          21          11 
'''
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px

def RadarPlot(name, statsList, attribute_labels, plot_markers, plot_str_markers):

    labels = np.array(attribute_labels)
    fig= plt.figure()
    for stats in statsList:
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
        stats = np.concatenate((stats,[stats[0]]))
        angles = np.concatenate((angles,[angles[0]]))

        ax = fig.add_subplot(111, polar=True)
        ax.plot(angles, stats, 'o-', linewidth=2)
        ax.fill(angles, stats, alpha=0.25)
        ax.set_thetagrids(angles * 180/np.pi, labels)
        plt.yticks(markers)
        ax.set_title(name)
        ax.grid(True)
    plt.show()

def RadarPlot_PlotLY(statsList, labels):
    for stats in statsList:
        df = pd.DataFrame(dict(r=stats, theta=labels))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.show()

# Driver Code
labels=['Textile', 'Jewellery', 'Cleaning Essentials', 'Cosmetics']
markers = range(22)
str_markers = list(map(str, markers))
AdsCount = [[10, 5, 15, 14], 
            [6, 5, 20, 10], 
            [8, 2, 16, 21], 
            [13, 4, 15, 11]]

# RadarPlot_PlotLY(AdsCount, labels)
RadarPlot("Ads", AdsCount, attribute_labels = labels, plot_markers = markers, plot_str_markers = str_markers) # example