from skyfield.api import EarthSatellite, Topos, load
from numpy import around
import tkinter as tk
from tkinter import ttk
import threading
import datetime
import pyfiglet
import urllib.request
import os

def mapping():
    data = urllib.request.urlopen("https://www.celestrak.com/NORAD/elements/stations.txt").read().decode("utf-8")
    data=data.split('\n')
    global parsedData
    parsedData={}
    i=0
    while i < len(data)-1:
        parsedData[data[i].split('  ')[0]]=[data[i+1].replace('\r',''),data[i+2].replace('\r','')]
        i+=3


# --------- fullsat.py --------- Apr.27-May.07, 2019 --------------------
def localisation(years, month, day, hours, minute, second):
  ts = load.timescale()
  timestring= str(years+month+day+hours+"h"+minute+"m"+second+"s")
  t = ts.utc(years, month, day, hours, minute, second)   # datetime selection
  # TLE twoline dbase
  line1,line2=calculTle()

  loc = Topos('37.0328 N', '15.0650 E')    # location coords
  satellite = EarthSatellite(line1, line2)

  # Geocentric
  geometry = satellite.at(t)

  # Geographic point beneath satellite
  subpoint = geometry.subpoint()
  latitude = subpoint.latitude
  longitude = subpoint.longitude
  elevation = subpoint.elevation

  # Topocentric
  difference = satellite - loc
  geometry = difference.at(t)
  topoc= loc.at(t)
  #
  topocentric = difference.at(t)
  geocentric = satellite.at(t)
  # ------ Start outputs -----------
  print ('\n Heures locale', timestring)
  print (' Temps Solaire: ',t)
  print ('',loc)
  print ('\n Subpoint Longitude= ', longitude )
  print (' Subpoint Latitude = ', latitude )
  print (' Subpoint Elevation=  {0:.3f}'.format(elevation.km),'km')
  # ------ Step 1: compute sat horizontal coords ------
  alt, az, distance = topocentric.altaz()
  if alt.degrees > 0:
      print('\n',satellite, "\n est au dessu de l'horizon")
  print ('\n Altitude= ', alt )
  print (' Azimute = ', az )
  print (' Distance=  {0:.3f}'.format(distance.km), 'km')
  #
  # ------ Step 2: compute sat RA,Dec [equinox of date] ------
  ra, dec, distance = topocentric.radec(epoch='date')
  print ('\n Ascention droite= ', ra )
  print (' Déclinaison =', dec )
  #
  # ------ Step 3: compute sat equatorial coordinates  --------
  print ('\n Vecteur définissant la position du satellite: r = R + rho')
  print('    Obs. posit.(R): ',topoc.position.km,'km')
  print(' topocentrique (rho): ',topocentric.position.km,'km')
  print(' -----------------')
  print('    Geocentrique (r): ',geocentric.position.km,'km')
  #
  # ------ Step 4: sat equatorial coordinates roundoff 3 decimals  --------
  sho1= around(topoc.position.km, decimals=3)
  sho2= around(topocentric.position.km, decimals=3)
  sho3= around(geocentric.position.km, decimals=3)
  print ('\n Arrondi du vecteur définissant la position du satellite: r = R + rho')
  print('    Obs. posit.(R): ',sho1,'km')
  print(' Topocentrique (rho): ',sho2,'km')
  print(' -----------------')
  print('    Geocentrique (r): ',sho3,'km')
  # EOF: ----- fullsat.py ---------


def actuelhours():
  current=str(datetime.datetime.now()).split(" ")
  currentday=current[0].split("-")
  currentime=current[1].split(":")

  yearentry.delete(0,tk.END)
  monthentry.delete(0,tk.END)
  dayentry.delete(0,tk.END)
  hoursentry.delete(0,tk.END)
  minutentry.delete(0,tk.END)
  secondentry.delete(0,tk.END)

  yearentry.insert(0,currentday[0])
  monthentry.insert(0,currentday[1])
  dayentry.insert(0,currentday[2])
  hoursentry.insert(0,currentime[0])
  minutentry.insert(0,currentime[1])
  secondentry.insert(0,round(float(currentime[2])))


# ---------------------------------------

try:
  os.system("color c")
except:
  print("Votre systeme n'est pas compatible avec le changement de couleur de la console, pour le moment ...")

print(pyfiglet.figlet_format("Astree", font = "cosmike"))
print("A Calamar Industries application")
# Tkinter

def clear_entry(event, entry):
    entry.delete(0, tk.END)
    entry.unbind('<Button-1>', click_event)


root = tk.Tk()
root.title("Astrée")
root.geometry("700x300")
root.resizable(height="false",width="false")
root.configure(bg="#151e3b")

temps = tk.LabelFrame(root,text="Horaire",bg="#151e3b",fg="#ff2424", relief="solid",width="340",height="140",font=("Helvetica", 12))
temps.grid_propagate(0)
temps.grid(row=0,column=0)

datelabel = tk.LabelFrame(temps,text="Date de l'observation",bg="#151e3b",fg="#ff2424", relief="solid",font=("Helvetica", 11))
datelabel.grid(column=0,row=0)

hourslabel = tk.LabelFrame(temps,text="Heure de l'observation",bg="#151e3b",fg="#ff2424", relief="solid",font=("Helvetica", 11))
hourslabel.grid(column=1,row=0)

tlelabel = tk.LabelFrame(root,text="TLE du satellite à observer",bg="#151e3b",fg="#ff2424", relief="solid",width="690",height="140",font=("Helvetica", 12))
tlelabel.grid_propagate(0)
tlelabel.grid(row=1,column=0,columnspan=2)

