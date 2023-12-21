from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.views import View #, generic
# from django.conf import settings
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, BookForm, OrderForm, PublisherForm, ProfileUpdateForm, AuthorForm, CategoryForm

from .models import Book, Fav, Basket, BasketRecord, Order, OrderRecord, Publisher, AddressRecord, Author, Category, Authority, Categorisation
from django.db.utils import IntegrityError
from django.db.models import Q, Sum

def signup_method(request):
    success_url=reverse_lazy('prototype:all')
    if request.user.is_anonymous:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                form.save()
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(success_url)                 #################
            else:
                errors = "errors"
                form = SignUpForm()
                context = {
                    'form': form, 'errors' : errors
                }
                return render(request, 'registration/signup.html', context)
    else:
        return render(request, 'home/home.html')
    form = SignUpForm()
    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)

def login_method(request):
    success_url=reverse_lazy('prototype:all')
    if request.user.is_anonymous:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(success_url)                    ###############
    else:
        return redirect(success_url)
    form = AuthenticationForm()
    context = {
        "form": form
    }
    return render(request, "registration/login.html", context)

class ProfileUpdateView(View):
    template_name = "home/profile_update.html"
    success_url=reverse_lazy('prototype:all')
    def get(self, request):
        if request.user.is_authenticated:
            address = request.user.address.all()
            if address.count() == 0:
                address = AddressRecord(user=request.user)
                address.save()
            else:
                address = address[0]
            address = address.address
            form = ProfileUpdateForm(instance=request.user)
            context = { 'form' : form, 'address' : address }
            return render(request, self.template_name, context)
        else:
            return redirect(success_url)

    def post(self, request):
        if request.user.is_authenticated:
            if request.method == "POST":
                form = ProfileUpdateForm(request.POST, instance=request.user)
                if form.is_valid():
                    new_address = request.POST.get("address")
                    address = request.user.address.all()[0]
                    address.address = new_address
                    address.save()
                    update = form.save()
                    # ctx = home_view(request)
                    # return render(request, "home/home.html", ctx)                    ##############
                    return redirect(self.success_url)
                else:
                    errors = "errors"
                    address = request.user.address.all()[0].address
                    form = ProfileUpdateForm(instance=request.user)
                    context = { 'form' : form, 'address' : address, 'errors' : errors }
                    return render(request, self.template_name, context)
        else:
            return render(request, 'home/home.html')
        address = request.user.address.all()[0].address
        form = ProfileUpdateForm(instance=request.user)
        context = { 'form' : form, 'address' : address }
        return render(request, self.template_name, context)

class HomeView(View):
    template_name = 'home/home.html'
    def get(self, request):
        trending_books = list()
        book1 = Book.objects.filter(id=1).first()
        book2 = Book.objects.filter(id=2).first()
        book3 = Book.objects.filter(id=3).first()
        book4 = Book.objects.filter(id=4).first()
        book5 = Book.objects.filter(id=5).first()
        trending_books.append(book1)
        trending_books.append(book2)
        trending_books.append(book3)
        trending_books.append(book4)
        trending_books.append(book5)
        bk = Book.objects.all()[:5]
        non_fiction = Category.objects.filter(name="Non-fiction").first()
        non_books = Categorisation.objects.filter(category=non_fiction)[:5]
        fiction = Category.objects.filter(name="Fiction").first()
        fic_books = Categorisation.objects.filter(category=fiction)[:5]
        history = Category.objects.filter(name="History").first()
        his_books = Categorisation.objects.filter(category=history)[:5]
        fantasy = Category.objects.filter(name="Fantasy").first()
        fan_books = Categorisation.objects.filter(category=fantasy)[:5]
        science = Category.objects.filter(name="Science").first()
        sci_books = Categorisation.objects.filter(category=science)[:5]
        horror = Category.objects.filter(name="Horror").first()
        hor_books = Categorisation.objects.filter(category=horror)[:5]
        kid = Category.objects.filter(name="Kid").first()
        kid_books = Categorisation.objects.filter(category=kid)[:5]
        ctx = {
            'book_list': bk, 'trending_books':trending_books, 'non_books':non_books,
            'fic_books' : fic_books, 'his_books' : his_books, 'fan_books' : fan_books,
            'sci_books' : sci_books, 'hor_books' : hor_books, 'kid_books' : kid_books
        }
        return render(request, self.template_name, ctx)

