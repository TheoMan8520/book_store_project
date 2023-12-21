from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
# from django.contrib.auth.models import User

from taggit.managers import TaggableManager

# class Webuser(User):
#     address = models.CharField(
#         default="address",
#         max_length=100,
#         blank=True
#     )

class Author(models.Model):
    name = models.CharField(
        max_length=70
    )
    description = models.TextField(null=True, editable=True)
    tags = TaggableManager(blank=True)

    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')


    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(
        max_length=70
    )

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(
        max_length=70
    )
    description = models.TextField(null=True, editable=True)
    tags = TaggableManager(blank=True)

    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')

    def __str__(self):
        return self.name

class AddressRecord(models.Model):
    address = models.CharField(
        default="address",
        max_length=100,
        null=True,
        editable=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='address')

    def __str__(self):
        return self.address

class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    total = models.DecimalField(max_digits=7, decimal_places=2, null=True, editable=True)
    shipping = models.DecimalField(default=50, max_digits=7, decimal_places=2, null=True)

    def __str__(self):
        return self.id

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    shipping = models.DecimalField(default=50, max_digits=7, decimal_places=2, null=True)

    payment = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    destination = models.CharField(max_length=256, null=True,  editable=True)
    post_code = models.CharField(max_length=256, null=True,  editable=True)

    status = models.CharField(max_length=256, default="รอการชำระเงิน", editable=True)

    def __str__(self):
        return self.id

class Book(models.Model):
    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField()
    #Translator = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(blank=True)

    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')

    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Fav', related_name='favorite_books')

    basket = models.ManyToManyField(Basket,
        through='BasketRecord', related_name='inbasket_books')
    order = models.ManyToManyField(Order,
        through='OrderRecord', related_name='inorder_books')

    author = models.ManyToManyField(Author,
        through='Authority', related_name='written_books')
    category = models.ManyToManyField(Category,
        through='Categorisation', related_name='related_books')

    publisher = models.ForeignKey(Publisher, null=True, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title



####################################        RELATIONSHIPS        ################################################
class Fav(models.Model) :
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favs_users')

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.book.title[:10])

class BasketRecord(models.Model):
    amount = models.IntegerField(default=1, editable=True)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name = "records")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=7, decimal_places=2, null=True, editable=True)

    def tot(self): #new
        return float(self.amount) * float(self.book.price)

    class Meta:
        unique_together = ('basket', 'book')

    def __str__(self) :
        return 'basket %s from %s has %s'%(self.basket.id, self.basket.user.username, self.book.title[:10])

class OrderRecord(models.Model):
    amount = models.IntegerField(default=1, editable=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name = "records")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    def tot(self): #new
        return self.amount * self.book.price

    class Meta:
        unique_together = ('order', 'book')

    def __str__(self) :
        return 'order %s from %s has %s'%(self.order.id, self.order.user.username, self.book.title[:10])

class Authority(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('author', 'book')

    def __str__(self) :
        return '%s wrote %s'%(self.author.name, self.book.title[:10])

class Categorisation(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('category', 'book')

    def __str__(self) :
        return '%s is %s'%(self.book.title[:10], self.category.name)


# class Section(models.Model):
#     name = models.CharField(
#         max_length=70
#     )
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)

#     def __str__(self) :
#         return self.name