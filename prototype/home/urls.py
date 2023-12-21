from django.urls import path, reverse_lazy, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='prototype'
urlpatterns = [
    # path('', include('js.urls')),
    path('', views.HomeView.as_view(), name='all'),
    path('search/', views.SearchView.as_view(), name='search'),
    # path('book_list/', views.BookListView.as_view(), name='search'),

    ########################       ACCOUNT       ##########################
    path("signup/", views.signup_method, name="signup"),
    path("login/", views.login_method, name="login"),
    path('profile/update', views.ProfileUpdateView.as_view(), name='profile_update'),

    ########################       BOOK       ##########################
    path('create_book/', views.BookCreateView.as_view(), name='book_create'),
    path('book_list/', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('book/<int:pk>/update', views.BookUpdateView.as_view(), name='book_update'),
    path('book_delete/<int:pk>', views.book_delete, name='book_delete'),
    path('book_picture/<int:pk>', views.stream_file, name='book_picture'),


    ########################       PUBLISHER       ##########################
    path('create_publisher/', views.PublisherCreateView.as_view(), name='publisher_create'),
    path('publisher_list/', views.PublisherListView.as_view(), name='publisher_list'),
    path('publisher/<int:pk>', views.PublisherDetailView.as_view(), name='publisher_detail'),
    path('publisher/<int:pk>/update', views.PublisherUpdateView.as_view(), name='publisher_update'),
    path('publisher_delete/<int:pk>', views.publisher_delete, name='publisher_delete'),
    path('publisher_picture/<int:pk>', views.view_publisher, name='publisher_picture'),


    ########################       AUTHOR       ##########################
    path('create_author/', views.AuthorCreateView.as_view(), name='author_create'),
    path('author_list/', views.AuthorListView.as_view(), name='author_list'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author_detail'),
    path('author/<int:pk>/update', views.AuthorUpdateView.as_view(), name='author_update'),
    path('author_delete/<int:pk>', views.author_delete, name='author_delete'),
    path('author_picture/<int:pk>', views.view_author, name='author_picture'),


    ########################       CATEGORY       ##########################
    path('create_category/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category_list/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/<int:pk>/update', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category_delete/<int:pk>', views.category_delete, name='category_delete'),


    ########################       FAV       ##########################
    path('book/<int:pk>/favorite',
        views.AddFavoriteView.as_view(), name='book_favorite'),
    path('book/<int:pk>/unfavorite',
        views.DeleteFavoriteView.as_view(), name='book_unfavorite'),
    path('favorites/', views.favorites_view, name='favorites'),


    ########################       BASKET       ##########################
    path('basket/', views.BasketDetailView.as_view(), name='basket'),
    path('amount/<int:pk>/update', views.amount_update, name='amount_update'),
    path('basket_add/<int:pk>/',
        views.AddIntoBasket.as_view(), name='basket_add'),
    path('basket_delete/<int:pk>/',
        views.DeleteOutofBasket.as_view(), name='basket_delete'),
    path('confirm_order/', views.ConfirmOrderView.as_view(), name='confirm_order'),


    ########################       ORDER       ##########################
    path('order_list/', views.OrderListView.as_view(), name='orders'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order_delete/<int:pk>', views.order_delete, name='order_delete'),
    path('order_payment/<int:pk>', views.view_payment, name='order_picture'),
    path('order/<int:pk>/confirm/', views.admin_confirm, name='admin_confirm')
]
