import shutil
import tarfile
import zipfile
from pathlib import Path


class ArchiveFunction:

    @staticmethod
    def folder_to_zip(input_path: Path, output_path: Path):
        shutil.make_archive(str(output_path.with_suffix('')), 'zip', root_dir=input_path)

    @staticmethod
    def folder_to_tar_gz(input_path: Path, output_path: Path):
        with tarfile.open(output_path, "w:gz") as tar:
            tar.add(input_path, arcname=".")

    @staticmethod
    def zip_to_folder(input_path: Path, output_path: Path):
        with zipfile.ZipFile(input_path, 'r') as zip_ref:
            zip_ref.extractall(output_path)

    @staticmethod
    def tar_gz_to_folder(input_path: Path, output_path: Path):
        with tarfile.open(input_path, 'r:gz') as tar:
            tar.extractall(path=output_path)
