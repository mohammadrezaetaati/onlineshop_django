from django.urls import path

from .views import ProductList , ProductDetail, add_comment, delete_comment, like_comment , dislike_comment, test

urlpatterns = [
    path('product-list/', ProductList.as_view(), name="product_list"),
    path('product-detail/<int:id>/<slug>', ProductDetail.as_view(), name="product_detail"),
    path('add-comment/', add_comment, name="add_comment"),
    path('delete-comment/<int:id>', delete_comment, name="delete_comment"),
    path('like-comment/<int:id>', like_comment, name="like_comment"),
    path('dislike-comment/<int:id>', dislike_comment, name="dislike_comment"),
    path('test', test, name="test"),
]
