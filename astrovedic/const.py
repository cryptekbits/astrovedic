"""
    This file is part of astrovedic - (C) FlatAngle
    Author: João Ventura (flatangleweb@gmail.com)
    Modified for Vedic Astrology


    This module defines the names of signs, objects, angles,
    houses and fixed-stars used in the library.

"""

# === Base constants === */

# Primitive qualities
HOT = 'Hot'
COLD = 'Cold'
DRY = 'Dry'
HUMID = 'Humid'

# Five Elements (Pancha Tattva)
FIRE = 'Fire'    # Agni
EARTH = 'Earth'  # Prithvi
AIR = 'Air'      # Vayu
WATER = 'Water'  # Jala
ETHER = 'Ether'  # Akasha

# Four Temperaments (Western) - Kept for backward compatibility
CHOLERIC = 'Choleric'
MELANCHOLIC = 'Melancholic'
SANGUINE = 'Sanguine'
PHLEGMATIC = 'Phlegmatic'

# Three Doshas (Ayurvedic)
VATA = 'Vata'      # Air + Ether
PITTA = 'Pitta'    # Fire + Water
KAPHA = 'Kapha'    # Earth + Water

# Genders
MASCULINE = 'Masculine'
FEMININE = 'Feminine'
NEUTRAL = 'Neutral'

# Factions - Kept for backward compatibility
DIURNAL = 'Diurnal'
NOCTURNAL = 'Nocturnal'

# Sun seasons
SPRING = 'Spring'
SUMMER = 'Summer'
AUTUMN = 'Autumn'
WINTER = 'Winter'

# Moon Quarters
MOON_FIRST_QUARTER = 'First Quarter'
MOON_SECOND_QUARTER = 'Second Quarter'
MOON_THIRD_QUARTER = 'Third Quarter'
MOON_LAST_QUARTER = 'Last Quarter'

# === Signs === */

ARIES = 'Aries'
TAURUS = 'Taurus'
GEMINI = 'Gemini'
CANCER = 'Cancer'
LEO = 'Leo'
VIRGO = 'Virgo'
LIBRA = 'Libra'
SCORPIO = 'Scorpio'
SAGITTARIUS = 'Sagittarius'
CAPRICORN = 'Capricorn'
AQUARIUS = 'Aquarius'
PISCES = 'Pisces'

# Sign modes
CARDINAL = 'Cardinal'
FIXED = 'Fixed'
MUTABLE = 'Mutable'

# Sign figures
SIGN_FIGURE_NONE = 'None'
SIGN_FIGURE_BEAST = 'Beast'
SIGN_FIGURE_HUMAN = 'Human'
SIGN_FIGURE_WILD = 'Wild'

# Sign fertilities
SIGN_FERTILE = 'Fertile'
SIGN_STERILE = 'Sterile'
SIGN_MODERATELY_FERTILE = 'Moderately Fertile'
SIGN_MODERATELY_STERILE = 'Moderately Sterile'

# === Objects === */

# Names
SUN = 'Sun'         # Surya
MOON = 'Moon'       # Chandra
MERCURY = 'Mercury' # Budha
VENUS = 'Venus'     # Shukra
MARS = 'Mars'       # Mangala
JUPITER = 'Jupiter' # Guru
SATURN = 'Saturn'   # Shani
URANUS = 'Uranus'
NEPTUNE = 'Neptune'
PLUTO = 'Pluto'
NO_PLANET = 'None'

# Nodes
RAHU = 'Rahu'       # North Node
KETU = 'Ketu'       # South Node
NORTH_NODE = RAHU
SOUTH_NODE = KETU

# Shadow Planets (Upagrah)
GULIKA = 'Gulika'   # Son of Saturn
MANDI = 'Mandi'     # Another name for Gulika
DHUMA = 'Dhuma'     # Smoky one
VYATIPATA = 'Vyatipata' # Calamity
PARIVESHA = 'Parivesha' # Halo
INDRACHAPA = 'Indrachapa' # Rainbow
UPAKETU = 'Upaketu' # Comet
KALA = 'Kala'       # Time/Death
MRITYU = 'Mrityu'   # Death
ARTHA_PRAHARA = 'Artha Prahara' # Wealth


# Asteroids
LILITH = 'Lilith'
CHIRON = 'Chiron'
PHOLUS = 'Pholus'
CERES = 'Ceres'
PALLAS = 'Pallas'
JUNO = 'Juno'
VESTA = 'Vesta'

