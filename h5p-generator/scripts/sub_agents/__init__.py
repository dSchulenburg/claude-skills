# H5P Sub-Agents
# Spezialisierte Agenten für verschiedene H5P-Content-Typen

from .base_agent import BaseH5PAgent, AgentResult
from .quiz_agent import QuizAgent
from .card_agent import CardAgent
from .drag_agent import DragAgent
from .design_agent import DesignAgent, DesignResult
from .combiner_agent import CombinerAgent, CombineResult, ContainerType
from .scenario_agent import ScenarioAgent
from .media_agent import MediaAgent

# Text-zu-Quiz Agents (NEU v2.3)
from .text_parser_agent import (
    TextParserAgent,
    ParsedQuestion,
    ParseResult,
    QuestionType,
    InputFormat
)
from .distractor_generator import DistractorGenerator, DistractorResult

__all__ = [
    'BaseH5PAgent',
    'AgentResult',
    'QuizAgent',
    'CardAgent',
    'DragAgent',
    'DesignAgent',
    'DesignResult',
    'CombinerAgent',
    'CombineResult',
    'ContainerType',
    'ScenarioAgent',
    'MediaAgent',
    # Text-zu-Quiz
    'TextParserAgent',
    'ParsedQuestion',
    'ParseResult',
    'QuestionType',
    'InputFormat',
    'DistractorGenerator',
    'DistractorResult',
]
