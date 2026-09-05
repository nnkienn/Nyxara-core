from typing import TypedDict
class CRAGeneratorState(TypedDict): 
    query : str
    retrieved_docs : list[str] 
    verdict : str
    attempts : int
    answer : str
    tenant_id : str
    grades : list[bool]
    candidate_k : int