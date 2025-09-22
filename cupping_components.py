import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple
import json
from datetime import datetime
import uuid

class CuppingWheel:
    """Interactive coffee flavor wheel"""
    
    def __init__(self):
        self.flavor_wheel = {
            "Fruity": {
                "color": "#FF6B6B",
                "subcategories": {
                    "Citrus": ["Lemon", "Lime", "Orange", "Grapefruit", "Bergamot"],
                    "Berry": ["Blueberry", "Raspberry", "Blackberry", "Strawberry", "Sweet Cherry"],
                    "Stone Fruit": ["Peach", "Apricot", "Plum", "Tart Cherry"],
                    "Tropical": ["Pineapple", "Mango", "Papaya", "Coconut", "Passion Fruit"]
                }
            },
            "Sweet": {
                "color": "#4ECDC4",
                "subcategories": {
                    "Chocolate": ["Dark Chocolate", "Milk Chocolate", "Cocoa", "White Chocolate"],
                    "Vanilla": ["Vanilla", "Liquid Caramel", "Honey", "Molasses"],
                    "Sugars": ["Brown Sugar", "Maple Syrup", "White Sugar"],
                    "Candy": ["Solid Caramel", "Toffee", "Butterscotch", "Marshmallow"]
                }
            },
            "Floral": {
                "color": "#45B7D1",
                "subcategories": {
                    "White Flowers": ["Jasmine", "Orange Blossom", "Magnolia"],
                    "Red Flowers": ["Rose", "Hibiscus", "Geranium"],
                    "Herbs": ["Lavender", "Rosemary", "Thyme", "Black Tea"]
                }
            },
            "Spiced": {
                "color": "#96CEB4",
                "subcategories": {
                    "Sweet Spices": ["Cinnamon", "Nutmeg", "Cardamom", "Anise"],
                    "Hot Spices": ["Black Pepper", "Clove", "Ginger"],
                    "Dried Herbs": ["Oregano", "Sage", "Tobacco"]
                }
            },
            "Nutty": {
                "color": "#FFEAA7",
                "subcategories": {
                    "Tree Nuts": ["Almond", "Hazelnut", "Walnut", "Pecan"],
                    "Nut Butters": ["Peanut Butter", "Almond Butter"],
                    "Cereals": ["Oats", "Wheat", "Barley", "Toasted Bread"]
                }
            },
            "Earthy": {
                "color": "#DDA0DD",
                "subcategories": {
                    "Minerals": ["Wet Stone", "Earth", "Graphite"],
                    "Woods": ["Cedar", "Oak", "Smoky"],
                    "Vegetables": ["Fresh Grass", "Green Leaves", "Moss"]
                }
            }
        }
    
    def render_flavor_wheel(self) -> List[str]:
        """Render flavor wheel and return selected flavors"""
        st.subheader("🎯 Flavor Wheel")
        
        selected_flavors = []
        
        # Create tabs for each main category
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
        """Render visual flavor wheel with Plotly"""
        # Prepare data for chart
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
        
        # Create sunburst chart
        fig = go.Figure(go.Sunburst(
            labels=categories + subcategories + flavors,
            parents=[""] * len(categories) + categories * len(set(subcategories)) + subcategories,
            values=[1] * (len(categories) + len(subcategories) + len(flavors)),
            branchvalues="total",
            hovertemplate='<b>%{label}</b><br>Category: %{parent}<extra></extra>',
            maxdepth=3,
        ))
        
        fig.update_layout(
            title="Coffee Flavor Wheel",
            font_size=12,
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)

