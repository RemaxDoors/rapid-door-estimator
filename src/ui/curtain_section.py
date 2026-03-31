import pandas as pd
import streamlit as st
from services.mapping_service import mapped_selectbox


def render_curtain_section(Data_Mapping: dict):
    with st.expander("Curtain Options", expanded=True):
        curt1, curt2,curt3 = st.columns([0.75,1,1.5], vertical_alignment="top")
        with curt1:

            curtaincolour_label, curtaincolour_code = mapped_selectbox("Select Curtain Colour", "CMBCURTAINCOLOUR", Data_Mapping,   key="CMBCURTAINCOLOUR",default_label=st.session_state.get("CMBCURTAINCOLOUR", ""),)
            CHKSLOPEREQUIRED = int(st.checkbox("Slope Edge Required", value=bool(st.session_state.get("CHKSLOPEREQUIRED", 0)), key="CHKSLOPEREQUIRED"))
            CHKCUSTBOTTOMEDGE = int(st.checkbox("Custom Bottom Edge (Color)"))
            CHKCUSTSCREENPRINT = int(st.checkbox("Custom Screen Printing")  )
            CHKEMERGEZIP = int(st.checkbox("Emergency Zip with 'Push here' Graphic"))
        with curt2:
            CHKDRIPEDGE  = int(st.checkbox("Drip Edge Required"))
            CHKCOMOWEAR = int(st.checkbox("Como Wear Strip"))
            CHKEX35BVSEAL = int(st.checkbox("EX BV Seal"))
        with curt3:
            windowtypedefault_label, windowtypedefault_code = mapped_selectbox("Window Type", "CMBWINDOWTYPEDEFAULT",Data_Mapping,   key="CMBWINDOWTYPEDEFAULT",default_label=st.session_state.get("CMBWINDOWTYPEDEFAULT", ""),)
            NUMWINDOWDEFAULT = st.number_input(
                        "Default # of Windows",
                        min_value=0,
                        value=int(st.session_state.get("NUMWINDOWDEFAULT", 0)),
                        key="NUMWINDOWDEFAULT",
                    )
            CHKUSEDEFAULTWINPERROW = int(st.checkbox("Use Default # Windows"))
            NUMWINDOWREQ = st.number_input("# of Windows Required Per Row",
                                            min_value=0,
                                            value=None,width = 100
                                            )

            


    curtain_input_data = {
                      "CMBCURTAINCOLOUR":curtaincolour_code,
                      "CHKSLOPEREQUIRED" :CHKSLOPEREQUIRED,
                      "CHKCUSTBOTTOMEDGE" :CHKCUSTBOTTOMEDGE,
                      "CHKCUSTSCREENPRINT":CHKCUSTSCREENPRINT,
                      "CHKEMERGEZIP":CHKEMERGEZIP,
                      "CHKDRIPEDGE":CHKDRIPEDGE,
                      "CHKCOMOWEAR":CHKCOMOWEAR,
                      "CHKEX35BVSEAL":CHKEX35BVSEAL,
                      "CMBWINDOWTYPEDEFAULT":windowtypedefault_code,
                      "NUMWINDOWDEFAULT":NUMWINDOWDEFAULT,
                      "CHKUSEDEFAULTWINPERROW":CHKUSEDEFAULTWINPERROW,
                      "NUMWINDOWREQ":NUMWINDOWREQ,

                      }
    
    curtain_df = pd.DataFrame([curtain_input_data])
    return {
        "curtain_input_data": curtain_input_data,
        "curtain_df": curtain_df,
    }