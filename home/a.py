# CHARTS
import shrimpy
import plotly.graph_objects as go
from plotly.offline import plot


def plot_chart(sym):
    # get the candles
    candles = []

    # create lists to hold our different data elements
    dates = []
    close_data = []

    # convert from the Shrimpy candlesticks to the plotly graph objects format
    for candle in candles:
        dates.append(candle['Date'])
        
        close_data.append(candle['Close'])

    # construct the figure
    fig = go.Figure(data=[go.Candlestick(x=dates,
                         close=close_data)])
    fig.update_layout(height = 600,width = 1800)

    # display our graph
    # fig.show()
    # print(fig)
    plt_div = plot(fig, output_type='div')
    return plt_div
