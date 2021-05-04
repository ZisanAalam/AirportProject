from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import UserPasswordResetForm, UserSetPasswordForm
from django.views.i18n import JavaScriptCatalog
from . decorators import unauthenticated_user


urlpatterns = [
    path('', views.login.user_login, name='login'),
    path('home/', views.home.home_page, name='home'),
    path('signup/', views.signup.user_signup, name='signup'),
    path('logout/', views.logout.user_logout, name='logout'),
    path('profile/', views.profile.user_profile, name='profile'),
    path('changepass/', views.passchange.user_change_pass, name='changepass'),
    path('editprofile/', views.profile.user_profile_edit, name='editprofile'),
    path('addprofile/', views.profile.user_profile_add, name='addprofile'),
    path('about/', views.about.About, name='about'),
    path('contact/', views.contact.Contact, name='contact'),

    path('viewrunway/', views.runway.view_runway, name='viewrunway'),
    path('editrunway/<int:id>', views.runway.edit_runway, name='editrunway'),
    path('addrunway/', views.runway.add_runway, name='addrunway'),
    path('deleterunway/<int:id>', views.runway.delete_runway, name='deleterunway'),

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


    path('ReportProblem/', unauthenticated_user(views.problem.AddFaultView.as_view()),
         name='addfault'),
     
    path('ReportProblem/loactionpart-json/<int:id>/', views.problem.get_location_parts, name='loactionpart-json'),
    path('ReportProblem/get_model/<int:id>/',views.problem.get_model, name='get_model'),

    path('updatefault/<int:id>',
         unauthenticated_user(views.problem.updatefault), name='updatefault'),
    path('deletefault/<int:id>',
         unauthenticated_user(views.problem.deletefault), name='deletefault'),
    path('viewfault/', unauthenticated_user(views.problem.ViewFault.as_view()), name='viewfault'),
    path('calcnav/', unauthenticated_user(views.problem.calculate_nav_parameter), name='calcnav'),
    
    path('ReportProblem/equiment/<int:id>/',views.equipment.get_equipment,name='get-equipment')
]
