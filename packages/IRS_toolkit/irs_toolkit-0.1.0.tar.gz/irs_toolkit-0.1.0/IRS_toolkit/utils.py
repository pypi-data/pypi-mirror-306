import calendar
import datetime as dt
from datetime import datetime, timedelta
from math import *
from pathlib import Path
from typing import Union

from dateutil.relativedelta import relativedelta
from zoneinfo import ZoneInfo

tz = ZoneInfo("Europe/Paris")

import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import xlrd


############ - Function ############################
def dataframe_from_sheet(sheet: pd.DataFrame, keyword: str) -> pd.DataFrame:
    """
    Extract and clean a DataFrame from a sheet based on a keyword.

    Args:
        sheet (pd.DataFrame): The input sheet as a DataFrame.
        keyword (str): The keyword to locate in the sheet.

    Returns:
        pd.DataFrame: The cleaned and extracted DataFrame.
    """

    def locate_in_df(df: pd.DataFrame, value: str) -> tuple[int, int]:
        """
        Locate the position of a value in a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to search.
            value (str): The value to find.

        Returns:
            tuple[int, int]: The row and column indices of the value.
        """
        np_object = df.to_numpy()
        check_value = np.where(np_object == value)
        rows, cols = check_value[0], check_value[1]
        row = rows[0] if rows.size > 0 else -1
        col = cols[0] if cols.size > 0 else -1
        return row, col

    # Find the position of the keyword
    row_code_valeur, col_code_valeur = locate_in_df(sheet, keyword)

    # Remove rows above the keyword
    sheet = sheet.iloc[row_code_valeur:]

    # Set the first row as column names
    sheet.columns = sheet.iloc[0]

    # Remove columns to the left of the keyword
    sheet = sheet.iloc[:, col_code_valeur:]

    # Remove the first row (now redundant column names)
    sheet = sheet.iloc[1:]

    # Reset the index
    sheet = sheet.reset_index(drop=True)

    return sheet


def get_as_of_date_from_sheet(dict_sheet: dict) -> datetime:
    """
    Extract the 'as of' date from a sheet dictionary.

    Args:
        dict_sheet (dict): A dictionary containing sheet data.

    Returns:
        datetime: The extracted 'as of' date. If not found, returns the current date.
    """
    # Default to current date if 'as of' date is not found
    as_of_date_object = datetime.now()

    if "Détails" in dict_sheet:
        sheet = dict_sheet["Détails"]

        # Extract non-null values from the 'Unnamed: 1' column
        sheet = sheet["Unnamed: 1"].dropna()

        # Find the row containing 'au ' (which likely precedes the date)
        date_rows = sheet[sheet.str.contains("au ", case=False, na=False)]

        if not date_rows.empty:
            # Extract the date string (assumes format: "... au DD/MM/YYYY")
            as_of_date_str = date_rows.iloc[0].split("au ")[-1].strip()

            try:
                # Parse the date string into a datetime object
                as_of_date_object = datetime.strptime(as_of_date_str, "%d/%m/%Y")
            except ValueError:
                print(
                    f"Warning: Unable to parse date string '{as_of_date_str}'. Using current date."
                )

    return as_of_date_object


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


