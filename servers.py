#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from typing import Optional, Union, List


class Product:
    def __init__(self, name: str, price: float):
        if re.fullmatch('[a-zA-Z]+[0-9]+', name) is None:
            raise ValueError
        self.name = name
        self.price = price

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    def __init__(self, n: int):
        self.n = n
        super().__init__("Ilość produktów wyniosła: {}".format(n))


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class ListServer:
    def __init__(self, products: List[Product]):
        self.__n_max_returned_entries = 3
        self.__products = products[:]

    def get_entries(self, n_letters: Optional[int] = 1):
        res = []
        for entry in self.__products:
            pattern = '[a-zA-Z]{' + str(n_letters) + '}[0-9]{2,3}'
            if re.fullmatch(pattern, entry.name) is not None:
                res.append(entry)
        if len(res) > self.__n_max_returned_entries:
            raise TooManyProductsFoundError
        res.sort(key=lambda x: x.price)
        return res

    @property
    def n_max_returned_entries(self):
        return self.__n_max_returned_entries


class MapServer:
    def __init__(self, products: List[Product]):
        self.__n_max_returned_entries = 3
        self.__products = {p.name: p for p in products}

    def get_entries(self, n_letters: Optional[int] = 1):
        res = []
        for entry in self.__products.values():
            pattern = '[a-zA-Z]{' + str(n_letters) + '}[0-9]{2,3}'
            if re.fullmatch(pattern, entry.name) is not None:
                res.append(entry)
        if len(res) > self.__n_max_returned_entries:
            raise TooManyProductsFoundError
        res.sort(key=lambda x: x.price)
        return res

    @property
    def n_max_returned_entries(self):
        return self.__n_max_returned_entries


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server: Union[ListServer, MapServer]):
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            if n_letters is None:
                prod = self.server.get_entries()
            else:
                prod = self.server.get_entries(n_letters)
            if not prod:
                return None
            else:
                return sum([p.price for p in prod])
        except TooManyProductsFoundError:
            return None
