from pathlib import Path

import cairosvg
import svgwrite
from PIL import Image


class ImageFunction:
    @staticmethod
    def jpg_to_webp(input_path: Path, output_path: Path):
        with Image.open(input_path) as img:
            img.save(output_path, "WEBP")

    @staticmethod
    def png_to_webp(input_path: Path, output_path: Path):
        with Image.open(input_path) as img:
            img.save(output_path, "WEBP")

    @staticmethod
    def webp_to_png(input_path: Path, output_path: Path):
        with Image.open(input_path) as img:
            img = img.convert("RGB")  # Убираем альфа-канал для совместимости
            img.save(output_path, "PNG")

    @staticmethod
    def webp_to_jpg(input_path: Path, output_path: Path):
        with Image.open(input_path) as img:
            img = img.convert("RGB")
            img.save(output_path, "JPEG")

    @staticmethod
    def svg_to_png(input_path: Path, output_path: Path):
        cairosvg.svg2png(url=str(input_path), write_to=str(output_path))

    @staticmethod
    def raster_to_svg(input_path: Path, output_path: Path, threshold: int = 128):
        img = Image.open(input_path).convert("L")  # Grayscale
        width, height = img.size
        pixels = img.load()

        dwg = svgwrite.Drawing(str(output_path), profile='tiny', size=(width, height))

        for y in range(height):
            for x in range(width):
                if pixels[x, y] < threshold:  # Чёрная точка
                    dwg.add(dwg.rect(insert=(x, y), size=(1, 1), fill='black'))

        dwg.save()

    @staticmethod
    def jpg_to_svg(input_path: Path, output_path: Path):
        ImageFunction.raster_to_svg(input_path, output_path)

    @staticmethod
    def png_to_svg(input_path: Path, output_path: Path):
        ImageFunction.raster_to_svg(input_path, output_path)
