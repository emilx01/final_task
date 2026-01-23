import io
import json
import base64
import binascii
from ninja import NinjaAPI, UploadedFile, Form, File
from ninja.errors import HttpError
from django.conf import settings
from .models import RequestLog, ImagesArtifact
from .schemas import UploadResponse, StatusResponse
from django.shortcuts import get_object_or_404
from .utils import process_image, generate_gif
from typing import List
from django.core.files.base import ContentFile

api = NinjaAPI()

@api.get("/health")
def health_check(request):
    return {"status": "ok"}

@api.post("/upload", response={201: List[UploadResponse], 400: dict, 422: dict})
def upload_image(request, 
                 file: List[UploadedFile] = File(None), 
                 file_json: str = Form(""), 
                 specs: str = Form(...)):
    
    try:
        operations = json.loads(specs)
    except json.JSONDecodeError:
        raise HttpError(400, "Invalid JSON format in specs")

    if file_json:
        file_json = file_json.strip()
        if not file_json:
            file_json = None

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    is_gif = False
    for op_type in operations:
        if op_type.get("type") == "gif":
            is_gif = True
            break
            
    results = []

    if is_gif:
        gif_log = RequestLog.objects.create(
            status="PENDING",
            ip_address=ip,
            payload={"operations": operations}
        )

        if file:
            for current_file in file:
                ImagesArtifact.objects.create(
                    request_log=gif_log,
                    filename=current_file.name,
                    artifact_type="INPUT",
                    uploaded_image=current_file
                )

        if file_json:
            try:
                if "," in file_json:
                    png_str = file_json.split(",")[1]
                else:
                    png_str = file_json

                png_bytes = base64.b64decode(png_str)
                manual_filename = f"{gif_log.id}_{gif_log.timestamp.strftime('%Y-%m-%d')}_base64_upload.png" 

                ImagesArtifact.objects.create(
                    request_log=gif_log,
                    filename=manual_filename,
                    artifact_type="INPUT",
                    uploaded_image=ContentFile(png_bytes, name=manual_filename)
                )

            except binascii.Error:
                gif_log.status = "FAILED"
                gif_log.save()
                results.append({
                    "request_id": gif_log.id, 
                    "status": "FAILED", 
                    "error": "Invalid Base64 string format"
                })

            except Exception as e:
                gif_log.status = "FAILED"
                gif_log.save()
                results.append({"request_id": gif_log.id, "status": gif_log.status, "error": str(e)})

        if file or file_json:
            error_message = generate_gif(gif_log.id)
            gif_log.refresh_from_db()
            results.append({
                "request_id": gif_log.id,
                "status": gif_log.status,
                "error": str(error_message) if error_message else "No errors"
            })

    else:
        if file:
            for current_file in file:
                log = RequestLog.objects.create(
                    status="PENDING",
                    ip_address=ip,
                    payload={"original_filename": current_file.name, "operations": operations}
                )

                save_filename = f"{log.id}_{log.timestamp.strftime('%Y-%m-%d')}_{current_file.name}"

                ImagesArtifact.objects.create(
                    request_log=log,
                    filename=save_filename,
                    artifact_type="INPUT",
                    uploaded_image=current_file
                )

                error_message = process_image(log.id)
                log.refresh_from_db()

                final_error = "No errors"
                if log.status == "FAILED":
                    raise HttpError(422, f"Processing failed: {error_message}")

                results.append({
                    "request_id": log.id,
                    "status": log.status,
                    "error": final_error
                })


        if file_json:
            log = RequestLog.objects.create(
                status="PENDING",
                ip_address=ip,
                payload={"original_filename": "base64_upload.png", "operations": operations}
            )

            try:
                if "," in file_json:
                    png_str = file_json.split(",")[1]
                else:
                    png_str = file_json
                png_bytes = base64.b64decode(png_str)

                manual_filename = f"{log.id}_{log.timestamp.strftime('%Y-%m-%d')}_base64_upload.png"

                ImagesArtifact.objects.create(
                    request_log=log,
                    filename=manual_filename,
                    artifact_type="INPUT",
                    uploaded_image=ContentFile(png_bytes, name=manual_filename)
                )

                error_message = process_image(log.id)
                log.refresh_from_db()

                final_error = "No errors"
                if log.status == "FAILED":
                    raise HttpError(422, f"Processing failed: {error_message}")

                results.append({
                    "request_id": log.id,
                    "status": log.status,
                    "error": final_error
                })

            except binascii.Error:
                log.status = "FAILED"
                log.save()
                results.append({
                    "request_id": log.id, 
                    "status": log.status, 
                    "error": "Invalid Base64 string format"
                })

            except Exception as e:
                log.status = "FAILED"
                log.save()
                results.append({"request_id": log.id, "status": log.status, "error": str(e)})

    return 201, results

@api.get("requests/{request_id}", response=StatusResponse)
def get_status(request, request_id: int):
    log = get_object_or_404(RequestLog, pk=request_id)
    input_img = log.artifacts.filter(artifact_type="INPUT").first()
    output_img = log.artifacts.filter(artifact_type="OUTPUT").first()
    return {
        "request_id": log.id,
        "status": log.status,
        "input_file": input_img.uploaded_image.url if input_img else "",
        "output_file": output_img.processed_image.url if output_img else None
        }