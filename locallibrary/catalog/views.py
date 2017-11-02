from django.shortcuts import render
from django.views import generic

from .models import Book, BookInstance, Author, Genre

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()    # The all() is implied by default
    num_genres = Genre.objects.all().count()
    num_garden_books = Book.objects.all().filter(title__exact="garden").count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context = {
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_genres': num_genres,
            'num_garden_books': num_garden_books,
            'num_visits': num_visits,
        },
    )

# List of Books
class BookListView(generic.ListView):
    model = Book
    # Adding pagination
    paginate_by = 2


# Details of the books
class BookDetailView(generic.DetailView):
    model = Book

# List of authors
class AuthorListView(generic.ListView):
    model = Author

    paginate_by = 2

# Details of authors
class AuthorDetailView(generic.DetailView):
    model = Author
