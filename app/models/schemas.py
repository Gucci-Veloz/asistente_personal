from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

# Esquemas base
class ItemBase(BaseModel):
    """Esquema base para todos los items."""
    text: str = Field(..., description="Contenido principal del item")
    
class ItemCreate(ItemBase):
    """Esquema para crear un nuevo item."""
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Metadatos adicionales del item")

class ItemUpdate(BaseModel):
    """Esquema para actualizar un item existente."""
    text: Optional[str] = Field(None, description="Contenido principal del item")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadatos adicionales del item")

class Item(ItemBase):
    """Esquema para representar un item completo."""
    id: str = Field(..., description="Identificador único del item")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadatos adicionales del item")
    
    class Config:
        from_attributes = True

class ItemList(BaseModel):
    """Esquema para representar una lista de items."""
    items: List[Item] = Field(..., description="Lista de items")
    total: int = Field(..., description="Número total de items")

class QueryResult(BaseModel):
    """Esquema para representar el resultado de una consulta semántica."""
    items: List[Item] = Field(..., description="Items encontrados")
    distances: List[float] = Field(..., description="Distancias de similitud (menor es más similar)")

# Esquemas específicos para cada módulo

# Módulo de Identidad y Psicología
class IdentityItemCreate(ItemCreate):
    """Esquema para crear un item en el módulo de Identidad y Psicología."""
    metadata: Dict[str, Any] = Field(
        default_factory=lambda: {
            "category": "general",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        description="Metadatos del item de identidad"
    )

class IdentityItemUpdate(ItemUpdate):
    """Esquema para actualizar un item en el módulo de Identidad y Psicología."""
    pass

# Módulo de Negocios y Estrategia
class BusinessItemCreate(ItemCreate):
    """Esquema para crear un item en el módulo de Negocios y Estrategia."""
    metadata: Dict[str, Any] = Field(
        default_factory=lambda: {
            "category": "idea",
            "priority": "medium",
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        description="Metadatos del item de negocios"
    )

class BusinessItemUpdate(ItemUpdate):
    """Esquema para actualizar un item en el módulo de Negocios y Estrategia."""
    pass

# Módulo de Recordatorios y URLs
class ReminderItemCreate(ItemCreate):
    """Esquema para crear un item en el módulo de Recordatorios y URLs."""
    metadata: Dict[str, Any] = Field(
        default_factory=lambda: {
            "type": "reminder",
            "url": "",
            "due_date": None,
            "priority": "medium",
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        description="Metadatos del recordatorio"
    )

class ReminderItemUpdate(ItemUpdate):
    """Esquema para actualizar un item en el módulo de Recordatorios y URLs."""
    pass

# Módulo de Conexiones Inteligentes
class ConnectionItemCreate(ItemCreate):
    """Esquema para crear un item en el módulo de Conexiones Inteligentes."""
    metadata: Dict[str, Any] = Field(
        default_factory=lambda: {
            "source_id": "",
            "source_module": "",
            "target_id": "",
            "target_module": "",
            "connection_type": "semantic",
            "strength": 0.0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        description="Metadatos de la conexión"
    )

class ConnectionItemUpdate(ItemUpdate):
    """Esquema para actualizar un item en el módulo de Conexiones Inteligentes."""
    pass

class ConnectionAnalysisRequest(BaseModel):
    """Esquema para solicitar un análisis de conexiones."""
    item_id: str = Field(..., description="ID del item a analizar")
    module: str = Field(..., description="Módulo al que pertenece el item")
    min_similarity: float = Field(0.7, ge=0.0, le=1.0, description="Similitud mínima para considerar una conexión")
    max_connections: int = Field(5, ge=1, le=20, description="Número máximo de conexiones a retornar")

class ConnectionAnalysisResult(BaseModel):
    """Esquema para representar el resultado de un análisis de conexiones."""
    source_id: str = Field(..., description="ID del item de origen")
    source_module: str = Field(..., description="Módulo del item de origen")
    connections: List[Item] = Field(..., description="Conexiones encontradas")
    total: int = Field(..., description="Número total de conexiones encontradas")

# Módulo de Aprendizajes y Reflexiones
class LearningItemCreate(ItemCreate):
    """Esquema para crear un item en el módulo de Aprendizajes y Reflexiones."""
    metadata: Dict[str, Any] = Field(
        default_factory=lambda: {
            "category": "general",
            "source": "",
            "context": "",
            "importance": "medium",
            "tags": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        description="Metadatos del aprendizaje"
    )

class LearningItemUpdate(ItemUpdate):
    """Esquema para actualizar un item en el módulo de Aprendizajes y Reflexiones."""
    pass

class LearningSummaryRequest(BaseModel):
    """Esquema para solicitar un resumen de aprendizajes."""
    category: Optional[str] = Field(None, description="Categoría de aprendizajes a resumir")
    tags: Optional[List[str]] = Field(None, description="Tags para filtrar aprendizajes")
    importance: Optional[str] = Field(None, description="Nivel de importancia para filtrar")
    max_items: int = Field(10, ge=1, le=50, description="Número máximo de items a incluir en el resumen")

class LearningSummary(BaseModel):
    """Esquema para representar un resumen de aprendizajes."""
    items: List[Item] = Field(..., description="Items incluidos en el resumen")
    total: int = Field(..., description="Número total de items")
    categories: Dict[str, int] = Field(..., description="Conteo de items por categoría")
    summary_text: str = Field(..., description="Texto de resumen generado")

# Módulo de Priorización y Filtrado
class PriorityItemCreate(ItemCreate):
    """Esquema para crear un item en el módulo de Priorización y Filtrado."""
    metadata: Dict[str, Any] = Field(
        default_factory=lambda: {
            "item_id": "",
            "module": "",
            "priority_level": "medium",  # high, medium, low
            "relevance_score": 0.0,
            "usage_count": 0,
            "last_accessed": datetime.now().isoformat(),
            "is_duplicate": False,
            "duplicate_of": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        description="Metadatos de priorización"
    )

class PriorityItemUpdate(ItemUpdate):
    """Esquema para actualizar un item en el módulo de Priorización y Filtrado."""
    pass

class PriorityReviewRequest(BaseModel):
    """Esquema para solicitar una revisión de prioridades."""
    module: Optional[str] = Field(None, description="Módulo específico a revisar (si no se especifica, se revisan todos)")
    min_similarity: float = Field(0.85, ge=0.0, le=1.0, description="Similitud mínima para considerar duplicados")
    max_items: int = Field(100, ge=1, description="Número máximo de items a revisar")
    include_low_relevance: bool = Field(True, description="Incluir items con baja relevancia en la revisión")
    include_duplicates: bool = Field(True, description="Incluir posibles duplicados en la revisión")

class PriorityAdjustRequest(BaseModel):
    """Esquema para ajustar la prioridad de un item."""
    item_id: str = Field(..., description="ID del item a ajustar")
    module: str = Field(..., description="Módulo al que pertenece el item")
    priority_level: str = Field(..., description="Nuevo nivel de prioridad (high, medium, low)")
    relevance_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Nueva puntuación de relevancia")

class PriorityOptimizeRequest(BaseModel):
    """Esquema para solicitar una optimización de prioridades."""
    module: Optional[str] = Field(None, description="Módulo específico a optimizar (si no se especifica, se optimizan todos)")
    auto_merge_duplicates: bool = Field(False, description="Fusionar automáticamente duplicados")
    auto_archive_low_relevance: bool = Field(False, description="Archivar automáticamente items con baja relevancia")

class PriorityReviewResult(BaseModel):
    """Esquema para representar el resultado de una revisión de prioridades."""
    total_items_reviewed: int = Field(..., description="Número total de items revisados")
    potential_duplicates: List[Dict[str, Any]] = Field(..., description="Posibles duplicados encontrados")
    low_relevance_items: List[Dict[str, Any]] = Field(..., description="Items con baja relevancia")
    suggested_actions: List[Dict[str, Any]] = Field(..., description="Acciones sugeridas")

class PriorityOptimizeResult(BaseModel):
    """Esquema para representar el resultado de una optimización de prioridades."""
    total_items_optimized: int = Field(..., description="Número total de items optimizados")
    merged_duplicates: List[Dict[str, Any]] = Field(..., description="Duplicados fusionados")
    archived_items: List[Dict[str, Any]] = Field(..., description="Items archivados")
    reprioritized_items: List[Dict[str, Any]] = Field(..., description="Items con prioridad ajustada")

# Módulo de Sugerencias Inteligentes
class SuggestionItemCreate(ItemCreate):
    """Esquema para crear un item en el módulo de Sugerencias Inteligentes."""
    metadata: Dict[str, Any] = Field(
        default_factory=lambda: {
            "type": "action",  # action, insight, connection
            "context": "",
            "relevance_score": 0.0,
            "source_modules": [],
            "source_items": [],
            "is_implemented": False,
            "implementation_date": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        description="Metadatos de la sugerencia"
    )

class SuggestionItemUpdate(ItemUpdate):
    """Esquema para actualizar un item en el módulo de Sugerencias Inteligentes."""
    pass

class SuggestionRequest(BaseModel):
    """Esquema para solicitar sugerencias."""
    modules: Optional[List[str]] = Field(None, description="Módulos específicos a analizar (si no se especifica, se analizan todos)")
    max_suggestions: int = Field(5, ge=1, le=20, description="Número máximo de sugerencias a generar")
    suggestion_types: Optional[List[str]] = Field(None, description="Tipos de sugerencias a generar (action, insight, connection)")
    min_relevance: float = Field(0.6, ge=0.0, le=1.0, description="Relevancia mínima para incluir una sugerencia")

class SuggestionAnalysisRequest(BaseModel):
    """Esquema para solicitar un análisis de datos para generar sugerencias."""
    modules: Optional[List[str]] = Field(None, description="Módulos específicos a analizar (si no se especifica, se analizan todos)")
    time_range: Optional[Dict[str, str]] = Field(None, description="Rango de tiempo para el análisis (start_date, end_date)")
    focus_areas: Optional[List[str]] = Field(None, description="Áreas específicas en las que enfocar el análisis")

class SuggestionResult(BaseModel):
    """Esquema para representar el resultado de una solicitud de sugerencias."""
    suggestions: List[Item] = Field(..., description="Sugerencias generadas")
    total: int = Field(..., description="Número total de sugerencias")
    by_type: Dict[str, int] = Field(..., description="Conteo de sugerencias por tipo")
    analysis_summary: str = Field(..., description="Resumen del análisis realizado")

# Esquemas para respuestas de error
class ErrorResponse(BaseModel):
    """Esquema para representar una respuesta de error."""
    detail: str = Field(..., description="Descripción del error")

# Esquemas para respuestas de éxito
class SuccessResponse(BaseModel):
    """Esquema para representar una respuesta exitosa."""
    message: str = Field(..., description="Mensaje de éxito")

# Función para generar IDs únicos
def generate_id() -> str:
    """Genera un ID único para los items."""
    return str(uuid.uuid4()) 