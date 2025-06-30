from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cliente, Proyecto, MiembroEquipo, Rol, Tarea

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email', 'telefono', 'direccion']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre']

class MiembroEquipoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    rol = RolSerializer(read_only=True)
    rol_id = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all(), source='rol', write_only=True, allow_null=True, required=False)
    proyecto_id = serializers.PrimaryKeyRelatedField(queryset=Proyecto.objects.all(), source='proyecto', write_only=True)

    class Meta:
        model = MiembroEquipo
        fields = ['id', 'user', 'user_id', 'rol', 'rol_id', 'proyecto_id']

class ProyectoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all(), source='cliente', write_only=True)
    creado_por = UserSerializer(read_only=True)
    miembros_equipo = MiembroEquipoSerializer(many=True, read_only=True)

    class Meta:
        model = Proyecto
        fields = [
            'id', 'nombre', 'descripcion', 'cliente', 'cliente_id',
            'fecha_inicio', 'fecha_fin', 'creado_por', 'miembros_equipo',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['creado_por'] = user
        return super().create(validated_data)

class TareaSerializer(serializers.ModelSerializer):
    proyecto = ProyectoSerializer(read_only=True)
    proyecto_id = serializers.PrimaryKeyRelatedField(queryset=Proyecto.objects.all(), source='proyecto', write_only=True)
    asignados = MiembroEquipoSerializer(many=True, read_only=True)
    asignados_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=MiembroEquipo.objects.all(), source='asignados', write_only=True, required=False)

    class Meta:
         model = Tarea
    fields = [
        'id', 'titulo', 'descripcion', 'fecha_creacion', 'fecha_vencimiento',
        'estado', 'proyecto', 'proyecto_id', 'asignados', 'asignados_ids',
    ]