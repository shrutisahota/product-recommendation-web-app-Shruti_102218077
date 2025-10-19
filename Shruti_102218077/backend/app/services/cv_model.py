import os, torch
from torchvision import transforms
from PIL import Image

LABELS = ["chair","table","sofa","bed","cabinet","lamp","shelf","stool","bench","desk"]

_model = None
_device = "cuda" if torch.cuda.is_available() else "cpu"
_transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

def _try_load_model():
    global _model
    if _model is not None: 
        return
    model_path = os.environ.get("CV_MODEL_PATH", "/content/models/cv.pt")
    if os.path.exists(model_path):
        _model = torch.jit.load(model_path, map_location=_device)
        _model.eval()

def predict_image(path: str):
    _try_load_model()
    if _model is None:
        return None  # fallback handled by metadata predictor
    img = Image.open(path).convert("RGB")
    x = _transform(img).unsqueeze(0).to(_device)
    with torch.no_grad():
        logits = _model(x)
        probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
    idx = int(probs.argmax())
    return LABELS[idx], float(probs[idx])

def predict_from_metadata(title: str, categories: str|None):
    text = (title or "") + " " + (categories or "")
    t = text.lower()
    for lab in LABELS:
        if lab in t:
            return lab, 0.78
    return "furniture", 0.45
