from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ValidationError

DataT = TypeVar('DataT')

class Response(BaseModel, Generic[DataT]):
  message : str
  data: Optional[DataT] = None