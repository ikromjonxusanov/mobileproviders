from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm as UserForm

from .decorators import *
from .forms import *
from .models import *
from django.forms import inlineformset_factory

# Create your views here.

@allowed_users(allowed_roles=["provider"])
def registerDiller(request):    
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        dillersForm = DealerForm(data=request.POST)
        if user_form.is_valid() and dillersForm.is_valid():
            try:
                user = user_form.save()
                user.set_password(user.password)
                group = Group.objects.get(name='dealer')
                user.groups.add(group)
                user.save()
            except:
                return redirect("/registration/dealer/")
            try:
                dillers = dillersForm.save(commit=False)
                dillers.user = user
                try:
                    dillers.provider = Provider.objects.get(user=request.user)
                except:
                    pass
                dillers.save()
            except:
                user.delete()
                return redirect("/registration/dealer/")
            return redirect("/login/")
        else:
            messages.info(request, user_form.errors)
    else:
        user_form = UserForm()
        dillersForm = DealerForm()

    return render(request, 'registration.html', context={'user_form': user_form,"registered": registered, 'appForm': dillersForm} )
    
@allowed_users(allowed_roles=["admin"])
def registerPro(request):    
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        providerForm = ProviderForm(data=request.POST)

        if user_form.is_valid() and providerForm.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            group = Group.objects.get(name='provider')
            user.groups.add(group)
            user.is_staff = True
            user.save()
            provider = providerForm.save(commit=False)
            provider.user = user

            provider.save()
            return redirect("/login/")
        else:
            messages.info(request, user_form.errors)
    else:
        user_form = UserForm()
        providerForm = ProviderForm()
    return render(request, 'registration.html',
                    context={'user_form': user_form,"registered": registered, 'appForm': providerForm} )
 
@allowed_users(allowed_roles=['admin', 'provider'])
def registerDealler(request):    
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        dealerForm = DealerForm(data=request.POST)

        if user_form.is_valid() and dealerForm.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            group = Group.objects.get(name='dealer')
            user.groups.add(group)
            user.save()
            dealer = dealerForm.save(commit=False)
            dealer.user = user
            provider = Provider.objects.get(user=request.user)
            dealer.provider = provider
            dealer.save()
            return redirect(f"/providers/{provider.id}")
        else:
            messages.info(request, user_form.errors)
    else:
        user_form = UserForm()
        dealerForm = DealerForm()
    return render(request, 'registration.html',
                    context={'user_form': user_form,"registered": registered, 'appForm': dealerForm} )
 

@logout_required
def user_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect("/")

        else:
            print("SOMEONE TRIED TO LOGIN and FIELD!")
            print(f"Username: {username} and password: {password}")
            messages.info(request, "Username OR Password is incurrent")
    # print(messages)
    return render(request, "login.html",
                    {})
@login_required
def user_logout(request):
    logout(request)
    return redirect('/')

def home(request):
    return render(request, "index.html")

@allowed_users(allowed_roles=['admin', 'provider'])
def providerSettings(request):
    provider = Provider.objects.get(user=request.user) 
    form = ProviderForm(instance=provider)
    if request.method == "POST":
        form = ProviderForm(instance=provider, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"/providers/{provider.id}")
    return render(request, 'Providers/providerSettings.html', {'form':form})

def providers(request):
    providers = Provider.objects.order_by('-startDate')
    return render(request, 'Providers/providers.html', {"providers":providers})

def provider(request, pk):
    provider = Provider.objects.get(id=pk)
    codes = Code.objects.filter(provider=provider)
    number = Number.objects.all()
    numbers = []
    for item in number:
        for code in codes:
            if item.code == code:
                numbers.append(item)
    return render(request, 'Providers/provider.html', {"provider":provider, "numbers":numbers})

def numberCreate(request, pk):
    provider = Provider.objects.get(id=pk)
    codes = Code.objects.filter(provider=provider)
    numberForm = NumberForm()
    if request.method == "POST":
        numberForm = NumberForm(request.POST)
        print(request.POST)
        if numberForm.is_valid():
            numberForm.save()
            return redirect(f"/providers/{pk}")

    return render(request, "Providers/numbers/numberCreate.html", context={
        "form": numberForm, 'codes':codes
    })
@allowed_users(allowed_roles=['admin', 'provider', 'dealer'])
def numbers(request):
    if request.user.groups.all()[0].name == 'dealer':
        dealer = Dealer.objects.get(user=request.user)
        codes = Code.objects.filter(provider=dealer.provider)
        number = Number.objects.all()
        numbers = []
        for item in number:
            for code in codes:
                if item.code == code:
                    numbers.append(item)
    elif request.user.groups.all()[0].name == 'provider':
        codes = Code.objects.filter(provider=request.user.provider)
        number = Number.objects.all()
        numbers = []
        for item in number:
            for code in codes:
                if item.code == code:
                    numbers.append(item)
    elif request.user.groups.all()[0].name == 'admin':
        numbers = Number.objects.all()
    return render(request, 'Providers/numbers/numbers.html', {"numbers":numbers})


@allowed_users(allowed_roles=['dealer'])
def numberBuy(request, pk):

    print(request.user.dealer)
    # provider = Provider.objects.get(id=pk)
    # codes = Code.objects.filter(provider=provider)
    try:
        number = Number.objects.get(id=pk)
        print(number.status)
        if number.status:
            buy = True
        else:
            buy = False
        code = Code.objects.get(code=number.code.code)

        provider1 = Provider.objects.get(code=code)
        dealers = Dealer.objects.filter(provider=provider1)
        print(request.user.dealer in dealers)
        if request.user.dealer in dealers:

            form = ClientForm()
            if request.method == "POST":
                form = ClientForm(request.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    number.status = True
                    number.save()
                    form.number = number
                    form.save()
                    return redirect('numbers')
            return render(request, "Providers/numbers/numberBuy.html",
                          {
                              'form': form, 'buy': buy, 'number': number,
                          })
        else:
            return render(request, '404.html')
    except:
        return render(request, '404.html')

@allowed_users(allowed_roles=['admin', 'provider'])
def clients(request):
    if request.user.is_superuser:
        clients = Client.objects.all()
    else:
        codes = Code.objects.filter(provider=request.user.provider)
        numbers = []
        for item in codes:
            numbers.extend(list(Number.objects.filter(code=item)))

        clients = []
        for item in numbers:
            client = list(Client.objects.filter(number=item))
            clients.extend(client)
    return render(request, 'Providers/clients/clients.html', {'clients':clients})
