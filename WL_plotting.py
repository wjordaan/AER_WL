df=pd.DataFrame(columns=['LIC','COMP','WELL','SURF_LOC','UWI','FIELD','DEPTH','GL','NORTH','EAST','TYPE','PROD'])

import os

Folder = os.path.join('C:\\','1AER')
for root, dirs, files in os.walk(Folder, topdown=False):
    for name in files:
        if '.txt'.lower() in name.lower():
            if 'WELL'.lower() in name.lower():
                try:
                    with open(os.path.join(root,name),'r') as f:
                        searchlines = f.readlines()
                    with open(os.path.join(root,name),'r') as f:
                        searchtext = f.read()
                        
                        print(name,dirs[0])
                        df=build_df(searchlines,searchtext,df)
                        print('###')
                        
                except:
                    pass
                   

#for file in Folder:
    #with open(file,'r') as f:
        #searchlines = f.readlines()
        #searchtext = f.read()
        #build_df(searchlines,searchtext,df)
df


############################
def build_df(searchlines,searchtext,df):
    
    import pandas as pd
    import re
    regex = re.compile(r'(\d{7})')

    string = re.compile('AMENDMENTS OF WELL LICENCES')
    temp = string.search(searchtext)
    #print(temp)
    start = temp.span()[0]
    #print(start)
    lic_temp = re.findall(regex,searchtext[:start])


    for lic in lic_temp:
        lic_lines=[]
        x=0
        for i, line in enumerate(searchlines):
            if str(lic) in line:
                for l in searchlines[i+1:i+30]:
                    if not re.search(r'(\d{7})',l):
                        x +=1
                        lic_lines = searchlines[i:i+x]
                    else:
                        break
        regex = re.compile(r'[\S]{1,50}')

        l0 = re.findall(regex,lic_lines[0])
        l1 = re.findall(regex,lic_lines[1])
        l2 = re.findall(regex,lic_lines[2])
        l3 = re.findall(regex,lic_lines[3])
        l4 = re.findall(regex,lic_lines[4])


        df_temp=pd.DataFrame({
            'LIC':lic,
            'COMP':(' '.join(l4[:-1])),
            'WELL':(' '.join(l0[:-4])),
            'SURF_LOC':l4[-1],
            'UWI':l1[0],
            'FIELD':l2[-2],
            'DEPTH':l1[-1],
            'GL':l0[-1],
            'NORTH':' '.join(l1[-7:-5]),
            'EAST':(' '.join(l1[-5:-3])),
            'TYPE':l3[-2],
            'PROD':l3[-1]
            },
            index=[lic])

        df=pd.concat([df,df_temp])
        print('TEMP',df_temp['LIC'][0],df_temp['COMP'][0],start)
        print('DF',df['LIC'][-1],df['COMP'][-1],len(df))
    return df
###################

def get_latlong(sec_val,sub_div,twn_val,rng_val,mer_val):
    
    import requests,bs4
    string = 'https://geocoder.ca/' +sec_val+'-'+sub_div+'-'+twn_val+'-'+rng_val+'-'+mer_val
    res=requests.get(string)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "lxml")
    longt = soup.find_all(attrs={'name':'longt'})[0]['value']
    latt = soup.find_all(attrs={'name':'latt'})[0]['value']
    return (latt,longt)
	
	
###################

def conv_LSD(df,counter):    
    df_add=pd.DataFrame(columns=['LATT','LONGT'])
    for l in df.index:
        sec=int(df.loc[l]['SURF_LOC'][0:2])
        sub_div =df.loc[l]['SURF_LOC'][3:5]
        twn_val =df.loc[l]['SURF_LOC'][6:9]
        rng_val =df.loc[l]['SURF_LOC'][10:12]
        mer_val =df.loc[l]['SURF_LOC'][12:14]
        if sec == 15 or sec == 16 or sec == 9 or sec == 10:
            sec_val = 'NE'
        elif sec == 13 or sec == 14 or sec == 11 or sec == 12:
            sec_val ='NW'
        elif sec == 5 or sec == 6 or sec == 4 or sec == 3:
            sec_val ='SW'
        elif sec == 1 or sec == 2 or sec == 7 or sec == 8:
            sec_val ='SE'
        print(counter,l,sec,sec_val,'-',sub_div,'-',twn_val,'-',rng_val,'-',mer_val)
        counter=counter+1
        latt,longt = get_latlong(sec_val,sub_div,twn_val,rng_val,mer_val)

        df_temp=pd.DataFrame({'LATT':latt,'LONGT':longt},index=[l])

        df_add=pd.concat([df_add,df_temp])

    df['LATT']=df_add['LATT']
    df['LONGT']=df_add['LONGT']
    return df
	
###########

from  plotly import  __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=True)

#import plotly.plotly as py
import pandas as pd

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')
#df.head()


df['TEXT'] = df['LIC'] + ' | ' + df['UWI']+' | '+df['COMP']

scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
    [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]

data = [ dict(
        type = 'scattergeo',
        locationmode = 'ISO-3',
        lon = df['LONGT'],
        lat = df['LATT'],
        text = df['TEXT'],
        mode = 'markers',
        marker = dict(
            size = 5,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'circle',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale = scl,
            cmin = min(df['DEPTH']),
            cmax = max(df['DEPTH']),
            colorbar=dict(
                title="Depth"
            )
        ))]

layout = dict(
        title = 'WCR - 2018 Wells',
        colorbar = True,
        geo = dict(
            scope='north america',
            projection=dict( type='Mercator' ),
            showland = True,
            showcountries = True,
            showsubunits = True,
            resolution = 50,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(191, 191, 191)",
            countrycolor = "rgb(191, 191, 191)",
            countrywidth = 0.5,
            subunitwidth = 0.5,
            
            lonaxis = dict(
            showgrid = True,
            gridwidth = 0.5,
            range= [ -140.0, -100.0 ],
            dtick = 5
            ),
            
            lataxis = dict (
            showgrid = True,
            gridwidth = 0.5,
            range= [ 50.0, 60.0 ],
            dtick = 5
            )
        ),
    )

fig = dict( data=data, layout=layout )
iplot( fig, validate=False, filename='WCR-Wells' )
