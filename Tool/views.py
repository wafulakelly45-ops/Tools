from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from  django.urls import reverse
from.models import Tool
from django import forms
from django.db import IntegrityError

# form for new adding new tool

class NewToolForm(forms.Form):
    Name = forms.CharField(label="Tool Name")
    cover =forms.FileField(label="AddImage")
    Description = forms.CharField(max_length=300)


# function to render the add form and add new tools
def add(request):
    if request.method == "POST":
        form = NewToolForm(request.POST, request.FILES)
        if form.is_valid():
            
            tool = Tool(
               Name=form.cleaned_data["Name"],
               cover=form.cleaned_data["cover"],
               Description=form.cleaned_data["Description"]
            )
            tool.save() 
            return HttpResponseRedirect(reverse("index")) 
            
        
        
    else:
        form = NewToolForm()      

    return render(request, "Tool/add.html", {
        "form": form
    })

# A function to render the User info page
def  data(request):
    return render(request,"Tool/user.html")





# renders the main page is the user is authenticated
def index(request):
    return render(request,"Tool/index.html",{
        "tools":Tool.objects.all()
    })

#function to view detail of the tool
# You must be authenticated to view  a tool
def tool(request, tool_id):
    tool =Tool.objects.get(id=tool_id)
    if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
    return render(request,"Tool/tool.html",{
        "tool":tool
    })
    

 # function to authenticate Users     
def login_view(request):
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "Tool/login.html",{
                "message":"Invalid Credentials"
            })

    return render(request,"Tool/login.html")
 # function to logout users
def logout_view(request):
    logout(request)
    return render(request, "Tool/login.html",{
        "message":"Logged Out"
    })