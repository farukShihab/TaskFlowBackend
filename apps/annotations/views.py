from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import (
    Response
)

from .models import (
    Study,
    StudyImage,
    Polygon,
)

from .serializers import (
    StudySerializer,
    StudyDetailSerializer,
    StudyImageSerializer,
    PolygonSerializer,
)

class StudyListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = StudySerializer
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return Study.objects.filter(
            owner=self.request.user
        )

    def perform_create(
        self,
        serializer,
    ):
        serializer.save(
            owner=self.request.user
        )

class StudyRetrieveView(
    generics.RetrieveAPIView
):
    serializer_class = (
        StudyDetailSerializer
    )
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return Study.objects.filter(
            owner=self.request.user
        )

class StudyDeleteView(
    generics.DestroyAPIView
):
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return Study.objects.filter(
            owner=self.request.user
        )

class StudyImageUploadView(
    generics.CreateAPIView
):
    serializer_class = (
        StudyImageSerializer
    )
    permission_classes = [
        IsAuthenticated
    ]

    def create(
        self,
        request,
        *args,
        **kwargs,
    ):
        study = Study.objects.get(
            pk=kwargs["study_id"],
            owner=request.user,
        )

        files = request.FILES.getlist(
            "images"
        )

        created = []

        for index, file in enumerate(
            files
        ):
            image = (
                StudyImage.objects.create(
                    study=study,
                    image=file,
                    order=index,
                )
            )

            created.append(image)

        serializer = (
            StudyImageSerializer(
                created,
                many=True,
                context={
                    "request": request
                },
            )
        )

        return Response(
            serializer.data
        )

class PolygonCreateView(
    generics.CreateAPIView
):
    serializer_class = PolygonSerializer
    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(
        self,
        serializer
    ):
        image = StudyImage.objects.get(
            pk=self.kwargs["image_id"],
            study__owner=self.request.user,
        )

        serializer.save(
            image=image
        )

class PolygonUpdateView(
    generics.RetrieveUpdateAPIView
):
    serializer_class = (
        PolygonSerializer
    )
    permission_classes = [
        IsAuthenticated
    ]

    queryset = Polygon.objects.all()

class PolygonDeleteView(
    generics.DestroyAPIView
):
    permission_classes = [
        IsAuthenticated
    ]

    queryset = Polygon.objects.all()

