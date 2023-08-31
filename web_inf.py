from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
from time import sleep
from PIL import Image
import pandas as pd
import numpy as np
import requests
import json
import os

id2 = ""    
#id2 = 'SGC2022tmqchk'
#id2 = 'SGC2022dugzug'
#id2 = "SGC2022scjdwq"
#id2 = "SGC2022sniasj"
#id2 = "SGC2022sniasj"

download_fol = '/home/jsoriano'

class Reporte:

    def __init__(self, id, download_folder):

        self.download_folder = download_folder
        self.id = id
        
        try:

            ##Firefox
            options = Options()
            options.add_argument('--headless')
            
            #configuración para Descarga
            fp = webdriver.FirefoxProfile()
            fp.set_preference('browser.download.folderList', 2)
            fp.set_preference('browser.download.manager.showWhenStarting', False)
            fp.set_preference('browser.download.dir', download_folder)
            fp.set_preference('browser.helperApps.neverAsk.saveToDisk', "'application/force-download','application/vnd.google-earth.kml+xml','application/xml','text/csv','text/xml'")
            fp.set_preference('browser.download.useDownloadDir', True)
            fp.set_preference('browser.download.viewableInternally.previousHandler.alwaysAskBeforeHandling.xml', False)
            fp.set_preference('browser.download.viewableInternally.previousHandler.preferredAction.xml', 0)
            fp.set_preference('browser.download.viewableInternally.typeWasRegistered.xml', True)
            self.driver = webdriver.Firefox(firefox_profile=fp, options=options)

            
        except:

            ##Chrome
            
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')

            #configuración para Descarga
            prefs = {"profile.default_content_settings.popups":0,"download.default_directory" : download_folder, "directory_upgrade": True}
            options.add_experimental_option("prefs",prefs)
            self.driver = webdriver.Chrome(options=options)

    #Informacion general
    def inf_general(self):

        try:

            driver = self.driver
            id = self.id
            download_folder = self.download_folder
            
            #Extraccion de datos
            fuente = f"https://www.sgc.gov.co/detallesismo/{id}/resumen"
            fuente_sentidos = f"https://sismosentido.sgc.gov.co/EvaluacionIntensidadesServlet?id_sismo={id}&metodo=verSalidas"
            driver.get(fuente)
            sleep(2)
            fecha_hora_utc = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div/div[2]/main/div[2]/div[1]/div[2]/p[5]/span[2]').text
            fecha_hora_local = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div/div[2]/main/div[2]/div[1]/div[2]/p[2]/span[2]').text
            localizacion = driver.find_element(by=By.XPATH, value='//*[@id="container-resumen-1"]/div[2]/div[2]/table/tbody/tr[2]/td').text
            latitud, longitud = localizacion.split(',')
            profundidad = driver.find_element(by=By.XPATH, value='//*[@id="container-resumen-1"]/div[2]/div[2]/table/tbody/tr[3]/td').text
            magnitud = driver.find_element(by=By.XPATH, value='//*[@id="container-resumen-1"]/div[2]/div[2]/table/tbody/tr[4]/td').text
            ubi = driver.find_elements(by=By.TAG_NAME, value='h2')
            ubicacion = ubi[1].text
            

            datos = [fecha_hora_utc, fecha_hora_local, latitud, longitud, profundidad, magnitud, ubicacion, fuente]
            observ = ''
            quien = ''
            
            #Creacion de Json
            datos_json = [{'inf_general':datos,'observaciones':observ,'quien_reviso':quien}]
            with open(download_folder + '/Data/' + f"inf_general_{id}.json", 'w') as (file):
                json.dump(datos_json, file)
            
            #Mapa
            #try:
            #Mapa opcion1 cuando funciona la url del mapa, usando verify=False

            url_map = requests.get(driver.find_element(by=By.XPATH, value='//*[@id="container-resumen-1"]/div[2]/div[1]/img').get_attribute("src"), verify=False)
            nombre_map = f"Mapc_{id}.gif"
            open(download_folder + '/Images/' + nombre_map, 'wb').write(url_map.content)
            im = Image.open(os.path.join(download_folder + '/Images', nombre_map))
            im = im.crop((15, 224, 658, 845))
            im.save(os.path.join(download_folder + '/Images', f"Mapc_{id}.gif"))

            #except:
            """
            #Mapa opcion2 con screenshot para cuando la url del mapa no funciona
            nombre_map = f"Map_{id}.png"
            url = driver.find_element(by=By.XPATH, value='//*[@id="container-resumen-1"]/div[2]/div[1]/img').get_attribute("src")
            driver.get(url)
            driver.save_screenshot(download_folder+f"/Images/"+nombre_map)

            im = Image.open(os.path.join(download_folder + '/Images', nombre_map))
            im = im.crop((180, 145,600, 553))
            im.save(os.path.join(download_folder + '/Images', f"Mapc_{id}.png"))
            os.system('rm ' + download_folder + '/Images/' + nombre_map) 
            """

            return True

        except:

            return False
            print(f"\t\t El id {id} no existe")

    #Mecanismo focal
    def inf_mecanismofocal(self):

        try:

            driver = self.driver
            id = self.id
            download_folder = self.download_folder

            fuente = f"https://www.sgc.gov.co/detallesismo/{id}/tm"
            driver.get(fuente)
            sleep(2)

            #Planos nodales
            pl1 = driver.find_elements(by=By.XPATH, value="//*[@class= 'tabla1']/div/table/tbody/tr[1]/td")
            pl2 = driver.find_elements(by=By.XPATH, value="//*[@class= 'tabla1']/div/table/tbody/tr[2]/td")

            strike1 = round(float(pl1[1].text), 2)
            dip1 = round(float(pl1[2].text), 2)
            rake1 = round(float(pl1[3].text), 2)

            strike2 = round(float(pl2[1].text), 2)
            dip2 = round(float(pl2[2].text), 2)
            rake2 = round(float(pl2[3].text), 2)
            
            #Metodologia
            metodologia = driver.find_element(by=By.XPATH, value='//*[@id="full-width-tab-0"]/span[1]').text
            metodologia_min = metodologia.lower()
            inf_metodologia = {'SCMTV':'SCMTV (modulo de SeisComP3 (Minson & Dreger, 2008))',  'SWIFT':'SWIFT (Source parameter determination based on Waveform Inversion of Fourier Transformed seismograms), propuesta por Nakano et al. (2008)', 
                'ISOLA':'ISOLA (Software  desarrollado en Fortran para tensor de momento (J. Zahradnik y E. Sokos,  2003))', 
                'PHASEW':'PHASEW()'}
            informacion = inf_metodologia[metodologia]
            
            datos = [strike1, dip1, rake1, strike2, dip2, rake2,metodologia_min, informacion, fuente]
            observ = ''
            quien = ''
            tipo = ''
            
            #Creacion de Json
            datos_json = [{'inf_mecanismofocal':datos,'observaciones':observ,'quien_reviso':quien,'tipo_f':tipo}]
            with open(download_folder + '/Data/' + f"inf_mecanismofocal_{id}.json", 'w') as (file):
                json.dump(datos_json, file)

            #Pelota de playa
            #try:
            #Enlace de la pelota de plalla de la pagina
            url_ball = requests.get(driver.find_element(by=By.XPATH, value='//*[@id="tmpPanel0"]/div/div/div/div[2]/div/div[2]/div/img').get_attribute("src"), verify=False) #enlace
            #except:
            
            #Pelota de playa 2 usando enlace de la pelota de la base de datos
            #url_ball = requests.get(f"http://bdrsnc.sgc.gov.co/sismologia1/sismologia/focal_seiscomp_3/events_seiscomp3/events/{id[3:7]}//{id}/mt/{metodologia_min}/beachball.png")
            
            nombre_ball = f"ball_{metodologia_min}_{id}.png"
            open(download_folder + '/Images/' + nombre_ball, 'wb').write(url_ball.content)
            
            #Pelota de playa 3 cuando con la url no funciona, tomando pantallaso
            ##nombre_ball = f"ball_{metodologia_min}_{id}.png"
            ##url = driver.find_element(by=By.XPATH, value='//*[@id="tmpPanel0"]/div/div/div/div[2]/div/div[2]/div/img').get_attribute("src")
            ##driver.get(url)
            ##driver.save_screenshot(download_folder+f"/Images/"+nombre_ball)
            #cup
            ##im = Image.open(os.path.join(download_folder + '/Images', nombre_ball))
            ##im = im.crop((300, 200,500, 423))
            ##im.save(os.path.join(download_folder + '/Images', nombre_ball))
            #os.system('rm ' + download_folder + '/Images/' + nombre_map)


            return True

        except:

            return False
            print('\t\t No existe Mecanismo focal para este evento')

    #Valores de aceleracion
    def inf_aceleracion(self):

        try:

            driver = self.driver
            id = self.id
            download_folder = self.download_folder

            fuente = f"https://www.sgc.gov.co/detallesismo/{id}/sm"
            driver.get(fuente)
            sleep(2)

            tab_ac = driver.find_element(by=By.XPATH, value='//*[@id="scrollable-auto-tabpanel-0"]/div/div/div/div/div[1]/div[2]/button[2]/span[1]').click()
            sleep(2)
            os.system(f"mv {download_folder}/tableDownload.csv {download_folder}/Tables/aceleracion_{id}.csv")

            #Extraccion de datos
            tab = pd.read_csv(f"{download_folder}/Tables/aceleracion_{id}.csv")

            tab = tab.sort_values('PGA EW(cm/s^2)', ascending=False)
            #tab = tab.sort_index()
            #print(tab)
            ##Estación más cercana
            in_min_dist = tab['Dist.Epi(km)'].idxmin()

            codigo1 = tab.loc[in_min_dist]['Código']
            nombre_estacion_min = tab.loc[in_min_dist]['Nombre Estación']
            estacion_min1 = tab.loc[in_min_dist]['Código']
            dist_epi1 = int(tab.loc[in_min_dist]['Dist.Epi(km)'])
            dist_hip1 = int(tab.loc[in_min_dist]['Dist.Hip(km)'])
            ac_ew1 = round(float(tab.loc[in_min_dist]['PGA EW(cm/s^2)']), 2)
            ac_ns1 = round(float(tab.loc[in_min_dist]['PGA NS(cm/s^2)']), 2)
            ac_z1 = round(float(tab.loc[in_min_dist]['PGA Z(cm/s^2)']), 2)
            ac_mx_h1 = round(((ac_ew1**2 + ac_ns1**2)/2)**0.5, 2)
            gr1 = round((ac_mx_h1/980)*100, 2)

            datos1 = [nombre_estacion_min, codigo1, dist_epi1, dist_hip1, ac_ew1, ac_ns1, ac_z1, ac_mx_h1, gr1]
            
            ##Aceleracion maxima
            
            in_max_ac = tab['PGA EW(cm/s^2)'].idxmax()

            codigo2 = tab.loc[in_max_ac]['Código']
            nombre_estacion_max = tab.loc[in_max_ac]['Nombre Estación']
            dist_epi2 = int(tab.loc[in_max_ac]['Dist.Epi(km)'])
            dist_hip2 = int(tab.loc[in_max_ac]['Dist.Hip(km)'])
            ac_ew2 = round(float(tab.loc[in_max_ac]['PGA EW(cm/s^2)']), 2)
            ac_ns2 = round(float(tab.loc[in_max_ac]['PGA NS(cm/s^2)']), 2)
            ac_z2 = round(float(tab.loc[in_max_ac]['PGA Z(cm/s^2)']), 2)
            ac_mx_h2 = round(((ac_ew2**2 + ac_ns2**2)/2)**0.5, 2)
            gr2 = round((ac_mx_h2/980)*100, 2)
            
            datos2 = [nombre_estacion_max, codigo2, dist_epi2, dist_hip2, ac_ew2, ac_ns2, ac_z2,ac_mx_h2, gr2,fuente]
            observ = ""
            quien = ""
            
            #Segunda Aceleracion maxima
            if nombre_estacion_min == nombre_estacion_max:
                ##Estación más cercana
                #in_min_dist = tab['Dist.Epi(km)'].idxmin()
                codigo1 = tab.loc[1]['Código']
                nombre_estacion_min = tab.loc[1]['Nombre Estación']
                estacion_min1 = tab.loc[1]['Código']
                dist_epi1 = int(tab.loc[1]['Dist.Epi(km)'])
                dist_hip1 = int(tab.loc[1]['Dist.Hip(km)'])
                ac_ew1 = round(float(tab.loc[1]['PGA EW(cm/s^2)']), 2)
                ac_ns1 = round(float(tab.loc[1]['PGA NS(cm/s^2)']), 2)
                ac_z1 = round(float(tab.loc[1]['PGA Z(cm/s^2)']), 2)
                ac_mx_h = round(((ac_ew1**2 + ac_ns1**2)/2)**0.5, 2)
                gr = round((ac_mx_h/980)*100, 2)

                datos1 = [nombre_estacion_min, codigo1, dist_epi1, dist_hip1, ac_ew1, ac_ns1, ac_z1, ac_mx_h, gr]
	
            datos_ac = [datos1, datos2]				            

            #Creacion de Json
            datos_json = [{'inf_aceleracion':datos_ac,'observaciones':observ,'quien_reviso':quien, 'datos3':[], 'datos4':[]}]
            with open(download_folder + '/Data/' + f"inf_aceleracion_{id}.json", 'w') as (file):
                json.dump(datos_json, file)

            #Mapa
            driver.set_window_size(1350, 1800)
            driver.get(f"https://www.sgc.gov.co/detallesismo/{id}/sm")
            sleep(2)
            tab_ac = driver.find_element(by=By.XPATH, value='//*[@id="scrollable-auto-tab-3"]/span[1]').click()
            sleep(3)
            mapa = driver.find_element(by=By.XPATH, value='//*[@id="interactive_map"]')
            
            
            #recorte de mapa
            location = mapa.location
            size = mapa.size
            zoom = driver.find_element(by=By.XPATH, value='//*[@id="interactive_map"]/div[2]/div[2]/div[2]/a[2]').click()
            
            sleep(2)
            driver.save_screenshot(download_folder +'/Images/mapa_ac.png')
            x = location['x']
            y = location['y']
            width = location['x'] + size['width']
            height = location['y'] + size['height']
            
            im = Image.open(download_folder+'/Images/mapa_ac.png')
            im = im.crop((int(x)+350, int(y)+175, int(width)-350, int(height)))
            im.save(download_folder+f"/Images/map_ac_{id}.png")
            os.system('rm ' + download_folder +'/Images/mapa_ac.png')
            
            return True

        except:

            return False
            print('\t\t No existe Valores de aceleracion para este evento')

    #Intensidad instrumental
    def inf_instrumental(self):

        try:

            driver = self.driver
            id = self.id
            download_folder = self.download_folder
            
            descripcion_int = 'Mapa que muestra el movimiento del terreno por niveles de intensidad y los posibles efectos causados por el sismo,generado de la combinación de registros en sismómetros, acelerógrafos, relaciones de atenuación de la energía sísmica e información sobre condiciones sísmicas locales.'
            escala = 'Mercalli modificada (MMI)'
            
            #Extraccion de datos
            file = requests.get(f"https://archive.sgc.gov.co/events/{id}/mmi/grid.xml")
            
            if file.content[len(file.content)-6:len(file.content)-1] == b'Error':
                
                file = requests.get(f"https://xylon.sgc.gov.co/eqevents/events/{id[3:7]}/{id}/mmi/grid.xml", verify=False)
                
            else:
                
                file = requests.get(f"https://archive.sgc.gov.co/events/{id}/mmi/grid.xml")

            
            open(download_folder + '/Tables/grid.xml', 'wb').write(file.content)
            os.system(f"mv {download_folder}/Tables/grid.xml {download_folder}/Tables/instrumental_{id}.xml")

            grid = open(download_folder + f"/Tables/instrumental_{id}.xml", 'r').readlines()
            p_grid = {}
            long, lat, intensidad, pga, pgv = ([], [], [], [], [])
            for e in grid:
                if e[0] != '<':
                    ev = e.split()
                    long.append(float(ev[0]))
                    lat.append(float(ev[1]))
                    intensidad.append(float(ev[2]))
                    pga.append(float(ev[3]))
                    pgv.append(float(ev[4]))

            p_grid['longitud'] = long
            p_grid['latitud'] = lat
            p_grid['intensidad'] = intensidad
            p_grid['pga'] = pga
            p_grid['pgv'] = pgv
            grilla = pd.DataFrame(p_grid)
            
            intensidad_max = grilla['intensidad'].max()
            pga_max = grilla['pga'].max()
            pgv_max = grilla['pgv'].max()
            romanos = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI']
            
            int_max_romano = romanos[(int(round(intensidad_max, 0)) - 1)]
            mov = ['No Sentido', 'Debil', 'Debil', 'Ligero', 'Moderado', 'Fuerte', 'Muy Fuerte', 'Severo', 'Violento', 'Extremo']
            da = ['Nunguno', 'Ninguno', 'Ninguno', 'Ninguno', 'Muy Poco', 'Poco', 'Moderado', 'Moderado/Mucho', 'Mucho', 'Cuantioso']
            movimiento = mov[(int(round(intensidad_max, 0)) - 1)]
            dano = da[(int(round(intensidad_max, 0)) - 1)]
            fuente = f"https://archive.sgc.gov.co/events/{id}/mmi"
            
            datos = [int_max_romano, movimiento, dano, round(float(pga_max), 2), round(float(pgv_max), 2),fuente]
            observ = ""
            quien = ""

            #Creacion de Json
            datos_json = [{'inf_instrumental':datos,'observaciones':observ,'quien_reviso':quien}]
            with open(download_folder + '/Data/' + f"inf_instrumental_{id}.json", 'w') as (file):
                json.dump(datos_json, file)

            #mapa
            mapa = requests.get(f"{fuente}/intensity.jpg")
            if mapa.content[len(mapa.content)-6:len(mapa.content)-1] == b'Error':
                
                map_intensidad = requests.get(f"https://xylon.sgc.gov.co/eqevents/events/{id[3:7]}/{id}/mmi/intensity.jpg", verify=False)
                
            else:
                
                map_intensidad = requests.get(f"{fuente}/intensity.jpg")

            open(download_folder + f"/Images/map_intensity_{id}.jpg", 'wb').write(map_intensidad.content)
            
            return True
        
        except:
            
            return False
            print('\t\t No existe Intensidad Instrumental para este evento')

    #Intensidad percibida (macrosísmica)
    def inf_intpercibida(self):

        try:

            driver = self.driver
            id = self.id
            download_folder = self.download_folder

            #Extracción de datos en formato .xlsx,    
            #se puede en .csv  directamente desde la pagina pero ahí tiene un error en los valores de intensidad
            file = requests.get(f"https://sismosentido.sgc.gov.co/EvaluacionIntensidadesServlet?metodo=tablaRespuestasXLS&idSismo={id}")
            open(download_folder + f"/Reportes_Intpercibida_{id}.xlsx", 'wb').write(file.content)

            tit = ['Centro poblado', 'Municipio', 'Intensidad', 'No. formularios', 'Distancia al hipocentro', 'Latitud', 'Longitud']
            #tit = ['Centro poblado', 'Municipio', 'Intensidad', 'No. formularios', 'Distancia al hipocentro', 'Latitud', 'Longitud', '.', '.', '.', '.']
            int_rep = ['Apenas \nsentido', 'Sentido \nlevemente', 'Sentido \nampliamente', 'Sentido \nfuertemente', 'Daño \nleve', 'Daño \nmoderado', 'Daño \nsevero']

            tab_i = pd.read_excel(download_folder + f"/Reportes_Intpercibida_{id}.xlsx")
            tab_i = tab_i.drop(tab_i.index[[0, 1, 2, 3, 4, 5, 6]])
            tab_i.columns = tit

            #Numero de reportes recibidos
            n_reportes = int(pd.to_numeric((tab_i['No. formularios']), errors='coerce').sum())
            #Numero de centros poblados
            n_centros_poblados = int(tab_i['Centro poblado'].count())
            munic = []
            for mun in tab_i['Municipio']:
                if mun not in munic:
                    munic.append(mun.title())

            #Numero de municipios
            n_municipio = len(munic)
            l_dep = []
            for i in tab_i['Municipio']:
                if i != 'Municipio':
                    d = i.split(',')
                    l_dep.append(d[1])
            #Numero de departamentos
            n_departamentos = len(set(l_dep))
            #Intensidad maxima
            int_maxima = int(tab_i['Intensidad'].max())

            #Intensidad Maxima reportada
            if int_maxima in (2, 3, 4, 5, 6, 7):
                intensidad_reportada = int_rep[(int_maxima - 2)]
            if int_maxima > 7:
                intensidad_reportada = 'Daño \nsevero'

            in_int_max = list(tab_i['Intensidad']).index(str(tab_i['Intensidad'].max()))

            #Centros poblados donde se reportó la intensidad máxima
            centro_poblado_max = tab_i.loc[(in_int_max + 7, 'Centro poblado')].title().strip(",")
            
            municipio_max = tab_i.loc[(in_int_max + 7, 'Municipio')].title().strip(",")

            #Municiíos con mayor número de reportes
            n_form = map(int, list(tab_i['No. formularios']))
            n_form_s = sorted(list(n_form))
            n_form_m = map(str, n_form_s[len(n_form_s) - 6:len(n_form_s)])
            in_form_max = map(list(tab_i['No. formularios']).index, list(n_form_m))
            mun_rep_max = ''
            for e in in_form_max:
                mun_rep_max += tab_i.loc[(e + 7, 'Centro poblado')] + ', '

            mun_rep_max = mun_rep_max.title().strip(", ")

            #Centros poblados más alejados del hipocentro donde fue reportado como sentido el sismo
            po_alejados = map(float, list(tab_i['Distancia al hipocentro']))
            po_alejados_s = sorted(list(po_alejados))
            po_alejados_m = map(str, po_alejados_s[len(po_alejados_s) - 3:len(po_alejados_s)])
            in_alejados_max = map(list(tab_i['Distancia al hipocentro']).index, list(po_alejados_m))
            poblados_alejados_max = ''
            for e in in_alejados_max:
                poblados_alejados_max += tab_i.loc[(e + 7, 'Centro poblado')] + ', '

            poblados_alejados_max = poblados_alejados_max.title().strip(", ")
            fuente = f"https://www.sgc.gov.co/detallesismo/{id}/cdi"

            datos = [n_reportes, n_centros_poblados, n_municipio, n_departamentos, int_maxima, intensidad_reportada, centro_poblado_max, municipio_max, mun_rep_max, poblados_alejados_max,fuente]
            print(datos)
            descrip_im = ""
            sentido_otros_paises = ""
            replicas_sentidas = ""
            quien = ""

            #Creacion de Json
            datos_json = [{'inf_intpercibida':datos,'quien_reviso':quien, 'descr_im':descrip_im, 'sent_otros_paises':sentido_otros_paises,'replicas_sentidas':replicas_sentidas}]
            with open(download_folder + '/Data/' + f"inf_intpercibida_{id}.json", 'w') as (file):
                json.dump(datos_json, file)

            #Histograma número de sitios Vs intensidad
            apenas_sentido = list(tab_i['Intensidad']).count('2')
            sentido_levemente = list(tab_i['Intensidad']).count('3')
            sentido_ampliamente = list(tab_i['Intensidad']).count('4')
            sentido_fuertemente = list(tab_i['Intensidad']).count('5')
            dano_leve = list(tab_i['Intensidad']).count('6')
            dano_moderado = list(tab_i['Intensidad']).count('7')
            dano_severo = list(tab_i['Intensidad']).count('8')
            fig, ax = plt.subplots(figsize=(8, 5), dpi=100)

            ejx = int_rep
            ejy = [apenas_sentido, sentido_levemente, sentido_ampliamente, sentido_fuertemente, dano_leve, dano_moderado, dano_severo]

            ##Fuente
            #font_path = f'{os.path.dirname(os.path.abspath(__file__))}/fonts/Aller'
            font_prop1 = font_manager.FontProperties(size=15)
            font_prop2 = font_manager.FontProperties(size=12)
            ##Histograma
            plt.bar(ejx, ejy, align='center', width=0.4, color=['#d9d9f5', '#a0d3ff', '#02fffd', '#00fa00', '#ffff01', '#ffa901', '#fe0000'])
            plt.title('Histograma número de sitios Vs intensidad\n\n\n', fontproperties=font_prop1)
            index = np.arange(len(ejy))
            plt.xticks(index, ejx, fontproperties=font_prop2)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.get_yaxis().set_visible(False)
            for e in range(len(int_rep)):
                plt.text(e, (ejy[e] + 5), (str(ejy[e])), ha='center', fontproperties=font_prop2)

            fig.tight_layout()
            plt.savefig(f"{download_folder}/Images/histo_int_percibida_{id}.png", format='png', dpi=100)

            #Mapa
            driver.set_window_size(1350, 1800)
            driver.get(fuente)
            sleep(2)

            try:

                mapa = driver.find_element(by=By.XPATH, value='//*[@id="map-cdi"]')
                location = mapa.location
                size = mapa.size

                driver.save_screenshot(download_folder+ '/Images/mapa_int_perc.png')
                x = location['x']
                y = location['y']
                width = location['x'] + size['width']
                height = location['y'] + size['height']

                ##Corte
                im = Image.open(download_folder+'/Images/mapa_int_perc.png')
                im = im.crop((int(x)+350, int(y)+175, int(width)-350, int(height)))
                im.save(download_folder+ f"/Images/map_int_perc_{id}.png")
                os.system('rm ' + download_folder  + '/Images/mapa_int_perc.png')

            except:
                try: 
                    fuente_sentidos = f"https://sismosentido.sgc.gov.co/EvaluacionIntensidadesServlet?id_sismo={id}&metodo=verSalidas"
                    driver.get(fuente_sentidos)
                    sleep(2)

                    mapa = driver.find_element(by=By.XPATH, value='//*[@id="map_gc"]')
                    location = mapa.location
                    size = mapa.size

                    driver.save_screenshot(download_folder+ '/Images/mapa_int_perc.png')
                    x = location['x']
                    y = location['y']
                    width = location['x'] + size['width']
                    height = location['y'] + size['height']

                    ##Corte
                    im = Image.open(download_folder+'/Images/mapa_int_perc.png')
                    im = im.crop((int(x)+350, int(y)+175, int(width)-350, int(height)))
                    im.save(download_folder+ f"/Images/map_int_perc_{id}.png")
                    os.system('rm ' + download_folder  + '/Images/mapa_int_perc.png')                
                
				
                except:
                    fuente_sentidos = f"https://sismosentido.sgc.gov.co/EvaluacionIntensidadesServlet?id_sismo={id}&metodo=verSalidas"
                    driver.get(fuente_sentidos)
                    sleep(2)

                    mapa = driver.find_element(by=By.XPATH, value='//*[@id="map_gc"]')
                    location = mapa.location
                    size = mapa.size

                    driver.save_screenshot(download_folder+ '/Images/mapa_int_perc.png')
                    x = location['x']
                    y = location['y']
                    width = location['x'] + size['width']
                    height = location['y'] + size['height']

                    ##Corte
                    im = Image.open(download_folder+'/Images/mapa_int_perc.png')
                    
                    im = im.crop((int(x)+140, int(y), int(width)-150, int(height)))
                    im.save(download_folder+ f"/Images/map_int_perc_{id}.png")
                    os.system('rm ' + download_folder  + '/Images/mapa_int_perc.png')  
                    #error = "no hay mapa de intensidad percibida"
                    #os.system(f"cp {download_folder[0:len(download_folder)-20]}PDF_Images/nomap.png {download_folder}/Images/")
                    #os.system(f"mv {download_folder}/Images/nomap.png {download_folder}/Images/map_int_perc_{id}.png")

            return True
        
        except:
            return False
            print('\t\t No existe Intensidad percibida para este evento')

reporte = Reporte(id2, download_fol)
print(reporte.inf_aceleracion())
