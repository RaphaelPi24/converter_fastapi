import subprocess
from pathlib import Path

# Маппинг форматов: источник ➔ целевой ➔ параметры ffmpeg
conversion_params = {
    'mp4': {
        'avi': ['-c:v', 'mpeg4'],
        'webm': ['-c:v', 'libvpx', '-b:v', '1M', '-c:a', 'libvorbis'],
        'mov': ['-c:v', 'libx264', '-c:a', 'aac'],
    },
    'avi': {
        'mp4': ['-c:v', 'libx264', '-c:a', 'aac'],
    },
    'webm': {
        'mp4': ['-c:v', 'libx264', '-c:a', 'aac'],
    },
    'mov': {
        'mp4': ['-c:v', 'libx264', '-c:a', 'aac'],
    }
}


def convert(input_path: Path, destination_format: str) -> Path:
    source_format = input_path.suffix.lstrip('.').lower()
    destination_format = destination_format.lower()

    if source_format not in conversion_params:
        raise ValueError(f"Конвертация из {source_format} не поддерживается.")
    if destination_format not in conversion_params[source_format]:
        raise ValueError(f"Конвертация из {source_format} в {destination_format} не поддерживается.")

    params = conversion_params[source_format][destination_format]
    if destination_format is None:
        output_path = input_path.with_suffix(f".{destination_format}")

    command = ["ffmpeg", "-i", str(input_path)] + params + [str(output_path)]

    subprocess.run(command, check=True)

    return output_path


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