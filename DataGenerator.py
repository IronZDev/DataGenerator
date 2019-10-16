import random
import PySimpleGUI as sg
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Calculating gaussian distribution
def calculate_gaussian(size=1000, number_of_clusters=3, mean_min=-10.0, mean_max=10.0, std_deviation_min=0.5,
                       std_deviation_max=2.0):
    # Generate random clasters in 2d
    colors_available = ['r', 'g']
    data = [[], [], []]
    for cluster in range(number_of_clusters):
        center = [random.uniform(mean_min, mean_max), random.uniform(mean_min, mean_max)]
        x, y = np.random.multivariate_normal(center,
                                             [[random.uniform(std_deviation_min, std_deviation_max), 0],
                                              [0, random.uniform(std_deviation_min, std_deviation_max)]],
                                             size).T
        data[0].append(x)
        data[1].append(y)
        # Assign a color to each cluster
        data[2].extend([colors_available[cluster % 2] for i in range(size)])
    return data


# Generating plot
def generate_plot(x):
    plt.scatter(x[0], x[1], c=x[2])
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    return plt.gcf()


# Helper functions
# Draw plot on canvas
def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# Validate data
def is_valid():
    for i, val in enumerate(values):
        if type(values[val]) is str or type(values[val]) is int:
            # Check if values are not empty
            if len(str(values[val])) == 0:
                window[val].Update('')
                sg.popup_error('Invalid values!', 'Value of '+column1[i-1][0].DisplayText+' is invalid')
                return False
            # Check if values are numbers
            if not is_number(values[val]):
                window[val].Update('')
                sg.popup_error('Invalid values!', 'Value of '+column1[i-1][0].DisplayText+' is invalid')
                return False
            # Check deviations
            if 'Deviation' in val and float(values[val]) < 0:
                window[val].Update('')
                sg.popup_error('Invalid values!', 'Value of '+column1[i-1][0].DisplayText+' can\'t be lower than 0')
                return False
    if float(values['minDeviation']) > float(values['maxDeviation']):
        sg.popup_error('Invalid values!', 'Min std deviation can\'t be greater than max std deviation')
        return False
    # Check number of clusters
    if int(values['clustersNum']) <= 0 or int(values['clustersNum']) > 7:
        sg.popup_error('Invalid values!', 'Clusters number can\'t be lower than 1 and greater than 7')
        return False
    # Check size
    if int(values['clustersNum']) > int(values['size']):
        sg.popup_error('Invalid values!', 'Size can\'t be lower than number of clusters')
        return False
    return True


# GUI
column1 = [
    [sg.Text('Min mean value')],
    [sg.Text('Max mean value')],
    [sg.Text('Min std deviation')],
    [sg.Text('Max std deviation')],
    [sg.Text('Number of values to generate per cluster')],
    [sg.Text('Number of clusters')],
    [sg.Button('Draw', size=(15, 1))]
]

column2 = [
    [sg.In(default_text='-10.0', key='minVal', size=(4, 1))],
    [sg.In(default_text='10.0', key='maxVal', size=(4, 1))],
    [sg.In(default_text='0.5', key='minDeviation', size=(4, 1))],
    [sg.In(default_text='2.0', key='maxDeviation', size=(4, 1))],
    [sg.Spin([i for i in range(100, 100000, 100)], initial_value=100, key='size', size=(5, 1))],
    [sg.Spin([i for i in range(1, 8)], initial_value=2, key='clustersNum', size=(1, 1))],
    [sg.Exit(size=(8, 1))]
]

layout = [
    [sg.Canvas(size=(1, 1), key='canvas')],
    [sg.Column(column1), sg.Column(column2)]
]

# Create the Window
window = sg.Window('Data generator', layout).Finalize()

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Exit'):  # if user closes window or clicks cancel
        print('Close')
        plt.close('all')
        break
    if event == 'Draw':
        if is_valid():
            points = calculate_gaussian(int(values['size']), int(values['clustersNum']), float(values['minVal']),
                                      float(values['maxVal']), float(values['minDeviation']),
                                      float(values['maxDeviation']))
            if 'fig_canvas_agg' in globals():  # Update if plot already exists
                plt.clf()
                plt.scatter(points[0], points[1], c=points[2])
                fig_canvas_agg.draw()
            else:  # Generate new plot
                fig = generate_plot(points)
                fig_canvas_agg = draw_figure(window['canvas'].TKCanvas, fig)

window.close()
