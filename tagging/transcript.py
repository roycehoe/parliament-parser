from enum import StrEnum, auto
import re
from typing import Iterable


def is_oral_answer_title(text: str) -> bool:
    pattern = r"\*\*[A-Z\s]+\*\*"
    return bool(re.search(pattern, text))


def is_oral_answer_subtitle(text: str) -> bool:
    pattern = r"(?m)^\*\*(?=.*[a-z])[^*]+\*\*$"
    return bool(re.search(pattern, text))


def is_speech(text: str) -> bool:
    contains_bolded_text_pattern = r"\*\*.*?\*\*"
    return bool(re.search(contains_bolded_text_pattern, text))


def is_blank_line(text: str) -> bool:
    return text.strip() == ""


class TranscriptLineType(StrEnum):
    TITLE = auto()
    SUBTITLE = auto()
    BLANK = auto()
    SPEECH = auto()
    CONTD_TEXT = auto()


def get_transcript_line_type(text: str) -> TranscriptLineType:
    if is_blank_line(text):
        return TranscriptLineType.BLANK
    if is_oral_answer_title(text):
        return TranscriptLineType.TITLE
    if is_oral_answer_subtitle(text):
        return TranscriptLineType.SUBTITLE
    if is_speech(text):
        return TranscriptLineType.SPEECH
    return TranscriptLineType.CONTD_TEXT


def get_transcript_tagged_data(
    handsard_transcript_data: list[str],
) -> Iterable[tuple[str, TranscriptLineType]]:
    transcript_tags: list[TranscriptLineType] = [
        get_transcript_line_type(line) for line in handsard_transcript_data
    ]
    return zip(handsard_transcript_data, transcript_tags)
