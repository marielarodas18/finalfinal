from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render, get_object_or_404, redirect,render_to_response
from .models import Post
from .models import Archivos
from .forms import PostForm
from .forms import ArchivoForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required()
def home(request):
    return render_to_response('home.html', {'user': request.user}, context_instance=RequestContext(request))

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
 
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = True
            user.is_active = True
 
            user.save()
 
            return HttpResponseRedirect(reverse('login')) 
    else:
        form = SignUpForm()
 
    data = {
        'form': form,
    }
    return render(request,"signup.html",data)

def entrada(request):
    form = ArchivoForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect('http://diegolguz.pythonanywhere.com/create/')
    context = {
        "form": form,
    }
    return render(request,"post_form.html",context)

def logout(request):
    return render(request,reverse('list'))

def login(request):
    return render(request,"login.html")

@login_required()
def post_create(request):
    form = PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.usuar = request.user
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request,"post_form.html",context)

def post_detail(request,id=None):
    usuario = request.user
    instance = get_object_or_404(Post,id=id)
    context = {
        "title": instance.titulo,
        "instance": instance,
        "usuario": usuario,
    }
    return render(request,"post_detail.html",context)


def post_list(request):
    usuario = request.user
    queryset_list = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(queryset_list, 5) 
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:    
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    if request.user.is_authenticated():
        context = {
            "object_list": queryset,
            "title": "XelaGangas"
        }
    else:
        context = {
            "title": "Inicie sesion para ver la lista de articulos"
        }
    return render(request,"post_list.html",context)

def post_list2(request):
    usuario = request.user
    queryset_list = Post.objects.all().order_by("-timestamp")
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(titulo__icontains=query)
        ).distinct()
        
    paginator = Paginator(queryset_list, 5) 
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:    
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    if request.user.is_authenticated():
        
        context = {
            "object_list": queryset,
            "title": "XelaGangas",
            "usuario": usuario,
        }
    else:
        context = {
            "title": "Inicie sesion para ver la lista de articulos"
        }
    return render(request,"post_list2.html",context)

@login_required()
def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None,instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.titulo,
        "instance": instance,
        "form": form,
    }
    return render(request,"post_form.html",context)

@login_required()
def post_delete(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        return redirect("main2")
    if not request.user.is_staff or not request.user.is_superuser:
        return redirect("main2")
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    return redirect("main")

def nopermiso(request):
    usuario = request.user
    query2 = Archivos.objects.filter(user = usuario.id)
    queryset_list = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(queryset_list, 5) 
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:    
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    if request.user.is_authenticated():
        
        context = {
            "object_list": queryset,
            "title": "XelaGangas",
            "usuario": usuario,
        }
    else:
        context = {
            "title": "Inicie sesion para ver la lista de articulos"
        }
    return render(request,"nopermiso.html",context) 
    