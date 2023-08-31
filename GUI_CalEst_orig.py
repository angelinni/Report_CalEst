#
#GUI_CalEst
import streamlit as st
import datetime
from PIL import Image
import os
import glob, os.path
import plot_CalEst
from datetime import date, datetime, timedelta

st.set_page_config(
    page_title="Reporte CalEst - SGC",
    menu_items={"About": """*Reporte CalEst* es un Aplicativo desarrollado por A. Agudelo y Miguel Lizarazo
     para generar un unforme en pdf con la información de calidad de cada estación en tiempo real de la RSNC, 
     analizando por estación datos de disponibilidad, gaps, overlaps, offset, picos, ppsd.
      **si encuentra un error escribir al correo adagudelo@sgc.gov.co**""",},
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_image(image_file):
    img = Image.open(image_file)
    return img

def main():

    st.title("""Reporte Calidad Estacion""")
    st.write("_______________________________________________")

    ##Parametros generales
    image = Image.open('images/Simbolo_SGC_Blanco.png')
    st.sidebar.image(image)
    folder = os.path.dirname(os.path.abspath(__file__))+'/informes_estaciones'
    
    #Selección de Estacion
    all_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/*")
    estaciones = []
    for est in all_est:
        nom_est = est.split("/")[6].split("_")[0]
        if nom_est not in estaciones:
            estaciones.append(nom_est)
        
    #estaciones = ["DBB","CRU"]
    option = st.sidebar.selectbox('Seleccione la estación',sorted(estaciones) ,key ="est")

    list_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/{option}*")
    #print(option, list_est)
    sensores = []
    for e in list_est:
        if e[-14:-12] not in sensores:
            sensores.append(e[-14:-12])

    option_sen = st.sidebar.selectbox('Seleccione el canal',sensores ,key ="can")

    #st.session_state.IDev
    st.sidebar.markdown(".")

    #fecha_ini = st.sidebar.date_input("Fecha Inicial", datetime.datetime(2019, 7, 6))
    #fecha_fin = st.sidebar.date_input("Fecha Final", datetime.date(2019, 7, 6))

    col1, col2 = st.sidebar.columns([1,1])
    with col1:
        fecha_ini1 = st.date_input("Fecha Inicial", None, key="f_ini")
        fecha_ini = datetime(fecha_ini1.year, fecha_ini1.month,fecha_ini1.day)
    with col2:
        fecha_fin1 = st.date_input("Fecha Final", None, key="f_fin")
        fecha_fin = datetime(fecha_fin1.year, fecha_fin1.month,fecha_fin1.day)

    
    #Graficar datos
    if st.sidebar.button("Graficar"):

        est = "Dabeiba"
        st.title(f"Estación {est} - {option}")

        st.write(option,fecha_ini,fecha_fin)


    plt_inf = plot_CalEst.Plot(option,option_sen,fecha_ini,fecha_fin, folder) 
    plt_inf.graf_est()

    if st.sidebar.button("Guardar y Crear Informe"):
        n_foler = folder+"/"+option
        os.mkdir(n_folder)


main()