import streamlit as st
import json
import os
import pandas as pd




class Plot():
    
    def __init__(self, id, download_folder):

        self.folder = download_folder
        self.ID_event = id
    
    ##Informacion General
    def inf_g(self,):
        
        
        ID_event = self.ID_event
        folder = self.folder

        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_general_{ID_event}.json") == True:
            st.header("""Parámetros generales del sismo""")
                

            with open(folder+"/Data/"+f"inf_general_{ID_event}.json","r") as json_file: 
                results_IG = json.load(json_file)                               

            fecha_utc = results_IG[0]["inf_general"][0]        
            fecha_local = results_IG[0]["inf_general"][1]              
            lat = results_IG[0]["inf_general"][2]        
            lon = results_IG[0]["inf_general"][3]               
            prof = results_IG[0]["inf_general"][4]        
            mag = results_IG[0]["inf_general"][5]        
            ubic = results_IG[0]["inf_general"][6]        
            fuente = results_IG[0]["inf_general"][7]
            observ_IG= results_IG[0]["observaciones"]
            revisado = results_IG[0]['quien_reviso']


            st.subheader(f"{ubic}")
            st.image(f"{folder}/Images/Mapc_{ID_event}.gif")
            
            st.markdown(".")
            st.markdown(f" **Fecha UTC :** {fecha_utc}")    
            st.markdown(f" **Fecha Local :** {fecha_local}")    
            st.markdown(f" **Latitud :** {lat}")    
            st.markdown(f" **Longitud:** {lon}")    
            st.markdown(f" **Profundidad:** {prof}")    
            st.markdown(f" **Magnitud:** {mag}")    
            st.markdown(f" **Ubicación:** {ubic}")    
            st.markdown('_')
            st.markdown(f" **Observaciones:** {observ_IG}")
            st.markdown(f" **Revisó:** {revisado}")
            st.markdown(f"**Fuente:**  {fuente}")
            st.markdown("__________")
            
        else:
            print(f"aún no existe el json inf_general_{ID_event}.json")
    
    #Mecanismo Focal
    def inf_mf(self):

        ID_event = self.ID_event
        folder = self.folder

        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_mecanismofocal_{ID_event}.json") == True:

            st.header("""Mecanismo Focal""")
            with open(folder+"/Data/"+f"inf_mecanismofocal_{ID_event}.json","r") as json_file: ###____________
                results_MF = json.load(json_file)   

            strike1 = results_MF[0]["inf_mecanismofocal"][0]
            dip1 = results_MF[0]["inf_mecanismofocal"][1]
            rake1 = results_MF[0]["inf_mecanismofocal"][2]
            strike2 = results_MF[0]["inf_mecanismofocal"][3]
            dip2 = results_MF[0]["inf_mecanismofocal"][4]
            rake2 = results_MF[0]["inf_mecanismofocal"][5]
            metodologia = results_MF[0]["inf_mecanismofocal"][6]
            informacion = results_MF[0]["inf_mecanismofocal"][7]
            fuente = results_MF[0]["inf_mecanismofocal"][8]
            tipo = results_MF[0]["tipo_f"]
            observ_MF = results_MF[0]["observaciones"]
            revisado = results_MF[0]['quien_reviso']


            st.image(f"{folder}/Images/ball_{metodologia}_{ID_event}.png")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f" **Strike1 :** {strike1}")    
                st.markdown(f" **Dip1 :** {dip1}")    
                st.markdown(f" **Rake1 :** {rake1}")    
            with col2:
                st.markdown(f" **Strike2:** {strike2}")    
                st.markdown(f" **Dip2:** {dip2}")    
                st.markdown(f" **Rake2:** {rake2}")    
            st.markdown(f" **Metodología:** {informacion}")
            st.markdown(f" **Tipo de falla:** {tipo}") 

            if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/fallas/{tipo}.png") == True:
                st.image(os.path.dirname(os.path.abspath(__file__))+f"/fallas/{tipo}.png")
            st.markdown('__')   
            st.markdown(f" **Observaciones:** {observ_MF}")
            st.markdown(f" **Revisó:** {revisado}")
            st.markdown(f"**Fuente:** {fuente}")
            st.markdown("_______") 

        else:
            st.error(f"No hay datos de Mecanismo focal para el evento {ID_event}")
            print(f"aún no existe el json inf_mecanismofocal_{ID_event}.json")
    
    #Valores de aceleración
    def inf_a(self):

        ID_event = self.ID_event
        folder = self.folder

        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_aceleracion_{ID_event}.json") == True:

            st.header("Valores de aceleración")

            with open(folder+"/Data/"+f"inf_aceleracion_{ID_event}.json","r") as json_file: 
                results_A = json.load(json_file) 

            nombre_estacion_min = results_A[0]["inf_aceleracion"][0][0]
            codigo1 = results_A[0]["inf_aceleracion"][0][1]
            dist_epi1 = results_A[0]["inf_aceleracion"][0][2]
            dist_hip1 = results_A[0]["inf_aceleracion"][0][3]
            ac_ew1 = results_A[0]["inf_aceleracion"][0][4]
            ac_ns1 = results_A[0]["inf_aceleracion"][0][5]
            ac_z1 = results_A[0]["inf_aceleracion"][0][6]
            ac_max_h1 = results_A[0]["inf_aceleracion"][0][7]
            grav1 = results_A[0]["inf_aceleracion"][0][8]

            nombre_estacion_max = results_A[0]["inf_aceleracion"][1][0]
            codigo2 = results_A[0]["inf_aceleracion"][1][1]
            dist_epi2 = results_A[0]["inf_aceleracion"][1][2]
            dist_hip2 = results_A[0]["inf_aceleracion"][1][3]
            ac_ew2 = results_A[0]["inf_aceleracion"][1][4]
            ac_ns2 = results_A[0]["inf_aceleracion"][1][5]
            ac_z2 = results_A[0]["inf_aceleracion"][1][6]
            ac_max_h2 = results_A[0]["inf_aceleracion"][1][7]
            grav2 = results_A[0]["inf_aceleracion"][1][8]
            
            tab = pd.read_csv(f"{folder}/Tables/aceleracion_{ID_event}.csv")
            fuente = results_A[0]["inf_aceleracion"][1][9]
            observ_A = results_A[0]["observaciones"]
            revisado = results_A[0]['quien_reviso']
            
            tab_plot_ac = tab.loc[:,["Código","Dist.Epi(km)","Dist.Hip(km)",'PGA EW(cm/s^2)','PGA NS(cm/s^2)']]
            tab_plot_ac['Aceleración Máxima'] =( ((tab_plot_ac['PGA EW(cm/s^2)']**2 + tab_plot_ac['PGA NS(cm/s^2)']**2)/2)**0.5 )
            tab_plot_ac['gravedad (%)'] =(tab_plot_ac['Aceleración Máxima']/980)
            #tab_plot_ac['Aceleración maxima'] = tab_plot_ac.
            #((ac_ew2**2 + ac_ns2**2)/2)**0.5, 2

            st.markdown(".")
            
            colac1, colac2 = st.columns(2)
            

            with colac1:
                st.dataframe(tab_plot_ac,height=387 )
                st.markdown("_")
                st.markdown("**1era estación**")
                if dist_epi1 < dist_epi2:
                    st.markdown(f" **Estación con aceleración máxima :** \t{nombre_estacion_max}")
                else:
                    st.markdown(f" **Estación más cercana y Acel.max :** \t{nombre_estacion_max}")
                st.markdown(f" **Codigo :** \t{codigo2}")
                st.markdown("_")
                
            with colac2:
                st.image(f"{folder}/Images/map_ac_{ID_event}.png")
                st.markdown("_")
                st.markdown("**2da estación**")
                if dist_epi1 < dist_epi2:
                    st.markdown(f" **Estación más cercana :** \t{nombre_estacion_min}")       
                else:
                    st.markdown(f" **Segunda estación más cercana :** \t{nombre_estacion_min}")
                
                st.markdown(f" **Codigo :** \t{codigo1}")
                st.markdown("_")
            
            
            selected_options = [codigo1,codigo2]

            
            for i in range(2):
                available_options = [o for o in tab_plot_ac["Código"] if o not in selected_options]
                st.markdown("**3ra estación**" if i == 0 else "**4ta estación**") 
                selected_option = st.selectbox(f"Selecciona porfavor alguna estación relevante ({i+3}):", available_options)                    
                
                selected_options.append(selected_option)            
                st.markdown(f"Nombre de la estacion({i+3}) :"+ tab[tab["Código"]==selected_options[i+2]]["Nombre Estación"].values[0]) 
                st.markdown("_")
            

      
            #Extraccion de datos
            tab = pd.read_csv(f"{folder}/Tables/aceleracion_{ID_event}.csv")
            
            
            #ESTACION3
            if  len(selected_options) >=2 :
                indx_est3 = tab.index[tab['Código'] == selected_options[2]].tolist()
                inf_est3 = tab.iloc[(indx_est3[0])]
                
                codigo3 = inf_est3.loc['Código']
                nombre_estacion3 = inf_est3.loc['Nombre Estación']
                dist_epi3 = int(inf_est3.loc['Dist.Epi(km)'])
                dist_hip3 = int(inf_est3.loc['Dist.Hip(km)'])
                ac_ew3 = round(float(inf_est3.loc['PGA EW(cm/s^2)']), 2)
                ac_ns3 = round(float(inf_est3.loc['PGA NS(cm/s^2)']), 2)
                ac_z3 = round(float(inf_est3.loc['PGA Z(cm/s^2)']), 2)
                ac_mx_h3 = round(((ac_ew3**2 + ac_ns3**2)/2)**0.5, 2)
                gr3 = round((ac_mx_h3/980)*100, 2)
                
            #ESTACION4
            if  len(selected_options) >=3 :
                indx_est4 = tab.index[tab['Código'] == selected_options[3]].tolist()
                inf_est4 = tab.iloc[(indx_est4[0])]
                
                codigo4 = inf_est4.loc['Código']
                nombre_estacion4 = inf_est4.loc['Nombre Estación']
                dist_epi4 = int(inf_est4.loc['Dist.Epi(km)'])
                dist_hip4 = int(inf_est4.loc['Dist.Hip(km)'])
                ac_ew4 = round(float(inf_est4.loc['PGA EW(cm/s^2)']), 2)
                ac_ns4 = round(float(inf_est4.loc['PGA NS(cm/s^2)']), 2)
                ac_z4 = round(float(inf_est4.loc['PGA Z(cm/s^2)']), 2)
                ac_mx_h4 = round(((ac_ew3**2 + ac_ns3**2)/2)**0.5, 2)
                gr4 = round((ac_mx_h3/980)*100, 2)
                
                datos3 = [nombre_estacion3, codigo3, dist_epi3, dist_hip3, ac_ew3, ac_ns3, ac_z3, ac_mx_h3, gr3] 
                datos4 = [nombre_estacion4, codigo4, dist_epi4, dist_hip4, ac_ew4, ac_ns4, ac_z4, ac_mx_h4, gr4]             
                
                if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_aceleracion_{ID_event}.json") == True:

                    with open(folder+"/Data/"+f"inf_aceleracion_{ID_event}.json","r") as json_file: 
                        results_A = json.load(json_file)
                    results_A[0]["datos3"] = datos3
                    results_A[0]["datos4"] = datos4
                            
            

                #adicion de datos al Json
                with open(folder + '/Data/' + f"inf_aceleracion_{ID_event}.json", 'w') as (file):
                    json.dump(results_A, file)                
                
   
            
            
            st.markdown("_")
            st.markdown(f" **Observaciones:** \t{observ_A}")
            st.markdown(f" **Revisó:** {revisado}")
            st.markdown(f"**Fuente:** {fuente}")
            
            st.markdown("_______") 

        else:
            st.error(f"No hay datos de Aceleraciones para el evento {ID_event}")
            print(f"aún no existe el json inf_aceleracion_{ID_event}.json")

    ##Intensidad instrumental
    def inf_ii(self):

        ID_event = self.ID_event
        folder = self.folder

        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_instrumental_{ID_event}.json") == True:

            st.header("""Intensidad instrumental""")

            with open(folder+"/Data/"+f"inf_instrumental_{ID_event}.json","r") as json_file:
                results_II = json.load(json_file)                               

            int_max_romano = results_II[0]["inf_instrumental"][0]        
            movimiento = results_II[0]["inf_instrumental"][1]              
            danno = results_II[0]["inf_instrumental"][2]       
            pga_max = results_II[0]["inf_instrumental"][3]               
            pgv_max = results_II[0]["inf_instrumental"][4]        
            fuente = results_II[0]["inf_instrumental"][5]
            observ_II= results_II[0]["observaciones"]
            revisado = results_II[0]['quien_reviso']
            

            st.image(f"{folder}/Images/map_intensity_{ID_event}.jpg")
            st.markdown(".")  
            st.markdown(f" **Descripción:** Mapa que muestra el movimiento del terreno por niveles de intensidad y los posibles efectos\
                             causados por el sismo, generado de la combinación de registros en sismómetros, acelerógrafos, relaciones de atenuación de la\
                             energía sísmica e información sobre condiciones sísmicas locales." )
            st.markdown(" **Escala:** Mercalli modificada (MMI)")
            st.markdown(f" **Intensidad máxima :** \t{int_max_romano}")    
            st.markdown(f" **Percepción del movimiento :** \t{movimiento}")    
            st.markdown(f" **Daño :** \t{danno}")    
            st.markdown(f" **Máxima aceleración:** \t{pga_max} %g")    
            st.markdown(f" **Máxima velocidad:** \t{pgv_max} cm/s") 
            st.markdown("_")   
            st.markdown(f" **Observaciones:** \t{observ_II}")
            st.markdown(f" **Revisó:** {revisado}")
            st.markdown(f" **Fuente:** {fuente}")
            st.markdown("_______") 
        
        else:
            st.error(f"No hay datos de Intensidad instrumental para el evento {ID_event}")
            print(f"aún no existe el json inf_instrumental_{ID_event}.json")


    ##Intensidad percibida
    def inf_ip(self):
        
        ID_event = self.ID_event
        folder = self.folder

        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_intpercibida_{ID_event}.json") == True:

            st.header("""Intensidad percibida (macrosísmica) """)

            with open(folder+"/Data/"+f"inf_intpercibida_{ID_event}.json","r") as json_file: 
                results_IP = json.load(json_file)    

            n_reportes = results_IP[0]["inf_intpercibida"][0]
            n_centros_poblados = results_IP[0]["inf_intpercibida"][1]
            n_municipio = results_IP[0]["inf_intpercibida"][2]
            n_departamentos = results_IP[0]["inf_intpercibida"][3]
            int_maxima = results_IP[0]["inf_intpercibida"][4]
            intensidad_reportada = results_IP[0]["inf_intpercibida"][5]
            centro_poblado_max = results_IP[0]["inf_intpercibida"][6]
            municipio_max = results_IP[0]["inf_intpercibida"][7]
            mun_rep_max = results_IP[0]["inf_intpercibida"][8]
            poblados_alejados_max = results_IP[0]["inf_intpercibida"][9]
            fuente = results_IP[0]["inf_intpercibida"][10]
            descripcion = results_IP[0]["descr_im"]
            sent_otros_paises = results_IP[0]["sent_otros_paises"]
            replicas_sentidas = results_IP[0]["replicas_sentidas"]

            revisado = results_IP[0]['quien_reviso']
            
            colac1, colac2 = st.columns(2)
            
            with colac1:
                st.image(f"{folder}/Images/histo_int_percibida_{ID_event}.png")
                st.markdown(".")

            with colac2:
                st.image(f"{folder}/Images/map_int_perc_{ID_event}.png")    
                st.markdown(".")                  

            st.markdown(f" **Número de reportes recibidos :** {n_reportes}")    
            st.markdown("**Sitios donde se reportó como sentido**")
            st.markdown(f"**Centros poblados :** \t{n_centros_poblados}")    
            st.markdown(f" **municipios:** \t{n_municipio}")    
            st.markdown(f" **departamentos:** \t{n_departamentos}")    
            st.markdown(f" **Intensidad máxima Reportada :** \t{int_maxima}. {intensidad_reportada}")   
            st.markdown(f" **Centros poblados donde se \nreportó la intensidad máxima :** \t{centro_poblado_max}, {municipio_max}")   
            st.markdown(f" **Municipios con mayor número de reportes :** \t{mun_rep_max}")    
            st.markdown(f" **Centros poblados más alejados del hipocentro \n donde fue reportado como sentido el sismo. :** \t{poblados_alejados_max}")    ###____________
            st.markdown(f" **Descripción intensidad máxima :** {descripcion}")
            st.markdown(f" **Sentido en otros países :** {sent_otros_paises}")   
            st.markdown(f" **Réplicas reportadas como sentidas :** \t{replicas_sentidas}")
            st.markdown("_") 
            st.markdown(f" **Revisó:** {revisado}")
            st.markdown(f" **Fuente:** {fuente}")
            st.markdown("_______")   
       
        else:
            st.error(f"No hay datos de Intensidad percibida para el evento {ID_event}")
            print(f"aún no existe el json inf_intpercibida_{ID_event}.json")

    ##Reporte de daños en infraestructura
    def inf_reporte_danos(self):

        ID_event = self.ID_event
        folder = self.folder

        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_repdanos_{ID_event}.json") == True:

            with open(folder+"/Data/"+f"inf_repdanos_{ID_event}.json","r") as json_file1: ###____________
                    results_rd = json.load(json_file1)

            st.header("""Reporte de daños en infraestructura""")

            
            
            n_mun = results_rd[0]["n_mun"]
            dis_rd = results_rd[0]["dist_rep"]
            danos = results_rd[0]["danos"]

            
            fuente = results_rd[0]["fuente"]
            revisado = results_rd[0]["autor"]


            #file =folder+"/Images/image_file_damage_report"+str(files_saved_dr)+"."+type_file

            
            #st.image(f"{folder}/Images/image_file_damage_report*")daños
            st.markdown(".")  

            st.markdown(f" **Número de municipios donde se reportaron daños :  ** {n_mun}")    
            st.markdown(f"**Distancia hipocentral máxima de reporte de daños :  ** \t{dis_rd}")    
            
            cold, colm = st.columns(2)
            with cold:
                st.markdown(f" **Departamento:**")  
            with colm:
                st.markdown(f" **Municipios:**")  

            #departamentos y municipios
            if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_dep_mun{ID_event}.json") == True:
                with open(folder+"/Data/"+f"inf_dep_mun{ID_event}.json","r") as json_file2: ###____________
                    results_dep_mun = json.load(json_file2)
                    

                if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_dep{ID_event}.json") == True:
                    with open(folder+"/Data/"+f"inf_dep{ID_event}.json","r") as json_file3: ###____________
                        results = json.load(json_file3)
                    
                    results_dep = results[0]["departamentos"]

                    for dep in results_dep:
                        
                        mun = ""
                        municipios = results_dep_mun[0][dep]
                        for m in municipios:
                            mun += m+", "     #municipios
                        
                        coldep, colmun = st.columns(2)
                        with coldep:
                            st.markdown(dep)
                        with colmun:
                            st.markdown(mun)

            st.markdown(f" **Daños reportados :  ** {danos}")    
            #st.markdown(f" **__Municipio:** \t{municipios}")    
        
            st.markdown("_") 
            st.markdown(f" **Revisó:** {revisado}")
            st.markdown(f" **Fuente:** {fuente}")
            st.markdown("____________________")   

            
            n_images = results_rd[1]["n_imagenes"]
            for e in range(n_images):

                st.markdown(f"** Imagen{e+1} **")
                name_images = results_rd[1][f"name_image{e+1}"]
                if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Images/{name_images}") == True:
                
                    path_images = f"{folder}/Images/{name_images}"
                    st.image(path_images)

                fuente_image = results_rd[1][f"input_fuente{e+1}"] 
                ubicacion_image =  results_rd[1][f"input_ubicacion{e+1}"]

                st.markdown(f"** Fuente de imagen{e+1}** : {fuente_image}")
                st.markdown(f"** Ubicación de imagen{e+1}** : {ubicacion_image}")
                st.markdown(f".")
            st.markdown("____________________")   

                



        
