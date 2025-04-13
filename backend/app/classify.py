from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import io

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

themes = [
    "travel and sightseeing",
    "wedding ceremony",
    "first birthday party",
    "family gathering at home",
    "friends gathering or party",
    "company event or meeting",
    "graduation or school ceremony",
    "concert or stage performance",
    "pets and animals",
    "sports and fitness activity",
    "food and dining",
    "landscape or nature",
    "birthday celebration",
    "baby and toddler",
    "night view or city lights",
    "museum or exhibition",
    "school life",
    "religious or spiritual event",
    "camping or outdoor activity",
    "beach and swimming",
    "mountains and hiking",
    "winter snow scenery",
    "autumn foliage",
    "spring flowers or cherry blossoms"
]

label_translation = {
    "travel and sightseeing": "여행",
    "wedding ceremony": "결혼식",
    "first birthday party": "돌잔치",
    "family gathering at home": "가족 모임",
    "friends gathering or party": "친구 모임",
    "company event or meeting": "회사 행사",
    "graduation or school ceremony": "졸업/입학식",
    "concert or stage performance": "콘서트/공연",
    "pets and animals": "반려동물",
    "sports and fitness activity": "운동/스포츠",
    "food and dining": "음식",
    "landscape or nature": "자연/풍경",
    "birthday celebration": "생일 파티",
    "baby and toddler": "아기/유아",
    "night view or city lights": "야경/도시 조명",
    "museum or exhibition": "박물관/전시",
    "school life": "학교생활",
    "religious or spiritual event": "종교 행사",
    "camping or outdoor activity": "캠핑/야외 활동",
    "beach and swimming": "해변/수영",
    "mountains and hiking": "산/등산",
    "winter snow scenery": "겨울/눈 풍경",
    "autumn foliage": "가을 단풍",
    "spring flowers or cherry blossoms": "봄꽃/벚꽃"
}


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

        eng_label = themes[max_idx]
        kor_label = label_translation.get(eng_label, "알 수 없음")

        results.append({
            "filename": file.filename,
            "label": kor_label,  # ✅ 한글 라벨로 출력
            "confidence": round(float(probs[max_idx]), 2)
        })
    return results

# async def classify_images(files):
#     results = []
#     for file in files:
#         image_bytes = await file.read()
#         image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
#         inputs = processor(text=themes, images=image, return_tensors="pt", padding=True)
#         outputs = model(**inputs)
#         logits = outputs.logits_per_image
#         probs = logits.softmax(dim=1).detach().cpu().numpy()[0]
#         max_idx = int(probs.argmax())
#         results.append({
#             "filename": file.filename,
#             "label": themes[max_idx],
#             "confidence": round(float(probs[max_idx]), 2)
#         })
#     return results
