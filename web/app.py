"""
FastAPI backend for Civilization VII mod YAML editor.

Provides REST API for:
- Loading/saving YAML civilization configurations
- Exposing validation data from JSON reference files
- Form field autocomplete and validation
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import Response, StreamingResponse
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


class YAMLLoadRequest(BaseModel):
    """Request to load a YAML file."""

    file_path: str


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
async def load_yaml(request: YAMLLoadRequest) -> YAMLLoadResponse:
    """
    Load a YAML civilization file.

    Args:
        request: Contains file path to load

    Returns:
        Parsed YAML data
    """
    path = Path(request.file_path)

    if not path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {request.file_path}")

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


@app.post("/api/civilization/export-built")
async def export_built_mod(data: dict[str, Any]) -> StreamingResponse:
    """
    Export data as a fully built mod (zipped).

    Processes the configuration through the mod building pipeline:
    1. Convert YAML to Python using YamlToPyConverter
    2. Execute the generated Python to build the mod
    3. Zip the generated mod folder
    4. Return zip file

    Args:
        data: Dictionary containing mod configuration

    Returns:
        Zip file as downloadable response
    """
    temp_dir = None
    try:
        from civ7_modding_tools.yml_to_py import YamlToPyConverter

        # Create temp directories
        temp_dir = tempfile.mkdtemp()
        temp_path = Path(temp_dir)
        yaml_file = temp_path / "config.yml"
        python_file = temp_path / "build_mod.py"
        build_dir = temp_path / "dist"

        # Save YAML to temp location
        with open(yaml_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        # Convert YAML to Python
        converter = YamlToPyConverter(data)
        python_code = converter.convert()

        # Modify the generated code to use our temp build directory
        mod_id = data.get("metadata", {}).get("id", "mod")
        new_call = f"mod.build(r'{str(build_dir)}')"
        
        # Try to replace both literal string and f-string variants
        patterns = [
            # Literal string: mod.build('./dist-babylon')
            f"mod.build('./dist-{mod_id}')",
            # F-string: mod.build(f'./dist-{{mod.mod_id}}')
            "mod.build(f'./dist-{mod.mod_id}')",
        ]
        
        replaced = False
        for pattern in patterns:
            if pattern in python_code:
                python_code = python_code.replace(pattern, new_call)
                replaced = True
                break
        
        if not replaced:
            # Fallback: use regex to find any mod.build call
            python_code = re.sub(
                r"mod\.build\(['\"]\.?/?dist-[^'\"]*['\"]\)",
                new_call,
                python_code
            )
            # Also try f-string variant
            python_code = re.sub(
                r"mod\.build\(f['\"]\.?/?dist-\{[^}]*\}['\"]\)",
                new_call,
                python_code
            )

        # Save generated Python
        with open(python_file, "w", encoding="utf-8") as f:
            f.write(python_code)

        # Execute the generated Python to build the mod
        result = subprocess.run(
            [sys.executable, str(python_file)],
            cwd=str(temp_path),
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "Unknown error during build"
            print(f"[BUILD_ERROR] Build process failed:")
            print(f"[BUILD_ERROR] Return code: {result.returncode}")
            print(f"[BUILD_ERROR] STDERR: {result.stderr}")
            print(f"[BUILD_ERROR] STDOUT: {result.stdout}")
            raise RuntimeError(f"Build failed: {error_msg}")

        # Check if build directory was created
        if not build_dir.exists():
            raise RuntimeError(f"Build directory not created at {build_dir}")

        # Create zip file in memory
        zip_path = temp_path / f"{mod_id}.zip"

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in build_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(build_dir)
                    zipf.write(file_path, arcname)

        # Read zip file into memory
        with open(zip_path, "rb") as f:
            zip_content = f.read()

        # Return zip file as response
        return StreamingResponse(
            iter([zip_content]),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={mod_id}.zip"},
        )

    except ImportError as e:
        raise HTTPException(
            status_code=500,
            detail=f"civ7_modding_tools not available in backend environment: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to build and export mod: {str(e)}",
        )
    finally:
        # Cleanup temp directory
        if temp_dir:
            try:
                shutil.rmtree(temp_dir)
            except Exception as cleanup_error:
                print(f"Warning: Failed to cleanup temp directory: {cleanup_error}")


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

