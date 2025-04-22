import subprocess
from pathlib import Path


def convert(path, destination_format):
    params = {
        'mp4': {
            'avi': ['-c:v', 'libvpx', ...],
            'webm': {},
        }
    }
    source_format = path.suffix
    _params = params[source_format][destination_format]
    output_path = path.with_suffix(f"{destination_format}")
    subprocess.run(["ffmpeg", "-i", str(path), *_params], check=True)


def mp4_to_avi(input_path: Path, output_path: Path):
    output_path = output_path.with_suffix(".avi")
    subprocess.run(["ffmpeg", "-i", str(input_path), str(output_path)], check=True)


def avi_to_mp4(input_path: Path, output_path: Path):
    output_path = output_path.with_suffix(".mp4")
    subprocess.run(["ffmpeg", "-i", str(input_path), str(output_path)], check=True)


def mp4_to_webm(input_path: Path, output_path: Path):
    output_path = output_path.with_suffix(".webm")
    subprocess.run(["ffmpeg", "-i", str(input_path), "-c:v", "libvpx", "-b:v", "1M", "-c:a", "libvorbis", str(output_path)], check=True)


def webm_to_mp4(input_path: Path, output_path: Path):
    output_path = output_path.with_suffix(".mp4")
    subprocess.run(["ffmpeg", "-i", str(input_path), "-c:v", "libx264", "-c:a", "aac", str(output_path)], check=True)


def mov_to_mp4(input_path: Path, output_path: Path):
    output_path = output_path.with_suffix(".mp4")
    subprocess.run(["ffmpeg", "-i", str(input_path), "-c:v", "libx264", "-c:a", "aac", str(output_path)], check=True)


def mp4_to_mov(input_path: Path, output_path: Path):
    output_path = output_path.with_suffix(".mov")
    subprocess.run(["ffmpeg", "-i", str(input_path), "-c:v", "libx264", "-c:a", "aac", str(output_path)], check=True)


""""
1. ffmpeg
Команда, запускающая утилиту FFmpeg.

2. -i input_file
Указывает путь к входному видеофайлу. Это может быть .mp4, .mov, .avi и т.д.

3. -c:v libx264
-c:v означает видеокодек (video codec).

libx264 — это один из самых популярных видеокодеков (кодек H.264), обеспечивающий хорошее качество при малом размере файла. Подходит практически везде (веб, плееры и т.п.).

4. -c:a aac
-c:a означает аудиокодек (audio codec).

aac — популярный аудиокодек, который широко поддерживается (особенно в .mp4). Он обеспечивает хорошее качество звука и небольшую задержку.

5. output_file
Имя и путь к выходному файлу, который будет создан после конвертации.
"""