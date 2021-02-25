from typing import Mapping


def inverse_mapping(mapping: Mapping) -> Mapping:
    """
    Inverse key -> value to value -> key
    # NOTE: make sure values are unique
    """
    return mapping.__class__(map(reversed, mapping.items()))


def get_applicable_filters(query_params: Mapping, filter_map: dict) -> dict:
    """
    get applicable filters from filter map
    """
    return {
        filter_map.get(k): v for k, v in query_params.items() if
        k in filter_map.keys() and v is not None and v != ''
    }
