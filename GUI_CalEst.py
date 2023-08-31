#
#GUI_CalEst
import streamlit as st  
import datetime
from PIL import Image
import os
import glob, os.path
import plot_CalEst
from datetime import date, datetime, timedelta
import json
import create_doc 
import plt_3d

st.set_page_config(
    page_title="Reporte CalEst - SGC",
    menu_items={"About": """*Reporte_CalEst (Reporte de funcionamiento y calidad de estaciones)* es una aplicación desarrollada por Angel Daniel Agudelo, 
                quien reunió aplicaciones de Miguel Lizarazo en la toma de datos de estaciones y Monica Acosta con SIIGEO.
                La app muestra consultas por fechas y genera informes semestrales y mensuales en pdf con la información de funcionamiento y calidad de cada estación en tiempo real, 
                mostrando por estación datos de disponibilidad, gaps, overlaps, offset, picos y ppsd. Además, 
                el sismólogo encargado puede ingresar sus observaciones del estado de cada estación.
      **si encuentra un error escribir al correo adagudelo@sgc.gov.co**""",},
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_image(image_file):
    img = Image.open(image_file)
    return img


def est1_fechas():
    
    
    
    #Selección de Estacion
    all_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/*")
    #print(all_est)
    estaciones = []
    for est in all_est:
        nom_est = est.split("/")[8].split("_")[0]
        if nom_est not in estaciones:
            estaciones.append(nom_est)
        
    #LISTA DE ESTACIONES
    col1, col2 = st.sidebar.columns([1,1])
    with col1:
        
        option = st.selectbox('**Estación**',sorted(estaciones) ,key ="est")

    with col2:
        list_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option}*")

        #SENSORES
        sensores = []
        
        for e in list_est:
            
            if option == "ROSC":
                sensores = ["BH","HN"]
            if option != "ROSC":   
                if e[-14:-12] not in sensores:
                    sensores.append(e[-14:-12])
                
                
        option_sen = st.selectbox('**Sensor**',sensores ,key ="can")
        
        list_est_sen = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option}_{option_sen}Z*")
        
        cod_sensor=[]
        option_cod_sen="."
        if len(list_est_sen) == 2:
            for s in list_est_sen:
                if s[-10:-8] not in cod_sensor:
                   cod_sensor.append(s[-10:-8]) 
            option_cod_sen = st.selectbox('**Codigo de Localicación**',cod_sensor ,key ="cod_can")

    st.sidebar.markdown(".")

    #SELECCION DE FECHAS
    mes_antes=datetime.now()-timedelta(days=31)
    ayer= datetime.now()-timedelta(days=1)
    col1, col2 = st.sidebar.columns([1,1])
    with col1:
        fecha_ini1 = st.date_input("**Fecha Inicial**", value=mes_antes,min_value=datetime(2018,1,1),max_value=ayer, key="f_ini")
        fecha_ini = datetime(fecha_ini1.year, fecha_ini1.month,fecha_ini1.day)
        
    with col2:
        fecha_fin1 = st.date_input("**Fecha Final**", value=ayer,min_value=datetime(2018,1,1),max_value=ayer, key="f_fin")
        fecha_fin = datetime(fecha_fin1.year, fecha_fin1.month,fecha_fin1.day)
        
    

    
    ##GRAFICAR DATOS
    #if st.sidebar.button("Graficar"):

    #    est = "Dabeiba"
    #    st.title(f"Estación {est} - {option}")

    #    st.write(option,fecha_ini,fecha_fin)
    
    #TITULO
    st.header("""Funcionamiento y calidad de señal  """)
    st.header(option+" _ "+option_sen+"."+option_cod_sen)
    
    #INFORMACIÓN GENERAL DE LA ESTACIÓN
    with st.expander("**Datos generales de la estación**"):
        
        plot_CalEst.get_data_est(option,False) 
        col1, col2 = st.columns([1,2])
        with col1:
            if st.button('Actualizar información',help="recargar y actualizar los datos con la información del SIIGEO"):
                plot_CalEst.actualizar_est_siigeo()   
                st.experimental_rerun()
        with col2:
            st.markdown("**Esta información es extraida del SIIGEO**")
       
    #BITACORA     
    with st.expander(f"**Registro de {option} en Bitacora**"):
            plot_CalEst.get_bitacora(option, fecha_ini, fecha_fin)

            col1, col2 = st.columns([3,0.8])
            with col2:

                
                if st.button('Actualizar Bitacora',help="recargar y actualizar los datos con la información del SIIGEO"):
                    plot_CalEst.actualizar_bitacora_siigeo()   
                    st.experimental_rerun()
            with col1:
                st.markdown("**Esta información es extraida del SIIGEO**")

    #ESTADO ACTUAL
    with st.expander("Estado Actual"):
        col1, col2 =st.columns(2)
        with col1:
            plot_CalEst.estado_a(option,option_sen)
        with col2:
            
            t_act=st.text_area("",key="t_act")
            if st.button("Actualizar estado", key="but_create"):
                plot_CalEst.actualizar_estado(option,option_sen,t_act) 
                st.experimental_rerun() 
                
            
    #TRES COMPONENTES
    tabz, tabn,tabe = st.tabs(["Z","N","E"])
    with tabz:
        com="Z"
        folder = os.path.dirname(os.path.abspath(__file__))+'/informes_estaciones'
        #folder = os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option}_{option_sen}/{optionf}/"
        if option_cod_sen == ".":
            list_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option}_{option_sen}{com}*")
        if len(option_cod_sen) > 1:
            list_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option}_{option_sen}{com}_{option_cod_sen}*")
          
        plt_inf = plot_CalEst.Plot(option,option_sen,fecha_ini,fecha_fin,list_est) 
        
        
        #tab1, tab2 = st.tabs(["Graficas Dinamicas","Graficas Fijas"])
        
        #with tab1: #graficas dinamicas
        #col1,col2= st.columns([5,1.1])
        #with col1:
        plt_inf.plot_disp_din(com)
        #with col2:
        
        #se guardarán en un formato json y los veré aquí""", key="obs1",height=250)
        #st.write(obs1)
        plt_inf.plot_off_din(com)
        
        #se guardarán en un formato json y los veré aquí""",key="obs2")
        plt_inf.plot_ppsd_din(com)
        
        #se guardarán en un formato json y los veré aquí""",key="obs3")
        
        ##GRAFICA MEDIA DEL ESPECTRO 
        st.write(".")
        st.write(f"**Media del PPSD de la estación {option} para el día seleccionado.**", help="PPSD:Espectro probabilístico de densidad de potencia")
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write(".")
            #fecha_ruido = st.slider("Fecha", fecha_ini,fecha_fin,key="sli_z")
            fecha_ruido = st.date_input("**Fecha:**", value=fecha_fin,min_value=fecha_ini,max_value=fecha_fin, key="f_ruidoz")
            mes=str(fecha_ruido.month).rjust(2,"0")
            dia=str(fecha_ruido.day).rjust(2,"0")
            fecha = f"{fecha_ruido.year}-{mes}-{dia}"
        with col2:
   
                plot_CalEst.plot_ruido(fecha,option,option_sen, com)
        with col3:
            st.write(".")

            
        #with tab2: ##graficas fijas
        #    plt_inf.plot_disp_fij(com)
        #    plt_inf.plot_off_fij(com)
        #    plt_inf.plot_ppsd_fij(com)
           
            
        
            
                
    with tabn:
        com="N"
        
        if option_cod_sen == ".":
            list_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option}_{option_sen}{com}*")
        if len(option_cod_sen) > 1:
            list_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option}_{option_sen}{com}_{option_cod_sen}*")
        
        if len(list_est) != 0:
            plt_inf = plot_CalEst.Plot(option,option_sen,fecha_ini,fecha_fin,list_est) 
            
            #tab1, tab2 = st.tabs(["Graficas Dinamicas","Graficas Fijas"])
            
            #with tab1: #graficas dinamicas
            plt_inf.plot_disp_din(com)
            plt_inf.plot_off_din(com)
            plt_inf.plot_ppsd_din(com)
            
             ##GRAFICA MEDIA DEL ESPECTRO 
            st.write(".")
            st.write(f"**Media del PPSD de la estación {option} para el día seleccionado.**", help="PPSD:Espectro probabilístico de densidad de potencia")
            col1, col2,col3 = st.columns(3)
            with col1:
                st.write(".")
                #fecha_ruido = st.slider("Fecha ppsd", fecha_ini,fecha_fin,key="sli_n")
                fecha_ruido = st.date_input("**Fecha:**", value=fecha_fin,min_value=fecha_ini,max_value=fecha_fin, key="f_ruidon")
                mes=str(fecha_ruido.month).rjust(2,"0")
                dia=str(fecha_ruido.day).rjust(2,"0")
                fecha = f"{fecha_ruido.year}-{mes}-{dia}"
            with col2:
    
                    plot_CalEst.plot_ruido(fecha,option,option_sen, com)
            with col3:
                st.write(".")
                
            #with tab2: ##graficas fijas
            #    plt_inf.plot_disp_fij(com)
            #    plt_inf.plot_off_fij(com)
            #    plt_inf.plot_ppsd_fij(com)
        else: 
            st.info(f"NO HAY DATOS PARA EL CANAL NORTE DE LA ESTACIÓN {option}")
    with tabe:  
        com="E"
        if option_cod_sen == ".":
            list_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option}_{option_sen}{com}*")
        if len(option_cod_sen) > 1:
            list_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option}_{option_sen}{com}_{option_cod_sen}*")
        
        if len(list_est) != 0:
            plt_inf = plot_CalEst.Plot(option,option_sen,fecha_ini,fecha_fin,list_est) 
            
            #tab1, tab2 = st.tabs(["Graficas Dinamicas","Graficas Fijas"])
            
            #with tab1: #graficas dinamicas
            plt_inf.plot_disp_din(com)
            plt_inf.plot_off_din(com)
            plt_inf.plot_ppsd_din(com)
            
             ##GRAFICA MEDIA DEL ESPECTRO 
            st.write(".")
            st.write(f"**Media del PPSD de la estación {option} para el día seleccionado.**", help="PPSD:Espectro probabilístico de densidad de potencia")
            col1, col2,col3 = st.columns(3)
            with col1:
                st.write(".")
                #fecha_ruido = st.slider("Fecha ppsd", fecha_ini,fecha_fin,key="sli_e")
                fecha_ruido = st.date_input("**Fecha:**", value=fecha_fin,min_value=fecha_ini,max_value=fecha_fin, key="f_ruidoe")
                mes=str(fecha_ruido.month).rjust(2,"0")
                dia=str(fecha_ruido.day).rjust(2,"0")
                fecha = f"{fecha_ruido.year}-{mes}-{dia}"
            with col2:
    
                    plot_CalEst.plot_ruido(fecha,option,option_sen, com)
            with col3:
                st.write(".")

        else: 
            st.info(f"NO HAY DATOS PARA EL CANAL ESTE DE LA ESTACIÓN {option}")

            
def est1_informe_s():

    #Parametros de entrada

    folder_inf= os.path.dirname(os.path.abspath(__file__))+'/Inf_semestrales/'
    #Seleccion de Estacion
    all_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/*")
    estaciones = []
    for est in all_est:
        nom_est = est.split("/")[8].split("_")[0]
        if nom_est not in estaciones:
            estaciones.append(nom_est)
        
    #LISTA DE ESTACIONES
    col1, col2 = st.sidebar.columns([1,1])
    with col1:
        
        option_est = st.selectbox('**Estación**',sorted(estaciones) ,key ="est")

    with col2:
        list_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option_est}*")

        #SENSORES
        sensores = []
        for e in list_est:
            if option_est == "ROSC":
                sensores = ["BH","HN"]
            if option_est != "ROSC":   
                if e[-14:-12] not in sensores:
                    sensores.append(e[-14:-12])
                
        option_sen = st.selectbox('**Sensor**',sensores ,key ="can")
        
        list_est_sen = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option_est}_{option_sen}Z*")
        cod_sensor=[]
        option_cod_sen="."
        if len(list_est_sen) == 2:
            for s in list_est_sen:
                if s[-10:-8] not in cod_sensor:
                   cod_sensor.append(s[-10:-8]) 
            option_cod_sen = st.selectbox('**Codigo de Localicación**',cod_sensor ,key ="cod_can")
         
        

    

    st.sidebar.markdown(".")

    #SELECCION DE FECHAS

    semestre = ["2023-I","2022-II"]
    option_s = st.sidebar.selectbox('**Semestre**',semestre,key ="semestre")

    op_s= option_s.split("-")

    if op_s[1] == "I":

        fecha_ini=datetime(int(op_s[0]),1,1)
        fecha_fin=datetime(int(op_s[0]),6,30)

    if op_s[1] == "II":

        fecha_ini=datetime(int(op_s[0]),7,1)
        fecha_fin=datetime(int(op_s[0]),12,31)

    for all_sen in sensores:
        #crear Informe inicial de todos los sensores de la estación
        plot_CalEst.create_info_s(option_est,all_sen,fecha_ini, fecha_fin,folder_inf,option_s)
    
    
    


    #TITULO
    st.header(f"""Informe semestral de Funcionamiento y calidad de señal | {option_s}""")
    st.header(option_est+" _ "+option_sen+"."+option_cod_sen)

    #INFORMACIÓN GENERAL DE LA ESTACIÓN
    with st.expander("**Datos generales de la estación**"):
        
        plot_CalEst.get_data_est(option_est,False) 
        col1, col2 = st.columns([1,2])
        with col1:
            if st.button('Actualizar información',help="recargar y actualizar los datos con la información del SIIGEO"):
                plot_CalEst.actualizar_est_siigeo()   
                st.experimental_rerun()
        with col2:
            st.markdown("**Esta información es extraida del SIIGEO**")
    
    #BITACORA
    with st.expander(f"**Registro de {option_est} en Bitacora**"):
            plot_CalEst.get_bitacora(option_est,fecha_ini, fecha_fin)

            col1, col2 = st.columns([3,0.8])
            with col2:
        
                if st.button('Actualizar Bitacora',help="recargar y actualizar los datos con la información del SIIGEO"):
                    plot_CalEst.actualizar_bitacora_siigeo()   
                    st.experimental_rerun()
            with col1:
                st.markdown("**Esta información es extraida del SIIGEO**")
    

    #Secciones del Informe
    tab_fun, tab_cal,tab_ul, tab_rec = st.tabs(["Funcionamiento","Calidad","Última visita","Recomendaciones"])

    
    ###################################################################################################################
    #componentes
    z,n,e="Z","N","E"

    if option_cod_sen == ".":
        
        file_z = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option_est}_{option_sen}{z}*")
        plt_inf_z = plot_CalEst.Plot(option_est,option_sen,fecha_ini,fecha_fin,file_z) 


        file_n = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option_est}_{option_sen}{n}*")
        if len(file_n) != 0:
            plt_inf_n = plot_CalEst.Plot(option_est,option_sen,fecha_ini,fecha_fin,file_n) 

        file_e = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option_est}_{option_sen}{e}*")
        if len(file_e) != 0:
            plt_inf_e = plot_CalEst.Plot(option_est,option_sen,fecha_ini,fecha_fin,file_e)    
            
    if len(option_cod_sen) > 1:
        
        file_z = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option_est}_{option_sen}{z}_{option_cod_sen}*")
        plt_inf_z = plot_CalEst.Plot(option_est,option_sen,fecha_ini,fecha_fin,file_z) 


        file_n = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option_est}_{option_sen}{n}_{option_cod_sen}*")
        if len(file_n) != 0:
            plt_inf_n = plot_CalEst.Plot(option_est,option_sen,fecha_ini,fecha_fin,file_n) 

        file_e = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option_est}_{option_sen}{e}_{option_cod_sen}*")
        if len(file_e) != 0:
            plt_inf_e = plot_CalEst.Plot(option_est,option_sen,fecha_ini,fecha_fin,file_e)  
            
            
     

    

    #pestaña Funcionamiento
    with tab_fun:

        #Pestaña de Funcionamiento
        st.header("Disponibilidad")
        col1, col2 = st.columns([2,1])
        with col1:
            est_dinz= plt_inf_z.plot_disp_din(z)# contiene [min_dis,max_dis,prom_dis,codigo_l]
            est_dinn,est_dine=[],[]
            if len(file_n) != 0:
                est_dinn=plt_inf_n.plot_disp_din(n)
            if len(file_e) != 0:
                est_dine=plt_inf_e.plot_disp_din(e)
            est_din =[est_dinz,est_dinn,est_dine]
        with col2:

            #mostrar informaión guardada
            folder_semestre = os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option_est}_{option_sen}/{option_s}/"

            if option_cod_sen == ".": option_cod_sen=""
    
            with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                inf_json = json.load(file)
                    

            
            text_fun= inf_json[0]["funcionamiento"]
            text_dis= inf_json[0]["disponibilidad"]
            text_gap= inf_json[0]["gapover"]

            st.write(".")
            st.write("**Funcionamiento general**")
            st.write(text_fun)
                
            t_fun=st.text_area("",key="t_fun")
            
            st.write("_______________________")
            st.write("**Disponibilidad**")
            st.write(text_dis)
            t_dis=st.text_area("",key="t_dis")
            

        st.write("_______________")
        st.header("Gaps y Overlaps")
        col1, col2 = st.columns([2,1])
        with col1:
            est_gapoverz=plt_inf_z.plot_gapover_din(z) #continenen [num_gaps,max_gaps,gaps_prom,num_overlaps,max_overlap,overlaps_prom, codigo_l]
            est_gapovern, est_gapovere=[],[]
            if len(file_n) != 0:
                est_gapovern=plt_inf_n.plot_gapover_din(n)
            if len(file_e) != 0:
                est_gapovere=plt_inf_e.plot_gapover_din(e)
            est_gapover=[est_gapoverz,est_gapovern,est_gapovere]

        with col2:
            #leer datos de json
            st.write("**Gaps y Overlaps**")
            st.write(text_gap)

            #pedir datos para json
            t_gap=st.text_area("",key="t_gaps")


            #Guardar datos en json
            if st.button("Guardar", help="Ingrese los comentarios y luego de Guardar, al volver a guardar se reemplazarán siempre los comentarios",key="but_fun"):

                folder_semestre = os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option_est}_{option_sen}/{option_s}/"
                
                if option_cod_sen == ".": option_cod_sen=""
                
                
                if os.path.exists(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json") == True:
                    with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                        inf_json = json.load(file)
                    
                    if len(t_fun) != 0:
                        inf_json[0]["funcionamiento"] = t_fun
                    if len(t_dis) != 0:
                        inf_json[0]["disponibilidad"] = t_dis
                    if len(t_gap) != 0:
                        inf_json[0]["gapover"] = t_gap

                    with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'w') as (file):
                        json.dump(inf_json, file, indent=4)
                st.experimental_rerun()





        #inf_funcionamiento(option,option_sen,fecha_ini, fecha_fin)

    #pestaña Calidad
    with tab_cal:
        #Pestaña de Calidad
        st.header("Offset")
        col1, col2 = st.columns([2,1])
        with col1:

            est_offz=plt_inf_z.plot_off2_din(z) #contienen [min_offset,max_offset,offset_prom, codigo_l]
            est_offn,est_offe=[],[]
            if len(file_n) != 0:
                est_offn=plt_inf_n.plot_off2_din(n)
            if len(file_e) != 0:
                est_offe=plt_inf_e.plot_off2_din(e)
            est_off=[est_offz,est_offn,est_offe]
        with col2:

            #t_gap=st.text_area("",key="t_gaps")
            folder_semestre = os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option_est}_{option_sen}/{option_s}/"
            
            if option_cod_sen == ".": option_cod_sen=""

            with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                inf_json = json.load(file)
            
            text_cal= inf_json[0]["calidad"]
            text_offs= inf_json[0]["offset"]
            text_ruido= inf_json[0]["ruido"]

            st.write(".")
            st.write("**Calidad general**")
            st.write(text_cal)
                
            t_cal=st.text_area("",key="t_cal")
            
            st.write("_______________________")
            st.write("**Offset**")
            st.write(text_offs)
            t_offs=st.text_area("",key="t_offs")
            
            
        
            

        st.write("_______________")
        st.header("Analisis de ruido")
        
        st.header("%PPSD")

        co1, co2 = st.columns([2,1])
        with co1:
            est_ppsd_picz=plt_inf_z.plot_ppsd_din(z)#tomando [ppsd_prom,num_picos,max_picos, codigo_l]
            est_ppsd_picn,est_ppsd_pice=[],[]
            if len(file_n) != 0:
                est_ppsd_picn=plt_inf_n.plot_ppsd_din(n)
            if len(file_e) != 0:
                est_ppsd_pice=plt_inf_e.plot_ppsd_din(e)
            est_ppsd_pic=[est_ppsd_picz,est_ppsd_picn,est_ppsd_pice]
        with co2:

            ##GRAFICA MEDIA DEL ESPECTRO 
        
            st.write(f"**Media del PPSD de la estación {option_est} para el día seleccionado.**", help="PPSD:Espectro probabilístico de densidad de potencia")
            #c1, c2,c3 = st.columns(3)
            #with c1:
                
            
            #fecha_ruido = st.slider("Fecha ppsd", fecha_ini,fecha_fin,key="sli_e")
            #colu1,colu2 = st.columns(2)
            #with colu1:
            if len(file_n) != 0 and len(file_e) != 0:
                com = st.selectbox("Canal",("Z","N","E"))
            else:
                com = st.selectbox("Canal",("Z"))
            #with colu2:
            fecha_ruido = st.date_input("**Fecha:**", value=fecha_fin,min_value=fecha_ini,max_value=fecha_fin, key="f_ruidoe")
            mes=str(fecha_ruido.month).rjust(2,"0")
            dia=str(fecha_ruido.day).rjust(2,"0")
            fecha = f"{fecha_ruido.year}-{mes}-{dia}"
                
            #with c2:
            plot_CalEst.plot_ruido(fecha,option_est,option_sen, com)
            #with c3:
            st.write(".")
                
            
            
        st.header("Espectro de ruido")
        col1, col2 = st.columns([2,1])
        with col1:
            image_ruido=st.file_uploader("**Suba la imagen del espectro de ruido**", type =["png", "jpg","jpeg"], key ="image_ruido",accept_multiple_files=True)
            
            #if image_ruido is not None:    
            
            img_ruido = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option_est}_{option_sen}/{option_s}/img_ruido{option_cod_sen}_*")
            for image_file in img_ruido:
                #file_details_damage = {"filename":image_file.name,"filetype":image_file.type,
                #                "filesize":image_file.size}
                #st.write(file_details_damage)
                st.image(load_image(image_file), width=500)
            

        with col2:
            st.write("**Analisis de ruido**")
            st.write(text_ruido)
            t_ruido=st.text_area("",key="t_ruido")

            #Guardar datos en json
            if st.button("Guardar", help="Ingrese los comentarios y luego de Guardar, al volver a guardar se reemplazarán siempre los comentarios", key="but_cal"):

                folder_semestre = os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option_est}_{option_sen}/{option_s}/"
                if option_cod_sen == ".": option_cod_sen=""
                if os.path.exists(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json") == True:
                    with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                        inf_json_cal = json.load(file)
                    
                    if len(t_cal) != 0:
                        inf_json_cal[0]["calidad"] = t_cal
                    if len(t_offs) != 0:
                        inf_json_cal[0]["offset"] = t_offs
                    if len(t_ruido) != 0:
                        inf_json_cal[0]["ruido"] = t_ruido

                    with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'w') as (file):
                        json.dump(inf_json_cal, file, indent=4)
                
                #Guardar imagenes
                if len(image_ruido) >0:
                    c=1
                    for image_file in image_ruido:
                        file_details_damage = {"filename":image_file.name,"filetype":image_file.type,
                                        "filesize":image_file.size}
                        if option_cod_sen == ".": option_cod_sen=""
                        if os.path.exists(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json") == True:
                            with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                                inf_json_cal = json.load(file)
                                
                            inf_json_cal[0]["n_img_ruido"] += 1

                            with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'w') as (file):
                                json.dump(inf_json_cal, file, indent=4)

                        #Saving upload
                        with open(folder_semestre+f'img_ruido{option_cod_sen}_{inf_json_cal[0]["n_img_ruido"]}.'+str(image_file.type).split("/")[1],"wb") as f:
                            f.write((image_file).getbuffer())
                        c+=1
                if len(image_ruido) ==0:
                    if option_cod_sen == ".": option_cod_sen=""
                    os.system(f"rm {os.path.dirname(os.path.abspath(__file__))}/Inf_semestrales/{option_est}_{option_sen}/{option_s}/img_ruido{option_cod_sen}_*")
                    if os.path.exists(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json") == True:
                        with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                            inf_json_cal = json.load(file)
                                
                            inf_json_cal[0]["n_img_ruido"] = 0

                        with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'w') as (file):
                            json.dump(inf_json_cal, file, indent=4)
                            
                        
                st.experimental_rerun()


    #Ultima visita
    with tab_ul:
        
        st.header("Última visita")
        st.write(".")

        
        

        #get ultima visita
        folder_semestre = os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option_est}_{option_sen}/{option_s}/"
        if option_cod_sen == ".": option_cod_sen=""
            
        with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
            inf_json = json.load(file)
        
        text_fecha= inf_json[0]["ultima_v"][0]
        text_man= inf_json[0]["ultima_v"][1]
        text_com= inf_json[0]["ultima_v"][2]
        text_vis= inf_json[0]["ultima_v"][3]

        if len(text_man) == 0 or len(text_com) == 0 or len(text_vis) == 0:
            plot_CalEst.get_ultima_v(option_est,option_sen, folder_semestre,option_cod_sen)
            with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                inf_json = json.load(file)
        
            text_fecha= inf_json[0]["ultima_v"][0]
            text_man= inf_json[0]["ultima_v"][1]
            text_com= inf_json[0]["ultima_v"][2]
            text_vis= inf_json[0]["ultima_v"][3]

        st.write(f"**Fecha de Mantenimiento:** {text_fecha}")
        st.write(f"**Tipo de Mantenimiento:** {text_man}")
        st.write(f"**Comentarios:** {text_com}")
        st.write(f"**Visitada por:** {text_vis}")
        st.write("__________")

            


        
        #if st.button("Actualizar ultima visita", key="act_ult_v"):
        #    plot_CalEst.actualizar_ultima_v()
        #    plot_CalEst.get_ultima_v(option_est,option_sen, option_s,option_cod_sen)
        #    st.experimental_rerun()


                
            
    #Recomendaciones
    with tab_rec:


        st.header("Recomendaciones")
        
        #Guardar y mostrar recomendaciones
        folder_semestre = os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option_est}_{option_sen}/{option_s}/"
        if option_cod_sen == ".": option_cod_sen=""
        with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
            inf_json = json.load(file)
        
        text_recom= inf_json[0]["recomendaciones"]
        
        st.write(text_recom)

        recomendaciones = st.text_area('')

        #guardar y mostrar imagenes
        image_recom=st.file_uploader("**Suba una imagen**", type =["png", "jpg","jpeg"],accept_multiple_files=True,key="image_recom")

        
        

        #Guardar
        if st.button("Guardar", help="Ingrese los comentarios y luego de Guardar, al volver a guardar se reemplazarán siempre los comentarios", key="but_recom"):

            hoy = datetime.now()
            fecha_hoy= f"{hoy.year}-{hoy.month}-{hoy.day}"

            folder_semestre = os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option_est}_{option_sen}/{option_s}/"
            if option_cod_sen == ".": option_cod_sen=""
            
            if os.path.exists(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json") == True:
                with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                    inf_json_recom = json.load(file)
                
                if len(recomendaciones) != 0:
                    inf_json_recom[0]["recomendaciones"] = recomendaciones
                inf_json_recom[0]["fecha_creacion"] = fecha_hoy

                with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'w') as (file):
                        json.dump(inf_json_recom, file, indent=4)
            #Guardar imagenes
            if len(image_recom) >0:
                c=1
                for image_file in image_recom:
                    file_details_damage = {"filename":image_file.name,"filetype":image_file.type,
                                    "filesize":image_file.size}
                    #st.write(file_details_damage)
                    #st.image(load_image(image_file), width=250)

                    #Saving uploadif os.path.exists(folder_semestre + f"inf_{option_est}_{option_sen}.json") == True:
                    if option_cod_sen == ".": option_cod_sen=""
                    
                    with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                        inf_json_recom = json.load(file)
                        
                    inf_json_recom[0]["n_img_recom"] += 1

                    with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'w') as (file):
                        json.dump(inf_json_recom, file, indent=4)
                    
                    
                    with open(folder_semestre+f'img_recom{option_cod_sen}_{inf_json_recom[0]["n_img_recom"]}.'+str(image_file.type).split("/")[1],"wb") as f:
                        f.write((image_file).getbuffer())
                    c+=1
                    
            if len(image_recom) ==0:
                os.system(f"rm {os.path.dirname(os.path.abspath(__file__))}/Inf_semestrales/{option_est}_{option_sen}/{option_s}/img_recom{option_cod_sen}_*")
                
                if option_cod_sen == ".": option_cod_sen=""
                if os.path.exists(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json") == True:
                    with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                        inf_json_recom = json.load(file)
                            
                        inf_json_recom[0]["n_img_recom"] = 0

                    with open(folder_semestre + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'w') as (file):
                        json.dump(inf_json_recom, file, indent=4)

                            

            st.experimental_rerun()
        
        #Mostrar imagenes cargadas
        #if image_recom is not None:
            
            
        img_recom = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option_est}_{option_sen}/{option_s}/img_recom{option_cod_sen}_*")
        for image_file in img_recom:
            #file_details_damage = {"filename":image_file.name,"filetype":image_file.type,
            #                "filesize":image_file.size}
            #st.write(file_details_damage)
            st.image(load_image(image_file), width=500)

    cod_l = est_din[0][3] #[min_dis,max_dis,prom_dis,codigo_l]
    st.sidebar.write("_______")
    col1, col2 = st.sidebar.columns([1,1])
    with col1:
        if est_din[0][0] == 0 and est_din[0][1] == 0 and est_din[0][2] == 0:
            st.write(".")
        else:
            if st.button("Crear Documento", key="but_create"):
                
                if option_cod_sen == ".": option_cod_sen=""
                
                #for all_sen in sensores:
                #    plot_CalEst.actualizar_info_s(option_est,all_sen,fecha_ini, fecha_fin,folder_inf,option_s)
                    
                create_doc.mk_doc(option_est,option_sen,cod_l,option_s,est_din,est_gapover,est_off,est_ppsd_pic,cod_sen=option_cod_sen)
                #descargar
                folder_semestre = os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option_est}_{option_sen}/{option_s}/"
    with col2:
        if os.path.exists(folder_semestre+f'{option_est}_{cod_l}_{option_s}_informe.docx') == True:
            with open(folder_semestre+f'{option_est}_{cod_l}_{option_s}_informe.docx', "rb") as file:
                btn = st.download_button(label="Descargar Docx", data=file, file_name=f'{option_est}_{cod_l}_{option_s}_informe.docx', mime="application/octet-stream")
    
    #if st.button("G", key="but_gr"):

    #    all_est2 = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/*")
    #    estaciones2 = []
    #    for est2 in all_est2:
    #        nom_est2 = est2.split("/")[8].split("_")[0]
    #        if nom_est2 not in estaciones2:
    #            estaciones2.append(nom_est2)
            
        #LISTA DE ESTACIONES
    #    for e2 in estaciones2:
    #        list_est2 = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{e2}*")

            #SENSORES
    #        sensores2 = []
    #        for e in list_est2:
    #            if e[-14:-12] not in sensores2:
    #                sensores2.append(e[-14:-12])
                    
    #        for all_sen in sensores2:
    #            plot_CalEst.actualizar_info_s(e2,all_sen,fecha_ini, fecha_fin,folder_inf,option_s)
    #            print(e2,all_sen)

def est1_informe_m():
    
    #Parametros de entrada

    folder_inf= os.path.dirname(os.path.abspath(__file__))+'/Inf_mensuales/'
    #Seleccion de Estacion
    all_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/*")
    estaciones = []
    for est in all_est:
        nom_est = est.split("/")[8].split("_")[0]
        if nom_est not in estaciones:
            estaciones.append(nom_est)
        
    #LISTA DE ESTACIONES
    col1, col2 = st.sidebar.columns([1,1])
    with col1:
        
        option_est = st.selectbox('**Estación**',sorted(estaciones) ,key ="est")

    with col2:
        list_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option_est}*")

        #SENSORES
        sensores = []
        for e in list_est:
            if option_est == "ROSC":
                sensores = ["BH","HN"]
            if option_est != "ROSC":   
                if e[-14:-12] not in sensores:
                    sensores.append(e[-14:-12])
      
                
        option_sen = st.selectbox('**Sensor**',sensores ,key ="can")
        
        list_est_sen = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option_est}_{option_sen}Z*")
        cod_sensor=[]
        option_cod_sen="."
        if len(list_est_sen) == 2:
            for s in list_est_sen:
                if s[-10:-8] not in cod_sensor:
                   cod_sensor.append(s[-10:-8]) 
            option_cod_sen = st.selectbox('**Codigo de Localicación**',cod_sensor ,key ="cod_can")   

    st.sidebar.markdown(".")
    
    #SELECCION DE FECHAS
    year =["2023","2022"]
    month = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
    col1, col2 = st.sidebar.columns([1,1])
    with col1:
        option_year = st.selectbox('**Año**',year,key ="year")
    with col2:
        option_month = st.selectbox('**Mes**',month,key ="month")

    bisiesto = int(option_year) % 4 == 0 and (int(option_year) % 100 != 0 or int(option_year) % 400 == 0)
    ul_dia_feb= 29 if bisiesto == True else 28    
    meses_f={}
    for e in range(len(month)):
        if e in [0,2,4,6,7,9,11]:
            meses_f[month[e]]=[datetime(int(option_year),e+1,1),datetime(int(option_year),e+1,31)]
        if e in [3,5,8,10]:
            meses_f[month[e]]=[datetime(int(option_year),e+1,1),datetime(int(option_year),e+1,30)]
        if e == 1:
            meses_f[month[e]]=[datetime(int(option_year),e+1,1),datetime(int(option_year),e+1,ul_dia_feb)]

    fecha_ini=meses_f[option_month][0]
    fecha_fin=meses_f[option_month][1]

    for all_sen in sensores:
        #crear Informe inicial de todos los sensores de la estació
        plot_CalEst.create_info_m(option_est,all_sen,fecha_ini, fecha_fin,folder_inf)
        
    
        
    #TITULO
    st.header(f"""Informe mensual de Funcionamiento y calidad de señal | {option_month}-{option_year}""")
    st.header(option_est+" _ "+option_sen+"."+option_cod_sen)

    #INFORMACIÓN GENERAL DE LA ESTACIÓN
    with st.expander("**Datos generales de la estación**"):
        
        plot_CalEst.get_data_est(option_est,False) 
        col1, col2 = st.columns([1,2])
        with col1:
            if st.button('Actualizar información',help="recargar y actualizar los datos con la información del SIIGEO"):
                plot_CalEst.actualizar_est_siigeo()   
                st.experimental_rerun()
        with col2:
            st.markdown("**Esta información es extraida del SIIGEO**")
    
    #BITACORA
    with st.expander(f"**Registro de {option_est} en Bitacora**"):
            plot_CalEst.get_bitacora(option_est,fecha_ini, fecha_fin)

            col1, col2 = st.columns([3,0.8])
            with col2:
        
                if st.button('Actualizar Bitacora',help="recargar y actualizar los datos con la información del SIIGEO"):
                    plot_CalEst.actualizar_bitacora_siigeo()   
                    st.experimental_rerun()
            with col1:
                st.markdown("**Esta información es extraida del SIIGEO**")
    

    #Secciones del Informe
    tab_fun, tab_cal,tab_ul, tab_rec = st.tabs(["Funcionamiento","Calidad","Última visita","Recomendaciones"])
    
    ###################################################################################################################
    #componentes
    z,n,e="Z","N","E"

    if option_cod_sen == ".":
        
        file_z = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option_est}_{option_sen}{z}*")
        plt_inf_z = plot_CalEst.Plot(option_est,option_sen,fecha_ini,fecha_fin,file_z) 


        file_n = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option_est}_{option_sen}{n}*")
        if len(file_n) != 0:
            plt_inf_n = plot_CalEst.Plot(option_est,option_sen,fecha_ini,fecha_fin,file_n) 

        file_e = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option_est}_{option_sen}{e}*")
        if len(file_e) != 0:
            plt_inf_e = plot_CalEst.Plot(option_est,option_sen,fecha_ini,fecha_fin,file_e)    
            
    if len(option_cod_sen) > 1:
        
        file_z = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option_est}_{option_sen}{z}_{option_cod_sen}*")
        plt_inf_z = plot_CalEst.Plot(option_est,option_sen,fecha_ini,fecha_fin,file_z) 


        file_n = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option_est}_{option_sen}{n}_{option_cod_sen}*")
        if len(file_n) != 0:
            plt_inf_n = plot_CalEst.Plot(option_est,option_sen,fecha_ini,fecha_fin,file_n) 

        file_e = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{option_est}_{option_sen}{e}_{option_cod_sen}*")
        if len(file_e) != 0:
            plt_inf_e = plot_CalEst.Plot(option_est,option_sen,fecha_ini,fecha_fin,file_e)  
            
            
     

    

    #pestaña Funcionamiento
    with tab_fun:

        #Pestaña de Funcionamiento
        st.header("Disponibilidad")
        col1, col2 = st.columns([2,1])
        with col1:
            est_dinz= plt_inf_z.plot_disp_din(z)# contiene [min_dis,max_dis,prom_dis,codigo_l]
            est_dinn,est_dine=[],[]
            if len(file_n) != 0:
                est_dinn=plt_inf_n.plot_disp_din(n)
            if len(file_e) != 0:
                est_dine=plt_inf_e.plot_disp_din(e)
            est_din =[est_dinz,est_dinn,est_dine]
        with col2:

            #mostrar informaión guardada
            #   folder_semestre = os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option_est}_{option_sen}/{option_month}/"
            folder_mes = os.path.dirname(os.path.abspath(__file__))+f"/Inf_mensuales/{option_est}_{option_sen}/{option_year}/{option_month}/"

            if option_cod_sen == ".": option_cod_sen=""
                
            with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                inf_json = json.load(file)
                    

            
            text_fun= inf_json[0]["funcionamiento"]
            text_dis= inf_json[0]["disponibilidad"]
            text_gap= inf_json[0]["gapover"]

            st.write(".")
            st.write("**Funcionamiento general**")
            st.write(text_fun)
                
            t_fun=st.text_area("",key="t_fun")
            
            st.write("_______________________")
            st.write("**Disponibilidad**")
            st.write(text_dis)
            t_dis=st.text_area("",key="t_dis")
            

        st.write("_______________")
        st.header("Gaps y Overlaps")
        col1, col2 = st.columns([2,1])
        with col1:
            est_gapoverz=plt_inf_z.plot_gapover_din(z) #continenen [num_gaps,max_gaps,gaps_prom,num_overlaps,max_overlap,overlaps_prom, codigo_l]
            est_gapovern, est_gapovere=[],[]
            if len(file_n) != 0:
                est_gapovern=plt_inf_n.plot_gapover_din(n)
            if len(file_e) != 0:
                est_gapovere=plt_inf_e.plot_gapover_din(e)
            est_gapover=[est_gapoverz,est_gapovern,est_gapovere]
        
        with col2:
            #leer datos de json
            st.write("**Gaps y Overlaps**")
            st.write(text_gap)

            #pedir datos para json
            t_gap=st.text_area("",key="t_gaps")


            #Guardar datos en json
            if st.button("Guardar", help="Ingrese los comentarios y luego de Guardar, al volver a guardar se reemplazarán siempre los comentarios",key="but_fun"):

                #folder_semestre = os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option_est}_{option_sen}/{option_s}/"
                folder_mes = os.path.dirname(os.path.abspath(__file__))+f"/Inf_mensuales/{option_est}_{option_sen}/{option_year}/{option_month}/"
                
                if option_cod_sen == ".": option_cod_sen=""
                
                
                if os.path.exists(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json") == True:
                    with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                        inf_json = json.load(file)
                    
                    if len(t_fun) != 0:
                        inf_json[0]["funcionamiento"] = t_fun
                    if len(t_dis) != 0:
                        inf_json[0]["disponibilidad"] = t_dis
                    if len(t_gap) != 0:
                        inf_json[0]["gapover"] = t_gap

                    with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'w') as (file):
                        json.dump(inf_json, file, indent=4)
                st.experimental_rerun()





        #inf_funcionamiento(option,option_sen,fecha_ini, fecha_fin)
        
    with tab_cal:
        #Pestaña de Calidad
        st.header("Offset")
        col1, col2 = st.columns([2,1])
        with col1:

            est_offz=plt_inf_z.plot_off2_din(z) #contienen [min_offset,max_offset,offset_prom, codigo_l]
            est_offn,est_offe=[],[]
            if len(file_n) != 0:
                est_offn=plt_inf_n.plot_off2_din(n)
            if len(file_e) != 0:
                est_offe=plt_inf_e.plot_off2_din(e)
            est_off=[est_offz,est_offn,est_offe]
        with col2:
            #t_gap=st.text_area("",key="t_gaps")
            #folder_semestre = os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option_est}_{option_sen}/{option_s}/"
            folder_mes = os.path.dirname(os.path.abspath(__file__))+f"/Inf_mensuales/{option_est}_{option_sen}/{option_year}/{option_month}/"
            
            if option_cod_sen == ".": option_cod_sen=""

            with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                inf_json = json.load(file)
            
            text_cal= inf_json[0]["calidad"]
            text_offs= inf_json[0]["offset"]
            text_ruido= inf_json[0]["ruido"]

            st.write(".")
            st.write("**Calidad general**")
            st.write(text_cal)
                
            t_cal=st.text_area("",key="t_cal")
            
            st.write("_______________________")
            st.write("**Offset**")
            st.write(text_offs)
            t_offs=st.text_area("",key="t_offs")
        
        
        st.write("_______________")
        st.header("Analisis de ruido")
        
        st.header("%PPSD")

        co1, co2 = st.columns([2,1])
        
        with co1:

            est_ppsd_picz=plt_inf_z.plot_ppsd_din(z)#tomando [ppsd_prom,num_picos,max_picos, codigo_l]
            est_ppsd_picn,est_ppsd_pice=[],[]
            if len(file_n) != 0:
                est_ppsd_picn=plt_inf_n.plot_ppsd_din(n)
            if len(file_e) != 0:
                est_ppsd_pice=plt_inf_e.plot_ppsd_din(e)
            est_ppsd_pic=[est_ppsd_picz,est_ppsd_picn,est_ppsd_pice]
        
        with co2:

            ##GRAFICA MEDIA DEL ESPECTRO 
            
            st.write(f"**Media del PPSD de la estación {option_est} para el día seleccionado.**", help="PPSD:Espectro probabilístico de densidad de potencia")
            #col1, col2,col3 = st.columns(3)
            #with col1:
                
                
                #fecha_ruido = st.slider("Fecha ppsd", fecha_ini,fecha_fin,key="sli_e")
            co1,co2 = st.columns(2)
            #    with co1:
            if len(file_n) != 0 and len(file_e) != 0:
                com = st.selectbox("Canal",("Z","N","E"))
            else:
                com = st.selectbox("Canal",("Z"))
            #    with co2:
            fecha_ruido = st.date_input("**Fecha:**", value=fecha_fin,min_value=fecha_ini,max_value=fecha_fin, key="f_ruidoe")
            mes=str(fecha_ruido.month).rjust(2,"0")
            dia=str(fecha_ruido.day).rjust(2,"0")
            fecha = f"{fecha_ruido.year}-{mes}-{dia}"
                
            #with col2:
            plot_CalEst.plot_ruido(fecha,option_est,option_sen, com)
            #with col3:
            st.write(".")
            
        st.header("Espectro de ruido")
        col1, col2 = st.columns([2,1])
        with col1:
            image_ruido=st.file_uploader("**Suba la imagen del espectro de ruido**", type =["png", "jpg","jpeg"], key ="image_ruido",accept_multiple_files=True)
            
            #if image_ruido is not None:    
            #folder_mes = os.path.dirname(os.path.abspath(__file__))+f"/Inf_mensuales/{option_est}_{option_sen}/{option_year}/{option_month}/"
            img_ruido = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Inf_mensuales/{option_est}_{option_sen}/{option_year}/{option_month}/img_ruido{option_cod_sen}_*")
            for image_file in img_ruido:
                #file_details_damage = {"filename":image_file.name,"filetype":image_file.type,
                #                "filesize":image_file.size}
                #st.write(file_details_damage)
                st.image(load_image(image_file), width=500)
            

        with col2:
            st.write("**Analisis de ruido**")
            st.write(text_ruido)
            t_ruido=st.text_area("",key="t_ruido")

            #Guardar datos en json
            if st.button("Guardar", help="Ingrese los comentarios y luego de Guardar, al volver a guardar se reemplazarán siempre los comentarios", key="but_cal"):
                
                folder_mes = os.path.dirname(os.path.abspath(__file__))+f"/Inf_mensuales/{option_est}_{option_sen}/{option_year}/{option_month}/"
                #folder_semestre = os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option_est}_{option_sen}/{option_s}/"
                if option_cod_sen == ".": option_cod_sen=""
                if os.path.exists(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json") == True:
                    with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                        inf_json_cal = json.load(file)
                    
                    if len(t_cal) != 0:
                        inf_json_cal[0]["calidad"] = t_cal
                    if len(t_offs) != 0:
                        inf_json_cal[0]["offset"] = t_offs
                    if len(t_ruido) != 0:
                        inf_json_cal[0]["ruido"] = t_ruido

                    with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'w') as (file):
                        json.dump(inf_json_cal, file, indent=4)
                
                #Guardar imagenes
                if len(image_ruido) >0:
                    c=1
                    for image_file in image_ruido:
                        file_details_damage = {"filename":image_file.name,"filetype":image_file.type,
                                        "filesize":image_file.size}
                        if option_cod_sen == ".": option_cod_sen=""
                        if os.path.exists(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json") == True:
                            with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                                inf_json_cal = json.load(file)
                                
                            inf_json_cal[0]["n_img_ruido"] += 1

                            with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'w') as (file):
                                json.dump(inf_json_cal, file, indent=4)

                        #Saving upload
                        with open(folder_mes+f'img_ruido{option_cod_sen}_{inf_json_cal[0]["n_img_ruido"]}.'+str(image_file.type).split("/")[1],"wb") as f:
                            f.write((image_file).getbuffer())
                        c+=1
                if len(image_ruido) ==0:
                    if option_cod_sen == ".": option_cod_sen=""
                    os.system(f"rm {os.path.dirname(os.path.abspath(__file__))}/Inf_semestrales/{option_est}_{option_sen}/{option_year}/{option_month}/img_ruido{option_cod_sen}_*")
                    if os.path.exists(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json") == True:
                        with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                            inf_json_cal = json.load(file)
                                
                            inf_json_cal[0]["n_img_ruido"] = 0

                        with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'w') as (file):
                            json.dump(inf_json_cal, file, indent=4)
                            
                        
                st.experimental_rerun()

    #Ultima visita
    with tab_ul:
        
        st.header("Última visita")
        st.write(".")

        
        

        #get ultima visita
        #folder_semestre = os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option_est}_{option_sen}/{option_s}/"
        folder_mes = os.path.dirname(os.path.abspath(__file__))+f"/Inf_mensuales/{option_est}_{option_sen}/{option_year}/{option_month}/"
        if option_cod_sen == ".": option_cod_sen=""
            
        with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
            inf_json = json.load(file)
        
        text_fecha= inf_json[0]["ultima_v"][0]
        text_man= inf_json[0]["ultima_v"][1]
        text_com= inf_json[0]["ultima_v"][2]
        text_vis= inf_json[0]["ultima_v"][3]

        if len(text_man) == 0 or len(text_com) == 0 or len(text_vis) == 0:
            plot_CalEst.get_ultima_v(option_est,option_sen, folder_mes,option_cod_sen)
            with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                inf_json = json.load(file)
        
            text_fecha= inf_json[0]["ultima_v"][0]
            text_man= inf_json[0]["ultima_v"][1]
            text_com= inf_json[0]["ultima_v"][2]
            text_vis= inf_json[0]["ultima_v"][3]

        st.write(f"**Fecha de Mantenimiento:** {text_fecha}")
        st.write(f"**Tipo de Mantenimiento:** {text_man}")
        st.write(f"**Comentarios:** {text_com}")
        st.write(f"**Visitada por:** {text_vis}")
        st.write("__________")

            


        
        #if st.button("Actualizar ultima visita", key="act_ult_v"):
        #    plot_CalEst.actualizar_ultima_v()
        #    plot_CalEst.get_ultima_v(option_est,option_sen, option_s,option_cod_sen)
        #    st.experimental_rerun()


    #Recomendaciones
    with tab_rec:


        st.header("Recomendaciones")
        
        #Guardar y mostrar recomendaciones
        #folder_semestre = os.path.dirname(os.path.abspath(__file__))+f"/Inf_semestrales/{option_est}_{option_sen}/{option_s}/"
        folder_mes = os.path.dirname(os.path.abspath(__file__))+f"/Inf_mensuales/{option_est}_{option_sen}/{option_year}/{option_month}/"
        if option_cod_sen == ".": option_cod_sen=""
        with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
            inf_json = json.load(file)
        
        text_recom= inf_json[0]["recomendaciones"]
        
        st.write(text_recom)

        recomendaciones = st.text_area('')

        #guardar y mostrar imagenes
        image_recom=st.file_uploader("**Suba una imagen**", type =["png", "jpg","jpeg"],accept_multiple_files=True,key="image_recom")

        
        

        #Guardar
        if st.button("Guardar", help="Ingrese los comentarios y luego de Guardar, al volver a guardar se reemplazarán siempre los comentarios", key="but_recom"):

            hoy = datetime.now()
            fecha_hoy= f"{hoy.year}-{hoy.month}-{hoy.day}"

            folder_mes = os.path.dirname(os.path.abspath(__file__))+f"/Inf_mensuales/{option_est}_{option_sen}/{option_year}/{option_month}/"

            if option_cod_sen == ".": option_cod_sen=""
            
            if os.path.exists(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json") == True:
                with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                    inf_json_recom = json.load(file)
                
                if len(recomendaciones) != 0:
                    inf_json_recom[0]["recomendaciones"] = recomendaciones
                inf_json_recom[0]["fecha_creacion"] = fecha_hoy

                with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'w') as (file):
                        json.dump(inf_json_recom, file, indent=4)
            #Guardar imagenes
            if len(image_recom) >0:
                c=1
                for image_file in image_recom:
                    file_details_damage = {"filename":image_file.name,"filetype":image_file.type,
                                    "filesize":image_file.size}
                    #st.write(file_details_damage)
                    #st.image(load_image(image_file), width=250)

                    #Saving uploadif os.path.exists(folder_semestre + f"inf_{option_est}_{option_sen}.json") == True:
                    if option_cod_sen == ".": option_cod_sen=""
                    
                    with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                        inf_json_recom = json.load(file)
                        
                    inf_json_recom[0]["n_img_recom"] += 1

                    with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'w') as (file):
                        json.dump(inf_json_recom, file, indent=4)
                    
                    
                    with open(folder_mes+f'img_recom{option_cod_sen}_{inf_json_recom[0]["n_img_recom"]}.'+str(image_file.type).split("/")[1],"wb") as f:
                        f.write((image_file).getbuffer())
                    c+=1
                    
            if len(image_recom) ==0:
                
                os.system(f"rm {os.path.dirname(os.path.abspath(__file__))}/Inf_mensuales/{option_est}_{option_sen}/{option_year}/{option_month}/img_recom{option_cod_sen}_*")
                #os.system(f"rm {os.path.dirname(os.path.abspath(__file__))}/Inf_semestrales/{option_est}_{option_sen}/{option_s}/img_recom{option_cod_sen}_*")
                
                if option_cod_sen == ".": option_cod_sen=""
                if os.path.exists(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json") == True:
                    with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'r') as file:
                        inf_json_recom = json.load(file)
                            
                        inf_json_recom[0]["n_img_recom"] = 0

                    with open(folder_mes + f"inf_{option_est}_{option_sen}{option_cod_sen}.json", 'w') as (file):
                        json.dump(inf_json_recom, file, indent=4)

                            

            st.experimental_rerun()
        
        #Mostrar imagenes cargadas
        #if image_recom is not None:
            
            
        img_recom = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Inf_mensuales/{option_est}_{option_sen}/{option_year}/{option_month}/img_recom{option_cod_sen}_*")
        for image_file in img_recom:
            #file_details_damage = {"filename":image_file.name,"filetype":image_file.type,
            #                "filesize":image_file.size}
            #st.write(file_details_damage)
            st.image(load_image(image_file), width=500)

    cod_l = est_din[0][3] #[min_dis,max_dis,prom_dis,codigo_l]
    st.sidebar.write("_______")

    epoc=option_year+option_month

    col1, col2 = st.sidebar.columns([1,1])
    with col1:
        if est_din[0][0] == 0 and est_din[0][1] == 0 and est_din[0][2] == 0:
            st.write(".")
        else:
            if st.button("Crear Documento", key="but_create"):
                
                if option_cod_sen == ".": option_cod_sen=""
                
                #for all_sen in sensores:
                #    plot_CalEst.actualizar_info_s(option_est,all_sen,fecha_ini, fecha_fin,folder_inf,option_s)
                
                    
                create_doc.mk_doc(option_est,option_sen,cod_l,epoc,est_din,est_gapover,est_off,est_ppsd_pic,cod_sen=option_cod_sen,mes=True)
                #descargar
                folder_mes = os.path.dirname(os.path.abspath(__file__))+f"/Inf_mensuales/{option_est}_{option_sen}/{option_year}/{option_month}/"
    with col2:
        if os.path.exists(folder_mes+f'{option_est}_{cod_l}_{epoc}_informe.docx') == True:
            with open(folder_mes+f'{option_est}_{cod_l}_{epoc}_informe.docx', "rb") as file:
                btn = st.download_button(label="Descargar Docx", data=file, file_name=f'{option_est}_{cod_l}_{epoc}_informe.docx', mime="application/octet-stream")
    
    #if st.button("G", key="but_gr"):

    #    all_est2 = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/*")
    #    estaciones2 = []
    #    for est2 in all_est2:
    #        nom_est2 = est2.split("/")[8].split("_")[0]
    #        if nom_est2 not in estaciones2:
    #            estaciones2.append(nom_est2)
            
        #LISTA DE ESTACIONES
    #    for e2 in estaciones2:
    #        list_est2 = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/CM/Tablas_Cal_tiempos/{e2}*")

            #SENSORES
    #        sensores2 = []
    #        for e in list_est2:
    #            if e[-14:-12] not in sensores2:
    #                sensores2.append(e[-14:-12])
                    
    #        for all_sen in sensores2:
    #            plot_CalEst.actualizar_info_s(e2,all_sen,fecha_ini, fecha_fin,folder_inf,option_s)
    #            print(e2,all_sen)
        

  
def main():

    

    ##Parametros generales
    image = Image.open('images/Simbolo_SGC_Blanco.png')
    st.sidebar.image(image)
    st.sidebar.title("""Reporte Calidad Estacion""")
    st.sidebar.write("_______________________________________________")
    folder = os.path.dirname(os.path.abspath(__file__))+'/informes_estaciones'
    
    #Tipo de Consulta
    option_consulta = st.sidebar.selectbox('**Consulta**',["Por fechas","Informe semestral","Informe mensual"] ,key ="cons")
    
    st.sidebar.write("_________")
    

    if option_consulta == "Por fechas":
        est1_fechas()
    
    if option_consulta == "Informe mensual":
        est1_informe_m()
        #plt_3d.d4()

    if option_consulta == "Informe semestral":
        est1_informe_s()
    
    st.sidebar.write("_________")      
    with st.sidebar.expander("**Sobre la app Report_CalEst**"):
        st.write("""
                **Reporte_CalEst (Reporte de funcionamiento y calidad de estaciones)**\n 
                """)
        st.write(""" 
                Es una aplicación desarrollada por Angel Daniel Agudelo, 
                donde reune aplicaciones de Miguel Lizarazo en la toma de datos de estaciones y Monica Acosta con SIIGEO.
                La app muestra consultas por fechas y genera informes semestrales y mensuales en formato docx con la información de funcionamiento y calidad de cada estación en tiempo real, 
                mostrando por estación datos de disponibilidad, gaps, overlaps, offset, picos y ppsd. Además, 
                el sismólogo encargado puede ingresar sus observaciones del estado de cada estación.
      """)
        st.write("**Sugerencias y recomendaciones escribir al correo adagudelo@sgc.gov.co**")
        st.write("**Actualización, agosto de 2023**")

main()
