import whisper
from pydub import AudioSegment
import torch
import os
import sys
import argparse
import subprocess
import tempfile
import json
import time
from faster_whisper import WhisperModel
from datetime import datetime

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

def transcribe_audio_chunk(audio_chunk: AudioSegment, model) -> dict:
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        audio_chunk.export(temp_file.name, format="wav")
        segments, _ = model.transcribe(temp_file.name, beam_size=5)
    os.unlink(temp_file.name)
    return segments

def transcribe_audio(audio_file: str, progress_file: str, device, model_size: str) -> list:
    model = WhisperModel(model_size, device=device.type, compute_type="float16" if device.type == "cuda" else "int8")
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
        segments = transcribe_audio_chunk(chunk, model)
        transcriptions.append({"segments": [{"start": seg.start, "end": seg.end, "text": seg.text} for seg in segments]})
        
        # Save progress
        with open(progress_file, 'w') as f:
            json.dump({'transcriptions': transcriptions, 'last_chunk': i}, f)
        
        # Add a sleep to reduce CPU usage
        # time.sleep(0.5)  # Adjust this value to control CPU usage
    
    return transcriptions

def print_timestamp(step_name: str, start_time: datetime):
    current_time = datetime.now()
    elapsed_time = current_time - start_time
    print(f"\n{step_name}開始時刻: {current_time}")
    print(f"{step_name}までの経過時間: {elapsed_time}")

def main(input_file: str, output_file: str, model_size: str):
    start_time = datetime.now()
    print(f"開始時刻: {start_time}")

    if not os.path.exists(input_file):
        print(f"Error: The specified file '{input_file}' does not exist.")
        sys.exit(1)

    progress_file = f"{output_file}.progress"

    print_timestamp("WAV変換", start_time)
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
    print(f"Using device: {device.type}")

    print_timestamp("文字起こし", start_time)
    print("Transcribing audio...")
    transcriptions = transcribe_audio(wav_file, progress_file, device, model_size)

    print_timestamp("結果の出力", start_time)
    print(f"Writing output to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transcriptions, f, ensure_ascii=False, indent=4)

    print("Transcription complete. Cleaning up...")
    os.remove(wav_file)
    os.remove(progress_file)

    end_time = datetime.now()
    total_elapsed_time = end_time - start_time
    print(f"\n終了時刻: {end_time}")
    print(f"総経過時間: {total_elapsed_time}")
    print("All steps completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio.")
    parser.add_argument("input_file", help="Path to the input audio file (MP3, M4A, or MP4)")
    parser.add_argument("output_file", help="Path to the output text file")
    parser.add_argument("--model_size", default="large-v3", help="Size of the Whisper model to use (e.g. tiny, base, large, large-v3)")
    args = parser.parse_args()

    main(args.input_file, args.output_file, args.model_size)
