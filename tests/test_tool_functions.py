#!/usr/bin/env python3
"""
Test Tool Functions

This script tests the tool functions in flatlib.
"""

import unittest
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from flatlib import angle
from flatlib import aspects
from flatlib.dignities import essential

# Define utility functions that might not be directly exposed in the modules
def normalize_longitude(longitude):
    """Normalize longitude to [0, 360) range"""
    return angle.norm(longitude)

def get_sign_from_longitude(longitude):
    """Get sign from longitude"""
    lon = normalize_longitude(longitude)
    sign_num = int(lon / 30)
    return const.LIST_SIGNS[sign_num]

def get_sign_number(sign):
    """Get sign number (1-12) from sign name"""
    return const.LIST_SIGNS.index(sign) + 1

def get_sign_from_number(num):
    """Get sign name from sign number (1-12)"""
    return const.LIST_SIGNS[num - 1]

# Define essential dignity functions
def getEssentialDignity(obj):
    """Get essential dignity of an object"""
    if essential.ruler(obj):
        return "Ruler"
    elif essential.exaltation(obj):
        return "Exaltation"
    elif essential.triplicity(obj):
        return "Triplicity"
    elif essential.term(obj):
        return "Term"
    elif essential.face(obj):
        return "Face"
    elif essential.detriment(obj):
        return "Detriment"
    elif essential.fall(obj):
        return "Fall"
    else:
        return "Peregrine"

def getEssentialDignityScore(obj):
    """Get essential dignity score of an object"""
    score = 0
    if essential.ruler(obj):
        score += 5
    if essential.exaltation(obj):
        score += 4
    if essential.triplicity(obj):
        score += 3
    if essential.term(obj):
        score += 2
    if essential.face(obj):
        score += 1
    if essential.detriment(obj):
        score -= 5
    if essential.fall(obj):
        score -= 4
    return score

def inRuler(obj):
    """Check if an object is in its ruler"""
    return essential.ruler(obj)

def inExaltation(obj):
    """Check if an object is in its exaltation"""
    return essential.exaltation(obj)

def inTriplicity(obj):
    """Check if an object is in its triplicity"""
    return essential.triplicity(obj)

def inTerm(obj):
    """Check if an object is in its term"""
    return essential.term(obj)

def inFace(obj):
    """Check if an object is in its face"""
    return essential.face(obj)

def inDetriment(obj):
    """Check if an object is in its detriment"""
    return essential.detriment(obj)

def inFall(obj):
    """Check if an object is in its fall"""
    return essential.fall(obj)

# Define aspect functions
def getAspect(obj1, obj2):
    """Get aspect between two objects"""
    return aspects.getAspect(obj1, obj2, const.MAJOR_ASPECTS)

def isAspecting(obj1, obj2, aspect_type=None):
    """Check if two objects are aspecting"""
    if aspect_type:
        return aspects.isAspecting(obj1, obj2, [aspect_type])
    else:
        return aspects.isAspecting(obj1, obj2, const.MAJOR_ASPECTS)

def getAspects(objects):
    """Get all aspects between objects"""
    result = []
    for i, obj1 in enumerate(objects):
        for obj2 in objects[i+1:]:
            aspect = getAspect(obj1, obj2)
            if aspect['type'] != 'None':
                result.append({
                    'p1': obj1.id,
                    'p2': obj2.id,
                    'type': aspect['type'],
                    'orb': aspect['orb']
                })
    return result


class TestAngleFunctions(unittest.TestCase):
    """Test case for angle functions"""

    def test_norm(self):
        """Test angle.norm function"""
        # Test with various angles
        test_cases = [
            (0, 0),
            (30, 30),
            (360, 0),
            (361, 1),
            (720, 0),
            (-1, 359),
            (-30, 330),
            (-360, 0)
        ]

        for input_angle, expected_output in test_cases:
            result = angle.norm(input_angle)
            self.assertEqual(result, expected_output)

            # Print the result for reference
            print(f"angle.norm({input_angle}) = {result}")

    def test_znorm(self):
        """Test angle.znorm function"""
        # Test with various angles
        test_cases = [
            (0, 0),
            (30, 30),
            (90, 90),
            (180, 180),
            (181, -179),
            (270, -90),
            (360, 0),
            (-1, -1),
            (-30, -30),
            (-180, 180),  # Note: flatlib's znorm treats -180 as 180
            (-181, 179),
            (-270, 90),
            (-360, 0)
        ]

        for input_angle, expected_output in test_cases:
            result = angle.znorm(input_angle)
            self.assertEqual(result, expected_output)

            # Print the result for reference
            print(f"angle.znorm({input_angle}) = {result}")

    def test_distance(self):
        """Test angle.distance function"""
        # Test with various angles
        test_cases = [
            (0, 0, 0),
            (0, 30, 30),
            (30, 0, 30),
            (0, 180, 180),
            (0, 181, 179),
            (0, 359, 1),
            (359, 0, 1),
            (90, 270, 180)
        ]

        for angle1, angle2, expected_output in test_cases:
            result = angle.distance(angle1, angle2)
            self.assertEqual(result, expected_output)

            # Print the result for reference
            print(f"angle.distance({angle1}, {angle2}) = {result}")

    def test_closestdistance(self):
        """Test angle.closestdistance function"""
        # Test with various angles
        test_cases = [
            (0, 0, 0),
            (0, 30, 30),
            (30, 0, -30),
            (0, 180, 180),
            (0, 181, -179),
            (0, 359, -1),
            (359, 0, 1),
            (90, 270, 180)
        ]

        for angle1, angle2, expected_output in test_cases:
            result = angle.closestdistance(angle1, angle2)
            self.assertEqual(result, expected_output)

            # Print the result for reference
            print(f"angle.closestdistance({angle1}, {angle2}) = {result}")


