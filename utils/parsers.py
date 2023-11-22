import re


def get_price_range(text: str):
    if not text:
        return

    def price(tag: str):
        if tag not in text:
            return
        right_side = text.split(tag, 1)[1]
        num_str = right_side.split()[0]
        try:
            num = int(num_str)
            if num < 0:
                num = 0
            if num < 20:
                num *= 1000
            return num
        except ValueError:
            return

    res = dict

    from_num = price("от")
    to_num = price("до")
    if from_num and to_num and to_num < from_num:
        from_num = None

    if from_num or to_num:
        return {"from": from_num, "to": to_num}
