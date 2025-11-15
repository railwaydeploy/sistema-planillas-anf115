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

        # Listado basado en fuentes públicas (p.ej. Wikipedia "Municipios de El Salvador").
        # Los códigos son internos al sistema y no necesariamente estándares oficiales.
        datos = {
            # 01 - Ahuachapán
            ("01", "Ahuachapán"): [
                ("01", "Ahuachapán"),
                ("02", "Apaneca"),
                ("03", "Atiquizaya"),
                ("04", "Concepción de Ataco"),
                ("05", "El Refugio"),
                ("06", "Guaymango"),
                ("07", "Jujutla"),
                ("08", "San Francisco Menéndez"),
                ("09", "San Lorenzo"),
                ("10", "San Pedro Puxtla"),
                ("11", "Tacuba"),
                ("12", "Turín"),
            ],

            # 02 - Cabañas
            ("02", "Cabañas"): [
                ("01", "Cinquera"),
                ("02", "Dolores"),
                ("03", "Guacotecti"),
                ("04", "Ilobasco"),
                ("05", "Jutiapa"),
                ("06", "San Isidro"),
                ("07", "Sensuntepeque"),
                ("08", "Tejutepeque"),
                ("09", "Victoria"),
            ],

            # 03 - Chalatenango
            ("03", "Chalatenango"): [
                ("01", "Agua Caliente"),
                ("02", "Arcatao"),
                ("03", "Azacualpa"),
                ("04", "Chalatenango"),
                ("05", "Comalapa"),
                ("06", "Citalá"),
                ("07", "Concepción Quezaltepeque"),
                ("08", "Dulce Nombre de María"),
                ("09", "El Carrizal"),
                ("10", "El Paraíso"),
                ("11", "La Laguna"),
                ("12", "La Palma"),
                ("13", "La Reina"),
                ("14", "Las Vueltas"),
                ("15", "Nombre de Jesús"),
                ("16", "Nueva Concepción"),
                ("17", "Nueva Trinidad"),
                ("18", "Ojos de Agua"),
                ("19", "Potonico"),
                ("20", "San Antonio de la Cruz"),
                ("21", "San Antonio Los Ranchos"),
                ("22", "San Fernando"),
                ("23", "San Francisco Lempa"),
                ("24", "San Francisco Morazán"),
                ("25", "San Ignacio"),
                ("26", "San Isidro Labrador"),
                ("27", "San José Cancasque"),
                ("28", "San José Las Flores"),
                ("29", "San Luis del Carmen"),
                ("30", "San Miguel de Mercedes"),
                ("31", "San Rafael"),
                ("32", "Santa Rita"),
                ("33", "Tejutla"),
            ],

            # 04 - Cuscatlán
            ("04", "Cuscatlán"): [
                ("01", "Candelaria"),
                ("02", "Cojutepeque"),
                ("03", "El Carmen"),
                ("04", "El Rosario"),
                ("05", "Monte San Juan"),
                ("06", "Oratorio de Concepción"),
                ("07", "San Bartolomé Perulapía"),
                ("08", "San Cristóbal"),
                ("09", "San José Guayabal"),
                ("10", "San Pedro Perulapán"),
                ("11", "San Rafael Cedros"),
                ("12", "San Ramón"),
                ("13", "Santa Cruz Analquito"),
                ("14", "Santa Cruz Michapa"),
                ("15", "Suchitoto"),
                ("16", "Tenancingo"),
            ],

            # 05 - La Libertad
            ("05", "La Libertad"): [
                ("01", "Antiguo Cuscatlán"),
                ("02", "Chiltiupán"),
                ("03", "Ciudad Arce"),
                ("04", "Colón"),
                ("05", "Comasagua"),
                ("06", "Huizúcar"),
                ("07", "Jayaque"),
                ("08", "Jicalapa"),
                ("09", "La Libertad"),
                ("10", "Nueva San Salvador"),
                ("11", "Nuevo Cuscatlán"),
                ("12", "San Juan Opico"),
                ("13", "Quezaltepeque"),
                ("14", "Sacacoyo"),
                ("15", "San José Villanueva"),
                ("16", "San Matías"),
                ("17", "San Pablo Tacachico"),
                ("18", "Talnique"),
                ("19", "Tamanique"),
                ("20", "Teotepeque"),
                ("21", "Tepecoyo"),
                ("22", "Zaragoza"),
            ],

            # 06 - La Paz
            ("06", "La Paz"): [
                ("01", "Cuyultitán"),
                ("02", "El Rosario"),
                ("03", "Jerusalén"),
                ("04", "Mercedes La Ceiba"),
                ("05", "Olocuilta"),
                ("06", "Paraíso de Osorio"),
                ("07", "San Antonio Masahuat"),
                ("08", "San Emigdio"),
                ("09", "San Francisco Chinameca"),
                ("10", "San Juan Nonualco"),
                ("11", "San Juan Talpa"),
                ("12", "San Juan Tepezontes"),
                ("13", "San Luis La Herradura"),
                ("14", "San Luis Talpa"),
                ("15", "San Miguel Tepezontes"),
                ("16", "San Pedro Masahuat"),
                ("17", "San Pedro Nonualco"),
                ("18", "San Rafael Obrajuelo"),
                ("19", "Santa María Ostuma"),
                ("20", "Santiago Nonualco"),
                ("21", "Tapalhuaca"),
                ("22", "Zacatecoluca"),
            ],

            # 07 - La Unión
            ("07", "La Unión"): [
                ("01", "Anamorós"),
                ("02", "Bolívar"),
                ("03", "Concepción de Oriente"),
                ("04", "Conchagua"),
                ("05", "El Carmen"),
                ("06", "El Sauce"),
                ("07", "Intipucá"),
                ("08", "La Unión"),
                ("09", "Lislique"),
                ("10", "Meanguera del Golfo"),
                ("11", "Nueva Esparta"),
                ("12", "Pasaquina"),
                ("13", "Polorós"),
                ("14", "San Alejo"),
                ("15", "San José"),
                ("16", "Santa Rosa de Lima"),
                ("17", "Yayantique"),
                ("18", "Yucuaiquín"),
            ],

            # 08 - Morazán
            ("08", "Morazán"): [
                ("01", "Arambala"),
                ("02", "Cacaopera"),
                ("03", "Chilanga"),
                ("04", "Corinto"),
                ("05", "Delicias de Concepción"),
                ("06", "El Divisadero"),
                ("07", "El Rosario"),
                ("08", "Gualococti"),
                ("09", "Guatajiagua"),
                ("10", "Joateca"),
                ("11", "Jocoaitique"),
                ("12", "Jocoro"),
                ("13", "Lolotiquillo"),
                ("14", "Meanguera"),
                ("15", "Osicala"),
                ("16", "Perquín"),
                ("17", "San Carlos"),
                ("18", "San Fernando"),
                ("19", "San Francisco Gotera"),
                ("20", "San Isidro"),
                ("21", "San Simón"),
                ("22", "Sensembra"),
                ("23", "Sociedad"),
                ("24", "Torola"),
                ("25", "Yamabal"),
                ("26", "Yoloaiquín"),
            ],

            # 09 - San Miguel
            ("09", "San Miguel"): [
                ("01", "Carolina"),
                ("02", "Chapeltique"),
                ("03", "Chinameca"),
                ("04", "Chirilagua"),
                ("05", "Ciudad Barrios"),
                ("06", "Comacarán"),
                ("07", "El Tránsito"),
                ("08", "Lolotique"),
                ("09", "Moncagua"),
                ("10", "Nueva Guadalupe"),
                ("11", "Nuevo Edén de San Juan"),
                ("12", "Quelepa"),
                ("13", "San Antonio"),
                ("14", "San Gerardo"),
                ("15", "San Jorge"),
                ("16", "San Luis de la Reina"),
                ("17", "San Miguel"),
                ("18", "San Rafael Oriente"),
                ("19", "Sesori"),
                ("20", "Uluazapa"),
            ],

            # 10 - San Salvador
            ("10", "San Salvador"): [
                ("01", "Aguilares"),
                ("02", "Apopa"),
                ("03", "Ayutuxtepeque"),
                ("04", "Cuscatancingo"),
                ("05", "Delgado"),
                ("06", "El Paisnal"),
                ("07", "Guazapa"),
                ("08", "Ilopango"),
                ("09", "Mejicanos"),
                ("10", "Nejapa"),
                ("11", "Panchimalco"),
                ("12", "Rosario de Mora"),
                ("13", "San Marcos"),
                ("14", "San Martín"),
                ("15", "San Salvador"),
                ("16", "Santiago Texacuangos"),
                ("17", "Santo Tomás"),
                ("18", "Soyapango"),
                ("19", "Tonacatepeque"),
            ],

            # 11 - San Vicente
            ("11", "San Vicente"): [
                ("01", "Apastepeque"),
                ("02", "Guadalupe"),
                ("03", "San Cayetano Istepeque"),
                ("04", "San Esteban Catarina"),
                ("05", "San Ildefonso"),
                ("06", "San Lorenzo"),
                ("07", "San Sebastián"),
                ("08", "San Vicente"),
                ("09", "Santa Clara"),
                ("10", "Santo Domingo"),
                ("11", "Tecoluca"),
                ("12", "Tepetitán"),
                ("13", "Verapaz"),
            ],

            # 12 - Santa Ana
            ("12", "Santa Ana"): [
                ("01", "Candelaria de la Frontera"),
                ("02", "Chalchuapa"),
                ("03", "Coatepeque"),
                ("04", "El Congo"),
                ("05", "El Porvenir"),
                ("06", "Masahuat"),
                ("07", "Metapán"),
                ("08", "San Antonio Pajonal"),
                ("09", "San Sebastián Salitrillo"),
                ("10", "Santa Ana"),
                ("11", "Santa Rosa Guachipilín"),
                ("12", "Santiago de la Frontera"),
                ("13", "Texistepeque"),
            ],

            # 13 - Sonsonate
            ("13", "Sonsonate"): [
                ("01", "Acajutla"),
                ("02", "Armenia"),
                ("03", "Caluco"),
                ("04", "Cuisnahuat"),
                ("05", "Izalco"),
                ("06", "Juayúa"),
                ("07", "Nahuizalco"),
                ("08", "Nahulingo"),
                ("09", "Salcoatitán"),
                ("10", "San Antonio del Monte"),
                ("11", "San Julián"),
                ("12", "Santa Catarina Masahuat"),
                ("13", "Santa Isabel Ishuatán"),
                ("14", "Santo Domingo de Guzmán"),
                ("15", "Sonsonate"),
                ("16", "Sonzacate"),
            ],

            # 14 - Usulután
            ("14", "Usulután"): [
                ("01", "Alegría"),
                ("02", "Berlín"),
                ("03", "California"),
                ("04", "Concepción Batres"),
                ("05", "El Triunfo"),
                ("06", "Ereguayquín"),
                ("07", "Estanzuelas"),
                ("08", "Jiquilisco"),
                ("09", "Jucuapa"),
                ("10", "Jucuarán"),
                ("11", "Mercedes Umaña"),
                ("12", "Nueva Granada"),
                ("13", "Ozatlán"),
                ("14", "Puerto El Triunfo"),
                ("15", "San Agustín"),
                ("16", "San Buenaventura"),
                ("17", "San Dionisio"),
                ("18", "San Francisco Javier"),
                ("19", "Santa Elena"),
                ("20", "Santa María"),
                ("21", "Santiago de María"),
                ("22", "Tecapán"),
                ("23", "Usulután"),
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
