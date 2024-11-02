"""
Module to provide a combined storage and data classes for specified data models.
The classes include pydantic validation of the data and storage of the data via
a selected storage class.


Available methods
'init_database'
    - method to define name and alias for the database
    - if needed host info and credentials can be added to the arguments

>>> configure_database(host="localhost", port=27017, username="user", password="pass")


available Dataclasses
- GeoNameDataClass, data class aimed at storing data from GeoNames website
- RetailLocationsDataClass, data class aimed at storing retail locations

avaialble fieldtypes (to be used to instantiatie specific dataclasses fields)
- PointField


Objects for discovery of available dataclasses
- AVAILABLE_MODELS: List with all data models names (as str)
- DatagardenModels: Class with all Datagarden models as class constant
	>>> DatagardenModels.DEMOGRAPHICS  # returns latest version of the Demographic
	                                     Pydantic data class

- DatagardenModelKeys: Class with all key classes for the Datagarden model classes.
	>>> keys = DatagardenModelKeys.DEMOGRAPHICS  # returns latest version of the
	                                               Demographic key class
	>>> keys.POPULATION  # returns the model key for the POPUPLATION field.

"""

from .models import DatagardenModelKeys, DatagardenModels


def get_values_from_class(cls: type):
	for key, value in vars(cls).items():
		if not key.startswith("__"):
			yield value


AVAILABLE_MODELS_NAMES = [
	klass.DATAGARDEN_MODEL_NAME for klass in get_values_from_class(DatagardenModelKeys)
]

AVAILABLE_MODELS = [klass for klass in get_values_from_class(DatagardenModels)]


__all__ = [
	"DatagardenModels",
	"DatagardenModelKeys",
	"AVAILABLE_MODELS",
	"AVAILABLE_MODELS_NAMES",
]
