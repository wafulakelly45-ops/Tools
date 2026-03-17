from django .urls import path
from. import views

urlpatterns =[
    
    path("data/",views.data, name="data"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("<int:tool_id>", views.tool, name="tool"),
    path("add/",views.add ,name="add"),
    path("", views.index, name="index"),


   
]