# Special Points
SYZYGY = 'Syzygy'

# Object movement
DIRECT = 'Direct'
RETROGRADE = 'Retrograde'
STATIONARY = 'Stationary'

# Mean daily motions
MEAN_MOTION_SUN = 0.9833
MEAN_MOTION_MOON = 13.1833

# Object type
OBJ_PLANET = 'Planet'
OBJ_HOUSE = 'House'
OBJ_MOON_NODE = 'Moon Node'
OBJ_SHADOW_PLANET = 'Shadow Planet'
OBJ_FIXED_STAR = 'Fixed Star'
OBJ_ASTEROID = 'Asteroid'
OBJ_LUNATION = 'Lunation'
OBJ_GENERIC = 'Generic'
OBJ_SPECIAL_POINT = 'Special Point'

# List of Objs with Orbital properties for Orbital Class
LIST_ORBITAL_OBJ = [OBJ_PLANET, OBJ_ASTEROID]

# === Houses === */

HOUSE1 = 'House1'
HOUSE2 = 'House2'
HOUSE3 = 'House3'
HOUSE4 = 'House4'
HOUSE5 = 'House5'
HOUSE6 = 'House6'
HOUSE7 = 'House7'
HOUSE8 = 'House8'
HOUSE9 = 'House9'
HOUSE10 = 'House10'
HOUSE11 = 'House11'
HOUSE12 = 'House12'

# House conditions
ANGULAR = 'Angular'
SUCCEDENT = 'Succedent'
CADENT = 'Cadent'

# Benefic/Malefic houses
HOUSES_BENEFIC = [HOUSE1, HOUSE5, HOUSE11]
HOUSES_MALEFIC = [HOUSE6, HOUSE12]

# House Systems
HOUSES_PLACIDUS = 'Placidus'
HOUSES_KOCH = 'Koch'
HOUSES_PORPHYRIUS = 'Porphyrius'
HOUSES_REGIOMONTANUS = 'Regiomontanus'
HOUSES_CAMPANUS = 'Campanus'
HOUSES_EQUAL = 'Equal'
HOUSES_EQUAL_2 = 'Equal 2'
HOUSES_VEHLOW_EQUAL = 'Vehlow Equal'
HOUSES_WHOLE_SIGN = 'Whole Sign'
HOUSES_MERIDIAN = 'Meridian'
HOUSES_AZIMUTHAL = 'Azimuthal'
HOUSES_POLICH_PAGE = 'Polich Page'
HOUSES_ALCABITUS = 'Alcabitus'
HOUSES_MORINUS = 'Morinus'
HOUSES_DEFAULT = HOUSES_WHOLE_SIGN

# === Angles === */

ASC = 'Asc'
DESC = 'Desc'
MC = 'MC'
IC = 'IC'
VERTEX = 'Vertex'

# === Fixed Stars === */

STAR_ALGENIB = 'Algenib'
STAR_ALPHERATZ = 'Alpheratz'
STAR_ALGOL = 'Algol'
STAR_ALCYONE = 'Alcyone'
STAR_PLEIADES = STAR_ALCYONE
STAR_ALDEBARAN = 'Aldebaran'
STAR_RIGEL = 'Rigel'
STAR_CAPELLA = 'Capella'
STAR_BETELGEUSE = 'Betelgeuse'
STAR_SIRIUS = 'Sirius'
STAR_CANOPUS = 'Canopus'
STAR_CASTOR = 'Castor'
STAR_POLLUX = 'Pollux'
STAR_PROCYON = 'Procyon'
STAR_ASELLUS_BOREALIS = 'Asellus Borealis'
STAR_ASELLUS_AUSTRALIS = 'Asellus Australis'
STAR_ALPHARD = 'Alphard'
STAR_REGULUS = 'Regulus'
STAR_DENEBOLA = 'Denebola'
STAR_ALGORAB = 'Algorab'
STAR_SPICA = 'Spica'
STAR_ARCTURUS = 'Arcturus'
STAR_ALPHECCA = 'Alphecca'
STAR_ZUBEN_ELGENUBI = 'Zuben Elgenubi'
STAR_ZUBEN_ELSCHEMALI = 'Zuben Eshamali'
STAR_UNUKALHAI = 'Unukalhai'
STAR_AGENA = 'Agena'
STAR_RIGEL_CENTAURUS = 'Rigel Kentaurus'
STAR_ANTARES = 'Antares'
STAR_LESATH = 'Lesath'
STAR_VEGA = 'Vega'
STAR_ALTAIR = 'Altair'
STAR_DENEB_ALGEDI = 'Deneb Algedi'
STAR_FOMALHAUT = 'Fomalhaut'
STAR_DENEB_ADIGE = 'Deneb'  # Alpha-Cygnus
STAR_ACHERNAR = 'Achernar'

