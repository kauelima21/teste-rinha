from pydantic import BaseModel, Field
from enum import Enum


class TipoEnum(str, Enum):
    c = 'c'
    d = 'd'


class TransacaoSchema(BaseModel):
    valor: int = Field(gt=0)
    tipo: TipoEnum
    descricao: str = Field(max_length=10, min_length=1)
