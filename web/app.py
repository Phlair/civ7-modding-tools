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
import base64
from io import BytesIO
from pathlib import Path
from typing import Any

import yaml
import requests
from PIL import Image
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

# Mount reference icons from civ7_modding_tools package
icons_path = Path(__file__).parent.parent / "src" / "civ7_modding_tools" / "icons"
if icons_path.exists():
    app.mount("/icons", StaticFiles(directory=str(icons_path)), name="icons")

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
        /api/data/wonders  # Filtered from constructibles
        /api/data/leaders
    """
    # Special case: wonders - filter from constructibles
    if data_type == "wonders":
        try:
            constructibles = load_reference_data("constructibles")
            wonders = {
                "values": [
                    item for item in constructibles.get("values", [])
                    if item.get("id", "").startswith("WONDER_")
                ]
            }
            return wonders
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Constructibles data not found")
    
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


@app.post("/api/civilization/upload")
async def upload_yaml(file: UploadFile = File(...)) -> YAMLLoadResponse:
    """
    Upload and parse a YAML civilization file.

    Args:
        file: Uploaded YAML file

    Returns:
        Parsed YAML data and file path
    """
    if file.filename is None or not file.filename.endswith((".yml", ".yaml")):
        raise HTTPException(
            status_code=400, detail="File must be a YAML file (.yml or .yaml)"
        )

    try:
        contents = await file.read()
        data = yaml.safe_load(contents) or {}
        return YAMLLoadResponse(data=data, path=file.filename)
    except yaml.YAMLError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse YAML: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}",
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

        # Convert YAML to Python (YamlToPyConverter handles all preprocessing)
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
        
        # Debug: print the generated Python to see imports
        print(f"[BUILD_DEBUG] Generated Python code (first 2000 chars):")
        print(python_code[:2000])
        print(f"[BUILD_DEBUG] Generated Python code (looking for 'imports' section):")
        import_section = [line for line in python_code.split('\n') if 'import' in line.lower() and ('source_path' in line or 'target_name' in line)]
        for line in import_section[:10]:
            print(f"  {line}")

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
        error_detail = str(e)
        print(f"[BUILD_EXPORT_ERROR] Exception: {error_detail}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to build and export mod: {error_detail}",
        )
    finally:
        # Cleanup temp directory
        if temp_dir:
            try:
                shutil.rmtree(temp_dir)
            except Exception as cleanup_error:
                print(f"Warning: Failed to cleanup temp directory: {cleanup_error}")


class ExportToDiskRequest(BaseModel):
    """Request to export to disk."""
    
    data: dict[str, Any]
    download_path: str


@app.post("/api/civilization/export-disk")
async def export_yaml_to_disk(request: ExportToDiskRequest) -> dict[str, str]:
    """
    Export YAML to disk at specified path.

    Args:
        request: Contains data and target download path

    Returns:
        Confirmation with file path
    """
    try:
        download_path = Path(request.download_path).expanduser().resolve()
        
        if not download_path.exists():
            raise HTTPException(
                status_code=400,
                detail=f"Download path does not exist: {request.download_path}",
            )
        
        if not download_path.is_dir():
            raise HTTPException(
                status_code=400,
                detail=f"Download path is not a directory: {request.download_path}",
            )
        
        mod_id = request.data.get("metadata", {}).get("id", "mod")
        file_path = download_path / f"{mod_id}.yml"
        
        yaml_content = yaml.dump(
            request.data,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(yaml_content)
        
        return {
            "status": "success",
            "message": f"YAML exported to {file_path}",
            "path": str(file_path),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to export YAML to disk: {str(e)}",
        )


@app.post("/api/civilization/export-built-disk")
async def export_built_mod_to_disk(request: ExportToDiskRequest) -> dict[str, str]:
    """
    Export built mod to disk at specified path.

    Args:
        request: Contains data and target download path

    Returns:
        Confirmation with file path
    """
    temp_dir = None
    try:
        from civ7_modding_tools.yml_to_py import YamlToPyConverter
        
        download_path = Path(request.download_path).expanduser().resolve()
        
        if not download_path.exists():
            raise HTTPException(
                status_code=400,
                detail=f"Download path does not exist: {request.download_path}",
            )
        
        if not download_path.is_dir():
            raise HTTPException(
                status_code=400,
                detail=f"Download path is not a directory: {request.download_path}",
            )
        
        # Create temp directories
        temp_dir = tempfile.mkdtemp()
        temp_path = Path(temp_dir)
        yaml_file = temp_path / "config.yml"
        python_file = temp_path / "build_mod.py"
        build_dir = temp_path / "dist"

        # Save YAML to temp location
        with open(yaml_file, "w", encoding="utf-8") as f:
            yaml.dump(request.data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        # Convert YAML to Python (YamlToPyConverter handles all preprocessing)
        converter = YamlToPyConverter(request.data)
        python_code = converter.convert()

        # Modify the generated code to use our temp build directory
        mod_id = request.data.get("metadata", {}).get("id", "mod")
        new_call = f"mod.build(r'{str(build_dir)}')"
        
        # Try to replace both literal string and f-string variants
        patterns = [
            f"mod.build('./dist-{mod_id}')",
            "mod.build(f'./dist-{mod.mod_id}')",
        ]
        
        replaced = False
        for pattern in patterns:
            if pattern in python_code:
                python_code = python_code.replace(pattern, new_call)
                replaced = True
                break
        
        if not replaced:
            python_code = re.sub(
                r"mod\.build\(['\"]\.?/?dist-[^'\"]*['\"]\)",
                new_call,
                python_code
            )
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
            raise RuntimeError(f"Build failed: {error_msg}")

        # Check if build directory was created
        if not build_dir.exists():
            raise RuntimeError(f"Build directory not created at {build_dir}")

        # Copy built mod to download path
        output_dir = download_path / mod_id
        if output_dir.exists():
            shutil.rmtree(output_dir)
        
        shutil.copytree(build_dir, output_dir)
        
        # Also save YAML to download path
        yaml_output = download_path / f"{mod_id}.yml"
        yaml_content = yaml.dump(
            request.data,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
        with open(yaml_output, "w", encoding="utf-8") as f:
            f.write(yaml_content)
        
        return {
            "status": "success",
            "message": f"Mod exported to {output_dir}",
            "path": str(output_dir),
            "yaml_path": str(yaml_output),
        }
    except HTTPException:
        raise
    except ImportError as e:
        raise HTTPException(
            status_code=500,
            detail=f"civ7_modding_tools not available in backend environment: {str(e)}",
        )
    except Exception as e:
        error_detail = str(e)
        print(f"[BUILD_EXPORT_DISK_ERROR] Exception: {error_detail}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to build and export mod to disk: {error_detail}",
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


# ============================================================================
# Icon Generation Endpoints
# ============================================================================


class IconGenerateRequest(BaseModel):
    """Request to generate an icon using OpenAI."""
    prompt: str
    icon_type: str  # 'civilization', 'unit', 'building'
    model: str = "gpt-image-1-mini"
    quality: str = "medium"
    reference_images: list[str] = []
    api_key: str


class IconSaveRequest(BaseModel):
    """Request to save a generated icon."""
    image_b64: str
    icon_type: str
    target_name: str
    prompt: str


@app.post("/api/icons/generate")
async def generate_icon(request: IconGenerateRequest) -> dict[str, Any]:
    """
    Generate an icon using OpenAI GPT Image API.
    
    Args:
        request: Icon generation parameters
        
    Returns:
        Generated icon as base64 string
    """
    try:
        from openai import OpenAI
        
        # Build prompt with style guidance based on icon type
        prompt_template = {
            'civilization': (
                f"Create a minimalist, geometric game icon for a civilization. "
                f"Description: {request.prompt}\n"
                f"Ensure consistency in colour/shade with examples."
                f"Requirements: 256x256 PNG, white emblem with transparent background, "
                f"clean vector-like style, recognizable at any size, matches Civilization VII aesthetic. "
                f"No text or labels. Match the artistic style of the reference images."
            ),
            'unit': (
                f"Create a minimalist game icon for a unit in civilization VII. "
                f"Description: {request.prompt}\n"
                f"Ensure consistency in colour/shade with examples."
                f"Requirements: 256x256 PNG, white emblem with transparent background, "
                f"clean vector-like style, recognizable at any size, matches Civilization VII aesthetic. "
                f"No text or labels. Match the artistic style of the reference images."
            ),
            'building': (
                f"Create a minimalist game icon for a building or improvement in civilization VII. "
                f"Description: {request.prompt}\n"
                f"Ensure consistency in style/colours/shading with examples. "
                f"Requirements: 256x256 PNG, gold diamond with building image in centre, transparent background. "
                f"Style: Match Civilization VII's icons that have been provided. "
                f"No text or labels. Match the artistic style of the reference images."
            ),
        }
        
        prompt = prompt_template.get(request.icon_type, request.prompt)
        
        # Initialize OpenAI client
        client = OpenAI(api_key=request.api_key)
        
        # Load reference image files
        reference_file_handles = []
        icons_dir = Path(__file__).parent.parent / "src" / "civ7_modding_tools" / "icons"
        
        if request.reference_images:
            for icon_path_str in request.reference_images:
                # Parse path like "/icons/civs/america.png" or "/icons/units/ANT/atlatl.png"
                # Strip leading /icons/ and use the rest as relative path
                if icon_path_str.startswith('/icons/'):
                    relative_path = icon_path_str[7:]  # Remove '/icons/' prefix
                    icon_path = icons_dir / relative_path
                    if icon_path.exists():
                        reference_file_handles.append(open(icon_path, "rb"))
                    else:
                        print(f"[ICON_WARNING] Reference icon not found: {icon_path}")
                else:
                    # Legacy format: just icon name (assume civs/)
                    icon_path = icons_dir / "civs" / f"{icon_path_str}.png"
                    if icon_path.exists():
                        reference_file_handles.append(open(icon_path, "rb"))
        
        # Use images.edit() with reference images (GPT Image 1.5 supports multiple references)
        if reference_file_handles:
            result = client.images.edit(
                model=request.model,
                image=reference_file_handles,
                prompt=prompt,
            )
            
            # Close file handles
            for fh in reference_file_handles:
                fh.close()
        else:
            # Fallback to generate if no references provided
            result = client.images.generate(
                model=request.model,
                prompt=prompt,
                size="1024x1024",
                n=1,
            )
        
        # Extract base64 image (edit API returns b64_json by default)
        b64_image = result.data[0].b64_json
        
        # Resize to 256x256
        try:
            image_bytes = base64.b64decode(b64_image)
            img = Image.open(BytesIO(image_bytes))
            img_resized = img.resize((256, 256), Image.Resampling.LANCZOS)
            
            # Convert back to base64
            buffer = BytesIO()
            img_resized.save(buffer, format="PNG")
            resized_b64 = base64.b64encode(buffer.getvalue()).decode()
        except Exception:
            resized_b64 = b64_image
        
        return {
            "success": True,
            "image": resized_b64,
            "size": "256x256",
            "references_used": len(reference_file_handles),
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Icon generation failed: {str(e)}"
        )


@app.post("/api/icons/save")
async def save_generated_icon(request: IconSaveRequest) -> dict[str, Any]:
    """
    Save a generated icon and prepare for import into mod.
    
    Args:
        request: Save request with icon data
        
    Returns:
        Icon path, import configuration, and metadata for addition to mod config
    """
    try:
        # Create persistent directory for generated icons (relative to project root)
        # This ensures the file exists when the mod is built
        icons_dir = Path.cwd() / "generated_icons"
        icons_dir.mkdir(exist_ok=True)
        
        # Save image file
        filename = f"{request.target_name}.png"
        file_path = icons_dir / filename
        
        image_bytes = base64.b64decode(request.image_b64)
        with open(file_path, "wb") as f:
            f.write(image_bytes)
        
        # Create import configuration for YAML - use ABSOLUTE path so it works from temp dir
        import_id = f"{request.icon_type}_icon_{request.target_name}"
        # Convert to forward slashes for cross-platform compatibility in generated Python code
        absolute_source_path = str(file_path.resolve()).replace("\\", "/")
        import_entry = {
            "id": import_id,
            "source_path": absolute_source_path,
            "target_name": request.target_name,
        }
        
        # Icon path in mod (what gets referenced in icon.path)
        # Use civs subfolder for civilization icons, units/ for unit icons
        if request.icon_type == "civilization":
            subfolder = "civs/"
        elif request.icon_type == "unit":
            subfolder = "units/"
        else:
            subfolder = ""
        icon_path = f"icons/{subfolder}{request.target_name}"
        
        return {
            "success": True,
            "icon_path": icon_path,
            "file_path": str(file_path),
            "target_name": request.target_name,
            "icon_type": request.icon_type,
            "import_entry": import_entry,
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save icon: {str(e)}"
        )


@app.post("/api/icons/upload")
async def upload_icon(file: UploadFile = File(...), icon_type: str = Form("civilization")) -> dict[str, Any]:
    """
    Upload a local icon file and save it for use in the mod.
    
    Args:
        file: Uploaded image file
        icon_type: Type of icon ('civilization', 'unit', 'building')
        
    Returns:
        Icon path and import configuration
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith("image/"):
            raise ValueError(f"Invalid file type: {file.content_type}. Must be an image.")
        
        # Create persistent directory for uploaded icons
        icons_dir = Path.cwd() / "generated_icons"
        icons_dir.mkdir(exist_ok=True)
        
        # Read and validate image
        content = await file.read()
        if not content:
            raise ValueError("File is empty")
        
        try:
            img = Image.open(BytesIO(content))
            # Resize to 256x256 for consistency
            img_resized = img.resize((256, 256), Image.Resampling.LANCZOS)
        except Exception as e:
            raise ValueError(f"Failed to process image: {str(e)}")
        
        # Generate unique filename
        import time
        timestamp = int(time.time() * 1000)
        filename = f"icon_uploaded_{timestamp}.png"
        file_path = icons_dir / filename
        
        # Save image
        img_resized.save(file_path, "PNG")
        
        # Create import configuration - include icon_type in ID for proper filtering
        import_id = f"{icon_type}_icon_uploaded_{timestamp}"
        absolute_source_path = str(file_path.resolve()).replace("\\", "/")
        import_entry = {
            "id": import_id,
            "source_path": absolute_source_path,
            "target_name": filename.replace(".png", ""),
        }
        
        # Icon path in mod
        # Use civs subfolder for civilization icons, units/ for unit icons
        if icon_type == "civilization":
            subfolder = "civs/"
        elif icon_type == "unit":
            subfolder = "units/"
        else:
            subfolder = ""
        icon_path = f"icons/{subfolder}{filename.replace('.png', '')}"
        
        return {
            "success": True,
            "icon_path": icon_path,
            "file_path": str(file_path),
            "target_name": filename.replace(".png", ""),
            "import_entry": import_entry,
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Upload failed: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload icon: {str(e)}"
        )


