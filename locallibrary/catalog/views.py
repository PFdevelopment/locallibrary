from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import datetime

from .models import Book, BookInstance, Author, Genre
from .forms import RenewBookForm

# @login_required
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

class BookListView(LoginRequiredMixin, generic.ListView):
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

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksByLibrarianListView(PermissionRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to librarians.
    """

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_librarian.html'
    permission_required = ('catalog.can_mark_returned')
    paginate_by = 2

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request(binding)
        form = RenewBookForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # proccess the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('catalog:borrowed'))

    # If this is a GET method create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})
