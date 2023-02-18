from rest_framework import serializers
from books.models import Books, Carts, Review
from django.contrib.auth.models import User


class Bookserial(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    author = serializers.CharField()
    price = serializers.IntegerField()
    discription = serializers.CharField()


class BookModelserial(serializers.ModelSerializer):
    avg_rating=serializers.CharField(read_only=True)
    total_review=serializers.CharField(read_only=True)

    class Meta:
        model = Books
        fields = '__all__'


class UserModelAerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CartsSerialize(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Carts
        fields = '__all__'


class ReviewSerial(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    comment = serializers.CharField(max_length=200)
    class Meta:
        model = Review
        fields = '__all__'
