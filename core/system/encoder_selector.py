"""Automatic encoder selection."""

from dataclasses import dataclass

from core.system.environment import EnvironmentInfo


@dataclass(frozen=True)
class EncoderDecision:
    """Immutable selected encoder result."""

    selected_encoder: str
    reason: str
    priority: int

    @property
    def auto_label(self) -> str:
        """Return a future settings-friendly Auto label."""
        return f"Auto ({self.selected_encoder})"


class EncoderSelector:
    """Choose the best encoder from detected environment information."""

    PRIORITY = (
        ("NVENC", 1),
        ("AMF", 2),
        ("QSV", 3),
        ("Software (libx264)", 4),
    )

    def select(self, environment_info: EnvironmentInfo) -> EncoderDecision:
        """Return the best encoder decision for the given environment."""
        available_encoders = {
            self._normalize_encoder(encoder)
            for encoder in environment_info.available_encoders
        }

        for encoder, priority in self.PRIORITY:
            if self._normalize_encoder(encoder) in available_encoders:
                return EncoderDecision(
                    selected_encoder=encoder,
                    reason=self._reason_for_encoder(encoder, environment_info),
                    priority=priority,
                )

        return EncoderDecision(
            selected_encoder="Software (libx264)",
            reason="No hardware encoder was detected. Using software H.264.",
            priority=4,
        )

    def _normalize_encoder(self, encoder: str) -> str:
        return encoder.lower().replace(" ", "")

    def _reason_for_encoder(
        self,
        encoder: str,
        environment_info: EnvironmentInfo,
    ) -> str:
        if encoder == "NVENC":
            return f"NVIDIA GPU detected: {environment_info.gpu_name}."
        if encoder == "AMF":
            return f"AMD GPU detected: {environment_info.gpu_name}."
        if encoder == "QSV":
            return f"Intel GPU detected: {environment_info.gpu_name}."

        return "Software encoder is available on all supported systems."
