from rest_framework import serializers

from .models import (
    Study,
    StudyImage,
    Polygon,
)

class PolygonSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = Polygon
        fields = [
            "id",
            "hidden",
            "points",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]

class StudyImageSerializer(
    serializers.ModelSerializer
):
    polygons = PolygonSerializer(
        many=True,
        read_only=True,
    )

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = StudyImage
        fields = [
            "id",
            "image",
            "image_url",
            "order",
            "polygons",
            "created_at",
        ]

    def get_image_url(
        self,
        obj,
    ):
        request = self.context.get(
            "request"
        )

        if request:
            return request.build_absolute_uri(
                obj.image.url
            )

        return obj.image.url

class StudySerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = Study
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

class StudyDetailSerializer(
    serializers.ModelSerializer
):
    images = StudyImageSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Study
        fields = [
            "id",
            "title",
            "description",
            "images",
            "created_at",
            "updated_at",
        ]