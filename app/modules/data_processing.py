import pandas as pd
from sklearn.preprocessing import StandardScaler

def check_data(df):
    required_columns = ["Date", "Net Cashflow from Operations", "Total Inflows", "Total Outflows"]

    # Check if dataframe has all the required columns
    if not all(column in df.columns for column in required_columns):
        return False

    # Check if 'Date' column can be converted to datetime format
    try:
        df['Date'] = pd.to_datetime(df['Date'])
    except ValueError:
        return False

    return True

def process_data(df):
    df = df[["Date", "Net Cashflow from Operations", "Total Inflows", "Total Outflows"]].copy()
    df["period"] = pd.to_datetime(df["Date"]).dt.to_period("M")

    sc = StandardScaler()
    all_periods = df.period.unique().tolist()
    p1 = all_periods[-2:]
    p1df = df.loc[df["period"].isin(p1)]
    sc.fit(p1df[["Net Cashflow from Operations"]])

    for per in all_periods[::-1][2:]:
        sc2 = StandardScaler()
        p2df = df.loc[df["period"]==per]
        ncf_t = sc2.fit_transform(p2df[["Net Cashflow from Operations"]])
        ncf_it = sc.inverse_transform(ncf_t)
    
        df.loc[df["period"]==per, "Net Cashflow from Operations"] = ncf_it

    df["Net Cashflow from Operations"] = df["Net Cashflow from Operations"].clip(
        df["Net Cashflow from Operations"].quantile(0.05),
        df["Net Cashflow from Operations"].quantile(0.95)
    )

    df["Net Cashflow from Operations"] = df["Net Cashflow from Operations"] / 10000000

    df = df.reset_index(drop=True)
    df.set_index('Date', inplace=True)

    return df
