from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dropout, Dense, LSTM, Embedding, add
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.xception import Xception
from PIL import Image
import numpy as np
import pickle
import io

app = Flask(__name__)
CORS(app)

# --- Load tokenizer ---
with open("model/tokenizer.p", "rb") as f:
    tokenizer = pickle.load(f)

max_length = 32
vocab_size = len(tokenizer.word_index) + 1

# --- Define the LSTM model architecture ---
def define_model(vocab_size, max_length):
    # Image feature input
    inputs1 = Input(shape=(2048,), name='input_1')
    fe1 = Dropout(0.5)(inputs1)
    fe2 = Dense(256, activation='relu')(fe1)

    # Sequence input
    inputs2 = Input(shape=(max_length,), name='input_2')
    se1 = Embedding(vocab_size, 256, mask_zero=True)(inputs2)
    se2 = Dropout(0.5)(se1)
    se3 = LSTM(256)(se2)

    # Decoder model
    decoder1 = add([fe2, se3])
    decoder2 = Dense(256, activation='relu')(decoder1)
    outputs = Dense(vocab_size, activation='softmax')(decoder2)

    model = Model(inputs=[inputs1, inputs2], outputs=outputs)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model

# --- Load LSTM model ---
model = define_model(vocab_size, max_length)
model.load_weights('model/model.h5')

# --- Load Xception model for feature extraction ---
xception_model = Xception(include_top=False, pooling="avg")

# --- Extract features from PIL image ---
def extract_features(img, model):
    img = img.resize((299, 299))
    img_array = np.array(img)
    if img_array.shape[2] == 4:  # convert RGBA to RGB
        img_array = img_array[..., :3]
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 127.5
    img_array = img_array - 1.0
    features = model.predict(img_array)
    return features

# --- Map integer to word ---
def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

# --- Generate caption ---
def generate_desc(model, tokenizer, photo, max_length):
    in_text = 'start'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        pred = model.predict([photo, sequence], verbose=0)
        pred = np.argmax(pred)
        word = word_for_id(pred, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'end':
            break
    # remove start and end tokens
    final_caption = in_text.split()[1:]
    if final_caption[-1] == 'end':
        final_caption = final_caption[:-1]
    return ' '.join(final_caption)

# --- Flask route ---
@app.route("/generate_caption", methods=["POST"])
def generate_caption_api():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image_file = request.files['image']
    img = Image.open(io.BytesIO(image_file.read())).convert('RGB')
    
    # Extract features and generate caption
    photo_features = extract_features(img, xception_model)
    caption = generate_desc(model, tokenizer, photo_features, max_length)
    
    return jsonify({"caption": caption})

if __name__ == "__main__":
    app.run(debug=True)