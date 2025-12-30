import os
import threading
import json
from ninja import NinjaAPI, UploadedFile, Form, File
from django.conf import settings
from .models import RequestLog, ImagesArtifact
from .schemas import UploadResponse, StatusResponse
from django.shortcuts import get_object_or_404
from .utils import process_image, generate_gif
from typing import List

api = NinjaAPI()

@api.get("/health")
def health_check(request):
    return {"status": "ok"}

@api.post("/upload", response=List[UploadResponse])
def upload_image(request, file: List[UploadedFile] = File(...), specs: str = Form(...)):
    try:
        pipeline = json.loads(specs)
    except json.JSONDecodeError:
        pipeline = []

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    is_gif = False
    if len(file) >= 2:
        for op_type in pipeline:
            if op_type.get("type") == "gif":
                is_gif = True
                break

    results = []

    if is_gif:
        gif_log = RequestLog.objects.create(
            status="PENDING",
            ip_address=ip,
            payload={
                "pipeline": pipeline, "mode": "gif_batch"
            }
        )

        for current_file in file:
            save_filename = f"{gif_log.id}_{current_file.name}"
            save_path = os.path.join(settings.MEDIA_ROOT, save_filename)

            with open(save_path, 'wb+') as destination:
                for chunk in current_file.chunks():
                    destination.write(chunk)    
            
            ImagesArtifact.objects.create(
                request_log=gif_log,
                filename=save_filename,
                artifact_type="INPUT"
            )

    else:
        for current_file in file:
            log = RequestLog.objects.create(
                status="PENDING",
                ip_address=ip,
                payload={
                    "original_filename": current_file.name,
                    "pipeline": pipeline
                }
            )

            save_filename = f"{log.id}_{current_file.name}"
            save_path = os.path.join(settings.MEDIA_ROOT, save_filename)

            with open(save_path, 'wb+') as destination:
                for chunk in current_file.chunks():
                    destination.write(chunk)    
            
            ImagesArtifact.objects.create(
                request_log=log,
                filename=save_filename,
                artifact_type="INPUT"
            )

            threading.Thread(target=process_image, args=(log.id,)).start()
            results.append({"request_id": log.id, "status": log.status})

    return results

@api.get("requests/{request_id}", response=StatusResponse)
def get_status(request, request_id: int):
    log = get_object_or_404(RequestLog, pk=request_id)
    input_img = log.artifacts.filter(artifact_type="INPUT").first()
    output_img = log.artifacts.filter(artifact_type="OUTPUT").first()

    return {
        "request_id": log.id,
        "status": log.status,
        "input_file": input_img.filename if input_img else "",
        "output_file": output_img.filename if output_img else None
        }