def GetInventory(dict_data_file):
    """
        This function returns a dataframe different charachterisitcs of the fund
        using the daily inventory file
        and save the underlying assets codes in dataset file.
    Args:
        workbook (xls): xls file sent by depositary

    Returns:
        DataFrame : preprocessed data of valuation

    Example
    -------
        f=GetInventory(WK)
    """

    # we get the workbook and then we precise that we want to get infomations from the Détails sheet
    if "Détails" in dict_data_file:
        details_sheet = dict_data_file["Détails"]
        details_sheet = dataframe_from_sheet(details_sheet, "Code valeur")

    headers = {
        "Action": "Stocks",
        "Obligation": "Bonds",
        "Sicav (O.P.C.V.M.)": "Sicav",
        "Interets precomptes.": "Negotiable_instruments",
        "Swap de Taux": "IRS",
    }
    # headers is the words we need to find their position in the sheet
    asset_class = []
    asset_class_str = ""
    on_coupon = False

    for data in details_sheet["Code valeur"]:
        asset_class.append(asset_class_str)
        if data == "Coupons":
            on_coupon = True
        elif data == "Total Coupons":
            on_coupon = False

        if data in headers:
            if on_coupon:
                asset_class_str = "Coupons"
            else:
                asset_class_str = headers[data]
        elif "Total" in data:
            asset_class_str = ""

    details_sheet["ASSET_CLASS"] = asset_class

    mapping_rename = {
        "Code valeur": "ISIN",
        "Libellé": "DESCRIPTION",
        "Quantité": "QUANTITY",
        "Cours": "PRICE",
        "Dev": "CURRENCY",
        "Date du cours": "VALUATION_DATE",
        "Valeur boursière": "MARKET_VALUE",
        "ASSET_CLASS": "ASSET_CLASS",
    }

    # We rename the relevant columns
    details_sheet = details_sheet.rename(columns=mapping_rename)
    # We drop the irrelevant columns
    for col in details_sheet.columns:
        if col not in mapping_rename.values():
            details_sheet = details_sheet.drop(columns=col)

    details_sheet = details_sheet[details_sheet["ASSET_CLASS"] != ""]
    details_sheet = details_sheet[~details_sheet["ISIN"].str.contains("Total")]
    details_sheet["VALUATION_DATE"] = details_sheet["VALUATION_DATE"].apply(
        lambda x: x.split(" ")[0] if isinstance(x, str) and " " in x else x
    )
    details_sheet["VALUATION_DATE"] = details_sheet["VALUATION_DATE"].astype(str)
    details_sheet = details_sheet[details_sheet["VALUATION_DATE"] > "2023-05-05"]
    details_sheet["cash_data"] = False
    details_sheet = details_sheet.reset_index(drop=True)
    details_sheet.columns = details_sheet.columns.str.upper()

    return details_sheet


def fix_swap_position(swaps_MV):
    swaps_MV.sort_values(by=["ISIN"], ascending=True)
    swaps_MV = swaps_MV.reset_index(drop=True)

    # BSK puis IRS
    # QLF ok
    # Amundi2 IRS BSK

    list_isin = list(swaps_MV["ISIN"])

    # BSK
    # print(list_isin)
    if "SWAP04025840" in list_isin and "SWAP04011952" in list_isin:
        if list_isin.index("SWAP04025840") > list_isin.index("SWAP04011952"):
            (
                list_isin[list_isin.index("SWAP04025840")],
                list_isin[list_isin.index("SWAP04011952")],
            ) = (
                list_isin[list_isin.index("SWAP04011952")],
                list_isin[list_isin.index("SWAP04025840")],
            )

    # IRS
    if "SWAP04025842" in list_isin and "SWAP04011953" in list_isin:
        if list_isin.index("SWAP04025842") < list_isin.index("SWAP04011953"):
            (
                list_isin[list_isin.index("SWAP04011953")],
                list_isin[list_isin.index("SWAP04025842")],
            ) = (
                list_isin[list_isin.index("SWAP04025842")],
                list_isin[list_isin.index("SWAP04011953")],
            )

    list_swaps_MV = []
    for isin in list_isin:
        desc = swaps_MV[swaps_MV["ISIN"] == isin]["DESCRIPTION"].values[0]
        if "VRAC" in desc or "BSK" in desc:
            list_swaps_MV.append(
                swaps_MV[swaps_MV["ISIN"] == isin]["MARKET_VALUE"].values[0]
            )
    for isin in list_isin:
        desc = swaps_MV[swaps_MV["ISIN"] == isin]["DESCRIPTION"].values[0]
        if "IDX" in desc or "INDX" in desc or "INDEX" in desc:
            list_swaps_MV.append(
                swaps_MV[swaps_MV["ISIN"] == isin]["MARKET_VALUE"].values[0]
            )
    number_of_tranche = len(list_swaps_MV) // 2

    list_valuation_date = []
    list_tranche = []
    list_BSK = []
    list_IRS = []

    for tranche in range(1, number_of_tranche + 1):
        try:
            val_date = swaps_MV[swaps_MV["MARKET_VALUE"] == list_swaps_MV[tranche - 1]][
                "VALUATION_DATE"
            ].values[0]
            list_valuation_date.append(val_date)
            list_tranche.append(tranche)
            list_BSK.append(list_swaps_MV[tranche - 1])
            list_IRS.append(list_swaps_MV[tranche + number_of_tranche - 1])
        except Exception as e:
            pass
    dict_result = {
        "VALUATION_DATE": list_valuation_date,
        "TRANCHE": list_tranche,
        "BSK": list_BSK,
        "IRS": list_IRS,
    }
    df_result = pd.DataFrame.from_dict(dict_result)
    return df_result