# def home_view(request):
#     bk = Book.objects.all()[:5]
#     ctx = {'book_list': bk}
#     return ctx

class SearchView(View):
    template_name = "home/search.html"
    success_url=reverse_lazy('prototype:all')
    def get(self, request):
        search =  request.GET.get("search") #, False
        if search :
            # Simple title-only search
            # __icontains for case-insensitive search
            query = Q(title__icontains=search)
            query.add(Q(description__icontains=search), Q.OR)
            query.add(Q(tags__name__in=[search]), Q.OR)
            books = Book.objects.filter(query).select_related().distinct() #.order_by('-created_at')[:10]

            query = Q(name__icontains=search)
            query.add(Q(description__icontains=search), Q.OR)
            query.add(Q(tags__name__in=[search]), Q.OR)
            authors = Author.objects.filter(query).select_related().distinct()

            query = Q(name__icontains=search)
            query.add(Q(description__icontains=search), Q.OR)
            query.add(Q(tags__name__in=[search]), Q.OR)
            publishers = Publisher.objects.filter(query).select_related().distinct()

            ctx = {'book_list': books, 'author_list': authors, 'publisher_list': publishers, 'search' : search}
            return render(request, self.template_name, ctx)
        else:
            return redirect(self.success_url)

def aut_and_cat_update(request, pk):
    book = get_object_or_404(Book, id=pk)
    author_records = Authority.objects.filter(book=book)[:3]
    for record in author_records:
        record.delete()
    category_records = Categorisation.objects.filter(book=book)[:3]
    for record in category_records:
        record.delete()
    aut_and_cat_check(request, pk)

def aut_and_cat_check(request, pk):
    book = get_object_or_404(Book, id=pk)
    author1_name = request.POST.get("author1")
    author2_name = request.POST.get("author2")
    author3_name = request.POST.get("author3")
    category1_name = request.POST.get("category1")
    category2_name = request.POST.get("category2")
    category3_name = request.POST.get("category3")
    if author1_name != "":
        author1 = Author.objects.filter(name=author1_name).first()
        if author1 == None:
            author1 = Author(name=author1_name)
            author1.save()
        record = Authority(author=author1, book=book)
        record.save()
    if author2_name != "":
        author2 = Author.objects.filter(name=author2_name).first()
        if author2 == None:
            author2 = Author(name=author2_name)
            author2.save()
        record = Authority(author=author2, book=book)
        record.save()
    if author3_name != "":
        author3 = Author.objects.filter(name=author3_name).first()
        if author3 == None:
            author3 = Author(name=author3_name)
            author3.save()
        record = Authority(author=author3, book=book)
        record.save()
    if category1_name != "":
        category1 = Category.objects.filter(name=category1_name).first()
        if category1 == None:
            category1 = Category(name=category1_name)
            category1.save()
        record = Categorisation(category=category1, book=book)
        record.save()
    if category2_name != "":
        category2 = Category.objects.filter(name=category2_name).first()
        if category2 == None:
            category2 = Category(name=category2_name)
            category2.save()
        record = Categorisation(category=category2, book=book)
        record.save()
    if category3_name != "":
        category3 = Category.objects.filter(name=category3_name).first()
        if category3 == None:
            category3 = Category(name=category3_name)
            category3.save()
        record = Categorisation(category=category3, book=book)
        record.save()


########################################          BOOK           ###############################################
class BookCreateView(View):
    model = Book
    template_name = "home/book_form.html"
    success_url=reverse_lazy('prototype:all')
    def get(self, request):
        if request.user.is_superuser:
            form = BookForm()
            publisher_list = Publisher.objects.all()
            author_list = Author.objects.all()
            category_list = Category.objects.all()
            ctx = { 'form':form, 'publisher_list' : publisher_list, 'author_list' : author_list, 'category_list' : category_list }
            return render(request, self.template_name, ctx)
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)

    def post(self, request):
        if request.user.is_superuser:
            if request.method == "POST":
                form = BookForm(request.POST, request.FILES or None)
                if form.is_valid():
                    publisher_name = request.POST.get("publisher")
                    publisher = Publisher.objects.filter(name=publisher_name).first()

                    if publisher == None:
                        publisher = Publisher(name=publisher_name)
                        publisher.save()
                    book_save = form.save(commit=False)
                    book_save.publisher = publisher
                    book_save.save()
                    aut_and_cat_check(request, book_save.id)
                    return redirect(self.success_url)                    ##################
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)
        form = BookForm()
        publisher_list = Publisher.objects.all()
        author_list = Author.objects.all()
        category_list = Category.objects.all()
        ctx = { 'form':form, 'publisher_list' : publisher_list, 'author_list' : author_list, 'category_list' : category_list }
        return render(request, self.template_name, ctx)

