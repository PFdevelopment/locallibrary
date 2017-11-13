from django.contrib import admin

from .models import Book, BookInstance, Genre, Author, Language

# Adding inline editing of associated records
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

# admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # display_genre - is a function
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]




# admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # list_display contains items to be displayed
    list_display = ('book', 'status', 'borrower', 'due_back')
    # list_filter contains items for filtering
    list_filter = ('status', 'due_back')
    # fieldsets creates the section of grouped items
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        })
    )


admin.site.register(Genre)
# admin.site.register(Author)

class BookInline(admin.TabularInline):
    model = Book

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # Controlling which fields are displayed and laid out
    # ('date_of_birth', 'date_of_death') - means that
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

admin.site.register(Language)
