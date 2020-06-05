def train():
    import numpy as np
    from sklearn.externals import joblib

    import pandas as pd
    df = pd.read_csv('test_points.csv')#, skiprows=1)
    
    df.dropna(inplace=True)
    
    data = df[['W_speed', 'S1', 'S2', 'S3']]
    position = df[['waveX', 'waveY']]
    
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    
    data_train, data_test, pos_train, pos_test = train_test_split(data, position, random_state=13)
    
    model = LinearRegression()
    
    model.fit(data_train, pos_train)
    print(f'\n\tSCORE:\t{model.score(data_test, pos_test)}')

    # coeficientes = model.coef_
    # print(f'\nCoef:\n\t{coeficientes}')
    
    to_predict = [10, 20, 8, 0]
    predecir = np.array(to_predict).reshape(1,-1)
    print(F'\nLA PREDICCION ES:\n\t{model.predict(predecir)}\n')
    
    joblib.dump(model, 'trained_model.pkl')
    print('Saved!')

    return df

def predict(wave_speed, S):#S son diccionarios con posicion y activacion
    import numpy as np
    import joblib
    model_loaded = joblib.load('trained_model.pkl')
    S1,S2,S3=S
    S1=S1[-1]
    S2=S2[-1]
    S3=S3[-1]
    values = np.array([wave_speed, S1, S2, S3]).reshape(1,-1)
    predicted = model_loaded.predict(values)
    pX = predicted[0][0]
    pY = predicted[0][1]
    return pX,pY

if __name__=='__main__':
    dataframe=train()

