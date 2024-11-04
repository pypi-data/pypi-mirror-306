from typing import List

from ai.core.ai_file_type import AiFileType, HgFile
from util import unitutils


class AiSource:

    def __init__(
            self,
            model_name: str,
            url: str | None = None,
            hg_files: List[HgFile] | None = None,
    ):
        self.url = url
        self.hg_files = hg_files
        self.model_name = model_name

    def get_ggml_file(self) -> HgFile:
        for hg_file in self.hg_files:
            if hg_file.file_type == AiFileType.HG_GGML:
                return hg_file
        raise Exception("No ggml file found in the source.")

    def get_mmproj_file(self) -> HgFile:
        for hg_file in self.hg_files:
            if hg_file.file_type == AiFileType.HG_MMPROJ:
                return hg_file
        raise Exception("No mmproj file found in the source.")

    def get_files_size_mb(self) -> float:
        total = 0.0
        for hg_file in self.hg_files:
            size_byte = hg_file.get_file_size_byte()
            size_mb = unitutils.convert_byte_to_mb(size_byte)
            total += size_mb
        return total
