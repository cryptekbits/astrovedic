"""
    Author: João Ventura <flatangleweb@gmail.com>
    
    
    This recipe shows sample code for handling 
    accidental dignities.

"""

from astrovedic import const
from astrovedic.chart import Chart
from astrovedic.datetime import Datetime
from astrovedic.geopos import GeoPos

from astrovedic.dignities import accidental
from astrovedic.dignities.accidental import AccidentalDignity


# Build a chart for a date and location
date = Datetime('2015/03/13', '17:00', '+00:00')
pos = GeoPos('38n32', '8w54')
chart = Chart(date, pos)

# Get some objects
obj = chart.get(const.VENUS)
sun = chart.get(const.SUN)

# Sun relation
relation = accidental.sunRelation(obj, sun)
print(relation)

# Augmenting or Diminishing light
light = accidental.light(obj, sun)
print(light)

# Orientality
orientality = accidental.orientality(obj, sun)
print(orientality)

# Haiz
haiz = accidental.haiz(obj, chart)
print(haiz)

# Build AccidentalDignity class
aDign = AccidentalDignity(obj, chart)

# Check for haiz
haiz = aDign.haiz()
print(haiz)

# List good aspects to benefics
asp = aDign.aspectBenefics()
print(asp)

# Get the accidental dignity score properties and its sum
scoreP = aDign.getScoreProperties()
score = aDign.score()
print(scoreP)
print(score)