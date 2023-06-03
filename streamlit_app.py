from collections import namedtuple
from components.interest import *
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


with st.echo(code_location='below'):
    start_investment = st.slider("Starting Investment:", 0, 1000000, 5000, step=100)
    rate_of_return = st.slider("Interest Rate:", 0, 100.0, 5.0, step=0.01)
    rate_of_inflation = st.slider("Current Inflation Rate:", 0, 100.0, 4.7, step=0.01)
    years_invested = st.slider("Years Invested:", 0, 80, 4)
    num_withdrawals = st.slider("Withdrawal Amount per Year:", 0, 1000000, 1000, step=100)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
