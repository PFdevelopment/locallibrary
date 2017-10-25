from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
"""
Common field arguments:

    help_text: Provides a text label for HTML forms (e.g. in the admin site), as described above.
    verbose_name: A human-readable name for the field used in field labels. If not specified, Django will infer the default verbose name from the field name.
    default: The default value for the field. This can be a value or a callable object, in which case the object will be called every time a new record is created.
    null: If True, Django will store blank values as NULL in the database for fields where this is appropriate (a CharField will instead store an empty string). The default is False.
    blank: If True, the field is allowed to be blank in your forms. The default is False, which means that Django's form validation will force you to enter a value. This is often used with null=True , because if you're going to allow blank values, you also want the database to be able to represent them appropriately.
    choices: A group of choices for this field. If this is provided, the default corresponding form widget will be a select box with these choices instead of the standard text field.
    primary_key: If True, sets the current field as the primary key for the model (A primary key is a special database column designated to uniquely identify all the different table records). If no field is specified as the primary key then Django will automatically add a field for this purpose.

Common field types:

    CharField is used to define short-to-mid sized fixed-length strings. You must specify the max_length of the data to be stored.
    TextField is used for large arbitrary-length strings. You may specify a max_length for the field, but this is used only when the field is displayed in forms (it is not enforced at the database level).
    IntegerField is a field for storing integer (whole number) values, and for validating entered values as integers in forms.
    DateField and DateTimeField are used for storing/representing dates and date/time information (as Python datetime.date in and datetime.datetime objects, respectively). These fields can additionally declare the (mutually exclusive) parameters auto_now=True (to set the field to the current date every time the model is saved), auto_now_add (to only set the date when the model is first created) , and default (to set a default date that can be overridden by the user).
    EmailField is used to store and validate email addresses.
    FileField and ImageField are used to upload files and images respectively (the ImageField simply adds additional validation that the uploaded file is an image). These have parameters to define how and where the uploaded files are stored.
    AutoField is a special type of IntegerField that automatically increments. A primary key of this type is automatically added to your model if you don’t explicitly specify one.
    ForeignKey is used to specify a one-to-many relationship to another database model (e.g. a car has one manufacturer, but a manufacturer can make many cars). The "one" side of the relationship is the model that contains the key.
    ManyToManyField is used to specify a many-to-many relationship (e.g. a book can have several genres, and each genre can contain several books). In our library app we will use these very similarly to ForeignKeys, but they can be used in more complicated ways to describe the relationships between groups. These have the parameter on_delete to define what happens when the associated record is deleted (e.g. a value of models.SET_NULL would simply set the value to NULL).

"""

class Genre(models.Model):
    """
    Model representing a book genre(e.g. Science Fiction, Non Fiction, Poem)
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class Book(models.Model):
    """
    Model representing a book (but not a specific copy of book).
    """
    title = models.CharField(max_length=200)
    # Foreign Key used because book can only have one author,
    # but author can have multiple books.
    # Author as a string rather than object because it hasn't been declared yet in the file.
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    """
    Model representing a specific copy of a book(i.e. that can be borrowed from the library)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return "{0} ({1})".format(self.id, self.book.title)

class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instances.
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return "{0} {1}".format(self.first_name, self.last_name)

class Language(models.Model):
    """
    Model representing the Language of book
    """
    language = models.CharField(max_length=100, help_text="Enter a the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """
        String representing the Model object.
        """
        return self.language