class BookUpdateView(View):
    model = Book
    template_name = "home/book_update.html"
    success_url=reverse_lazy('prototype:all')
    def get(self, request, pk):
        if request.user.is_superuser:
            book = get_object_or_404(Book, id=pk)
            form = BookForm(instance=book)
            publisher_list = Publisher.objects.all()
            author_list = Author.objects.all()
            category_list = Category.objects.all()
            context = { 'form' : form, 'book' : book, 'publisher_list' : publisher_list, 'author_list' : author_list, 'category_list' : category_list }
            return render(request, self.template_name, context)
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)

    def post(self, request, pk):
        if request.user.is_superuser:
            if request.method == "POST":
                book = get_object_or_404(Book, id=pk)
                form = BookForm(request.POST, request.FILES or None, instance=book)
                publisher_name = request.POST.get("publisher")
                if form.is_valid():
                    publisher = Publisher.objects.filter(name=publisher_name).first()
                    if publisher == None:
                        publisher = Publisher(name=publisher_name)
                        publisher.save()

                        # publisher_name = publisher_name.lower()
                        # title = form.cleaned_data.get('title')
                        # price = form.cleaned_data.get('price')
                        # description = form.cleaned_data.get('description')
                        # ctx = {'title':title, 'price': price, 'description':description, 'publisher':publisher_name}
                        # return render(request, 'home/test.html', ctx)

                    book_update = form.save(commit=False)
                    book_update.publisher = publisher
                    book_update.save()
                    aut_and_cat_update(request, book_update.id)
                    return redirect(self.success_url)                    #####################
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)
        book = get_object_or_404(Book, id=pk)
        form = BookForm(instance=book)
        publisher_list = Publisher.objects.all()
        author_list = Author.objects.all()
        category_list = Category.objects.all()
        context = { 'form' : form, 'book' : book, 'publisher_list' : publisher_list, 'author_list' : author_list, 'category_list' : category_list }
        return render(request, self.template_name, context)

class BookListView(View):
    def get(self, request):
        bk = Book.objects.all()
        ctx = {'book_list': bk}
        return render(request, 'home/book_list.html', ctx)

class BookDetailView(View):
    model = Book
    template_name = "home/book_detail.html"
    def get(self, request, pk) :
        x = Book.objects.get(id=pk)
        if request.user.is_authenticated:
            favorites = list()
            if request.user.is_authenticated:
                rows = request.user.favorite_books.values('id')
                favorites = [ row['id'] for row in rows ]

                basket = request.user.basket.all()
                if basket.count() == 0:
                    basket = Basket(user=request.user)
                    basket.save()
                else:
                    basket = basket[0]
                inbasket_books = basket.inbasket_books.all()

                author_records = Authority.objects.filter(book=x)
                category_records = Categorisation.objects.filter(book=x)
            context = { 'book' : x, 'favorites' : favorites, 'inbasket_books' : inbasket_books, 'author_records' : author_records, 'category_records' : category_records}
            return render(request, self.template_name, context)
        else:
            context = { 'book' : x }
            return render(request, self.template_name, context)

def stream_file(request, pk):
    book = get_object_or_404(Book, id=pk)
    response = HttpResponse()
    response['Content-Type'] = book.content_type
    response['Content-Length'] = len(book.picture)
    response.write(book.picture)
    return response

def book_delete(request, pk):
    book = get_object_or_404(Book, id=pk)
    if request.user.is_superuser:
        if request.method == "POST":
            book.delete()
            success_url=reverse_lazy('prototype:all')
            return redirect(success_url)                       ######################
        context = {'book': book}
        return render(request, 'home/book_delete.html', context)
    else:
        if request.user.is_authenticated:
            logout(request)
        return login_method(request)





