"""
Constants for Notion MCP Server

All valid statuses, priorities, and configuration values for each database type.
"""

from enum import Enum
from typing import Dict, List, Optional


class DatabaseType(str, Enum):
    """Supported database types"""

    WORK = "work"
    STUDIES = "studies"
    PERSONAL = "personal"
    YOUTUBER = "youtuber"


class WorkStatus(str, Enum):
    """Valid statuses for Work database"""

    NAO_INICIADO = "Não iniciado"
    EM_ANDAMENTO = "Em Andamento"
    EM_REVISAO = "Em Revisão"
    CONCLUIDO = "Concluído"
    PAUSADO = "Pausado"
    CANCELADO = "Cancelado"


class StudiesStatus(str, Enum):
    """Valid statuses for Studies database"""

    NAO_ADQUIRIDO = "Não Adquirido"
    PARA_FAZER = "Para Fazer"
    EM_REVISAO = "Em Revisão"
    EM_PAUSA = "Em Pausa"
    EM_ANDAMENTO = "Em Andamento"
    DESCONTINUADO = "Descontinuado"
    CONCLUIDO = "Concluido"


class PersonalStatus(str, Enum):
    """Valid statuses for Personal database"""

    NAO_INICIADO = "Não iniciado"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDO = "Concluído"
    CANCELADO = "Cancelado"


class YoutuberStatus(str, Enum):
    """Valid statuses for Youtuber database"""

    PARA_GRAVAR = "Para Gravar"
    NAO_INICIADO = "Não iniciado"
    EDITADO = "Editado"
    EDITANDO = "Editando"
    PARA_EDICAO = "Para Edição"
    GRAVANDO = "Gravando"
    PUBLICADO = "Publicado"
    CONCLUIDO = "Concluído"


class Priority(str, Enum):
    """Valid priorities"""

    BAIXA = "Baixa"
    NORMAL = "Normal"
    ALTA = "Alta"
    URGENTE = "Urgente"


# Status mapping per database type
STATUS_BY_DATABASE: Dict[DatabaseType, List[str]] = {
    DatabaseType.WORK: [s.value for s in WorkStatus],
    DatabaseType.STUDIES: [s.value for s in StudiesStatus],
    DatabaseType.PERSONAL: [s.value for s in PersonalStatus],
    DatabaseType.YOUTUBER: [s.value for s in YoutuberStatus],
}

# Default statuses per database type
DEFAULT_STATUS: Dict[DatabaseType, str] = {
    DatabaseType.WORK: WorkStatus.NAO_INICIADO.value,
    DatabaseType.STUDIES: StudiesStatus.PARA_FAZER.value,
    DatabaseType.PERSONAL: PersonalStatus.NAO_INICIADO.value,
    DatabaseType.YOUTUBER: YoutuberStatus.NAO_INICIADO.value,
}

# Field names per database type
TITLE_FIELD: Dict[DatabaseType, str] = {
    DatabaseType.WORK: "Nome do projeto",
    DatabaseType.STUDIES: "Project name",
    DatabaseType.PERSONAL: "Nome da tarefa",
    DatabaseType.YOUTUBER: "Nome do projeto",
}

DATE_FIELD: Dict[DatabaseType, str] = {
    DatabaseType.WORK: "Periodo",
    DatabaseType.STUDIES: "Período",
    DatabaseType.PERSONAL: "Data",
    DatabaseType.YOUTUBER: "Periodo",
}

DESCRIPTION_FIELD: Dict[DatabaseType, Optional[str]] = {
    DatabaseType.WORK: None,
    DatabaseType.STUDIES: "Descrição",
    DatabaseType.PERSONAL: "Descrição",
    DatabaseType.YOUTUBER: "Resumo do Episodio",
}

RELATION_FIELD: Dict[DatabaseType, str] = {
    DatabaseType.WORK: "item principal",
    DatabaseType.STUDIES: "Parent item",
    DatabaseType.PERSONAL: "tarefa principal",
    DatabaseType.YOUTUBER: "item principal",
}

# Recommended icons per database type
RECOMMENDED_ICONS: Dict[DatabaseType, List[str]] = {
    DatabaseType.WORK: ["🚀", "💼", "🏢", "📋", "✅", "🔧"],
    DatabaseType.STUDIES: ["🎓", "📚", "🎯", "📖", "📑", "💡"],
    DatabaseType.PERSONAL: ["👤", "📝", "🎯", "✅", "📌", "⚡"],
    DatabaseType.YOUTUBER: ["🎬", "🎮", "📺", "🎥", "▶️"],
}

# Study hours configuration
STUDY_HOURS = {
    "default": {"start": 19, "end": 21},  # 19:00-21:00
    "tuesday": {"start": 19.5, "end": 21},  # 19:30-21:00 (post-treatment schedule)
    "max_end": 21,  # NUNCA passar das 21:00
}

# YouTube recording hours
YOUTUBE_HOURS = {
    "start": 21,  # 21:00
    "end": 23.83,  # 23:50
}

# Work clients
WORK_CLIENTS = ["Astracode", "Pessoal", "FIAP"]
WORK_PROJECTS = ["ExpenseIQ", "HubTravel", "Avulso"]

# Notion API Configuration
NOTION_API_VERSION = "2022-06-28"
NOTION_BASE_URL = "https://api.notion.com/v1"
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RATE_LIMIT_PER_SECOND = 3
