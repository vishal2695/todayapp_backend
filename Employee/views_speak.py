import json
import os
from io import BytesIO

import boto3
from botocore.config import Config
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def speak(request):
    print("request speak...", request.method)
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    text = body.get("text")
    model = body.get("model")
    language = body.get("lang")
    engine = body.get("engine") or "standard"

    if not text or not model:
        return JsonResponse({"error": "Missing 'text' or 'model'"}, status=400)

    aws_region = os.getenv("AWS_REGION", "us-east-1")
    print("aws keysssssssssssssssssss.", aws_region)
    polly_client = boto3.client(
        "polly",
        region_name=aws_region,
        config=Config(region_name=aws_region),
    )

    try:
        response = polly_client.synthesize_speech(
            OutputFormat="mp3",
            Text=text,
            VoiceId=model,
            LanguageCode=language,
            Engine=engine,
        )
    except Exception as exc:
        return JsonResponse({"error": f"Polly synth failed: {exc}"}, status=500)

    audio_stream = response.get("AudioStream")
    if not audio_stream:
        return JsonResponse({"error": "No audio stream returned"}, status=500)

    data = audio_stream.read()
    audio_stream.close()

    http_response = HttpResponse(data, content_type="audio/mpeg")
    http_response["Content-Disposition"] = 'inline; filename="output.mp3"'
    return http_response
