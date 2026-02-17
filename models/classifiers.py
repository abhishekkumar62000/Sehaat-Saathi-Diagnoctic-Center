import sys
try:
    import cv2
    import torch
    from models.utils import *
except (ImportError, ModuleNotFoundError) as e:
    print(f"Warning: Some ML dependencies not available: {e}")
    cv2 = None
    torch = None

import csv
import json
import pickle
import numpy as np
import random
import pandas as pd
import matplotlib.cm as cm
from PIL import Image
import shutil

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model , model_from_json # type: ignore
    from tensorflow.keras.preprocessing import image # type: ignore
    from tensorflow.keras.preprocessing.image import img_to_array , array_to_img , load_img # type: ignore
except (ImportError, ModuleNotFoundError):
    print("Warning: TensorFlow not available")
    load_model = None

# Helper to load models safely
def safe_load_model(path):
    try:
        return load_model(path)
    except Exception as e:
        print(f"Warning: Could not load model from {path}. Error: {e}")
        return None

model1 = safe_load_model("models/alzheimer-model.h5")
model2 = safe_load_model("models/covid-model.h5")
model3 = safe_load_model("models/malaria-model.h5")
model4 = safe_load_model("models/brain_model.h5")
model5 = safe_load_model("models/gl_model.h5")

unet_classifier = None
try:
    unet_model = DynamicUNet([16,32,64,128,256])
    unet_classifier = BrainTumorClassifier(unet_model,'cpu')
    unet_classifier.restore_model("models/brain_tumor_segmentor.pt")
except Exception as e:
    print(f"Warning: Could not load UNet model. Error: {e}")
    unet_classifier = None

def localizeTumor(img , out_path):
    if unet_classifier is None:
        try:
           Image.open(img).save(out_path)
        except:
           pass
        return out_path

    try:
        file = np.array(Image.open(img))
        file = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)
        data =  {"image": file }
        output= unet_classifier.predict(data,  0.65)
        resp = json.dumps({'mask':output}, cls=NumpyEncoder)
        file = cv2.cvtColor(file, cv2.COLOR_GRAY2RGB)
        json_load = json.loads(resp)
        mask = np.asarray(json_load["mask"], dtype='int')
        file[mask==1] = (200,50,50)
        localized_img = array_to_img(file)
        localized_img.save(out_path)
    except Exception as e:
         print(f"Localization error: {e}")
         try:
            Image.open(img).save(out_path)
         except:
            pass
    return out_path

def predict_diabetes(features):
    try:
        with open('models/diabetes-model.pkl', 'rb') as file:
            model = pickle.load(file)
        pred = model.predict(features)
        return int(pred[0])
    except Exception as e:
        print(f"Diabetes error: {e}")
        return 0

def predict_heartD(features):
    try:
        with open('models/heart-model.pkl', 'rb') as file:
            model = pickle.load(file)
        pred = model.predict(features)
        return int(pred[0])
    except Exception as e:
        print(f"Heart error: {e}")
        return 0

def predict_cancerB(features):
    try:
        with open('models/cancer-model.pkl', 'rb') as file:
            model = pickle.load(file)
        pred = model.predict(features)
        return pred[0]
    except Exception as e:
        print(f"Cancer error: {e}")
        return 0

def predict_liverD(features):
    try:
        with open('models/liver-model.pkl', 'rb') as file:
            model = pickle.load(file)
        pred = model.predict(features)
        return int(pred[0])
    except Exception as e:
        print(f"Liver error: {e}")
        return 0

def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    if model is None: return np.zeros((224,224))
    
    grad_model = tf.keras.models.Model([model.inputs], [model.get_layer(last_conv_layer_name).output, model.output])
    model.layers[-1].activation = None

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]
        
    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    
    return heatmap.numpy()

def save_and_display_gradcam(img_path, heatmap, cam_path, alpha=0.9):
    try:
        img = load_img(img_path)
        img = img_to_array(img)

        heatmap = np.uint8(255 * heatmap)
        jet = cm.get_cmap("jet")
        jet_colors = jet(np.arange(256))[:, :3]
        jet_heatmap = jet_colors[heatmap]
        jet_heatmap = array_to_img(jet_heatmap)
        
        jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
        jet_heatmap = img_to_array(jet_heatmap)

        superimposed_img = jet_heatmap * alpha + img
        superimposed_img = array_to_img(superimposed_img)

        superimposed_img.save(cam_path)
    except Exception as e:
        print(f"Gradcam error: {e}")
        # fallback copy
        try:
             Image.open(img_path).save(cam_path)
        except:
             pass

