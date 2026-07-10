"""GPU detection foundation."""

import platform
import subprocess
import tempfile
from pathlib import Path


class GPUDetector:
    """Detect GPU vendor, name, and likely hardware encoders."""

    SOFTWARE_ENCODER = "Software (libx264)"

    def detect(self) -> tuple[str, str, list[str]]:
        """Return GPU vendor, GPU name, and available encoder names."""
        gpu_names = self._detect_gpu_names()
        vendor, gpu_name = self._select_primary_gpu(gpu_names)
        encoders = self._encoders_for_vendor(vendor)
        return vendor, gpu_name, encoders

    def _detect_gpu_names(self) -> list[str]:
        if platform.system() == "Windows":
            return self._detect_windows_gpu_names()

        return []

    def _detect_windows_gpu_names(self) -> list[str]:
        gpu_names: list[str] = []
        gpu_names.extend(self._detect_nvidia_smi_gpu_names())
        if self._has_vendor(gpu_names, "NVIDIA"):
            return self._unique_gpu_names(gpu_names)

        gpu_names.extend(
            self._detect_command_gpu_names(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    (
                        "Get-CimInstance Win32_VideoController "
                        "| Select-Object -ExpandProperty Name"
                    ),
                ],
                ignored_lines=(),
            )
        )
        gpu_names.extend(
            self._detect_command_gpu_names(
                ["wmic", "path", "win32_VideoController", "get", "name"],
                ignored_lines=("name",),
            )
        )
        gpu_names.extend(self._detect_dxdiag_gpu_names())
        return self._unique_gpu_names(gpu_names)

    def _detect_nvidia_smi_gpu_names(self) -> list[str]:
        return self._detect_command_gpu_names(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            ignored_lines=(),
        )

    def _detect_command_gpu_names(
        self,
        command: list[str],
        *,
        ignored_lines: tuple[str, ...],
    ) -> list[str]:
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=8,
            )
        except OSError:
            return []
        except subprocess.TimeoutExpired:
            return []

        if result.returncode != 0:
            return []

        ignored = {line.lower() for line in ignored_lines}
        return [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip() and line.strip().lower() not in ignored
        ]

    def _detect_dxdiag_gpu_names(self) -> list[str]:
        output_path = Path(tempfile.gettempdir()) / "eck-dxdiag.txt"
        try:
            result = subprocess.run(
                ["dxdiag", "/whql:off", "/t", str(output_path)],
                capture_output=True,
                text=True,
                timeout=15,
            )
        except OSError:
            return []
        except subprocess.TimeoutExpired:
            return []

        if result.returncode != 0 or not output_path.exists():
            return []

        try:
            lines = output_path.read_text(encoding="utf-16", errors="ignore").splitlines()
        except OSError:
            return []

        names: list[str] = []
        for line in lines:
            text = line.strip()
            if text.startswith("Card name:"):
                names.append(text.removeprefix("Card name:").strip())

        return names

    def _unique_gpu_names(self, gpu_names: list[str]) -> list[str]:
        unique_names: list[str] = []
        seen: set[str] = set()
        for gpu_name in gpu_names:
            normalized = gpu_name.strip()
            key = normalized.lower()
            if not normalized or key in seen or "microsoft basic" in key:
                continue

            seen.add(key)
            unique_names.append(normalized)

        return unique_names

    def _has_vendor(self, gpu_names: list[str], vendor: str) -> bool:
        return any(self._detect_vendor(gpu_name) == vendor for gpu_name in gpu_names)

    def _select_primary_gpu(self, gpu_names: list[str]) -> tuple[str, str]:
        vendor_priority = ("NVIDIA", "AMD", "Intel")
        for vendor in vendor_priority:
            for gpu_name in gpu_names:
                if self._detect_vendor(gpu_name) == vendor:
                    return vendor, gpu_name

        if gpu_names:
            return "Unknown", gpu_names[0]

        return "Unknown", "Unknown"

    def _detect_vendor(self, gpu_name: str) -> str:
        name = gpu_name.lower()
        if "nvidia" in name or "geforce" in name or "rtx" in name or "gtx" in name:
            return "NVIDIA"
        if "amd" in name or "radeon" in name:
            return "AMD"
        if "intel" in name or "arc" in name or "iris" in name or "uhd" in name:
            return "Intel"

        return "Unknown"

    def _encoders_for_vendor(self, vendor: str) -> list[str]:
        encoders = {
            "NVIDIA": ["NVENC"],
            "AMD": ["AMF"],
            "Intel": ["QSV"],
        }.get(vendor, [])

        return [*encoders, self.SOFTWARE_ENCODER]
