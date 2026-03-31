import pandas as pd
import streamlit as st
from services.mapping_service import mapped_selectbox

# -----------------------------
# Door model, size and price - configurator selections
# -----------------------------
def render_installation_section(Data_Mapping: dict, door_height, door_width):
    st.header("Installation Details")
    with st.expander("Installation Options", expanded=True):
        up1, up2, up3,up4 = st.columns([0.75, 0.5, 0.5,1], vertical_alignment="top")
        with up1:        
            jobtype_label, jobtype_code = mapped_selectbox(
                "Job Type", "CMBJOBTYPE", Data_Mapping,key="CMBJOBTYPE",
                 default_label=st.session_state.get("CMBJOBTYPE", ""),
            )
            if jobtype_label == "Install":
                CHKINSAH = 1
            else:
                CHKINSAH = 0
            
            ch1, ch2, ch3 = st.columns(3)
            with ch1:
                CHKLIFTINGFRAME = int(st.checkbox("Lifting Frame Required?", value=bool(st.session_state.get("CHKLIFTINGFRAME", 0)), key="CHKLIFTINGFRAME"))
                CHKASSAREMOVAL = int(st.checkbox("Assa Door Removal Kit", value=bool(st.session_state.get("CHKASSAREMOVAL", 0)), key="CHKASSAREMOVAL"))
                CHKSPAREISOLATOR = int(st.checkbox("Spare Isolator Required?", value=bool(st.session_state.get("CHKSPAREISOLATOR", 0)), key="CHKSPAREISOLATOR"))
                CHKROLLERSHUTTERREMOVAL = int(st.checkbox("Roller Shutter Removal Kit?", value=bool(st.session_state.get("CHKROLLERSHUTTERREMOVAL", 0)), key="CHKROLLERSHUTTERREMOVAL")) 
            with ch2:    
                CHKLABSITEASS = int(st.checkbox("Site Assessment", value=bool(st.session_state.get("CHKLABSITEASS", 0)), key="CHKLABSITEASS"))
                CHKLABSITEATT = int(st.checkbox("Site Attendance / Visit", value=bool(st.session_state.get("CHKLABSITEATT", 0)), key="CHKLABSITEATT"))
                CHKINSAH = int(st.checkbox("After Hours?", value=bool(st.session_state.get("CHKINSAH", 0)), key="CHKINSAH"))
                CHKRETURNTRIP = int(st.checkbox("Return Trip for connect + commision", value=bool(st.session_state.get("CHKRETURNTRIP", 0)), key="CHKRETURNTRIP"))
            with ch3:    
                CHKINSRRD4X4 = int(st.checkbox("Rapid Door Installation - Up to 4x4", value=bool(st.session_state.get("CHKINSRRD4X4", 0)), key="CHKINSRRD4X4"))
                CHKINSRRD6X6 = int(st.checkbox("Rapid Door Installation - Above 4x4", value=bool(st.session_state.get("CHKINSRRD6X6", 0)), key="CHKINSRRD6X6"))
                CHKINSHSDFOLDING = int(st.checkbox("Concertina/Movifold Door Installation", value=bool(st.session_state.get("CHKINSHSDFOLDING", 0)), key="CHKINSHSDFOLDING"))
                CHKLABRRDREMOVAL = int(st.checkbox("Removal of existing Rapid Door", value=bool(st.session_state.get("CHKLABRRDREMOVAL", 0)), key="CHKLABRRDREMOVAL"))
                CHKLABRRDDISPOSAL = int(st.checkbox("Disposal of existing Rapid Door", value=bool(st.session_state.get("CHKLABRRDDISPOSAL", 0)), key="CHKLABRRDDISPOSAL"))
                if door_height <= 4000 and door_width <= 4000:
                    CHKINSRRD4X4 = 1
                    CHKINSRRD6X6 = 0
                else:
                    CHKINSRRD4X4 = 0
                    CHKINSRRD6X6 = 1
            
            fr1, fr2, fr3,fr4 = st.columns(4, vertical_alignment="bottom")

            with fr1:
                    NUMFREIGHTALLOWANCE = st.number_input(
                                    "Freight Allowance",
                                    min_value=0.0,
                                    value=float(st.session_state.get("NUMFREIGHTALLOWANCE", 0.0)),
                                    key="NUMFREIGHTALLOWANCE",
                                )
            with fr2:
                    rates_map = {"VIC": 0.5, "TAS": 1.4001, "NSW": 0.6, "SA": 0.7, "QLD": 0.9, "WA": 1.4002, "NT": 1.8}

                    CMBFREIGHTRATE_value = st.selectbox(
                                    "Freight Rate",
                                    options=list(rates_map.values()),
                                    format_func=lambda x: [k for k, v in rates_map.items() if v == x][0]
                                )
                    
                    def calculate_freight():
                        nLongest = (max(door_height, door_width) + 500) / 1000
                        nVol = 360 * nLongest * 0.8 * 0.8
                        nRate = nVol * CMBFREIGHTRATE_value
                        st.session_state["NUMFREIGHTALLOWANCE"] = round(nRate, 2)
            with fr3:
                    
                    st.button("Calculate Freight", on_click=calculate_freight)
    

           
        with up2:
            NUMDRIVINGTIME =st.number_input(
                "Driving Time (hours)",
                min_value=0,
                value=int(st.session_state.get("NUMDRIVINGTIME", 0)),
                key="NUMDRIVINGTIME",
                placeholder="Driving Time"
            )
            NUMTOTALDOORSPROJ = st.number_input(
                "Total Doors in Project",
                min_value=0,
                value=int(st.session_state.get("NUMTOTALDOORSPROJ", 0)),
                placeholder="Total Doors"
            )
            NUMESTPROJECTSONRUN = st.number_input(
                "Estimated Project on Install Run",
                min_value=0,
                value=int(st.session_state.get("NUMESTPROJECTSONRUN", 0)),
                placeholder="Estimated Project"
            )
        with up3:   
            CHKACCOM = int(st.checkbox("Accommodation Required?"))
            
            NUMACCOMNIGHT = st.number_input(
                "Number of Nights for Accommodation",
                min_value=0,
                value=int(st.session_state.get("NUMACCOMNIGHT", 0)),
                placeholder="Number of Nights"
            )
            
            if NUMACCOMNIGHT >= 1:
                CHKACCOM = 1

            NUMPERSONINSTALL = st.number_input(
                "Number of People on Install",
                min_value=0,
                value=int(st.session_state.get("NUMPERSONINSTALL", 2)),
                placeholder="Number of People"
            )
        with up4:
            NUMLUMSUM = st.number_input(
                "LUMP SUM COST (if applicable)",
                min_value=0,
                value=int(st.session_state.get("NUMLUMSUM", 0))
            )
    installation_input_data = {
                    "CHKLIFTINGFRAME": CHKLIFTINGFRAME,
                    "CHKASSAREMOVAL": CHKASSAREMOVAL,
                    "CHKSPAREISOLATOR": CHKSPAREISOLATOR,
                    "CHKROLLERSHUTTERREMOVAL": CHKROLLERSHUTTERREMOVAL,
                    "CMBJOBTYPE": jobtype_code,
                    "CHKLABSITEASS": CHKLABSITEASS,
                    "CHKLABSITEATT": CHKLABSITEATT,
                    "CHKINSAH": CHKINSAH,
                    "CHKRETURNTRIP": CHKRETURNTRIP,
                    "NUMDRIVINGTIME": NUMDRIVINGTIME,
                    "NUMTOTALDOORSPROJ": NUMTOTALDOORSPROJ,
                    "NUMESTPROJECTSONRUN": NUMESTPROJECTSONRUN,
                    "CHKACCOM": CHKACCOM,
                    "NUMACCOMNIGHT": NUMACCOMNIGHT,
                    "NUMPERSONINSTALL": NUMPERSONINSTALL,
                    "NUMLUMSUM": NUMLUMSUM,
                    "NUMFREIGHTALLOWANCE": NUMFREIGHTALLOWANCE,
                    "CHKINSRRD4X4": CHKINSRRD4X4,
                    "CHKINSRRD6X6": CHKINSRRD6X6,
                    "CHKINSHSDFOLDING" :CHKINSHSDFOLDING,
                    "CHKLABRRDREMOVAL" :CHKLABRRDREMOVAL,
                    "CHKLABRRDDISPOSAL":CHKLABRRDDISPOSAL

              }
    installation_df = pd.DataFrame([installation_input_data])
    return {
        "installation_input_data": installation_input_data,
        "installation_df": installation_df,
        "jobtype_label": jobtype_label,
        "jobtype_code": jobtype_code,
    }