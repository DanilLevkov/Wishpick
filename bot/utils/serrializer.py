from aiogram.utils.formatting import (
    as_list, as_key_value, HashTag, as_line, TextLink, Text
)


def gift_to_str(gift: dict) -> Text:
    result = []
    keys = gift.keys()
    if "name" in keys:
        result.append(as_key_value("Название", gift["name"]))
    if "price" in keys:
        result.append(as_key_value("Цена", str(gift["price"]) + " руб."))
    if "score" in keys:
        result.append(as_key_value("Оценка", gift["score"]))
    if "url" in keys:
        result.append(TextLink("Ссылка", url=gift["url"]))
    if "category" in keys:
        tags = as_line([HashTag("#" + x) for x in gift["category"].keys()], end='', sep=' ')
        result.append(tags)
    return as_list(*result)