class CuppingForm:
    """Professional coffee cupping form"""
    
    def __init__(self):
        self.sca_attributes = {
            "Fragrance/Aroma": {"max": 10, "description": "Smell of dry and wet ground coffee"},
            "Flavor": {"max": 10, "description": "Main taste characteristics"},
            "Aftertaste": {"max": 10, "description": "Duration and quality of residual flavor"},
            "Acidity": {"max": 10, "description": "Brightness and liveliness of coffee"},
            "Body": {"max": 10, "description": "Tactile sensation of liquid in mouth"},
            "Uniformity": {"max": 10, "description": "Consistency between cups"},
            "Balance": {"max": 10, "description": "Harmony between elements"},
            "Clean Cup": {"max": 10, "description": "Absence of defects"},
            "Sweetness": {"max": 10, "description": "Natural sweetness of coffee"},
            "Cupper's Points": {"max": 10, "description": "Overall subjective evaluation"}
        }
        
        self.defects = [
            "Over-fermented", "Moldy", "Earthy", "Astringent", 
            "Bitter", "Sour", "Green", "Phenolic", "Chemical", "Medicinal"
        ]
    
    def render_cupping_setup(self):
        """Initial cupping setup"""
        st.subheader("⚙️ Cupping Setup")
        
        col1, col2 = st.columns(2)
        
        with col1:
            session_name = st.text_input("Session Name", placeholder="Cupping - Lot 001")
            coffee_name = st.text_input("Coffee Name *", placeholder="El Paraiso Farm")
            origin = st.text_input("Origin *", placeholder="Huila, Colombia")
            variety = st.text_input("Variety", placeholder="Geisha, Caturra")
            
        with col2:
            farm = st.text_input("Farm", placeholder="El Paraiso Farm")
            altitude = st.number_input("Altitude (masl)", min_value=0, max_value=3000, step=50)
            harvest_date = st.date_input("Harvest Date")
            process_method = st.selectbox("Processing Method", [
                "Washed", "Natural", "Honey", "Pulped Natural", 
                "Semi-washed", "Anaerobic", "Carbonic Maceration", "Other"
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
        """Brewing parameters"""
        st.subheader("☕ Brewing Parameters")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            grind_size = st.selectbox("Grind Size", 
                ["Very Fine", "Fine", "Medium-Fine", "Medium", "Medium-Coarse", "Coarse"])
            water_temp = st.number_input("Water Temperature (°C)", 
                min_value=80, max_value=100, value=93)
            
        with col2:
            coffee_dose = st.number_input("Coffee Dose (g)", 
                min_value=1.0, max_value=50.0, value=8.25, step=0.25)
            water_volume = st.number_input("Water Volume (ml)", 
                min_value=50, max_value=500, value=150, step=10)
            
        with col3:
            brew_time = st.text_input("Contact Time", placeholder="4:00")
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
        """Individual evaluation per cup and cupper"""
        st.subheader(f"🏆 Evaluation - Cup {cup_number} - {cupper_name}")
        
        scores = {}
        total_score = 0
        
        # SCA attributes
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
        
        # Defects
        st.markdown("#### 🚫 Defects")
        defects_found = []
        defect_intensity = {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            for defect in self.defects[:len(self.defects)//2]:
                if st.checkbox(defect, key=f"defect_{defect}_{cup_number}_{cupper_name}"):
                    defects_found.append(defect)
                    intensity = st.slider(f"{defect} Intensity", 
                        min_value=1, max_value=4, value=2,
                        key=f"intensity_{defect}_{cup_number}_{cupper_name}")
                    defect_intensity[defect] = intensity
        
        with col2:
            for defect in self.defects[len(self.defects)//2:]:
                if st.checkbox(defect, key=f"defect_{defect}_{cup_number}_{cupper_name}"):
                    defects_found.append(defect)
                    intensity = st.slider(f"{defect} Intensity", 
                        min_value=1, max_value=4, value=2,
                        key=f"intensity_{defect}_{cup_number}_{cupper_name}")
                    defect_intensity[defect] = intensity
        
        # Calculate defect deduction
        defect_deduction = sum(defect_intensity.values()) * 2
        final_score = max(0, total_score - defect_deduction)
        
        # Show final score
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Base Score", f"{total_score:.2f}")
        with col2:
            st.metric("Defect Deduction", f"-{defect_deduction}")
        with col3:
            color = "normal"
            if final_score >= 85:
                color = "inverse"
            elif final_score < 70:
                color = "off"
            
            st.metric("**Final Score**", f"{final_score:.2f}/100", 
                delta=None)
        
        # Additional notes
        notes = st.text_area("Additional Notes", 
            placeholder="Specific observations for this cup...",
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
    """Complete cupping session manager"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.cupping_wheel = CuppingWheel()
        self.cupping_form = CuppingForm()
    
    def render_complete_session(self):
        """Render complete cupping session"""
        st.title("🏆 Professional Coffee Cupping")
        
        # Initial setup
        with st.expander("⚙️ Cupping Setup", expanded=True):
            coffee_info = self.cupping_form.render_cupping_setup()
            brewing_params = self.cupping_form.render_brewing_parameters()
        
        # Cupper and cup configuration
        st.subheader("👥 Evaluation Setup")
        
        col1, col2 = st.columns(2)
        
        with col1:
            num_cuppers = st.number_input("Number of Cuppers", 
                min_value=1, max_value=8, value=1)
            cuppers = []
            for i in range(num_cuppers):
                cupper = st.text_input(f"Cupper {i+1}", 
                    value=f"Cupper {i+1}", key=f"cupper_{i}")
                cuppers.append(cupper)
        
        with col2:
            num_cups = st.number_input("Number of Cups", 
                min_value=1, max_value=5, value=3)
            st.info(f"Will evaluate {num_cups} cups per {num_cuppers} cupper(s)")
            st.info(f"Total evaluations: {num_cups * num_cuppers}")
        
        # Flavor wheel
        with st.expander("🎯 Flavor Wheel", expanded=False):
            tab1, tab2 = st.tabs(["Manual Selection", "Visual Wheel"])
            
            with tab1:
                selected_flavors = self.cupping_wheel.render_flavor_wheel()
            
            with tab2:
                self.cupping_wheel.render_interactive_wheel()
        
        # Evaluations per cupper and cup
        st.subheader("📝 Evaluations")
        
        all_evaluations = {}
        
        # Create tabs per cupper
        if num_cuppers > 1:
            cupper_tabs = st.tabs(cuppers)
            
            for i, cupper in enumerate(cuppers):
                with cupper_tabs[i]:
                    all_evaluations[cupper] = {}
                    
                    # Create sub-tabs per cup for each cupper
                    cup_tabs = st.tabs([f"Cup {j+1}" for j in range(num_cups)])
                    
                    for j in range(num_cups):
                        with cup_tabs[j]:
                            evaluation = self.cupping_form.render_cupping_evaluation(j+1, cupper)
                            all_evaluations[cupper][f"cup_{j+1}"] = evaluation
        else:
            # Single cupper, tabs per cup
            cupper = cuppers[0]
            all_evaluations[cupper] = {}
            
            cup_tabs = st.tabs([f"Cup {j+1}" for j in range(num_cups)])
            
            for j in range(num_cups):
                with cup_tabs[j]:
                    evaluation = self.cupping_form.render_cupping_evaluation(j+1, cupper)
                    all_evaluations[cupper][f"cup_{j+1}"] = evaluation
        
        # Summary and saving
        st.subheader("📊 Results Summary")
        
        if st.button("📊 Calculate Averages", type="primary"):
            self.render_results_summary(all_evaluations, num_cups, cuppers)
        
        # Save button
        if st.button("💾 Save Cupping", type="primary"):
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
                st.success("✅ Cupping saved successfully!")
                st.balloons()
            else:
                st.error("❌ Error saving cupping")
    
    def render_results_summary(self, evaluations: Dict, num_cups: int, cuppers: List):
        """Render results summary"""
        
        # Calculate averages
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
            
            # Show metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Average Score", f"{overall_average:.2f}")
            
            with col2:
                st.metric("Highest Score", f"{max(all_scores):.2f}")
            
            with col3:
                st.metric("Lowest Score", f"{min(all_scores):.2f}")
            
            # Results chart
            if len(cuppers) > 1:
                # Comparison between cuppers
                cupper_names = list(cupper_averages.keys())
                averages = [cupper_averages[name]['average'] for name in cupper_names]
                
                fig = px.bar(
                    x=cupper_names,
                    y=averages,
                    title="Average Score by Cupper",
                    labels={'x': 'Cupper', 'y': 'Average Score'},
                    color=averages,
                    color_continuous_scale='Viridis'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Consistency between cups
            if num_cups > 1:
                cup_data = []
                for cupper, cups in evaluations.items():
                    for cup_id, evaluation in cups.items():
                        if evaluation and 'final_score' in evaluation:
                            cup_data.append({
                                'Cupper': cupper,
                                'Cup': cup_id.replace('cup_', 'Cup '),
                                'Score': evaluation['final_score']
                            })
                
                if cup_data:
                    import pandas as pd
                    df = pd.DataFrame(cup_data)
                    
                    fig = px.box(
                        df,
                        x='Cup',
                        y='Score',
                        title="Consistency Between Cups",
                        points="all"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
    
    def save_cupping_session(self, cupping_data: Dict) -> bool:
        """Save cupping session to database"""
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