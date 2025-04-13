# 📁 backend/app/slideshow.py

import os
import io
import tempfile
from typing import List
from fastapi import UploadFile
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
from moviepy.editor import ImageClip, concatenate_videoclips

def parse_prompt(prompt: str):
    style = {
        "fontsize": 36,
        "color": (255, 255, 255),  # RGB for PIL
        "bg_color": (0, 0, 0),
        "font": "arial.ttf"
    }
    if "감성" in prompt or "느리게" in prompt:
        style["fontsize"] = 40
    if "강조" in prompt or "빨강" in prompt:
        style["color"] = (255, 0, 0)
    return style

async def generate_slideshow(files: List[UploadFile], prompt: str) -> str:
    style = parse_prompt(prompt)
    total_duration = 10  # 전체 영상 길이 (초)
    num_images = len(files)
    if num_images == 0:
        raise ValueError("No images provided.")

    duration_per_image = total_duration / num_images
    fade_duration = 0.5

    temp_dir = tempfile.mkdtemp()
    clips = []

    for idx, file in enumerate(files):
        image_bytes = await file.read()
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # 비율 유지하며 FHD에 맞게 검정 베젤 삽입
        target_size = (1920, 1080)
        img_ratio = img.width / img.height
        target_ratio = target_size[0] / target_size[1]

        if img_ratio > target_ratio:
            new_width = target_size[0]
            new_height = int(new_width / img_ratio)
        else:
            new_height = target_size[1]
            new_width = int(new_height * img_ratio)

        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        background = Image.new("RGB", target_size, style["bg_color"])
        offset = ((target_size[0] - new_width) // 2, (target_size[1] - new_height) // 2)
        background.paste(resized_img, offset)

        # 텍스트 추가
        text = f"장면 {idx + 1}"
        draw = ImageDraw.Draw(background)
        try:
            pil_font = ImageFont.truetype(style["font"], style["fontsize"])
        except:
            pil_font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=pil_font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        text_x = (background.width - text_w) // 2
        text_y = background.height - text_h - 30
        draw.text((text_x, text_y), text, font=pil_font, fill=style["color"])

        frame_path = os.path.join(temp_dir, f"frame_{idx}.png")
        background.save(frame_path)

        clip = ImageClip(frame_path).set_duration(duration_per_image)
        if fade_duration * 2 < duration_per_image:
            clip = clip.crossfadein(fade_duration).crossfadeout(fade_duration)

        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")
    output_path = os.path.join(temp_dir, "slideshow.mp4")
    video.write_videofile(output_path, codec="libx264", fps=24)

    return output_path
