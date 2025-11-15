from django.core.management.base import BaseCommand
from django.db import transaction

from myadmin.models import Departamento, Municipio


class Command(BaseCommand):
    help = "Crea datos iniciales de Departamentos y Municipios."

    def handle(self, *args, **options):
        if Departamento.objects.exists() or Municipio.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Ya existen Departamentos o Municipios, no se generan datos."
                )
            )
            return

        datos = {
            ("01", "San Salvador"): [
                ("01", "San Salvador"),
                ("02", "Soyapango"),
                ("03", "Mejicanos"),
                ("04", "Ilopango"),
            ],
            ("02", "La Libertad"): [
                ("01", "Santa Tecla"),
                ("02", "Antiguo Cuscatlán"),
                ("03", "Colón"),
            ],
            ("03", "Santa Ana"): [
                ("01", "Santa Ana"),
                ("02", "Metapán"),
                ("03", "Chalchuapa"),
            ],
        }

        with transaction.atomic():
            for (dep_codigo, dep_nombre), municipios in datos.items():
                departamento = Departamento.objects.create(
                    codigo=dep_codigo,
                    nombre=dep_nombre,
                )
                for mun_codigo, mun_nombre in municipios:
                    Municipio.objects.create(
                        codigo=mun_codigo,
                        nombre=mun_nombre,
                        FK_departamento=departamento,
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "Se crearon Departamentos y Municipios de ejemplo correctamente."
            )
        )

