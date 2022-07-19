from astroquery.jplhorizons import Horizons
# https://astroquery.readthedocs.io/en/latest/jplhorizons/jplhorizons.html
import csv


name="pluto"


#planet = Horizons(id='1', location='@sun',epochs={'start':'2010-01-01', 'stop':'2010-03-30','step':'1d'})
#planet = Horizons(id='2', location='@sun',epochs={'start':'2010-01-01', 'stop':'2010-09-13','step':'1d'})
#planet = Horizons(id='3', location='@sun',epochs={'start':'2010-01-01', 'stop':'2011-01-01','step':'1d'})
#planet = Horizons(id='4', location='@sun',epochs={'start':'2010-01-01', 'stop':'2011-11-22','step':'2d'})
#planet = Horizons(id='5', location='@sun',epochs={'start':'2010-01-01', 'stop':'2021-11-10','step':'10d'})
#planet = Horizons(id='6', location='@sun',epochs={'start':'1990-10-22', 'stop':'2020-04-20','step':'20d'})
#planet = Horizons(id='7', location='@sun',epochs={'start':'1937-08-01', 'stop':'2021-12-15','step':'60d'})
#planet = Horizons(id='8', location='@sun',epochs={'start':'1856-03-01', 'stop':'2021-12-15','step':'120d'})
planet = Horizons(id='9', location='@sun',epochs={'start':'1772-01-01', 'stop':'2021-12-15','step':'180d'})

eph = planet.ephemerides()
r=[]
lon=[]
lat=[]
for i in range(len(eph["r"])):
    r.append(eph["r"][i])
    lon.append(eph["PABLon"][i])
    lat.append(eph["PABLat"][i])


name=name+"_data.csv"
with open(name,'w') as planetfile:
    w=csv.writer(planetfile,delimiter=',')
    w.writerow(r)
    w.writerow(lon)
    w.writerow(lat)
