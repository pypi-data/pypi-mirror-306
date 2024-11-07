from datetime import datetime, timedelta
from math import *
from typing import Union

from dateutil.relativedelta import relativedelta
from zoneinfo import ZoneInfo

tz = ZoneInfo("Europe/Paris")

import numpy as np
import pandas as pd

############ - Function ############################

def day_count(start, end, convention="ACT/360") -> float:
    """
    This fucntion computes the period in years between two given dates
            with a defined convention
    Args:
        start (datetime): start date
        end (datetime): end date
        convention (str, optional): day count convention. Defaults to "ACT/360".

    Returns:
        float: day count with the given  day count convention
    """

    if end == start:
        day_count = 0.0
    if convention == "ACT/360":
        # year_diff = np.floor((end - start).days/365)

        # start_diff = start + pd.DateOffset(years=year_diff)

        # day_count = (end - start_diff).days/360 + year_diff
        day_count = (end - start).days / 360
        return day_count

    elif convention == "ACT/ACT":
        # to set the dates at midnight 00:00:00
        start_date = dt.datetime.combine(start, dt.datetime.min.time())
        end_date = dt.datetime.combine(end, dt.datetime.min.time())
        # is is leap or not
        year_First = 366 if calendar.isleap(start.year) else 365
        year_Last = 366 if calendar.isleap(end.year) else 365
        # count the full years
        day_count = end_date.year - start_date.year - 1.0
        # count the first and last fractions of years
        diff_firstYear = (
            dt.datetime(1 + start_date.year, 1, 1, tzinfo=tz) - start_date
        )  # tzinfo=tz
        day_count += float(diff_firstYear.days) / year_First
        diff_lastYear = end_date - dt.datetime(
            end_date.year, 1, 1, tzinfo=tz
        )  # tzinfo=tz
        day_count += float(diff_lastYear.days) / year_Last
        return day_count

    elif convention == "30/360":
        # Ensure start_date is before end_date
        if start > end:
            start, end = end, start

        # Extract year, month, day from the dates
        start_year, start_month, start_day = start.year, start.month, start.day
        end_year, end_month, end_day = end.year, end.month, end.day

        # Adjust days for 30/360 calculation
        if start_day == 31 or (
            start_month == 2 and (start_day == 29 or start_day == 28)
        ):
            start_day = 30
        if end_day == 31 and start_day == 30:
            end_day = 30

        # Calculate the difference in days
        days = (
            (end_year - start_year) * 360
            + (end_month - start_month) * 30
            + (end_day - start_day)
        ) / 360
        return days
    else:
        return 0


def ZC_to_simplerate(zc, day_count) -> float:
    """
    Convert zero coupon rate to simple rate.

    Args:
        zc (float): Zero coupon rate (compound)
        day_count (float): Period of time in years

    Returns:
        float: Simple rate
    """
    # Return 0 if day_count is 0 or zc is None to avoid division by zero or None errors
    if day_count == 0 or zc is None:
        return 0

    # Calculate and return the simple rate
    return ((1 + zc) ** day_count - 1) / day_count



def previous_coupon_date(df, valuation_date):
    """
    get the pervios coupon date with a given valuation date

    Args:
        df (Dataframe): Payments  details
        valuation_date (datetime): valuation date

    Returns:
        datetime: previous coupon date
    """

    date = valuation_date

    for ind, row in df.iterrows():
        try:
            if valuation_date >= row["start_date"] and valuation_date < row["end_date"]:
                date = row["start_date"]
        except:
            if valuation_date >= row["start date"] and valuation_date < row["end date"]:
                date = row["start date"]


    return date


def str_to_datetime(strg) -> datetime:
    """
    transfer str to datetime

    Args:
        strg (str): string date

    Returns:
        datetime: date
    """
    date_format = "%Y-%m-%d"
    if type(strg) == (str):
        return datetime.strptime(strg, date_format)
    else:
        return strg

def ExitPortion(date, amount: float) -> float:
    """_summary_

    Args:
        date (datetime): early exit date
        amount (float): amount of early exit

    Returns:
        float: early exit amount
    """
    if date < "2022-06-30":
        return -0.8 * amount / 100
    elif date < "2023-06-30":
        return -0.6 * amount / 100
    elif date < "2024-06-30":
        return -0.4 * amount / 100
    elif date < "2025-06-25":
        return -0.2 * amount / 100
    else:
        return 0.0


