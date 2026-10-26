"""Pruebas unitarias para Radix Sort."""
import sys
from pathlib import Path
import unittest

# Asegurar que la ruta raiz del proyecto este en el PATH para permitir importaciones de src
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.bibliometric_analysis.ranking.radix_sort import counting_sort_by_digit, radix_sort


class TestRadixSort(unittest.TestCase):
    def test_empty_list(self):
        """Verifica que una lista vacia retorne una lista vacia."""
        self.assertEqual(radix_sort([]), [])

    def test_single_element(self):
        """Verifica que una lista de un solo elemento se mantenga igual."""
        data = [("intelligence", 42)]
        self.assertEqual(radix_sort(data), [("intelligence", 42)])

    def test_already_sorted_descending(self):
        """Verifica que respete una lista ya ordenada de mayor a menor."""
        data = [("model", 100), ("data", 50), ("learning", 20), ("ai", 5)]
        expected = [("model", 100), ("data", 50), ("learning", 20), ("ai", 5)]
        self.assertEqual(radix_sort(data, descending=True), expected)

    def test_unsorted_descending_ranking(self):
        """Verifica el ordenamiento descendente (ranking por frecuencia)."""
        data = [
            ("learning", 15),
            ("ai", 120),
            ("system", 5),
            ("data", 45),
            ("model", 80),
        ]
        result = radix_sort(data, descending=True)
        frequencies = [freq for _, freq in result]
        self.assertEqual(frequencies, [120, 80, 45, 15, 5])

    def test_ascending_order(self):
        """Verifica el ordenamiento ascendente si descending=False."""
        data = [("b", 30), ("a", 10), ("c", 20)]
        result = radix_sort(data, descending=False)
        self.assertEqual(result, [("a", 10), ("c", 20), ("b", 30)])

    def test_ties_same_frequency(self):
        """Verifica que maneje terminos con frecuencias repetidas sin perder ninguno."""
        data = [("alpha", 10), ("beta", 10), ("gamma", 20), ("delta", 10)]
        result = radix_sort(data, descending=True)
        self.assertEqual(len(result), 4)
        # El primero debe ser gamma con 20
        self.assertEqual(result[0], ("gamma", 20))
        # Los otros tres deben tener frecuencia 10
        self.assertTrue(all(freq == 10 for _, freq in result[1:]))
        terms = {term for term, _ in result}
        self.assertEqual(terms, {"alpha", "beta", "gamma", "delta"})

    def test_various_digit_lengths(self):
        """Verifica numeros de diferentes longitudes de digitos (1, 2, 3 y 4 digitos)."""
        data = [
            ("uno", 7),
            ("dos", 89),
            ("tres", 3),
            ("cuatro", 1050),
            ("cinco", 240),
            ("seis", 12),
        ]
        result = radix_sort(data, descending=True)
        frequencies = [freq for _, freq in result]
        self.assertEqual(frequencies, [1050, 240, 89, 12, 7, 3])

    def test_zero_frequency(self):
        """Verifica que maneje terminos con frecuencia 0."""
        data = [("zero", 0), ("one", 1), ("another_zero", 0)]
        result = radix_sort(data, descending=True)
        self.assertEqual(result[0], ("one", 1))
        self.assertEqual(result[1][1], 0)
        self.assertEqual(result[2][1], 0)


if __name__ == "__main__":
    unittest.main()
