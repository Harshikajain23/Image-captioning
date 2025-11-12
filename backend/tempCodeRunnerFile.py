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