def PayFrequency(period: str) -> float:
    """
    coupon payment frequency

    Args:
        period (str): period

    Returns:
        float: number of month in period (default = 3)

    """
    delta = 3
    if period == "Monthly":
        delta = 1
    elif period == "Quarterly":
        delta = 3
    elif period == "Semi-Annual":
        delta = 6
    elif period == "Annual":
        delta = 12
    return delta


def Accrued_coupon(
    curve,
    Cash_flows,
    notionel,
    valuation_date,
    ESTR_df=None,
    relative_delta=relativedelta(days=0),
) -> float:
    """This function computes the accrued coupon of the float leg
        and for the past we use ESTR compounded and for the future we compute forwards

    Args:
        curve (curve): yield curve
        ESTR (dataframe): Estr compounded
        Cash_flows (Dataframe): dataframe
        notionel (float): float
        valuation_date (datetime): valuation date

    Returns:
        float: accrued coupon
    """

    if ESTR_df is not None:
        # if ESTR file is provided
        # we don't have weekends so we need to use interplation
        ESTR_df = ESTR_df.rename(
            columns={"dates": "date", "DATES": "date", "estr": "ESTR"}
        )
        ESTR = linear_interpolation(ESTR_df)
        date_min = min(ESTR["date"])
        date_max = max(ESTR["date"])
        SDate = previous_coupon_date(Cash_flows, pd.Timestamp(valuation_date))
        SDate = SDate.strftime("%Y-%m-%d")

        ESTR_start = ESTR[ESTR["date"] == SDate]["ESTR"]
        ESTR_end = ESTR[ESTR["date"] == valuation_date]["ESTR"]
        ESTR_max = ESTR[ESTR["date"] == date_max]["ESTR"]
        if (
            curve.date.strftime("%Y-%m-%d") > SDate and date_max < SDate
            # Here my start Date is a Date in which no ESTR no FORWARD RATE (can't compute the forward)
        ):
            raise ValueError(
                "Forward can't be computed (ex :Use an ESTR compounded up to curve date)"
            )

        result = 0

        if SDate < date_min or SDate > date_max:
            FRate = curve.ForwardRates(
                previous_coupon_date(Cash_flows, pd.Timestamp(valuation_date)),
                pd.Timestamp(valuation_date),
                relative_delta,
            )

            Day_count_years = day_count(
                previous_coupon_date(Cash_flows, pd.Timestamp(valuation_date)),
                pd.Timestamp(valuation_date),
            )
            Perf = 0 if FRate is None else (1 + FRate) ** Day_count_years - 1
        elif valuation_date <= date_max:
            Perf = (float(ESTR_end) / float(ESTR_start)) - 1
        elif valuation_date > date_max:
            perf_0 = (float(ESTR_max) / float(ESTR_start)) - 1
            FRate0 = curve.ForwardRates(
                pd.Timestamp(date_max) + timedelta(days=1),
                pd.Timestamp(valuation_date),
                relative_delta,
            )

            Day_count_years = day_count(
                pd.Timestamp(date_max) + timedelta(days=1),
                pd.Timestamp(valuation_date),
            )
            Perf = ((1 + FRate0) ** (Day_count_years) - 1) + perf_0 / notionel
        else:
            FRate = curve.ForwardRates(
                previous_coupon_date(Cash_flows, pd.Timestamp(valuation_date)),
                pd.Timestamp(valuation_date),
                relative_delta,
            )

            Day_count_years = day_count(
                previous_coupon_date(Cash_flows, pd.Timestamp(valuation_date)),
                pd.Timestamp(valuation_date),
            )
            Perf = 0 if FRate is None else (1 + FRate) ** Day_count_years - 1
        result = notionel * Perf
        return result

    else:
        raise ValueError("Provide an ESTR compounded xls")


def Spread_amount(cashflow, notionel, spread, valuation_date, convention="ACT/360") -> float:
    """this function compute the spread amount for a giving valuation date and start date

    Args:
        cashflow (dataframe): coupon start and end dates
        notionel (float): notionel amount
        spread (float): swap spread
        valuation_date (datetime): valuation date

    Returns:
        float: the spread amount
    """
    period = day_count(
        previous_coupon_date(cashflow, pd.Timestamp(valuation_date)),
        pd.Timestamp(valuation_date),
        convention,
    )
    return notionel * (spread) * period


