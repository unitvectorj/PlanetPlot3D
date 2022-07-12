import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path
from astroquery.jplhorizons import Horizons
from datetime import date, timedelta
from mpl_toolkits import mplot3d
import numpy as np
import csv
from matplotlib.backend_bases import MouseButton

# sets chunk size to 10000 so millions of points/lines can be plotted (helpful)
mpl.rcParams['agg.path.chunksize'] = 10000

# variables and lists
two_pi = 2*np.pi
csvs=["mercury_data.csv","venus_data.csv","earth_data.csv","mars_data.csv","jupiter_data.csv","saturn_data.csv","uranus_data.csv","neptune_data.csv","pluto_data.csv"]
rad_lists,lon_lists,lat_lists,ox_lists,oy_lists,oz_lists=[],[],[],[],[],[]


######################################
###   THE DATA YOU NEED TO ENTER   ###
######################################

#  the color palette
theme = "black" # "white","black","bcolor",'wcolor'


#  the date plotted  {"yyyy-mm-dd"}
    # in some cases, you will need to use the previous or next day instead of your intended day :(
    # - no one can tell the difference
the_date="1981-08-18"


#  the size things are rendered  (it will be the same thickness/size no matter how you zoom the plot)
planetscale=0.4     # make this larger if you want to zoom in
ringscale=planetscale*2.4       # you'll have to adjust this as well depending on zoom level
linethick=1 # 2.2      # this works well for printing them 10x8 inches
visible=0.6      # portion of orbit rendered (faded from full to invisible)


#  the font for text (for displaying date, name, legend...)
#fpath=Path(mpl.get_data_path(),'/Users/jim/Desktop/Unit_Vector_Games/fonts/0_AlltheFonts/Regular_Fonts/Exo2-Light.ttf')




#  this part will get the next day, which is needed for getting the positional data. Don't worry about this.
_d=date(int(the_date[:4]),int(the_date[5:7]),int(the_date[8:]))
_d+=timedelta(days=1)
next=_d.strftime("%Y-%m-%d")



#####################################################
###   FUNCTION FOR PLOTTING THE RINGS OF SATURN   ###
#####################################################
def rings(x,y,z,s):
    ringxs,ringys,ringzs=[],[],[]
    thets=np.arange(0,two_pi,two_pi/24)
    for r in range(24):
        ringxs.append(x+s*0.15*np.cos(thets[r]))
        ringys.append(y+s*0.15*np.sin(thets[r]))
        ringzs.append(z+s*0.045*np.sin(thets[r]))
    ringxs.append(ringxs[0])
    ringys.append(ringys[0])
    ringzs.append(ringzs[0])
    return ringxs,ringys,ringzs



##################################################
###   GET THE PLANETS' POSITIONS ON THE_DATE   ###
##################################################
scatx,scaty,scatz=[0],[0],[0]
scatlons=[]
# 'scale' scales the outer planets' orbital radii down
scale=[1,1,1,1,0.5,0.4,0.3,0.25,0.25]
#scale=[1,1,1,1,1,1,1,1,1]
for p in range(1,10):
    planet = Horizons(id=p, location='@sun',epochs={'start':the_date, 'stop':next,'step':'1d'})
    eph = planet.ephemerides()
    r=eph["r"][0]
    lon=np.radians(eph["PABLon"][0])
    scatlons.append(lon)
    lat=np.radians(eph["PABLat"][0])
    scatx.append(r*scale[p-1]*np.cos(lon))
    scaty.append(r*scale[p-1]*np.sin(lon))
    scatz.append(r*scale[p-1]*np.sin(lat))





#######################################
###   GET ORBITAL PATHS FROM CSVs   ###
#######################################
for j,p_data in enumerate(csvs):
    p_index=0
    this_r,this_lon,this_lat,this_ox,this_oy,this_oz=[],[],[],[],[],[]
    with open("csvs/"+p_data,newline='') as this_p:
        pr=csv.reader(this_p,delimiter=",")
        p_rows=[]
        for row in pr:
            p_rows.append(row)
        for i in range(len(p_rows[0])):
            this_r.append(float(p_rows[0][i])*scale[j])
            this_lon.append(np.radians(float(p_rows[1][i])))
            if this_lon[i-1]<scatlons[j] and this_lon[i]>scatlons[j]:
                p_index=i
            this_lat.append(np.radians(float(p_rows[2][i])))

    this_r[-1]=this_r[0]
    this_lon[-1]=this_lon[0]
    this_lat[-1]=this_lat[0]
    this_r=this_r[p_index:]+this_r[:p_index]
    this_lon=this_lon[p_index:]+this_lon[:p_index]
    this_lat=this_lat[p_index:]+this_lat[:p_index]


    for i in range(len(this_r)):
        this_ox.append(this_r[i]*np.cos(this_lon[i]))
        this_oy.append(this_r[i]*np.sin(this_lon[i]))
        this_oz.append(this_r[i]*np.sin(this_lat[i]))
    this_ox.append(scatx[j+1])
    this_oy.append(scaty[j+1])
    this_oz.append(scatz[j+1])
    rad_lists.append(this_r)
    lon_lists.append(this_lon)
    lat_lists.append(this_lat)
    ox_lists.append(this_ox)
    oy_lists.append(this_oy)
    oz_lists.append(this_oz)




