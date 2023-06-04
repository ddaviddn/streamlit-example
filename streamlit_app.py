from collections import namedtuple
from components.interest import investment_calc
import altair as alt
import math
import pandas as pd
import numpy as np
import streamlit as st

"""
# Investment Calculator.

Play around with the investment parameters and run a break-even analysis. Given an interest rate offered by your financial institution, this calculator is able to answer a few questions, including, but not limited to: 

- How much are you able to withdraw each year based on a starting investment?
- What interest rate should you strive to aim for in a financial institution to keep up with the pace of inflation.
- How long until you're able to reach your investment goals?


"""

with st.echo(code_location='below'):
    start_investment = st.slider("Starting Investment:", 0, 500000, 5000, step=500)
    rate_of_return = st.slider("Interest Rate:", 0.0, 100.0, 5.0, step=0.01)
    rate_of_inflation = st.slider("Current Inflation Rate:", 0.0, 100.0, 4.7, step=0.01)
    years_invested = st.slider("Years Invested:", 0, 80, 4)
    amt_withdrawals = st.slider("Withdrawal Amount per Year:", 0, 10000, 1000, step=250)

    Investment = namedtuple('InvestmentOvertime', 'time, amount')
    time = [i for i in range(years_invested + 1)]
    balance = investment_calc(start_investment,
                              1 + (rate_of_return / 100),
                              1 + (rate_of_inflation / 100),
                              years_invested,
                              amt_withdrawals)
    interest_earned = [0]
    inflation_hit = [0]

    for i in range(len(balance) - 1):
        interest_earned.append(np.round(balance[i+1] * (rate_of_return / 100), 2))
        inflation_hit.append(np.round(balance[i+1] * (rate_of_inflation / 100), 2))

    df = pd.DataFrame(
        {
            'Years': time,
            'Current Balance': [np.round(bal, 2) for bal in balance],
            'Interest Earned': interest_earned,
            'Inflation Loss': inflation_hit
        }
    )

    st.dataframe(df, use_container_width=True)

    # st.altair_chart(alt.Chart(pd.DataFrame([time, data]), height=500, width=500)
    #     .mark_circle(color='#0068c9', opacity=0.5)
    #     .encode(x='x:Q', y='y:Q'))
