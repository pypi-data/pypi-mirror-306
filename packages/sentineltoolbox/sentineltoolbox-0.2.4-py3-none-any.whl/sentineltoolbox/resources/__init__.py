from typing import Any

from sentineltoolbox.readers.resources import load_resource_file

MAPPING_LEGACY_SEMANTIC_TO_DPR_WITH_SAT: dict[str, Any] = load_resource_file("metadata/mapping_legacy_dpr.json")
MAPPING_LEGACY_SEMANTIC_TO_DPR: dict[str, Any] = {}

PRODUCT_FORMATS: dict[str, Any] = load_resource_file("metadata/product_formats.json")
MAPPING_DPR_WITH_SAT_SEMANTIC_TO_LEGACY: dict[str, Any] = {}
MAPPING_DPR_SEMANTIC_TO_LEGACY: dict[str, Any] = {}

LIST_DPR_ADFS_FROM_SPLIT_LEGACY: list[str] = []
for legacy, dpr_outputs in MAPPING_LEGACY_SEMANTIC_TO_DPR_WITH_SAT.items():
    if isinstance(dpr_outputs, str):
        dpr_outputs = [dpr_outputs]
    for dpr_sat in dpr_outputs:
        dpr = dpr_sat[3:]
        if len(dpr_outputs) > 1:
            MAPPING_LEGACY_SEMANTIC_TO_DPR.setdefault(legacy, []).append(dpr)
            LIST_DPR_ADFS_FROM_SPLIT_LEGACY.append(dpr)
        else:
            MAPPING_LEGACY_SEMANTIC_TO_DPR[legacy] = dpr
        MAPPING_DPR_WITH_SAT_SEMANTIC_TO_LEGACY.setdefault(dpr_sat, []).append(legacy)
        MAPPING_DPR_SEMANTIC_TO_LEGACY.setdefault(dpr, []).append(legacy)

LIST_DPR_ADFS_FROM_MERGED_LEGACY: list[str] = []
LIST_DPR_WITH_SAT_ADFS_FROM_MERGED_LEGACY: list[str] = []
for dpr_sat, legacies in MAPPING_DPR_WITH_SAT_SEMANTIC_TO_LEGACY.items():
    dpr = dpr_sat[3:]
    if len(legacies) > 1:
        LIST_DPR_ADFS_FROM_MERGED_LEGACY.append(dpr)
        LIST_DPR_WITH_SAT_ADFS_FROM_MERGED_LEGACY.append(dpr_sat)
