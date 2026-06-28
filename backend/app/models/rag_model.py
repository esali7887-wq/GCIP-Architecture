from pydantic import BaseModel, Field

class RAGUploadModel(BaseModel):
    project_id: str = Field(..., description="ID of the project to associate this document with.", example="PRJ-101")
    source_name: str = Field(..., description="Name or identifier of the source document.", example="contract_clause_v1")
    text: str = Field(..., description="Raw text content of the document.", example="Sözleşme bedelinin %10'u oranında avans verilecektir.")

class RAGQueryModel(BaseModel):
    project_id: str = Field(..., description="ID of the project containing the documents.", example="PRJ-101")
    query: str = Field(..., description="Semantic search query.", example="Ön ödeme ve hakediş kuralları")
    k: int = Field(default=3, ge=1, le=10, description="Number of matches to return.", example=3)
