# AudioTranscribePro

## Overview
AudioTranscribePro is a powerful Python-based tool that combines audio transcription with speaker diarization. It processes various audio file formats (MP3, M4A, MP4), converts them to WAV, transcribes the content, and identifies different speakers in the audio. This tool is ideal for transcribing interviews, podcasts, or any multi-speaker audio content.

## Features
- Supports multiple audio formats (MP3, M4A, MP4)
- Converts input audio to WAV format
- Transcribes audio content using Whisper models
- Performs speaker diarization
- Supports various Whisper model sizes (e.g., tiny, base, large, large-v3)
- Implements progress tracking and resumable transcription
- Caches diarization results for faster re-runs
- Provides detailed progress and timing information

## Installation
Follow these steps to install AudioTranscribePro:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/AudioTranscribePro
   ```
2. Navigate to the project directory:
   ```
   cd AudioTranscribePro
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `config.yaml` file in the project directory with your Hugging Face authentication token:
   ```yaml
   huggingface:
     use_auth_token: "YOUR_HUGGING_FACE_TOKEN"
   ```

## Usage
To use AudioTranscribePro, run the following command:

```
python audiotranscribepro.py input_file output_file [--model_size MODEL_SIZE]
```

- Replace `input_file` with the path to your audio file
- Replace `output_file` with the desired output text file path
- Optionally, specify `MODEL_SIZE` to choose a Whisper model (default is "large-v3")

Example:
```
python audiotranscribepro.py my_podcast.mp3 transcript.txt --model_size large
```

## Notes
- The script requires an internet connection to download the necessary models
- Processing large audio files may take significant time and computational resources
- Ensure you have sufficient disk space for temporary WAV file conversion
- The script supports resuming interrupted transcriptions
- Diarization results are cached for faster subsequent runs

## Troubleshooting
- If you encounter issues with diarization, ensure your authentication token in `config.yaml` is correct and you have the necessary permissions
- For manual model downloads, ensure the files are in the correct location
- Check your internet connection if you experience download issues

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

# AudioTranscribePro

## 概要
AudioTranscribeProは、音声トランスクリプションと話者ダイアリゼーションを組み合わせた強力なPythonベースのツールです。様々な音声ファイル形式（MP3、M4A、MP4）を処理し、WAVに変換し、内容を文字起こしし、音声内の異なる話者を識別します。このツールは、インタビュー、ポッドキャスト、または複数の話者による音声コンテンツの文字起こしに最適です。

## 機能
- 複数の音声フォーマットをサポート（MP3、M4A、MP4）
- 入力音声をWAV形式に変換
- Whisperモデルを使用して音声コンテンツを文字起こし
- 話者ダイアリゼーションを実行
- 様々なWhisperモデルサイズをサポート（例：tiny、base、large、large-v3）
- 進捗状況の追跡と中断可能な文字起こし機能を実装
- ダイアリゼーション結果をキャッシュして後続の実行を高速化
- 詳細な進捗状況とタイミング情報を提供

## インストール方法
AudioTranscribeProをインストールするには、以下の手順に従ってください：

1. リポジトリをクローンします：
   ```
   git clone https://github.com/yourusername/AudioTranscribePro
   ```
2. プロジェクトディレクトリに移動します：
   ```
   cd AudioTranscribePro
   ```
3. 必要な依存関係をインストールします：
   ```
   pip install -r requirements.txt
   ```
4. プロジェクトディレクトリに`config.yaml`ファイルを作成し、Hugging Face認証トークンを記載します：
   ```yaml
   huggingface:
     use_auth_token: "あなたのHugging Faceトークン"
   ```

## 使い方
AudioTranscribeProを使用するには、以下のコマンドを実行します：

```
python audiotranscribepro.py 入力ファイル 出力ファイル [--model_size モデルサイズ]
```

- `入力ファイル`を音声ファイルのパスに置き換えてください
- `出力ファイル`を希望する出力テキストファイルのパスに置き換えてください
- オプションで`モデルサイズ`を指定してWhisperモデルを選択できます（デフォルトは"large-v3"）

例：
```
python audiotranscribepro.py my_podcast.mp3 transcript.txt --model_size large
```

## 注意点
- スクリプトは必要なモデルをダウンロードするためにインターネット接続が必要です
- 大きな音声ファイルの処理には、かなりの時間と計算リソースが必要になる場合があります
- 一時的なWAVファイル変換用に十分なディスク容量があることを確認してください
- スクリプトは中断された文字起こしの再開をサポートしています
- ダイアリゼーション結果がキャッシュされ、後続の実行が高速化されます

## トラブルシューティング
- ダイアリゼーションに問題が発生した場合は、`config.yaml`の認証トークンが正しいこと、必要な権限があることを確認してください
- モデルを手動でダウンロードした場合は、ファイルが正しい場所にあることを確認してください
- ダウンロードに問題がある場合は、インターネット接続を確認してください

## ライセンス
このプロジェクトはMITライセンスの下でライセンスされています。詳細はLICENSEファイルを参照してください。
