import yfinance as yf
import pandas as pd
from utils import calculate_gann_values, test_data
from bisect import bisect_left




def day_test(date, data):
    first_close = data.iloc[0]['Close']
    gann_values = calculate_gann_values(first_close)
    trades = []

    def initialize_trade():
        return {
            "date": date,
            "entry": None,
            "entryTime": None,
            "tradeType": None,
            "exit": None,
            "exitTime": None,
            "target": None,
            "stopLoss": None,
            "stopLossTime": None,
            "level": -1,
            **gann_values
        }

    trade_details = initialize_trade()
    for _, row in data.iterrows():
        if trade_details["stopLossTime"]:
            trades.append(trade_details)
            trade_details = initialize_trade()

        high = row["High"]
        low = row["Low"]
        close = row["Close"]
        open_price = row["Open"]

        #entry
        if trade_details["tradeType"] is not None and trade_details["entry"] is None:
            trade_details.update({
                    "entry": open_price,
                    "entryTime": row["time"],
            })
            if trade_details["tradeType"] == "buy":
                trade_details.update({
                    "target": gann_values["buy_target"],
                    "stopLoss": gann_values["sell_below"],
                })
            else:
                trade_details.update({
                    "target": gann_values["sell_target"],
                    "stopLoss": gann_values["buy_above"]
                })

        #entry check
        if trade_details["entry"] is None:
            if close >= gann_values["buy_above"]:
                # print(close, gann_values["buy_above"], date)
                trade = True
                trade_details.update({
                    "tradeType": "buy",
                })
            elif close <= gann_values["sell_below"]:
                trade = True
                trade_details.update({
                    "tradeType": "sell",
                })
        #target and stoploss check
        else:
             #stoploss check
            if trade_details["tradeType"] == "buy" and close <= trade_details["stopLoss"]:
                trade_details["stopLossTime"] = row["time"] 
                
            if trade_details["tradeType"] == "sell" and close >= trade_details["stopLoss"]:
                trade_details["stopLossTime"] = row["time"]

            if trade_details["tradeType"] == "buy":
                idx = bisect_left(trade_details["target"], high)
                if idx == 0 and high < trade_details["target"][0]:
                    continue
                if trade_details["level"] < idx:
                    trade_details["level"] = idx
                    trade_details["exitTime"] = row["time"]

            else:
                idx = len(trade_details["target"]) - bisect_left(trade_details["target"][::-1], low) - 1#need 
                if idx == 0 and low > trade_details["target"][0]:
                    continue
                if trade_details["level"] < idx:
                    trade_details["level"] = idx
                    trade_details["exitTime"] = row["time"]



    if trade_details["level"] != -1:
        idx = min(trade_details["level"], len(trade_details["target"]) - 1)
        trade_details["exit"] = trade_details["target"][idx]
    trades.append(trade_details)

    return trades



def test(data):
    grouped = data.groupby(data.index.date)

    for date, group in grouped:
        trades = day_test(date, group)
        for trade_details in trades:
            print(date, ": ",  trade_details)
            print()

if __name__ == "__main__":
    # data = yf.download("VOLTAS.NS", interval="5m", period="1mo")
    # data.index = pd.to_datetime(data.index).tz_convert('Asia/Kolkata')
    # data.columns = data.columns.get_level_values(0)
    data = test_data()
    
    test(data)
