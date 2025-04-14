import unittest
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos
from astrovedic.vedic.jaimini import karakas as jaimini_karakas
from astrovedic import const

class TestCharaKarakas(unittest.TestCase):

    def setUp(self):
        """Set up a standard chart for testing."""
        self.date = Datetime('2023/10/26', '12:00', '+00:00') # Example date
        self.pos = GeoPos(51, 0) # Example location (London: lat 51, lon 0)
        self.chart = Chart(self.date, self.pos)
        # You might want to manually set planet longitudes here for precise testing
        # e.g., self.chart.getObject(const.SUN).lon = 182.5 # Libra 2.5 deg

    def test_standard_calculation(self):
        """Test Chara Karaka calculation for a known chart."""
        # Manually set longitudes for a predictable outcome
        # Example: Sun=10, Moon=25, Mars=5, Merc=15, Jup=20, Ven=28, Sat=2, Rahu=100
        self.chart.getObject(const.SUN).lon = 10.0
        self.chart.getObject(const.MOON).lon = 25.0
        self.chart.getObject(const.MARS).lon = 5.0
        self.chart.getObject(const.MERCURY).lon = 15.0
        self.chart.getObject(const.JUPITER).lon = 20.0
        self.chart.getObject(const.VENUS).lon = 28.0
        self.chart.getObject(const.SATURN).lon = 2.0
        self.chart.getObject(const.RAHU).lon = 100.0 # Rahu lon 100 -> Adjusted 260 -> Mod 30 = 20

        calculated_karakas = jaimini_karakas.calculate_chara_karakas(self.chart)

        # Expected based on degrees: Ven(28), Moon(25), Rahu(20, lon 260), Jup(20, lon 130), Merc(15), Sun(10), Mars(5), Sat(2)
        # Tie-break(Rahu/Jup): Rahu (260) > Jup (130), so Rahu ranks higher
        expected_karakas = {
            const.JAI_AK: const.VENUS,
            const.JAI_AMK: const.MOON,
            const.JAI_BK: const.RAHU,    # Corrected: Rahu wins tie-break vs Jupiter
            const.JAI_MK: const.JUPITER, # Corrected: Jupiter is after Rahu
            const.JAI_PK: const.MERCURY,
            const.JAI_GK: const.SUN,
            const.JAI_DK: const.MARS,
            const.JAI_SK: const.SATURN
        }
        self.assertDictEqual(calculated_karakas, expected_karakas, "Standard Karaka calculation failed.")

    def test_tie_breaking(self):
        """Test tie-breaking based on full longitude for AK."""
        # Set Sun and Venus to have the highest equal degree (e.g., 25 degrees)
        # Sun = Leo 25 -> 145.0
        # Venus = Virgo 25 -> 175.0
        self.chart.getObject(const.SUN).lon = 145.0 # 25 deg in sign
        self.chart.getObject(const.VENUS).lon = 175.0 # 25 deg in sign

        # Set others to lower degrees to ensure Sun/Venus tie is for AK/AmK
        self.chart.getObject(const.MOON).lon = 10.0   # 10 deg
        self.chart.getObject(const.MARS).lon = 15.0   # 15 deg
        self.chart.getObject(const.MERCURY).lon = 5.0    # 5 deg
        self.chart.getObject(const.JUPITER).lon = 20.0   # 20 deg
        self.chart.getObject(const.SATURN).lon = 12.0   # 12 deg
        self.chart.getObject(const.RAHU).lon = 100.0  # Rahu lon 100 -> Adjusted 260 -> 20 deg

        karakas = jaimini_karakas.calculate_chara_karakas(self.chart)

        # Tie-break between Sun (145) and Venus (175) for AK/AmK
        # Venus (175) has higher longitude than Sun (145), so Venus should be AK
        expected_ak = const.VENUS
        expected_amk = const.SUN

        self.assertEqual(karakas[const.JAI_AK], expected_ak, "Tie-breaking failed (Venus should be AK).")
        self.assertEqual(karakas[const.JAI_AMK], expected_amk, "Tie-breaking failed (Sun should be AmK).")

        # Verify a lower karaka as well
        # Jupiter (20 deg) or Rahu (20 deg, lon 260) should be BK.
        # Rahu wins tie-break
        expected_bk = const.RAHU
        self.assertEqual(karakas[const.JAI_BK], expected_bk, "Lower karaka check failed (Rahu should be BK).")


if __name__ == '__main__':
    unittest.main()
