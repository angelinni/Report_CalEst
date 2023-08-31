import streamlit as st
import json
import os
import pandas as pd
import glob, os.path
from datetime import date, datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DayLocator, HourLocator, MinuteLocator, DateFormatter
from matplotlib.patches import Rectangle
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import matplotlib.patches as patches
import numpy as np
#import seaborn as sns

import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from bokeh.plotting import figure




class Plot():
    
    def __init__(self, estacion,sensor, fecha_ini,fecha_fin, download_folder):

        self.folder = download_folder
        self.estacion = estacion
        self.sensor = sensor
        self.fecha_ini = fecha_ini
        self.fecha_fin = fecha_fin
    
    ##Graficar Calidad de Estaciones
    def graf_est(self):
        
        
        
        folder = self.folder
        estacion = self.estacion
        sensor = self.sensor
        fecha_ini = self.fecha_ini
        fecha_fin = self.fecha_fin 

        st.header("""Datos disponibilidad, offset,gaps, picos, ppsd""")
        ##función para plotear canal y llamarlo en la tabla de cada componente
        def plot_Cal(estacion,sensor,fecha_ini, fecha_fin, list_est,can):

            #if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Datos/{estacion}*") == True:
            if len(list_est) !=0:
                
                
                df_est = pd.read_csv(list_est[0])
                #st.dataframe(df_est)
                
                #filtro de tiempo
                
                #Cambio de formato de fecha a datetime
                f_date = []
                for e in df_est["fecha"]:
                    year, month, day = e.split("-")
                    f_date.append(datetime(int(year),int(month),int(day)))
                
                #Cambio de formato de fecha times_gaps a datetime
                df_est["fecha"] = f_date
                
                f_date_gap = []
                f_date_gap_graf = []
                f_date_gap_graf_din = []
                for te, dis, fe in zip(df_est["times_gaps"], df_est["disponibilidad"], df_est["fecha"]):
                    
                    
                    if float(dis) == 0.0:
                        f_date_gap.append([[datetime(fe.year,fe.month,fe.day,0,0,0,0),3600*24]])
                        
                        f_date_gap_graf.append([[datetime(fe.year,fe.month,fe.day,0,0,0,0),3600*24]])
                        f_date_gap_graf_din.append([[datetime(fe.year,fe.month,fe.day,0,0,0,0),datetime(fe.year,fe.month,fe.day,23,59,59)]])


                    if len(te) != 2:
                        t_gaps = te.split("_")

                        gaps_dia = []    
                        gaps_dia_din = []                
                        for t in t_gaps:

                            if len(t) != 0:
                                y_g, mo_g, d_g, h_g, mi_g, s_g, ms_g, del_g = t.split("-")
                                gaps_dia.append([datetime(int(y_g),int(mo_g),int(d_g),int(h_g),int(mi_g),int(s_g),int(ms_g)),float(del_g)])
                                gaps_dia_din.append([datetime(int(y_g),int(mo_g),int(d_g),int(h_g),int(mi_g),int(s_g),int(ms_g)),datetime(int(y_g),int(mo_g),int(d_g),int(h_g),int(mi_g),int(s_g),int(ms_g))+timedelta(seconds=float(del_g))])


                        f_date_gap.append(gaps_dia)
                        f_date_gap_graf.append(gaps_dia)
                        f_date_gap_graf_din.append(gaps_dia_din)
                    
                    elif len(te) == 2 and dis != 0.0:
                        #f_date_gap.append([[datetime(fe.year,fe.month,fe.day,0,0,0,0),0]])
                        f_date_gap.append([[[],[]]])
                        f_date_gap_graf_din.append([[[],[]]])
                        
                
                #st.write(f_date_gap_graf_din)
                #remontar fechas con datetime
                df_est["times_gaps"]= f_date_gap
                

                #cree una nueva columna para los datos de tiempos de gaps para el mapa dinamico
                df_est["times_gaps_graf_din"]= f_date_gap_graf_din
                

                   
                
                #filtro por fechas seleccionadas
                filtro_fecha = (df_est["fecha"] >= fecha_ini) & (df_est["fecha"] <= fecha_fin) 
                fil_time = df_est[filtro_fecha]
                
                #st.dataframe(fil_time[" times_gaps"])
                
                
                
                #GRAFICAR
                
                del_time_m=(fecha_fin-fecha_ini).total_seconds()/60/60/24/30  #en meses
                dias_ad=int(round((4*del_time_m)-3 ,0 ) ) #al hacerce mas larga la grafica, debe adicionar mas dias para construir columna de calor (para que se vea)
                
                if dias_ad <= 0:
                    dias_ad=1
                
                
                #-----GRAFICA DISPONIBILIDAD
                
                #fil_time[" disponibilidad"] = fil_time[" disponibilidad"].astype(float)
                fil_time["disponibilidad"] = list(map(lambda x: float(x), fil_time["disponibilidad"]))
                
                lista_disponibilidad_sin_nueves=[] #es posible que no haya podido leer un mseed por tanto escribio un -9
                for di in fil_time["disponibilidad"]:
                    if di != -9:
                        lista_disponibilidad_sin_nueves.append(di)

                fil_time2 = fil_time[(fil_time["disponibilidad"] != -9)]
                min_dis = fil_time2["disponibilidad"].min()             #minima desponibilidad
                max_dis = fil_time2["disponibilidad"].max()             #maxima disponibilidad
                prom_dis = fil_time2["disponibilidad"].mean()           #promedio disponibilidad
                
                #min_dis=round( min(lista_disponibilidad_sin_nueves),1 )
                #max_dis=round( max(lista_disponibilidad_sin_nueves),1 )
                #prom_dis=round( np.mean( np.array(lista_disponibilidad_sin_nueves) ),1 )
                
                


                tab1, tab2 = st.tabs(["otros","matplotlib"])
                with tab2:

                    col1,col2= st.columns([5,1.1])
                    with col1:
                        #Con Matplotlib
                        fig = plt.figure(figsize=(21., 11.))
                        ax = fig.add_subplot(311)
                        plt.plot(fil_time["fecha"],fil_time["disponibilidad"],linewidth=1,color='#0000ff',label="Disponibilidad",zorder=1000)
                        ax.set_ylabel('Disponibilidad \n (%)', color='k', fontsize=14)
                        ax.xaxis.grid(True, which='major')
                        ax.yaxis.grid(True, which='major')
                        ax.xaxis.set_tick_params(labelsize=9)
                        ax.set_xlim(list(fil_time["fecha"])[0]-timedelta(days=1), list(fil_time["fecha"])[-1]+timedelta(days=dias_ad))


                        #con este foorloop se selecciona en una lista solo los tiempos de gaps existentes
                        l_fil_tgap = []
                        for fil_time_gap in fil_time["times_gaps"]:
                            if len(str(fil_time_gap[0][0])) > 2 :
                                l_fil_tgap.append(fil_time_gap)
                        
                                
                        if len(l_fil_tgap) > 0:
                        
                            ax1 = ax.twinx()
                            f_i = datetime(fecha_ini.year,fecha_ini.month,fecha_ini.day)
                            f_f = datetime(fecha_fin.year,fecha_fin.month,fecha_fin.day,0,0,0,0)
                            ax1.vlines(f_i,0,0, lw=1, color="k",label="Gaps (tiempo)" )  
                            to_r=datetime(1,1,1,0,0,1)
                            rectangulo3 = patches.Rectangle( ( list(fil_time["fecha"])[-1], to_r ),timedelta(dias_ad),timedelta(hours=24),fill=True,facecolor='b',edgecolor='b',linewidth=0.2,alpha=0.6)
                            ax1.add_patch(rectangulo3)
                            
                            #para graficar los gaps existentes
                            for tg in l_fil_tgap:
                                for g in tg:
                                    tdia=datetime(g[0].year,g[0].month,g[0].day,12,0,0)
                                    to=datetime(1,1,1,g[0].hour,g[0].minute,g[0].second)
                                    ax1.text(tdia,to,"o",fontsize=7,alpha=0.8,zorder=100,horizontalalignment='center',verticalalignment='baseline')
                                    ax1.text(tdia,to+timedelta(seconds=g[1]),"x",fontsize=10,alpha=0.8,zorder=100,horizontalalignment='center',verticalalignment='baseline')
                                    rectangulo = patches.Rectangle( ( tdia-timedelta(seconds=int(g[1]/2)), to),timedelta(seconds=g[1]),timedelta(seconds=g[1]),fill=True,facecolor='k',edgecolor='k',linewidth=0.6,alpha=0.6, ) 
                                    ax1.add_patch(rectangulo)
                    
                                    if g[1] < 3600*24:#si el gap fue de todo el dia no lo grafica en columna calor
                                        rectangulo2 = patches.Rectangle( ( list(fil_time["fecha"])[-1], to),timedelta(dias_ad),timedelta(seconds=g[1]),fill=True,facecolor='k',edgecolor='k',linewidth=0.2,alpha=0.08, ) 
                                        ax1.add_patch(rectangulo2)
                            
                            
                            ax1.set_ylim( datetime(1,1,1,0,0,0), datetime(1,1,1,23,59,59))
                            ax1.yaxis.set_minor_locator( HourLocator(interval = int(2)))
                            ax1.yaxis.set_minor_formatter( DateFormatter('%H:%m') )
                            ax1.yaxis.set_major_locator( HourLocator(interval = int(8)))
                            ax1.yaxis.set_major_formatter( DateFormatter('%H') )  
                            
                            labels = ax1.yaxis.get_minorticklabels()
                            plt.setp(labels, rotation=0, fontsize=10)
                            labels = ax1.get_yticklabels() 
                            plt.setp(labels, rotation=0, fontsize=9) 
                            
                            ax1.set_ylabel('Gaps\nHora (UTC)', color='k', fontsize=14)
                            ax1.legend(loc='upper right')
                        
                        ax.legend(loc='upper left')        
                        plt.title('Disponibilidad ' +estacion+" "+sensor+can+" | "+fecha_ini.strftime("%Y-%m-%d")+" - "+fecha_fin.strftime("%Y-%m-%d"))

                        st.pyplot(fig=fig, )
                        
                        
                        #-----GRAFICA CONTEO DE GAPS, OVERLAPS y offset
                        #-----GRAFICA OFFSET
                        fig = plt.figure(figsize=(21., 11.))
                        ax = fig.add_subplot(312)
                        #cuando una estacion entra genera un offset muy grande ese dia, si por ejemplo viene un offet promedio de 2000, pero el dia que entra             nuevamente la estacion ese offset es de 200000, entonces se ve plana la grafica de offset y un pico en el 200000,Para mejorar la             visualizacion, se pone un offset cero el dia que se reconoce que entra la estacion.
                
                
                        ###### Esto es para que el valor de offset despues de l 0 sea 0 tambien
                        busca_ceros=[]
                        i=0
                        
                        for e in fil_time["offs"]:
                            #print("##file_time offset |",e)
                            if e == 0:
                                busca_ceros.append(i)
                            if len(busca_ceros)>0:
                                if e!=0:
                                    
                                    fil_time["offs"].iloc[i]=0
                                    busca_ceros=[]
                            if e == -9:
                                fil_time["offs"].iloc[i]=None
                            #print("#cada offset", fil_time["offs"].iloc[i])
                            

                            i=i+1

                        ######
                        

                        lista_offset_sin_ceros=[]
                        for of in fil_time["offs"]:
                            if of != 0 and str(of) != "nan":
                                
                                lista_offset_sin_ceros.append(of)
                                
                        
                        
                        if len(lista_offset_sin_ceros) >0:
                            offset_prom=round(np.mean(np.array(lista_offset_sin_ceros)),2) #Promedio del offset
                            max_offset=round(max(lista_offset_sin_ceros),2)
                            min_offset=round(min(lista_offset_sin_ceros),2)
                        else:
                            offset_prom=0   
                            max_offset=""
                            min_offset=""

                        #------para mejorar visalizacion offset. Los ceros puestos que son cuando no se pudo calcular (por no disponibilidad)
                        #los convierte en el promedio. Si existen valores gigantes, 50 veces mayor a la media grafica el offset en escala log
                        escala="linear"
                        i=0       
                        for e in fil_time["offs"]:
                            if e==0:
                                fil_time["offs"].iloc[i]=offset_prom
                            if abs(e) >abs(50*offset_prom) or abs(e)>100000:
                                escala="log"
                            i=i+1
                        #--------  
                        
                               
                                
                        if escala == "linear":
                            ax.plot(fil_time["fecha"],fil_time["offs"],linewidth=1,color="#ff0000",label="Offset")   
                            ax.hlines(offset_prom, fecha_ini, fecha_fin, colors='#000000', linestyles='--', linewidth=0.6)
                            
                            ax.text(fil_time["fecha"].iloc[int(len(fil_time["fecha"])/2)], offset_prom, "media: "+str(offset_prom), verticalalignment='top',fontsize=9)
                            ax.set_ylabel('Offset', color='k', fontsize=14)

                        if escala == "log": #si esta en escala lineal obtiene el abs del offset (para poder graficar valores negativos del offset original, no                     grafica media porque pierde sentido, esto sucede porque hay valores gigantes respecto a la media)
                            ax.plot(fil_time["fecha"],np.abs(np.array(list(fil_time["offs"]))),linewidth=1,color="#ff0000",label="Offset")         
                            ax.set_ylabel('abs (Offset)', color='k', fontsize=14)

                        ax.legend(loc='upper left')        
                        ax.xaxis.grid(True, which='major')
                        ax.yaxis.grid(True, which='major')
                        ax.xaxis.set_tick_params(labelsize=9)
                        ax.set_yscale(escala)
                        ax.set_xlim( fecha_ini-timedelta(days=1), fecha_fin+timedelta(days=dias_ad))

                        #overlaps

                        ax1 = ax.twinx()
                        lista_overlaps_sin_nueves=[]
                        for i in range(0,len(fil_time["fecha"])):
                            
                            if fil_time["num_overlaps"].iloc[i] != -9: #se le puso -9 a los datos no disponibles
                                lista_overlaps_sin_nueves.append(fil_time["num_overlaps"].iloc[i])
                                ax1.vlines(fil_time["fecha"].iloc[i]-timedelta(minutes=5), 0, fil_time["num_overlaps"].iloc[i], colors='#32cd32', linewidth=1.5,alpha=0.8)
                        #print(lista_overlaps_sin_nueves)
                        ax1.set_ylabel('Conteo de \n(Overlaps, Gaps)', color='k', fontsize=14)
                        ax1.xaxis.grid(True, which='major')
                        #ax1.yaxis.grid(True, which='major')
                        ax1.xaxis.set_tick_params(labelsize=9)
                        ax1.vlines(fecha_ini, 0, 0, colors='#32cd32', linewidth=1.5, label='Overlaps')   

                        overlaps_prom=round(np.mean(np.array(lista_overlaps_sin_nueves)),2)   #Promedio overlaps
                        num_overlaps = np.sum(lista_overlaps_sin_nueves)
                        max_overlap=max(lista_overlaps_sin_nueves)

                        # gaps
                        lista_gaps_sin_nueves=[]
                        for i in range(0,len(fil_time["fecha"])):
                            if fil_time["num_gaps"].iloc[i] != -9: #se le puso -9 a los datos no disponibles
                                lista_gaps_sin_nueves.append(fil_time["num_gaps"].iloc[i])
                                ax1.vlines(fil_time["fecha"].iloc[i]+timedelta(minutes=5), 0, fil_time["num_gaps"].iloc[i], colors='k', linewidth=1.5,alpha=0.8)

                        ax1.vlines(fecha_fin, 0, 0, colors='k', linewidth=1.5, label='Gaps')            
                        ax1.legend(loc='upper right')
                        plt.title('\n\n\nConteo de (Gaps - Overlaps) y Offset ' + estacion + " "+sensor+can+" | "+fecha_ini.strftime("%Y-%m-%d")+" - "+fecha_fin.strftime("%Y-%m-%d"))

                        gaps_prom = round(np.mean(np.array(lista_gaps_sin_nueves)),2)
                        num_gaps = np.sum(lista_gaps_sin_nueves)
                        max_gaps = max(lista_gaps_sin_nueves)
                        
                        st.pyplot(fig=fig, )
                        
                        #-------GRFICA DE PPSD, CONTEO PICOS Y PICOS EN EL DÍA
                        fig = plt.figure(figsize=(21., 11.))
                        ax = fig.add_subplot(313)
                        
                        #ppsd sin -9
                        lista_ppsd_sin_menosnueves=[]
                        lista_ppsd=[]
                        for of in fil_time["p_ppsd"]:
                            if of != -9:
                                lista_ppsd_sin_menosnueves.append(of)
                                lista_ppsd.append(of)
                                #print(type(of),of)
                            if of == -9:
                                lista_ppsd.append(None)
                            
                            
                        
                        #st.dataframe(fil_time["p_ppsd"])
                        #promedio ppsd % fuera
                        ppsd_prom = round(np.mean(np.array(lista_ppsd_sin_menosnueves)),2)
                    
                        #plotear promedio ppsd
                        ax.plot(fil_time["fecha"],lista_ppsd,linewidth=2,color="#0D9000",label="ppsd")   
                        ax.vlines(fecha_fin, 0, 0, colors='#0D9000', linewidth=1.0, label='PPSD (%)fuera')        
                        ax.set_ylabel('PPSD % por fuera', color='k', fontsize=14)                
                        ax.legend(loc='upper left')
                        ax.xaxis.grid(True, which='major')
                        ax.set_xlim( fecha_ini-timedelta(days=1), fecha_fin+timedelta(days=dias_ad))
                        ax.xaxis.set_tick_params(labelsize=9)
                        #picos
                        ax1 = ax.twinx()
                        lista_picos_sin_nueves=[]
                        
                        for i in range(0,len(fil_time["fecha"])):
                            if fil_time["peaks"].iloc[i] != -9 : #se le puso -9 a los datos no disponibles
                                lista_picos_sin_nueves.append(fil_time["peaks"].iloc[i])                
                                ax1.vlines(fil_time["fecha"].iloc[i], 0, fil_time["peaks"].iloc[i], colors='#8000ff', linewidth=1.0,alpha=1,zorder=100)
                        
                        ax1.vlines(fecha_fin, 0, 0, colors='#8000ff', linewidth=1.0, label='Picos (conteo)')        
                        ax1.set_ylabel('Conteo de \nPicos', color='k', fontsize=14)                
                        ax1.legend(loc='upper left')    
                        plt.title('\n\n\n Picos ' + estacion + " "+sensor+can+" | "+fecha_ini.strftime("%Y-%m-%d")+" - "+fecha_fin.strftime("%Y-%m-%d"))
                                
                        ax1.yaxis.grid(True, which='major')   
                        
                        

                        
                        ppsd_prom = round(np.mean(np.array(lista_ppsd_sin_menosnueves)),2)
                        num_picos = np.sum(lista_picos_sin_nueves)
                        max_picos = max(lista_picos_sin_nueves)
                        
                        #EN TIEMPO
                        """
                        l_fil_tpics = []
                        for fil_time_pic in fil_time["time_peaks"]:
                            if len(str(fil_time_pic)) > 2 :
                                l_fil_tpics.append(fil_time_pic)

                        ax2 = ax.twinx()
                        if len(l_fil_tpics) > 0:
                            
                            to_r=datetime(1,1,1,0,0,1)
                            rectangulo3 = patches.Rectangle( ( fecha_fin, to_r ),timedelta(dias_ad),timedelta(hours=24),fill=True,facecolor='b',edgecolor='b',linewidth=0.2,alpha=0.8)
                            ax2.add_patch(rectangulo3)

                            
                            for tp in fil_time["time_peaks"]:
                                tdia=datetime(tp.year,tp.month,tp.day,12,0,0)
                                to=datetime(1,1,1,tp.hour,tp.minute,tp.second)                    
                                ax1.scatter(tdia,to,s=1.5,c="k",alpha=0.5,zorder=100)
                                ax1.hlines(to, tdia, max(lista_tiempo), colors='k', linestyles='--', linewidth=0.1,alpha=0.7) 
                                ax1.hlines(to, lista_tiempo[-1], lista_tiempo[-1]+timedelta(dias_ad), colors='k', linestyles='-', linewidth=0.2,alpha=0.7)
                        """
                        
                        st.pyplot(fig=fig, )
                        
                    with col2:
                        st.markdown(".")
                        st.write("_________________________")
                        st.markdown(f"**:blue[Min. disp.:]** {min_dis}%**:blue[| Max. disp.:]** {max_dis}%")
                        #st.write(f"Max. disp: {max_dis}")
                        st.markdown(f"**:blue[Promedio disp.:]** {round(prom_dis,2)}%")
                        st.write("_________________________")
                        #st.write(f"Max. offset : {max_offset}" )
                        st.markdown(f"**:red[Min. offset:]** {min_offset} **:red[| Max. offset :]** {max_offset}" )
                        st.markdown(f"**:red[Promedio offset:]** {offset_prom}" )
                        
                        st.write("_______________")
                        #st.write(f"Max. gaps: {max_gaps}")
                        st.markdown(f"**Num. gaps:** {num_gaps} **| Max. gaps:** {max_gaps}")
                        st.markdown(f"**Promedio de gaps:** {gaps_prom}")
                        
                        #st.write(f"Max. overlaps: {max_overlap}")
                        st.markdown(f"**:green[Num. overlaps:]** {num_overlaps} **:green[| Max. overlaps:]** {max_overlap}")
                        st.markdown(f"**:green[Promedio overlaps:]** {overlaps_prom}")
                        
                        
                        st.write("_______________")
                        #st.write(f"Max. de picos: {max_picos}")
                        st.markdown(f"**:violet[Num. picos:]** {num_picos} **:violet[| Max. de picos:]** {max_picos}")
                        st.markdown(f"**:green[Promedio (%) ppsd por fuera:]** {ppsd_prom}%")
            
                    
                
                with tab1:

                    
                    col1,col2= st.columns([5,1.1])
                    with col1:
                        ##Con streamlit
                        #df_index_time = fil_time.set_index("fecha")
                            #linea
                        #st.line_chart(df_index_time[" disponibilidad"])
                        
                        ##con Bokeh
                        #p = figure(title="Disponibilidad", x_axis_label="fecha", y_axis_label="Disponibilidad %")
                        #p.line(fil_time["fecha"], fil_time[" disponibilidad"], legend_label="Trend", line_width=2)
                        #st.bokeh_chart(p, use_container_width=True)

                        ##Con altair
                            ##para mostrar punto cuando se acerca
                        #hover = alt.selection_single(nearest=True, on="mouseover", resolve="global")
                        #c = alt.Chart(fil_time, title=f"Disponibilidad {estacion}").mark_line().encode(
                        #    x= "fecha", y=alt.Y(" disponibilidad", title="Disponibilidad %"), color=alt.datum(" disponibilidad"), tooltip=["fecha"," disponibilidad"]).add_selection(hover)
                        #st.altair_chart(c.interactive(), use_container_width=True)
                        
                        ##Con plotly.express
                        """
                        figex = px.line(fil_time, x="fecha", y=" disponibilidad", title=f"Disponibilidad {estacion}")
                        figex.update_xaxes(showgrid=True, ticklabelmode="period",tickformat="%d\n%b\n%Y")
                        figex.update_layout(hovermode="x unified")
                        """
                        
                        #Cambio de los tiempos gaps para uso en grafica dinamica
                        
                        
                        fig = make_subplots(specs=[[{"secondary_y": True}]])
                        f_i = datetime(fecha_ini.year,fecha_ini.month,fecha_ini.day)
                        
                        #Graficar Disponibilidad
                        fig.add_trace(go.Scatter( x=fil_time["fecha"], y=fil_time["disponibilidad"], mode = "lines",connectgaps=True,name='Disponibilidad',),secondary_y=False,)
                        fig.add_trace(go.Scatter( x=[f_i], y=[0], mode = "lines",marker_color='rgba(140,140,140,1)',name="Gaps (time)",line=dict(width=9),), secondary_y=False)
                        
                        ##Graficar Gaps
                        
                        #con este foorloop se selecciona en una lista solo los tiempos de gaps existentes
                        l_fil_tgap = []
                        for fil_time_gap in fil_time["times_gaps_graf_din"]:
                            if len(str(fil_time_gap[0][0])) > 2:
                                l_fil_tgap.append(fil_time_gap)
                        
                        
                        #para graficar los gaps existentes
                        if len(l_fil_tgap) > 0:
                            for tg in l_fil_tgap:
                                
                                for g in tg:
                                    
                                    #Esta condicional es para que cuando el gap  hace que la fecha final sea el dia siguiente a las 00:00:00, lo cambie por el mismo día a las 23:59:59
                                    if g[1].day == g[0].day:
                                        dia = [datetime(g[0].year,g[0].month,g[0].day,0,0,0),datetime(g[1].year,g[1].month,g[1].day,0,0,0)]
                                        
                                        t_gap = [datetime(1,1,1,g[0].hour,g[0].minute,g[0].second,g[0].microsecond), datetime(1,1,1,g[1].hour,g[1].minute,g[1].second,g[1].microsecond)]    
                                        fig.add_trace(go.Scatter(x=dia, y=t_gap,mode='lines', connectgaps=False,marker_color='rgba(140,140,140,0.75)',name='Gaps (time)'
                                                        ,showlegend=False,line=dict(width=10)),  secondary_y=True,)
                                        
                                    else:
                                        dia = [datetime(g[0].year,g[0].month,g[0].day,0,0,0),datetime(g[1].year,g[1].month,g[0].day,0,0,0)]
                                        
                                        t_gap = [datetime(1,1,1,g[0].hour,g[0].minute,g[0].second,g[0].microsecond), datetime(1,1,1,23,59,59)]    
                                        fig.add_trace(go.Scatter(x=dia, y=t_gap,mode='lines', connectgaps=False,marker_color='rgba(140,140,140,0.75)',name='Gaps (time)'
                                                        ,showlegend=False,line=dict(width=10)),  secondary_y=True,)
                                        
                        
                                    
                        fig.update_yaxes(range=(datetime(1,1,1,0,0,0),datetime(1,1,1,23,59,59)), tickformat="%H:%M:%S\nHora",)  #Limites en eje y horas
                        
                        #detalles
                        tit = f"Disponibilidad {estacion}  {sensor}{can} |  {fecha_ini.strftime('%Y-%m-%d')} - {fecha_fin.strftime('%Y-%m-%d')}"
                        
                        fig.update_layout(width = 800, height = 310,title_text=tit,hovermode="x unified", 
                                        legend=dict(orientation="h",yanchor="bottom",y=1.1,xanchor="right",x=1),
                                        yaxis_title='Disponibilidad (%)')
                        fig.update_xaxes(showgrid=True, ticklabelmode="period",tickformat="%d\n%b\n%Y", gridwidth=1, gridcolor='LightGrey')
                        fig.update_xaxes(showline=True, linewidth=2, linecolor='lightgray', mirror=True)
                        fig.update_yaxes(showline=True, linewidth=2, linecolor='lightgray', mirror=True, )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        
                        
                        #-----GRAFICA CONTEO DE GAPS, OVERLAPS y offset
                        #-----GRAFICA OFFSET
                        
                        ###### Esto es para que el valor de offset despues de l 0 sea 0 tambien
                        busca_ceros=[]
                        i=0
                        
                        for e in fil_time["offs"]:
                            
                            if e == 0:
                                busca_ceros.append(i)
                            if len(busca_ceros)>0:
                                if e!=0:
                                    
                                    fil_time["offs"].iloc[i]=0
                                    busca_ceros=[]
                            if e == -9:
                                fil_time["offs"].iloc[i]=None
                            
                            i=i+1
                        ######
                        
                        #------para mejorar visalizacion offset. Los ceros puestos que son cuando no se pudo calcular (por no disponibilidad)
                        #los convierte en el promedio. Si existen valores gigantes, 50 veces mayor a la media grafica el offset en escala log
                        escala="linear"
                        i=0       
                        for e in fil_time["offs"]:
                            if e==0:
                                fil_time["offs"].iloc[i]=offset_prom
                            if abs(e) >abs(50*offset_prom) or abs(e)>100000:
                                escala="log"
                            i=i+1
                        #-------- 
                        
                        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
                        
                        
                        if escala == "linear":
                            fig2.add_trace(go.Scatter( x=fil_time["fecha"], y=fil_time["offs"], mode = "lines",marker_color='rgba(225,0,0,1)', connectgaps=True,name='offset',),secondary_y=False,)
                            fig2.add_hline(y=offset_prom,line_dash="dot",line_width=1,line_color="grey",annotation_text=f"media: {offset_prom}", 
                            annotation_position="bottom")
                            #fig2.update_yaxes(type="log")

                        if escala == "log": #si esta en escala lineal obtiene el abs del offset (para poder graficar valores negativos del offset original, no                     grafica media porque pierde sentido, esto sucede porque hay valores gigantes respecto a la media)
                            fig2.add_trace(go.Scatter( x=fil_time["fecha"], y=np.abs(np.array(list(fil_time["offs"]))), mode = "lines",marker_color='rgba(225,0,0,1)', connectgaps=True,name='offset_abs',),secondary_y=False,)
                            fig2.add_trace(go.Scatter( x=[f_i], y=[0], mode = "lines",marker_color='rgba(140,140,140,1)',name="Gaps",line=dict(width=9),), secondary_y=False)
                        
                        #leyenda overlaps
                        fig2.add_trace(go.Scatter( x=[fecha_ini ], y=[0], mode = "lines",marker_color='rgba(50,205,50,0.7)',name="Overlaps",line=dict(width=2),), secondary_y=True)
                        #leyenda de gaps
                        fig2.add_trace(go.Scatter( x=[fecha_ini ], y=[0], mode = "lines",marker_color='rgba(140,140,140,0.7)',name="Gaps",line=dict(width=2),), secondary_y=True)
                    
                        #para graficar conteo de overlaps
                        for n_over,n_gaps,time in zip(fil_time["num_overlaps"],fil_time["num_gaps"],fil_time["fecha"]):
                            
                            #graficar numero de overlaps por dia
                            fig2.add_trace(go.Scatter(x=[time,time], y=[0,n_over],mode='lines', connectgaps=False,marker_color='rgba(50,205,50,0.7)',name='Overlaps'
                                                        ,showlegend=False   ,line=dict(width=2),),  secondary_y=True,)
                            #graficar numero de gaps por dia
                            fig2.add_trace(go.Scatter(x=[time,time], y=[0,n_gaps],mode='lines', connectgaps=False,marker_color='rgba(140,140,140,0.7)',name='Gaps'
                                                        ,showlegend=False   ,line=dict(width=2)),  secondary_y=True,)
                            
                        
                        
                        #limites eje auxiliar o secundario
                        fig2.update_yaxes(range=(0,int(max_overlap)*1.5),secondary_y=True) #Limites en eje conteo
                        fig2.update_yaxes(range=(0,int(max_gaps)*2),title_text="Conteo (Overlaps, Gaps)",secondary_y=True)  #Limites en eje conteo

                        #detalles
                        tit2 = 'Conteo de (Gaps - Overlaps) y Offset ' + estacion + " "+sensor+can+" | "+fecha_ini.strftime("%Y-%m-%d")+" - "+fecha_fin.strftime("%Y-%m-%d")
                        fig2.update_layout(width = 800, height = 310,title_text=tit2,hovermode="x unified", 
                                        legend=dict(orientation="h",yanchor="bottom",y=1.1,xanchor="right",x=1),
                                        yaxis_title='Offset')
                        
                        fig2.update_xaxes(showgrid=True, ticklabelmode="period",tickformat="%d\n%b\n%Y", gridwidth=1, gridcolor='LightGrey')
                        fig2.update_xaxes(showline=True, linewidth=2, linecolor='lightgray', mirror=True)
                        fig2.update_yaxes(showline=True, linewidth=2, linecolor='lightgray', mirror=True, )
                        
                        st.plotly_chart(fig2, use_container_width=True)
                                    
                        #-------------GRAFICA DE PPSD, Y CONTEO PICOS E HORAS
                        lista_ppsd_sin_menosnueves=[]
                        lista_ppsd=[]
                        for of in fil_time["p_ppsd"]:
                            if of != -9:
                                lista_ppsd_sin_menosnueves.append(of)
                                lista_ppsd.append(of)
                                
                            if of == -9:
                                lista_ppsd.append(None)
                                
                        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
                        fig3.add_trace(go.Scatter( x=fil_time["fecha"], y=lista_ppsd, mode = "lines",marker_color='rgba(13,144,0,1)', connectgaps=False,name='ppsd',),secondary_y=False,)
                        
                        #leyenda de picos
                        fig3.add_trace(go.Scatter( x=[fecha_ini ], y=[0], mode = "lines",marker_color='rgba(128,0,255,0.7)',name="Picos",line=dict(width=2),), secondary_y=True)
                    
                        #para graficar conteo de picos
                        for n_picos,time in zip(fil_time["peaks"],fil_time["fecha"]):

                            fig3.add_trace(go.Scatter(x=[time,time], y=[0,n_picos],mode='lines', connectgaps=False,marker_color='rgba(128,0,255,0.7)',name='Picos'
                                                        ,showlegend=False   ,line=dict(width=2),),  secondary_y=True,)

                        #limites eje auxiliar o secundario
                        fig3.update_yaxes(range=(0,int(max_picos)*1.5),title_text="Conteo Picos",secondary_y=True)  #Limites en eje conteo

                        #detalles
                        tit3 = '% ppsd fuera - picos ' + estacion + " "+sensor+can+" | "+fecha_ini.strftime("%Y-%m-%d")+" - "+fecha_fin.strftime("%Y-%m-%d")
                        fig3.update_layout(width = 800, height = 310,title_text=tit3,hovermode="x unified", 
                                        legend=dict(orientation="h",yanchor="bottom",y=1.1,xanchor="right",x=1),
                                        yaxis_title='ppsd (%)')
                        
                        fig3.update_xaxes(showgrid=True, ticklabelmode="period",tickformat="%d\n%b\n%Y", gridwidth=1, gridcolor='LightGrey')
                        fig3.update_xaxes(showline=True, linewidth=2, linecolor='lightgray', mirror=True)
                        fig3.update_yaxes(showline=True, linewidth=2, linecolor='lightgray', mirror=True, )
                        
                        st.plotly_chart(fig3, use_container_width=True)
                        
                
                with col2:


                    st.markdown(".")
                    st.write("_________________________")
                    st.markdown(f"**:blue[Min. disp.:]** {min_dis}%**:blue[| Max. disp.:]** {max_dis}%")
                    #st.write(f"Max. disp: {max_dis}")
                    st.markdown(f"**:blue[Promedio disp.:]** {round(prom_dis,2)}%")
                    st.write("_________________________")
                    #st.write(f"Max. offset : {max_offset}" )
                    st.markdown(f"**:red[Min. offset:]** {min_offset} **:red[| Max. offset :]** {max_offset}" )
                    st.markdown(f"**:red[Promedio offset:]** {offset_prom}" )
                    
                    st.write("_______________")
                    #st.write(f"Max. gaps: {max_gaps}")
                    st.markdown(f"**Num. gaps:** {num_gaps} **| Max. gaps:** {max_gaps}")
                    st.markdown(f"**Promedio de gaps:** {gaps_prom}")
                    
                    #st.write(f"Max. overlaps: {max_overlap}")
                    st.markdown(f"**:green[Num. overlaps:]** {num_overlaps} **:green[| Max. overlaps:]** {max_overlap}")
                    st.markdown(f"**:green[Promedio overlaps:]** {overlaps_prom}")
                    
                    
                    st.write("_______________")
                    #st.write(f"Max. de picos: {max_picos}")
                    st.markdown(f"**:violet[Num. picos:]** {num_picos} **:violet[| Max. de picos:]** {max_picos}")
                    st.markdown(f"**:green[Promedio (%) ppsd por fuera:]** {ppsd_prom}%")
            

                          
            
            else:
                st.write("no existe")
        
        tabz, tabn,tabe = st.tabs(["Z","N","E"])
        with tabz:
            list_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/{estacion}_{sensor}Z*")
            plot_Cal(estacion,sensor,fecha_ini, fecha_fin, list_est,"Z")
        with tabn:
            list_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/{estacion}_{sensor}N*")
            plot_Cal(estacion,sensor,fecha_ini, fecha_fin, list_est,"N")
        with tabe:  
            list_est = glob.glob(os.path.dirname(os.path.abspath(__file__))+f"/Datos/{estacion}_{sensor}E*")
            plot_Cal(estacion,sensor,fecha_ini, fecha_fin, list_est,"E")
        
        """
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_general_{ID_event}.json") == True:
            st.header("Parámetros generales del sismo")
                

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

        """
    
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

                



        
