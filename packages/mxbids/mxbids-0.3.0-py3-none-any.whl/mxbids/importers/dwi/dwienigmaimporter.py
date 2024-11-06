"""anatomybidsexporter.py

"""
# Package Header #
from mxbids.header import __author__, __credits__, __email__, __maintainer__

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


from json import dump, load
from pathlib import Path
from typing import Any, Optional

from mxbids.importspec import FileSpec
from mxbids.modalities import DWI
from mxbids.modalities.importers.base import DWIImporter



TO_STRIP = [
    "InstitutionName",
    "InstitutionalDepartmentName",
    "InstitutionAddress",
    "DeviceSerialNumber",
]
DEFAULT_FILES = [
    FileSpec("dwi", ".nii.gz", [Path("dti.nii.gz")]),
    FileSpec("dwi", ".json", [Path("dti.json")], copy_command=strip_json),
    FileSpec("dwi", ".bval", [Path("dti.bval")]),
    FileSpec("dwi", ".bvec", [Path("dti.bvec")]),
]


class DWIEnigmaImporter(DWIImporter):
    def construct(
        self,
        modality: Optional[DWI] = None,
        src_root: Optional[Path] = None,
        files: list[FileSpec] = [],
        **kwargs: Any,
    ) -> None:
        if modality is not None:
            self.modality = modality

        if src_root is not None:
            self.src_root = src_root

        files.extend(DEFAULT_FILES)
        self.files = files
        super().construct(**kwargs)

    def import_all_files(self, path: Path, source_name: str) -> None:
        assert self.modality is not None
        assert self.src_root is not None

        for file in self.files:
            imaging_root = Path("/Users/rchristin/Kleen-Lab/dti/")
            new_path = path / f"{self.modality.full_name}_{file.suffix}{file.extension}"
            for filepath in file.path_from_root:
                imaging_path = imaging_root / source_name / filepath
                print(imaging_path)
                old_name = imaging_path.name
                exclude = any(n in old_name for n in self.import_exclude_names)

                if new_path.exists():
                    continue

                if exclude:
                    continue

                if imaging_path.is_file():
                    self._import_file(file, imaging_path, new_path)
                    break

                if not callable(file.copy_command):
                    continue

                file.copy_command(imaging_path, new_path)

            if not callable(file.copy_command) and not new_path.exists():
                print(new_path)
                raise RuntimeError(
                    "No source file but no function provided to gather data"
                )


DWI.default_importers["Enigma"] = DWIEnigmaImporter
