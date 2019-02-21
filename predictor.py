import datetime
import time

def soil():
    import serial
    tosend=0
    arduino=serial.Serial("COM6",9600)
    inputs=7
    count=0
    rawdata=[]
    f=[]
    while(count<inputs):
        rawdata.append(str(arduino.readline()))
        count=count+1
    #print (rawdata)
    raw=str(rawdata)
    r=raw.split('\'')
    for i in range (1,len(r),2):
        f.append(r[i])
    f=str(f)
    #print (f)
    f=f.split('\'')
    for i in range(1,len(f),2):
        z=f[i]
        rawdata.append(z[:2])
    for i in range(inputs,len(rawdata),1):
        #print (rawdata[i])
        tosend=tosend+float(rawdata[i])
    return (tosend/7)
    

def water_level():
    import serial
    tosend=0
    arduino=serial.Serial("COM4",9600)
    inputs=7
    rawdata=[]
    count=0
    f=[]
    while (count<inputs):
        rawdata.append(str(arduino.readline()))
        count=count+1
    #print (rawdata)
    raw=str(rawdata)
    r=raw.split('\'')
    for i in range (1,len(r),2):
        f.append(r[i])
    f=str(f)
    #print (f)
    f=f.split('\'')
    for i in range(1,len(f),2):
        z=f[i]
        rawdata.append(z[:4])
    for i in range(inputs,len(rawdata),1):
        #print (rawdata[i])
        tosend=tosend+float(rawdata[i])
    return (tosend/7)


def weather():
    tosend=[]
    time=[]
    import forecastio
    api_key="<Insert API key here>"
    lat=23.2599
    lng=77.4126
    #extendHourly=True
    forecast=forecastio.load_forecast(api_key, lat, lng)
    byday=forecast.daily()
    for day in byday.data:
        #print(day.precipProbability)
        tosend.append(day.precipProbability)
        time.append(str(day.time))
    print ("API used")
    return time, tosend
    
x,y=weather()
#print (x)
#print (y)
#soil()
water_level=water_level()
soil=soil()

def data():
    import pandas as pd
    df=pd.read_csv('dist.txt')
    print (df.head())
#data()
import warnings
warnings.filterwarnings('ignore')
def coastal():
    print ("warning levels for coastal areas\n")
    print ("Predictions:\nIn order of:\nDate and time\tprediction level    water level   rainfall possibility\n")
    with open('data.txt','a',encoding='utf-8') as f:
        f.write("\n        Warning levels for coastal areas:\n")
        f.write("\n\nPredictions for dates            Danger level\n\n")
    f.close()
    import pandas as pd
    df=pd.read_csv('dist.txt')
    data=df.iloc[:,0:2]
    #print (data)
    label=df[['alert']]
    #print (label)
    from sklearn.linear_model import LogisticRegression #try regression here
    clf=LogisticRegression(random_state=0, solver='lbfgs',multi_class='multinomial')
    clf=clf.fit(data, label)
    for i in range(0,8,1):
        c=[water_level,y[i]]
        pred=clf.predict([c])
        print(x[i],"\t",pred,"\t",water_level,"\t",y[i])
        with open ('data.txt','a', encoding='utf-8') as f:
            f.write(x[i])
            f.write('                  ')
            f.write(str(pred))
            f.write('\n')
    f.close()
    
#coastal()
def merge():
    print ("Predictions:\nIn order of:\nDate and time\tprediction level    water level      soil moisture   rainfall possibility\n")
    with open('data.txt','a',encoding='utf-8') as f:
        f.write("\nWarning levels for low-lying areas:\t")
    f.close()
    import pandas as pd
    df=pd.read_csv('dist.txt')
    data=df.iloc[:,0:2]
    #print (data)
    
    df1=pd.read_csv('soil.txt')
    datasoil=df1.iloc[:,0:1]
    frames=[data,datasoil]
    dataf=pd.concat(frames, axis=1)
    #print (dataf)
    label=df1[['alert']]
    #print (label)
    from sklearn import tree
    clf=tree.DecisionTreeClassifier()
    clf=clf.fit(dataf, label)
    for i in range(0,8,1):
        c=[water_level,y[i],soil]
        pred=clf.predict([c])
        print(x[i],"\t",pred,"\t",water_level,"\t",soil,"\t",y[i])
#merge()
    
def low():
    print ("Predictions for inland areas:")
    print ("Predictions:\nIn order of:\nDate and time\tprediction level    water level      soil moisture   rainfall possibility\n")
    with open('data.txt','a',encoding='utf-8') as f:
        f.write("\n\n    Warning levels for low-lying inland areas:\n")
        f.write("\n\nPredictions for dates            Danger level\n\n")
    f.close()
    import pandas as pd
    df=pd.read_csv('dist.txt')
    data=df.iloc[:,0:2]
    #print (data)
    
    df1=pd.read_csv('soil.txt')
    datasoil=df1.iloc[:,0:1]
    frames=[data,datasoil]
    dataf=pd.concat(frames, axis=1)
    #print (dataf)
    label=df1[['alert']]
    #print (label)
    from sklearn.linear_model import LogisticRegression #try regression here
    clf=LogisticRegression(random_state=0, solver='lbfgs',multi_class='multinomial')
    clf=clf.fit(dataf, label)
    for i in range(0,8,1):
        c=[water_level,y[i],soil]
        pred=clf.predict([c])
        print(x[i],"\t",pred,"\t",water_level,"\t",soil,"\t",y[i])
        with open ('data.txt','a', encoding='utf-8') as f:
            f.write(x[i])
            f.write('                  ')
            f.write(str(pred))
            f.write('\n')
    f.close()
#low()
def main():
    now=datetime.datetime.now()
    with open('data.txt','w',encoding='utf-8') as f:
        f.write("\nValues predicted at current timing ")
        f.write(str(now))
        f.write("\n\n")
    f.close()
    coastal()
    low()

for i in range(10):
    main()
    time.sleep(5)
