import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple
import json
from datetime import datetime
import uuid

class CuppingWheel:
    """Rueda de sabores de café interactiva"""
    
    def __init__(self):
        self.flavor_wheel = {
            "Frutales": {
                "color": "#FF6B6B",
                "subcategories": {
                    "Cítricos": ["Limón", "Lima", "Naranja", "Toronja", "Bergamota"],
                    "Frutas del Bosque": ["Arándano", "Frambuesa", "Mora", "Fresa", "Cereza Dulce"],
                    "Frutas de Hueso": ["Durazno", "Albaricoque", "Ciruela", "Cereza Ácida"],
                    "Tropicales": ["Piña", "Mango", "Papaya", "Coco", "Maracuyá"]
                }
            },
            "Dulces": {
                "color": "#4ECDC4",
                "subcategories": {
                    "Chocolate": ["Chocolate Negro", "Chocolate con Leche", "Cacao", "Chocolate Blanco"],
                    "Vainilla": ["Vainilla", "Caramelo Líquido", "Miel", "Melaza"],
                    "Azúcares": ["Azúcar Morena", "Jarabe de Arce", "Azúcar Blanca"],
                    "Dulces": ["Caramelo Sólido", "Toffee", "Butterscotch", "Marshmallow"]
                }
            },
            "Florales": {
                "color": "#45B7D1",
                "subcategories": {
                    "Flores Blancas": ["Jazmín", "Azahar", "Magnolia"],
                    "Flores Rojas": ["Rosa", "Hibisco", "Geranio"],
                    "Hierbas": ["Lavanda", "Romero", "Tomillo", "Té Negro"]
                }
            },
            "Especiados": {
                "color": "#96CEB4",
                "subcategories": {
                    "Especias Dulces": ["Canela", "Nuez Moscada", "Cardamomo", "Anís"],
                    "Especias Picantes": ["Pimienta", "Clavo", "Jengibre"],
                    "Hierbas Secas": ["Orégano", "Salvia", "Tabaco"]
                }
            },
            "Nueces": {
                "color": "#FFEAA7",
                "subcategories": {
                    "Nueces de Árbol": ["Almendra", "Avellana", "Nuez", "Pecana"],
                    "Mantequillas": ["Mantequilla de Maní", "Mantequilla de Almendra"],
                    "Cereales": ["Avena", "Trigo", "Cebada", "Pan Tostado"]
                }
            },
            "Terrosos": {
                "color": "#DDA0DD",
                "subcategories": {
                    "Minerales": ["Piedra Húmeda", "Tierra", "Grafito"],
                    "Maderas": ["Cedro", "Roble", "Ahumado"],
                    "Vegetales": ["Pasto", "Hojas Verdes", "Musgo"]
                }
            }
        }
    
    def render_flavor_wheel(self) -> List[str]:
        """Renderiza la rueda de sabores y retorna sabores seleccionados"""
        st.subheader("🎯 Rueda de Sabores")
        
        selected_flavors = []
        
        # Crear tabs para cada categoría principal
        category_tabs = st.tabs(list(self.flavor_wheel.keys()))
        
        for i, (category, data) in enumerate(self.flavor_wheel.items()):
            with category_tabs[i]:
                st.markdown(f"### {category}")
                
                cols = st.columns(2)
                for j, (subcat, flavors) in enumerate(data["subcategories"].items()):
                    with cols[j % 2]:
                        st.markdown(f"**{subcat}:**")
                        for flavor in flavors:
                            if st.checkbox(flavor, key=f"flavor_{category}_{subcat}_{flavor}"):
                                selected_flavors.append(flavor)
        
        return selected_flavors
    
    def render_interactive_wheel(self):
        """Renderiza una rueda de sabores visual con Plotly"""
        # Preparar datos para el gráfico
        categories = []
        subcategories = []
        flavors = []
        colors = []
        
        for cat_name, cat_data in self.flavor_wheel.items():
            for subcat_name, flavor_list in cat_data["subcategories"].items():
                for flavor in flavor_list:
                    categories.append(cat_name)
                    subcategories.append(subcat_name)
                    flavors.append(flavor)
                    colors.append(cat_data["color"])
        
        # Crear gráfico de sunburst
        fig = go.Figure(go.Sunburst(
            labels=categories + subcategories + flavors,
            parents=[""] * len(categories) + categories * len(set(subcategories)) + subcategories,
            values=[1] * (len(categories) + len(subcategories) + len(flavors)),
            branchvalues="total",
            hovertemplate='<b>%{label}</b><br>Categoría: %{parent}<extra></extra>',
            maxdepth=3,
        ))
        
        fig.update_layout(
            title="Rueda de Sabores de Café",
            font_size=12,
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)

