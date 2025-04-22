import tarfile
import zipfile
from pathlib import Path

from scipy.stats import describe


class BaseArchiver:
    def archive(self, source: Path, destination: Path):
        raise NotImplementedError

    def extract(self, source: Path, destination: Path):
        raise NotImplementedError


class ZipArchiver(BaseArchiver):
    def archive(self, source: Path, destination: Path):
        pass

    def extract(self, source: Path, destination: Path):
        pass


class TarGzArchiver(BaseArchiver):
    def archive(self, source: Path, destination: Path):
        pass

    def extract(self, source: Path, destination: Path):
        pass


def extract(source, destination):
    archiver_classes = {
        '.zip': ZipArchiver,
        '.tar.gz': TarGzArchiver
    }
    archiver_class = archiver_classes[source.suffix]
    archiver = archiver_class(source, destination)
    try:
        archiver.extract()
    except DecompressingError as e:
        ...



def folder_to_zip(folder_path: Path, zip_path: Path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in folder_path.rglob('*'):
            zipf.write(file, file.relative_to(folder_path))


def folder_to_tar_gz(folder_path: Path, tar_gz_path: Path):
    with tarfile.open(tar_gz_path, "w:gz") as tar:
        tar.add(folder_path, arcname=".")


def zip_to_folder(zip_path: Path, extract_to: Path):
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(extract_to)


def tar_gz_to_folder(tar_gz_path: Path, extract_to: Path):
    with tarfile.open(tar_gz_path, "r:gz") as tar:
        tar.extractall(path=extract_to)
