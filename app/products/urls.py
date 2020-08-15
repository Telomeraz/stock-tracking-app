from django.urls import path
from .views import *

urlpatterns = [
    path('', PanelView.as_view()),

    path('kisiler/', PersonView.as_view()),
    path('kisi-ekle/', AddPersonView.as_view()),
    path('kisi-duzenle/<int:person_id>/', EditPersonView.as_view()),
    path('kisi-sil/<int:person_id>/', DeletePersonView.as_view()),

    path('urunler/', ProductView.as_view()),
    path('urun-ekle/', AddProductView.as_view()),
    path('urun-duzenle/<int:product_id>/', EditProductView.as_view()),
    path('urun-sil/<int:product_id>/', DeleteProductView.as_view()),

    path('alis-tablosu/', PurchaseView.as_view()),
    path('alis-ekle/', AddPurchaseView.as_view()),
    path('alis-duzenle/<int:purchase_id>/', EditPurchaseView.as_view()),
    path('alis-sil/<int:purchase_id>/', DeletePurchaseView.as_view()),

    path('satis-tablosu/', SaleView.as_view()),
    path('satis-ekle/', AddSaleView.as_view()),
    path('satis-duzenle/<int:sale_id>/', EditSaleView.as_view()),
    path('satis-sil/<int:sale_id>/', DeleteSaleView.as_view())
]