class CuppingForm:
    """Formulario profesional de catación de café"""
    
    def __init__(self):
        self.sca_attributes = {
            "Fragancia/Aroma": {"max": 10, "description": "Olor del café molido seco y húmedo"},
            "Sabor": {"max": 10, "description": "Características gustativas principales"},
            "Retrogusto": {"max": 10, "description": "Duración y calidad del sabor residual"},
            "Acidez": {"max": 10, "description": "Brillo y vivacidad del café"},
            "Cuerpo": {"max": 10, "description": "Sensación táctil del líquido en boca"},
            "Uniformidad": {"max": 10, "description": "Consistencia entre tazas"},
            "Balance": {"max": 10, "description": "Armonía entre los elementos"},
            "Taza Limpia": {"max": 10, "description": "Ausencia de defectos"},
            "Dulzor": {"max": 10, "description": "Dulzor natural del café"},
            "Puntuación del Catador": {"max": 10, "description": "Evaluación general subjetiva"}
        }
        
        self.defects = [
            "Sobre-fermentado", "Mohoso", "Terroso", "Astringente", 
            "Amargo", "Agrio", "Verde", "Fenólico", "Químico", "Medicinal"
        ]
    
    def render_cupping_setup(self):
        """Configuración inicial de la catación"""
        st.subheader("⚙️ Configuración de Catación")
        
        col1, col2 = st.columns(2)
        
        with col1:
            session_name = st.text_input("Nombre de la Sesión", placeholder="Catación - Lote 001")
            coffee_name = st.text_input("Nombre del Café *", placeholder="Finca El Paraíso")
            origin = st.text_input("Origen *", placeholder="Huila, Colombia")
            variety = st.text_input("Variedad", placeholder="Geisha, Caturra")
            
        with col2:
            farm = st.text_input("Finca", placeholder="Finca El Paraíso")
            altitude = st.number_input("Altitud (msnm)", min_value=0, max_value=3000, step=50)
            harvest_date = st.date_input("Fecha de Cosecha")
            process_method = st.selectbox("Método de Proceso", [
                "Lavado", "Natural", "Honey", "Pulped Natural", 
                "Semi-lavado", "Anaerobic", "Carbonic Maceration", "Otro"
            ])
        
        return {
            "session_name": session_name,
            "coffee_name": coffee_name,
            "origin": origin,
            "variety": variety,
            "farm": farm,
            "altitude": altitude,
            "harvest_date": harvest_date,
            "process_method": process_method
        }
    
    def render_brewing_parameters(self):
        """Parámetros de preparación"""
        st.subheader("☕ Parámetros de Preparación")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            grind_size = st.selectbox("Tamaño de Molienda", 
                ["Muy Fino", "Fino", "Medio-Fino", "Medio", "Medio-Grueso", "Grueso"])
            water_temp = st.number_input("Temperatura del Agua (°C)", 
                min_value=80, max_value=100, value=93)
            
        with col2:
            coffee_dose = st.number_input("Dosis de Café (g)", 
                min_value=1.0, max_value=50.0, value=8.25, step=0.25)
            water_volume = st.number_input("Volumen de Agua (ml)", 
                min_value=50, max_value=500, value=150, step=10)
            
        with col3:
            brew_time = st.text_input("Tiempo de Contacto", placeholder="4:00")
            tds = st.number_input("TDS (%)", min_value=0.0, max_value=3.0, 
                value=1.30, step=0.01, format="%.2f")
        
        ratio = round(water_volume / coffee_dose, 1) if coffee_dose > 0 else 0
        st.info(f"📊 Ratio: 1:{ratio}")
        
        return {
            "grind_size": grind_size,
            "water_temp": water_temp,
            "coffee_dose": coffee_dose,
            "water_volume": water_volume,
            "brew_time": brew_time,
            "tds": tds,
            "ratio": ratio
        }
    
    def render_cupping_evaluation(self, cup_number: int, cupper_name: str):
        """Evaluación individual por taza y catador"""
        st.subheader(f"🏆 Evaluación - Taza {cup_number} - {cupper_name}")
        
        scores = {}
        total_score = 0
        
        # Atributos SCA
        for attribute, config in self.sca_attributes.items():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                score = st.slider(
                    f"{attribute} ({config['description']})",
                    min_value=6.0,
                    max_value=float(config['max']),
                    value=7.0,
                    step=0.25,
                    key=f"{attribute}_{cup_number}_{cupper_name}"
                )
                scores[attribute] = score
                total_score += score
            
            with col2:
                st.metric("", f"{score}/10")
        
        # Defectos
        st.markdown("#### 🚫 Defectos")
        defects_found = []
        defect_intensity = {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            for defect in self.defects[:len(self.defects)//2]:
                if st.checkbox(defect, key=f"defect_{defect}_{cup_number}_{cupper_name}"):
                    defects_found.append(defect)
                    intensity = st.slider(f"Intensidad {defect}", 
                        min_value=1, max_value=4, value=2,
                        key=f"intensity_{defect}_{cup_number}_{cupper_name}")
                    defect_intensity[defect] = intensity
        
        with col2:
            for defect in self.defects[len(self.defects)//2:]:
                if st.checkbox(defect, key=f"defect_{defect}_{cup_number}_{cupper_name}"):
                    defects_found.append(defect)
                    intensity = st.slider(f"Intensidad {defect}", 
                        min_value=1, max_value=4, value=2,
                        key=f"intensity_{defect}_{cup_number}_{cupper_name}")
                    defect_intensity[defect] = intensity
        
        # Calcular deducción por defectos
        defect_deduction = sum(defect_intensity.values()) * 2
        final_score = max(0, total_score - defect_deduction)
        
        # Mostrar puntuación final
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Puntuación Base", f"{total_score:.2f}")
        with col2:
            st.metric("Deducción Defectos", f"-{defect_deduction}")
        with col3:
            color = "normal"
            if final_score >= 85:
                color = "inverse"
            elif final_score < 70:
                color = "off"
            
            st.metric("**Puntuación Final**", f"{final_score:.2f}/100", 
                delta=None)
        
        # Notas adicionales
        notes = st.text_area("Notas Adicionales", 
            placeholder="Observaciones específicas de esta taza...",
            key=f"notes_{cup_number}_{cupper_name}")
        
        return {
            "scores": scores,
            "total_score": total_score,
            "defects": defects_found,
            "defect_intensity": defect_intensity,
            "defect_deduction": defect_deduction,
            "final_score": final_score,
            "notes": notes
        }

class CuppingSession:
    """Manejador de sesiones de catación completas"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.cupping_wheel = CuppingWheel()
        self.cupping_form = CuppingForm()
    
    def render_complete_session(self):
        """Renderiza una sesión completa de catación"""
        st.title("🏆 Catación Profesional de Café")
        
        # Configuración inicial
        with st.expander("⚙️ Configuración de Catación", expanded=True):
            coffee_info = self.cupping_form.render_cupping_setup()
            brewing_params = self.cupping_form.render_brewing_parameters()
        
        # Configuración de catadores y tazas
        st.subheader("👥 Configuración de Evaluación")
        
        col1, col2 = st.columns(2)
        
        with col1:
            num_cuppers = st.number_input("Número de Catadores", 
                min_value=1, max_value=8, value=1)
            cuppers = []
            for i in range(num_cuppers):
                cupper = st.text_input(f"Catador {i+1}", 
                    value=f"Catador {i+1}", key=f"cupper_{i}")
                cuppers.append(cupper)
        
        with col2:
            num_cups = st.number_input("Número de Tazas", 
                min_value=1, max_value=5, value=3)
            st.info(f"Se evaluarán {num_cups} tazas por {num_cuppers} catador(es)")
            st.info(f"Total de evaluaciones: {num_cups * num_cuppers}")
        
        # Rueda de sabores
        with st.expander("🎯 Rueda de Sabores", expanded=False):
            tab1, tab2 = st.tabs(["Selección Manual", "Rueda Visual"])
            
            with tab1:
                selected_flavors = self.cupping_wheel.render_flavor_wheel()
            
            with tab2:
                self.cupping_wheel.render_interactive_wheel()
        
        # Evaluaciones por catador y taza
        st.subheader("📝 Evaluaciones")
        
        all_evaluations = {}
        
        # Crear tabs por catador
        if num_cuppers > 1:
            cupper_tabs = st.tabs(cuppers)
            
            for i, cupper in enumerate(cuppers):
                with cupper_tabs[i]:
                    all_evaluations[cupper] = {}
                    
                    # Crear sub-tabs por taza para cada catador
                    cup_tabs = st.tabs([f"Taza {j+1}" for j in range(num_cups)])
                    
                    for j in range(num_cups):
                        with cup_tabs[j]:
                            evaluation = self.cupping_form.render_cupping_evaluation(j+1, cupper)
                            all_evaluations[cupper][f"cup_{j+1}"] = evaluation
        else:
            # Un solo catador, tabs por taza
            cupper = cuppers[0]
            all_evaluations[cupper] = {}
            
            cup_tabs = st.tabs([f"Taza {j+1}" for j in range(num_cups)])
            
            for j in range(num_cups):
                with cup_tabs[j]:
                    evaluation = self.cupping_form.render_cupping_evaluation(j+1, cupper)
                    all_evaluations[cupper][f"cup_{j+1}"] = evaluation
        
        # Resumen y guardado
        st.subheader("📊 Resumen de Resultados")
        
        if st.button("📊 Calcular Promedios", type="primary"):
            self.render_results_summary(all_evaluations, num_cups, cuppers)
        
        # Botón para guardar
        if st.button("💾 Guardar Catación", type="primary"):
            cupping_data = {
                "coffee_info": coffee_info,
                "brewing_params": brewing_params,
                "cuppers": cuppers,
                "num_cups": num_cups,
                "selected_flavors": selected_flavors if 'selected_flavors' in locals() else [],
                "evaluations": all_evaluations,
                "created_at": datetime.now(),
                "session_id": str(uuid.uuid4())
            }
            
            if self.save_cupping_session(cupping_data):
                st.success("✅ Catación guardada exitosamente!")
                st.balloons()
            else:
                st.error("❌ Error al guardar la catación")
    
    def render_results_summary(self, evaluations: Dict, num_cups: int, cuppers: List):
        """Renderiza resumen de resultados"""
        
        # Calcular promedios
        all_scores = []
        cupper_averages = {}
        
        for cupper, cups in evaluations.items():
            cupper_scores = []
            for cup_id, evaluation in cups.items():
                if evaluation and 'final_score' in evaluation:
                    all_scores.append(evaluation['final_score'])
                    cupper_scores.append(evaluation['final_score'])
            
            if cupper_scores:
                cupper_averages[cupper] = {
                    'average': sum(cupper_scores) / len(cupper_scores),
                    'scores': cupper_scores
                }
        
        if all_scores:
            overall_average = sum(all_scores) / len(all_scores)
            
            # Mostrar métricas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Puntuación Promedio", f"{overall_average:.2f}")
            
            with col2:
                st.metric("Puntuación Máxima", f"{max(all_scores):.2f}")
            
            with col3:
                st.metric("Puntuación Mínima", f"{min(all_scores):.2f}")
            
            # Gráfico de resultados
            if len(cuppers) > 1:
                # Comparación entre catadores
                cupper_names = list(cupper_averages.keys())
                averages = [cupper_averages[name]['average'] for name in cupper_names]
                
                fig = px.bar(
                    x=cupper_names,
                    y=averages,
                    title="Promedio por Catador",
                    labels={'x': 'Catador', 'y': 'Puntuación Promedio'},
                    color=averages,
                    color_continuous_scale='Viridis'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Consistencia entre tazas
            if num_cups > 1:
                cup_data = []
                for cupper, cups in evaluations.items():
                    for cup_id, evaluation in cups.items():
                        if evaluation and 'final_score' in evaluation:
                            cup_data.append({
                                'Catador': cupper,
                                'Taza': cup_id.replace('cup_', 'Taza '),
                                'Puntuación': evaluation['final_score']
                            })
                
                if cup_data:
                    import pandas as pd
                    df = pd.DataFrame(cup_data)
                    
                    fig = px.box(
                        df,
                        x='Taza',
                        y='Puntuación',
                        title="Consistencia entre Tazas",
                        points="all"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
    
    def save_cupping_session(self, cupping_data: Dict) -> bool:
        """Guarda la sesión de catación en la base de datos"""
        try:
            current_user = st.session_state.auth_manager.get_current_user()
            
            session_record = {
                'session_id': cupping_data['session_id'],
                'user_id': current_user.get('user_id'),
                'cupper_name': current_user.get('username'),
                'coffee_info': cupping_data['coffee_info'],
                'brewing_params': cupping_data['brewing_params'],
                'cuppers': cupping_data['cuppers'],
                'num_cups': cupping_data['num_cups'],
                'selected_flavors': cupping_data['selected_flavors'],
                'evaluations': cupping_data['evaluations'],
                'created_at': cupping_data['created_at'],
                'session_type': 'professional_cupping'
            }
            
            self.db_manager.db.collection('cupping_sessions').document(
                cupping_data['session_id']
            ).set(session_record)
            
            return True
            
        except Exception as e:
            st.error(f"Error saving cupping session: {e}")
            return False