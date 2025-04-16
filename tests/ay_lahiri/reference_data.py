"""
    Reference data for Lahiri ayanamsa tests
"""

# Reference date and location
REFERENCE_DATE = "2025/04/09"
REFERENCE_TIME = "20:51"
REFERENCE_TIMEZONE = "+05:30"
REFERENCE_LOCATION = "Bangalore, India"
REFERENCE_LAT = 12.9716
REFERENCE_LON = 77.5946

# Ashtakavarga reference data
ASHTAKAVARGA_REFERENCE = {
    "bhinnashtakavarga": {
        "Ascendant": [3, 6, 6, 3, 5, 2, 4, 2, 6, 5, 2, 5],
        "Sun": [3, 3, 3, 3, 4, 5, 5, 3, 4, 7, 3, 5],
        "Moon": [2, 7, 3, 4, 6, 4, 3, 3, 6, 5, 2, 4],
        "Mars": [2, 3, 2, 4, 5, 1, 6, 1, 3, 6, 3, 3],
        "Mercury": [4, 5, 3, 5, 4, 2, 5, 6, 3, 7, 3, 7],
        "Jupiter": [6, 4, 5, 6, 6, 2, 3, 5, 5, 5, 5, 4],
        "Venus": [2, 5, 5, 4, 3, 3, 5, 6, 6, 6, 3, 4],
        "Saturn": [3, 2, 3, 2, 4, 3, 5, 2, 4, 6, 2, 3]
    },
    "sarvashtakavarga": [22, 29, 24, 28, 32, 20, 32, 26, 31, 42, 21, 30]
}

# Bhavbala reference data
BHAVBALA_REFERENCE = {
    "bhavbala": [
        {"house": 1, "ranking": 3, "bhavadhipati": 461.76, "disha": 60.00, "drishti": 28.93, "total_pinda": 550.70, "rupas": 9.18},
        {"house": 2, "ranking": 6, "bhavadhipati": 423.87, "disha": 10.00, "drishti": 75.36, "total_pinda": 509.23, "rupas": 8.49},
        {"house": 3, "ranking": 10, "bhavadhipati": 438.08, "disha": 10.00, "drishti": 19.83, "total_pinda": 467.91, "rupas": 7.80},
        {"house": 4, "ranking": 11, "bhavadhipati": 250.81, "disha": 60.00, "drishti": 50.56, "total_pinda": 361.37, "rupas": 6.02},
        {"house": 5, "ranking": 12, "bhavadhipati": 250.81, "disha": 20.00, "drishti": 13.78, "total_pinda": 284.59, "rupas": 4.74},
        {"house": 6, "ranking": 7, "bhavadhipati": 438.08, "disha": 40.00, "drishti": 5.80, "total_pinda": 483.88, "rupas": 8.06},
        {"house": 7, "ranking": 9, "bhavadhipati": 423.87, "disha": 30.00, "drishti": 18.89, "total_pinda": 472.77, "rupas": 7.88},
        {"house": 8, "ranking": 5, "bhavadhipati": 461.76, "disha": 40.00, "drishti": 28.51, "total_pinda": 530.27, "rupas": 8.84},
        {"house": 9, "ranking": 8, "bhavadhipati": 435.11, "disha": 20.00, "drishti": 23.98, "total_pinda": 479.09, "rupas": 7.98},
        {"house": 10, "ranking": 1, "bhavadhipati": 546.76, "disha": 0.00, "drishti": 17.95, "total_pinda": 564.70, "rupas": 9.41},
        {"house": 11, "ranking": 4, "bhavadhipati": 407.97, "disha": 50.00, "drishti": 90.47, "total_pinda": 548.45, "rupas": 9.14},
        {"house": 12, "ranking": 2, "bhavadhipati": 435.11, "disha": 50.00, "drishti": 76.11, "total_pinda": 561.21, "rupas": 9.35}
    ]
}

