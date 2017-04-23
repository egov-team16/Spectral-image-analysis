import pandas as pd
import numpy as np

df = pd.read_excel('sampledata.xlsx')
print(df.columns)

sun_elevation = df['Sun Elevation (in degrees)']
sat_angle = df['Satellite off-nadir (in degrees)']
shadow = df['Shadow height (in metres)']

def cal_TempHeight(sun_elevation,shadow):
    tempHeight = np.tan(sun_elevation)*shadow
    return tempHeight

def cal_extraShadow(sat_angle,tempHeight):
    extraShadow = np.tan(sat_angle)*tempHeight
    return extraShadow

def cal_actualShadowLen(shadow,extraShadow):
    actualShadow = shadow + extraShadow
    return actualShadow

def get_calculatedHeight(sun_elevation, actualShadow):
    calculatedHeight = actualShadow * np.tan(sun_elevation)
    return calculatedHeight

tempHeight = cal_TempHeight(sun_elevation,shadow)
df['Temporary Height of Building'] = tempHeight

extraShadow = cal_extraShadow(sat_angle,tempHeight)
df['Extra Shadow'] = extraShadow

actualShadow = cal_actualShadowLen(shadow,extraShadow)
df['Actual Shadow'] = actualShadow

calculatedHeight = get_calculatedHeight(sun_elevation,actualShadow)
df['Calculated Height'] = calculatedHeight

print(df.head())