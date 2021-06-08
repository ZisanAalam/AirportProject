from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
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
    path('change password/', views.passchange.user_change_pass, name='changepass'),
    path('editprofile/', views.profile.user_profile_edit, name='editprofile'),
    #path('addprofile/', views.profile.user_profile_add, name='addprofile'),
    path('about us/', views.about.About, name='about'),
    path('contact us/', views.contact.Contact, name='contact'),

    path('viewrunway/', views.runway.view_runway, name='viewrunway'),
    path('editrunway/<int:id>', views.runway.edit_runway, name='editrunway'),
    path('addrunway/', views.runway.add_runway, name='addrunway'),
    path('deleterunway/<int:id>', views.runway.delete_runway, name='deleterunway'),

    path('faultmodule/', views.faultmodule.view_faultmodule, name='viewfaultmodule'),
    path('addfaultmodule/',views.faultmodule.add_faultmodule, name='addfaultmodule'),
    path('editfaultmodule/<int:id>', views.faultmodule.edit_faultmodule, name='editfaultmodule'),
    path('deletefaultmodule/<int:id>', views.faultmodule.delete_faultmodule, name='deletefaultmodule'),

    path('make/', views.make.view_make, name='viewmake'),
    path('addmake/',views.make.add_make, name='addmake'),
    path('editmake/<int:id>', views.make.edit_make, name='editmake'),
    path('deletemake/<int:id>', views.make.delete_make, name='deletemake'),

    path('model/', views.model.view_model, name='viewmodel'),
    path('addmodel/',views.model.add_model, name='addmodel'),
    path('editmodel/<int:id>', views.model.edit_model, name='editmodel'),
    path('deletemodel/<int:id>', views.model.delete_model, name='deletemodel'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="account/forgotpassword/password_reset.html", form_class=UserPasswordResetForm),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="account/forgotpassword/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="account/forgotpassword/password_reset_form.html", form_class=UserSetPasswordForm),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="account/forgotpassword/password_reset_done.html"),
         name="password_reset_complete"),


    path('ReportProblem/', unauthenticated_user(views.problem.AddFaultView.as_view()),
         name='addfault'),

    path('ReportProblem/loactionpart/<int:id>/',
         views.problem.get_location_parts, name='loactionpart-json'),
    path('ReportProblem/get_model/<int:id>/',
         views.problem.get_model, name='get_model'),

    path('updatefault/<int:id>',
         unauthenticated_user(views.problem.updatefault), name='updatefault'),
    path('deletefault/<int:id>',
         unauthenticated_user(views.problem.deletefault), name='deletefault'),
    path('view problem/', unauthenticated_user(views.problem.ViewFault.as_view()),
         name='viewfault'),
    path('PerformanceAnalysis/',
         unauthenticated_user(views.problem.calculate_nav_parameter), name='calcnav'),
    path('PerformanceAnalysis/get_model/<int:id>/',
         views.problem.get_model, name='get_model'),
    path('PerformanceAnalysis/get_data/',
         views.problem.nav_calculation, name='get_data'),

    path('ReportProblem/equiment/<int:id>/',
         views.equipment.get_equipment, name='get-equipment')
]
