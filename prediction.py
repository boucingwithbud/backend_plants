from fastapi .routing import APIRouter
from fastapi import UploadFile, File
import joblib
import torch
from torch.nn.functional import softmax
from torchvision import models
from PIL import Image
import transformers
from transformers import pipeline
from accelerate import Accelerator
import boto3
from dotenv import load_dotenv
import os
import boto3

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

modeles = [
    'cafe_cacao_resnet152.pth',
    'cassava_resnet152.pth',
    'cashew_resnet152.pth',
    'rubber_resnet152.pth',
]

os.makedirs('models', exist_ok=True)

for model in modeles:
    local_path = f'models/{model}'
    if not os.path.exists(local_path):
        print(f"Téléchargement de {model}...")
        s3.download_file('backend-models-plants', model, local_path)
        print(f"{model} téléchargé.")
    else:
        print(f"{model} existe déjà, téléchargement ignoré.")

router = APIRouter(tags=["prediction"])

state_dict_café_cocoa = torch.load('models/cafe_cacao_resnet152.pth', map_location=torch.device('cpu'))
model_café_cacao = models.resnet152()
model_café_cacao.fc = torch.nn.Linear(in_features=model_café_cacao.fc.in_features, out_features=8)
model_café_cacao.load_state_dict(state_dict_café_cocoa)
class_names_café_cacao = joblib.load("café_cacao/classes_café_cacao.pkl")
class_to_idx_café_cacao = joblib.load("café_cacao/class_to_idx_café_cacao.pkl")
idx_to_class_café_cacao = {v: k for k,v in class_to_idx_café_cacao.items()}
transform_café_cacao =joblib.load('café_cacao/transforms_café_cacao.pkl')


state_dict_cassava = torch.load('models/cassava_resnet152.pth', map_location=torch.device('cpu'))
model_cassava = models.resnet152()
model_cassava.fc = torch.nn.Linear(in_features=model_cassava.fc.in_features, out_features=5)
model_cassava.load_state_dict(state_dict_cassava)
class_names_cassava = joblib.load("cassava/classes_cassava.pkl")
class_to_idx_cassava = joblib.load("cassava/class_to_idx_cassava.pkl")
idx_to_class_cassava = {v: k for k,v in class_to_idx_cassava.items()}
transform_cassava = joblib.load('cassava/transforms.pkl')


state_dict_cashew = torch.load('models/cashew_resnet152.pth', map_location=torch.device('cpu'))
model_cashew = models.resnet152()
model_cashew.fc = torch.nn.Linear(in_features=model_cashew.fc.in_features, out_features=5)
model_cashew.load_state_dict(state_dict_cashew)
class_names_cashew = joblib.load("cashew/classes_cashew.pkl")
class_to_idx_cashew = joblib.load("cashew/class_to_idx.pkl")
idx_to_class_cashew = {v: k for k,v in class_to_idx_cashew.items()}
transform_cashew = joblib.load('cashew/transforms.pkl')



model_4_url = "Doyourhomework/model_4_tomato"
accelerator = Accelerator()
pipeline_tomato = pipeline("image-classification", model=model_4_url)



model_5_url = "Doyourhomework/model_5_rice"
accelerator = Accelerator()
pipeline_rice = pipeline("image-classification", model=model_5_url)



model_6_url = "Doyourhomework/model_6_maize"
accelerator = Accelerator()
pipeline_maize = pipeline("image-classification", model=model_6_url)




state_dict_rubber_tree = torch.load('models/rubber_resnet152.pth', map_location=torch.device('cpu'))
model_rubber_tree = models.resnet152()
model_rubber_tree.fc = torch.nn.Linear(in_features=model_rubber_tree.fc.in_features, out_features=4)
model_rubber_tree.load_state_dict(state_dict_rubber_tree)
class_names_rubber_tree = joblib.load("Rubber tree/rubber_classes.pkl")
class_to_idx_rubber_tree = joblib.load("Rubber tree/rubber_class_to_idx.pkl")
idx_to_class_rubber_tree = {v: k for k,v in class_to_idx_rubber_tree.items()}
transform_rubber_tree = joblib.load('Rubber tree/rubber_transforms.pkl')









@router.post("/predict_model1_café_cacao")
def predict_model1(img: UploadFile = File(...) ):

    img = Image.open(img.file)
    img = img.convert('RGB')
    img = transform_café_cacao(img)
    img = img.unsqueeze(0)
    model_café_cacao.eval()
    with torch.no_grad():
        output = model_café_cacao(img)
        _, predicted = torch.max(output, 1)
        probabilities = softmax(output, dim = 1)
        return {"prediction": idx_to_class_café_cacao[predicted.item()], "probabilities": probabilities.tolist()}




@router.post("/predict_model2_cassava")
def predict_model2(img: UploadFile = File(...) ):
    img = Image.open(img.file)
    img = img.convert('RGB')
    img = transform_cassava(img)
    img = img.unsqueeze(0)
    model_cassava.eval()
    with torch.no_grad():
        output = model_cassava(img)
        _, predicted = torch.max(output, 1)
        probabilities = softmax(output, dim = 1)
        return {"prediction": idx_to_class_cassava[predicted.item()], "probabilities": probabilities.tolist()}




@router.post("/predict_model3_cashew")
def predict_model(img: UploadFile = File(...) ):
    img = Image.open(img.file)
    img = img.convert('RGB')
    img = transform_cashew(img)
    img = img.unsqueeze(0)
    model_cashew.eval()
    with torch.no_grad():
        output = model_cashew(img)
        _, predicted = torch.max(output, 1)
        probabilities = softmax(output, dim = 1)
        return {"prediction": idx_to_class_cashew[predicted.item()], "probabilities": probabilities.tolist()}
    


@router.post("/predict_model4_tomato")
def predict_model4(img: UploadFile = File(...)):
    
    image = Image.open(img.file).convert("RGB")

    result = pipeline_tomato(image)

    return {
        "prediction": result[0]["label"],
        "probability": result[0]["score"]
    }



@router.post("/predict_model5_rice")
def predict_model5(img: UploadFile = File(...)):
    
    image = Image.open(img.file).convert("RGB")

    result = pipeline_rice(image)

    return {
        "prediction": result[0]["label"],
        "probability": result[0]["score"]
    }




@router.post("/predict_model6_maize")
def predict_model6(img: UploadFile = File(...)):
    
    image = Image.open(img.file).convert("RGB")

    result = pipeline_maize(image)

    return {
        "prediction": result[0]["label"],
        "probability": result[0]["score"]
    }




@router.post("/predict_model7_rubber_tree")
def predict_model7(img: UploadFile = File(...) ):

    img = Image.open(img.file)
    img = img.convert('RGB')
    img = transform_rubber_tree(img)
    img = img.unsqueeze(0)
    model_rubber_tree.eval()
    with torch.no_grad():
        output = model_rubber_tree(img)
        _, predicted = torch.max(output, 1)
        probabilities = softmax(output, dim = 1)
        return {"prediction": idx_to_class_rubber_tree[predicted.item()], "probabilities": probabilities.tolist()}
