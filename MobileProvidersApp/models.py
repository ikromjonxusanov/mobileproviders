from django.db.models import *
from django.contrib.auth.models import User

# Create your models here.

class Provider(Model):
    user = OneToOneField(User, null=True, blank=True, on_delete=SET_NULL)
    name = CharField(max_length=100, unique=True)
    profilePicture = ImageField(upload_to="profilePicture", default="default.png")
    description = TextField()
    startDate = DateField(auto_now_add=True)
    status = BooleanField(default=True)
    def __str__(self):
        return self.name

class Dealer(Model):
    user = OneToOneField(User, null=True, blank=True, on_delete=SET_NULL)
    name = CharField(max_length=100)
    description = TextField()
    startDate = DateField(auto_now_add=True)
    provider = ForeignKey(Provider, on_delete=CASCADE)

    def __str__(self):
        return self.name

class Category(Model):
    name = CharField(max_length=20)
    description = TextField()
    create_date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Code(Model):
    code = CharField(max_length=2)
    provider = ForeignKey(Provider, on_delete=CASCADE)
    create_date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

class Number(Model):
    number = CharField(max_length=7)
    code = ForeignKey(Code, on_delete=CASCADE)
    category = ForeignKey(Category, on_delete=CASCADE)
    status = BooleanField(default=False)
    create_date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return "+998"+str(self.code.code)+str(self.number)

class Client(Model):
    number = OneToOneField(Number, on_delete=CASCADE)
    fullname = CharField(max_length=255, null=True)
    passportID = CharField(max_length=10)
    address = CharField(max_length=255)
    startDate = DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.fullname