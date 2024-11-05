from typing import Any, Union, get_args, get_origin

from pydantic import BaseModel


class DataGardenModelLegends:
	DATAGARDEN_MODEL_VERSION: str = "Version of the data model."


class Legend:
	"""A class to handle model and field legends/descriptions for DataGarden models.

	This class provides functionality to extract and manage descriptions and metadata
	from DataGardenSubModel classes and their fields, creating a hierarchical structure
	of legends.

	Parameters to instantiate the class:
	------------------------------------
	model : type[DataGardenSubModel]
	    The model class for which the Legend class is created

	    there are more parameters, but they are only used by the Legend class itself
		as they are needed to describe the nested models.

	    As a user of the Legend class, you only need instantiate the class with a
	    DatagardenModel class.

	    >>> legends = Legend(model=DemograpicsV1)
	    >>> legends
	    Data model DemographicsV1 : DemographicsV1 (with attributes [population,
	    life_expectancy, mortality, fertility, education])

	    Now you can access information about the models attributes

	    >>> legends.population
	    Data model population : Population indicators for the region.  (with attributes
		[by_age_gender, total, total_male, total_female, male_to_female_ratio, density,
	    change, natural_change, natural_change_rate])

	    or the nested attributes

	    >>> legends.population.total
	    Attribute total : Total population. In number of individuals.

	    or the type of the attribute

	    >>> legends.population.total.type
	    <class 'int'>


	Instance Attributes
	-------------------
	attribute : str
	    Name of the attribute or model
	type : str
	    Type of the attribute
	legend : str
	    Description of the model or attribute

	Methods
	-------
	attributes
	    Get list of all field names in the legend
	has_attributes
	    Check if the legend has any attributes
	"""

	def __init__(
		self,
		model: type["DataGardenSubModel"] | None = None,  # type: ignore  # noqa: F821
		description: str | None = None,
		attribute: str | None = None,
		attribute_type: Any | None = None,
	):
		self.model = model
		self.attribute = attribute or (model.__name__ if model else None)
		self.field_legends = self._field_to_legends() if model else {}
		self.type = attribute_type or model

		if description:
			self.legend = description
		elif model:
			self.legend = getattr(model(), "MODEL_LEGEND", model.__name__)
		else:
			self.legend = "No legend provided in the data model"

	def __repr__(self) -> str:
		if self.field_legends:
			return (
				f"Data model <{self.attribute}> : {self.legend} "
				f"(with attributes [{', '.join(self.field_legends.keys())}])"
			)
		return f"Attribute <{self.attribute}> : {self.legend}"

	def is_base_model(self, annotation):
		if isinstance(annotation, type) and issubclass(annotation, BaseModel):
			return True
		if get_origin(annotation) is Union:
			return any(self.is_base_model(arg) for arg in get_args(annotation))
		return False

	def _field_to_legends(self) -> dict[str, "Legend"]:
		legends: dict[str, Legend] = {}
		if not self.model:
			return legends
		for field_name, field_info in self.model.model_fields.items():
			if field_name in ("datagarden_model_version", "MODEL_LEGEND"):
				continue
			actual_class = None
			if self.is_base_model(field_info.annotation):
				if field_info.annotation:
					annotation = field_info.annotation
					if get_origin(annotation) is Union:
						# Get the first non-None type from Union (Optional)
						annotation = next(
							arg for arg in get_args(annotation) if arg is not type(None)
						)
					# If it's a class, use it directly
					actual_class = (
						annotation
						if isinstance(annotation, type)
						else get_args(annotation)[0]
					)
				attribute_type = actual_class
			else:
				annotation = field_info.annotation
				if get_origin(annotation) is Union:
					# Get the first non-None type from Union (Optional)
					annotation = next(
						arg for arg in get_args(annotation) if arg is not type(None)
					)
				# If it's a class, use it directly
				attr_class = (
					annotation
					if isinstance(annotation, type)
					else get_args(annotation)[0]
				)
				attribute_type = attr_class

			legends[field_name] = Legend(
				model=actual_class,
				description=field_info.description,
				attribute=field_name,
				attribute_type=attribute_type,
			)
		return legends

	def __getattr__(self, name: str):
		# Check if the attribute exists in field_legends
		if name in self.field_legends:
			return self.field_legends[name]
		# Raise AttributeError if the attribute doesn't exist
		raise AttributeError(
			f"'{self.__class__.__name__}' object has no attribute '{name}'"
		)

	@property
	def attributes(self) -> list[str]:
		return list(self.field_legends.keys())

	@property
	def has_attributes(self) -> bool:
		return bool(self.attributes)

	@property
	def attributes_as_str(self) -> str:
		return ", ".join(list(self.field_legends.keys()))

	@property
	def type_as_str(self) -> str:
		return self.type.__name__ if self.type else ""