########################################          PUBLISHER           ###############################################
class PublisherCreateView(View):
    model = Publisher
    template_name = "home/publisher_form.html"
    success_url=reverse_lazy('prototype:all')
    def get(self, request):
        if request.user.is_superuser:
            form = PublisherForm()
            ctx = { 'form': form }
            return render(request, self.template_name, ctx)
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)

    def post(self, request):
        if request.user.is_superuser:
            if request.method == "POST":
                form = PublisherForm(request.POST, request.FILES or None)
                if form.is_valid():
                    publisher_save = form.save(commit=False)
                    publisher_save.save()
                    return redirect(self.success_url)               ############################
                else:
                    raise Http404
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)
        form = PublisherForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

class PublisherUpdateView(View):
    model = Publisher
    template_name = "home/publisher_update.html"
    success_url=reverse_lazy('prototype:all')
    def get(self, request, pk):
        if request.user.is_superuser:
            publisher = get_object_or_404(Publisher, id=pk)
            form = PublisherForm(instance=publisher)
            context = { 'form' : form, 'publisher' : publisher }
            return render(request, self.template_name, context)
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)

    def post(self, request, pk):
        if request.user.is_superuser:
            if request.method == "POST":
                publisher = get_object_or_404(Publisher, id=pk)
                form = PublisherForm(request.POST, request.FILES or None, instance=publisher)
                if form.is_valid():
                    publisher_update = form.save(commit=False)
                    publisher_update.save()
                    return redirect(self.success_url)               #######################
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)

class PublisherListView(View):
    def get(self, request):
        pb = Publisher.objects.all()
        ctx = {'publisher_list': pb}
        return render(request, 'home/publisher_list.html', ctx)

class PublisherDetailView(View):
    model = Publisher
    template_name = "home/publisher_detail.html"
    def get(self, request, pk) :
        pb = Publisher.objects.get(id=pk)
        books = pb.books.all()
        context = { 'publisher': pb, 'books' : books }
        return render(request, self.template_name, context)

def view_publisher(request, pk):
    publisher = get_object_or_404(Publisher, id=pk)
    response = HttpResponse()
    response['Content-Type'] = publisher.content_type
    response['Content-Length'] = len(publisher.picture)
    response.write(publisher.picture)
    return response

def publisher_delete(request, pk):
    publisher = get_object_or_404(Publisher, id=pk)
    if request.user.is_superuser:
        if request.method == "POST":
            publisher.delete()
            success_url=reverse_lazy('prototype:all')
            return redirect(success_url)                            #######################
        context = {'publisher': publisher}
        return render(request, 'home/publisher_delete.html', context)
    else:
        if request.user.is_authenticated:
            logout(request)
        return login_method(request)




########################################          AUTHOR           ###############################################
class AuthorCreateView(View):
    model = Author
    template_name = "home/author_form.html"
    success_url=reverse_lazy('prototype:all')
    def get(self, request):
        if request.user.is_superuser:
            form = AuthorForm()
            ctx = { 'form': form }
            return render(request, self.template_name, ctx)
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)

    def post(self, request):
        if request.user.is_superuser:
            if request.method == "POST":
                form = AuthorForm(request.POST, request.FILES or None)
                if form.is_valid():
                    author_save = form.save(commit=False)
                    author_save.save()
                    return redirect(self.success_url)                          ###########################
                else:
                    raise Http404
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)
        form = AuthorForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

class AuthorUpdateView(View):
    model = Author
    template_name = "home/author_update.html"
    success_url=reverse_lazy('prototype:all')
    def get(self, request, pk):
        if request.user.is_superuser:
            author = get_object_or_404(Author, id=pk)
            form = AuthorForm(instance=author)
            context = { 'form' : form, 'author' : author }
            return render(request, self.template_name, context)
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)

    def post(self, request, pk):
        if request.user.is_superuser:
            if request.method == "POST":
                author = get_object_or_404(Author, id=pk)
                form = AuthorForm(request.POST, request.FILES or None, instance=author)
                if form.is_valid():
                    author_update = form.save(commit=False)
                    author_update.save()
                    return redirect(self.success_url)               #######################
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)

class AuthorListView(View):
    def get(self, request):
        at = Author.objects.all()
        ctx = {'author_list': at}
        return render(request, 'home/author_list.html', ctx)

