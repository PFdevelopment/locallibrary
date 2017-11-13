from django.conf.urls import url

from . import views

app_name = 'catalog'

urlpatterns = [
    # Calls index view
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name="book-detail"),
    url(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    url(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
    url(r'^borrowed/$', views.LoanedBooksByLibrarianListView.as_view(), name='borrowed')
]
