import subprocess
from pathlib import Path

from convert_code.funcs.archive import TarGzArchiver, ZipArchiver
from convert_code.funcs.image import svg_to_png, webp_to_jpg, webp_to_png, png_to_svg, png_to_webp, jpg_to_svg, \
    jpg_to_webp
from convert_code.funcs.text import docx_to_txt, pdf_to_txt, json_to_txt, csv_to_txt, txt_to_docx, txt_to_pdf, \
    txt_to_json, txt_to_csv
from convert_code.validators import ConversionParams


class BaseInterface:
    all_source_format = None
    all_target_format = None
    all_format_pairs = None

    def __init__(self, source_format: str, target_format: str, input_data: Path, output_path: Path):
        validated = ConversionParams(
            source_format=source_format,
            target_format=target_format,
            input_data=input_data,
            output_path=output_path,
            allowed_source=self.all_source_format,
            allowed_target=self.all_target_format,
            allowed_pairs=self.all_format_pairs,
        )
        self.source_format = validated.source_format
        self.target_format = validated.target_format
        self.input_data = validated.input_data
        self.output_path = validated.output_path


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
        return True


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
        '.tar.gz': TarGzArchiver,
    }

    all_source_format = list(archiver_classes.keys()) + ["folder"]
    all_target_format = list(archiver_classes.keys()) + ["folder"]
    all_format_pairs = [
        ("folder", ".zip"),
        ("folder", ".tar.gz"),
        (".zip", "folder"),
        (".tar.gz", "folder"),
    ]

    def __init__(self, source_format: str, target_format: str, input_data: Path, output_path: Path):
        super().__init__(source_format, target_format, input_data, output_path)
        self.is_archiving = self.source_format == "folder"
        self.suffix = self.target_format if self.is_archiving else self.source_format
        self._check_suffix_supported()

    def _check_suffix_supported(self):
        if self.suffix not in self.archiver_classes:
            raise ValueError(f"Неподдерживаемый формат архива: {self.suffix}")

    def run(self):
        archiver_class = self.archiver_classes[self.suffix]
        archiver = archiver_class(self.input_data, self.output_path)

        try:
            if self.is_archiving:
                archiver.archive()
            else:
                archiver.extract()
            return True
        except Exception as e:
            raise DecompressingError(f"Ошибка при архивации/распаковке: {e}")

    def _resolve_suffix(self, path: Path) -> str:
        if path.is_dir():
            return "folder"
        name = path.name
        if name.endswith(".tar.gz"):
            return ".tar.gz"
        suffix = path.suffix
        if suffix in self.all_source_format:
            return suffix
        raise ValueError(f"Не удалось определить формат по пути: {path}")


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
    INTERFACES = [TextInterface, VideoInterface, ImageInterface, ArchiveInterface]

    def __init__(self, source_format: str, target_format: str, input_data: Path, output_path: Path):
        self.source_format = source_format
        self.target_format = target_format
        self.input_data = input_data
        self.output_path = output_path
        self.interface = self.resolve_interface()

    def resolve_interface(self):
        for iface_cls in self.INTERFACES:
            if (
                    self.source_format in iface_cls.all_source_format
                    or self.target_format in iface_cls.all_target_format
            ):
                return iface_cls(self.source_format, self.target_format, self.input_data, self.output_path)
        raise ValueError(
            f"Формат '{self.source_format}' → '{self.target_format}' не поддерживается ни одним интерфейсом.")

    def run(self) -> bool:
        return self.interface.run()

    @classmethod
    def get_all_supported_pairs(cls):
        pairs = []
        for iface in cls.INTERFACES:
            pairs.extend(iface.all_format_pairs)
        return pairs
