import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from nltk import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from twilio.rest import Client
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
import json

tfidf = TfidfVectorizer()

def clean(dis):
    app_l=[]
    stopword= set(stopwords.words('english'))
    for val in dis:
       review = val[0].lower()
       review = re.sub('[-,./!@#$%^]'," ",review)
       review = word_tokenize(review)
       review = [v for v in review if not v in stopword]
       review = ' '.join(review)
       app_l.append(review)
    return app_l

def testing_algorithm(x_train,y_train):
    svc = SVC(kernel='rbf',degree=2)
    svc.fit(x_train,y_train)
    algo1 = str(svc.score(x_train,y_train))

    knn = KNeighborsClassifier(n_neighbors=50,leaf_size=50)
    knn.fit(x_train,y_train)
    algo2 = str(knn.score(x_train,y_train))

    dtc = DecisionTreeClassifier(max_depth=50,min_samples_split=5)
    dtc.fit(x_train,y_train)
    algo3 = str(dtc.score(x_train,y_train))
 
    rfc = RandomForestClassifier(max_depth=50,min_samples_split=5)
    rfc.fit(x_train,y_train)
    algo4 = str(rfc.score(x_train,y_train))
  
    adb = AdaBoostClassifier(n_estimators=80,learning_rate=1)
    adb.fit(x_train,y_train)
    algo5 = str(adb.score(x_train,y_train))
    
    print("Accuracy of SVC=> ",algo1)
    print("Accuracy of KNeighborsClassifier=>",algo2)
    print("Accuracy of DecisionTreeClassifier=>",algo3)
    print("Accuracy of RandomForestClassifier=>",algo4)
    print("Accuracy of AdaBoostClassifier=>",algo5)
    
def get_sms(que):
    account_sid = 'ACbb59adbd378263bdf673c15fcdd6c037'
    auth_token = '73e7843f2315dd26b49949c667ec4703'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                                  from_='+13202814192',
                                  body= que,
                                  to='+919087000556'
                              )

    print(message.sid)
def get_loc():
    send_url = 'http://api.ipstack.com/122.15.164.134?access_key=81bfc1791b638958108b037b7642ad11'
    req = requests.get(send_url)
    data = json.loads(req.text)
    
    lat = data['latitude']
    lon = data['longitude']
    add = data['city'] + ", " + data['region_name'] + ", " + data['zip']
    address = "Your location: Latitude: "+str(lat)+" Longitude: "+str(lon)+" Address: "+str(add)
    return address

def doct_loc():
    send_url1 = 'http://api.ipstack.com/122.15.164.134?access_key=81bfc1791b638958108b037b7642ad11'
    req = requests.get(send_url1)
    data = json.loads(req.text)
    lat = data['latitude']
    lon = data['longitude']
    send_url2 = 'https://api.betterdoctor.com/2016-03-01/doctors?location=37.773%2C-122.413%2C100&user_location=37.773%2C-122.413&skip=0&limit=10&user_key=a215b40d8a81855e83b468e64d7c87de'
    request = requests.get(send_url2)
    json_data = json.loads(request.text)
    
    name =[]
    latitude =[]
    longitude =[]
    distance = []
    address = []
    phone_no=[]
    for i in range(10):
        name.append(json_data['data'][i]['practices'][0]['name'])
        latitude.append(json_data['data'][i]['practices'][0]['lat'])
        longitude.append(json_data['data'][i]['practices'][0]['lon'])
        distance.append(json_data['data'][i]['practices'][0]['distance'])
        address.append(json_data['data'][i]['practices'][0]["visit_address"]["street"])
        phone_no.append(json_data['data'][i]['practices'][0]["phones"][0]['number'])
    
    add_dict={}
    for i in range(10):
        address = "Hospital Name: "+str(name[i]+'\n'+"Distnace:")
        add_dict[address]=distance[i]
    
    return sorted(add_dict.items(), key=lambda kv: kv[1])
    
    
def get_prediction(x_data_tfidf,y_data,y_dict,query):
    #testing_algorithm(x_data_tfidf,y_data)
    svc = SVC(kernel='rbf',degree=2)
    svc.fit(x_data_tfidf,y_data)
    #----------------------------------------------------
    loc = np.array([query])
    msg = tfidf.transform(loc.ravel())
    prediction = svc.predict(msg)
    #------------------------
    location = doct_loc()
    address = str()
    for loc in location:
        for i in loc:
            address+=str(i)+'\n'
    #------------------------
    er = str()
    flag=0
    for dis,ser in y_dict.items():
        if(ser == prediction[0]):
            er = dis
            flag=1
            break
    
    que=str()
    if(flag==1):
        que = str("You may have "+str(er)+'\n\n'+"Nearest doctor:"+'\n'+str(address))
        #que="hello"
    else:
        que = "System cannot understand you probleam"
    
    #get_sms(que)
    return que
#-------------------------------------------------
def detect_dis(disease):
#if __name__ == '__main__':
    data = pd.read_csv("clean_data.csv")
    dis = data.iloc[:,1:2].values
    sym = data.iloc[:,2].values   
    x_data = clean(dis)
    y_data = np.array(range(len(np.unique(sym))))
    
    
    x_data_tfidf= tfidf.fit_transform(x_data)
    y_dict = {n:i for i,n in enumerate(sym)} 
    #----------------------------------------------------
    query=(disease)
    #----------------------------------------------------
    result = get_prediction(x_data_tfidf,y_data,y_dict,query)
    #print(result)
    return(result)#"i have fever,vommiting from morning"
    