# === Aspects === */

# Western Aspects (kept for compatibility but should use Vedic aspects instead)
NO_ASPECT = -1
CONJUNCTION = 0
SEXTILE = 60
SQUARE = 90
TRINE = 120
OPPOSITION = 180

# Minor Aspects - Kept for backward compatibility
SEMISEXTILE = 30
SEMIQUINTILE = 36
SEMISQUARE = 45
QUINTILE = 72
SESQUIQUINTILE = 108
SESQUISQUARE = 135
BIQUINTILE = 144
QUINCUNX = 150

# Aspect movement
APPLICATIVE = 'Applicative'
SEPARATIVE = 'Separative'
EXACT = 'Exact'
NO_MOVEMENT = 'None'

# Aspect direction
DEXTER = 'Dexter'  # Right side
SINISTER = 'Sinister'  # Left side

# Aspect properties
ASSOCIATE = 'Associate'
DISSOCIATE = 'Dissociate'

# Aspect lists
MAJOR_ASPECTS = [0, 60, 90, 120, 180]
MINOR_ASPECTS = [30, 36, 45, 72, 108, 135, 144, 150]
ALL_ASPECTS = MAJOR_ASPECTS + MINOR_ASPECTS

# Vedic Aspects (Graha Drishti)
# All planets aspect the 7th house from their position
VEDIC_ASPECT_ALL = 7
# Mars aspects the 4th and 8th houses from its position
VEDIC_ASPECT_MARS = [4, 8]
# Jupiter aspects the 5th and 9th houses from its position
VEDIC_ASPECT_JUPITER = [5, 9]
# Saturn aspects the 3rd and 10th houses from its position
VEDIC_ASPECT_SATURN = [3, 10]

# Vedic Aspect Types
VEDIC_FULL_ASPECT = 'Full Aspect'  # 100% strength
VEDIC_THREE_QUARTER_ASPECT = 'Three-Quarter Aspect'  # 75% strength
VEDIC_HALF_ASPECT = 'Half Aspect'  # 50% strength
VEDIC_QUARTER_ASPECT = 'Quarter Aspect'  # 25% strength

# Rashi Drishti (Sign Aspects)
# Each sign aspects the 7th sign from it
RASHI_DRISHTI_ALL = 7
# Movable (Cardinal) signs also aspect the 4th and 10th signs
RASHI_DRISHTI_MOVABLE = [4, 10]
# Fixed signs also aspect the 5th and 9th signs
RASHI_DRISHTI_FIXED = [5, 9]
# Dual (Mutable) signs also aspect the 3rd and 11th signs
RASHI_DRISHTI_DUAL = [3, 11]

# === Ayanamsas / Sidereal Zodiac === */

