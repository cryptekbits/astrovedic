# tests/vedic/shadbala/test_advanced.py
"""
Unit tests for functions in astrovedic.vedic.shadbala.advanced
Specifically testing the refactored Ishta and Kashta Phala calculations.
"""

import unittest
import math

from astrovedic.vedic.shadbala.advanced import calculate_ishta_phala, calculate_kashta_phala


class TestIshtaKashtaPhala(unittest.TestCase):
    """Tests the Ishta and Kashta Phala calculations."""

    def test_ishta_phala_high_values(self):
        """Test Ishta Phala with high Uchcha and Cheshta Bala."""
        uchcha = 50.0
        cheshta = 45.0
        expected_ishta = math.sqrt(uchcha * cheshta)  # sqrt(2250) approx 47.43
        result = calculate_ishta_phala(uchcha, cheshta)
        self.assertAlmostEqual(result['value'], expected_ishta, places=4)
        self.assertEqual(result['description'], 'Very High (Auspicious Potential)')

    def test_ishta_phala_low_values(self):
        """Test Ishta Phala with low Uchcha and Cheshta Bala."""
        uchcha = 10.0
        cheshta = 5.0
        expected_ishta = math.sqrt(uchcha * cheshta)  # sqrt(50) approx 7.07
        result = calculate_ishta_phala(uchcha, cheshta)
        self.assertAlmostEqual(result['value'], expected_ishta, places=4)
        self.assertEqual(result['description'], 'Low (Auspicious Potential)')

    def test_ishta_phala_zero_values(self):
        """Test Ishta Phala with zero Uchcha or Cheshta Bala."""
        self.assertAlmostEqual(calculate_ishta_phala(0, 30)['value'], 0.0, places=4)
        self.assertAlmostEqual(calculate_ishta_phala(30, 0)['value'], 0.0, places=4)
        self.assertAlmostEqual(calculate_ishta_phala(0, 0)['value'], 0.0, places=4)

    def test_ishta_phala_max_values(self):
        """Test Ishta Phala with maximum Uchcha and Cheshta Bala."""
        uchcha = 60.0
        cheshta = 60.0
        expected_ishta = math.sqrt(uchcha * cheshta) # 60.0
        result = calculate_ishta_phala(uchcha, cheshta)
        self.assertAlmostEqual(result['value'], expected_ishta, places=4)
        self.assertEqual(result['description'], 'Very High (Auspicious Potential)')

    def test_kashta_phala_high_values(self):
        """Test Kashta Phala with low Uchcha and Cheshta Bala (high Kashta)."""
        uchcha = 5.0
        cheshta = 10.0
        expected_kashta = math.sqrt((60 - uchcha) * (60 - cheshta)) # sqrt(55*50) = sqrt(2750) approx 52.44
        result = calculate_kashta_phala(uchcha, cheshta)
        self.assertAlmostEqual(result['value'], expected_kashta, places=4)
        self.assertEqual(result['description'], 'Very High (Inauspicious Potential)')

    def test_kashta_phala_low_values(self):
        """Test Kashta Phala with high Uchcha and Cheshta Bala (low Kashta)."""
        uchcha = 55.0
        cheshta = 50.0
        expected_kashta = math.sqrt((60 - uchcha) * (60 - cheshta)) # sqrt(5*10) = sqrt(50) approx 7.07
        result = calculate_kashta_phala(uchcha, cheshta)
        self.assertAlmostEqual(result['value'], expected_kashta, places=4)
        self.assertEqual(result['description'], 'Low (Inauspicious Potential)')

    def test_kashta_phala_zero_values(self):
        """Test Kashta Phala with max Uchcha or Cheshta Bala (zero Kashta)."""
        self.assertAlmostEqual(calculate_kashta_phala(60, 30)['value'], 0.0, places=4)
        self.assertAlmostEqual(calculate_kashta_phala(30, 60)['value'], 0.0, places=4)
        self.assertAlmostEqual(calculate_kashta_phala(60, 60)['value'], 0.0, places=4)

    def test_kashta_phala_max_values(self):
        """Test Kashta Phala with zero Uchcha and Cheshta Bala (max Kashta)."""
        uchcha = 0.0
        cheshta = 0.0
        expected_kashta = math.sqrt((60 - uchcha) * (60 - cheshta)) # 60.0
        result = calculate_kashta_phala(uchcha, cheshta)
        self.assertAlmostEqual(result['value'], expected_kashta, places=4)
        self.assertEqual(result['description'], 'Very High (Inauspicious Potential)')

    def test_ishta_kashta_phala_mixed(self):
        """Test Ishta and Kashta with mixed high/low values."""
        uchcha = 50.0
        cheshta = 10.0
        expected_ishta = math.sqrt(50 * 10)  # sqrt(500) approx 22.36
        expected_kashta = math.sqrt((60 - 50) * (60 - 10)) # sqrt(10 * 50) = sqrt(500) approx 22.36

        ishta_result = calculate_ishta_phala(uchcha, cheshta)
        kashta_result = calculate_kashta_phala(uchcha, cheshta)

        self.assertAlmostEqual(ishta_result['value'], expected_ishta, places=4)
        self.assertEqual(ishta_result['description'], 'Moderate (Auspicious Potential)')
        self.assertAlmostEqual(kashta_result['value'], expected_kashta, places=4)
        self.assertEqual(kashta_result['description'], 'Moderate (Inauspicious Potential)')

    def test_invalid_input_range(self):
        """Test that ValueError is raised for out-of-range inputs."""
        with self.assertRaises(ValueError):
            calculate_ishta_phala(-1, 30)
        with self.assertRaises(ValueError):
            calculate_ishta_phala(30, -1)
        with self.assertRaises(ValueError):
            calculate_ishta_phala(61, 30)
        with self.assertRaises(ValueError):
            calculate_ishta_phala(30, 61)

        with self.assertRaises(ValueError):
            calculate_kashta_phala(-1, 30)
        with self.assertRaises(ValueError):
            calculate_kashta_phala(30, -1)
        with self.assertRaises(ValueError):
            calculate_kashta_phala(61, 30)
        with self.assertRaises(ValueError):
            calculate_kashta_phala(30, 61)


if __name__ == '__main__':
    unittest.main()
