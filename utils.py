import math

def calculate_gann_values(num):
    y = num

    if num:
        root = num ** 0.5
        minus_two = root - 2
        rounded = math.ceil(minus_two)
        result = rounded ** 2

        x = []
        sqr_x = []
        sqr_x_rounded = []
        sqr_x_rounded_root = []

        for i in range(24):
            x.append(rounded + 0.125 * (i + 1))
            sqr_x.append(x[i] * x[i])
            sqr_x_rounded.append(round(sqr_x[i] * 100) / 100)
            sqr_x_rounded_root.append(round((num - sqr_x_rounded[i]) * 100) / 100)

        min_positive_index = -1
        for i in range(len(sqr_x_rounded_root)):
            if sqr_x_rounded_root[i] < 0:
                min_positive_index = i
                break

        support = []
        resistance = []
        buy_target = []
        sell_target = []

        def roundup(number, places):
            factor = 10 ** places
            return round(number * factor) / factor

        if min_positive_index >= 0:
            buy_above = sqr_x_rounded[min_positive_index]
            sell_below = sqr_x_rounded[min_positive_index - 1]

            for i in range(5):
                support.append(sqr_x_rounded[min_positive_index - 2 - i])
                resistance.append(sqr_x_rounded[min_positive_index + 1 + i])
                buy_target.append(roundup(resistance[i] * 0.9995, 2))
                sell_target.append(roundup(support[i] * 1.0005, 2))
        else:
            buy_above = ""
            sell_below = ""
            support = [""] * 5
            resistance = [""] * 5
            buy_target = [""] * 5
            sell_target = [""] * 5

        return {
            "buy_above": buy_above,
            "sell_below": sell_below,
            "buy_target": buy_target,
            "sell_target": sell_target
        }
    else:
        return {
            "buy_above": "",
            "sell_below": "",
            "buy_target": [""] * 5,
            "sell_target": [""] * 5
        }


if __name__ == "__main__":
    inpt = float(input("Enter value: "))
    print(calculate_gann_values(inpt))
