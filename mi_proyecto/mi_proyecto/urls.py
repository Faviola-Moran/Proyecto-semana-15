from django.contrib import admin
from django.urls import path, include
from core.views import index  # Corrección: "views" en lugar de "vlews"
from rest_framework.routers import DefaultRouter
from core.views import ClienteViewSet, MiembroEquipoViewSet, ProyectoViewSet, RolViewSet, TareaViewSet  # Nombres corregidos

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)  # Coherencia con el nombre del modelo
router.register(r'roles', RolViewSet)
router.register(r'proyectos', ProyectoViewSet)
router.register(r'miembros', MiembroEquipoViewSet)  # Corrección ortográfica
router.register(r'tareas', TareaViewSet)  # Nombre corregido

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # Corrección: "api-auth" en lugar de "api-anth"
    path('api/', include(router.urls)),  # ¡Incluye las URLs del router!
]