import joblib
import streamlit as st
from config import PRICING_MODEL_DIR, COSTING_MODEL_DIR
from repositories.pricing_lookup import DoorPriceLookup

@st.cache_resource
def load_artifacts():
    model_pricing = joblib.load(PRICING_MODEL_DIR / "door_price_model.pkl")
    model_pricing_features = joblib.load(PRICING_MODEL_DIR / "model_features.pkl")
    model_costing = joblib.load(COSTING_MODEL_DIR / "LGBM_door_COSTING_model.pkl")
    model_costing_features = joblib.load(COSTING_MODEL_DIR / "LGBM__costing_model_features.pkl")
    Data_Mapping = joblib.load(PRICING_MODEL_DIR / "data_mapping.pkl")
    price_lookup = DoorPriceLookup()
    return model_costing, model_costing_features, model_pricing, model_pricing_features, Data_Mapping, price_lookup,