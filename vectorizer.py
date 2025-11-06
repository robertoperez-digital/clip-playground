import torch
import clip
from io import BytesIO
from PIL import Image

def get_image_embedding(imageStream):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device) # in a prod env you only want to do this once and keep the model in memory
    print("Model loaded on", device)
    image = preprocess(Image.open(BytesIO(imageStream))).unsqueeze(0).to(device)
    print("Image preprocessed")
    with torch.no_grad():
        image_features = model.encode_image(image)
        print("Image encoded")

    embedding = image_features[0].tolist()
    embedding_str = str(embedding).replace('\n', '')
    
    return embedding_str

def get_text_embedding(text):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device) # in a prod env you only want to do this once and keep the model in memory
    print("Model loaded on", device)
    text_inputs = clip.tokenize([text]).to(device)
    print("Text tokenized")
    with torch.no_grad():
        text_features = model.encode_text(text_inputs)
        print("Text encoded")

    embedding = text_features[0].tolist()
    embedding_str = str(embedding).replace('\n', '')
    
    return embedding_str