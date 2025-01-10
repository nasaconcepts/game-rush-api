# strategy/__init__.py
from .multiple_choice import MultipleChoice
from .single_choice import SingleChoice
from .speech_input import SpeechChoice

__all__ = ["SingleChoice", "SpeechChoice", "MultipleChoice"]