# Vedic Ayanamsas
AY_LAHIRI = 'Ayanamsa Lahiri'  # Official ayanamsa of the Indian government
AY_RAMAN = 'Ayanamsa Raman'    # B.V. Raman's ayanamsa, a variant of Lahiri
AY_KRISHNAMURTI = 'Ayanamsa Krishnamurti'  # K.S. Krishnamurti's ayanamsa for KP system
AY_YUKTESHWAR = 'Ayanamsa Yukteshwar'  # Based on Sri Yukteshwar's book "The Holy Science"
AY_JN_BHASIN = 'Ayanamsa JN Bhasin'  # J.N. Bhasin's ayanamsa
AY_SURYASIDDHANTA = 'Ayanamsa Surya Siddhanta'  # Based on the ancient Surya Siddhanta text
AY_SURYASIDDHANTA_MSUN = 'Ayanamsa Surya Siddhanta (Mean Sun)'  # Variant using mean solar position
AY_ARYABHATA = 'Ayanamsa Aryabhata'  # Based on Aryabhata's work
AY_ARYABHATA_MSUN = 'Ayanamsa Aryabhata (Mean Sun)'  # Variant using mean solar position
AY_SS_REVATI = 'Ayanamsa SS Revati'  # Surya Siddhanta with Revati at 0° Aries
AY_SS_CITRA = 'Ayanamsa SS Citra'  # Surya Siddhanta with Citra at 0° Libra
AY_TRUE_CITRA = 'Ayanamsa True Citra'  # True Citra ayanamsa with Spica at 0° Libra
AY_TRUE_REVATI = 'Ayanamsa True Revati'  # True Revati ayanamsa with Revati at 0° Aries
AY_TRUE_PUSHYA = 'Ayanamsa True Pushya'  # True Pushya ayanamsa
AY_TRUE_MULA = 'Ayanamsa True Mula'  # True Mula ayanamsa
AY_ARYABHATA_522 = 'Ayanamsa Aryabhata 522'  # Aryabhata's ayanamsa for the year 522 CE
AY_TRUE_SHEORAN = 'Ayanamsa True Sheoran'  # True Sheoran ayanamsa

# Default Ayanamsas for different systems
AY_DEFAULT_VEDIC = AY_LAHIRI
AY_DEFAULT_KP = AY_KRISHNAMURTI

# === Jaimini Constants ===

# Chara Karakas (Temporary Significators)
JAI_AK = 'Atma Karaka'       # Soul Significator
JAI_AMK = 'Amatya Karaka'    # Minister Significator
JAI_BK = 'Bhratri Karaka'    # Sibling Significator
JAI_MK = 'Matri Karaka'      # Mother Significator
JAI_PK = 'Putra Karaka'      # Children Significator
JAI_GK = 'Gnati Karaka'      # Relative/Obstacle Significator
JAI_DK = 'Dara Karaka'       # Spouse Significator
JAI_SK = 'Strī Karaka'       # Alternate Spouse/Co-born Significator (often same as DK or lowest degree)

# List of Chara Karaka ranks (in order)
LIST_CHARA_KARAKAS = [
    JAI_AK, JAI_AMK, JAI_BK, JAI_MK, JAI_PK, JAI_GK, JAI_DK, JAI_SK
]

# Planets considered for Chara Karakas (Sun to Saturn + Rahu)
CHARA_KARAKA_PLANETS = [
    SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN, RAHU
]


# === Some Lists === */

LIST_SIGNS = [
    ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO, LIBRA,
    SCORPIO, SAGITTARIUS, CAPRICORN, AQUARIUS, PISCES
]

LIST_OBJECTS = [
    SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN,
    URANUS, NEPTUNE, PLUTO, LILITH, CHIRON, RAHU, KETU, SYZYGY
]

# Traditional objects list - Kept for backward compatibility
LIST_OBJECTS_TRADITIONAL = [
    SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN,
    RAHU, KETU, SYZYGY
]

# Modern objects list - Kept for backward compatibility
LIST_OBJECTS_MODERN = [
    SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN, NEPTUNE, URANUS, PLUTO,
    RAHU, KETU, SYZYGY
]

LIST_OBJECTS_VEDIC = [
    SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN, URANUS, NEPTUNE, PLUTO, RAHU, KETU
]

LIST_SHADOW_PLANETS = [
    GULIKA, MANDI, DHUMA, VYATIPATA, PARIVESHA, INDRACHAPA, UPAKETU,
    KALA, MRITYU, ARTHA_PRAHARA
]

LIST_VEDIC_BODIES = [
    URANUS, NEPTUNE, PLUTO
]

LIST_SEVEN_PLANETS = [
    SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN
]

"""MH on 2018/3/3 - List of 10 plantes for modern astrology"""
LIST_TEN_PLANETS = [
    SUN, MOON, MERCURY, VENUS, MARS, JUPITER, SATURN, NEPTUNE, URANUS, PLUTO
]

"""MH on 2018/3/4 - List of aspecting planets"""

LIST_ASP_PLANETS = [
    SUN, MERCURY, VENUS, MARS, JUPITER, SATURN, NEPTUNE, URANUS, PLUTO, NORTH_NODE, SOUTH_NODE
]

LIST_HOUSES = [
    HOUSE1, HOUSE2, HOUSE3, HOUSE4, HOUSE5, HOUSE6,
    HOUSE7, HOUSE8, HOUSE9, HOUSE10, HOUSE11, HOUSE12,
]

