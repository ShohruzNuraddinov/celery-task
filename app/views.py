from django.shortcuts import render
from rest_framework import generics

from app.models import ImageFile
from app.serializers import ImageSerialzier

from app.tasks import image_save
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class ImageListApiView(generics.ListAPIView):
    queryset = ImageFile.objects.all()
    serializer_class = ImageSerialzier


class RandomImageDownload(generics.GenericAPIView):
    def get(self, request):
        image_save.delay()
        return Response(status=status.HTTP_200_OK)
