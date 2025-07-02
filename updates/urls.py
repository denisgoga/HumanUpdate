from django.urls import path
from .views import DashboardView, CreateUpdateView, RegisterView, LoginView, logout_view, ProfileView, TimelineView, StatsView, ExportPDFView, ExportMarkdownView, AskAIView, EditUpdateView, DeleteUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('timeline/', TimelineView.as_view(), name='timeline'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('export/pdf/', ExportPDFView.as_view(), name='export_pdf'),
    path('export/markdown/', ExportMarkdownView.as_view(), name='export_markdown'),
    path('ask-ai/', AskAIView.as_view(), name='ask_ai'),
    path('edit/<int:pk>/', EditUpdateView.as_view(), name='edit_update'),
    path('delete/<int:pk>/', DeleteUpdateView.as_view(), name='delete_update'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('add/', CreateUpdateView.as_view(), name='create_update'),
] 