#################################
###   BODY AND ORBIT COLORS   ###
#################################

#  the orbit colors are slightly darker than the corresponding body color
# can use ccs color strings, or rgb values 0-255, or 0-1
bodycols=[
    (1.0,0.845,0.0,1.0), # sun
    "gray",  # mercury
    "orange", # venus
    (0.1,0.4451,0.562), # earth
    "red", # mars
    "chocolate", # jupiter
    (0.39,0.49,0.16), # saturn
    (0.89,0.639,0.0), # uranus
    (0.1,0.1,0.725), # neptune
    (0.3,0.52,0.75) # pluto
    ]
orbcols=[
    (0.38,0.38,0.38), # mercury
    (0.85,0.497,0.0), # venus
    (0.1,0.3951,0.512), # earth
    (0.9127,0.1288,0.2852), # mars
    (0.8,0.4405,0.0), # jupiter
    (0.35,0.45,0.13), # saturn
    (0.85,0.599,0.0), # uranus
    (0.0,0.0,0.695), # neptune
    (0.2445,0.5098,0.7358) # pluto
    ]


##############################
###   FIGURE PARAMETERS   ####
##############################
if theme!="white" and theme!="wcolor":
    plt.style.use('dark_background')
reach=max(rad_lists[-1]) # sets the size of the plot to the maximum radius of Pluto's orbit
fig = plt.figure(figsize=(8,8)) # display inches 
ax = plt.axes(projection='3d',xlim3d=(-reach,reach),ylim3d=(-reach,reach),zlim3d=(-reach,reach))
ax.set_axis_off()
plt.subplots_adjust(left=0,right=1,top=1,bottom=0)


#ax.set_title(str(the_date),color="orangered",font=fpath, fontsize=32)



#################################
###   PLOT ORBITS WITH FADE   ###
#################################
for p in range(len(rad_lists)):
    final_l=0
    ocol=(0,0,0)
    olength=len(ox_lists[p])
    seg=4
    start = round(olength*(1-visible))
    segments=(olength-3)/seg
    thickincr=(linethick/2)/segments

    # plots each line segment with incremented fade
    for l in range(start,olength-seg+1,seg):
        alpha=(l-start)/(olength-start)
        if theme=="white":
            ocol=(1-alpha,1-alpha,1-alpha)
        elif theme=="black":
            ocol=(alpha,alpha,alpha)
        elif theme=="bcolor":
            ocol=(orbcols[p][0]*alpha, orbcols[p][1]*alpha, orbcols[p][2]*alpha)
        elif theme=="wcolor":
            coldiff0 = (1-orbcols[p][0])*alpha
            coldiff1 = (1-orbcols[p][1])*alpha
            coldiff2 = (1-orbcols[p][2])*alpha
            ocol=(1-coldiff0, 1-coldiff1, 1-coldiff2)
        ax.plot3D(ox_lists[p][l:l+seg+1],oy_lists[p][l:l+seg+1],oz_lists[p][l:l+seg+1],linewidth=linethick/2+thickincr*l/4,c=ocol)
        final_l=l
    if (final_l+seg)!=len(ox_lists[p]):
        # plots one more line in case there's a gap between the line and the planet
        # sometimes it looks cool if you comment this out
        ax.plot3D(ox_lists[p][final_l+seg:],oy_lists[p][final_l+seg:],oz_lists[p][final_l+seg:],linewidth=linethick,c=ocol)



################################
###   SET BODY/RING COLORS   ###
################################
circlecols=bodycols
ringcol=bodycols[6]
if theme=="white":
    circlecols="black"
    ringcol="black"
elif theme=="black":
    circlecols="white"
    ringcol="white"



###############################
###   DRAW SATURN'S RINGS   ###
###############################
for n in range(1,4):
    sc=(1+(0.2*n))*ringscale
    rxs,rys,rzs=rings(scatx[6],scaty[6],scatz[6],sc)
    ax.plot3D(rxs,rys,rzs,linewidth=0.5,c=ringcol)



####################################
###   DRAW THE SUN AND PLANETS   ###
####################################
plansizes=[150*planetscale,10*planetscale,24*planetscale,30*planetscale,20*planetscale,80*planetscale,60*planetscale,47*planetscale,43*planetscale,8*planetscale]
ax.scatter3D(scatx,scaty,scatz,s=plansizes,c=circlecols,depthshade=False)


#####################################
###   SET A STARTING VIEW ANGLE   ###
#####################################
ax.view_init(90,0)

"""
def on_click(event):
    if event.button is MouseButton.LEFT:
        plt.savefig("orbit.svg")

plt.connect('button_press_event', on_click)
"""
plt.show()