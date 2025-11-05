# reglas_auto.py

from experta import *
from basehechos_auto import Auto, PreferenciasUsuario, HechoPuntaje

class AsesorAutomoviles(KnowledgeEngine):
    """
    Motor de inferencia basado en un sistema de puntuación (scoring).
    Cada regla evalúa una prioridad del usuario y asigna puntos
    a los autos que la cumplen.
    """

    # --- REGLA BASE OBLIGATORIA ---
    # Todos los autos que cumplen con lo básico (presupuesto y pasajeros)
    # reciben 1 punto para entrar en la lista de candidatos.
    @Rule(
        PreferenciasUsuario(
            presupuesto=MATCH.presupuesto,
            cantidad_pasajeros=MATCH.pasajeros_req
        ),
        'auto' << Auto(
            rango_precio=MATCH.presupuesto
        ),
        TEST(lambda auto, pasajeros_req: auto['cantidad_pasajeros'] >= pasajeros_req),
        salience=10 # Prioridad más baja, se ejecuta siempre.
    )
    def auto_cumple_requisitos_basicos(self, auto):
        """
        Esta regla asigna un puntaje base a CUALQUIER auto que cumpla
        con el presupuesto y la cantidad de pasajeros.
        """
        self.declare(HechoPuntaje(
            modelo=auto['modelo'],
            puntos=1,
            motivo="Cumple requisitos básicos"
        ))

    # --- REGLAS DE PUNTUACIÓN POR PRIORIDADES ---
    # Cada regla se activa si el usuario marcó "si" en una prioridad.
    # Asignan puntos adicionales.

    @Rule(
        PreferenciasUsuario(
            presupuesto=MATCH.presupuesto,
            cantidad_pasajeros=MATCH.pasajeros_req,
            prioridad_seguridad='si' # El usuario quiere seguridad
        ),
        'auto' << Auto(
            rango_precio=MATCH.presupuesto,
            seguridad='alta' # El auto tiene alta seguridad
        ),
        TEST(lambda auto, pasajeros_req: auto['cantidad_pasajeros'] >= pasajeros_req),
        salience=50
    )
    def asignar_puntos_por_seguridad(self, auto):
        """
        ENCADENAMIENTO: Asigna puntos si el auto es de 'alta seguridad'.
        """
        self.declare(HechoPuntaje(
            modelo=auto['modelo'],
            puntos=30, # La seguridad es muy importante
            motivo="Alta Seguridad"
        ))

    @Rule(
        PreferenciasUsuario(
            presupuesto=MATCH.presupuesto,
            cantidad_pasajeros=MATCH.pasajeros_req,
            prioridad_reventa='si' # El usuario quiere buena reventa
        ),
        'auto' << Auto(
            rango_precio=MATCH.presupuesto,
            reventa='buena' # El auto tiene buena reventa
        ),
        TEST(lambda auto, pasajeros_req: auto['cantidad_pasajeros'] >= pasajeros_req),
        salience=50
    )
    def asignar_puntos_por_reventa(self, auto):
        """
        ENCADENAMIENTO: Asigna puntos si el auto tiene 'buena reventa'.
        """
        self.declare(HechoPuntaje(
            modelo=auto['modelo'],
            puntos=20,
            motivo="Buena Reventa"
        ))

    @Rule(
        PreferenciasUsuario(
            presupuesto=MATCH.presupuesto,
            cantidad_pasajeros=MATCH.pasajeros_req,
            prioridad_consumo='si' # El usuario quiere bajo consumo
        ),
        'auto' << Auto(
            rango_precio=MATCH.presupuesto,
            consumo='bajo' # El auto tiene bajo consumo
        ),
        TEST(lambda auto, pasajeros_req: auto['cantidad_pasajeros'] >= pasajeros_req),
        salience=50
    )
    def asignar_puntos_por_consumo(self, auto):
        """
        ENCADENAMIENTO: Asigna puntos si el auto tiene 'bajo consumo'.
        """
        self.declare(HechoPuntaje(
            modelo=auto['modelo'],
            puntos=20,
            motivo="Bajo Consumo"
        ))

    @Rule(
        PreferenciasUsuario(
            presupuesto=MATCH.presupuesto,
            cantidad_pasajeros=MATCH.pasajeros_req,
            prioridad_baul='si' # El usuario quiere baúl grande
        ),
        'auto' << Auto(
            rango_precio=MATCH.presupuesto,
            baul=~L('pequeño') # El auto tiene baúl mediano O grande
        ),
        TEST(lambda auto, pasajeros_req: auto['cantidad_pasajeros'] >= pasajeros_req),
        salience=50
    )
    def asignar_puntos_por_baul(self, auto):
        """
        ENCADENAMIENTO: Asigna puntos si el auto tiene baúl 'mediano' o 'grande'.
        """
        self.declare(HechoPuntaje(
            modelo=auto['modelo'],
            puntos=15,
            motivo="Buen Baúl"
        ))

    @Rule(
        PreferenciasUsuario(
            presupuesto=MATCH.presupuesto,
            cantidad_pasajeros=MATCH.pasajeros_req,
            uso_principal='ruta' # Preferencia de uso
        ),
        'auto' << Auto(
            rango_precio=MATCH.presupuesto,
            tipo=L('sedan') | L('suv') # Tipos de auto buenos para ruta
        ),
        TEST(lambda auto, pasajeros_req: auto['cantidad_pasajeros'] >= pasajeros_req),
        salience=40 # Un poco menos de prioridad, es un "plus"
    )
    def asignar_puntos_por_tipo_ruta(self, auto):
        """
        ENCADENAMIENTO: Asigna puntos extra si el tipo de auto
        es bueno para el uso en ruta.
        """
        self.declare(HechoPuntaje(
            modelo=auto['modelo'],
            puntos=10,
            motivo="Ideal para Ruta"
        ))