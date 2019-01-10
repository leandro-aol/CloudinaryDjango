from cloudinary.templatetags import cloudinary
from cloudinary import uploader
from django.shortcuts import render
from django.http import JsonResponse
from random import randint
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Items
from .serializer import ItemsSerializer


class ItemsView(APIView):

    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = ItemsSerializer

    def get(self, request, format = None):
        items = Items.objects.all()
        serializer = ItemsSerializer(items, many = True)
        return Response(data = serializer.data, status = status.HTTP_200_OK)

    def upload_image_cloudinary(self, request, imageName):
        uploader.upload(
            request.FILES['ImageFile'],
            public_id = imageName,
            crop = 'limit',
            width = 2000,
            height = 2000,
            eager = [
                {
                    'width': 200,
                    'height': 200,
                    'crop': 'thumb',
                    'gravity': 'face',
                    'radius': 20,
                    'effect': 'sepia'
                },
                {
                    'width': 100,
                    'height': 150,
                    'crop': 'fit',
                    'format': 'png'
                }
            ],
            tags = ['item', 'CloudinaryAPI'],
            folder = 'DjangoAPI'
        )

    def post(self, request, format = None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                imageName = '{0}_v{1}'.format(request.FILES['ImageFile'].name.split('.')[0], randint(0, 100))
                self.upload_image_cloudinary(request, imageName)
                serializer.save(image = imageName)
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            except Exception:
                return Response({'imagem': 'Envie uma imagem válida'}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)


class ItemView(APIView):

    serializer_class = ItemsSerializer

    def get_object(self, pk):
        return Items.objects.get(pk=pk)

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = self.serializer_class(item)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = self.serializer_class(item, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            item = self.get_object(pk)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as message:
            return Response(status=status.HTTP_404_NOT_FOUND)
