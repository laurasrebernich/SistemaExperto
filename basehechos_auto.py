# basehechos_auto.py

from experta import Fact, Field

# ---------------------------------------------------------------------------
# DEFINICIÓN DE LA ESTRUCTURA DE LOS HECHOS (FACTS)
# Un "Hecho" es una pieza de información que el sistema experto conoce.
# ---------------------------------------------------------------------------

class PreferenciasUsuario(Fact):
    """
    Define la estructura para almacenar las preferencias del usuario.
    """
    presupuesto = Field(str, mandatory=True)
    uso_principal = Field(str, mandatory=True)
    cantidad_pasajeros = Field(int, mandatory=True)
    prioridad_consumo = Field(str, mandatory=True)
    prioridad_seguridad = Field(str, mandatory=True)
    prioridad_baul = Field(str, mandatory=True)
    prioridad_reventa = Field(str, mandatory=True)

class Auto(Fact):
    """
    Define la estructura de cada vehículo en nuestra base de conocimiento.
    """
    marca = Field(str, mandatory=True)
    modelo = Field(str, mandatory=True)
    cantidad_pasajeros = Field(int, mandatory=True)
    rango_precio = Field(str, mandatory=True)
    tipo = Field(str, mandatory=True)
    consumo = Field(str, mandatory=True)
    seguridad = Field(str, mandatory=True)
    baul = Field(str, mandatory=True)
    costo_mantenimiento = Field(str, mandatory=True)
    reventa = Field(str, mandatory=True)

    def __str__(self):
        return f"{self['marca']} {self['modelo']}"

# ---------------------------------------------------------------------------
# ¡NUEVO HECHO INTERMEDIO PARA PUNTUACIÓN!
# ---------------------------------------------------------------------------
class HechoPuntaje(Fact):
    """
    HECHO INTERMEDIO para encadenamiento.
    Cada regla que encuentra una coincidencia con una prioridad,
    crea este hecho asignando puntos a un modelo.
    """
    modelo = Field(str, mandatory=True)
    puntos = Field(int, mandatory=True)
    motivo = Field(str, mandatory=True) # Razón por la que obtuvo los puntos

