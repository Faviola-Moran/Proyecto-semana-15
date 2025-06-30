from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)

    def _str_(self):
        return self.nombre

class Proyecto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    cliente = models.ForeignKey(Cliente, related_name='proyectos', on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    creado_por = models.ForeignKey(User, related_name='proyectos_creados', null=True, on_delete=models.SET_NULL)

    def _str_(self):
        return self.nombre

class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def _str_(self):
        return self.nombre

class MiembroEquipo(models.Model):
    user = models.ForeignKey(User, related_name='miembros_equipo', on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, related_name='miembros_equipo', on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, related_name='miembros_equipo', on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('user', 'proyecto')

    def _str_(self):
        return f"{self.user.username} ({self.rol.nombre if self.rol else 'Sin rol'}) en {self.proyecto.nombre}"

class Tarea(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('finalizada', 'Finalizada'),
    )
    proyecto = models.ForeignKey(Proyecto, related_name='tareas', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    asignados = models.ManyToManyField(MiembroEquipo, related_name='tareas_asignadas', blank=True)

    def _str_(self):
        return f"{self.titulo} [{self.estado}]"