LIST_ANGLES = [
    ASC, MC, DESC, IC, VERTEX
]

LIST_ASTEROIDS = [
    LILITH,
    CHIRON,
    PHOLUS,
    CERES,
    PALLAS,
    JUNO,
    VESTA
]

LIST_MOON_NODES = [
    RAHU,
    KETU
]

LIST_FIXED_STARS = [
    STAR_ALGENIB, STAR_ALPHERATZ, STAR_ALGOL, STAR_ALCYONE,
    STAR_PLEIADES, STAR_ALDEBARAN, STAR_RIGEL, STAR_CAPELLA,
    STAR_BETELGEUSE, STAR_SIRIUS, STAR_CANOPUS, STAR_CASTOR,
    STAR_POLLUX, STAR_PROCYON, STAR_ASELLUS_BOREALIS,
    STAR_ASELLUS_AUSTRALIS, STAR_ALPHARD, STAR_REGULUS,
    STAR_DENEBOLA, STAR_ALGORAB, STAR_SPICA, STAR_ARCTURUS,
    STAR_ALPHECCA, STAR_ZUBEN_ELSCHEMALI, STAR_UNUKALHAI,
    STAR_AGENA, STAR_RIGEL_CENTAURUS, STAR_ANTARES,
    STAR_LESATH, STAR_VEGA, STAR_ALTAIR, STAR_DENEB_ALGEDI,
    STAR_FOMALHAUT, STAR_DENEB_ADIGE, STAR_ACHERNAR,
]

""" Taken from https://github.com/lightflicker/flatlib"""

"""MH on 2018/3/6 - List of Positive Aspects"""
LIST_ASPECTS_POS = [
    SEXTILE, TRINE
]

"""MH on 2018/3/6 - List of Negative Aspects"""
LIST_ASPECTS_NEG = [
    SQUARE, OPPOSITION
]

"""MH on 2018/3/6 - List of tight orbs"""

# Asteroids Orbs at http://straightwoo.com/2016/05/23/asteroids-astrology-use/
# Donna Cunningham’s system of giving 10 degrees

LIST_ORBS_TIGHT = {
    NO_PLANET: 0,
    SUN: 15,
    MOON: 12,
    MERCURY: 7,
    VENUS: 7,
    MARS: 8,
    JUPITER: 9,
    SATURN: 9,
    URANUS: 5,
    NEPTUNE: 5,
    PLUTO: 5,
    LILITH: 5,
    CHIRON: 5,
    NORTH_NODE: 12,
    SOUTH_NODE: 12,
    SYZYGY: 0,
    PHOLUS: 5,
    CERES: 5,
    JUNO: 5,
    VESTA: 5,
    PALLAS: 5,
}

"""MH on 2018/3/6 - List of wide orbs"""
LIST_ORBS_WIDE = {
    NO_PLANET: 0,
    SUN: 5,
    MOON: 4,
    MERCURY: 2,
    VENUS: 2,
    MARS: 3,
    JUPITER: 3,
    SATURN: 3,
    URANUS: 2,
    NEPTUNE: 1,
    PLUTO: 3,
    LILITH: 1,
    CHIRON: 1,
    NORTH_NODE: 2,
    SOUTH_NODE: 2,
    SYZYGY: 0,
    PHOLUS: 1,
    CERES: 1,
    JUNO: 1,
    VESTA: 1,
    PALLAS: 1
}

LIST_ORBS = LIST_ORBS_TIGHT

"""MH on 2018/3/18"""
LIST_RULERS = {
    ARIES: MARS,
    TAURUS: VENUS,
    GEMINI: MERCURY,
    CANCER: MOON,
    LEO: SUN,
    VIRGO: MERCURY,
    LIBRA: VENUS,
    SCORPIO: PLUTO,
    SAGITTARIUS: JUPITER,
    CAPRICORN: SATURN,
    AQUARIUS: URANUS,
    PISCES: NEPTUNE
}

"""MH on 2018/3/9 - Time constants"""
MINUTE = 0.00069444440305233
HOUR = 0.04166666651144624

"""Alstrat on 2020/04/03 - House offsets"""

TRADITIONAL_HOUSE_OFFSET = -5
MODERN_HOUSE_OFFSET = 0
