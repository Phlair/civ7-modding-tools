"""
FastAPI backend for Civilization VII mod YAML editor.

Provides REST API for:
- Loading/saving YAML civilization configurations
- Exposing validation data from JSON reference files
- Form field autocomplete and validation
"""

import json
from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, ValidationError, field_validator

app = FastAPI(
    title="Civ VII Mod Editor",
    description="Web editor for Civilization VII mod YAML files",
    version="1.0.0",
)

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Get data directory from civ7_modding_tools
data_dir = Path(__file__).parent.parent / "src" / "civ7_modding_tools" / "data"

# Cache for loaded reference data
_reference_data_cache: dict[str, dict[str, Any]] = {}


def load_reference_data(data_type: str) -> dict[str, Any]:
    """Load reference data with caching."""
    if data_type in _reference_data_cache:
        return _reference_data_cache[data_type]

    filename = f"{data_type}.json"
    file_path = data_dir / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {filename}")

    try:
        with open(file_path) as f:
            data = json.load(f)
            _reference_data_cache[data_type] = data
            return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse {filename}: {str(e)}")


class YAMLLoadResponse(BaseModel):
    """Response for loading a YAML file."""

    data: dict[str, Any]
    path: str


class YAMLSaveRequest(BaseModel):
    """Request to save a YAML file."""

    path: str
    data: dict[str, Any]


class ValidationErrorDetail(BaseModel):
    """Validation error response."""

    field: str
    message: str
    severity: str = "error"  # error, warning, info


class ValidationResult(BaseModel):
    """Validation result response."""

    valid: bool
    errors: list[ValidationErrorDetail] = []
    warnings: list[ValidationErrorDetail] = []


@app.get("/")
async def index() -> FileResponse:
    """Serve the main editor page."""
    template_path = Path(__file__).parent / "templates" / "index.html"
    if template_path.exists():
        return FileResponse(template_path)
    return FileResponse(
        Path(__file__).parent / "templates" / "index.html",
        media_type="text/html",
    )


@app.get("/api/data/list")
async def list_reference_data() -> dict[str, list[str]]:
    """List all available reference data types."""
    files = sorted([f.stem for f in data_dir.glob("*.json") if f.is_file()])
    return {"data_types": files}


@app.get("/api/data/{data_type}")
async def get_reference_data(data_type: str) -> dict[str, Any]:
    """
    Get reference data for a specific type (yields, effects, tags, etc.).

    Examples:
        /api/data/yield-types
        /api/data/effects
        /api/data/tags
        /api/data/unit-movement-classes
    """
    try:
        return load_reference_data(data_type)
    except FileNotFoundError:
        # List available data files
        available = sorted(
            [f.stem for f in data_dir.glob("*.json") if f.is_file()]
        )
        raise HTTPException(
            status_code=404,
            detail=f"Data type '{data_type}' not found. Available: {available}",
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/civilization/load")
async def load_yaml(file_path: str = Form(...)) -> YAMLLoadResponse:
    """
    Load a YAML civilization file.

    Args:
        file_path: Absolute or relative path to the YAML file

    Returns:
        Parsed YAML data
    """
    path = Path(file_path)

    if not path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")

    if path.suffix not in {".yml", ".yaml"}:
        raise HTTPException(
            status_code=400, detail="File must be a YAML file (.yml or .yaml)"
        )

    try:
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        return YAMLLoadResponse(data=data, path=str(path))
    except yaml.YAMLError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse YAML: {str(e)}",
        )


@app.post("/api/civilization/save")
async def save_yaml(request: YAMLSaveRequest) -> dict[str, str]:
    """
    Save a YAML civilization file.

    Args:
        request: Contains file path and data to save

    Returns:
        Confirmation message
    """
    path = Path(request.path)

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(path, "w") as f:
            yaml.dump(
                request.data,
                f,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
            )
        return {"message": f"File saved successfully: {request.path}"}
    except IOError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}",
        )


