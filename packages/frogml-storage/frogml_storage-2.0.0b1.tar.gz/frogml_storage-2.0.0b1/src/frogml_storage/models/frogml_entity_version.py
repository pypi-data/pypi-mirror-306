from typing import Optional

from pydantic import BaseModel


class FrogMLEntityVersion(BaseModel):
    """
    Represent a metadata of uploaded entity

    Attributes:
        entity_name: The entity name (model | dataset)
        namespace: The namespace of the model | dataset
        version: The version of the model | dataset
    """

    entity_name: str
    namespace: Optional[str] = None
    version: str

    def __eq__(self, other):
        if not isinstance(other, FrogMLEntityVersion):
            return False
        if self.version != other.version:
            return False
        if self.namespace != other.namespace:
            return False
        if self.entity_name != other.entity_name:
            return False

        return True
