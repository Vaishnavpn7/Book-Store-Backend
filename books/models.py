from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Books(models.Model):
    name = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    discription = models.CharField(max_length=150)

    @property
    def avg_rating(self):
        rating= self.review_set.all().values_list('rating',flat=True)
        if rating:
            return sum(rating)/len(rating)
        else:
            return 0

    @property
    def total_review(self):
        total=self.review_set.all().values_list('rating',flat=True)
        return len(total)

    def __str__(self):
        return self.name


class Carts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(Books, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    name = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
