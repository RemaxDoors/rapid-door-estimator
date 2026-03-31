import streamlit as st
import pandas as pd
from repositories.quote_repository import search_records, load_record_controls
from services.artifact_loader import load_artifacts
from services.configuration_loader import pivot_controls, apply_loaded_config_to_session

_, _, _, _, Data_Mapping, _ = load_artifacts()

st.title("Checking Old Configured Parts")

search_text = st.text_input("Search by quote, customer, part, or description")

if st.button("Search", key="BTN_SEARCH"):
    if not search_text.strip():
        st.warning("Enter a search value.")
    else:
        results_df = search_records(search_text)
        st.session_state["search_results"] = results_df

# -----------------------------
# Show search results
# -----------------------------
results_df = st.session_state.get("search_results", pd.DataFrame())

if not results_df.empty:
    st.subheader("Search Results")
    st.dataframe(results_df, width="stretch")

    result_options = results_df.index.tolist()

    selected_index = st.selectbox(
        "Select a quote line to load",
        options=result_options,
        format_func=lambda i: (
            f"Quote {results_df.loc[i, 'qmlQuoteID']} | "
            f"Line {results_df.loc[i, 'qmlQuoteLineID']} | "
            f"Part {results_df.loc[i, 'qmlPartID']} | "
            f"Customer {results_df.loc[i, 'CUSTOMERNAME']}"
        ),
        key="SELECT_QUOTE_LINE",
    )

    selected_row = results_df.loc[selected_index]

    st.markdown("### Selected Record")
    st.write({
        "Quote ID": selected_row["qmlQuoteID"],
        "Quote Line ID": selected_row["qmlQuoteLineID"],
        "Part ID": selected_row["qmlPartID"],
        "Door Model": selected_row["uqmlDoorModelID"],
        "Customer": selected_row["CUSTOMERNAME"],
        "Ship Customer": selected_row["SHIPCUSTOMERNAME"],
        "Unit Sell Price": selected_row["UNITSELLPRICE"],
        "Cost": selected_row["qmqTotalUnitCost"],
        "Margin": selected_row["uqmqMargin"],
    })

    # -----------------------------
    # Load configurator controls
    # -----------------------------
    if st.button("Load Configurator", key="BTN_LOAD_CONFIG"):
        try:
            controls_df = load_record_controls(
                quote_id=int(selected_row["qmlQuoteID"]),
                quote_line_id=int(selected_row["qmlQuoteLineID"]),
                part_id=str(selected_row["qmlPartID"]),
            )

            st.session_state["loaded_controls_raw"] = controls_df

            if controls_df.empty:
                st.warning("No configurator controls found for this record.")
            else:
                pivot_df = pivot_controls(controls_df)
                st.session_state["loaded_controls_pivot"] = pivot_df

                apply_loaded_config_to_session(pivot_df, Data_Mapping)

                st.success("Configurator values loaded into session.")
                st.dataframe(pivot_df, width="stretch")

        except Exception as e:
            st.error(f"Failed to load configurator controls: {e}")