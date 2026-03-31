import pandas as pd
import streamlit as st
from services.mapping_service import mapped_selectbox

# -----------------------------
# Door model, size and price - configurator selections
# -----------------------------
def render_door_section(Data_Mapping: dict, price_lookup):
    top1, top2, top3, top4, top5 = st.columns([1, 1.5, 1, 1, 1])

    with top1:
        door_model_label, door_model_code = mapped_selectbox(
            "Door Model",
            "CMBDOORMODEL",
            Data_Mapping,
            key="CMBDOORMODEL",
            default_label=st.session_state.get("CMBDOORMODEL", ""),
        )
    
    with top2:
        NUMDOORHEIGHT = st.number_input(
            "Door Height (mm)",
            min_value=0,
            value=int(st.session_state.get("NUMDOORHEIGHT", 0)),
            placeholder="Height"
        )

    with top3:
        NUMDOORWIDTH = st.number_input(
            "Door Width (mm)",
            min_value=0,
            value=int(st.session_state.get("NUMDOORWIDTH", 0)),
            placeholder="Width"
        )
    with top4:
        NUMCEILINGHEIGHT = st.number_input(
            "Ceiling Height (mm)",
            min_value=0,
            value=int(st.session_state.get("NUMCEILINGHEIGHT", 0)),
            placeholder="Ceiling Height"
        )

    door_sell_price = None
    if door_model_code and NUMDOORWIDTH > 0 and NUMDOORHEIGHT > 0:
        door_sell_price = price_lookup.get_door_sell_price(
            door_model=door_model_label,
            width=NUMDOORWIDTH,
            height=NUMDOORHEIGHT
        )
        
    with top5:
        st.markdown("**DoorSellPrice**")
        if door_sell_price:
            st.success(f"{door_sell_price:,.2f}")
        else:
            st.caption("Select model + size")

        QTY = st.number_input(
            "Quantity",
            min_value=1,
            value=int(st.session_state.get("QTY", 1)),
            step=1
        )
        

    # -----------------------------
    # overview
    # -----------------------------
    with st.expander("Configurations", expanded=True):
        con1, con2, con3 = st.columns(3, vertical_alignment="top")
        with con1:
            with st.expander("Overview", expanded=True):
                ov1, ov2, = st.columns([1.5,1], vertical_alignment="top")
                with ov1:
                        cmbGPOISO_label, cmbGPOISO_code = mapped_selectbox(
                           "GPO / Isolator",
                            "CMBGPOISO",
                            Data_Mapping,
                            key="CMBGPOISO",
                            default_label=st.session_state.get("CMBGPOISO", ""),
                            mandatory=True,
                        )
                        motor_oride_label, motor_oride_code = mapped_selectbox(
                            "Hand Crank / Chain Drive",
                            "CMBMOTORORIDE",
                            Data_Mapping,
                            key="CMBMOTORORIDE",
                            default_label=st.session_state.get("CMBMOTORORIDE", ""),
                        )
                        track_config_label, track_config_code = mapped_selectbox(
                            "Tracks Proud / Conc?",
                            "CMBTRACKCONFIG",
                            Data_Mapping,
                            key="CMBTRACKCONFIG",
                            default_label=st.session_state.get("CMBTRACKCONFIG", ""),
                        )
                        wind_track_label, wind_track_code = mapped_selectbox(
                            "High Wind Tracks Required",
                            "CMBWINDTRACK",
                            Data_Mapping,
                            key="CMBWINDTRACK",
                            default_label=st.session_state.get("CMBWINDTRACK", ""),
                        )

                with ov2:
                        cmbPowerSupply_label, cmbPowerSupply_code = mapped_selectbox(
                            "Power Supply",
                            "CMBPOWERSUPPLY",
                            Data_Mapping,
                            key="CMBPOWERSUPPLY",
                            default_label=st.session_state.get("CMBPOWERSUPPLY", ""),
                        )
                
        with con2:
                    # -----------------------------
                    # common options
                    # -----------------------------
            with st.expander("Upgrades / Common Options", expanded=True):
                up1, up2, up3, up4  = st.columns([1.25, 1.75, 1.5, 1.5], vertical_alignment="top")

                with up1:
                            
                            CHKHYPERLIFT = int(st.checkbox("Hyperlift Motor?", value=bool(st.session_state.get("CHKHYPERLIFT", 0)), key="CHKHYPERLIFT"))
                            CHKINTERLOCK = int(st.checkbox("Interlock?", value=bool(st.session_state.get("CHKINTERLOCK", 0)), key="CHKINTERLOCK"))
                            CHKSTAINLESS = int(st.checkbox("Movisan (Stainless Spec)", value=bool(st.session_state.get("CHKSTAINLESS", 0)), key="CHKSTAINLESS"))
                            CHKEX35FELT = int(st.checkbox("EX35 Felt", value=bool(st.session_state.get("CHKEX35FELT", 0)), key="CHKEX35FELT"))

                with up2:
                            controller_enclosure_label, controller_enclosure_code = mapped_selectbox(
                                "Controller Enclosure", "CMBCONTROLLERENCLOSURE", Data_Mapping, key="CMBCONTROLLERENCLOSURE",default_label=st.session_state.get("CMBCONTROLLERENCLOSURE", "")
                            )
                            motor_shroud_label, motor_shroud_code = mapped_selectbox(
                                "Motor Shroud", "CMBMOTORSHROUD", Data_Mapping, key="CMBMOTORSHROUD",default_label=st.session_state.get("CMBMOTORSHROUD", ""),
                            )
                            motor_spec_label, motor_spec_code = mapped_selectbox(
                                "Brake/VSD Protection", "CMBMOTORSPEC", Data_Mapping,   key="CMBMOTORSPEC",default_label=st.session_state.get("CMBMOTORSPEC", ""),
                            )
                            brushseal_label, brushseal_code = mapped_selectbox(
                                "Brush Seal", "CMBBRUSHSEAL", Data_Mapping, key="CMBBRUSHSEAL",default_label=st.session_state.get("CMBBRUSHSEAL", ""),
                            )
                            traffic_light_label, traffic_light_code = mapped_selectbox(
                                "Traffic Light", "CMBTRAFFICLIGHT", Data_Mapping,   key="CMBTRAFFICLIGHT",default_label=st.session_state.get("CMBTRAFFICLIGHT", ""),
                            )
                            pe_beam_label, PE_Beam_code = mapped_selectbox(
                                "PE Beam", "CMBPEBEAMS", Data_Mapping,   key="CMBPEBEAMS",default_label=st.session_state.get("CMBPEBEAMS", ""),
                            )

                with up3:
                            UPS_label, UPS_code = mapped_selectbox(
                                "UPS", "CMBUPS", Data_Mapping
                            )
                            custsteel_label, custsteel_code = mapped_selectbox(
                                "Custom Steel Work", "CMBCUSTSTEEL", Data_Mapping,   key="CMBCUSTSTEEL",default_label=st.session_state.get("CMBCUSTSTEEL", ""),
                            )
                            rearhoodbrushseal_label, rearhoodbrushseal_code = mapped_selectbox(
                                "Rear Hood Brush Seal", "CMBREARHOODBRUSHSEAL", Data_Mapping,   key="CMBREARHOODBRUSHSEAL",default_label=st.session_state.get("CMBREARHOODBRUSHSEAL", ""),
                            )
                            specialconduit_label, specialconduit_code = mapped_selectbox(
                                "Conduit", "CMBSPECIALCONDUIT", Data_Mapping,   key="CMBSPECIALCONDUIT",default_label=st.session_state.get("CMBSPECIALCONDUIT", ""),
                            )
                            colourfinishtype_label, colourfinishtype_code = mapped_selectbox(
                                "Powdercoat / Painting", "CMBCOLOURFINISHTYPE", Data_Mapping,   key="CMBCOLOURFINISHTYPE",default_label=st.session_state.get("CMBCOLOURFINISHTYPE", ""),
                            )
                with up4:
                            expand_es40 = False
                            expand_thermic_movi = False
                            if door_model_label and door_model_label != "":
                                model_upper = door_model_label.upper() 
                                
                                if "ES40" in model_upper:
                                    expand_es40 = True
                                if "THERMIC" in model_upper or "MOVICHILL" in model_upper:
                                    expand_thermic_movi = True

                            with st.expander("ES40 Only", expanded=expand_es40):
                                cmbES40Fascia_label, cmbES40Fascia_code = mapped_selectbox(
                                    "Fascia", "CMBES40FASCIA", Data_Mapping,key="CMBES40FASCIA",default_label=st.session_state.get("CMBES40FASCIA", ""),
                                )
                                cmbES40VSDMtr_LABEL, cmbES40VSDMtr_CODE = mapped_selectbox(
                                    "VSD Motor", "CMBES40VSDMTR", Data_Mapping,key="CMBES40VSDMTR",default_label=st.session_state.get("CMBES40VSDMTR", ""),
                                )
                            with st.expander("THERMIC+MOVICHILL ONLY", expanded=expand_thermic_movi):
                                    cmbHeatTraceLeg_label, cmbHeatTraceLeg_code = mapped_selectbox(
                                        "Heat Trace Legs", "CMBHEATTRACELEG", Data_Mapping,key="CMBHEATTRACELEG",default_label=st.session_state.get("CMBHEATTRACELEG", ""),
                                    )
                                    cmbGearboxHeater_label, cmbGearboxHeater_code = mapped_selectbox(
                                        "Gearbox Heater", "CMBGEARBOXHEATER", Data_Mapping,key="CMBGEARBOXHEATER",default_label=st.session_state.get("CMBGEARBOXHEATER", ""),
                                    )
                                    cmbHeatTraceHood_label, cmbHeatTraceHood_code = mapped_selectbox(
                                        "In Hood", "CMBHEATTRACEHOOD", Data_Mapping,key="CMBHEATTRACEHOOD",default_label=st.session_state.get("CMBHEATTRACEHOOD", ""),
                                    )
                                    cmbFeltSeal_label, cmbFeltSeal_code = mapped_selectbox(
                                        "Felt Seal", "CMBFELTSEAL", Data_Mapping,key="CMBFELTSEAL",default_label=st.session_state.get("CMBFELTSEAL", ""),
                                    )
            with con3:
                with st.expander("Activations", expanded=True):
                    CmbPed1_label, CmbPed1_code = mapped_selectbox(
                        "Pedestrian Button 1", "CMBPED1", Data_Mapping,key="CMBPED1",default_label=st.session_state.get("CMBPED1", ""),
                    )
                    CmbPed2_label, CmbPed2_code = mapped_selectbox(
                        "Pedestrian Button 2", "CMBPED2", Data_Mapping,key="CMBPED2",default_label=st.session_state.get("CMBPED2", ""),
                    )
                    CmbRadar1_label, CmbRadar1_code = mapped_selectbox(
                        "Door Side Radar", "CMBRADAR1", Data_Mapping,key="CMBRADAR1",default_label=st.session_state.get("CMBRADAR1", ""),
                    )
                    CmbRadar2_label, CmbRadar2_code = mapped_selectbox(
                        "Non Door Side Radar", "CMBRADAR2", Data_Mapping,key="CMBRADAR2",default_label=st.session_state.get("CMBRADAR2", ""),
                    )
                    CmbAct1_label, CmbAct1_code = mapped_selectbox(
                        "Activation 1", "CMBACT1", Data_Mapping,key="CMBACT1",default_label=st.session_state.get("CMBACT1", ""),
                    )
                    CmbAct2_label, CmbAct2_code = mapped_selectbox(
                        "Activation 2", "CMBACT2", Data_Mapping ,key="CMBACT2",default_label=st.session_state.get("CMBACT2", ""),
                    )
                    CmbAct3_label, CmbAct3_code = mapped_selectbox(
                        "Activation 3", "CMBACT3", Data_Mapping,key="CMBACT3",default_label=st.session_state.get("CMBACT3", ""),
                    )
                    CmbAct4_label, CmbAct4_code = mapped_selectbox(
                        "Activation 4", "CMBACT4", Data_Mapping,key="CMBACT4",default_label=st.session_state.get("CMBACT4", ""),
                    )
                    CmbFloorLoopInstall_label, CmbFloorLoopInstall_code = mapped_selectbox(
                        "Floor Loop Installation", "CMBFLOORLOOPINSTALL", Data_Mapping,key="CMBFLOORLOOPINSTALL",default_label=st.session_state.get("CMBFLOORLOOPINSTALL", ""),
                    )
                
    door_input_data = {
                    "NUMDOORHEIGHT": NUMDOORHEIGHT,
                    "NUMDOORWIDTH": NUMDOORWIDTH,
                    "NUMCEILINGHEIGHT": NUMCEILINGHEIGHT,               
                    "CMBDOORMODEL": door_model_code,
                    "DoorSellPrice": door_sell_price,
                    "CMBMOTORORIDE": motor_oride_code,
                    "CMBTRACKCONFIG": track_config_code,
                    "CMBWINDTRACK": wind_track_code,
                    "CMBCONTROLLERENCLOSURE": controller_enclosure_code,
                    "CMBMOTORSHROUD": motor_shroud_code,
                    "CMBMOTORSPEC": motor_spec_code,             
                    "CMBBRUSHSEAL": brushseal_code,
                    "CMBGPOISO": cmbGPOISO_code,
                    "CMBPOWERSUPPLY": cmbPowerSupply_code,
                    "CMBTRAFFICLIGHT": traffic_light_code,
                    "CMBPEBEAMS": PE_Beam_code,
                    "CHKHYPERLIFT": CHKHYPERLIFT,
                    "CHKINTERLOCK": CHKINTERLOCK,
                    "CHKSTAINLESS": CHKSTAINLESS,
                    "CHKEX35FELT": CHKEX35FELT,
                    "CMBUPS": UPS_code,
                    "CMBCUSTSTEEL": custsteel_code,
                    "CMBREARHOODBRUSHSEAL": rearhoodbrushseal_code,
                    "CMBSPECIALCONDUIT": specialconduit_code,
                    "CMBCOLOURFINISHTYPE": colourfinishtype_code,
                    "CMBES40FASCIA": cmbES40Fascia_code,         
                    "CMBES40VSDMTR": cmbES40VSDMtr_CODE,         
                    "CMBHEATTRACELEG": cmbHeatTraceLeg_code,     
                    "CMBGEARBOXHEATER": cmbGearboxHeater_code,   
                    "CMBHEATTRACEHOOD": cmbHeatTraceHood_code,   
                    "CMBFELTSEAL": cmbFeltSeal_code,
                    "CMBPED1": CmbPed1_code,
                    "CMBPED2": CmbPed2_code,
                    "CMBRADAR1": CmbRadar1_code,
                    "CMBRADAR2": CmbRadar2_code,
                    "CMBACT1": CmbAct1_code,
                    "CMBACT2": CmbAct2_code,
                    "CMBACT3": CmbAct3_code,
                    "CMBACT4": CmbAct4_code,
                    "CMBFLOORLOOPINSTALL": CmbFloorLoopInstall_code,
                    "QTY": QTY
                }
    export_data = {
                    "CMBDOORMODEL": door_model_label,
                    "NUMDOORHEIGHT": NUMDOORHEIGHT,
                    "NUMDOORWIDTH": NUMDOORWIDTH,
                    "NUMCEILINGHEIGHT": NUMCEILINGHEIGHT,
                    "CMBGPOISO": cmbGPOISO_label,
                    "CMBMOTORORIDE": motor_oride_label,
                    "CMBTRACKCONFIG": track_config_label,
                    "CMBWINDTRACK": wind_track_label,
                    "CMBPOWERSUPPLY": cmbPowerSupply_label,
                    "CMBCONTROLLERENCLOSURE": controller_enclosure_label,
                    "CMBMOTORSHROUD": motor_shroud_label,
                    "CMBMOTORSPEC": motor_spec_label,
                    "CMBBRUSHSEAL": brushseal_label,
                    "CMBTRAFFICLIGHT": traffic_light_label,
                    "CMBPEBEAMS": pe_beam_label,
                    "CMBUPS": UPS_label,
                    "CMBCUSTSTEEL": custsteel_label,
                    "CMBREARHOODBRUSHSEAL": rearhoodbrushseal_label,
                    "CMBSPECIALCONDUIT": specialconduit_label,
                    "CMBCOLOURFINISHTYPE": colourfinishtype_label,
                    "CHKHYPERLIFT": CHKHYPERLIFT,
                    "CHKINTERLOCK": CHKINTERLOCK,
                    "CHKSTAINLESS": CHKSTAINLESS,
                    "CHKEX35FELT": CHKEX35FELT,
                    "CMBES40FASCIA": cmbES40Fascia_label,
                    "CMBES40VSDMTR": cmbES40VSDMtr_LABEL,
                    "CMBHEATTRACELEG": cmbHeatTraceLeg_label,
                    "CMBGEARBOXHEATER": cmbGearboxHeater_label,
                    "CMBHEATTRACEHOOD": cmbHeatTraceHood_label,
                    "CMBFELTSEAL": cmbFeltSeal_label,
                    "CMBPED1": CmbPed1_label,
                    "CMBPED2": CmbPed2_label,
                    "CMBRADAR1": CmbRadar1_label,
                    "CMBRADAR2": CmbRadar2_label,
                    "CMBACT1": CmbAct1_label,
                    "CMBACT2": CmbAct2_label,
                    "CMBACT3": CmbAct3_label,
                    "CMBACT4": CmbAct4_label,
                    "CMBFLOORLOOPINSTALL": CmbFloorLoopInstall_label
                }

    door_df = pd.DataFrame([door_input_data])

    return {
            "door_input_data": door_input_data,
            "door_df": door_df,
            "export_data": export_data,
            "door_model_label": door_model_label,
            "door_model_code": door_model_code,
            "door_sell_price": door_sell_price,
            "NUMDOORHEIGHT": NUMDOORHEIGHT,
            "NUMDOORWIDTH": NUMDOORWIDTH,
        }