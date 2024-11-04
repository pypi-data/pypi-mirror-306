import inspect
from collections.abc import Callable
from typing import Self

from pydantic import (
    BaseModel,
    Field,
    PrivateAttr,
    create_model,
    field_validator,
    model_validator,
)

from lion_core.funcs import to_json, validate_boolean, validate_keys
from lion_core.ln_undefined import LN_UNDEFINED
from lion_core.models import FieldModel, OperableModel, SchemaModel
from lion_core.types import FieldInfo
from lion_core.utils import copy


class NewModelParams(SchemaModel):

    name: str | None = None
    parameter_fields: dict[str, FieldInfo] = Field(default_factory=dict)
    base_type: type[BaseModel] = Field(default=BaseModel)
    field_models: list[FieldModel] = Field(default_factory=list)
    exclude_fields: list = Field(default_factory=list)
    field_descriptions: dict = Field(default_factory=dict)
    inherit_base: bool = Field(default=True)
    use_base_kwargs: bool = False
    config_dict: dict | None = Field(default=None)
    doc: str | None = Field(default=None)
    _class_kwargs: dict = PrivateAttr(default_factory=dict)
    frozen: bool = False
    _validators: dict[str, Callable] | None = PrivateAttr(default=None)
    _use_keys: set[str] = PrivateAttr(default_factory=set)

    @property
    def use_fields(self):
        params = {
            k: v
            for k, v in self.parameter_fields.items()
            if k in self._use_keys
        }
        params.update(
            {
                f.name: f.field_info
                for f in self.field_models
                if f.name in self._use_keys
            }
        )
        return {k: (v.annotation, v) for k, v in params.items()}

    @field_validator("field_models", mode="before")
    def _validate_field_models(cls, value):
        if value is None:
            return []
        value = [value] if not isinstance(value, list) else value
        if not all(isinstance(i, FieldModel) for i in value):
            raise ValueError("Field models must be FieldModel objects.")
        return value

    @field_validator("parameter_fields", mode="before")
    def validate_parameters(cls, value):
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ValueError("Fields must be a dictionary.")
        for k, v in value.items():
            if not isinstance(k, str):
                raise ValueError("Field names must be strings.")
            if not isinstance(v, FieldInfo):
                raise ValueError("Field values must be FieldInfo objects.")
        return copy(value)

    @field_validator("base_type", mode="before")
    def validate_base(cls, value) -> type[BaseModel]:
        if value is None:
            return BaseModel
        if isinstance(value, type) and issubclass(value, BaseModel):
            return value
        if isinstance(value, BaseModel):
            return value.__class__
        raise ValueError("Base must be a BaseModel subclass or instance.")

    @field_validator("exclude_fields", mode="before")
    def validate_fields(cls, value) -> list[str]:
        if value is None:
            return []
        if isinstance(value, dict):
            value = list(value.keys())
        if isinstance(value, set | tuple):
            value = list(value)
        if isinstance(value, list):
            if not all(isinstance(i, str) for i in value):
                raise ValueError("Field names must be strings.")
            return copy(value)
        raise ValueError("Fields must be a list, set, or dictionary.")

    @field_validator("field_descriptions", mode="before")
    def validate_field_descriptions(cls, value) -> dict[str, str]:
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ValueError("Field descriptions must be a dictionary.")
        for k, v in value.items():
            if not isinstance(k, str):
                raise ValueError("Field names must be strings.")
            if not isinstance(v, str):
                raise ValueError("Field descriptions must be strings.")
        return value

    @field_validator("inherit_base", mode="before")
    def validate_inherit_base(cls, value) -> bool:
        try:
            return validate_boolean(value)
        except Exception:
            return True

    @field_validator("name", mode="before")
    def validate_name(cls, value) -> str:
        if value is None:
            return "StepModel"
        if not isinstance(value, str):
            raise ValueError("Name must be a string.")
        return value

    @field_validator("field_models", mode="before")
    def validate_field_models(cls, value):
        if value is None:
            return []
        value = [value] if not isinstance(value, list) else value
        if not all(isinstance(i, FieldModel) for i in value):
            raise ValueError("Field models must be FieldModel objects.")
        return value

    @model_validator(mode="after")
    def validate_param_model(self) -> Self:

        if self.base_type is not None:
            self.parameter_fields.update(copy(self.base_type.model_fields))

        self.parameter_fields.update(
            {f.name: f.field_info for f in self.field_models}
        )

        use_keys = list(self.parameter_fields.keys())
        use_keys.extend(list(self._use_keys))

        if self.exclude_fields:
            use_keys = [i for i in use_keys if i not in self.exclude_fields]

        self._use_keys = set(use_keys)

        validators = {}

        for i in self.field_models:
            if i.field_validator is not None:
                validators.update(i.field_validator)
        self._validators = validators

        if self.field_descriptions:
            for i in self.field_models:
                if i.name in self.field_descriptions:
                    i.description = self.field_descriptions[i.name]

        # Prepare class attributes
        class_kwargs = {}
        if self.use_base_kwargs:
            class_kwargs.update(
                {
                    k: getattr(self.base_type, k)
                    for k in self.base_type.__dict__
                    if not k.startswith("__")
                }
            )
        self._class_kwargs = class_kwargs

        if hasattr(self.base_type, "class_name"):
            if callable(self.base_type.class_name):
                self.name = self.base_type.class_name()
            else:
                self.name = self.base_type.class_name
        elif inspect.isclass(self.base_type):
            self.name = self.base_type.__name__

        return self

    def create_new_model(self) -> type[BaseModel]:
        a: type[BaseModel] = create_model(
            self.name,
            __config__=self.config_dict,
            __doc__=self.doc,
            __base__=self.base_type if self.inherit_base else BaseModel,
            __cls_kwargs__=self._class_kwargs,
            __validators__=self._validators,
            **self.use_fields,
        )
        if self.frozen:
            a.model_config.frozen = True
        return a


