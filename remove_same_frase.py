import json
import sys

# プログラムの概要説明:
# このプログラムは、JSONファイル内の連続する同一のフレーズを削除するためのものです。
# 入力ファイルとして指定されたJSONファイルを読み込み、各トランスクリプションのセグメントから
# 連続する同一のフレーズを削除し、結果を標準出力にJSON形式で出力します。

# 処理の仕様:
# 1. 入力ファイルを読み込む。
# 2. 各トランスクリプションのセグメントを処理し、連続する同一のフレーズを削除する。
# 3. 処理結果をJSON形式で標準出力に出力する。

# コマンド例:
# 1. python remove_same_frase.py input.json
# 2. python remove_same_frase.py /path/to/your/input.json

def remove_consecutive_phrases(segments):
    new_segments = []
    for segment in segments:
        if new_segments and segment['text'] == new_segments[-1]['text']:
            continue
        new_segments.append(segment)
    return new_segments

def process_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for transcription in data['transcriptions']:
        transcription['segments'] = remove_consecutive_phrases(transcription['segments'])

    return data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python remove_same_frase.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    processed_data = process_json(input_file)

    print(json.dumps(processed_data, ensure_ascii=False, indent=2))