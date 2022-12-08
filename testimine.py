import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def mudelisample(data, test_data, test_station_IDs):
    
    mudel_list = []
    atribuut_list = []
    prediction_list = []
    train_y = data["compliance_2021"]
    data = data.drop(columns=["compliance_2021"])
    pikkus = len(data.columns)
    columns = data.columns
    
    for kogus in [5,10,15]:
        # Reguleerib sammu
        for samm in range(1,8):
            # Reguleerib stardipukki

            for stardipukk in range(samm):
                hetkeindeks = stardipukk
                # Reguleerib lõpetamistingimust
                while hetkeindeks < pikkus:
                    ajutine_list = []
                    ajutine_data = pd.DataFrame()
                    ajutine_test_data = pd.DataFrame()
                    # Reguleerib ühte mudelit
                    for k in range(kogus):

                        if hetkeindeks >= pikkus:
                            break

                        ajutine_list.append(hetkeindeks)
                        ajutine_data[columns[hetkeindeks]] = data[columns[hetkeindeks]]
                        
                        ajutine_test_data[columns[hetkeindeks]] = test_data[columns[hetkeindeks]]

                        hetkeindeks += samm

                    ajutine_data["compliance_2021"] = train_y
                    ajutine_data = ajutine_data.dropna()
                    
                    ajutine_test_data["station_id"] = test_station_IDs
                    ajutine_test_data = ajutine_test_data.dropna()
                    stationIDs = ajutine_test_data["station_id"]
                    ajutine_test_data = ajutine_test_data.drop(columns=["station_id"])
                    
                    ## Kui ennustusi liig-vähe, viskame minema
                    if len(ajutine_test_data) < 3:
                        continue
                    
                    ajutine_train_y = ajutine_data["compliance_2021"]
                    ajutine_data = ajutine_data.drop(columns=["compliance_2021"])

                    rf = RandomForestClassifier(n_estimators=100, max_depth=4, random_state=0).fit(ajutine_data, ajutine_train_y)
                    
                    prediction = pd.DataFrame(rf.predict(ajutine_test_data))
                    prediction["station_id"] = stationIDs
                    prediction.columns = ["compliance_2021","station_id"]
                    
                    prediction_list.append(prediction)
                    mudel_list.append(rf)
                    atribuut_list.append(ajutine_list)
                
    
    return (mudel_list, atribuut_list, prediction_list)

ilma_station_id = train_data.drop(columns=["station_id"])
test_ilma_station_id = test_data.drop(columns=["station_id"])
ennik = mudelisample(ilma_station_id, test_ilma_station_id, stationIDtest)

mudel_list = ennik[0]
atribuut_list = ennik[1]
predictions = ennik[2]

for i in range(len(predictions)):
    if len(atribuut_list[i]) > 2:
           usable_predictions.append(predictions[i])

print(predictions)