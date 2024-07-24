import sys
import json

# プログラムの概要説明:
# このプログラムは、指定されたファイルからJSONデータを抽出し、
# "text"フィールドの値をUnicodeエスケープからデコードして変換します。
# 変換後のJSONデータを標準出力に出力します。

# 処理の仕様:
# 1. 指定されたファイルを読み込む。
# 2. ファイル内容からJSONデータを抽出する。
# 3. JSONデータをパースする。
# 4. "transcriptions"フィールド内の各"segments"の"text"フィールドをデコードする。
# 5. 変換後のJSONデータを標準出力に出力する。

# コマンド例:
# 1. python convert_text.py input.txt
# 2. python convert_text.py /path/to/file.json

def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # JSONデータを抽出
    json_start = content.find('{"transcriptions":')
    json_end = content.rfind('}') + 1
    json_data = content[json_start:json_end]
    
    # JSONをパース
    data = json.loads(json_data)
    
    # "text"フィールドの値を変換
    for transcription in data['transcriptions']:
        for segment in transcription['segments']:
            # textフィールドの値がUnicodeエスケープされている場合は、デコードする
            text = segment['text']
            try:
                decoded_text = text.encode('latin-1').decode('unicode-escape')
                segment['text'] = decoded_text
            except UnicodeEncodeError:
                # すでにUTF-8でデコードされている場合は、そのまま使用
                pass
    
    # 変換後のJSONを出力
    print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_text.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    process_file(filename)
