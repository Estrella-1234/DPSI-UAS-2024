import tensorflow as tf
import numpy as np

class_names = [
    "Onion",
    "Garlic",
    "Chilli",
    "Chicken",
    "Tofu",
    "Egg",
    "Tempeh",
    "Tomato",
]
model = tf.keras.models.load_model("model.h5")


def preprocess_image(image_path):
    image = tf.keras.utils.load_img(image_path, target_size=(224, 224))
    image = tf.keras.utils.img_to_array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image


def predict_image(image_path, threshold=0.8):
    image = preprocess_image(image_path)
    prediction = model.predict(image)
    class_index = np.argmax(prediction)
    class_name = class_names[class_index]
    confidence = float(prediction[0][class_index])

    if confidence < threshold:
        class_name = "Unknown"
        confidence = 1 - confidence

    return class_name, confidence