# (La función cargar_base_de_conocimiento() no cambia en absoluto)
def cargar_base_de_conocimiento():
     # --- Rango de Precio BAJO ---
    yield Auto(marca="Fiat", modelo="Cronos", cantidad_pasajeros=5, rango_precio="bajo", tipo="sedan", consumo="bajo", seguridad="media", baul="grande", costo_mantenimiento="bajo", reventa="regular")
    yield Auto(marca="Chevrolet", modelo="Onix", cantidad_pasajeros=5, rango_precio="bajo", tipo="hatchback", consumo="bajo", seguridad="alta", baul="pequeño", costo_mantenimiento="bajo", reventa="regular")
    yield Auto(marca="Toyota", modelo="Yaris", cantidad_pasajeros=5, rango_precio="bajo", tipo="hatchback", consumo="bajo", seguridad="alta", baul="pequeño", costo_mantenimiento="bajo", reventa="buena")
    yield Auto(marca="Renault", modelo="Sandero", cantidad_pasajeros=5, rango_precio="bajo", tipo="hatchback", consumo="medio", seguridad="media", baul="pequeño", costo_mantenimiento="bajo", reventa="baja")
    yield Auto(marca="Peugeot", modelo="208", cantidad_pasajeros=5, rango_precio="bajo", tipo="hatchback", consumo="bajo", seguridad="alta", baul="pequeño", costo_mantenimiento="medio", reventa="regular")
    yield Auto(marca="Volkswagen", modelo="Virtus", cantidad_pasajeros=5, rango_precio="bajo", tipo="sedan", consumo="bajo", seguridad="alta", baul="grande", costo_mantenimiento="bajo", reventa="buena")
    yield Auto(marca="Renault", modelo="Kwid", cantidad_pasajeros=5, rango_precio="bajo", tipo="sedan", consumo="bajo", seguridad="alta", baul="grande", costo_mantenimiento="bajo", reventa="buena")
    yield Auto(marca="Fiat", modelo="Mobi", cantidad_pasajeros=4, rango_precio="bajo", tipo="Hatchback", consumo="muy bajo", seguridad="media", baul="pequeño", costo_mantenimiento="bajo", reventa="media")
    # --- Rango de Precio MEDIO ---
    yield Auto(marca="Toyota", modelo="Corolla", cantidad_pasajeros=5, rango_precio="medio", tipo="sedan", consumo="bajo", seguridad="alta", baul="mediano", costo_mantenimiento="bajo", reventa="buena")
    yield Auto(marca="Ford", modelo="Territory", cantidad_pasajeros=5, rango_precio="medio", tipo="suv", consumo="medio", seguridad="alta", baul="mediano", costo_mantenimiento="medio", reventa="regular")
    yield Auto(marca="Chevrolet", modelo="Tracker", cantidad_pasajeros=5, rango_precio="medio", tipo="suv", consumo="medio", seguridad="alta", baul="mediano", costo_mantenimiento="bajo", reventa="regular")
    yield Auto(marca="Jeep", modelo="Renegade", cantidad_pasajeros=5, rango_precio="medio", tipo="suv", consumo="alto", seguridad="media", baul="pequeño", costo_mantenimiento="medio", reventa="regular")
    yield Auto(marca="Ford", modelo="Ranger", cantidad_pasajeros=5, rango_precio="medio", tipo="camioneta", consumo="alto", seguridad="media", baul="grande", costo_mantenimiento="medio", reventa="buena")
    yield Auto(marca="Volkswagen", modelo="Nivus", cantidad_pasajeros=5, rango_precio="medio", tipo="suv", consumo="bajo", seguridad="alta", baul="mediano", costo_mantenimiento="bajo", reventa="buena")
    yield Auto(marca="Chevrolet", modelo="Cruze", cantidad_pasajeros=5, rango_precio="medio", tipo="sedan", consumo="bajo", seguridad="alta", baul="mediano", costo_mantenimiento="bajo", reventa="regular")
    yield Auto(marca="Renault", modelo="Duster", cantidad_pasajeros=5, rango_precio="medio", tipo="suv", consumo="medio", seguridad="media", baul="grande", costo_mantenimiento="bajo", reventa="regular")
    yield Auto(marca="Citroën", modelo="C4 Cactus", cantidad_pasajeros=5, rango_precio="medio", tipo="suv", consumo="bajo", seguridad="media", baul="pequeño", costo_mantenimiento="medio", reventa="regular")
    yield Auto(marca="Peugeot", modelo="Partner Patagónica", cantidad_pasajeros=5, rango_precio="medio", tipo="Furgón/Multiespacio", consumo="medio", seguridad="media", baul="muy grande", costo_mantenimiento="medio", reventa="buena")
    yield Auto(marca="Volkswagen", modelo="Taos", cantidad_pasajeros=5, rango_precio="medio", tipo="suv", consumo="medio", seguridad="alta", baul="grande", costo_mantenimiento="medio", reventa="buena")
    yield Auto(marca="Chevrolet", modelo="Spin", cantidad_pasajeros=7, rango_precio="medio", tipo="suv", consumo="bajo", seguridad="media/alta", baul="pequeño (con 7A)", costo_mantenimiento="bajo", reventa="buena")
    yield Auto(marca="Citroën", modelo="C3 Aircross", cantidad_pasajeros=7, rango_precio="medio", tipo="suv", consumo="bajo", seguridad="media", baul="pequeño (con 7A)", costo_mantenimiento="bajo", reventa="buena")
    yield Auto(marca="Volkswagen", modelo="Polo", cantidad_pasajeros=5, rango_precio="medio", tipo="Hatchback", consumo="bajo", seguridad="media/alta", baul="pequeño", costo_mantenimiento="medio", reventa="buena")
    yield Auto(marca="Fiat", modelo="Strada", cantidad_pasajeros=2, rango_precio="medio", tipo="Pick-up Compacta", consumo="medio", seguridad="media", baul="Grande (Caja)", costo_mantenimiento="bajo", reventa="buena")
    yield Auto(marca="Fiat", modelo="Strada", cantidad_pasajeros=5, rango_precio="medio", tipo="Pick-up Compacta", consumo="medio", seguridad="media", baul="Grande (Caja)", costo_mantenimiento="bajo", reventa="buena")
    # --- Rango de Precio ALTO ---
    yield Auto(marca="Toyota", modelo="Corolla Cross", cantidad_pasajeros=5, rango_precio="alto", tipo="suv", consumo="bajo", seguridad="alta", baul="mediano", costo_mantenimiento="bajo", reventa="buena")
    yield Auto(marca="Volkswagen", modelo="Taos", cantidad_pasajeros=5, rango_precio="alto", tipo="suv", consumo="medio", seguridad="alta", baul="grande", costo_mantenimiento="medio", reventa="regular")
    yield Auto(marca="Ford", modelo="Mustang", cantidad_pasajeros=4, rango_precio="alto", tipo="deportivo", consumo="alto", seguridad="alta", baul="pequeño", costo_mantenimiento="alto", reventa="regular")
    yield Auto(marca="Toyota", modelo="Hilux", cantidad_pasajeros=5, rango_precio="alto", tipo="camioneta", consumo="alto", seguridad="alta", baul="grande", costo_mantenimiento="medio", reventa="buena")
    yield Auto(marca="Volkswagen", modelo="Amarok", cantidad_pasajeros=5, rango_precio="alto", tipo="camioneta", consumo="alto", seguridad="media", baul="grande", costo_mantenimiento="medio", reventa="buena")
    yield Auto(marca="Volkswagen", modelo="Taos", cantidad_pasajeros=5, rango_precio="alto", tipo="suv", consumo="medio", seguridad="alta", baul="grande", costo_mantenimiento="medio", reventa="buena")
    yield Auto(marca="Toyota", modelo="SW4", cantidad_pasajeros=7, rango_precio="alto", tipo="suv grande/4x4", consumo="alto", seguridad="muy alta", baul="mediano (7A)", costo_mantenimiento="medio", reventa="excelente")
    yield Auto(marca="Ford", modelo="Ranger", cantidad_pasajeros=5, rango_precio="alto", tipo="Pick-up Mediana", consumo="alto", seguridad="alta", baul="muy grande", costo_mantenimiento="medio", reventa="buena")
    yield Auto(marca="Toyota", modelo="GR Yaris", cantidad_pasajeros=4, rango_precio="alto", tipo="Deportivo / Hatchback", consumo="alto", seguridad="alta", baul="chico", costo_mantenimiento="alto", reventa="muy buena")