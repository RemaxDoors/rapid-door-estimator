import pandas as pd
import numpy as np
import re


def combine_inputs(
    door_input_data: dict,
    installation_input_data: dict,
    curtain_input_data: dict,
) -> dict:
    return {
        **door_input_data,
        **installation_input_data,
        **curtain_input_data,
    }


def build_prediction_input(combined_inputs: dict, model_features) -> pd.DataFrame:
    prediction_input_data = {str(col): 0 for col in model_features}

    for col in model_features:
        col_str = str(col)
        if col_str in combined_inputs:
            val = combined_inputs[col_str]
            prediction_input_data[col_str] = val if val is not None else 0

    prediction_df = pd.DataFrame([prediction_input_data])

    feature_cols = [str(col) for col in model_features]
    prediction_df = prediction_df[feature_cols]
    prediction_df.columns = prediction_df.columns.astype(str)

    return prediction_df


def estimate_price_cost_margin(
    model_pricing,
    model_costing,
    pricing_prediction_df: pd.DataFrame,
    costing_prediction_df: pd.DataFrame,
    reseller_discount: float = 0.0,
) -> dict:
    price_pred = model_pricing.predict(pricing_prediction_df)[0]
    cost_pred = model_costing.predict(costing_prediction_df)[0]

    unit_sell_price = price_pred * (1 - (reseller_discount / 100))
    margin_value = unit_sell_price - cost_pred
    margin_pct = (margin_value / unit_sell_price) if unit_sell_price != 0 else 0

    return {
        "price_pred": price_pred,
        "cost_pred": cost_pred,
        "unit_sell_price": unit_sell_price,
        "margin_value": margin_value,
        "margin_pct": margin_pct,
    }


