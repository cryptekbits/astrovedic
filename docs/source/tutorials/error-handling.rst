Error Handling in Flatlib
=======================

Flatlib includes robust error handling to ensure that calculations don't fail unexpectedly.
This tutorial explains how error handling works in flatlib and how to use it effectively.

Object Creation and Validation
-----------------------------

When creating astronomical objects, flatlib validates that all required attributes are present.
If any required attributes are missing, flatlib will:

1. Log a warning message
2. Add default values for the missing attributes
3. Continue with the calculation

This ensures that your code won't crash due to missing attributes.

Example::

   >>> from flatlib.factory import AstronomicalObjectFactory
   >>> from flatlib import const
   >>> 
   >>> # Create an object with missing attributes
   >>> obj_data = {'id': const.SUN, 'lon': 45.0}  # Missing 'lat'
   >>> obj = AstronomicalObjectFactory.create_object(obj_data)
   >>> 
   >>> # The object is created with default values for missing attributes
   >>> print(obj.lat)  # 0.0
   >>> print(obj.sign)  # Taurus (calculated from lon)
   >>> print(obj.signlon)  # 15.0 (calculated from lon)

Calculation Errors
-----------------

When performing astronomical calculations, flatlib handles errors gracefully:

1. If a calculation fails, flatlib logs an error message
2. It returns a valid object with default values
3. Your code can continue running without crashing

Example::

   >>> from flatlib.chart import Chart
   >>> from flatlib.datetime import Datetime
   >>> from flatlib.geopos import GeoPos
   >>> 
   >>> # Create a chart with a non-existent object
   >>> date = Datetime('2015/03/13', '17:00', '+00:00')
   >>> pos = GeoPos('38n32', '8w54')
   >>> chart = Chart(date, pos, IDs=[const.SUN, 'NonExistentObject'])
   >>> 
   >>> # We can still access the valid object
   >>> sun = chart.getObject(const.SUN)
   >>> print(sun)  # <Sun Pisces +22:47:25 +00:59:51>
   >>> 
   >>> # And we can access the invalid object (it has default values)
   >>> invalid_obj = chart.getObject('NonExistentObject')
   >>> print(invalid_obj)  # <NonExistentObject Aries +00:00:00 +00:00:00>

Logging
-------

Flatlib uses Python's logging module to log errors and warnings. You can configure the logging
level to control how much information is logged::

   >>> import logging
   >>> logging.basicConfig(level=logging.INFO)
   >>> logger = logging.getLogger("flatlib")
   >>> logger.setLevel(logging.DEBUG)  # Show all messages

Factory Pattern
--------------

Flatlib uses a factory pattern to create objects with proper validation::

   >>> from flatlib.factory import AstronomicalObjectFactory
   >>> from flatlib import const
   >>> 
   >>> # Create a planet
   >>> planet_data = {
   ...     'id': const.JUPITER,
   ...     'lon': 120.0,
   ...     'lat': 1.5,
   ...     'lonspeed': 0.1,
   ...     'latspeed': 0.0
   ... }
   >>> jupiter = AstronomicalObjectFactory.create_object(planet_data, const.OBJ_PLANET)
   >>> 
   >>> # Create a house
   >>> house_data = {
   ...     'id': const.HOUSE1,
   ...     'lon': 0.0,
   ...     'lat': 0.0,
   ...     'size': 30.0
   ... }
   >>> house1 = AstronomicalObjectFactory.create_object(house_data, const.OBJ_HOUSE)

Interfaces
---------

Flatlib defines interfaces for different types of objects to ensure consistency::

   >>> from flatlib.interfaces import IAstronomicalObject, IOrbitalObject, IHouse, IFixedStar
   >>> 
   >>> # All astronomical objects implement IAstronomicalObject
   >>> # Planets implement IOrbitalObject
   >>> # Houses implement IHouse
   >>> # Fixed stars implement IFixedStar

This ensures that all objects have the required attributes and methods.