# D1 Chart reference data
D1_CHART_REFERENCE = {
    "planets": [
        {"planet": "Ascendant", "longitude": 209.8423, "nakshatra": "Vishakha", "pada": 3, "nakshatra_lord": "Jupiter", "nakshatra_sublord": "Moon", "house": 1, "house_lord": "Venus"},
        {"planet": "Sun", "longitude": 355.9057, "nakshatra": "Revati", "pada": 3, "nakshatra_lord": "Mercury", "nakshatra_sublord": "Rahu", "house": 6, "house_lord": "Jupiter", "relationship": "Friend's House"},
        {"planet": "Moon", "longitude": 138.8496, "nakshatra": "P.Phalguni", "pada": 2, "nakshatra_lord": "Venus", "nakshatra_sublord": "Rahu", "house": 11, "house_lord": "Sun", "relationship": "Friend's House"},
        {"planet": "Mars", "longitude": 92.4202, "nakshatra": "Punarvasu", "pada": 4, "nakshatra_lord": "Jupiter", "nakshatra_sublord": "Rahu", "house": 10, "house_lord": "Moon", "relationship": "Friend's House", "dignity": "Debilitated"},
        {"planet": "Mercury", "longitude": 332.8196, "nakshatra": "P.Bhadrapada", "pada": 4, "nakshatra_lord": "Jupiter", "nakshatra_sublord": "Rahu", "house": 6, "house_lord": "Jupiter", "relationship": "Neutral", "dignity": "Debilitated"},
        {"planet": "Jupiter", "longitude": 53.1691, "nakshatra": "Mrigasira", "pada": 4, "nakshatra_lord": "Moon", "nakshatra_sublord": "Sun", "house": 8, "house_lord": "Venus", "relationship": "Enemy's House"},
        {"planet": "Venus", "longitude": 330.6416, "nakshatra": "P.Bhadrapada", "pada": 4, "nakshatra_lord": "Jupiter", "nakshatra_sublord": "Mars", "house": 6, "house_lord": "Jupiter", "relationship": "Neutral", "dignity": "Exalted"},
        {"planet": "Saturn", "longitude": 331.2942, "nakshatra": "P.Bhadrapada", "pada": 4, "nakshatra_lord": "Jupiter", "nakshatra_sublord": "Mars", "house": 6, "house_lord": "Jupiter", "relationship": "Neutral"},
        {"planet": "Rahu", "longitude": 332.0571, "nakshatra": "P.Bhadrapada", "pada": 4, "nakshatra_lord": "Jupiter", "nakshatra_sublord": "Rahu", "house": 6, "house_lord": "Jupiter", "relationship": "Friend's House"},
        {"planet": "Ketu", "longitude": 152.0571, "nakshatra": "U.Phalguni", "pada": 2, "nakshatra_lord": "Sun", "nakshatra_sublord": "Jupiter", "house": 12, "house_lord": "Mercury", "relationship": "Neutral"}
    ],
    "houses": [
        {"house": 1, "sign": "Libra", "owner": "Venus", "qualities": "Mas, Movable", "aspected_by": "Mars"},
        {"house": 2, "sign": "Scorpio", "owner": "Mars", "qualities": "Fem, Fixed", "aspected_by": "Jupiter"},
        {"house": 3, "sign": "Sagittarius", "owner": "Jupiter", "qualities": "Mas, Common", "aspected_by": "Saturn"},
        {"house": 4, "sign": "Capricorn", "owner": "Saturn", "qualities": "Fem, Movable", "aspected_by": "Mars, Jupiter"},
        {"house": 5, "sign": "Aquarius", "owner": "Saturn", "qualities": "Mas, Fixed", "aspected_by": "Moon, Mars"},
        {"house": 6, "sign": "Pisces", "owner": "Jupiter", "qualities": "Fem, Common", "aspected_by": ""},
        {"house": 7, "sign": "Aries", "owner": "Mars", "qualities": "Mas, Movable", "aspected_by": ""},
        {"house": 8, "sign": "Taurus", "owner": "Venus", "qualities": "Fem, Fixed", "aspected_by": "Saturn"},
        {"house": 9, "sign": "Gemini", "owner": "Mercury", "qualities": "Mas, Common", "aspected_by": ""},
        {"house": 10, "sign": "Cancer", "owner": "Moon", "qualities": "Fem, Movable", "aspected_by": ""},
        {"house": 11, "sign": "Leo", "owner": "Sun", "qualities": "Mas, Fixed", "aspected_by": ""},
        {"house": 12, "sign": "Virgo", "owner": "Mercury", "qualities": "Fem, Common", "aspected_by": "Sun, Mercury, Jupiter, Venus, Saturn"}
    ]
}