class TestUtilsFunctions(unittest.TestCase):
    """Test case for utils functions"""

    def test_normalize_longitude(self):
        """Test utils.normalize_longitude function"""
        # Test with various longitudes
        test_cases = [
            (0, 0),
            (30, 30),
            (360, 0),
            (361, 1),
            (720, 0),
            (-1, 359),
            (-30, 330),
            (-360, 0)
        ]

        for input_lon, expected_output in test_cases:
            result = normalize_longitude(input_lon)
            self.assertEqual(result, expected_output)

            # Print the result for reference
            print(f"utils.normalize_longitude({input_lon}) = {result}")

    def test_get_sign_from_longitude(self):
        """Test utils.get_sign_from_longitude function"""
        # Test with various longitudes
        test_cases = [
            (0, const.ARIES),
            (15, const.ARIES),
            (29.99, const.ARIES),
            (30, const.TAURUS),
            (45, const.TAURUS),
            (60, const.GEMINI),
            (90, const.CANCER),
            (120, const.LEO),
            (150, const.VIRGO),
            (180, const.LIBRA),
            (210, const.SCORPIO),
            (240, const.SAGITTARIUS),
            (270, const.CAPRICORN),
            (300, const.AQUARIUS),
            (330, const.PISCES),
            (359.99, const.PISCES)
        ]

        for input_lon, expected_output in test_cases:
            result = get_sign_from_longitude(input_lon)
            self.assertEqual(result, expected_output)

            # Print the result for reference
            print(f"utils.get_sign_from_longitude({input_lon}) = {result}")

    def test_get_sign_number(self):
        """Test utils.get_sign_number function"""
        # Test with various signs
        test_cases = [
            (const.ARIES, 1),
            (const.TAURUS, 2),
            (const.GEMINI, 3),
            (const.CANCER, 4),
            (const.LEO, 5),
            (const.VIRGO, 6),
            (const.LIBRA, 7),
            (const.SCORPIO, 8),
            (const.SAGITTARIUS, 9),
            (const.CAPRICORN, 10),
            (const.AQUARIUS, 11),
            (const.PISCES, 12)
        ]

        for input_sign, expected_output in test_cases:
            result = get_sign_number(input_sign)
            self.assertEqual(result, expected_output)

            # Print the result for reference
            print(f"utils.get_sign_number({input_sign}) = {result}")

    def test_get_sign_from_number(self):
        """Test utils.get_sign_from_number function"""
        # Test with various sign numbers
        test_cases = [
            (1, const.ARIES),
            (2, const.TAURUS),
            (3, const.GEMINI),
            (4, const.CANCER),
            (5, const.LEO),
            (6, const.VIRGO),
            (7, const.LIBRA),
            (8, const.SCORPIO),
            (9, const.SAGITTARIUS),
            (10, const.CAPRICORN),
            (11, const.AQUARIUS),
            (12, const.PISCES)
        ]

        for input_num, expected_output in test_cases:
            result = get_sign_from_number(input_num)
            self.assertEqual(result, expected_output)

            # Print the result for reference
            print(f"utils.get_sign_from_number({input_num}) = {result}")


