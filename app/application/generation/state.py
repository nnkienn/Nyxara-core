from typing import TypedDict
class CRAGeneratorState(TypedDict): 
    query : str
    retrieved_docs : list[str] 
    verdict : str
    attempts : int
    answer : str
    tenant_id : str
    """
    Represents the state of a CRAG generator.
    """
    # Define the fields of the CRAG generator state here
    # For example:
    # field_name: field_type                                                