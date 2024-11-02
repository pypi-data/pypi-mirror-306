from .completeness import Completeness
from .borda_count import BordaCount


def start_borda_count(data: list, factor: int) -> dict:
    borda_instance = BordaCount(data, factor)
    return borda_instance.borda_result()

def start_completeness(data: list, weight: int) -> dict:
    completenss_instance = Completeness(data, weight)
    return completenss_instance.completeness_result()
