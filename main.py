from collections import Counter
from dataclasses import dataclass
from operator import attrgetter
from typing import List, Dict


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

    def __str__(self):
        return self.name


@dataclass
class Lack:
    item_name: str
    count: int
    shops: frozenset

    def __repr__(self):
        if self.count:
            shops_str = ", ".join(self.shops)
            shops_str = f" ({shops_str})"
        else:
            shops_str = ""

        return f"{self.item_name} - {self.count}{shops_str}"


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


def get_lacks(shops: List[Shop]) -> List[Lack]:
    set_of_lacks = set()

    lack_items_shops: Dict[str, set] = {}

    all_names = get_all_items_names(shops)

    lacks: List[Lack] = []

    for item_name in all_names:
        lack_items_shops[item_name] = set()
        for shop in shops:
            if shop.catalog[item_name] == 0:
                set_of_lacks.add(item_name)
                lack_items_shops[item_name].add(shop.name)

        lacks.append(Lack(
            item_name=item_name,
            count=len(lack_items_shops[item_name]),
            shops=frozenset(lack_items_shops[item_name])
        ))

    return lacks


def sort_lacks(lacks: List[Lack]):
    return sorted(lacks, key=attrgetter('count', 'item_name'))


def get_result_str(lacks: List[Lack]) -> str:
    return "\n".join(list(map(str, lacks)))


def write_result(result_str: str, filename='output.txt'):
    with open(filename, 'w', encoding='utf-8-sig') as file:
        file.write(result_str)


if __name__ == '__main__':
    shops = get_input_data()
    lacks = sort_lacks(get_lacks(shops))
    result_str = get_result_str(lacks)
    write_result(result_str)
