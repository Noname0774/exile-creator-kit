"""Smart video bitrate calculation."""


class SmartBitrate:
    """Calculate recommended video bitrate from duration."""

    MAX_SIZE_BYTES = 512 * 1024 * 1024
    RESERVED_AUDIO_BITRATE = 192_000
    OVERHEAD_RATIO = 0.05
    MIN_VIDEO_BITRATE = 500_000
    MAX_VIDEO_BITRATE = 50_000_000

    def calculate(self, duration_seconds: float) -> int:
        """Return recommended video bitrate in bps."""
        if duration_seconds <= 0:
            return self.MIN_VIDEO_BITRATE

        total_bitrate = (self.MAX_SIZE_BYTES * 8) / duration_seconds
        usable_bitrate = total_bitrate * (1 - self.OVERHEAD_RATIO)
        video_bitrate = int(usable_bitrate - self.RESERVED_AUDIO_BITRATE)

        return max(
            self.MIN_VIDEO_BITRATE,
            min(video_bitrate, self.MAX_VIDEO_BITRATE),
        )

