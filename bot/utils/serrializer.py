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
    if "brand" in keys:
        result.append(as_key_value("Бренд", gift["brand"]))
    if "category" in keys:
        tags = [HashTag("#" + x) for x in gift["category"]]
        tag_line = as_line(*tags, end='', sep=' ')
        result.append(tag_line)
    return as_list(*result)