def GetCurrencyExchangeRate(dict_data_file):
    mapping_rename = {
        "Devise": "Currency",
        "Date du cours": "VALUATION_DATE",
        "Cours utilisé": "Rate",
        "Cours inverse": "Inverted_rate",
        "currency1": "currency1",
        "currency2": "currency2",
    }

    if "Cours des devises utilisées" in dict_data_file:
        Currency_sheet = dict_data_file["Cours des devises utilisées"]
        Currency_sheet = dataframe_from_sheet(Currency_sheet, "Devise")
    else:
        Currency_sheet = pd.DataFrame(columns=list(mapping_rename.keys()))

    Currency_sheet = Currency_sheet.rename(columns=mapping_rename)
    Currency_sheet["VALUATION_DATE"] = Currency_sheet["VALUATION_DATE"].apply(
        lambda x: x.split(" ")[0] if isinstance(x, str) and " " in x else x
    )
    Currency_sheet["Rate"] = Currency_sheet["Rate"].astype(float)
    Currency_sheet["Inverted_rate"] = Currency_sheet["Inverted_rate"].astype(float)
    Currency_sheet["VALUATION_DATE"] = Currency_sheet["VALUATION_DATE"].astype(str)
    Currency_sheet = Currency_sheet[Currency_sheet["VALUATION_DATE"] > "2023-05-05"]
    if not Currency_sheet.empty:
        Currency_sheet[["currency1", "currency2"]] = Currency_sheet[
            "Currency"
        ].str.split("/", n=1, expand=True)
    Currency_sheet = Currency_sheet.reset_index(drop=True)
    Currency_sheet.columns = Currency_sheet.columns.str.upper()

    return Currency_sheet