class Operative(OperableModel):

    name: str | None = None

    request_params: NewModelParams | None = Field(default=None)
    request_type: type[BaseModel] | None = Field(default=None)

    response_params: NewModelParams | None = Field(default=None)
    response_type: type[BaseModel] | None = Field(default=None)
    response_model: OperableModel | None = Field(default=None)
    response_str_dict: dict | str | None = Field(default=None)

    auto_retry_parse: bool = True
    max_retries: int = 3
    _should_retry: bool = PrivateAttr(default=None)

    @model_validator(mode="after")
    def _validate(self) -> Self:
        if self.request_type is None:
            self.request_type = self.request_params.create_new_model()
        if self.name is None:
            self.name = self.request_params.name or self.request_type.__name__
        return self

    def raise_validate_pydantic(self, text: str):
        d_ = to_json(text, fuzzy_parse=True)
        if isinstance(d_, list | tuple) and len(d_) == 1:
            d_ = d_[0]
        try:
            d_ = validate_keys(
                d_, self.request_type.model_fields, handle_unmatched="raise"
            )
            d_ = {k: v for k, v in d_.items() if v != LN_UNDEFINED}
            self.response_model = self.request_type.model_validate(d_)
            self._should_retry = False
        except Exception:
            self.response_str_dict = d_
            self._should_retry = True

    def force_validate_pydantic(self, text: str):
        d_ = text
        try:
            d_ = to_json(text, fuzzy_parse=True)
            if isinstance(d_, list | tuple) and len(d_) == 1:
                d_ = d_[0]
            d_ = validate_keys(
                d_, self.request_type.model_fields, handle_unmatched="force"
            )
            d_ = {k: v for k, v in d_.items() if v != LN_UNDEFINED}
            self.response_model = self.request_type.model_validate(d_)
            self._should_retry = False
        except Exception:
            self.response_str_dict = d_
            self.response_model = None
            self._should_retry = True

    def update_response_model(
        self, text: str = None, data: dict = None
    ) -> BaseModel | dict | str | None:

        if text is None and data is None:
            raise ValueError("Either text or data must be provided.")

        if text:
            self.response_str_dict = text
            try:
                self.raise_validate_pydantic(text)
            except Exception:
                self.force_validate_pydantic(text)

        if data and self.response_type:
            d_ = self.response_model.model_dump()
            d_.update(data)
            self.response_model = self.response_type.model_validate(d_)

        return self.response_model or self.response_str_dict

    def create_response_type(
        self,
        response_params: NewModelParams = None,
        field_models: list[FieldModel] = [],
        parameter_fields: dict[str, FieldInfo] = None,
        exclude_fields: list = [],
        field_descriptions: dict = {},
        inherit_base: bool = True,
        use_base_kwargs: bool = False,
        config_dict: dict | None = None,
        doc: str | None = None,
        frozen: bool = False,
        validators=None,
    ):
        self.response_params = response_params or NewModelParams(
            parameter_fields=parameter_fields,
            field_models=field_models,
            exclude_fields=exclude_fields,
            field_descriptions=field_descriptions,
            inherit_base=inherit_base,
            use_base_kwargs=use_base_kwargs,
            config_dict=config_dict,
            doc=doc,
            frozen=frozen,
            base_type=self.request_params.base_type,
        )
        if validators and isinstance(validators, dict):
            self.response_params._validators.update(validators)

        self.response_type = self.response_params.create_new_model()
