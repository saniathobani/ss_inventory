from django.shortcuts import render,  redirect
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.
from .models import Lot, Expenses
from django.db.models import Sum
from .forms import LotForm, ExpensesForm
from django.contrib.auth.models import User
from django.contrib import auth
from .decorator import allowed_users, admin_only
from django.contrib import messages
from django.contrib.auth import login, logout


def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password= password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Logged In Successfully")
            return redirect('home')      
        else:
            messages.info(request, "Incorrect Credentials Or Authentication")
            return redirect('login')
    return  render(request, 'login.html')



def logoutUser(request):
        logout(request)
        return redirect('login')
   

@allowed_users(allow=['admin', 'other'])
def home(request):

    lots = Lot.objects.all().order_by('-purchased_date')
   # lots=  lotse.extra(select={'result': 'quantity * rate - extra_expenses'})
    

    paginator = Paginator(lots, 10)
    page = request.GET.get('page')
    paged_lots = paginator.get_page(page)


    tot_invest = 0
    tot_stock = 0
    tot_available = 0
    tot_sold = 0


    for lot in lots:
        tot_invest += lot.total
        tot_stock += lot.quantity

    lot_avai = lots.filter(status__iexact = 'available')
    tot_available = lot_avai.aggregate(Sum('quantity'))['quantity__sum']
    tot_sold = lots.filter(status__iexact = 'sold').aggregate(Sum('quantity'))['quantity__sum']

    lot = Lot.objects.filter(sold_at__isnull=False)
    lotsold =  lot.extra(select={'soldtot': 'quantity * sold_at'})
    
    ptot = 0
    stot = 0
    for lot in lotsold:
        stot += lot.soldtot
        ptot += lot.total

    profit = stot - ptot
    
    context = {

        'lots': paged_lots,
        'tot_invest':tot_invest,
        'tot_stock':tot_stock,
        'tot_available':tot_available,
        'tot_sold':tot_sold,
        'profit':profit,
        
    }



    return render(request, 'inventory/home.html', context)

@allowed_users(allow=['admin'])
def expenses(request):
    exs = Expenses.objects.all().order_by('-date')

    totdebit = Expenses.objects.filter(entry__iexact = 'Debited').aggregate(Sum('amount'))['amount__sum']
    totcredit = Expenses.objects.filter(entry__iexact = 'Credited').aggregate(Sum('amount'))['amount__sum']
    context = {
        'expenses':exs,
        'totdebit':totdebit,
        'totcredit':totcredit
    }
    return render(request, 'expenses/expenses.html', context)


@allowed_users(allow=['admin'])
def createExpenses(request):
    form = ExpensesForm()
    if request.method =='POST':
        form = ExpensesForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')

    context={'form':form}

    return render(request, 'expenses/expenses_form.html', context)
@allowed_users(allow=['admin'])
def updateExpenses(request, pk):
    this_e = Expenses.objects.get(id=pk)
    form = ExpensesForm(instance=this_e)
    if request.method =='POST':
        form = ExpensesForm(request.POST, instance=this_e)
        if form.is_valid:
            form.save()
            return redirect('expenses')
    context={'form':form,}
    return render(request, 'expenses/expenses_form.html', context)

@allowed_users(allow=['admin'])
def deleteExpenses(request, pk):
    this = Expenses.objects.get(id=pk)
    if request.method == 'POST':
        this.delete()
        return redirect('expenses')

    context = {'item':this,}
    return render(request, 'expenses/e_delete.html', context)

@allowed_users(allow=['admin'])
def eSearch(request):
    queryset_list = Expenses.objects.order_by('-date')
    if 'keywords' in request.GET:
        keywords= request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    if 'entry' in request.GET:
        entry= request.GET['entry']
        if entry:
            queryset_list = queryset_list.filter(entry__iexact=entry)
        
    if 'handler' in request.GET:
        handler= request.GET['handler']
        if handler:
            queryset_list = queryset_list.filter(handler__iexact=handler)

    if 'date' in request.GET:
        date= request.GET['date']
        if date:
            queryset_list = queryset_list.filter(date__icontains=date)

    if 'type_of_transaction' in request.GET:
        type_of_transaction= request.GET['type_of_transaction']
        if type_of_transaction:
            queryset_list = queryset_list.filter(type_of_transaction__iexact=type_of_transaction) 
    
    totdebit = queryset_list.filter(entry__iexact = 'Debited').aggregate(Sum('amount'))['amount__sum']
    totcredit = queryset_list.filter(entry__iexact = 'Credited').aggregate(Sum('amount'))['amount__sum']

    

    context ={
        'expenses':queryset_list,
        'totdebit':totdebit,
        'totcredit':totcredit,
        'values':request.GET,
    }
    return render(request, 'expenses/e_search.html', context)


@allowed_users(allow=['admin'])
def search(request):


    queryset_list = Lot.objects.order_by('-purchased_date')
    if 'keywords' in request.GET:
        keywords= request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    if 'scrap_category' in request.GET:
        scrap_category= request.GET['scrap_category']
        if scrap_category:
            queryset_list = queryset_list.filter(scrap_category__iexact=scrap_category)
        

    if 'purchased_date' in request.GET:
        purchased_date= request.GET['purchased_date']
        if purchased_date:
            queryset_list = queryset_list.filter(purchased_date__lte=purchased_date)

    if 'status' in request.GET:
        status= request.GET['status']
        if status:
            queryset_list = queryset_list.filter(status__lte=status) 

        tot_invest = 0
        tot_stock = 0
        tot_available = 0
        tot_sold = 0

        lots = queryset_list


        for lot in lots:
            tot_invest += lot.total
            tot_stock += lot.quantity

        lot_avai = queryset_list.filter(status__iexact = 'available')
        tot_available = lot_avai.aggregate(Sum('quantity'))['quantity__sum']
        tot_sold = queryset_list.filter(status__iexact = 'sold').aggregate(Sum('quantity'))['quantity__sum']

        lot = queryset_list.filter(sold_at__isnull=False)
        lotsold =  lot.extra(select={'soldtot': 'quantity * sold_at'})
        
        ptot = 0
        stot = 0
        for lot in lotsold:
            stot += lot.soldtot
            ptot += lot.total

        profit = stot - ptot

    context ={
        'lots':queryset_list,
         'tot_invest':tot_invest,
        'tot_stock':tot_stock,
        'tot_available':tot_available,
        'tot_sold':tot_sold,
        'profit':profit,
        'values':request.GET,
        

    }
    return render(request, 'inventory/search.html', context)


@allowed_users(allow=['admin'])
def createLot(request):
    form = LotForm()
    if request.method =='POST':
        form = LotForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')


    context={'form':form}

    return render(request, 'inventory/lot_form.html', context)
@allowed_users(allow=['admin'])
def updateLot(request, pk):
    this_lot = Lot.objects.get(id=pk)
    form = LotForm(instance=this_lot)
    if request.method =='POST':
        form = LotForm(request.POST, instance=this_lot)
        if form.is_valid:
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'inventory/lot_form.html', context)
@allowed_users(allow=['admin'])
def deleteLot(request, pk):
    this_lot = Lot.objects.get(id=pk)
    if request.method == 'POST':
        this_lot.delete()
        return redirect('home')

    context = {'item':this_lot,}
    return render(request, 'inventory/delete.html', context)
