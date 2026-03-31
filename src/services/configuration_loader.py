import pandas as pd
import streamlit as st


def pivot_controls(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    pivot_df = (
        df.pivot_table(
            index=[
                "Unique_ID",
                "Part-ID",
                "DoorModelID",
                "DoorSellPrice",
                "UNIT SELL PRICE",
                "QTY",
            ],
            columns="xaiControlName",
            values="xaiValue",
            aggfunc="first",
        )
        .reset_index()
    )

    pivot_df.columns.name = None
    pivot_df.columns = [str(c).strip() for c in pivot_df.columns]

    return pivot_df


def clean_loaded_value(value):
    if pd.isna(value):
        return None

    if isinstance(value, str):
        value = value.strip()

        if len(value) >= 2:
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1].strip()

        if value.lower() in {"none", "null", "nan", ""}:
            return None

    return value


def _to_float(value, default=0.0):
    try:
        if value in [None, ""]:
            return default
        return float(value)
    except Exception:
        return default


def _to_int(value, default=0):
    try:
        if value in [None, ""]:
            return default
        return int(float(value))
    except Exception:
        return default


def _to_checkbox(value):
    if value is None:
        return 0
    cleaned = str(value).strip().strip('"').strip("'").lower()
    return 1 if cleaned in {"1", "true", "yes"} else 0


def apply_loaded_config_to_session(pivot_df: pd.DataFrame, data_mapping: dict):
    if pivot_df.empty:
        return

    row = pivot_df.iloc[0].to_dict()

    expected_fields = {
        "CMBDOORMODEL",
        "NUMDOORHEIGHT",
        "NUMDOORWIDTH",
        "NUMCEILINGHEIGHT",
        "DoorSellPrice",
        "CMBMOTORORIDE",
        "CMBTRACKCONFIG",
        "CMBWINDTRACK",
        "CMBCONTROLLERENCLOSURE",
        "CMBMOTORSHROUD",
        "CMBMOTORSPEC",
        "CMBBRUSHSEAL",
        "CMBGPOISO",
        "CMBPOWERSUPPLY",
        "CMBTRAFFICLIGHT",
        "CMBPEBEAMS",
        "CHKHYPERLIFT",
        "CHKINTERLOCK",
        "CHKSTAINLESS",
        "CHKEX35FELT",
        "CMBUPS",
        "CMBCUSTSTEEL",
        "CMBREARHOODBRUSHSEAL",
        "CMBSPECIALCONDUIT",
        "CMBCOLOURFINISHTYPE",
        "CMBES40FASCIA",
        "CMBES40VSDMTR",
        "CMBHEATTRACELEG",
        "CMBGEARBOXHEATER",
        "CMBHEATTRACEHOOD",
        "CMBFELTSEAL",
        "CMBPED1",
        "CMBPED2",
        "CMBRADAR1",
        "CMBRADAR2",
        "CMBACT1",
        "CMBACT2",
        "CMBACT3",
        "CMBACT4",
        "CMBFLOORLOOPINSTALL",
        "QTY",
        "CHKLIFTINGFRAME",
        "CHKASSAREMOVAL",
        "CHKSPAREISOLATOR",
        "CHKROLLERSHUTTERREMOVAL",
        "CMBJOBTYPE",
        "CHKLABSITEASS",
        "CHKLABSITEATT",
        "CHKINSAH",
        "CHKRETURNTRIP",
        "NUMDRIVINGTIME",
        "NUMTOTALDOORSPROJ",
        "NUMESTPROJECTSONRUN",
        "CHKACCOM",
        "NUMACCOMNIGHT",
        "NUMPERSONINSTALL",
        "NUMLUMSUM",
        "NUMFREIGHTALLOWANCE",
        "CMBCURTAINCOLOUR",
        "CHKSLOPEREQUIRED",
        "CHKCUSTBOTTOMEDGE",
        "CHKCUSTSCREENPRINT",
        "CHKEMERGEZIP",
        "CHKDRIPEDGE",
        "CHKCOMOWEAR",
        "CHKEX35BVSEAL",
        "CMBWINDOWTYPEDEFAULT",
        "NUMWINDOWDEFAULT",
        "CMBNUMWINDROWS",
        "CHKUSEDEFAULTWINPERROW",
        "NUMWINDOWREQ",
    }

    numeric_float_fields = {
        "NUMDOORHEIGHT",
        "NUMDOORWIDTH",
        "NUMCEILINGHEIGHT",
        "DoorSellPrice",
        "NUMFREIGHTALLOWANCE",
        "NUMDRIVINGTIME",
        "NUMESTPROJECTSONRUN",
        "NUMLUMSUM",
    }

    numeric_int_fields = {
        "QTY",
        "NUMTOTALDOORSPROJ",
        "NUMACCOMNIGHT",
        "NUMPERSONINSTALL",
        "NUMWINDOWDEFAULT",
        "NUMWINDOWREQ",
        "NUMES40PANELSREQ",
    }

    checkbox_fields = {
        "CHKHYPERLIFT",
        "CHKINTERLOCK",
        "CHKSTAINLESS",
        "CHKEX35FELT",
        "CHKLIFTINGFRAME",
        "CHKASSAREMOVAL",
        "CHKSPAREISOLATOR",
        "CHKROLLERSHUTTERREMOVAL",
        "CHKLABSITEASS",
        "CHKLABSITEATT",
        "CHKINSAH",
        "CHKRETURNTRIP",
        "CHKACCOM",
        "CHKSLOPEREQUIRED",
        "CHKCUSTBOTTOMEDGE",
        "CHKCUSTSCREENPRINT",
        "CHKEMERGEZIP",
        "CHKDRIPEDGE",
        "CHKCOMOWEAR",
        "CHKEX35BVSEAL",
        "CHKUSEDEFAULTWINPERROW",
    }

    for field in expected_fields:
        raw_value = clean_loaded_value(row.get(field))

        if field in numeric_float_fields:
            st.session_state[field] = _to_float(raw_value, 0.0)

        elif field in numeric_int_fields:
            st.session_state[field] = _to_int(raw_value, 0)

        elif field in checkbox_fields:
            st.session_state[field] = _to_checkbox(raw_value)

        elif field.startswith("CMB"):
            st.session_state[field] = raw_value if raw_value is not None else ""

        else:
            st.session_state[field] = raw_value if raw_value is not None else 0