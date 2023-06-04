from collections import namedtuple
from components.interest import investment_calc
import altair as alt
import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np
import streamlit as st

plt.style.use('ggplot')

plt.rcParams.update({
    "figure.facecolor": (22 / 255, 22 / 255, 22 / 255, 0.85),
    "figure.figsize": (12, 7),
    "figure.dpi": 200,
    "axes.facecolor": (22 / 255, 22 / 255, 22 / 255, 0.2),
    "xtick.color": 'lightgrey',
    "ytick.color": 'lightgrey',
    "grid.alpha": 0.1,
    "grid.color": 'salmon',
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
    "axes.labelcolor": 'lightgrey',
    "axes.labelsize": 15,
    "text.color": 'white',
    "font.family": 'monospace',
    "font.size": 15,
    "font.weight": 600,
    "axes.titlecolor": "lightgrey",
    "legend.fontsize": 13
})

"""
# Investment Calculator.

Play around with the investment parameters and run a break-even analysis. Given an interest rate offered by your financial institution, this calculator is able to answer a few questions, including, but not limited to: 

- How much are you able to withdraw each year based on a starting investment?
- What interest rate should you strive to aim for in a financial institution to keep up with the pace of inflation.
- How long until you're able to reach your investment goals?


"""

"""
### The formula for calculating current balance is as follows:
"""

st.latex(r'''
B_i = B_{i-1} + (B_{i-1} * (1 + i_r)) - (B_{i-1} * (1 + i_f)) - W_{i-1}
''')

"""
Where,
"""
st.latex(r'''
B_i = \text{Balance at Year }i
\\
i_r = \text{Interest Rate of Institution }
\\
i_f = \text{Market Rate of Inflation}
\\
W_i = \text{Withdrawal Amount at Year }i
''')

start_investment = st.slider("Starting Investment:", 0, 500000, 5000, step=500)
rate_of_return = st.slider("Interest Rate:", 0.0, 100.0, 5.0, step=0.01)
rate_of_inflation = st.slider("Current Inflation Rate:", 0.0, 100.0, 4.7, step=0.01)
years_invested = st.slider("Years Invested:", 1, 80, 7)
amt_withdrawals = st.slider("Withdrawal Amount per Year:", 0, 10000, 1000, step=250)

Investment = namedtuple('InvestmentOvertime', 'time, amount')
time = [i for i in range(years_invested + 1)]
balance = investment_calc(start_investment,
                          1 + (rate_of_return / 100),
                          1 + (rate_of_inflation / 100),
                          years_invested,
                          amt_withdrawals)
net_difference = [0]
interest_earned = [0]
inflation_hit = [0]

for i in range(len(balance) - 1):
    net_difference.append(np.round(balance[i + 1] - balance[i], 2))
    interest_earned.append(np.round(balance[i + 1] * (rate_of_return / 100), 2))
    inflation_hit.append(np.round(balance[i + 1] * (rate_of_inflation / 100), 2))

    if interest_earned[i + 1] < 0:
        interest_earned[i + 1] = 0
    if inflation_hit[i + 1] < 0:
        inflation_hit[i + 1] = 0


df = pd.DataFrame(
    {
        'Years': time,
        'Current Balance': [np.round(bal, 2) for bal in balance],
        'Net Difference': net_difference,
        'Interest Earned': interest_earned,
        'Inflation Loss': inflation_hit
    }
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Lifetime Interest Earned",
            value=f'${np.round(sum(df["Interest Earned"]), 2)}')
col2.metric("Lifetime Inflation Loss",
            value=f'${np.round(sum(df["Inflation Loss"]), 2)}')
col3.metric("Ending Balance",
            value=f'${np.round(df["Current Balance"][years_invested], 2)}')
col4.metric("Avg Bal Change / Year",
            value=f'${np.round(np.mean(df["Net Difference"]), 2)}')

"""
# Data Table Visualization.
"""
st.data_editor(
    df,
    column_config={
        "Current Balance": st.column_config.NumberColumn(
            "Current Balance",
            format="$%.2f",
        ),
        "Net Difference": st.column_config.NumberColumn(
            "Net Difference",
            format="$%.2f",
        ),
        "Interest Earned": st.column_config.NumberColumn(
            "Interest Earned",
            format="$%.2f",
        ),
        "Inflation Loss": st.column_config.NumberColumn(
            "Inflation Loss",
            format="$%.2f",
        ),
    },
    hide_index=True,
    use_container_width=True,
    disabled=True,
)

fig, axs = plt.subplots()
axs.scatter(df['Years'], df['Current Balance'], label='Current Balance')
axs.plot(df['Years'], df['Current Balance'], label='Current Balance')
axs.set_xlabel('Years')
axs.set_ylabel('Account Balance')
axs.set_title('Current Balance Overtime')
axs.legend()

fig2, axs2 = plt.subplots()
axs2.scatter(df['Years'][1:], df['Net Difference'][1:], label='Net Difference')
axs2.plot(df['Years'][1:], df['Net Difference'][1:], label='Net Difference')
axs2.scatter(df['Years'][1:], df['Interest Earned'][1:], label='Interest Earned')
axs2.plot(df['Years'][1:], df['Interest Earned'][1:], label='Interest Earned')
axs2.scatter(df['Years'][1:], df['Inflation Loss'][1:], label='Inflation Loss')
axs2.plot(df['Years'][1:], df['Inflation Loss'][1:], label='Inflation Loss')
axs2.set_xlabel('Years')
axs2.set_ylabel('Account Balance')
axs2.set_title('Account Metrics Overtime')
axs2.legend()

"""
# Graphical Visualization.
"""
st.pyplot(fig)
st.pyplot(fig2)
