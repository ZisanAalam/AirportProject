from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import UserPasswordResetForm, UserSetPasswordForm
from django.views.i18n import JavaScriptCatalog
from . decorators import unauthenticated_user


urlpatterns = [
    path('', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('changepass/', views.user_change_pass, name='changepass'),
    path('editprofile/', views.user_profile_edit, name='editprofile'),
    path('addprofile/', views.user_profile_add, name='addprofile'),
    path('about/', views.About, name='about'),
    path('contact/', views.Contact, name='contact'),

    path('viewrunway/', views.view_runway, name='viewrunway'),
    path('editrunway/<int:id>', views.edit_runway, name='editrunway'),
    path('addrunway/', views.add_runway, name='addrunway'),
    path('deleterunway/<int:id>', views.delete_runway, name='deleterunway'),


    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="account/password_reset.html", form_class=UserPasswordResetForm),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="account/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="account/password_reset_form.html", form_class=UserSetPasswordForm),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="account/password_reset_done.html"),
         name="password_reset_complete"),


    path('ReportProblem/', unauthenticated_user(views.AddFaultView.as_view()),
         name='addfault'),
     path('ReportProblem/loactionpart-json/<str:location>/', unauthenticated_user(views.get_location_parts), name='loactionpart-json'),
    path('UpdateProblem/<int:id>',
         unauthenticated_user(views.updatefault), name='updatefault'),
    path('DeleteProblem/<int:id>',
         unauthenticated_user(views.deletefault), name='deletefault'),
    path('ViewProblem/', unauthenticated_user(views.ViewFault.as_view()), name='viewfault'),
    path('calcnav/', unauthenticated_user(views.calculate_nav_parameter), name='calcnav'),

    


]
