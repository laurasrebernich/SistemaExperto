# main_streamlit.py
#streamlit run C:\Users\inpi\Downloads\asesoria_autos\main_streamlit.py

import streamlit as st
from collections import defaultdict

# Importamos las clases y funciones de nuestros otros módulos
from reglas_auto import AsesorAutomoviles, HechoPuntaje
from basehechos_auto import PreferenciasUsuario, cargar_base_de_conocimiento

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Asesor de Automóviles",
    page_icon="🚗",
    layout="centered"
)

# Cargamos la base de autos
@st.cache_data
def cargar_autos():
    return list(cargar_base_de_conocimiento())

base_de_autos = cargar_autos()

# --- Interfaz de Usuario (Sin cambios) ---

st.title("🚗 Asesor Experto de Automóviles")
st.write("Responde a estas preguntas y te ayudaremos a encontrar tu auto ideal.")

col1, col2 = st.columns(2)
with col1:
    presupuesto = st.selectbox("¿Cuál es tu presupuesto?", ["bajo", "medio", "alto"])
    uso_principal = st.selectbox("¿Cuál será el uso principal?", ["urbano", "ruta"])
    cantidad_pasajeros = st.slider("¿Cantidad de pasajeros habituales?", 2, 7, 4)
with col2:
    prioridad_consumo = st.radio("¿El bajo consumo es prioridad?", ["si", "no"], index=1)
    prioridad_seguridad = st.radio("¿La alta seguridad es prioridad?", ["si", "no"], index=1)
    prioridad_baul = st.radio("¿El espacio de baúl es importante?", ["si", "no"], index=1)
    prioridad_reventa = st.radio("¿Es importante el valor de reventa?", ["si", "no"], index=1)

# --- Lógica de Procesamiento y Ranking ---

if st.button("Buscar mi auto ideal", type="primary"):

    # --- 1. Ejecución del Sistema Experto ---
    engine = AsesorAutomoviles()
    engine.reset()

    for auto in base_de_autos:
        engine.declare(auto)

    preferencias = PreferenciasUsuario(
        presupuesto=presupuesto,
        uso_principal=uso_principal,
        cantidad_pasajeros=cantidad_pasajeros,
        prioridad_consumo=prioridad_consumo,
        prioridad_seguridad=prioridad_seguridad,
        prioridad_baul=prioridad_baul,
        prioridad_reventa=prioridad_reventa
    )
    engine.declare(preferencias)
    engine.run()

    # --- 2. Recolección y Agregación de Puntos ---
    hechos_puntaje = [f for f in engine.facts.values() if isinstance(f, HechoPuntaje)]

    if not hechos_puntaje:
        st.warning("No se encontraron recomendaciones con esos criterios. Intenta con otras opciones.")
    else:
        puntuaciones = defaultdict(int)
        motivos = defaultdict(list)

        for hecho in hechos_puntaje:
            modelo = hecho['modelo']
            puntos = hecho['puntos']
            motivo = hecho['motivo']
            
            puntuaciones[modelo] += puntos
            if motivo != "Cumple requisitos básicos":
                motivos[modelo].append(motivo)

        # --- 3. Ordenamiento (Ranking) ---
        autos_rankeados = sorted(puntuaciones.items(), key=lambda item: item[1], reverse=True)
        
        # --- 4. Visualización del Top 5 ---
        st.header("Top 5 Recomendaciones 🏆") # <-- CAMBIO 1: Texto actualizado a Top 5
        
        # Iteramos sobre los 5 primeros del ranking
        for i, (modelo, puntos) in enumerate(autos_rankeados[:5]): # <-- CAMBIO 2: Slicing actualizado a [:5]
            
            auto_encontrado = next((auto for auto in base_de_autos if auto['modelo'] == modelo), None)
            if auto_encontrado:
                
                # Ajustamos la lógica de emojis para los puestos 4 y 5
                if i == 0:
                    st.subheader(f"🥇 1. {auto_encontrado['marca']} {auto_encontrado['modelo']}")
                elif i == 1:
                    st.subheader(f"🥈 2. {auto_encontrado['marca']} {auto_encontrado['modelo']}")
                elif i == 2:
                    st.subheader(f"🥉 3. {auto_encontrado['marca']} {auto_encontrado['modelo']}")
                else:
                    # Para el 4to y 5to puesto, solo mostramos el número
                    st.subheader(f" {i + 1}. {auto_encontrado['marca']} {auto_encontrado['modelo']}")

                # Mostramos los motivos por los que sumó puntos
                razones_lista = list(set(motivos[modelo])) # Usamos set para eliminar motivos duplicados si los hubiera
                razones = ", ".join(razones_lista)
                st.info(f"**Puntaje Total: {puntos}** (Motivos: {razones})")

                # Mostramos los detalles completos
                with st.expander("Ver detalles completos"):
                    detalles = (
                        f"- **Tipo:** {auto_encontrado['tipo'].capitalize()}\n"
                        f"- **Precio:** {auto_encontrado['rango_precio'].capitalize()}\n"
                        f"- **Consumo:** {auto_encontrado['consumo'].capitalize()}\n"
                        f"- **Seguridad:** {auto_encontrado['seguridad'].capitalize()}\n"
                        f"- **Baúl:** {auto_encontrado['baul'].capitalize()}\n"
                        f"- **Mantenimiento:** {auto_encontrado['costo_mantenimiento'].capitalize()}\n"
                        f"- **Reventa:** {auto_encontrado['reventa'].capitalize()}"
                    )
                    st.markdown(detalles)