# AudioTranscribePro

## Overview
AudioTranscribePro is a powerful Python-based tool that combines audio transcription with speaker diarization. It processes various audio file formats (MP3, M4A, MP4), converts them to WAV, transcribes the content, and identifies different speakers in the audio. This tool is ideal for transcribing interviews, podcasts, or any multi-speaker audio content.

## New Features and Improvements
- Added support for specifying the Whisper model to use (e.g., tiny, base, large)
- Implemented progress tracking and resumable transcription
- Improved error handling and user feedback
- Optimized CPU usage during transcription
- Added diarization result caching for faster re-runs

## Installation
Follow these steps to install AudioTranscribePro:

1. Clone the repository:
   ```
   git clone https://github.com/daishir0/AudioTranscribePro
   ```
2. Navigate to the project directory:
   ```
   cd AudioTranscribePro
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Obtain a Hugging Face authentication token:
   - Visit https://huggingface.co/settings/tokens
   - Create a new token with read access

## Usage
To use AudioTranscribePro, run the following command:

```
python audiotranscribepro.py input_file output_file --auth_token YOUR_HUGGING_FACE_TOKEN [--model_name MODEL_NAME]
```

- Replace `input_file` with the path to your audio file
- Replace `output_file` with the desired output text file path
- Replace `YOUR_HUGGING_FACE_TOKEN` with your Hugging Face authentication token
- Optionally, specify `MODEL_NAME` to choose a Whisper model (default is "tiny")

## Notes
- Supported input formats: MP3, M4A, MP4
- The script requires an internet connection to download the necessary models
- Processing large audio files may take significant time and computational resources
- Ensure you have sufficient disk space for temporary WAV file conversion
- The script now supports resuming interrupted transcriptions
- Diarization results are cached for faster subsequent runs

## Troubleshooting
- If you encounter issues with diarization, ensure your authentication token is correct and you have the necessary permissions
- For manual model downloads, ensure the files are in the correct location
- Check your internet connection if you experience download issues

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

# AudioTranscribePro

## 概要
AudioTranscribeProは、音声トランスクリプションと話者ダイアリゼーションを組み合わせた強力なPythonベースのツールです。様々な音声ファイル形式（MP3、M4A、MP4）を処理し、WAVに変換し、内容を文字起こしし、音声内の異なる話者を識別します。このツールは、インタビュー、ポッドキャスト、または複数の話者による音声コンテンツの文字起こしに最適です。

## 新機能と改善点
- 使用するWhisperモデルを指定する機能を追加（例：tiny、base、large）
- 進捗状況の追跡と中断可能な文字起こし機能を実装
- エラー処理とユーザーフィードバックを改善
- 文字起こし中のCPU使用率を最適化
- 再実行を高速化するためのダイアリゼーション結果のキャッシュ機能を追加

## インストール方法
AudioTranscribeProをインストールするには、以下の手順に従ってください：

1. リポジトリをクローンします：
   ```
   git clone https://github.com/daishir0/AudioTranscribePro
   ```
2. プロジェクトディレクトリに移動します：
   ```
   cd AudioTranscribePro
   ```
3. 必要な依存関係をインストールします：
   ```
   pip install -r requirements.txt
   ```
4. Hugging Face認証トークンを取得します：
   - https://huggingface.co/settings/tokens にアクセス
   - 読み取りアクセス権を持つ新しいトークンを作成

## 使い方
AudioTranscribeProを使用するには、以下のコマンドを実行します：

```
python audiotranscribepro.py 入力ファイル 出力ファイル --auth_token あなたのHugging Faceトークン [--model_name モデル名]
```

- `入力ファイル`を音声ファイルのパスに置き換えてください
- `出力ファイル`を希望する出力テキストファイルのパスに置き換えてください
- `あなたのHugging Faceトークン`をHugging Face認証トークンに置き換えてください
- オプションで`モデル名`を指定してWhisperモデルを選択できます（デフォルトは"tiny"）

## 注意点
- サポートされている入力形式：MP3、M4A、MP4
- スクリプトは必要なモデルをダウンロードするためにインターネット接続が必要です
- 大きな音声ファイルの処理には、かなりの時間と計算リソースが必要になる場合があります
- 一時的なWAVファイル変換用に十分なディスク容量があることを確認してください
- スクリプトは中断された文字起こしの再開をサポートするようになりました
- ダイアリゼーション結果がキャッシュされ、後続の実行が高速化されます

## トラブルシューティング
- ダイアリゼーションに問題が発生した場合は、認証トークンが正しいこと、必要な権限があることを確認してください
- モデルを手動でダウンロードした場合は、ファイルが正しい場所にあることを確認してください
- ダウンロードに問題がある場合は、インターネット接続を確認してください

## ライセンス
このプロジェクトはMITライセンスの下でライセンスされています。詳細はLICENSEファイルを参照してください。
