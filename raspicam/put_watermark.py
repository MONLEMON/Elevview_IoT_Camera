from PIL import Image

def set_watermark(image_name,watermar_name):
    background = Image.open(f"/home/monlemon/project/photo/{image_name}.jpg").convert("RGBA")

    watermark = Image.open(f"/home/monlemon/project/watermark/{watermar_name}.png").convert("RGBA")

    position = (background.width - watermark.width, background.height - watermark.height)

    combined = background.copy()
    combined.paste(watermark, position, mask=watermark)

    combined = combined.convert("RGB")
    
    combined.save(f"/home/monlemon/project/photo/{image_name}.jpg", "JPEG", quality=100, optimize=True)