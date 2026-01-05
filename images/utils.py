import os
import numpy as np
from django.conf import settings
from PIL import Image
from .models import RequestLog, ImagesArtifact
from json import JSONDecodeError

def process_image(request_log_id):
    log = RequestLog.objects.get(pk=request_log_id)

    input_artifact = log.artifacts.get(artifact_type="INPUT")
    print(input_artifact)

    input_path = os.path.join(settings.MEDIA_ROOT, input_artifact.filename)
    print(input_path)

    output_format = input_artifact.filename.split('.')[-1].upper()
    if output_format == 'JPG': output_format = 'JPEG'

    operations = log.payload.get("operations", [])

    try:
        with Image.open(input_path) as img:
            for operation in operations:
                op_type = operation.get("type")

                if op_type == "resize":
                    width, height = operation.get("width"), operation.get("height")
                    if width and height:
                        img = img.resize((width, height))

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


            output_filename = f"processed_{input_artifact.filename}"
            output_path = os.path.join(settings.MEDIA_ROOT, output_filename)
            img.save(output_path, format=output_format)

        log.status = "SUCCESS"
        log.save()

        ImagesArtifact.objects.create(
            request_log=log,
            filename=output_filename,
            artifact_type="OUTPUT"
        )

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
            full_path = os.path.join(settings.MEDIA_ROOT, artifact.filename)
            img = Image.open(full_path).convert("RGB")
            images.append(img)

        if images:
            first_image = images[0]
            resized_images = []
            for img in images:
                processed_img = img.resize(first_image.size, Image.Resampling.LANCZOS)
                resized_images.append(processed_img)

            output_filename = f"converted_{log.id}.gif"
        output_path = os.path.join(settings.MEDIA_ROOT, output_filename)

        resized_images[0].save(
            output_path,
            save_all=True,
            append_images=resized_images[1:],
            duration=500,
            loop=0
        )

        log.status = "SUCCESS"
        log.save()

        ImagesArtifact.objects.create(
            request_log=log,
            filename=output_filename,
            artifact_type="OUTPUT"
        )

    except Exception as e:
        log.status = "FAILED"
        log.save()
        return f"Error converting into gif: {e}"