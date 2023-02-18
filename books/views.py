from django.shortcuts import render
from books.models import Books, Carts, Review
from rest_framework.views import APIView
from books.serialize import Bookserial, BookModelserial, UserModelAerializer, CartsSerialize,ReviewSerial
from rest_framework.views import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication, permissions


class Bookview(APIView):
    def get(self, request, *args, **kwargs):
        qs = Books.objects.all()
        serialize = Bookserial(qs, many=True)
        return Response(data=serialize.data)

    def post(self, request, *args, **kwargs):
        serialize = Bookserial(data=request.data)
        if serialize.is_valid():
            Books.objects.create(**serialize.validated_data)
            return Response(data=serialize.data)
        else:
            return Response(data=serialize.errors)


class Bookdetail(APIView):

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        qs = Books.objects.get(id=id)
        serialize = Bookserial(qs, many=False)
        return Response(data=serialize.data)

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        Books.objects.filter(id=id).update(**request.data)
        qs = Books.objects.get(id=id)
        serialize = Bookserial(qs, many=False)
        return Response(data=serialize.data)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id')
        Books.objects.filter(id=id).delete()
        return Response(data='deleted')


class Bookviewseet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        qs = Books.objects.all()
        serialize = BookModelserial(qs, many=True)
        return Response(data=serialize.data)

    def create(self, request, *args, **kwargs):
        serialize = BookModelserial(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(data=serialize.data)
        else:
            return Response(data=serialize.errors)

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        qs = Books.objects.get(id=id)
        serialize = BookModelserial(qs, many=False)
        return Response(data=serialize.data)

    def update(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        qs = Books.objects.get(id=id)
        serialize = BookModelserial(data=request.data, instance=qs)
        if serialize.is_valid():
            serialize.save()
            return Response(data=serialize.data)
        else:
            return Response(serialize.errors)

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        Books.objects.filter(id=id).delete()
        return Response(data='deleted')

    @action(methods=['GET'], detail=False)
    def author(self, request, *args, **kwargs):
        res = Books.objects.values_list('author', flat=True).distinct()
        return Response(data=res)


class BookViewsetModel(viewsets.ModelViewSet):
    serializer_class =BookModelserial
    queryset = Books.objects.all()
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['POST'], detail=True)
    def addto_cart(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        item=Books.objects.get(id=id)
        user=request.user
        user.carts_set.create(name=item)
        return Response(data='item added to cart')

    @action(methods=['POST'],detail=True)
    def add_review(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        item=Books.objects.get(id=id)
        user=request.user
        serialize=ReviewSerial(data=request.data)
        if serialize.is_valid():
            serialize.save(name=item,user=user)
            return Response(data=serialize.data)
        else:
            return Response(data=serialize.errors)

    @action(methods=['GET'],detail=True)
    def review(self,request,*args,**kwargs):
        name=self.get_object()
        qs=name.review_set.all()
        serialize=ReviewSerial(qs,many=True)
        return Response(data=serialize.data)



class UserView(viewsets.ModelViewSet):
    # def create(self, request, *args, **kwargs):
    #     serialize = UserModelAerializer(data=request.data)
    #     if serialize.is_valid():
    #         serialize.save()
    #         return Response(data=serialize.data)
    #     else:
    #         return Response(serialize.errors)
    serializer_class = UserModelAerializer
    queryset = User.objects.all()


class CartsView(viewsets.ModelViewSet):
    serializer_class = CartsSerialize
    queryset = Carts.objects.all()
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user)

class ReviewView(APIView):
    def delete(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        Review.objects.get(id=id).delete()
        return Response(data='deleted')
