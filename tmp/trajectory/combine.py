import pandas as pd
import numpy as np
from glob import glob

files = glob('./*csv')

dt = []
for file in files:
  df = pd.read_csv(file)

  df[['Deviation', 'Azimuth']] = np.deg2rad(df[['Deviation', 'Azimuth']])

  md1 = df.MD_ft.shift(1).fillna(0)
  md2 = df.MD_ft

  azm1 = df.Azimuth.shift(1).fillna(0)
  azm2 = df.Azimuth

  dev1 = df.Deviation.shift(1).fillna(0)
  dev2 = df.Deviation

  df['DL'] = 0.000001+np.arccos(np.cos(dev2-dev1)-np.sin(dev1)*np.sin(dev2)*(1-np.cos(azm2-azm1)))
  dl = df.DL

  df['CF'] = 2/dl*(np.tan(dl/2))
  cf = df.CF

  df['North'] = (md2-md1) * ((np.sin(dev2)*np.cos(azm2) +  np.sin(dev1)*np.cos(azm1)) / 2*cf)
  df['North'] = df['North'].cumsum()

  df['East'] = (md2-md1) * ((np.sin(dev2)*np.sin(azm2) + np.sin(dev1)*np.sin(azm1)) / 2*cf)
  df['East'] = df['East'].cumsum()

  df['Res'] = np.sqrt(df['North']**2 + df['East']**2)
  df.fillna(0, inplace=True)

  dt.append(df)

data = pd.concat(dt, ignore_index=True)
data.to_csv("../trajectory_database.csv", index=False)