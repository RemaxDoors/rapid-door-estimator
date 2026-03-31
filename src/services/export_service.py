import io
import pandas as pd


def generate_excel_export(raw_export_data: dict) -> bytes:
    filtered_export_data = {}

    for param_name, label_value in raw_export_data.items():
        if param_name.startswith("CMB") and label_value not in ["", 0, None]:
            filtered_export_data[param_name] = label_value

        elif param_name.startswith("CHK") and label_value == 1:
            filtered_export_data[param_name] = "1"

        elif param_name.startswith("NUM") and label_value not in [None, ""]:
            filtered_export_data[param_name] = label_value

    df_export = pd.DataFrame(list(filtered_export_data.items()))

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_export.to_excel(
            writer,
            index=False,
            header=False,
            sheet_name="M1ParameterList",
        )

        worksheet = writer.sheets["M1ParameterList"]
        worksheet["G1"] = len(df_export)

    output.seek(0)
    return output.getvalue()