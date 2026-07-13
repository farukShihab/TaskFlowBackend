from django.conf import settings
from django.db import models


class Study(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="studies"
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title


class StudyImage(models.Model):
    study = models.ForeignKey(
        Study,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="studies/"
    )

    order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Image {self.order} - {self.study.title}"


class Polygon(models.Model):
    image = models.ForeignKey(
        StudyImage,
        on_delete=models.CASCADE,
        related_name="polygons"
    )

    hidden = models.BooleanField(
        default=False
    )

    points = models.JSONField(
        default=list
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Polygon {self.id}"