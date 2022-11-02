from rest_framework import generics , mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
 
from .models import Product
from .serializers import ProductSerializer
from api.mixins import StaffEditorPermissionMixin,UserQuerySetMixin

"""
class ProductMixinView(
    
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = "this is a single view doing cool stuff"
        serializer.save(content=content)

"""

class ProductListCreateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)


class ProductDetailAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductUpdateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
        return super().perform_update(serializer)

class ProductDeleteAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.DestroyAPIView):
    queryset =  Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)



product_delete_view = ProductDeleteAPIView.as_view()
product_update_view = ProductUpdateAPIView.as_view()
product_list_create_view = ProductListCreateAPIView.as_view()
product_detail_view = ProductDetailAPIView.as_view()
#product_mixin_view = ProductMixinView.as_view()



"""
@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):

    method = request.method

    if method == 'GET':
        # return one specific item
        # or list of all items
        if pk == None:
            # list items
            qs = Product.objects.all()
            data = ProductSerializer(qs, many=True).data
            return Response(data)
        #detail item
        obj = get_object_or_404(Product, pk=pk)
        data = ProductSerializer(obj, many=False).data
        return Response(data)


    if method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)             
            serializer.save()
            return Response(serializer.data)
        return Response({"invalid": "not good data"}, status=400)

"""