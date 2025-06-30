from rest_framework import viewsets # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from .models import Cliente, Proyecto, MiembroEquipo, Rol, Tarea
from .serializers import ClienteSerializer, ProyectoSerializer, MiembroEquipoSerializer, RolSerializer, TareaSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

class RolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated]

class ProyectoViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

class MiembroEquipoViewSet(viewsets.ModelViewSet):
    serializer_class = MiembroEquipoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Solo proyectos donde usuario es miembro para seguridad
        return MiembroEquipo.objects.filter(proyecto_miembros_equipo_user=user).distinct()

class TareaViewSet(viewsets.ModelViewSet):
    serializer_class = TareaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Tareas en proyectos donde usuario es miembro
        return Tarea.objects.filter(proyecto_miembros_equipo_user=user).distinct()
####
from django.shortcuts import render
from django.views.decorators.http import require_GET

@require_GET
def index(request):
    return render(request, 'core/index.html')