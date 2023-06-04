from typing import Any


def investment_calc(start_investment: int,
                    rate_of_return: float,
                    rate_of_inflation: float,
                    years_invested: int,
                    withdrawals: int) -> list[int | Any]:
    """
    This function will return the investment after the inputted
    number of years invested. This is useful for financial managers
    when doing financial planning.
    :param start_investment: Investment started with.
    :param rate_of_return: Rate of return on the investment account.
    :param rate_of_inflation: Rate of inflation, set at market level.
    :param years_invested: Years kept into investment account.
    :param withdrawals: The amount withdrawn each year.
    :return: Expected balance of account.
    """

    investment_history = [start_investment]

    for years in range(years_invested):
        next_year = (investment_history[years] + (investment_history[years] * rate_of_return)) - \
                    (investment_history[years] * rate_of_inflation) - withdrawals
        investment_history.append(round(next_year, 3))

    return investment_history
