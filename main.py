from collections import Counter
from pprint import pprint
from typing import List


class Shop:
    __slots__ = 'name', 'catalog'

    def __init__(self, name, catalog_str):
        self.name = name
        self.catalog = Counter()
        self._set_catalog(catalog_str)

    def _set_catalog(self, catalog_str: str):
        items = catalog_str.split(', ')

        for item in items:
            item_name, item_count = item.split(' - ', 1)
            self.catalog[item_name] = int(item_count)

    def get_items_names(self):
        return set(self.catalog)

    def __repr__(self):
        return f"{self.name}: {self.catalog}"


def get_input_data(filename='input.txt') -> List[Shop]:
    with open(filename, 'r', encoding='utf-8') as file:
        input_lines = file.readlines()
    shops = []
    for line in input_lines:
        line = line.rstrip()
        shop_name, catalog_str = line.split(': ', 1)
        shops.append(Shop(shop_name, catalog_str))

    return shops


def get_all_items_names(shops: List[Shop]) -> set:
    all_names = set()

    for shop in shops:
        all_names |= shop.get_items_names()

    return all_names


if __name__ == '__main__':
    shops = get_input_data()
    pprint(shops)
    all_names = get_all_items_names(shops)
    pprint(all_names)
