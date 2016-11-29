from __future__ import unicode_literals
from django.db import models
from ..login_reg.models import User
import re, time

#regex object stores regex validations and error messages
#some regexs are duplicates so that field-names can be preserved,
#fields like email and login_email have idetical regex but errors need to be displayed in different places
regex = {
    'title' : (re.compile(r'^([\w ]{1,50})$'), "Title must be only letters or numbers and no more than 50 characters long"),
    'author_list' : (re.compile(r'^[a-zA-Z]+[a-zA-Z ]*$'), "Author name must not contain any numbers or symbols"),
    'author_name' : (re.compile(r'^[a-zA-Z]+[a-zA-Z ]*$'), "Author name must not contain any numbers or symbols"),
    #Rating error should only show if something has gone wrong with the HTML or somone is messing with the front-end
    #The input should only allow valid ratings
    'rating' : (re.compile(r'^[1-5]$'), "Invalid rating"),
}

class BookManager(models.Manager):
    #Checks for empty fields and Uses regex object to validate format.
    #first value in tuple is true or false- registration is valid
    #second value returns an error notes object if form has errors, or a Book info object if form is valid
    def validateFields(self, form_data):
        print "Starting book_review.models.py BookManager validateFields method"
        valid = True
        error_notes = {}
        #Check for empty fields
        for key, value in form_data.items():
            print "Checking for value in {} field".format(key)
            if len(value) == 0:
                print "//////////////////// Form Error- {} field is empty".format(key)
                valid = False
                error_notes[key] = "This field cannot be empty"

        #Check for valid field formats- if regex exists for field- validate
        for key, value in form_data.items():
            #Check to see if regex exists for field
            if key in regex:
                print "Checking format of {} field".format(key)
                if not regex[key][0].search(value):
                    print "//////////////////// Form Error- {} field is invalid format".format(key)
                    valid = False
                    #If invalid, and no error note has been set for this field- pull error matching error message from regex dictionary
                    #The error notes will contain the most basic note for each field.
                    if not key in error_notes:
                        error_notes[key] = regex[key][1]

        return (valid, error_notes)

    def createBook(self, form_data, user):
        print "Starting book_review.models.py BookManager createBook method"
        print "models form_data = ", form_data
        book_author = 'none'
        create_author = False
        valid = True
        #Check to see if new author was added
        if form_data['author_list'] != 'none' and len(form_data['author_name']) == 0:
            #if an author was choosen from the list- set author name to 'None' so it will not trigger validation errors
            #it will be ignored in later steps
            print "Author selected from existing list"
            form_data['author_name'] = 'none'
        elif form_data['author_list'] == 'none' and len(form_data['author_name']) > 0:
            print "New Author entered"
            #Set create_author to true so that we know to create a new author
            create_author = True
        else:
            "Both new Author and Author from list selected"
            valid = False

        response = self.validateFields(form_data)
        error_notes = response[1]
        if not response[0]:
            print "return 1"
            return (False, error_notes)
        #Additional method-specific validations
        if len(form_data['review']) > 200:
            valid = False
            if not 'review' in error_notes:
                #Review length should already be limited by the html input field- this serves as a double-check
                error_notes['review'] = "Review must be less than 200 characters"
        if valid == False:
            print "Form has errors"
            print "return 2"
            for error in error_notes.values():
                print error
            return (False, error_notes)

        #After form has been validated- check to see if new Author needs to be created
        if create_author:
            new_author = Author.objects.create(name=form_data['author_name'])
            book_author = new_author
        else:
            try:
                book_author = Author.objects.get(name=form_data['author_list'])
            except Author.DoesNotExist:
                #The author list options are generated from the DB so this error should not occur
                print "////////////////////////////////////////// Form Error- Author from author_list does not match any record in the DB- cannot create new title and review"
                error_notes['author_list'] = 'We are sorry but the author you selected cannot be found in our records. Please try selecting a different author or create a new author below'
                print "return 3"
                return (False, error_notes)
        print "//////////////////////////////////Form is Vald- Creating Book"
        print form_data
        new_book = Book.objects.create(title=form_data['title'], author=book_author)

        #create a new review linked to the book_review
        new_review = Review.objects.create(content=form_data['review'], rating=form_data['rating'], user=user, book=new_book)
        print "return 4"
        return (True, new_book.id)

    def createReview(self, content, book, user):
        pass

    def updateBook(self, form_data, Book_id):
        print "Starting book_review.models.py BookManager update method"
        #Uses validateFields method to check for basic field validations- if successful,
        #Updates Book info if form is valid
        response = Book.objects.validateFields(form_data)
        valid = True
        error_notes = response[1]
        #Check if basic validation returned false
        if not response[0]:
            return (False, error_notes)
        #Additional method-specific validations
        if len(form_data['review']) > 200:
            valid = False
            if not 'review' in error_notes:
                #Review length should already be limited by the html input field- this serves as a double-check
                error_notes['review'] = "Review must be less than 200 characters"

        if valid == False:
            print "Form has errors"
            return (False, error_notes)
        #After form has been validated- add updates
        print "//////////////////////////////////Form is Vald- Updating Book"
        Book = Book.objects.get(id=Book_id)
        Book.name = form_data['name']
        Book.review = form_data['review']
        Book.price = form_data['price']
        Book.save()
        #Returning the Book id is not nessesary here but it maintains consistency
        #in the way the methods process and return data
        return (True, Book.id)

    def destroyBook(self, Book_id):
        try:
            delete_Book = Book.objects.get(id=Book_id)
        except Book.DoesNotExist:
            print "Book matching that id not found in DB"
            return False

        delete_Book.delete()
        return True

class Author(models.Model):
    name = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=55)
    author = models.ForeignKey(Author)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class Review(models.Model):
    content = models.TextField(max_length=300)
    rating = models.PositiveIntegerField()
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
