import subprocess
from pathlib import Path

from src.convert_code.archive import TarGzArchiver, ZipArchiver
from src.convert_code.image import svg_to_png, webp_to_jpg, webp_to_png, png_to_svg, png_to_webp, jpg_to_svg, \
    jpg_to_webp
from src.convert_code.text import docx_to_txt, pdf_to_txt, json_to_txt, csv_to_txt, txt_to_docx, txt_to_pdf, \
    txt_to_json, txt_to_csv


class BaseInterface:
    all_source_format = None
    all_target_format = None
    all_format_pairs = None

    def __init__(self, source_format: str, target_format: str, input_data: Path, output_path: Path):
        self.source_format = self.check_source_format(source_format)
        self.target_format = self.check_target_format(target_format)
        self.input_data = self.check_input_data(input_data)
        self.output_path = self.check_output_path(output_path)
        self.correct_func_convertion()

    def check_source_format(self, source_format: str):
        if source_format is None:
            raise ValueError("Source format not specified")
        if source_format not in self.all_source_format:
            raise ValueError(f"Конвертация из {self.source_format} не поддерживается.")
        return source_format.lower()

    def check_target_format(self, target_format: str):
        if target_format is None:
            raise ValueError("Target format not specified")
        if target_format not in self.all_target_format:
            raise ValueError(f"Конвертация  в {self.target_format} не поддерживается.")
        return target_format.lower()

    def correct_func_convertion(self):
        if (self.source_format, self.target_format) not in self.all_format_pairs:
            raise ValueError(f"Конвертация из {self.source_format} в {self.target_format} не поддерживается.")

    def check_input_data(self, input_data: Path):
        if input_data is None:
            raise ValueError("Input data not specified")
        if not isinstance(input_data, Path):
            raise ValueError("Input data must be a Path object")
        return input_data

    def check_output_path(self, output_path: Path):
        if output_path is None:
            raise ValueError("Output path not specified")
        if not isinstance(output_path, Path):
            raise ValueError("Output path must be a Path object")
        return output_path


class TextInterface(BaseInterface):
    conversion_format = {
        'txt': {
            'csv': txt_to_csv,
            'json': txt_to_json,
            'pdf': txt_to_pdf,
            'docx': txt_to_docx,
        },
        'csv': {
            'txt': csv_to_txt,
        },
        'json': {
            'txt': json_to_txt,
        },
        'pdf': {
            'txt': pdf_to_txt,
        },
        'docx': {
            'txt': docx_to_txt,
        }
    }
    all_source_format = conversion_format.keys()
    all_target_format = {target for targets in conversion_format.values() for target in targets.keys()}
    all_format_pairs = [(src, tgt) for src, tgts in conversion_format.items() for tgt in tgts.keys()]

    def run(self):
        converter_func = self.conversion_format[self.source_format][self.target_format]
        converter_func(self.input_data, self.output_path)


class VideoInterface(BaseInterface):
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

    all_source_format = conversion_params.keys()
    all_target_format = {target for targets in conversion_params.values() for target in targets.keys()}
    all_format_pairs = [(src, tgt) for src, tgts in conversion_params.items() for tgt in tgts.keys()]

    def run(self):
        params = self.conversion_params[self.source_format][self.target_format]
        command = ["ffmpeg", "-i", str(self.input_data)] + params + [str(self.output_path)]
        subprocess.run(command, check=True)


class DecompressingError(Exception):
    pass


class ArchiveInterface(BaseInterface):
    archiver_classes = {
        '.zip': ZipArchiver,
        '.tar.gz': TarGzArchiver
    }

    all_source_format = archiver_classes.keys()
    all_target_format = archiver_classes.keys()

    def __init__(self, source_format: str | None, target_format: str | None, input_data: Path, output_path: Path):
        # в одном должен быть нужный формат, в другом всегда None - означает папка
        if source_format is None:
            source_format = self._resolve_suffix(input_data)
            self.mode = 'archive'
        if target_format is None:
            target_format = self._resolve_suffix(output_path)
            self.mode = 'extract'
        super().__init__(source_format, target_format, input_data, output_path)

    def check_source_format(self, source_format: str):
        if source_format is not None:
            return source_format.lower()

    def check_target_format(self, target_format: str):
        if target_format is not None:
            return target_format.lower()

    def correct_func_convertion(self):
        if self.source_format is not None and self.source_format not in self.all_source_format:
            raise ValueError(f"Неподдерживаемый формат: {self.source_format}")
        if self.target_format is not None and self.target_format not in self.all_target_format:
            raise ValueError(f"Неподдерживаемый формат: {self.target_format}")
        if self.source_format is None and self.target_format is None:
            raise ValueError(f"Формат не задан: {self.source_format}, {self.target_format}")

    def run(self):
        suffix = self.source_format if self.mode == 'extract' else self.target_format

        if suffix not in self.archiver_classes:
            raise ValueError(f"Неподдерживаемый формат архива: {suffix}")

        archiver_class = self.archiver_classes[suffix]
        archiver = archiver_class(self.input_data, self.output_path)

        try:
            if self.mode == 'extract':
                archiver.extract()
            else:
                archiver.archive()
            return True
        except Exception as e:
            raise DecompressingError(f"Ошибка при архивации/распаковке: {e}")

    def _resolve_suffix(self, path: Path) -> str | None:
        name = path.name
        if name.endswith(".tar.gz"):
            return ".tar.gz"
        suffix = path.suffix
        if suffix in self.all_source_format:
            return suffix
        return None  # <--- если не подходит, пусть возвращает None


class ImageInterface(BaseInterface):
    conversion_format = {
        'jpg': {
            'webp': jpg_to_webp,
            'svg': jpg_to_svg,
        },
        'png': {
            'webp': png_to_webp,
            'svg': png_to_svg,
        },
        'webp': {
            'png': webp_to_png,
            'jpg': webp_to_jpg,
        },
        'svg': {
            'png': svg_to_png,
        },
    }

    all_source_format = list(conversion_format.keys())
    all_target_format = {tgt for tgts in conversion_format.values() for tgt in tgts.keys()}
    all_format_pairs = [(src, tgt) for src, tgts in conversion_format.items() for tgt in tgts.keys()]

    def run(self) -> bool:
        func = self.conversion_format[self.source_format][self.target_format]
        func(self.input_data, self.output_path)
        return True


class UniversalInterface:
    def __init__(self, source_format, target_format, input_data, output_path):
        self.source_format = source_format
        self.target_format = target_format
        self.input_data = input_data
        self.output_path = output_path

    def run(self) -> bool:
        return self.resolve_interface().run()

    def resolve_interface(self):
        for interface_cls in [TextInterface, VideoInterface, ImageInterface, ArchiveInterface]:
            if self.source_format in interface_cls.all_source_format or self.target_format in interface_cls.all_target_format:
                return interface_cls(self.source_format, self.target_format, self.input_data, self.output_path)
        raise ValueError(f"Формат '{self.source_format}' не поддерживается ни одним интерфейсом.")