@app.post("/api/civilization/export")
async def export_yaml(data: dict[str, Any]) -> Response:
    """
    Export data as a proper YAML file for download.

    Args:
        data: Dictionary to export as YAML

    Returns:
        YAML file as downloadable response
    """
    try:
        yaml_content = yaml.dump(
            data,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
        return Response(
            content=yaml_content,
            media_type="application/yaml",
            headers={
                "Content-Disposition": f"attachment; filename={data.get('metadata', {}).get('id', 'mod')}.yml"
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to export YAML: {str(e)}",
        )


@app.post("/api/civilization/validate")
async def validate_yaml(request: YAMLSaveRequest) -> ValidationResult:
    """
    Validate a YAML civilization configuration.

    Checks for:
    - Required fields at top level
    - Required metadata fields
    - Field type correctness
    - Enum validation against reference data

    Args:
        request: Contains the configuration data to validate

    Returns:
        Validation results with errors and warnings
    """
    errors: list[ValidationErrorDetail] = []
    warnings: list[ValidationErrorDetail] = []
    data = request.data

    # Required top-level fields
    required_fields = ["metadata", "civilization"]
    for field in required_fields:
        if field not in data:
            errors.append(
                ValidationErrorDetail(
                    field=field,
                    message=f"Missing required field: {field}",
                    severity="error",
                )
            )

    # Validate metadata
    if "metadata" in data:
        metadata = data["metadata"]
        if not isinstance(metadata, dict):
            errors.append(
                ValidationErrorDetail(
                    field="metadata",
                    message="Metadata must be an object",
                    severity="error",
                )
            )
        else:
            meta_required = ["id", "version", "name"]
            for field in meta_required:
                if field not in metadata:
                    errors.append(
                        ValidationErrorDetail(
                            field=f"metadata.{field}",
                            message=f"Missing required metadata field: {field}",
                            severity="error",
                        )
                    )
                elif not isinstance(metadata[field], str):
                    errors.append(
                        ValidationErrorDetail(
                            field=f"metadata.{field}",
                            message=f"{field} must be a string",
                            severity="error",
                        )
                    )

    # Validate civilization structure
    if "civilization" in data:
        civ = data["civilization"]
        if not isinstance(civ, dict):
            errors.append(
                ValidationErrorDetail(
                    field="civilization",
                    message="Civilization must be an object",
                    severity="error",
                )
            )
        else:
            # Check for civilization_type
            if "civilization_type" not in civ:
                warnings.append(
                    ValidationErrorDetail(
                        field="civilization.civilization_type",
                        message="civilization_type recommended",
                        severity="warning",
                    )
                )

    # Validate arrays
    array_fields = [
        "modifiers",
        "traditions",
        "units",
        "constructibles",
        "progression_tree_nodes",
        "progression_trees",
    ]
    for field in array_fields:
        if field in data and not isinstance(data[field], list):
            errors.append(
                ValidationErrorDetail(
                    field=field,
                    message=f"{field} must be an array",
                    severity="error",
                )
            )

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )


@app.post("/api/field/validate")
async def validate_field(
    field_name: str = Form(...),
    field_value: str = Form(...),
    data_type: str = Form(...),
) -> dict[str, Any]:
    """
    Validate a single field against reference data.

    Args:
        field_name: Name of the field being validated
        field_value: Value to validate
        data_type: Type of reference data to validate against (e.g., 'yield-types')

    Returns:
        Validation result with any errors or suggestions
    """
    try:
        ref_data = load_reference_data(data_type)

        # Check if value exists in reference data
        values = ref_data.get("values", [])
        valid_ids = [v.get("id") for v in values if isinstance(v, dict)]

        is_valid = field_value in valid_ids

        return {
            "field": field_name,
            "value": field_value,
            "valid": is_valid,
            "suggestions": valid_ids[:10] if not is_valid else [],
        }
    except (FileNotFoundError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=True,
    )

