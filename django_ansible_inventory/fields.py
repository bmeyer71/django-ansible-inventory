from django.db import models


class LowerCharField(models.CharField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if isinstance(value, str):
            return value.lower()
        return value


class UpperCharField(models.CharField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if isinstance(value, str):
            return value.upper()
        return value


class CommonFields(models.Model):
    """
    Provides the following fields and their default value:
        item_default (False)
        enabled (False)
        deprecated (False)
    """

    item_default = models.BooleanField(
        verbose_name="Default",
        default=False,
        help_text="Sets the default that will be used in forms.",
    )
    enabled = models.BooleanField(
        verbose_name="Enabled",
        default=False,
        help_text="Enables or Disables item.",
    )
    deprecated = models.BooleanField(
        verbose_name="Deprecated",
        default=False,
        help_text="Item should no longer be used.",
    )

    class Meta:
        abstract = True
