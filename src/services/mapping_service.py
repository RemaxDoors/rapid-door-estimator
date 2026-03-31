import streamlit as st


def get_code_from_label(mapping_key: str, label, data_mapping: dict):
    mapping = data_mapping.get(mapping_key, {})
    if not mapping or label in [None, "", 0]:
        return 0

    cleaned_label = str(label).strip().strip('"').strip("'")

    # exact label match
    if cleaned_label in mapping:
        return mapping[cleaned_label]

    # fallback: case-insensitive label match
    for display_label, code in mapping.items():
        if str(display_label).strip().lower() == cleaned_label.lower():
            return code

    return 0


def get_label_from_code(mapping_key: str, code, data_mapping: dict):
    mapping = data_mapping.get(mapping_key, {})
    if not mapping:
        return None

    for label, mapped_code in mapping.items():
        if mapped_code == code or str(mapped_code) == str(code):
            return label

    return None


def resolve_loaded_mapping_value(mapping_key: str, loaded_value, data_mapping: dict):
    """
    M1 loads LABELS.
    This function converts a loaded label into the code used by the app.
    If the value is already a code, it also handles that.
    """
    mapping = data_mapping.get(mapping_key, {})
    if not mapping or loaded_value in [None, "", 0]:
        return 0

    cleaned_value = str(loaded_value).strip().strip('"').strip("'")

    # Case 1: loaded value is the label
    if cleaned_value in mapping:
        return mapping[cleaned_value]

    # Case 1b: case-insensitive label match
    for display_label, code in mapping.items():
        if str(display_label).strip().lower() == cleaned_value.lower():
            return code

    # Case 2: loaded value is already the code
    for _, code in mapping.items():
        if str(code) == cleaned_value:
            return code

    return 0


def mapped_selectbox(
    label: str,
    mapping_key: str,
    data_mapping: dict,
    key: str | None = None,
    default_label=None,
    mandatory: bool = False,
):
    mapping = data_mapping.get(mapping_key, {})

    if not mapping:
        st.warning(f"No mapping found for {mapping_key}")
        return None, None

    display_values = [""] + list(mapping.keys())

    cleaned_default_label = ""
    if default_label not in [None, "", 0]:
        cleaned_default_label = str(default_label).strip().strip('"').strip("'")

    default_index = 0
    if cleaned_default_label:
        # exact match
        if cleaned_default_label in mapping:
            default_index = display_values.index(cleaned_default_label)
        else:
            # case-insensitive label match
            for i, display_label in enumerate(display_values):
                if display_label and str(display_label).strip().lower() == cleaned_default_label.lower():
                    default_index = i
                    break

    # IMPORTANT:
    # widget key should not be the raw field name, otherwise Streamlit
    # stores the selected LABEL in the same key used by your loader.
    widget_key = key or f"{mapping_key}__widget"

    selected_label = st.selectbox(
        label,
        options=display_values,
        index=default_index,
        key=widget_key,
    )

    if selected_label in [None, ""]:
        if mandatory:
            return None, None
        return 0, 0

    if selected_label not in mapping:
        if mandatory:
            return None, None
        return 0, 0

    selected_code = mapping[selected_label]
    return selected_label, selected_code