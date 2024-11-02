from django.db import models
from django.utils.translation import gettext_lazy as _
from .abstracts import MAFeedback


class MFeedback(MAFeedback):
    images = models.ManyToManyField(
        "xy_django_app_resource.MImage",
        verbose_name=_("图片"),
        related_name="%(app_label)s_%(class)s_images",
        blank=True,
    )

    class Meta:
        verbose_name = _("反馈")
        verbose_name_plural = _("反馈")
        app_label = "xy_django_app_feedback"
