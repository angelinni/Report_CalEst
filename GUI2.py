import os
from os import truncate
from os import remove as rm
from numpy import empty
import streamlit as st
import mkPDF as mkPDF
from PIL import Image
import shutil
import errno
import web_inf  ###____________
import json     ### 
import plot_info ###
from time import sleep

st.set_page_config(
    page_title="Reporte Sismo - SGC",
    menu_items={"About": """*Reporte Sismo* es un Aplicativo desarrollado por A. Agudelo y J. Soriano para generar un pdf con la información general de un Evento sismico publicado en https://www.sgc.gov.co/sismos .
      **si encuentra un error escribir al correo adagudelo@sgc.gov.co o jsoriano@sgc.gov.co**""",}
)

def load_image(image_file):
    img = Image.open(image_file)
    return img

def main():


    st.title("""Reporte sismo""")
    st.write("_______________________________________________")

    #Parametros generales
    image = Image.open('images/Simbolo_SGC_Blanco.png')
    st.sidebar.image(image)
    #st.sidebar.markdown("***Por favor Ingrese el ID del sismo***")
    ID_event = st.sidebar.text_input("Por favor Ingrese el ID del sismo","", max_chars=13,key ="IDev")
    #st.session_state.IDev
    st.sidebar.markdown(".")
    folder = os.path.dirname(os.path.abspath(__file__))+'/Events/'+ID_event    ###____________
    
    
    if st.sidebar.button("Aceptar"):
        try:
            
            #Creación de carpetas
            if ID_event[0:3] == "SGC" and len(ID_event) == 13:
                os.mkdir(folder)               ###____________
                try:
                    os.mkdir(folder+'/Images') ###____________
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise

                try:
                    os.mkdir(folder+'/Tables') ###____________
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
                
                try:
                    os.mkdir(folder+'/Data')
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
            elif len(ID_event) == 0:
                folder = folder+"falso"
                os.mkdir(folder)

            else:
                st.sidebar.error(f"El ID {ID_event} no existe ")
                

            
            #Extracción de los datos
            ##Informacion General
            reporte = web_inf.Reporte(ID_event, folder)  
            rep_ig = reporte.inf_general()  
            
            if rep_ig == True: 
                st.success("Información General ok")

                ##Mecanismo focal
                rep_mf = reporte.inf_mecanismofocal() 
                if rep_mf == True: st.success("Mecanismo focal ok")
                if rep_mf == False: st.error("No hay datos de Mecanismo focal")
                
                #Valores de aceleración
                rep_a =reporte.inf_aceleracion()
                if rep_a == True: st.success("Valores de aceleración ok")
                if rep_a == False: st.error("No hay datos de Valores de aceleración")

                ##Intensidad instrumental
                rep_ii= reporte.inf_instrumental()  ###____________
                if rep_ii == True: st.success("Intensidad instrumental ok")
                if rep_ii == False: st.error("No hay datos de Intensidad instrumental")
                ##Intensidad percibida
                rep_ip = reporte.inf_intpercibida()
                if rep_ip == True: st.success("Intensidad percibida ok")
                if rep_ip == False: st.error("No hay datos de Intensidad percibida")
                st.sidebar.success("Se ha cargado la información del sismo")
                sleep(3)
                st.experimental_rerun()
            
            else:
                
                os.system(f"rm -r {folder}")
                st.error(f"El ID {ID_event} no existe")
            
        except OSError as e:
            st.sidebar.success("ya existe información del Evento")
            if e.errno != errno.EEXIST:
                raise
        
        #st.sidebar.markdown(".")    
        #Reprocesar todo
        ##if st.sidebar.button("Reprocesar", help="Reiniciar consulta web, la información guardada se borrara."):
        ##    reporte = web_inf.Reporte(ID_event, folder)  ###____________

        ##    #Extracción de los datos
        ##    ##Informacion General
        ##    rep_ig = reporte.inf_general()  ###____________
            
        ##    if rep_ig == True: 
        ##        st.success("Información General ok")
        ##        

        ##        ##Mecanismo focal
        ##        rep_mf = reporte.inf_mecanismofocal() 
        ##        if rep_mf == True: st.success("Mecanismo focal ok")
        ##        if rep_mf == False: st.error("No hay datos de Mecanismo focal")
        ##        
        ##        #Valores de aceleración
        ##        rep_a =reporte.inf_aceleracion()
        ##        if rep_a == True: st.success("Valores de aceleración ok")
        ##        if rep_a == False: st.error("No hay datos de Valores de aceleración")

        ##        ##Intensidad instrumental
        ##        rep_ii= reporte.inf_instrumental()  ###____________
        ##        if rep_ii == True: st.success("Intensidad instrumental ok")
        ##        if rep_ii == False: st.error("No hay datos de Intensidad instrumental")
        ##        ##Intensidad percibida
        ##        rep_ip = reporte.inf_intpercibida()
        ##        if rep_ip == True: st.success("Intensidad percibida ok")
        ##        if rep_ip == False: st.error("No hay datos de Intensidad percibida")
        ##        st.sidebar.success("Se ha cargado la información del sismo")
        ##        sleep(3)
        ##        st.experimental_rerun()

        ##    else:
                
        ##        #os.system(f"rm -r {folder}")
        ##        print(f"El ID {ID_event} no existe")


    #Path
    main_path= os.path.dirname(os.path.abspath(__file__))+'/Events/'+ID_event
    
    #Datos en Streamlit
    plt_inf = plot_info.Plot(ID_event, folder) 
    st.sidebar.write("____________________________")
    option = st.sidebar.selectbox("Seleccione los parámetros",("Información General","Mecanismo focal","Aceleraciones","Intensidad instrumental","Intensidad percibida","Reporte de daños","Efectos de la naturaleza","Sismicidad histórica"))
    
    def guardar_json(id,folder,parametro, input_ob, input_author):

        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{id}/Data/{parametro}_{id}.json") == True:
 
                with open(folder+"/Data/"+f"{parametro}_{id}.json","r") as json_file: 
                        results = json.load(json_file) 

                results[0]["observaciones"] = input_ob
                for auth in input_author:
                    results[0]['quien_reviso'] += f"{auth},"
                


                with open(folder + '/Data/' + f"{parametro}_{id}.json", 'w') as (file):
                        json.dump(results, file)

    #infomracion General
    if option == "Información General":

        #Ploteo de los datos en la pagina

        plt_inf.inf_g()

        input_geneObservations = st.text_area(""" Por favor ingrese las observaciones generales del sismo""","", max_chars=700, key="<geneObservations>")
        

        #Lista de autores,   se encuentra en el autor.json
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+"/autor.json") == True:
            with open(os.path.dirname(os.path.abspath(__file__))+"/autor.json","r") as json_file_au: ###____________
                results_autor = json.load(json_file_au)   
            author1 = results_autor[0]["informacion_GM"]


        #Actualización de lista de autores
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_general_{ID_event}.json") == True:
            with open(folder+"/Data/"+f"inf_general_{ID_event}.json","r") as json_file: ###____________
                results_IG = json.load(json_file)   
            author = []
            revisado = results_IG[0]['quien_reviso'].split(",")
            for a in author1:
                if a not in revisado:
                    author.append(a)
        else:
            author = author1
        #


        author_gp = st.multiselect("Quien revisó", author,key="<Aut_gp>")
        st.markdown(".")
        
        col1,col2= st.columns([5,0.9])
        with col1:
            if st.button("Guardar", help="Ingrese todos los datos y luego de Guardar, si se vuelve a guardar se reemplazarán los datos menos la de Quién revisó."):
                
                #Para que no se elimine las observaciones si se guarda con datos vacios
                if len(input_geneObservations) == 0:
                    if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_general_{ID_event}.json") == True:
                        with open(folder+"/Data/"+f"inf_general_{ID_event}.json","r") as json_file: ###____________
                            results_IG = json.load(json_file)
                        observ = results_IG[0]['observaciones']
                        input_geneObservations = observ
                    else:
                        input_geneObservations = input_geneObservations

                 
                guardar_json(ID_event, folder, "inf_general",input_geneObservations,author_gp)
                st.experimental_rerun()
         
        with col2:

            if st.button("Reprocesar", help="Vuelve a hacer la consulta en la página y extrae los nuevos datos. La información ingresados se borraran"):
                reporte = web_inf.Reporte(ID_event, folder)
                rep_ig = reporte.inf_general()
                st.experimental_rerun()
                

        
    #Mecanismno Focal
    if option == "Mecanismo focal":
       
        

        plt_inf.inf_mf()
         
        input_tipofalla = st.multiselect("Tipo de falla", ["Normal", "Inversa", "Rumbo", "No hay información suficiente"])
        input_fmObservations = st.text_area("Por favor ingrese las observaciones del mecanismo focal del sismo"," ", max_chars=515,key="<mfObservations>")

        #Lista de autores,   se encuentra en el autor.json
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+"/autor.json") == True:
            with open(os.path.dirname(os.path.abspath(__file__))+"/autor.json","r") as json_file_au: ###____________
                results_autor = json.load(json_file_au)   
            author1 = results_autor[0]["informacion_GM"]

        #Actualización de lista de autores
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_mecanismofocal_{ID_event}.json") == True:
            with open(folder+"/Data/"+f"inf_mecanismofocal_{ID_event}.json","r") as json_file: ###____________
                results_MF = json.load(json_file)   
            author = []
            revisado = results_MF[0]['quien_reviso'].split(",")
            for a in author1:
                if a not in revisado:
                    author.append(a)

        else:
            author = author1
        
        author_fm = st.multiselect("Quien revisó", author ,key="<Aut_fm>")
        st.markdown(".")

        col1,col2= st.columns([5,0.9])
        with col1:

            if st.button("Guardar", help="Ingrese todos los datos y luego de Guardar, si se vuelve a guardar se reemplazarán los datos menos la de Quién revisó."):

                #Para que no se elimine las observaciones si se guarda con datos vacios
                if len(input_fmObservations) == 0:
                    if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_mecanismofocal_{ID_event}.json") == True:
                        with open(folder+"/Data/"+f"inf_mecanismofocal_{ID_event}.json","r") as json_file: ###____________
                            results_mf = json.load(json_file)
                        observ = results_mf[0]['observaciones']
                        input_fmObservations = observ
                    else:
                        input_fmObservations = input_fmObservations
                elif len(input_tipofalla) == 0: 
                    if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_mecanismofocal_{ID_event}.json") == True:
                        with open(folder+"/Data/"+f"inf_mecanismofocal_{ID_event}.json","r") as json_file: ###____________
                            results_mf = json.load(json_file)
                        observ = results_mf[0]['tipo_f']
                        input_tipofalla = observ
                    else:
                        input_tipofalla = input_tipofalla
                else:

                    if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_mecanismofocal_{ID_event}.json") == True:
                            ##Guardar datos de entrada en json
                            with open(folder+"/Data/"+f"inf_mecanismofocal_{ID_event}.json","r") as json_file: 
                                results = json.load(json_file) 

                            results[0]["tipo_f"] = input_tipofalla

                            results[0]["observaciones"] = input_fmObservations
                            for auth in author_fm:
                                results[0]['quien_reviso'] += f"{auth},"
                            results[0]["tipo_f"] = input_tipofalla[0]

                            with open(folder + '/Data/' + f"inf_mecanismofocal_{ID_event}.json", 'w') as (file):
                                json.dump(results, file)
                            #guardar_json(ID_event, folder, "inf_mecanismofocal",input_fmObservations,author_fm)
                            st.experimental_rerun()
                    elif os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_mecanismofocal_f{ID_event}.json") == True:
                            ##Guardar datos de entrada en json
                            with open(folder+"/Data/"+f"inf_mecanismofocal_{ID_event}.json","r") as json_file: 
                                results = json.load(json_file) 

                            results[0]["tipo_f"] = input_tipofalla

                            results[0]["observaciones"] = input_fmObservations
                            for auth in author_fm:
                                results[0]['quien_reviso'] += f"{auth},"
                            results[0]["tipo_f"] = input_tipofalla[0]

                            with open(folder + '/Data/' + f"inf_mecanismofocal_f{ID_event}.json", 'w') as (file):
                                json.dump(results, file)
                            #guardar_json(ID_event, folder, "inf_mecanismofocal",input_fmObservations,author_fm)
                            st.experimental_rerun()       
                
        with col2:

            if st.button("Reprocesar", help="Vuelve a hacer la consulta en la página y extrae los nuevos datos. La información ingresados se borraran"):
                reporte = web_inf.Reporte(ID_event, folder)
                rep_ig = reporte.inf_mecanismofocal()
                st.experimental_rerun()
       
        
        
    # Aceleraciones
    if option == "Aceleraciones":

        
        
        plt_inf.inf_a()

        #select_station3 = st.multiselect("Por favor seleciona una estacion con aceleraciones registradas relevantes: ",key ="<vaStattion3>")
        #select_station4 = st.multiselect("Por favor seleciona una estacion con aceleraciones registradas relevantes: ",key ="<vaStattion4>")
        input_vaObservations = st.text_area("Por favor ingrese las observaciones de los valores de aceleración del sismo",max_chars=400 ,key ="<vaObservations>")

        #Lista de autores,   se encuentra en el autor.json
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+"/autor.json") == True:
            with open(os.path.dirname(os.path.abspath(__file__))+"/autor.json","r") as json_file_au: ###____________
                results_autor = json.load(json_file_au)   
            author1 = results_autor[0]["valores_aceleracion"]


        #Actualización de lista de autores
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_aceleracion_{ID_event}.json") == True:
            with open(folder+"/Data/"+f"inf_aceleracion_{ID_event}.json","r") as json_file: ###____________
                results_A = json.load(json_file)   
            author = []
            revisado = results_A[0]['quien_reviso'].split(",")
            for a in author1:
                if a not in revisado:
                    author.append(a)

        else:
            author = author1
        

        author_ac = st.multiselect("Quien revisó", author,key="<Aut_ac>")
        st.markdown(".")

        col1, col2 = st.columns([5,0.9])
        with col1:
            if st.button("Guardar",  help="Ingrese todos los datos y luego de Guardar, si se vuelve a guardar se reemplazarán los datos menos la de Quién revisó."):
                
                #Para que no se elimine las observaciones si se guarda con datos vacios
                if len(input_vaObservations) == 0:
                    if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_aceleracion_{ID_event}.json") == True:
                        with open(folder+"/Data/"+f"inf_aceleracion_{ID_event}.json","r") as json_file: ###____________
                            results_ac = json.load(json_file)
                        observ = results_ac[0]['observaciones']
                        input_vaObservations = observ
                    else:
                        input_vaObservations = input_vaObservations

                guardar_json(ID_event, folder, "inf_aceleracion",input_vaObservations,author_ac)
                st.experimental_rerun()
        with col2:

            if st.button("Reprocesar", help="Vuelve a hacer la consulta en la página y extrae los nuevos datos. La información ingresados se borraran"):
                reporte = web_inf.Reporte(ID_event, folder)
                rep_ig = reporte.inf_aceleracion()
                st.experimental_rerun()

    #Intensidad Instrumental
    if option == "Intensidad instrumental":
        
        
        plt_inf.inf_ii()
        input_iiObservations= st.text_area("Por favor ingrese las observaciones de la intensidad instrumental del sismo", max_chars=310 ,key ="<iiObservations>")


        #Lista de autores,   se encuentra en el autor.json
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+"/autor.json") == True:
            with open(os.path.dirname(os.path.abspath(__file__))+"/autor.json","r") as json_file_au: ###____________
                results_autor = json.load(json_file_au)   
            author1 = results_autor[0]["intensidad_instrumental"]

        #Actualización de lista de autores
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_instrumental_{ID_event}.json") == True:
            with open(folder+"/Data/"+f"inf_instrumental_{ID_event}.json","r") as json_file: ###____________
                results_II = json.load(json_file)   
            author = []
            revisado = results_II[0]['quien_reviso'].split(",")
            for a in author1:
                if a not in revisado:
                    author.append(a)

        else:
            author = author1
        #

        author_ii = st.multiselect("Quien revisó",author,key="<Aut_ii>")
        st.markdown(".")

        col1, col2 = st.columns([5,0.9])
        with col1:
            if st.button("Guardar", help="Ingrese todos los datos y luego de Guardar, si se vuelve a guardar se reemplazarán los datos menos la de Quién revisó."):
                
                #Para que no se elimine las observaciones si se guarda con datos vacios
                if len(input_iiObservations) == 0:
                    if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_instrumental_{ID_event}.json") == True:
                        with open(folder+"/Data/"+f"inf_instrumental_{ID_event}.json","r") as json_file: ###____________
                            results_ii = json.load(json_file)
                        observ = results_ii[0]['observaciones']
                        input_iiObservations = observ
                    else:
                        input_iiObservations = input_iiObservations
                        
                guardar_json(ID_event, folder, "inf_instrumental",input_iiObservations,author_ii)
                st.experimental_rerun()
        with col2:

            if st.button("Reprocesar", help="Vuelve a hacer la consulta en la página y extrae los nuevos datos. La información ingresados se borraran"):
                reporte = web_inf.Reporte(ID_event, folder)
                rep_ig = reporte.inf_instrumental()
                st.experimental_rerun()
    
    #Intensidad Percibida
    if option == "Intensidad percibida":
       

        plt_inf.inf_ip()
        input_sent_otros_paises = st.text_area("Por favor ingrese otros países que sintieron el evento.", max_chars= 120 ,key ="<dr_sentido_en_otros_paises>")
        input_replicas_sentidas = st.text_area("Por favor ingrese las réplicas reportadas como sentidas.", max_chars= 200 ,key ="<dr_replicas_reportadas_como_sentidas>")

        #Lista de autores,   se encuentra en el autor.json
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+"/autor.json") == True:
            with open(os.path.dirname(os.path.abspath(__file__))+"/autor.json","r") as json_file_au: ###____________
                results_autor = json.load(json_file_au)   
            author1 = results_autor[0]["intensidad_PDEH"]

        #Actualización de lista de autores
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_intpercibida_{ID_event}.json") == True:
            with open(folder+"/Data/"+f"inf_intpercibida_{ID_event}.json","r") as json_file: ###____________
                results_IP = json.load(json_file)   
            author = []
            revisado = results_IP[0]['quien_reviso'].split(",")
            for a in author1:
                if a not in revisado:
                    author.append(a)

        else:
            author = author1
        ##

        author_ip = st.multiselect("Quien revisó", author,key="<Aut_ip>")
        st.markdown(".")

        col1, col2 = st.columns([5,0.9])
        with col1:
            if st.button("Guardar", help="Ingrese todos los datos y luego de Guardar, si se vuelve a guardar se reemplazarán los datos menos la de Quién revisó."):
                guardar_json(ID_event, folder, "inf_intpercibida",input_ipObservations,author_ip)

                if len(input_ipObservations) == 0:
                    if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_intpercibida_{ID_event}.json") == True:
                        with open(folder+"/Data/"+f"inf_intpercibida_{ID_event}.json","r") as json_file: ###____________
                            results_ip = json.load(json_file)
                        observ = results_ip[0]['descr_im']
                        input_ipObservations = observ
                    else:
                        input_ipObservations = input_ipObservations

                if len(input_sent_otros_paises) == 0:
                    if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_intpercibida_{ID_event}.json") == True:
                        with open(folder+"/Data/"+f"inf_intpercibida_{ID_event}.json","r") as json_file: ###____________
                            results_ip = json.load(json_file)
                        observ = results_ip[0]['sent_otros_paises']
                        input_sent_otros_paises = observ
                    else:
                        input_sent_otros_paises = input_sent_otros_paises
                
                if len(input_replicas_sentidas) == 0:
                    if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_intpercibida_{ID_event}.json") == True:
                        with open(folder+"/Data/"+f"inf_intpercibida_{ID_event}.json","r") as json_file: ###____________
                            results_ip = json.load(json_file)
                        observ = results_ip[0]['replicas_sentidas']
                        input_replicas_sentidas = observ
                    else:
                        input_replicas_sentidas = input_replicas_sentidas

                ##Guardar datos de entrada en json
                with open(folder+"/Data/"+f"inf_intpercibida_{ID_event}.json","r") as json_file: 
                    results = json.load(json_file) 


                results[0]["descr_im"] = input_ipObservations
                results[0]["sent_otros_paises"] = input_sent_otros_paises
                results[0]["replicas_sentidas"] = input_replicas_sentidas

                with open(folder + '/Data/' + f"inf_intpercibida_{ID_event}.json", 'w') as (file):
                    json.dump(results, file)

                st.experimental_rerun()
        with col2:

            if st.button("Reprocesar", help="Vuelve a hacer la consulta en la página y extrae los nuevos datos. La información ingresados se borraran"):
                reporte = web_inf.Reporte(ID_event, folder)
                rep_ig = reporte.inf_intpercibida()
                st.experimental_rerun()
    #Reporte de daños
    if option == "Reporte de daños":

        
        plt_inf.inf_reporte_danos()
        input_mun_rp = st.number_input("Ingrese el número municipios donde se reportaron daños.", min_value=1 ,step=0)
        input_dist_rp = st.text_input("Ingrese la distancia hipocentral máxima de reporte de daños")


        st.write(".")
        st.markdown("Ingrese el departamento y municipios, luego de guardar e ingrese el siguiente departamento y municipios.")
        
        #Departamentos y municipios
        #departamentos restantes
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/NO_inf_dep{ID_event}.json") == True:
                with open(folder+"/Data/"+f"NO_inf_dep{ID_event}.json","r") as json_file: ###____________
                    results_dep_munNO = json.load(json_file)
                    departamentos1 = results_dep_munNO[0]["departamentos"]    
        else:
            departamentos1 = ['ANTIOQUIA', 'ATLANTICO', 'BOGOTA DC', 'BOLIVAR', 'BOYACA', 'CALDAS', 'CAQUETÁ', 'CAUCA', 'CESAR', 'CÓRDOBA', 'CUNDINAMARCA', 'CHOCÓ', 'HUILA', 'LA GUAJIRA', 'MAGDALENA', 'META', 'NARIÑO',
                         'NORTE DE SANTANDER', 'QUINDIO', 'RISARALDA', 'SANTANDER', 'SUCRE', 'TOLIMA', 'VALLE DEL CAUCA', 'ARAUCA', 'CASANARE', 'PUTUMAYO', 'SAN ANDRÉS', 'AMAZONAS', 'GUANÍA', 'GUAVIARE', 'VAUPÉS', 'VICHADA']
        
        #municipios
        with open(os.path.dirname(os.path.abspath(__file__))+"/dep_mun.json","r") as json_file:
            results = json.load(json_file)
        
        col1, col2 = st.columns([1,1])
        with col1:
            dep = st.selectbox("Departamento", departamentos1)
            
        with col2:
            if len(dep) > 0:
                municipios = sorted(results[0][dep])
                mun = st.multiselect("Municipios",municipios)
        
        #Guardar departamentos y municipios de entrada en json
        
        if st.button("Guardar municipios", help="Puede guardar el número de departamentos y municipios que desee"):
            
            if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_dep{ID_event}.json") == True:
                with open(folder+"/Data/"+f"inf_dep{ID_event}.json","r") as json_file: ###____________
                    results_dep_mun = json.load(json_file) 
                revisado = results_dep_mun[0]['departamentos']
                dep_list = revisado
            else:
                dep_list = []
            
            dep_list.append(dep)

            datos_json = [{'departamentos':dep_list}]

            with open(folder + '/Data/' + f"inf_dep{ID_event}.json", 'w') as (file):
                json.dump(datos_json, file)

            #Actualización de lista de dep
            if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_dep{ID_event}.json") == True:
                with open(folder+"/Data/"+f"inf_dep{ID_event}.json","r") as json_file: ###____________
                    results_dep = json.load(json_file)   
                departamentos = []
                revisado = results_dep[0]['departamentos']
                for d in departamentos1:
                    if d not in revisado:
                        departamentos.append(d)
            
            #departamentos restantes
            with open(folder + '/Data/' + f"NO_inf_dep{ID_event}.json", 'w') as (file2):
                json.dump([{"departamentos":departamentos}], file2)
            

            #guardar departamentos y municipios
            
            if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_dep_mun{ID_event}.json") == True:
                with open(folder+"/Data/"+f"inf_dep_mun{ID_event}.json","r") as json_file: ###____________
                    results_dep_mun = json.load(json_file)   
                results_dep_mun[0][dep]= mun

                with open(folder + '/Data/' + f"inf_dep_mun{ID_event}.json", 'w') as (file3):
                    json.dump(results_dep_mun, file3)
            else:
                with open(folder + '/Data/' + f"inf_dep_mun{ID_event}.json", 'w') as (file3):
                    json.dump([{dep:mun}], file3)

            

            st.experimental_rerun()



        input_danos = st.text_area("Ingrese los daños reportados.")
        input_fuente = st.text_area("Ingrese la fuente de la información.")

        #Lista de autores,   se encuentra en el autor.json
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+"/autor.json") == True:
            with open(os.path.dirname(os.path.abspath(__file__))+"/autor.json","r") as json_file_au: ###____________
                results_autor = json.load(json_file_au)   
            author1 = results_autor[0]["intensidad_PDEH"]

        #Actualización de lista de autores
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_repdanos_{ID_event}.json") == True:
            with open(folder+"/Data/"+f"inf_repdanos_{ID_event}.json","r") as json_file: ###____________
                results_RD = json.load(json_file)   
                print("True_daños")
                
            author = []
            
            if len(results_RD[0]['autor']) > 1:

                revisado = ",".join(results_RD[0]['autor']).split(",")

            else:
                revisado = results_RD[0]['autor']
            for a in author1:
                if a not in revisado:
                    author.append(a)

        else:
            author = author1
        ##
        author_dr = st.multiselect("Quien revisó", author,key="<Aut_dr>")

        image_files_damage_report=st.file_uploader("Sube la imagen aquí", type =["png", "jpg","jpeg"], key ="<damage_report>",accept_multiple_files=True)
        
          

        if image_files_damage_report is not None:

            if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_repdanos_{ID_event}.json") == True:
                with open(folder+"/Data/"+f"inf_repdanos_{ID_event}.json","r") as json_file: ###____________
                    results_rep = json.load(json_file) 
            
                n_image = results_rep[1]["n_imagenes"]+len(image_files_damage_report)
                n_image1 = results_rep[1]["n_imagenes"]
            else:
                n_image = len(image_files_damage_report)
            if len(image_files_damage_report) >0:
                
                col1, col2 = st.columns([1,1])
                with col1:
                    input_fuente = st.text_area(f"Ingrese la fuente de la imagen{n_image}.",key =f"<fuente{n_image}>")
                    
                with col2:
                    input_ubicacion = st.text_area(f"Ingrese la ubicación de la imagen{n_image}.",key =f"<ubicacion{n_image}>")
                
                if st.button("Guardar Imagen e información"):
                    #inf_img = {}
                    #inf_img["n_imagenes"] = n_image
                    #inf_img[f"input_fuente{n_image}"] = input_fuente
                    #inf_img[f"input_ubicacion{n_image}"] = input_ubicacion

                    if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_repdanos_{ID_event}.json") == True:
                        with open(folder+"/Data/"+f"inf_repdanos_{ID_event}.json","r") as json_file: ###____________
                            results_rep = json.load(json_file) 
                    
                        results_rep[1]["n_imagenes"] = n_image
                        results_rep[1][f"input_fuente{n_image}"] = input_fuente
                        results_rep[1][f"input_ubicacion{n_image}"] = input_ubicacion


                        #with open(folder + '/Data/' + f"inf_repdanos_{ID_event}.json", 'w') as (file):
                        #    json.dump(results_rep, file)

                        #guardar imagen
                        files_saved_dr=0

                        # TO See details
                        
                        for image_file in image_files_damage_report:
                            file_details_damage = {"filename":image_file.name,"filetype":image_file.type,
                                            "filesize":image_file.size}
                            #st.write(file_details_damage)
                            st.image(load_image(image_file), width=250)

                            #Saving upload
                            with open(folder+"/Images/"+image_file.name,"wb") as f:
                                f.write((image_file).getbuffer())
                                files_saved_dr+=1
                            
                            for lt in range(len(image_file.type)):
                                if image_file.type[lt] =='/':
                                    type_file = image_file.type[lt+1:].upper()     
                            file =folder+"/Images/reporte_dano"+str(files_saved_dr)+"."+type_file
                            name_file = folder+"/Images/"+image_file.name
                            os.rename(name_file,file)                    
                            
                            results_rep[1][f"name_image{n_image}"] = f"reporte_dano{files_saved_dr}.{type_file}"
                            
                            
                            with open(folder + '/Data/' + f"inf_repdanos_{ID_event}.json", 'w') as (file):
                                json.dump(results_rep, file)
                            

                    

                    else:

                        datos_json = [{'n_mun':input_mun_rp,'dist_rep':input_dist_rp,"danos":input_danos,'fuente':input_fuente, 'autor':author_dr},{"n_imagenes":0,"name_image1":"i"}]

                        with open(folder + '/Data/' + f"inf_repdanos_{ID_event}.json", 'w') as (file):
                            json.dump(datos_json, file)

                        with open(folder+"/Data/"+f"inf_repdanos_{ID_event}.json","r") as json_file: ###____________
                            results_rep = json.load(json_file) 
                    
                        results_rep[1]["n_imagenes"] = n_image
                        results_rep[1][f"input_fuente{n_image}"] = input_fuente
                        results_rep[1][f"input_ubicacion{n_image}"] = input_ubicacion
                        
                        
                        
                        with open(folder + '/Data/' + f"inf_repdanos_{ID_event}.json", 'w') as (file):
                            json.dump(results_rep, file)

                    
                    st.markdown("***Después de ingresar la información cargue la siguiente imagen.***")
            
            
                

        

                
        
        if st.button("Guardar"):
            

            #Guardar datos
            if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_repdanos_{ID_event}.json") == True:
                    with open(folder+"/Data/"+f"inf_repdanos_{ID_event}.json","r") as json_file: ###____________
                        results_rep = json.load(json_file) 
                    
                    
                    results_rep[0]["n_mun"] = input_mun_rp
                    results_rep[0]["dist_rep"] = input_dist_rp
                    results_rep[0]["danos"] = input_danos
                    results_rep[0]["fuente"] = input_fuente
                    
                    
                    author_dr2= ""
                    for author in author_dr:
                        author_dr2 += author+","
                    results_rep[0]["autor"] = author_dr2

                    with open(folder + '/Data/' + f"inf_repdanos_{ID_event}.json", 'w') as (file):
                        json.dump(results_rep, file)
                    if image_files_damage_report is not None:
                        n_image = len(image_files_damage_report)
            else:

                    datos_json = [{'n_mun':input_mun_rp,'dist_rep':input_dist_rp,"danos":input_danos,'fuente':input_fuente, 'autor':author_dr},{"n_imagenes":0,"name_image1":"i"}]

                    with open(folder + '/Data/' + f"inf_repdanos_{ID_event}.json", 'w') as (file):
                        json.dump(datos_json, file)

           

            st.experimental_rerun()

    if option == "Efectos de la naturaleza":

        #Efectos de la naturaleza
        st.header("""Efectos en la naturaleza""")

        st.markdown("** Efectos reportados **")



        input_tipo = st.text_area("Ingrese el tipo de efecto.")
        input_desc = st.text_area("Ingrese la descripción del efecto.")

        if st.button("Guardar efectos"):

            if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_efectos_{ID_event}.json") == True:
                    with open(folder+"/Data/"+f"inf_efectos_{ID_event}.json","r") as json_file: ###____________
                        results_EN = json.load(json_file)   
                    

                    results_EN[1]["n_efectos"]= results_EN[1]["n_efectos"]+1
                    print(results_EN[1]["n_efectos"])

                    with open(folder + '/Data/' + f"inf_efectos_{ID_event}.json", 'w') as (file3):
                        json.dump(results_EN, file3)
            else:
                with open(folder + '/Data/' + f"inf_efectos_{ID_event}.json", 'w') as (file3):
                    estructura_efectos = [{"fuente_inf":"","quien_reviso":""},{f"n_efectos":1,"tipo_efecto1":input_tipo,"desc_efecto1":input_desc}]
                    json.dump(estructura_efectos, file3)
                    
            st.experimental_rerun()

        st.markdown("________")

        input_fuente = st.text_area("Ingrese la fuente de la información.")


        
        author1 = ["V. Dionisio", "R. Bolaños", "M. Lizarazo", "E. Mayorga","O. Mercado", "E. Poveda", "P. Predaza", "D. Siervo"]
        #Actualización de lista de autores
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_efectos_{ID_event}.json") == True:
            with open(folder+"/Data/"+f"inf_efectos_{ID_event}.json","r") as json_file: ###____________
                results_EN = json.load(json_file)   
            author = []
            revisado = results_EN[0]['quien_reviso'].split(",")
            for a in author1:
                if a not in revisado:
                    author.append(a)

        else:
            author = author1
        ##

        author_ip = st.multiselect("Quien revisó", author,key="<Aut_ip>")

        


        image_files_effect_on_nature=st.file_uploader("Sube la imagen aquí", type =["png", "jpg","jpeg"], key ="<Natures_Effects>",accept_multiple_files=True)

        


        if st.button("Guardar"):
            files_saved_ef=0
            if image_files_effect_on_nature is not None:
                    # TO See details
                for image_file_EF in image_files_effect_on_nature:
                    file_details_effect = {"filename":image_file_EF.name,"filetype":image_file_EF.type,
                                    "filesize":image_file_EF.size}
                    #st.write(file_details_effect)
                    st.image(load_image(image_file_EF), width=250)
                    #Saving upload
                    with open(os.path.join(main_path+'/Images/',image_file_EF.name),"wb") as f:
                        f.write((image_file_EF).getbuffer())
                        files_saved_ef+=1
                    
                    for lt in range(len(image_file_EF.type)):
                        if image_file_EF.type[lt] =='/':
                            type_file = image_file_EF.type[lt+1:].upper()     
                    file = main_path+"/Images/image_file_effects_nature"+str(files_saved_ef)+"."+type_file
                    name_file = main_path+"/Images/"+image_file_EF.name
                    os.rename(name_file,file)
        
    
    if option == "Sismicidad historica":
        #Sismicidad historica

        
        input_historic = st.text_area(""" Por favor ingrese las observaciones de la sismicidad histórica de la zona del evento""","", key="<Obs_historic>")
        st.write('Sus observaciones son:', input_historic)
    
    st.sidebar.write("____________________________")
    #Creacion PDF
    if st.sidebar.button("Crear PDF"):
        #try:
        

        mkPDF.mkPDF_report(ID_event)
        st.sidebar.success("Creado!")
        #except:
        #    st.write("No se ha podido generar el PDF")
        #    pass
            
        try:
            shutil.copy("Reporte_Sismo_Destacado.pdf", main_path+"/Reporte_Sismo_Destacado.pdf" )
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
                st.sidebar.success("ya existe un reporte del Evento desea re-escribirlo")
                if st.button("re-escribirlo"):
                    rm(main_path+"/Reporte_Sismo_Destacado.pdf")
                    shutil.copy("Reporte_Sismo_Destacado.pdf",main_path+"/Reporte_Sismo_Destacado.pdf" )
                if st.button("Cancelar"):
                    pass
                raise


    #descargar
    if os.path.exists(main_path+"/Reporte_Sismo_Destacado.pdf") == True:
        with open(main_path+"/Reporte_Sismo_Destacado.pdf", "rb") as file:
            btn = st.sidebar.download_button(label="Descargar PDF", data=file, file_name=f"{ID_event}_Reporte.pdf", mime="application/octet-stream")
main()