positionlabel = tk.LabelFrame(root,text="Position de l'observateur",bg="#151e3b",fg="#ff2424", relief="solid",font=("Helvetica", 11),height="140",width="340")
positionlabel.grid_propagate(0)
positionlabel.grid(column=1,row=0)


yearentry= tk.Entry(datelabel, width="6",justify="center",bg="#151e3b",fg="#ff2424",font=("Helvetica", 12))
yearentry.grid(column=0,row=0)
yearentry.insert(0,"AAAA")

monthentry= tk.Entry(datelabel, width="4",justify="center",bg="#151e3b",fg="#ff2424",font=("Helvetica", 12))
monthentry.grid(column=1,row=0)
monthentry.insert(0,"MM")

dayentry= tk.Entry(datelabel, width="4",justify="center",bg="#151e3b",fg="#ff2424",font=("Helvetica", 12))
dayentry.grid(column=2,row=0)
dayentry.insert(0,"JJ")

hoursentry= tk.Entry(hourslabel, width="4",justify="center",bg="#151e3b",fg="#ff2424",font=("Helvetica", 12))
hoursentry.grid(column=0,row=0)
hoursentry.insert(0,"HH")

minutentry= tk.Entry(hourslabel, width="4",justify="center",bg="#151e3b",fg="#ff2424",font=("Helvetica", 12))
minutentry.grid(column=1,row=0)
minutentry.insert(0,"MM")

secondentry= tk.Entry(hourslabel, width="4",justify="center",bg="#151e3b",fg="#ff2424",font=("Helvetica", 12))
secondentry.grid(column=2,row=0)
secondentry.insert(0,"SS")

yearentry.bind("<Button-1>", lambda event: yearentry.delete(0,tk.END))
monthentry.bind("<Button-1>", lambda event: monthentry.delete(0,tk.END))
dayentry.bind("<Button-1>", lambda event: dayentry.delete(0,tk.END))
hoursentry.bind("<Button-1>", lambda event: hoursentry.delete(0,tk.END))
minutentry.bind("<Button-1>", lambda event: minutentry.delete(0,tk.END))
secondentry.bind("<Button-1>", lambda event: secondentry.delete(0,tk.END))

actuelhoursbutton = tk.Button(temps,text="Temps actuel", command= actuelhours,font=("Helvetica", 12),bg="#151e3b",fg="#ff2424",activebackground='#ff2424')
actuelhoursbutton.grid(column=0,row=1, columnspan=2)


tle1label = tk.Label(tlelabel, text='TLE 1 :',bg="#151e3b",fg="#ff2424",font=("Helvetica", 12))
tle1label.grid(column=0,row=0)

tle1entry = tk.Entry(tlelabel, width="60",bg="#151e3b",fg="#ff2424",font=("Helvetica", 12))
tle1entry.grid(column=1,row=0)

tle2label = tk.Label(tlelabel, text='TLE 2 :',bg="#151e3b",fg="#ff2424",font=("Helvetica", 12))
tle2label.grid(column=0,row=1)

tle2entry = tk.Entry(tlelabel, width="60",bg="#151e3b",fg="#ff2424",font=("Helvetica", 12))
tle2entry.grid(column=1,row=1)

tle1entry.bind("<Button-1>", lambda event: tle1entry.delete(0,tk.END))
tle2entry.bind("<Button-1>", lambda event: tle2entry.delete(0,tk.END))

mapping()
def listesatellite() :
  sateliste = []
  for key in parsedData:
    sateliste.append(key)
  return sateliste

def refresh(event):
  tle1entry.delete(0, 'end')
  tle1entry.insert(0,parsedData[event.widget.get()][0])
  tle2entry.delete(0, 'end')
  tle2entry.insert(0,parsedData[event.widget.get()][1])

satelliteselector = ttk.Combobox(tlelabel, value=listesatellite())
satelliteselector.current(listesatellite().index(listesatellite()[0]))
satelliteselector.bind('<<ComboboxSelected>>', refresh)
satelliteselector.grid(column=0,row=2,columnspan=2)

latlabel = tk.Label(positionlabel, text='Lattitude :',bg="#151e3b",fg="#ff2424",font=("Helvetica", 12))
latlabel.grid(column=0,row=0)

latentry = tk.Entry(positionlabel, width="12",bg="#151e3b",fg="#ff2424",font=("Helvetica", 12))
latentry.grid(column=1,row=0)

longlabel = tk.Label(positionlabel, text='Longitude :',bg="#151e3b",fg="#ff2424",font=("Helvetica", 12))
longlabel.grid(column=0,row=1)

logentry = tk.Entry(positionlabel, width="12",bg="#151e3b",fg="#ff2424",font=("Helvetica", 12))
logentry.grid(column=1,row=1)


# print(mapping()["ISS (ZARYA)"])
threading.Thread(target=root.mainloop()).start()
# TODO : Interface :

#   -> bouton dynamique selecteur de couleur de police
#   -Temps :
#     ->Date JJ/MM/AAAA 
#     -> Heure HH:MM:SS
#     -> heure actuelle fonction
# 
#   -Satellite :
#     ->TLE : 2 lignes
#     ->Nom
#     ->Selecteur d'API
#   
#   Localisation : (préciser le format : degré,reste exemple : 37.238779, -115.803838)
#     ->Latitude : positif ou négatif : +=>N; -=>S
#     ->Longitude : positif ou négatif : +=>E; -=>W
# 
# 
