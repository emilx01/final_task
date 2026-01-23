import os
import io
import numpy as np
from django.conf import settings
from PIL import Image
from .models import RequestLog, ImagesArtifact
from json import JSONDecodeError
from django.core.files.base import ContentFile

def process_image(request_log_id):
    log = RequestLog.objects.get(pk=request_log_id)
    input_artifact = log.artifacts.get(artifact_type="INPUT")
    input_path = os.path.join(settings.MEDIA_ROOT, "Uploaded images", input_artifact.filename)
    output_format = input_artifact.filename.split('.')[-1].upper()
    if output_format == 'JPG': output_format = 'JPEG'

    operations = log.payload.get("operations", [])

    try:
        with Image.open(input_artifact.uploaded_image) as img:
            for operation in operations:
                op_type = operation.get("type")

                if op_type == "resize":
                    width, height = operation.get("width"), operation.get("height")
                    current_width, current_height = img.size

                    if width and not height:
                        ratio = width/float(current_width)
                        height = int(current_height*ratio)

                    if height and not width:
                        ratio = height/float(current_height)
                        width = int(current_width*ratio)

                    if width and height:
                        img = img.resize((width, height))

                if op_type == "crop":
                    width, height = img.size
                    left, upper, right, lower = operation.get("left"), operation.get("upper"), operation.get("right"), operation.get("lower")
                    img = img.crop((left, upper, right, lower))

                if op_type == "padding":
                    width, height = img.size
                    left = operation.get("left", 0)
                    upper = operation.get("upper", 0)
                    right = operation.get("right", 0)
                    lower = operation.get("lower", 0)
                    new_width = width + right + left
                    new_height = height + lower + upper
                    result = Image.new(img.mode, (new_width, new_height), (0, 0, 255))
                    result.paste(img, (left, upper))
                    img = result

                if op_type == "rotate":
                    theta = operation.get("angle", 0)
                    img = img.rotate(angle=theta)

                if op_type == "rgb_bgr_conversion":
                    if img.mode != "RGB":
                        img = img.convert('RGB')
                    rgb = np.array(img)
                    bgr = rgb[:, :, ::-1]
                    img = Image.fromarray(bgr)

                if op_type == "png_jpeg_conversion":
                    if output_format == "PNG":
                        img = img.convert('RGB')
                        output_format = "JPEG"
                    elif output_format == "JPEG" or output_format == "JPG":
                        output_format = "PNG"

                if op_type == "grayscale":
                    img = img.convert("L")

            base_name, _ = os.path.splitext(input_artifact.filename)
            if output_format == "JPEG":
                new_extension = ".jpg"
            else:
                new_extension = ".png"
            
            output_filename = f"{base_name}{new_extension}"
            output_path = os.path.join(settings.MEDIA_ROOT, "Processed images", output_filename)
            
            buffer = io.BytesIO()
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img.save(buffer, format=output_format)
            image_bytes = buffer.getvalue()

            file_to_save = ContentFile(image_bytes, name=output_filename)
            ImagesArtifact.objects.create(
                request_log=log,
                filename=output_filename,
                artifact_type="OUTPUT",
                processed_image=file_to_save
            )
            buffer.close()
            
        log.status = "SUCCESS"
        log.save()



    except Exception as e:
        log.status = "FAILED"
        log.save()
        return f"Error opening image: {e}"
    
def generate_gif(request_log_id):
    log = RequestLog.objects.get(pk=request_log_id)
    input_artifacts = log.artifacts.filter(artifact_type="INPUT")

    images = []
    
    try:
        for artifact in input_artifacts:
            full_path = os.path.join(settings.MEDIA_ROOT, "Uploaded images", artifact.filename)
            img = Image.open(full_path).convert("RGB")
            images.append(img)

        if images:
            first_image = images[0]
            resized_images = []
            for img in images:
                processed_img = img.resize(first_image.size, Image.Resampling.LANCZOS)
                resized_images.append(processed_img)

            output_filename = f"converted_{log.timestamp.strftime("%Y-%m-%d")}.gif"

            buffer = io.BytesIO()

            resized_images[0].save(
                buffer,
                format="GIF",
                save_all=True,
                append_images=resized_images[1:],
                duration=300,
                loop=0
            )

            image_bytes = buffer.getvalue()
            file_to_save = ContentFile(image_bytes, name=output_filename)
            ImagesArtifact.objects.create(
                request_log=log,
                filename=output_filename,
                artifact_type="OUTPUT",
                processed_image=file_to_save
            )
            buffer.close()

        log.status = "SUCCESS"
        log.save()

    except Exception as e:
        log.status = "FAILED"
        log.save()
        return f"Error converting into gif: {e}"