def GetCashDetails(dict_data_file):
    """
        This function returns a dataframe different components of cash in the fund
    Args:
        workbook (xls): xls file sent by depositary
        fund : which fund is it QLF or QTF

    Returns:
        DataFrame : preprocessed data of valuation

    Example
    -------
        f=GetInventory(WK)
    """

    if "Détails" in dict_data_file:
        details_sheet = dict_data_file["Détails"]
        details_sheet = dataframe_from_sheet(details_sheet, "Code valeur")

    # here we try to find the position of those headers

    headers = {
        "BANQUE OU ATTENTE": "Bank",
        "DEPOSIT DE GARANTIE": "margin_call",
        "DEPOTS A TERME": "terme_deposit",
        "FRAIS DE GESTION": "Management_fees",
    }

    asset_class = []
    asset_class_str = ""

    for data in details_sheet["Code valeur"]:
        asset_class.append(asset_class_str)
        if data in headers:
            asset_class_str = headers[data]
        elif "Total" in data:
            asset_class_str = ""

    details_sheet["ASSET_CLASS"] = asset_class

    mapping_rename = {
        "Code valeur": "ISIN",
        "Libellé": "DESCRIPTION",
        "Quantité": "QUANTITY",
        "Dev": "CURRENCY",
        "Date du cours": "VALUATION_DATE",
        "Valeur boursière": "MARKET_VALUE",
        "ASSET_CLASS": "ASSET_CLASS",
    }

    details_sheet = details_sheet.rename(columns=mapping_rename)
    # We drop the irrelevant columns
    for col in details_sheet.columns:
        if col not in mapping_rename.values():
            details_sheet = details_sheet.drop(columns=col)

    details_sheet = details_sheet[details_sheet["ASSET_CLASS"] != ""]
    details_sheet = details_sheet[~details_sheet["ISIN"].str.contains("Total")]
    details_sheet["VALUATION_DATE"] = details_sheet["VALUATION_DATE"].apply(
        lambda x: x.split(" ")[0] if isinstance(x, str) and " " in x else x
    )
    details_sheet["VALUATION_DATE"] = details_sheet["VALUATION_DATE"].astype(str)
    details_sheet = details_sheet[details_sheet["VALUATION_DATE"] > "2023-05-05"]
    details_sheet["CASH_DATA"] = True
    details_sheet["PRICE"] = np.nan
    details_sheet = details_sheet.reset_index(drop=True)
    details_sheet.columns = details_sheet.columns.str.upper()

    return details_sheet

def get_Recap(dict_data_file):
    """
    this function is used to get general informations about different buckets of the fund (assets / swaps / fees)
    the goal is to have the table in sheet Récapitulatif as a dataframe


    Args:
        workbook (_type_): an xls file

    Returns:
        _type_: dataframe with different asset classes and their value
    """

    if "Récapitulatif" in dict_data_file:
        Recap_sheet = dict_data_file["Récapitulatif"]
        date_from_file = datetime.strptime(
            Recap_sheet.at[3, "Unnamed: 1"].split(" ")[1], "%d/%m/%Y"
        ).strftime("%Y-%m-%d")
        Recap_sheet = dataframe_from_sheet(Recap_sheet, "Valeur boursière")

    if "ASSET_CLASS" not in Recap_sheet.columns:
        headers = [
            "Valeurs mobilieres",
            "Creances negociables",
            "Coupons",
            "Dossiers",
            "Swap de Taux",
            "Liquidites",
            "Total",
        ]
        list_header_ordered = []
        for i in Recap_sheet["Valeur boursière"]:
            if i in headers:
                list_header_ordered.append(i)
                Recap_sheet = Recap_sheet.drop(
                    Recap_sheet[Recap_sheet["Valeur boursière"] == i].index
                )
        Recap_sheet["ASSET_CLASS"] = list_header_ordered
        missing_headers = list(set(headers) - set(list_header_ordered))
        for header in missing_headers:
            Recap_sheet.loc[len(Recap_sheet), "ASSET_CLASS"] = header

    rename_dict = {
        "ASSET_CLASS": "ASSET_CLASS",
        "VALUATION_DATE": "VALUATION_DATE",
        "Valeur boursière": "MARKET_VALUE",
        "Prix de revient": "COST_PRICE",
        "+/- value": "GAIN_LOSS",
        "Intérêts courus": "ACCRUED_INTEREST",
    }

    Recap_sheet["VALUATION_DATE"] = date_from_file

    Recap_sheet = Recap_sheet.rename(columns=rename_dict)
    col = Recap_sheet.pop("ASSET_CLASS")
    Recap_sheet.insert(0, col.name, col)
    col = Recap_sheet.pop("VALUATION_DATE")
    Recap_sheet.insert(1, col.name, col)

    def rename_asset_class(string_name):
        result = string_name

        dict_string_convert = {
            "Valeurs mobilieres": "Securities",
            "Creances negociables": "Negotiable_Instruments",
            "Coupons": "Coupons",
            "Dossiers": "Dossiers",
            "Swap de Taux": "IR_Swaps",
            "Liquidites": "Cash",
            "Total": "Total",
        }

        if string_name in dict_string_convert:
            result = dict_string_convert[string_name]

        return result

    Recap_sheet["ASSET_CLASS"] = Recap_sheet["ASSET_CLASS"].apply(
        lambda x: rename_asset_class(x)
    )
    Recap_sheet.replace(np.nan, 0, inplace=True)
    Recap_sheet["VALUATION_DATE"] = Recap_sheet["VALUATION_DATE"].astype(str)
    Recap_sheet = Recap_sheet[Recap_sheet["VALUATION_DATE"] > "2023-05-05"]
    Recap_sheet.reset_index(drop=True, inplace=True)
    Recap_sheet.columns = Recap_sheet.columns.str.upper()

    return Recap_sheet


