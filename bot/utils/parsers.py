import re


def get_price_range(text: str):
    if not text:
        return

    def price(tag: str):
        if tag not in text:
            return
        right_side = text.split(tag, 1)[1]
        num_str = re.search(r'(\d+)', right_side)
        if not num_str:
            return
        try:
            num = int(num_str.group(0))
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
