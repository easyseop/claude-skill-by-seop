from __future__ import annotations

SUPPORTED={'no_code','existing_artifact','python_local','java_cli'}

def validate(builder:str)->bool: return builder in SUPPORTED
