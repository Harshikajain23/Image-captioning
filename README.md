![Demo Screenshot](linkedin_final.JPG)

# Image Captioning – CNN-LSTM Model

Image Captioning is a deep learning-based web application that generates natural language descriptions for images. It uses a CNN (for feature extraction) and LSTM (for sequence modeling) architecture to generate accurate captions.

## Features

- Automatically generates captions for images
- Uses CNN-LSTM architecture for accurate captioning
- Upload your own images and get instant captions

## Tech Stack

## Frontend

- React.js
- Tailwind CSS

## Backend

- Python (Flask)
- TensorFlow / Keras

## Other

- CNN for feature extraction (VGG16 / ResNet)
- LSTM for sequence generation
- BLEU score evaluation for model performance

## Installation & Setup
Step 1: Clone the repository
```
git clone https://github.com/Harshkajain23/Image-captioning.git
```

## Step 2: Navigate to the project directory
```
cd image-captioning
```

## Step 3: Install dependencies

Backend
```
cd backend
pip install -r requirements.txt
```

Frontend
```
cd ../frontend
npm install
```


## Step 4: Run the application

Start backend
```
cd backend
python app.py
```

Start frontend
```
cd ../frontend
npm start
```


Frontend runs on: http://localhost:3000

Backend runs on: http://localhost:5000


