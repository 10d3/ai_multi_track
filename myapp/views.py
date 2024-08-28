from django.shortcuts import render
import speech_recognition as sr
from pydub import AudioSegment
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tempfile import NamedTemporaryFile

# Create your views here.

def index(request):
    return render(request, "index.html")

@csrf_exempt
def transcribe_audio(request):
    if request.method == 'POST':
        if 'audio' not in request.FILES:
            return JsonResponse({"error": "No audio file provided"}, status=400)

        audio_file = request.FILES['audio']

        # Convert MP3 to WAV
        audio_segment = AudioSegment.from_file(audio_file, format="mp3")
        with NamedTemporaryFile(suffix=".wav", delete=True) as temp_wav_file:
            audio_segment.export(temp_wav_file.name, format="wav")

            # Now process the WAV file with speech recognition
            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_wav_file.name) as source:
                audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                return JsonResponse({"transcribed_text": text})
            except sr.UnknownValueError:
                return JsonResponse({"error": "Could not understand the audio"}, status=400)
            except sr.RequestError as e:
                return JsonResponse({"error": f"Service error: {e}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)