def getHistoric(path):
    """
    function to read the NAV file generated from SGSS website

    Args:
        path (xls): NAV file directory

    Returns:
        DataFrame: summary of NAVs in a single Dataframe
    """
    xlsfile = xlrd.open_workbook(path)
    # we read the details sheet in the worksheet
    sheetDetails = xlsfile.sheet_by_name("Details")
    # the dataframe to fill we need ti map each colon by his index
    details_df = pd.DataFrame(
        {
            "DATE_": sheetDetails.col_values(1),
            "NET_ASSET_VALUE": sheetDetails.col_values(4),
            "NUMBER_OF_SHARES": sheetDetails.col_values(5),
            "NAV_PER_SHARE": sheetDetails.col_values(6),
        }
    )

    details = details_df.dropna()
    # remove rows that contains a space ""
    details_ = details[~details.apply(lambda row: row.str.strip().eq("")).any(axis=1)]

    details_.reset_index(drop=True, inplace=True)
    # drop the header
    details_ = details_.drop(0)
    details_.reset_index(drop=True, inplace=True)

    # this is used to handle dates
    def to_datetime(var):
        return xlrd.xldate.xldate_as_datetime(var, xlsfile.datemode)

    # we use the function to handle dates
    details_["DATE_"] = details_["DATE_"].apply(to_datetime)
    # then we save the dataframe in a csv file and we return it
    file_path = Path("/output/historic.csv")
    if file_path.exists():
        file_path.unlink()
    details_.to_csv("output/historic.csv", index=False)
    return details_


def GetNAV(dict_data_file):
    """
    get the Net asset value from different xls files


    Args:
        workbook (xls): xls file of valuation

    Returns:
        dataframe: preprocessed dataframe
    """
    # workbook = xlrd.open_workbook(Path)

    if "Synthèse" in dict_data_file:
        synthesis_sheet = dict_data_file["Synthèse"]
        synthesis_sheet = dataframe_from_sheet(synthesis_sheet, "Code ISIN")

    mapping_rename = {
        "DATE_": "DATE_",
        "Actif de la part": "NET_ASSET_VALUE",
        "Nombre de parts": "NUMBER_OF_SHARES",
        "VL": "NAV_PER_SHARE",
        "Dev": "CURRENCY",
    }

    synthesis_sheet = synthesis_sheet.rename(columns=mapping_rename)
    # We drop the irrelevant columns
    for col in synthesis_sheet.columns:
        if col not in mapping_rename.values():
            synthesis_sheet = synthesis_sheet.drop(columns=col)

    synthesis_sheet.reset_index(drop=True, inplace=True)
    if len(synthesis_sheet) > 13:
        synthesis_sheet = synthesis_sheet.drop(10)
    synthesis_sheet.reset_index(drop=True, inplace=True)
    synthesis_sheet.columns = synthesis_sheet.columns.str.upper()
    """if os.path.exists('dataset/ISIN.csv'):
        os.remove('dataset/ISIN.csv')
    df_cleaned.to_csv('dataset/ISIN.csv', header=None, index=False)"""
    return synthesis_sheet


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
    date_column_numerical = mdates.date2num(df[date_column])
    complete_dates_numerical = mdates.date2num(complete_dates)

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
