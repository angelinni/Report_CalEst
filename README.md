![SGC](images/sgc_logo.png)<!-- .element width="700"-->

# Reporte Calidad Estacion Report_CalEst


La aplicación genera graficas dinamicas de consultas por fechas y genera informes semestrales y mensuales en formato docx 
con la información de funcionamiento y calidad de cada estación en tiempo real, mostrando por estación datos de disponibilidad, gaps, overlaps, offset, picos y ppsd. Además, 
el sismólogo encargado puede ingresar sus observaciones del estado de cada estación. Esta apliación reune desarrollos de Miguel Lizarazo en la toma de datos de estaciones y Monica Acosta con SIIGEO.
## 1. Instalacio linux

### - Python
Python Versión 3.7 en adelante. (Usaremos como ejemplo python 3.10)
```bash
sudo apt-get install python3.7 (o 3.8)
```

Tener virtualenv en python.
```bash
python3.7 -m pip install virtualenv
```

#### Instalación con pip 
```bash
python3.7 -m virtualenv env_sc2sf
source env_sc2sf/bin/activate
pip install -r requirements.txt
```

## Autor

- Angel Agudelo adagudelo@sgc.gov.co
