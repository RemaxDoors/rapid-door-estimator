import streamlit as st
import pandas as pd
from services.artifact_loader import load_artifacts
import streamlit as st
from services.artifact_loader import load_artifacts
from services.estimation_service import (
    combine_inputs,
    build_prediction_input,
    estimate_price_cost_margin,
)
from services.export_service import generate_excel_export
from ui.door_section import render_door_section
from ui.installation_section import render_installation_section
from ui.curtain_section import render_curtain_section
from ui.door_section import render_door_section
from ui.installation_section import render_installation_section
from ui.curtain_section import render_curtain_section
from services.export_service import generate_excel_export
# -----------------------------
# load artifacts
# -----------------------------
model_costing, model_costing_features, model_pricing, model_pricing_features, Data_Mapping, price_lookup = load_artifacts()

st.set_page_config(page_title="Rapid Door Estimator", layout="wide")
st.title("Rapid Door Estimator")

tab_door, tab_install, tab_curtain = st.tabs(["Door", "🛠 Installation", "🪟 Curtain"])
with tab_door:
    door_result = render_door_section(Data_Mapping, price_lookup)


door_export_data = door_result["export_data"]
door_model_label = door_result["door_model_label"]
door_model_code = door_result["door_model_code"]
door_sell_price = door_result["door_sell_price"]
NUMDOORHEIGHT = door_result["NUMDOORHEIGHT"]
NUMDOORWIDTH = door_result["NUMDOORWIDTH"]

with tab_install:
    installation_result = render_installation_section(
        Data_Mapping,
        NUMDOORHEIGHT,
        NUMDOORWIDTH,
    )


with tab_curtain:
    curtain_result = render_curtain_section(Data_Mapping)

# -----------------------------
# unpack section results
# -----------------------------
door_input_data = door_result["door_input_data"]
door_df = door_result["door_df"]

installation_input_data = installation_result["installation_input_data"]
installation_df = installation_result["installation_df"]

curtain_input_data = curtain_result["curtain_input_data"]
curtain_df = curtain_result["curtain_df"]

# -----------------------------
# Combine all current inputs into one dictionary
# -----------------------------
combined_inputs = combine_inputs(
    door_input_data,
    installation_input_data,
    curtain_input_data,
)

pricing_prediction_df = build_prediction_input(combined_inputs, model_pricing_features)
costing_prediction_df = build_prediction_input(combined_inputs, model_costing_features)

# -----------------------------
# Discount input
# -----------------------------
RESELLERDISCOUNT = st.number_input(
    "Reseller Discount (%)",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    key="RESELLERDISCOUNT",
)

# -----------------------------
# Predict
# -----------------------------
result = None
shap_result = None

if "result" not in st.session_state:
        st.session_state.result = None

if "shap_result" not in st.session_state:
    st.session_state.shap_result = None

if st.button("Estimate Price"):
    try:
        st.session_state.result = estimate_price_cost_margin(
            model_pricing=model_pricing,
            model_costing=model_costing,
            pricing_prediction_df=pricing_prediction_df,
            costing_prediction_df=costing_prediction_df,
            reseller_discount=RESELLERDISCOUNT,
        )

    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")

result = st.session_state.result
shap_result = st.session_state.shap_result
# -----------------------------
# Display prediction
# -----------------------------
if result is not None:
    with st.expander("Prediction", expanded=True):
        left_col, right_col = st.columns([1.25, 1], vertical_alignment="top")

        # -----------------------------
        # Left side: summary metrics
        # -----------------------------
        with left_col:
            st.subheader("Summary")

            c1, c2, c3 = st.columns(3)
            c1.metric("Estimated Price", f"${result['price_pred']:,.2f}")
            c2.metric("Estimated Cost", f"${result['cost_pred']:,.2f}")
            c3.metric("Margin %", f"{result['margin_pct'] * 100:.2f}%")

            c4, c5 = st.columns(2)
            c4.metric("Discounted Sell Price", f"${result['unit_sell_price']:,.2f}")
            c5.metric("Margin Value", f"${result['margin_value']:,.2f}")
               
# -----------------------------
# export
# -----------------------------
st.divider()
raw_export_data  = door_result["export_data"]
export_bytes = generate_excel_export(raw_export_data)

st.download_button(
    label="Download M1 Export",
    data=export_bytes,
    file_name="configurator_export.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    key="DOWNLOAD_MAIN_EXPORT",
)