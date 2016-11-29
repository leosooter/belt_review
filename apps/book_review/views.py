from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from ..login_reg.models import User
from models import Book, Author, Review

def index(request):
    print "///////////////////////////////////Starting book_review Index route"
    books = Book.objects.all()
    reviews = Review.objects.all()
    context = {
        'books' : books,
        'reviews' : reviews,
    }
    return render(request, 'book_review/index.html', context)

def new(request):
    print "///////////////////////////////////Starting book_review New route"
    authors = Author.objects.all()
    context = {
        'authors' : authors
    }
    return render(request, 'book_review/new.html', context)

def create(request):
    print "///////////////////////////////////Starting book_review Create route"
    try:
        user = User.objects.get(id=request.session['login_id'])
    except:
        print "User is not logged in"
        return redirect(reverse('login_reg:logout'))
    if request.method == 'POST':
        print "Post method"
        form_data = {
            'title' : request.POST['title'],
            'author_list' : request.POST['author_list'],
            'author_name' : request.POST['author_name'],
            'review' : request.POST['review'],
            'rating' : request.POST['rating'],
        }
        print "views form_data = ", form_data

        response = Book.objects.createBook(form_data, user)
        if response[0]:
            print "Create is successful"
            book_id = str(response[1])
            return redirect(reverse('book_review:index'))
            #return redirect( reverse('book_review:show', kwargs={'id':book_id}) )

        else:
            print "new_form has errors"
            #Load error_notes returned from registration method into messages
            error_notes = response[1]
            for key, note in error_notes.items():
                messages.error(request, note, extra_tags=key)

            #Preserve any values that do not have error messages and pass them back to the registration form
            for key, value in form_data.items():
                if key not in error_notes:
                    messages.info(request, value, extra_tags=key + "_value")
            print "Sending back to new.html"
            print messages
            return redirect(reverse('book_review:new'))
    else:
        print "Invalid request type"
    return redirect(reverse('book_review:index'))

def show(request, id):
    print "///////////////////////////////////Starting book_review Show route"
    try:
        user = User.objects.get(id=request.session['login_id'])
    except:
        print "User is not logged in"
        return redirect(reverse('login_reg:logout'))
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        print "No book matches the id", id
        return redirect(reverse('book_review:index'))

    reviews = Review.objects.filter(book=book)
    context = {
        'id' : book.id,
        'title' : book.title,
        'author' : book.author.name,
        'reviews' : reviews,
    }
    return render(request, 'book_review/show.html', context)

def edit(request, id):
    print "///////////////////////////////////Starting book_review Edit route"
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        print "No book matches the id", id
        return redirect(reverse('book_review:index'))

    context = {
        'id' : book.id,
        'name' : book.name,
        'description' : book.description,
        'price' : book.price,
    }

    return render(request, 'book_review/edit.html', context)

def update(request, id):
    print "///////////////////////////////////Starting book_review Update route"
    if request.method == 'POST':
        print "Post method id=", id
        form_data = {
            'name' : request.POST['name'],
            'description' : request.POST['description'],
            'price' : request.POST['price'],
        }
        print "views form_data = ", form_data
        response = Book.objects.updateBook(form_data, id)
        if response[0]:
            print "Update is successful"
            book_id = str(response[1])
            return redirect( reverse('book_review:show', kwargs={'id':book_id}) )

        else:
            print "edit_form has errors"
            #Load error_notes returned from registration method into messages
            error_notes = response[1]
            for key, note in error_notes.items():
                messages.error(request, note, extra_tags=key)

            #Preserve any values that do not have error messages and pass them back to the registration form
            for key, value in form_data.items():
                if key not in error_notes:
                    messages.info(request, value, extra_tags=key + "_value")
            print "Sending back to edit.html"
            return redirect(reverse('book_review:edit', kwargs={'id':id}))
    else:
        print "Invalid request type"
    return redirect(reverse('book_review:index'))

def delete(request, id):
    print "///////////////////////////////////Starting book_review Delete route"
    try:
        book = Book.objects.get(id=id)
        print "Book with id", book.id, "found"
    except Book.DoesNotExist:
        print "No book matches the id", id
        return redirect(reverse('book_review:index'))

    context = {
        'id' : book.id,
        'name' : book.name,
        'description' : book.description,
        'price' : book.price,
    }

    return render(request, 'book_review/destroy.html', context)

def destroy(request, id):
    print "///////////////////////////////////Starting book_review Destroy route"
    if request.method == 'POST':
        response = Book.objects.destroyBook(id)
        if response:
            print "Book has been deleted"
        else:
            print "Error- no book matching that id found in DB"
        print "Post method"

    else:
        print "Invalid request type"
    return redirect(reverse('book_review:index'))
