from typing import Union, get_args, get_origin

from pydantic import BaseModel, Field, model_validator


class DataGardenModelLegends:
	DATAGARDEN_MODEL_VERSION = "Version of the data model."


class DataGardenSubModel(BaseModel):
	class Meta:
		exclude_fields_in_has_values_check: list[str] = []

	def has_values(self, data: BaseModel | None = None) -> bool:
		# Recursively check if any field has a non-default or non-empty value
		data = data or self
		for field, value in data:
			if field == "datagarden_model_version":
				continue
			if field in self.Meta.exclude_fields_in_has_values_check:
				continue

			if isinstance(value, DataGardenSubModel):
				if self.has_values(value):
					return True
			elif isinstance(value, BaseModel):
				# If one nested model has values then return True
				if self.has_values(value):
					return True
			elif (
				value or value == 0 or value is False
			):  # This will check for truthy values (non-empty)
				return True
		return False

	@classmethod
	def units(
		cls,
		attribute: str | None = None,
		indent: int = 0,
		print_units: bool = False,
	):
		def print_description(prefix, field_info, indent_level):
			if print_units:
				indent_space = "    " * indent_level
				description = field_info.description
				if description:
					print(f"{indent_space}{prefix}: {description}")

		def is_base_model(annotation):
			if isinstance(annotation, type) and issubclass(annotation, BaseModel):
				return True
			if get_origin(annotation) is Union:
				return any(is_base_model(arg) for arg in get_args(annotation))
			return False

		def recursive_units(
			sub_cls: type[BaseModel], attr_prefix="", indent_level=0
		) -> dict:
			result = {}
			for field_name, field_info in sub_cls.model_fields.items():
				full_attr_name = (
					f"{attr_prefix}.{field_name}" if attr_prefix else field_name
				)
				result[full_attr_name] = field_info.description
				if is_base_model(field_info.annotation):
					print_description(full_attr_name, field_info, indent_level)
					if field_info.annotation:
						annotation = field_info.annotation
						if get_origin(annotation) is Union:
							# Get the first non-None type from Union (Optional)
							annotation = next(
								arg
								for arg in get_args(annotation)
								if arg is not type(None)
							)
						# If it's a class, use it directly
						actual_class = (
							annotation
							if isinstance(annotation, type)
							else get_args(annotation)[0]
						)
						result.update(
							recursive_units(
								actual_class,
								full_attr_name,
								indent_level + 1,
							)
						)
				else:
					print_description(full_attr_name, field_info, indent_level)
			return result

		base_result = {}

		if attribute:
			parts = attribute.split(".")
			current_model = cls
			for part in parts:
				field_info = current_model.model_fields.get(part)
				if not field_info:
					print(f"No description available for attribute: {attribute}")
					return
				base_result[part] = field_info.description
				if issubclass(field_info.__class__, BaseModel):
					current_model = field_info.__class__
				else:
					print_description(attribute, field_info, indent)
					return
			base_result.update(recursive_units(current_model, attribute, indent + 1))
		else:
			base_result.update(recursive_units(cls))
		return base_result

	@property
	def is_empty(self) -> bool:
		return not self.has_values()

	def __bool__(self) -> bool:
		return not self.is_empty


class DataGardenModel(DataGardenSubModel):
	datagarden_model_version: str = Field(
		"v1.0",
		frozen=True,
		description=DataGardenModelLegends.DATAGARDEN_MODEL_VERSION,
	)

	class Meta:
		exclude_fields_in_has_values_check: list[str] = []

	@model_validator(mode="before")
	def check_datagarden_model_version(cls, values):
		if (
			"datagarden_model_version" in values
			and values["datagarden_model_version"]
			!= cls.model_fields["datagarden_model_version"].default
		):
			raise ValueError("The field 'datagarden_model_version' is immutable.")
		return values