class AuthorDetailView(View):
    model = Author
    template_name = "home/author_detail.html"
    def get(self, request, pk) :
        a = Author.objects.get(id=pk)
        books = a.written_books.all()
        context = { 'author': a, 'books' : books }
        return render(request, self.template_name, context)

def view_author(request, pk):
    author = get_object_or_404(Author, id=pk)
    response = HttpResponse()
    response['Content-Type'] = author.content_type
    response['Content-Length'] = len(author.picture)
    response.write(author.picture)
    return response

def author_delete(request, pk):
    author = get_object_or_404(Author, id=pk)
    if request.user.is_superuser:
        if request.method == "POST":
            author.delete()
            success_url=reverse_lazy('prototype:all')
            return redirect(success_url)                               #####################
        context = {'author': author}
        return render(request, 'home/author_delete.html', context)
    else:
        if request.user.is_authenticated:
            logout(request)
        return login_method(request)




########################################          CATEGORY           ###############################################
class CategoryCreateView(View):
    model = Category
    template_name = "home/category_form.html"
    success_url=reverse_lazy('prototype:all')
    def get(self, request):
        if request.user.is_superuser:
            form = CategoryForm()
            ctx = { 'form': form }
            return render(request, self.template_name, ctx)
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)

    def post(self, request):
        if request.user.is_superuser:
            if request.method == "POST":
                form = CategoryForm(request.POST)
                if form.is_valid():
                    category_save = form.save()
                    return redirect(self.success_url)                             #################
                else:
                    raise Http404
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)
        form = CategoryForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

class CategoryUpdateView(View):
    model = Author
    template_name = "home/category_update.html"
    success_url=reverse_lazy('prototype:all')
    def get(self, request, pk):
        if request.user.is_superuser:
            category = get_object_or_404(Category, id=pk)
            form = CategoryForm(instance=category)
            context = { 'form' : form, 'category' : category }
            return render(request, self.template_name, context)
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)

    def post(self, request, pk):
        if request.user.is_superuser:
            if request.method == "POST":
                category = get_object_or_404(Category, id=pk)
                form = CategoryForm(request.POST, instance=category)
                if form.is_valid():
                    category_update = form.save()
                    return redirect(self.success_url)                         #####################
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)

class CategoryListView(View):
    def get(self, request):
        cg = Category.objects.all()
        ctx = {'category_list': cg}
        return render(request, 'home/category_list.html', ctx)

class CategoryDetailView(View):
    model = Category
    template_name = "home/category_detail.html"
    def get(self, request, pk) :
        c = Category.objects.get(id=pk)
        books = c.related_books.all()
        context = { 'category': c, 'books' : books }
        return render(request, self.template_name, context)

