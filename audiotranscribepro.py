import whisper
from pydub import AudioSegment
import torch
from pyannote.audio import Pipeline
import os
import sys
import argparse
import subprocess
import tempfile
import json
import time
from huggingface_hub import login
from huggingface_hub.utils import HfHubHTTPError
import numpy as np

CHUNK_LENGTH_MS = 5 * 60 * 1000  # 5 minutes

def convert_to_wav(input_file: str) -> str:
    file_name, file_extension = os.path.splitext(input_file)
    wav_file = file_name + '.wav'
    
    if not os.path.exists(wav_file):
        if file_extension.lower() in ['.mp3', '.m4a', '.mp4']:
            if file_extension.lower() == '.mp3':
                audio = AudioSegment.from_mp3(input_file)
                audio.export(wav_file, format="wav")
            elif file_extension.lower() in ['.m4a', '.mp4']:
                subprocess.run(['ffmpeg', '-i', input_file, '-acodec', 'pcm_s16le', '-ar', '16000', wav_file], check=True)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    return wav_file

def transcribe_audio_chunk(audio_chunk: AudioSegment, model, device) -> dict:
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        audio_chunk.export(temp_file.name, format="wav")
        result = model.transcribe(temp_file.name, fp16=device.type == "cuda")
    os.unlink(temp_file.name)
    return result

def transcribe_audio(audio_file: str, progress_file: str, device, model_name: str) -> list:
    model = whisper.load_model(model_name, device=device)  # Use the specified model
    audio = AudioSegment.from_wav(audio_file)
    chunks = [audio[i:i+CHUNK_LENGTH_MS] for i in range(0, len(audio), CHUNK_LENGTH_MS)]
    
    transcriptions = []
    start_chunk = 0
    
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress = json.load(f)
            transcriptions = progress['transcriptions']
            start_chunk = progress['last_chunk'] + 1
    
    for i, chunk in enumerate(chunks[start_chunk:], start=start_chunk):
        print(f"Transcribing chunk {i+1}/{len(chunks)}...")  # 進捗状況を出力
        result = transcribe_audio_chunk(chunk, model, device)
        transcriptions.append(result)
        
        # Save progress
        with open(progress_file, 'w') as f:
            json.dump({'transcriptions': transcriptions, 'last_chunk': i}, f)
        
        # Add a sleep to reduce CPU usage
        time.sleep(0.5)  # Adjust this value to control CPU usage
    
    return transcriptions

def perform_diarization(audio_file: str, auth_token: str) -> dict:
    try:
        # NumPyのNANをnp.nanに置き換え
        np.NAN = np.nan
        
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                            use_auth_token=auth_token)
        diarization = pipeline(audio_file)
        return diarization
    except HfHubHTTPError as e:
        print(f"Error during diarization: {str(e)}")
        print("It might be because the model is private or gated so make sure to authenticate.")
        print("Visit https://hf.co/settings/tokens to create your access token and retry.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during diarization: {str(e)}")
        print("If you've manually downloaded the model files, make sure they're in the correct location.")
        print("If the problem persists, please check your internet connection and try again.")
        sys.exit(1)

def merge_transcription_and_diarization(transcriptions: list, diarization: dict) -> str:
    merged_output = []
    total_offset = 0
    
    for transcription in transcriptions:
        for segment in transcription["segments"]:
            segment_start = segment["start"] + total_offset
            segment_end = segment["end"] + total_offset
            
            speaker = None
            for turn, _, spk in diarization.itertracks(yield_label=True):
                if turn.start <= segment_start < turn.end:
                    speaker = spk
                    break
            
            text = segment["text"]
            merged_output.append(f"{speaker}: {text}")
        
        total_offset += transcription["segments"][-1]["end"]
    
    return "\n".join(merged_output)

def main(input_file: str, output_file: str, auth_token: str, model_name: str):
    # Login to Hugging Face
    print(f"Using auth token: {auth_token}")  # トークンの確認
    login(token=auth_token)

    if not os.path.exists(input_file):
        print(f"Error: The specified file '{input_file}' does not exist.")
        sys.exit(1)

    progress_file = f"{output_file}.progress"
    diarization_file = f"{output_file}.diarization"

    print(f"Converting {input_file} to WAV...")
    try:
        wav_file = convert_to_wav(input_file)
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {str(e)}")
        sys.exit(1)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    print("Transcribing audio...")
    transcriptions = transcribe_audio(wav_file, progress_file, device, model_name)

    if not os.path.exists(diarization_file):
        print("Performing speaker diarization...")
        try:
            diarization = perform_diarization(wav_file, auth_token)
            with open(diarization_file, 'wb') as f:
                torch.save(diarization, f)
        except Exception as e:
            print(f"Error during diarization: {str(e)}")
            print("You can retry later by running the script again.")
            sys.exit(1)
    else:
        print("Loading existing diarization results...")
        with open(diarization_file, 'rb') as f:
            diarization = torch.load(f)

    print("Merging transcription and diarization results...")
    final_output = merge_transcription_and_diarization(transcriptions, diarization)

    print(f"Writing output to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_output)

    print("Transcription complete. Cleaning up...")
    os.remove(wav_file)
    os.remove(progress_file)
    os.remove(diarization_file)

    print("All steps completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio with speaker diarization.")
    parser.add_argument("input_file", help="Path to the input audio file (MP3, M4A, or MP4)")
    parser.add_argument("output_file", help="Path to the output text file")
    parser.add_argument("--auth_token", required=True, help="Hugging Face authentication token")
    parser.add_argument("--model_name", default="tiny", help="Name of the Whisper model to use (e.g. tiny, base, large)")
    args = parser.parse_args()

    main(args.input_file, args.output_file, args.auth_token, args.model_name)
