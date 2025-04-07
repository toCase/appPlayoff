from django.urls import path

from .views import site, tournament, category, participants, competitions, cp, protocols

urlpatterns = [
    path("", site.index, name='index'),
    path("login", site.login, name='login'),
    path('logout', site.logout, name='logout'),
    path("register", site.register, name='register'),
    path('features', site.features, name='features'),
    path('about', site.about, name='about'),
    
    path('app_index', tournament.load, name='app_index'),
    path('app_tournament_add', tournament.add, name='app_tournament_add'),
    path('app_tournament_filter', tournament.filter, name='app_tournament_filter'),
    path('app_tournament_close', tournament.filter, name='app_tournament_close'),
    path('app_tournament_save/<str:pk>', tournament.save, name='app_tournament_save'),
    path('app_tournament_edit/<str:pk>', tournament.edit, name='app_tournament_edit'),
    path('app_tournament_delete/<str:pk>', tournament.delete, name='app_tournament_delete'),
    path('app_tournament_page/<str:page>', tournament.page, name='app_tournament_page'),
    
    path('app_category', category.load, name='app_category'),
    path('app_category_add', category.add, name='app_category_add'),
    path('app_category_filter', category.filter, name='app_category_filter'),
    path('app_category_close', category.filter, name='app_category_close'),
    path('app_category_save/<str:pk>', category.save, name='app_category_save'),
    path('app_category_edit/<str:pk>', category.edit, name='app_category_edit'),
    path('app_category_delete/<str:pk>', category.delete, name='app_category_delete'),
    path('app_category_page/<str:page>', category.page, name='app_category_page'),
    
    path('app_participants/<str:pk>', participants.load, name='app_participants'),
    path('app_participants_filter', participants.filter, name='app_participants_filter'),
    path('app_participants_add', participants.add, name='app_participants_add'),
    path('app_participants_clear', participants.clear, name='app_participants_clear'),
    path('app_participants_delete/<str:pk>', participants.delete, name='app_participants_delete'),
    path('app_participants_page/<str:page>', participants.page, name='app_participants_page'),
    path('app_participants_save', participants.save, name='app_participants_save'),
    path('app_participants_close', participants.filter, name='app_participants_close'),
    
    path('app_competitions/<str:pk>', competitions.load, name='app_competitions'),
    path('app_competitions_filter', competitions.filter, name='app_competitions_filter'),
    path('app_competitions_add', competitions.add, name='app_competitions_add'),
    path('app_competitions_edit/<str:pk>', competitions.edit, name='app_competitions_edit'),
    path('app_competitions_delete/<str:pk>', competitions.delete, name='app_competitions_delete'),
    path('app_competitions_save/<str:pk>', competitions.save, name='app_competitions_save'),
    path('app_competitions_page/<str:page>', competitions.page, name='app_competitions_page'),
    path('app_competitions_close', competitions.filter, name='app_competitions_close'),
    
    path('app_cp/<str:pk>', cp.load, name='app_cp'),
    path('app_cp_filter', cp.filter, name='app_cp_filter'),
    path('app_cp_add', cp.add, name='app_cp_add'),
    path('app_cp_edit/<str:pk>', cp.edit, name='app_cp_edit'),
    path('app_cp_delete/<str:pk>', cp.delete, name='app_cp_delete'),
    path('app_cp_save/<str:pk>', cp.save, name='app_cp_save'),
    path('app_cp_page/<str:page>', cp.page, name='app_cp_page'),
    path('app_cp_close', cp.filter, name='app_cp_close'),
    
    path('app_protocols/<str:pk>', protocols.protocols_generate, name='app_protocols'),
]
