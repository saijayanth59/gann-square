import yfinance as yf
import calculate_gann_values from utils
from bisect import bisect_left

def day_test(date, data):
    first_close = data.iloc[0]['Close'].iloc[0]
    gann_values = calculate_gann_values(first_close)

    trade_details = {
        "date": date,
        "entry": None,
        "entryTime": None,
        "tradeType": None,
        "exit": None,
        "exitTime": None,
        "target": None,
        "stopLoss": None,
        "level": -1,
        "isHit": False,
        "isLoss": False
    }

    for _, row in data.iterrows():
        high = row.iloc["High"]
        low = row.iloc["Low"]
        close = row.iloc["Close"]
        open_price = row.iloc["Open"]

        #entry
        if trade_details["tradeType"] is not None and trade_details["entry"] is None:
            trade_details.update({
                    "entry": open_price,
                    "entryTime": data.index,
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
            if close > gann_values["buy_above"]:
                trade = True
                trade_details.update({
                    "tradeType": "buy",
                })
            elif close < gann_values["sell_below"]:
                trade = True
                trade_details.update({
                    "tradeType": "sell",
                })
        else:
            #target check
            if trade_details["tradeType"] == "buy":
                idx = bisect_left(trade_details["target"], high)
                if idx < len(trade_details["target"]) and high < trade_details["target"][idx]:
                    continue
                trade_details["level"] = max(trade_details["level"], idx)
            else:
                idx = len(trade_details["target"]) - bisect_left(trade_details["target"][::-1], low) - 1
                if idx >= 0 and  low > trade_details["target"][idx]:
                    continue
                trade_details["level"] = max(trade_details["level"], idx)

        #stoploss check
        






