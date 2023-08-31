import numpy as np
import pandas as pd
from PIL import Image
import plotly.graph_objects as go
from scipy import misc
import matplotlib.pyplot as plt
import streamlit as st

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json


def d3():
    
    #im = misc.face()
    #   im = misc.imageio("/mnt/almacenamiento/pyangel/Report_CalEst/Simbolo_SGC_Color.png")
    #im = np.array(plt.imread("/mnt/almacenamiento/pyangel/Report_CalEst/Simbolo_SGC_Color.png"))
    img_pil = Image.open("/mnt/almacenamiento/pyangel/Report_CalEst/map.png")
    im1 = np.array(img_pil)
    im = np.flip(im1, axis=0)
    #im2 = np.rot90(im1)
    #im = np.rot90(im2)
    im_x, im_y ,z= im.shape
    eight_bit_img = Image.fromarray(im).convert('P', palette='WEB', dither=None)
    dum_img = Image.fromarray(np.ones((3,3,3), dtype='uint8')).convert('P', palette='WEB')
    idx_to_color = np.array(dum_img.getpalette()).reshape((-1, 3))
    colorscale=[[i/255.0, "rgb({}, {}, {})".format(*rgb)] for i, rgb in enumerate(idx_to_color)]

    # Sample data: 3 trajectories
    t = np.linspace(0, 10, 200)
    df = pd.concat([pd.DataFrame({'x': 200 * (1 + np.cos(t + 5 * i)), 'y': 150 * (1 + np.sin(t)), 't': t, 'id': f'id000{i}'}) for i in [0, 1, 2]])
    #im = im.swapaxes(0, 1)[:, ::-1]
    colors=df['t'].to_list()

    # # 3d scatter plot
    x = np.linspace(100,im_x, im_x)
    y = np.linspace(0, im_y, im_y)
    z = np.zeros(im.shape[:2])+10
    fig = go.Figure()

    

    fig.add_trace(go.Scatter3d(
        x=df['x'], 
        y=df['y'], 
        z=df['t'],
        marker=dict(
            color=colors,
            size=4,
        )
        ))

    fig.add_trace(go.Surface(x=x, y=y, z=z,
        surfacecolor=eight_bit_img, 
        cmin=00, 
        cmax=255,
        colorscale=colorscale,
        showscale=False,
        lighting_diffuse=1,
        lighting_ambient=1,
        lighting_fresnel=1,
        lighting_roughness=1,
        lighting_specular=0.5,

    ))

    fig.update_layout(
        title="My 3D scatter plot",
        width=800,
        height=800,
        scene=dict(xaxis_visible=True,
                    yaxis_visible=True, 
                    zaxis_visible=True, 
                    xaxis_title="X",
                    yaxis_title="Y",
                    zaxis_title="Z" ,

        ))
    fig.update_scenes(camera_up=dict(z=1,x=0, y=0), camera_eye=dict(x=1.5, y=-1.5, z=1.5))

    st.plotly_chart(fig, use_container_width=True)
    
def d4():
    
    # Read data from a csv
    #_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')
    #z = z_data.values
    #sh_0, sh_1 = z.shape
    #x = np.linspace(0, 1, sh_0)
    #print(z_data)
    #print(x)
    
    """
    z_m= [[ 828.5, 2500.5, 2985,  2804, 2516,  2595,  1849, ],
        [ 955.,  2338.,  2545.,  2952.,  3131,  2628.5, 1983.5],
        [1627.,  2702.5, 2611.5, 2774.5, 3058.,  2152.5, 2566.5],
        [1116.,  1354.,  3042.,  2677.,  2672.,  2881.5, 1815. ]]
    lat=[4.5,        4.66666667, 4.83333333, 5.        ]
    lon=[-74.5,        -74.33333333, -74.16666667, -74.,        -73.83333333, -73.66666667, -73.5]
    """
    #z_m=[[715.5,378.5,314.0,426.0,1261.5,3050.5,3169.0,2487.0,1694.0,789.5,341.5,266.0,203.5],
    #     [915.0,644.0,391.0,437.0,1389.0,2107.5,3496.5,2762.5,2296.0,1673.0,621.0,357.5,219.5],
    #     [1849.0,601.0,447.5,564.5,828.5,2500.5,2985.0,2804.0,2516.0,2595.0,1849.0,489.0,395.5],
    #     [2711.0,915.0,273.5,737.5,955.0,2338.0,2545.0,2952.0,3131.0,2628.5,1983.5,981.5,626.0],
    #     [2619.0,995.0,277.0,845.0,1627.0,2702.5,2611.5,2774.5,3058.0,2152.5,2566.5,1693.5,618.0],
    #     [2260.0,1156.0,298.5,673.0,1116.0,1354.0,3042.0,2677.0,2672.0,2881.5,1815.0,1828.0,1251.0],
    #     [1995.0,1148.5,441.5,620.0,797.0,1328.0,1894.5,3284.0,2888.5,2801.5,2893.0,2244.0,1905.0],
    #     [2558.5,1137.0,351.5,465.5,1044.0,1311.0,1447.5,2828.0,2875.5,2919.0,2558.5,2583.5,2119.5],
    #     [1282.0,991.5,290.0,180.5,798.5,1066.5,1068.5,1494.5,2641.0,2612.0,2747.0,2841.5,3319.0],
    #     [1599.0,913.5,400.5,169.5,307.5,900.0,1054.5,966.5,2801.0,2959.5,2554.5,2968.5,2719.5],
    #     [1381.5,981.5,435.0,162.0,188.0,450.5,648.5,1628.5,2232.0,1968.5,2374.0,2723.5,3029.0]]
    
    #lat=[4.16666667, 4.33333333, 4.5,        4.66666667, 4.83333333, 5., 5.16666667, 5.33333333, 5.5,        5.66666667, 5.83333333]
    #lon=[-75.16666667, -75.,         -74.83333333, -74.66666667, -74.5, -74.33333333, -74.16666667, -74.,         -73.83333333, -73.66666667, -73.5,        -73.33333333, -73.16666667]

    
    with open("Colombia1.json","r") as json_file:
        results = json.load(json_file)
    
    
    max_prof = -30000 #metros negativo
    lat1=results["lat"]
    lon1=results["lon"]
    elev1=results["elev"]
    if max_prof >= -30000:
        elev1=[[float(cu)/8 for cu in l] for l in results["elev"]]
    
    col_scale= [[0, 'rgb(79, 118, 49)'], [0.4, 'rgb(112, 157, 86)'],[0.7, 'rgb(206,131, 42)'] ,[1, 'rgb(131, 72, 0)']]
    fig = go.Figure(data=[go.Surface(z=elev1, x=lon1, y=lat1,colorscale=col_scale)])
    fig.update_layout(title='colombia_el', autosize=False,
                    scene=dict(xaxis_visible=True,
                    yaxis_visible=True, 
                    zaxis_visible=True, 
                    xaxis_title="lon",
                    yaxis_title="lat",
                    zaxis_title="elevación",
                    zaxis=dict(range=[max_prof, 6000])))
    

    st.plotly_chart(fig, use_container_width=True)
    #fig.show()
    
    


    