def category_delete(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.user.is_superuser:
        if request.method == "POST":
            category.delete()
            success_url=reverse_lazy('prototype:all')
            return redirect(success_url)                                   #################
        context = {'category': category}
        return render(request, 'home/category_delete.html', context)
    else:
        if request.user.is_authenticated:
            logout(request)
        return login_method(request)






########################################          BASKET           ###############################################
class BasketDetailView(View):
    model = Basket
    template_name = "home/basket_detail.html"
    def get(self, request):
        if request.user.is_authenticated:
            basket = request.user.basket.all()
            if basket.count() == 0:
                basket = Basket(user=request.user)
                basket.save()
            else:
                basket = basket[0]

            # form = BasketRecordForm()
            records = basket.records.all()
            inbasket_books = basket.inbasket_books.all()
            context = { 'inbasket_books' : inbasket_books, 'records' : records, 'basket' : basket } #, 'form' : form
            return render(request, self.template_name, context)
        else:
            return login_method(request)

def amount_update(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            basket = request.user.basket.all()[0]
            # book_id = request.POST.get("book_id")
            book = Book.objects.get(id=pk)
            # record = get_object_or_404(BasketRecord, basket = basket, book = book)
            record = BasketRecord.objects.get(basket = basket, book = book)

            amount = request.POST.get("amount")
            record.amount = amount
            record.total = record.tot()
            record.save()
            update_total(request)

            records = basket.records.all()
            inbasket_books = basket.inbasket_books.all()
            context = { 'inbasket_books' : inbasket_books, 'records' : records, 'basket' : basket }
            return render(request, "home/basket_detail.html", context)
    else:
        return login_method(request)

def update_total(request):
    basket = request.user.basket.all()[0]
    sum_total = BasketRecord.objects.filter(basket=basket).aggregate(Sum('total'))['total__sum']
    if sum_total != None:
        basket.total = sum_total + basket.shipping
    else:
        basket.total = 0
    basket.save()

class AddIntoBasket(View):
    model = Basket
    template_name = "home/basket_detail.html"
    success_url=reverse_lazy('prototype:basket')
    def get(self, request, pk):
        if request.user.is_authenticated:
            basket = request.user.basket.all()
            if basket.count() == 0:
                basket = Basket(user=request.user)
                basket.save()
            else:
                basket = basket[0]

            book = get_object_or_404(Book, id=pk)
            record = BasketRecord(basket = basket, book = book)
            record.save()
            record = BasketRecord.objects.get(basket = basket, book = book)
            record.total = record.tot()
            record.save()
            update_total(request)

            return redirect(self.success_url)                                   ################
            # records = basket.records.all()
            # inbasket_books = basket.inbasket_books.all()
            # context = { 'inbasket_books' : inbasket_books, 'records' : records, 'basket' : basket }
            # return render(request, self.template_name, context)
        else:
            return login_method(request)

class DeleteOutofBasket(View):
    model = Basket
    template_name = "home/basket_detail.html"
    success_url=reverse_lazy('prototype:basket')
    def get(self, request, pk):
        if request.user.is_authenticated:
            basket = request.user.basket.all()[0]
            book = get_object_or_404(Book, id=pk)
            record = BasketRecord.objects.get(basket = basket, book = book).delete()

            update_total(request)
            return redirect(self.success_url)                                   ###################
            # records = basket.records.all()
            # inbasket_books = basket.inbasket_books.all()
            # context = { 'inbasket_books' : inbasket_books, 'records' : records, 'basket' : basket }
            # return render(request, self.template_name, context)
        else:
            return login_method(request)





########################################          ORDER           ###############################################
class ConfirmOrderView(View): #new
    model = Order
    template_name = "home/order_detail.html"
    success_url=reverse_lazy('prototype:orders')
    def get(self, request):
        if request.user.is_authenticated:
            basket = request.user.basket.all()[0]
            inbasket_books = basket.inbasket_books.all()
            order = Order(user=request.user)
            order.total = basket.total
            order.save()
            for book in inbasket_books:
                basket_record = BasketRecord.objects.get(basket = basket, book = book)
                amount = basket_record.amount
                total = basket_record.total
                record = OrderRecord(order = order, book = book, amount = amount, total=total)
                record.save()

            basket = Basket.objects.get(user=request.user).delete()
            return redirect(self.success_url)
            # return redirect(self.success_url, pk=order.id)
            # inorder_books = order.inorder_books.all()
            # records = order.records.all()
            # context = { 'inorder_books' : inorder_books, 'records' : records, 'order' : order }
            # return render(request, self.template_name, context)
        else:
            return login_method(request)


class OrderListView(View):
    model = Order
    template_name = "home/order_list.html"
    def get(self, request):
        if request.user.is_authenticated:
            orders = Order.objects.all()
            context = { 'orders' : orders }
            return render(request, self.template_name, context)
        else:
            return login_method(request)

class HistoryView(View):
    model = Order
    template_name = "home/history.html"
    def get(self, request):
        if request.user.is_authenticated:
            orders = Order.objects.all()
            context = { 'orders' : orders }
            return render(request, self.template_name, context)
        else:
            return login_method(request)

class OrderDetailView(View):
    model = Order
    template_name = "home/order_detail.html"
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        if request.user == order.user or request.user.is_superuser:
            records = order.records.all()
            inorder_books = order.inorder_books.all()
            address = AddressRecord.objects.filter(user=request.user).first()

            form = OrderForm(instance=order)
            context = { 'inorder_books' : inorder_books, 'records' : records, 'form' : form, 'order' : order, 'address' : address }
            return render(request, self.template_name, context)
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)

    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        if request.user == order.user:
            if request.method == "POST":
                form = OrderForm(request.POST, request.FILES or None, instance=order)
                if form.is_valid():
                    order.status = "รอการตรวจสอบการชำระเงิน"
                    order_save = form.save(commit=False)
                    order_save.save()

                    records = order.records.all()
                    inorder_books = order.inorder_books.all()
                    context = { 'inorder_books' : inorder_books, 'records' : records, 'order' : order}
                    return render(request, self.template_name, context)

            address = AddressRecord.objects.filter(user=request.user).first()
            records = order.records.all()
            inorder_books = order.inorder_books.all()

            form = OrderForm(instance=order)
            context = { 'inorder_books' : inorder_books, 'records' : records, 'form' : form, 'order' : order, 'address' : address }
            return render(request, self.template_name, context)
        else:
            if request.user.is_authenticated:
                logout(request)
            return login_method(request)

def order_delete(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.user == order.user or request.user.is_superuser:
        if request.method == "POST":
            order.delete()
            success_url=reverse_lazy('prototype:all')
            return redirect(success_url)                                    ###################
        context = {'order': order}
        return render(request, 'home/order_delete.html', context)
    else:
        if request.user.is_authenticated:
            logout(request)
        return login_method(request)

def admin_confirm(request, pk):
    if request.method == "POST":
        order = Order.objects.get(id=pk)
        post_code = request.POST.get("post_code")
        order.post_code = post_code
        order.status = "จัดส่งแล้ว"
        order.save()

        success_url=reverse_lazy('prototype:orders')
        return redirect(success_url)
        # return redirect(success_url, pk=order.id)
        # records = order.records.all()
        # inorder_books = order.inorder_books.all()
        # context = { 'inorder_books' : inorder_books, 'records' : records, 'order' : order }
        # return render(request, 'home/order_detail.html', context)
    elif request.user.is_superuser:
        order = Order.objects.get(id=pk)
        if order.status == "รอการตรวจสอบการชำระเงิน":
            order.status = "ยืนยันการชำระเงิน รอการจัดส่ง"
        # elif order.status == "ยืนยันการชำระเงิน รอการจัดส่ง":
        #     order.status = "จัดส่งแล้ว"
        order.save()

        success_url=reverse_lazy('prototype:orders')
        return redirect(self.success_url)
        # return redirect(success_url, pk=order.id)
        # records = order.records.all()
        # inorder_books = order.inorder_books.all()
        # context = { 'inorder_books' : inorder_books, 'records' : records, 'order' : order }
        # return render(request, 'home/order_detail.html', context)
    else:
        if request.user.is_authenticated:
            logout(request)
        return login_method(request)

def view_payment(request, pk):
    order = get_object_or_404(Order, id=pk)
    response = HttpResponse()
    response['Content-Type'] = order.content_type
    response['Content-Length'] = len(order.payment)
    response.write(order.payment)
    return response





########################################          FAV           ###############################################
class AddFavoriteView(View):
    model = Book
    template_name = "home/book_detail.html"
    def get(self, request, pk) :
        if request.user.is_authenticated:
            print("Add PK",pk)
            b = get_object_or_404(Book, id=pk)
            fav = Fav(book=b, user=request.user)
            try:
                fav.save()
                favorites = list()
                x = Book.objects.get(id=pk)
                if request.user.is_authenticated:
                    rows = request.user.favorite_books.values('id')
                    favorites = [ row['id'] for row in rows ]
                context = { 'book' : x, 'favorites' : favorites }
                return render(request, self.template_name, context)
            except IntegrityError as e:
                pass
            return HttpResponse()
        else:
            return login_method(request)

class DeleteFavoriteView(View):
    model = Book
    template_name = "home/book_detail.html"
    def get(self, request, pk) :
        if request.user.is_authenticated:
            print("Delete PK",pk)
            b = get_object_or_404(Book, id=pk)
            try:
                fav = Fav.objects.get(book=b, user=request.user).delete()
                favorites = list()
                x = Book.objects.get(id=pk)
                if request.user.is_authenticated:
                    rows = request.user.favorite_books.values('id')
                    favorites = [ row['id'] for row in rows ]
                context = { 'book' : x, 'favorites' : favorites }
                return render(request, self.template_name, context)
            except Fav.DoesNotExist as e:
                pass
            return HttpResponse()
        else:
            return login_method(request)

def favorites_view(request):
    template_name = "home/favorites.html"
    favorite_books = request.user.favorite_books.all()
    context = { 'favorite_books' : favorite_books }
    return render(request, template_name, context)

