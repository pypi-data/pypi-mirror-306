import base64

from django.db import models
from django.utils.translation import gettext_lazy as _

from .fernet import *

__all__ = [
    "FernetBinaryField",
    "FernetTextField",
]


class FernetBinaryField(models.BinaryField):
    description = _("Raw fernet encrypted binary data")
    empty_values = [None, b""]
    data_class = FernetBinaryFieldData

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value in self.empty_values:
            value = None
        elif isinstance(value, self.data_class):
            if value.data is None:
                value = None
            else:
                value = value.raw

        return super().get_db_prep_value(value, connection, prepared)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def value_to_string(self, obj):
        raw = self.value_from_object(obj).raw

        if raw is None:
            return None
        else:
            return base64.b64encode(raw).decode("ASCII")

    def to_python(self, value):
        if isinstance(value, self.data_class):
            return value

        else:
            value = super().to_python(value)

            if value in self.empty_values:
                value = None

            return self.data_class(raw=value)


class FernetTextField(FernetBinaryField):
    description = _("Fernet encrypted text data")
    empty_values = [None, ""]
    data_class = FernetTextFieldData
