from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import io

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

themes = [
    "wedding ceremony",
    "birthday party",
    "travel scenery",
    "family photo",
    "graduation event",
    "food shot",
    "pet picture",
    "business event"
]

async def classify_images(files):
    results = []
    for file in files:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        inputs = processor(text=themes, images=image, return_tensors="pt", padding=True)
        outputs = model(**inputs)
        logits = outputs.logits_per_image
        probs = logits.softmax(dim=1).detach().cpu().numpy()[0]
        max_idx = int(probs.argmax())
        results.append({
            "filename": file.filename,
            "label": themes[max_idx],
            "confidence": round(float(probs[max_idx]), 2)
        })
    return results
