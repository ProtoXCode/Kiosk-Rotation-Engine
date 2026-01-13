from kiosk.config import TimingConfig


def estimate_duration(words: int, timing: TimingConfig) -> int:
    seconds = int(words / timing.words_per_minute * 60)

    return max(timing.min_duration, min(seconds, timing.max_duration))
