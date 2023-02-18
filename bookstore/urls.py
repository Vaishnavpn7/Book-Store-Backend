from django.contrib import admin
from django.urls import path
from books import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('api/books', views.Bookviewseet, basename='books')
router.register('user', views.UserView, basename='user')
router.register('model/book', views.BookViewsetModel, basename='book')
router.register('carts', views.CartsView, basename='carts')

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('books/', views.Bookview.as_view()),
                  path('books/<int:id>', views.Bookdetail.as_view()),
                  path('review',views.ReviewView.as_view())
              ] + router.urls