class CitizenNamesGenerateRequest(BaseModel):
    """Request to generate citizen names using OpenAI."""
    civilization_name: str
    adjective: str
    count: int = 10
    api_key: str


@app.post("/api/citizens/generate")
async def generate_citizen_names(request: CitizenNamesGenerateRequest) -> dict[str, list[str]]:
    """
    Generate culturally appropriate citizen names using OpenAI GPT.
    
    Args:
        request: Citizen names generation parameters
        
    Returns:
        Lists of male and female names
    """
    try:
        from openai import OpenAI
        
        # Initialize OpenAI client
        client = OpenAI(api_key=request.api_key)
        
        prompt = f"""Generate {request.count} culturally appropriate male and {request.count} female citizen names for the {request.civilization_name} civilization ({request.adjective} people).

Requirements:
- Names should be historically accurate or inspired by the culture
- Use authentic {request.adjective} naming conventions
- Mix common and uncommon names for variety
- Avoid modern Western names unless culturally appropriate
- Return ONLY a JSON object with two arrays: "male_names" and "female_names"
- Each array should contain exactly {request.count} strings
- Example format: {{"male_names": ["Name1", "Name2"], "female_names": ["Name1", "Name2"]}}

Generate the names now:"""
        
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {
                    "role": "system",
                    "content": "You are a historical naming expert. Return ONLY valid JSON with no additional text."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Parse JSON response
        content = response.choices[0].message.content
        # Strip markdown code fences if present
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("\n", 1)[0]
            if content.startswith("json"):
                content = content[4:].strip()
        
        import json
        names_data = json.loads(content)
        
        return {
            "male_names": names_data.get("male_names", []),
            "female_names": names_data.get("female_names", [])
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate citizen names: {str(e)}"
        )


class CityNamesGenerateRequest(BaseModel):
    """Request to generate city names using OpenAI."""
    civilization_name: str
    adjective: str
    count: int = 16
    api_key: str


@app.post("/api/cities/generate")
async def generate_city_names(request: CityNamesGenerateRequest) -> dict[str, list[str]]:
    """
    Generate culturally appropriate city names using OpenAI GPT.
    
    Args:
        request: City names generation parameters
        
    Returns:
        List of city names
    """
    try:
        from openai import OpenAI
        
        # Initialize OpenAI client
        client = OpenAI(api_key=request.api_key)
        
        prompt = f"""Generate {request.count} culturally appropriate city names for the {request.civilization_name} civilization.
Requirements:
- Names should be historically accurate or inspired by actual {request.adjective} cities
- Use authentic {request.adjective} naming conventions and language
- Mix well-known historical cities and lesser-known regional cities for variety
- They should be in order from major cities to smaller towns
- Avoid generic or Western names unless culturally appropriate
- Return ONLY a JSON object with one array: "cities"
- The array should contain exactly {request.count} strings (just the city names)
- Example format: {{"cities": ["CityName1", "CityName2", "CityName3"]}}

Generate the city names now:"""
        
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {
                    "role": "system",
                    "content": "You are a historical geographer specialising in city names. Return ONLY valid JSON with no additional text."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Parse JSON response
        content = response.choices[0].message.content
        # Strip markdown code fences if present
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("\n", 1)[0]
            if content.startswith("json"):
                content = content[4:].strip()
        
        import json
        cities_data = json.loads(content)
        
        return {
            "cities": cities_data.get("cities", [])
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate city names: {str(e)}"
        )


class NamedPlacesGenerateRequest(BaseModel):
    """Request to generate named places using OpenAI."""
    civilization_name: str
    adjective: str
    place_type: str  # 'rivers' or 'volcanoes'
    count: int = 8
    api_key: str


@app.post("/api/named-places/generate")
async def generate_named_places(request: NamedPlacesGenerateRequest) -> dict[str, list[dict[str, str]]]:
    """
    Generate culturally appropriate river or volcano names using OpenAI GPT.
    
    Args:
        request: Named places generation parameters
        
    Returns:
        List of named places with type IDs and display names
    """
    try:
        from openai import OpenAI
        
        # Initialize OpenAI client
        client = OpenAI(api_key=request.api_key)
        
        place_desc = "rivers" if request.place_type == "rivers" else "volcanoes"
        prefix = "RIVER" if request.place_type == "rivers" else "VOLCANO"
        additional_info = "Use relevant local hills and/or mountains if there aren't geographical volcanoes" if request.place_type == "volcanoes" else ""
        
        prompt = f"""Generate {request.count} culturally appropriate {place_desc} names for the {request.civilization_name} civilization ({request.adjective} region).

Requirements:
- Names should be historically accurate or geographically plausible for the {request.adjective} region
- Use authentic {request.adjective} naming conventions and language
- Mix well-known and lesser-known {place_desc}. {additional_info}
- Each entry needs both a TYPE_ID and a display name
- TYPE_ID format: {prefix}_NAME_IN_CAPS (e.g., {prefix}_THAMES, {prefix}_MOUNT_VESUVIUS)
- Display name: The actual name as shown to players (e.g., "Thames", "Mount Vesuvius")
- Return ONLY a JSON object with one array: "places"
- Each place has "type_id" and "name" fields
- Example format: {{"places": [{{"type_id": "{prefix}_THAMES", "name": "Thames"}}, {{"type_id": "{prefix}_SEVERN", "name": "Severn"}}]}}

Generate the {place_desc} names now:"""
        
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {
                    "role": "system",
                    "content": "You are a geographic and historical naming expert. Return ONLY valid JSON with no additional text."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Parse JSON response
        content = response.choices[0].message.content
        # Strip markdown code fences if present
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("\n", 1)[0]
            if content.startswith("json"):
                content = content[4:].strip()
        
        import json
        places_data = json.loads(content)
        
        return {
            "places": places_data.get("places", [])
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate named places: {str(e)}"
        )


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

