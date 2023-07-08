from fastapi import FastAPI
import mlflow
import pandas as pd
from pydantic import BaseModel
import uvicorn
import sys
import os

app = FastAPI()

os.environ["AWS_ACCESS_KEY_ID"] = ''
os.environ["AWS_SECRET_ACCESS_KEY"] = ''
os.environ["AWS_DEFAULT_REGION"] = ''


mlflow.set_tracking_uri('') 

model_name = sys.argv[1]
stage = 'Production'
model = mlflow.pyfunc.load_model(model_uri=f'models:/{model_name}/{stage}')


class DataPredict(BaseModel):
    posted_on: str = '2022-07-04'
    bhk: float = 2
    size: float = 1100
    floor: str = '1 out of 3'
    area_type: str = 'Carpet Area	'
    area_local: str = 'Bandel'
    city: str = 'Kolkata'
    furnishing_status: str = 'Unfurnished'
    tenant_pref: str = 'Bachelors'
    bathroom: int = 4
    point_of_contact: str = "Contact Owner"


def create_df(data):
    input_df = pd.DataFrame(data)
    input_df = input_df.set_index([0]).transpose()
    input_df = input_df.rename(columns={
        'posted_on': 'Posted On',
        'bhk': 'BHK',
        'size': 'Size',
        'floor': 'Floor',
        'area_type': 'Area Type',
        'area_local': 'Area Locality',
        'city': 'City',
        'furnishing_status': 'Furnishing Status',
        'tenant_pref': 'Tenant Preferred',
        'bathroom': 'Bathroom',
        'point_of_contact': 'Point of Contact'
    })
    return input_df


@app.post('/predict')
def prediction(data: DataPredict):
    data = create_df( data )
    prediction = model.predict(data)
    response = {'prediction': prediction[0]}
    return response


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)