# Divisional Charts reference data
# D2 Chart
D2_CHART_REFERENCE = {
    "planets": [
        {"planet": "Ascendant", "longitude": 119.6845, "nakshatra": "Ashlesha", "pada": 4, "house": 1, "house_lord": "Moon"},
        {"planet": "Sun", "longitude": 141.4113, "nakshatra": "Purvaphalguni", "pada": 3, "house": 2, "house_lord": "Sun"},
        {"planet": "Moon", "longitude": 97.6993, "nakshatra": "Pushya", "pada": 2, "house": 1, "house_lord": "Moon"},
        {"planet": "Mars", "longitude": 94.9404, "nakshatra": "Pushya", "pada": 1, "house": 1, "house_lord": "Moon"},
        {"planet": "Mercury", "longitude": 95.0392, "nakshatra": "Pushya", "pada": 1, "house": 1, "house_lord": "Moon"},
        {"planet": "Jupiter", "longitude": 136.3983, "nakshatra": "Purvaphalguni", "pada": 1, "house": 2, "house_lord": "Sun"},
        {"planet": "Venus", "longitude": 91.2831, "nakshatra": "Punarvasu", "pada": 4, "house": 1, "house_lord": "Moon"},
        {"planet": "Saturn", "longitude": 92.5885, "nakshatra": "Punarvasu", "pada": 4, "house": 1, "house_lord": "Moon"},
        {"planet": "Rahu", "longitude": 94.1142, "nakshatra": "Pushya", "pada": 1, "house": 1, "house_lord": "Moon"},
        {"planet": "Ketu", "longitude": 94.1142, "nakshatra": "Pushya", "pada": 1, "house": 1, "house_lord": "Moon"}
    ]
}

# D9 Chart
D9_CHART_REFERENCE = {
    "planets": [
        {"planet": "Ascendant", "longitude": 88.5803, "nakshatra": "Punarvasu", "pada": 3, "house": 1, "house_lord": "Mercury"},
        {"planet": "Sun", "longitude": 323.251, "nakshatra": "P.Shadastaka", "pada": 1, "house": 9, "house_lord": "Saturn"},
        {"planet": "Moon", "longitude": 169.6446, "nakshatra": "Hasta", "pada": 3, "house": 4, "house_lord": "Mercury"},
        {"planet": "Mars", "longitude": 111.7818, "nakshatra": "Ashlesha", "pada": 2, "house": 2, "house_lord": "Moon"},
        {"planet": "Mercury", "longitude": 116.3743, "nakshatra": "Ashlesha", "pada": 3, "house": 2, "house_lord": "Moon"},
        {"planet": "Jupiter", "longitude": 118.5222, "nakshatra": "Ashlesha", "pada": 4, "house": 2, "house_lord": "Moon"},
        {"planet": "Venus", "longitude": 95.774, "nakshatra": "Pushya", "pada": 1, "house": 2, "house_lord": "Moon"},
        {"planet": "Saturn", "longitude": 101.6481, "nakshatra": "Pushya", "pada": 3, "house": 2, "house_lord": "Moon"},
        {"planet": "Rahu", "longitude": 108.514, "nakshatra": "Ashlesha", "pada": 1, "house": 2, "house_lord": "Moon"},
        {"planet": "Ketu", "longitude": 288.514, "nakshatra": "Shravana", "pada": 3, "house": 8, "house_lord": "Saturn"}
    ]
}

# Panchanga reference data
PANCHANGA_REFERENCE = {
    "tithi": "Dwadashi",
    "paksha": "Shukla Paksha",
    "nakshatra": "Purva Phalguni",
    "yoga": "Vriddhi",
    "karana": "Balava",
    "vara": "Budhawara",
    "moonsign": "Simha",
    "sunsign": "Meena",
    "surya_nakshatra": "Revati"
}

# Vimshottari Dasha reference data
VIMSHOTTARI_DASHA_REFERENCE = {
    "current_mahadasha": {
        "planet": "Venus",
        "start_date": "2016-12-30",
        "end_date": "2036-12-30",
        "balance": {
            "years": 11,
            "months": 8
        }
    },
    "current_antardasha": {
        "planet": "Mercury",
        "start_date": "2023-01-01",
        "end_date": "2025-11-01"
    },
    "antar_dasha_sequence": [
        {"planet": "Venus", "duration": "3y 4m", "start_date": "2016-12-30", "end_date": "2020-05-01"},
        {"planet": "Sun", "duration": "1y", "start_date": "2020-05-01", "end_date": "2021-05-01"},
        {"planet": "Moon", "duration": "1y 7m", "start_date": "2021-05-01", "end_date": "2022-12-31"},
        {"planet": "Mars", "duration": "1y 1m", "start_date": "2022-12-31", "end_date": "2024-03-01"},
        {"planet": "Rahu", "duration": "3y", "start_date": "2024-03-01", "end_date": "2027-03-02"},
        {"planet": "Jupiter", "duration": "2y 7m", "start_date": "2027-03-02", "end_date": "2029-10-31"},
        {"planet": "Saturn", "duration": "3y 1m", "start_date": "2029-10-31", "end_date": "2032-12-30"},
        {"planet": "Mercury", "duration": "2y 10m", "start_date": "2032-12-30", "end_date": "2035-10-31"},
        {"planet": "Ketu", "duration": "1y 1m", "start_date": "2035-10-31", "end_date": "2036-12-30"}
    ],
    "dasha_sequence": ["Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu"]
}