def DV01(actual: float, up: float, down: float) -> float:
    """

    Args:
        actual (float): unshifted value
        up (float): value with shifted curve (+1 bps)
        down (float): value with shifted curve (-1 bps)

    Returns:
        float: sensitivity of the swap price
    """
    return (abs(actual - up) + abs(actual - down)) / 2


def linear_interpolation(df, date_column="date", value_column="ESTR"):
    """this function return a dataframe filled with the missing dates and
    calculate the linear interpolation on the values column.

    Args:
        df (DataFrame): the original DFs
        date_column (str, optional): Date. Defaults to 'date'.
        value_column (str, optional): value. Defaults to 'ESTR'.

    Returns:
        _type_: _description_
    """

    if "Date" in df.columns:
        date_column = "Date"
    elif "dates" in df.columns:
        date_column = "dates"
    elif "date" in df.columns:
        date_column = "date"
    elif "DATES" in df.columns:
        date_column = "DATES"
    df = df.sort_values(by=[date_column])

    complete_dates = pd.date_range(
        start=df[date_column].min(), end=df[date_column].max(), freq="D"
    )

    # steps
    date_column_numerical = df[date_column].apply(lambda x: x.timestamp())
    complete_dates_numerical = [d.timestamp() for d in complete_dates]

    interpolated_values = np.interp(
        complete_dates_numerical, date_column_numerical, df[value_column]
    )
    dates = [dt.strftime("%Y-%m-%d") for dt in complete_dates]
    interpolated_df = pd.DataFrame(
        {date_column: dates, value_column: interpolated_values}
    )
    return interpolated_df


def tenor_to_period(tenor: str) -> Union[timedelta, relativedelta]:
    """
    Convert a given tenor to a period.

    Args:
        tenor (str): A string representing the tenor (e.g., '1D', '2W', '3M', '1Y').

    Returns:
        Union[timedelta, relativedelta]: The corresponding period as a timedelta or relativedelta object.

    Raises:
        ValueError: If the tenor unit is invalid.

    Example:
        >>> tenor_to_period('1D')
        datetime.timedelta(days=1)
        >>> tenor_to_period('2W')
        datetime.timedelta(days=14)
        >>> tenor_to_period('3M')
        relativedelta(months=+3)
    """
    # Extract numeric value and unit from the tenor
    tenor_value = int(tenor[:-1])
    tenor_unit = tenor[-1].lower()

    # Define a dictionary mapping tenor units to their corresponding period objects
    dict_tenor = {
        'd': timedelta(days=tenor_value),
        'w': timedelta(weeks=tenor_value),
        'm': relativedelta(months=tenor_value),
        'y': relativedelta(years=tenor_value)
    }

    # Return the corresponding period if the unit is valid, otherwise raise an error
    if tenor_unit in dict_tenor:
        return dict_tenor[tenor_unit]
    else:
        raise ValueError(f"Invalid tenor unit: {tenor_unit}. Valid units are 'd', 'w', 'm', 'y'.")


def period_to_tenor(period: int) -> str:
    """
    Convert a given period in days to its corresponding tenor.

    Args:
        period (int): Number of days.

    Returns:
        str: Corresponding tenor, or None if no match is found.

    Note:
        This function assumes 30 days per month and 360 days per year.
    """
    # Ensure period is an integer
    period = int(period)

    # Define tenor dictionary with optimized calculations
    tenor_dict = {
        1: "1D", 7: "1W", 14: "2W", 21: "3W",
        **{30 * i: f"{i}M" for i in range(1, 12)},  # 1M to 11M
        360: "1Y",
        360+90: "15M", 360+180: "18M", 360+270: "21M",
        **{360 * i: f"{i}Y" for i in range(2, 13)},  # 2Y to 12Y
        360 * 15: "15Y", 360 * 20: "20Y", 360 * 25: "25Y", 360 * 30: "30Y"
    }

    # Return the tenor if found, otherwise None
    return tenor_dict.get(period)
