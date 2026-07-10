from django.core.management.base import BaseCommand
from django.utils import timezone
from embarcaciones.models import Embarcacion
from capitanes.models import Capitan
from usuarios.models import Usuario

class Command(BaseCommand):
    help = 'Carga datos iniciales para pruebas (sin precios de especies)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Cargando datos iniciales...')
        
        # 1. Crear usuarios de prueba
        if not Usuario.objects.filter(username='despachador1').exists():
            Usuario.objects.create_user(
                username='despachador1',
                email='despachador@bodega.com',
                password='123456',
                first_name='Juan',
                last_name='Pérez',
                rol='despachador'
            )
            self.stdout.write(self.style.SUCCESS('✓ Usuario despachador1 creado'))
        
        if not Usuario.objects.filter(username='receptor1').exists():
            Usuario.objects.create_user(
                username='receptor1',
                email='receptor@bodega.com',
                password='123456',
                first_name='María',
                last_name='González',
                rol='receptor'
            )
            self.stdout.write(self.style.SUCCESS('✓ Usuario receptor1 creado'))
        
        # 2. Crear embarcaciones de prueba
        embarcaciones = [
            {'nombre': 'La Esperanza', 'matricula': 'EMB-001', 'capacidad_kg': 5000, 'tipo': 'Lancha'},
            {'nombre': 'El Tiburón', 'matricula': 'EMB-002', 'capacidad_kg': 8000, 'tipo': 'Barco'},
            {'nombre': 'Mar Azul', 'matricula': 'EMB-003', 'capacidad_kg': 6000, 'tipo': 'Lancha'},
            {'nombre': 'Doña Rosa', 'matricula': 'EMB-004', 'capacidad_kg': 4500, 'tipo': 'Panga'},
        ]
        
        for emb in embarcaciones:
            if not Embarcacion.objects.filter(nombre=emb['nombre']).exists():
                Embarcacion.objects.create(**emb)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(embarcaciones)} embarcaciones creadas'))
        
        # 3. Crear capitanes de prueba
        capitanes = [
            {
                'nombre': 'Pedro Martínez',
                'documento': '8-123-456',
                'telefono': '6000-0001',
                'direccion': 'Calle Principal, Ciudad',
                'email': 'pedro@email.com'
            },
            {
                'nombre': 'Carlos López',
                'documento': '8-234-567',
                'telefono': '6000-0002',
                'direccion': 'Av. Central, Puerto',
                'email': 'carlos@email.com'
            },
            {
                'nombre': 'José Rodríguez',
                'documento': '8-345-678',
                'telefono': '6000-0003',
                'direccion': 'Barrio Los Pescadores',
                'email': 'jose@email.com'
            },
            {
                'nombre': 'Miguel Sánchez',
                'documento': '8-456-789',
                'telefono': '6000-0004',
                'direccion': 'Costa del Mar',
                'email': 'miguel@email.com'
            },
        ]
        
        for cap in capitanes:
            if not Capitan.objects.filter(documento=cap['documento']).exists():
                Capitan.objects.create(**cap)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(capitanes)} capitanes creados'))
        
        self.stdout.write(self.style.SUCCESS('Datos iniciales cargados correctamente'))
        self.stdout.write('Para agregar precios de especies, use el comando: python manage.py cargar_precios_especies.py')
