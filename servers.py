#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from typing import Optional, List, TypeVar
from abc import ABC, abstractmethod


class Product:
    def __init__(self, name: str, price: float):
        if re.fullmatch('[a-zA-Z]+[0-9]+', name) is None:
            raise ValueError
        self.name = name
        self.price = price

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.price == other.price

    def __hash__(self) -> int:
        return hash((self.name, self.price))


class ServerError(Exception):
    pass


class TooManyProductsFoundError(ServerError):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


class Server(ABC):
    n_max_returned_entries = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_entries(self, n_letters: int = 1):
        res = []
        for entry in self._get_products():
            pattern = '[a-zA-Z]{' + str(n_letters) + '}[0-9]{2,3}'
            if re.fullmatch(pattern, entry.name) is not None:
                res.append(entry)
        if len(res) > self.n_max_returned_entries:
            raise TooManyProductsFoundError
        res.sort(key=lambda x: x.price)
        return res

    @abstractmethod
    def _get_products(self) -> List[Product]:
        raise NotImplementedError


ServerType = TypeVar('ServerType', bound=Server)


class ListServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = products

    def _get_products(self) -> List[Product]:
        return self.products


class MapServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = {p.name: p for p in products}

    def _get_products(self) -> List[Product]:
        return list(self.products.values())


class Client:

    def __init__(self, server: ServerType):
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
