# H5P Sub-Agents
# Spezialisierte Agenten für verschiedene H5P-Content-Typen

from .base_agent import BaseH5PAgent, AgentResult
from .quiz_agent import QuizAgent
from .card_agent import CardAgent
from .drag_agent import DragAgent

__all__ = [
    'BaseH5PAgent',
    'AgentResult',
    'QuizAgent',
    'CardAgent',
    'DragAgent'
]
