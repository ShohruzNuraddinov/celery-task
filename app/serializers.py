from rest_framework import serializers


from app.models import ImageFile


class ImageSerialzier(serializers.ModelSerializer):
    class Meta:
        model = ImageFile
        fields = (
            'id',
            'image',
        )