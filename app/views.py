from django.shortcuts import HttpResponse
from rest_framework import generics
from PIL import Image

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


class ImageRetrieveAPIView(generics.GenericAPIView):
    queryset = ImageFile.objects.all()
    serializer_class = ImageSerialzier

    def get(self, request):
        queryset = self.get_queryset().order_by('?').first()
        width = request.query_params.get('width')
        heigh = request.query_params.get('heigh')

        if width is None or heigh is None:
            return HttpResponse(queryset.image, content_type='image/png')

        img = Image.open(queryset.image)
        img.resize((int(width), int(heigh)))
        # img.seek(0)

        return HttpResponse(img, content_type='image/png')
