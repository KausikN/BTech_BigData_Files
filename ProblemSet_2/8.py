'''
8. An organization wants to calculate the % of time they spent on each process for their product development. 
Visualize the data using funnel chart with the data given below.
Product Development steps           Time spent (in hours) 
Requirement Elicitation             50 
Requirement Analysis                110 
Software Development                250 
Debugging & Testing                 180
Others                              70 
'''
import plotly.express as px

def FunnelPlot(X, labels):
    data = dict(number=X, stage=labels)
    fig = px.funnel(data, x='number', y='stage')
    fig.show()

# Driver Code
ProdDevSteps = ['Requirement Elicitation', 'Requirement Analysis', 'Software Development', 'Debugging & Testing', 'Others']
Time = [50, 110, 250, 180, 70]

FunnelPlot(Time, ProdDevSteps)