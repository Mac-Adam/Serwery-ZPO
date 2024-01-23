import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):
    def test_server_has_products(self):
        products = []
        for server_type in server_types:
            server = server_type(products)
            self.assertTrue(hasattr(server, 'products'))

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_get_entries_is_sorted(self):
        products = [Product('P12', 1), Product('PD235', 4), Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(products[2], entries[0])
            self.assertEqual(products[3], entries[1])
            self.assertEqual(products[1], entries[2])

    def test_get_entries_error(self):
        products = [Product('P12', 1), Product('GG12', 1), Product('PD235', 4), Product('PP234', 2),
                    Product('PP235', 3), Product('JK23', 1)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFoundError):
                server.get_entries(2)


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    def test_total_price_for_error(self):
        products = [Product('P12', 1), Product('GG12', 1), Product('PD235', 4), Product('PP234', 2),
                    Product('PP235', 3), Product('JK23', 1)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))


class ProductTest(unittest.TestCase):

    def test_valid_name(self):
        valid_names = ['asdad231', 'a2', 'faASF18274365']
        for name in valid_names:
            prod = Product(name, 0)
            self.assertEqual(prod.name, name)

    def test_invalid_names(self):
        invalid_names = ['asdasdad', '123123', 'casdasd21313afs', '23dsad', '23dasas23', 'sad*2']
        for name in invalid_names:
            with self.assertRaises(ValueError):
                p = Product(name, 0)

    def check_equals(self):
        p1 = Product("aabb12", 0)
        p2 = Product('aabb12', 1)
        p3 = Product('aabb13', 0)
        p4 = Product('aabb12', 0)
        self.assertTrue(p1 == p4)
        self.assertFalse(p1 == p2)
        self.assertFalse(p1 == p3)
        self.assertFalse(p3 == p4)


if __name__ == '__main__':
    unittest.main()