class TestAspectsFunctions(unittest.TestCase):
    """Test case for aspects functions"""

    def setUp(self):
        """Set up test case"""
        # Create a chart for testing
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos)

    def test_getAspect(self):
        """Test aspects.getAspect function"""
        # Get two planets
        sun = self.chart.getObject(const.SUN)
        moon = self.chart.getObject(const.MOON)

        # Get the aspect between them
        aspect = getAspect(sun, moon)

        # Check that the aspect is a dictionary
        self.assertIsInstance(aspect, dict)

        # Check that the aspect has the required keys
        self.assertIn('type', aspect)
        self.assertIn('orb', aspect)
        self.assertIn('diff', aspect)

        # Print the aspect for reference
        print(f"Aspect between Sun and Moon:")
        print(f"  Type: {aspect['type']}")
        print(f"  Orb: {aspect['orb']:.2f}°")
        print(f"  Diff: {aspect['diff']:.2f}°")

    def test_isAspecting(self):
        """Test aspects.isAspecting function"""
        # Get two planets
        sun = self.chart.getObject(const.SUN)
        moon = self.chart.getObject(const.MOON)

        # Check if they are aspecting
        is_aspecting = isAspecting(sun, moon)

        # Print the result for reference
        print(f"Sun and Moon are aspecting: {is_aspecting}")

        # Test with specific aspect types
        for aspect_type in const.MAJOR_ASPECTS:
            is_aspecting = isAspecting(sun, moon, aspect_type)
            print(f"Sun and Moon are in {aspect_type}: {is_aspecting}")

    def test_getAspects(self):
        """Test aspects.getAspects function"""
        # Get the aspects between all planets
        all_aspects = getAspects(self.chart.objects)

        # Check that the aspects is a list
        self.assertIsInstance(all_aspects, list)

        # Print the aspects for reference
        print(f"All aspects in the chart:")
        for aspect in all_aspects:
            print(f"  {aspect['p1']} {aspect['type']} {aspect['p2']} (Orb: {aspect['orb']:.2f}°)")


class TestEssentialDignities(unittest.TestCase):
    """Test case for essential dignities functions"""

    def setUp(self):
        """Set up test case"""
        # Create a chart for testing
        date = Datetime('2025/04/09', '20:51', '+05:30')
        pos = GeoPos(12.9716, 77.5946)  # Bangalore, India
        self.chart = Chart(date, pos)

    def test_getEssentialDignity(self):
        """Test essential.getEssentialDignity function"""
        # Get the essential dignity of each planet
        for obj_id in const.LIST_OBJECTS_VEDIC:
            obj = self.chart.getObject(obj_id)
            dignity = getEssentialDignity(obj)

            # Check that the dignity is a string
            self.assertIsInstance(dignity, str)

            # Print the dignity for reference
            print(f"Essential dignity of {obj_id}: {dignity}")

    def test_getEssentialDignityScore(self):
        """Test essential.getEssentialDignityScore function"""
        # Get the essential dignity score of each planet
        for obj_id in const.LIST_OBJECTS_VEDIC:
            obj = self.chart.getObject(obj_id)
            score = getEssentialDignityScore(obj)

            # Check that the score is a number
            self.assertIsInstance(score, (int, float))

            # Print the score for reference
            print(f"Essential dignity score of {obj_id}: {score}")

    def test_inRuler(self):
        """Test essential.inRuler function"""
        # Test with various planets and signs
        for obj_id in const.LIST_OBJECTS_VEDIC:
            obj = self.chart.getObject(obj_id)
            is_ruler = inRuler(obj)

            # Print the result for reference
            print(f"{obj_id} in ruler: {is_ruler}")

    def test_inExaltation(self):
        """Test essential.inExaltation function"""
        # Test with various planets and signs
        for obj_id in const.LIST_OBJECTS_VEDIC:
            obj = self.chart.getObject(obj_id)
            is_exalted = inExaltation(obj)

            # Print the result for reference
            print(f"{obj_id} in exaltation: {is_exalted}")

    def test_inTriplicity(self):
        """Test essential.inTriplicity function"""
        # Test with various planets and signs
        for obj_id in const.LIST_OBJECTS_VEDIC:
            obj = self.chart.getObject(obj_id)
            is_triplicity = inTriplicity(obj)

            # Print the result for reference
            print(f"{obj_id} in triplicity: {is_triplicity}")

    def test_inTerm(self):
        """Test essential.inTerm function"""
        # Test with various planets and signs
        for obj_id in const.LIST_OBJECTS_VEDIC:
            obj = self.chart.getObject(obj_id)
            is_term = inTerm(obj)

            # Print the result for reference
            print(f"{obj_id} in term: {is_term}")

    def test_inFace(self):
        """Test essential.inFace function"""
        # Test with various planets and signs
        for obj_id in const.LIST_OBJECTS_VEDIC:
            obj = self.chart.getObject(obj_id)
            is_face = inFace(obj)

            # Print the result for reference
            print(f"{obj_id} in face: {is_face}")

    def test_inDetriment(self):
        """Test essential.inDetriment function"""
        # Test with various planets and signs
        for obj_id in const.LIST_OBJECTS_VEDIC:
            obj = self.chart.getObject(obj_id)
            is_detriment = inDetriment(obj)

            # Print the result for reference
            print(f"{obj_id} in detriment: {is_detriment}")

    def test_inFall(self):
        """Test essential.inFall function"""
        # Test with various planets and signs
        for obj_id in const.LIST_OBJECTS_VEDIC:
            obj = self.chart.getObject(obj_id)
            is_fall = inFall(obj)

            # Print the result for reference
            print(f"{obj_id} in fall: {is_fall}")


if __name__ == '__main__':
    unittest.main()