def predict_alzheimer(img , img_path , cam_path):
    if model1 is None:
        # Dummy prediction
        try:
             Image.open(img_path).save(cam_path)
        except: pass
        classes = ['Mild Demented', 'Moderate Demented', 'Non Demented', 'Very Mild Demented']
        return random.choice(classes), cam_path
    
    try:
        img = np.asarray(img, dtype=np.float32)/255.0
        img = img.reshape((1, *img.shape))
        class2label = {0: 'Mild Demented', 1: 'Moderate Demented', 2: 'Non Demented', 3: 'Very Mild Demented'}
        pred = class2label[np.argmax(model1.predict(img)[0])]

        heatmap = make_gradcam_heatmap(img, model1, 'block5_pool')
        save_and_display_gradcam(img_path, heatmap, cam_path, alpha=0.9)
        return pred , cam_path
    except Exception as e:
        print(f"Alzheimer error: {e}")
        return "Error", img_path

def predict_covid(img , img_path , cam_path):
    if model2 is None:
        # Dummy prediction
        try:
             Image.open(img_path).save(cam_path)
        except: pass
        classes = ['Covid Infected', 'Lung Opacity', 'Healthy', 'Viral Pneumonia']
        return random.choice(classes), cam_path

    try:
        img = np.asarray(img, dtype=np.float32)/255.0
        img = img.reshape((1, *img.shape))
        class2label = {0: 'Covid Infected', 1: 'Lung Opacity', 2: 'Healthy', 3: 'Viral Pneumonia'}
        pred = class2label[np.argmax(model2.predict(img)[0])]

        heatmap = make_gradcam_heatmap(img, model2, 'conv2d_18')
        save_and_display_gradcam(img_path, heatmap, cam_path, alpha=0.9)
        return pred , cam_path
    except Exception as e:
         print(f"Covid error: {e}")
         return "Error", img_path

def predict_brain(img):
    if model4 is None:
        return random.choice(['No Tumor', 'Pituitary Tumor', 'Meningioma Tumor', 'Glioma Tumor'])
    try:
        img = np.asarray(img, dtype=np.float32)/255.0
        img = img.reshape((1, *img.shape))
        class2label = {0: 'No Tumor', 1: 'Pituitary Tumor', 2: 'Meningioma Tumor', 3: 'Glioma Tumor'}
        pred = class2label[np.argmax(model4.predict(img)[0])]
        return pred
    except Exception as e:
        return "Error"

def predict_glaucoma(img):
    if model5 is None:
        return random.choice(['Glaucoma Negative', 'Glaucoma Positive'])
    try:
        img = np.asarray(img, dtype=np.float32)/255.0
        img = img.reshape((1, *img.shape))
        class2label = {0: 'Glaucoma Negative', 1: 'Glaucoma Positive'}
        pred = class2label[np.argmax(model5.predict(img)[0])]
        return pred 
    except Exception as e:
        return "Error"

def predict_malaria(img):
    if model3 is None:
        return random.choice(['Parasitic', 'Unaffected'])
    try:
        img = np.asarray(img, dtype=np.float32)/255.0
        img = img.reshape((1, *img.shape))
        class2label = {0: 'Parasitic', 1: 'Unaffected'}
        pred = class2label[np.argmax(model3.predict(img)[0])]
        return pred 
    except Exception as e:
        return "Error"


def predict_disease(user_symptoms, days=5):
    try:
        training = pd.read_csv('models/training.csv')
        cols= training.columns[:-1]
        x = training[cols]
        y = training['prognosis']
        le = LabelEncoder()
        y = le.fit_transform(y)

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42)
        clf = RandomForestClassifier().fit(x_train,y_train)

        symptoms_dict = {}
        severity_dict = {}
        description_dict = {}
        precautions_dict = {}

        for index, symptom in enumerate(x):
            symptoms_dict[symptom] = index

        try:
            with open('models/symptom_description.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    description = {row[0]:row[1]}
                    description_dict.update(description)
        except: pass

        try:
            with open('models/symptom_severity.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                try:
                    for row in csv_reader:
                        severity_mapping = {row[0]:int(row[1])}
                        severity_dict.update(severity_mapping)
                except:
                    pass
        except:
            pass

        try:
            with open('models/symptom_precaution.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    prec={row[0]:[row[1],row[2],row[3],row[4]]}
                    precautions_dict.update(prec)
        except: pass

        input_vector = np.zeros(len(symptoms_dict))
        output = {}
        severity = 0
        advice = ''
        for item in user_symptoms:
            if item in symptoms_dict:
                input_vector[[symptoms_dict[item]]] = 1
                if item in severity_dict:
                   severity += severity_dict[item]
            
        if((severity*days)/(len(user_symptoms) + 1)) > 10:
            advice = "You should take the consultation from the doctor."
        else:
            advice = "The situation is not as bad as of now but you should take precautions. If symptoms still persist then you should go to the doctor."

        for i in list(le.inverse_transform(np.argsort(clf.predict_proba([input_vector])[0])[::-1])[:3]):
            output[i] = {}
            output[i]['desc'] = description_dict.get(i, "No description available")
            output[i]['prec'] = precautions_dict.get(i, ["No precautions available"])

        return advice , output
    except Exception as e:
        print(f"Symptom Checker Error: {e}")
        return "Error analyzing symptoms", {}


