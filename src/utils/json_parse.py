"""Utilities for parsing and validating JSON responses from LLM."""

import json
import re
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, ValidationError


def extract_json(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract JSON from text, handling cases where JSON is embedded in markdown or text.
    
    Args:
        text: Text that may contain JSON
        
    Returns:
        Parsed JSON dictionary or None if not found
    """
    # Try direct JSON parse first
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON in code blocks
    json_block_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    matches = re.findall(json_block_pattern, text, re.DOTALL)
    if matches:
        try:
            return json.loads(matches[0])
        except json.JSONDecodeError:
            pass
    
    # Try to find JSON object in text
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, text, re.DOTALL)
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    
    return None


def validate_and_fix_json(
    data: Dict[str, Any],
    schema: BaseModel,
    strict: bool = False
) -> BaseModel:
    """
    Validate JSON data against a Pydantic schema and fix common issues.
    
    Args:
        data: JSON data to validate
        schema: Pydantic model class
        strict: If True, raise error on validation failure
        
    Returns:
        Validated Pydantic model instance
    """
    try:
        return schema(**data)
    except ValidationError as e:
        if strict:
            raise
        
        # Try to fix common issues
        fixed_data = _fix_common_issues(data, schema)
        try:
            return schema(**fixed_data)
        except ValidationError:
            # If still fails, return partial model
            print(f"Warning: Could not fully validate data: {e}")
            return schema(**{k: v for k, v in data.items() if k in schema.model_fields})


def _fix_common_issues(data: Dict[str, Any], schema: BaseModel) -> Dict[str, Any]:
    """Fix common JSON validation issues."""
    fixed = data.copy()
    schema_fields = schema.model_fields
    
    # Ensure required fields exist
    for field_name, field_info in schema_fields.items():
        if field_name not in fixed:
            # Check for default value
            if hasattr(field_info, 'default') and field_info.default is not ...:
                fixed[field_name] = field_info.default
            elif hasattr(field_info, 'default_factory') and field_info.default_factory:
                fixed[field_name] = field_info.default_factory()
            else:
                # Set empty value based on annotation
                annotation = field_info.annotation
                if annotation == str or (hasattr(annotation, '__origin__') and str in getattr(annotation, '__args__', [])):
                    fixed[field_name] = ""
                elif annotation == list or (hasattr(annotation, '__origin__') and annotation.__origin__ is list):
                    fixed[field_name] = []
                elif annotation == dict or (hasattr(annotation, '__origin__') and annotation.__origin__ is dict):
                    fixed[field_name] = {}
    
    # Convert types if needed
    for field_name, field_info in schema_fields.items():
        if field_name in fixed:
            value = fixed[field_name]
            annotation = field_info.annotation
            
            # Handle List types
            if hasattr(annotation, '__origin__') and annotation.__origin__ is list:
                if not isinstance(value, list):
                    fixed[field_name] = [value] if value else []
            
            # Handle Optional types (Union[Type, None])
            if hasattr(annotation, '__origin__'):
                if annotation.__origin__ is type(None) or (hasattr(annotation, '__args__') and type(None) in annotation.__args__):
                    # Extract the actual type from Optional/Union
                    if hasattr(annotation, '__args__'):
                        args = [a for a in annotation.__args__ if a is not type(None)]
                        if args:
                            actual_type = args[0]
                            if not isinstance(value, actual_type) and value is not None:
                                try:
                                    fixed[field_name] = actual_type(value)
                                except (ValueError, TypeError):
                                    pass
    
    return fixed


def clean_json_string(json_str: str) -> str:
    """
    Clean JSON string by removing common formatting issues.
    
    Args:
        json_str: JSON string that may have formatting issues
        
    Returns:
        Cleaned JSON string
    """
    # Remove trailing commas
    json_str = re.sub(r',\s*}', '}', json_str)
    json_str = re.sub(r',\s*]', ']', json_str)
    
    # Fix single quotes to double quotes
    json_str = re.sub(r"'([^']*)'", r'"\1"', json_str)
    
    # Remove comments (not standard JSON but sometimes present)
    json_str = re.sub(r'//.*?$', '', json_str, flags=re.MULTILINE)
    json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
    
    return json_str

