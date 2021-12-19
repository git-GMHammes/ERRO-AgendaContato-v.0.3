from django.urls import path
from . import views

urlpatterns = [
    # -------- ↓ Arq view.py
    path('', views.index, name='index'),
    # def index(): - ↑ do arq view.py
    path('<int:contato_id>', views.verContato, name='verContato'),
    # Tag HTML ↑ com ID. Novo metodo ↑ para a view.py
    # <int:contato_id> vai para depois da request da função verContato.
    path('busca/', views.busca, name='busca'),
    
]
