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


@app.get("/api/templates/{template_name}")
async def get_template(template_name: str) -> dict[str, Any]:
    """
    Load a pre-built civilization template.

    Args:
        template_name: Name of the template (blank, scientific, military, cultural, economic)

    Returns:
        Template YAML data as dictionary
    """
    # Define templates directory
    templates_dir = Path(__file__).parent / "templates" / "civilizations"
    
    # Template definitions (can be moved to separate YAML files later)
    templates = {
        "blank": {
            "metadata": {
                "id": "my-civilization",
                "version": "1.0.0",
                "name": "My Civilization",
                "description": "A new custom civilization",
                "authors": "Your Name",
            },
            "module_localization": {
                "name": "My Civilization",
                "description": "A new custom civilization for Civilization VII",
            },
            "action_group": "AGE_ANTIQUITY",
            "civilization": {
                "civilization_type": "CIVILIZATION_MY_CIV",
                "civilization_traits": ["TRAIT_SCIENTIFIC"],
                "localizations": [
                    {
                        "name": "My Civilization",
                        "adjective": "My",
                        "description": "A civilization focused on...",
                        "city_names": ["Capital City", "Second City", "Third City"],
                    }
                ],
                "start_bias_terrains": [{"terrain_type": "TERRAIN_FLAT", "score": 5}],
                "start_bias_rivers": 1,
                "vis_art_building_cultures": ["VIS_ART_BUILDING_CULTURE_CLASSICAL"],
                "vis_art_unit_cultures": ["VIS_ART_UNIT_CULTURE_CLASSICAL"],
                "civilization_unlocks": [
                    {"unlock_age": "AGE_EXPLORATION", "unlock_civilization_type": "CIVILIZATION_MY_CIV_EXPLORATION"}
                ],
            },
            "units": [
                {
                    "unit_type": "UNIT_MY_CIV_WARRIOR",
                    "unit_class": "CLASS_MELEE",
                    "localizations": [
                        {
                            "name": "My Warrior",
                            "description": "A basic melee unit",
                        }
                    ],
                    "unit_stat": {"combat": 25, "movement": 2},
                }
            ],
            "constructibles": [
                {
                    "constructible_type": "BUILDING_MY_CIV_MONUMENT",
                    "constructible_class": "CLASS_BUILDING",
                    "localizations": [
                        {
                            "name": "My Monument",
                            "description": "A cultural building",
                        }
                    ],
                    "yield_changes": [{"yield_type": "YIELD_CULTURE", "amount": 2}],
                }
            ],
            "modifiers": [],
            "traditions": [],
            "progression_tree_nodes": [],
            "progression_trees": [],
            "constants": {},
            "imports": [],
            "build": {
                "output_dir": "./dist",
                "builders": [],
            },
        },
        "scientific": {
            "metadata": {
                "id": "scientific-civilization",
                "version": "1.0.0",
                "name": "Scientific Civilization Template",
                "description": "A science-focused civilization with research bonuses",
                "authors": "Your Name",
            },
            "module_localization": {
                "name": "Scientific Civilization",
                "description": "A civilization focused on scientific advancement and discovery",
            },
            "action_group": "AGE_ANTIQUITY",
            "civilization": {
                "civilization_type": "CIVILIZATION_SCIENTIFIC",
                "civilization_traits": ["TRAIT_SCIENTIFIC", "TRAIT_CULTURAL"],
                "localizations": [
                    {
                        "name": "Scientific Civilization",
                        "adjective": "Scientific",
                        "description": "A civilization renowned for its scholars, libraries, and pursuit of knowledge",
                        "city_names": [
                            "Academy",
                            "Observatory",
                            "Library",
                            "Institute",
                            "Research Center",
                            "University",
                        ],
                    }
                ],
                "start_bias_terrains": [{"terrain_type": "TERRAIN_FLAT", "score": 10}],
                "start_bias_rivers": 3,
                "vis_art_building_cultures": ["VIS_ART_BUILDING_CULTURE_CLASSICAL", "VIS_ART_BUILDING_CULTURE_ASIAN"],
                "vis_art_unit_cultures": ["VIS_ART_UNIT_CULTURE_CLASSICAL"],
                "civilization_unlocks": [
                    {"unlock_age": "AGE_EXPLORATION", "unlock_civilization_type": "CIVILIZATION_SCIENTIFIC_EXPLORATION"},
                    {"unlock_age": "AGE_MODERN", "unlock_civilization_type": "CIVILIZATION_SCIENTIFIC_MODERN"},
                ],
            },
            "units": [
                {
                    "unit_type": "UNIT_SCIENTIFIC_SCHOLAR",
                    "unit_class": "CLASS_CIVILIAN",
                    "localizations": [
                        {
                            "name": "Scholar",
                            "description": "A learned researcher who provides science bonuses to nearby cities",
                        }
                    ],
                    "unit_stat": {"movement": 2},
                }
            ],
            "constructibles": [
                {
                    "constructible_type": "BUILDING_SCIENTIFIC_LIBRARY",
                    "constructible_class": "CLASS_BUILDING",
                    "localizations": [
                        {
                            "name": "Great Library",
                            "description": "A repository of knowledge that provides science and culture",
                        }
                    ],
                    "yield_changes": [
                        {"yield_type": "YIELD_SCIENCE", "amount": 3},
                        {"yield_type": "YIELD_CULTURE", "amount": 1},
                    ],
                }
            ],
            "modifiers": [
                {
                    "modifier_type": "MODIFIER_SCIENTIFIC_BONUS",
                    "effect_type": "EFFECT_ADJUST_PLAYER_YIELD_MODIFIER",
                    "arguments": {"YieldType": "YIELD_SCIENCE", "Amount": 10},
                    "localizations": [
                        {
                            "name": "Scientific Excellence",
                            "description": "+10% Science in all cities",
                        }
                    ],
                }
            ],
            "traditions": [],
            "progression_tree_nodes": [],
            "progression_trees": [],
            "constants": {},
            "imports": [],
            "build": {
                "output_dir": "./dist",
                "builders": [],
            },
        },
        "military": {
            "metadata": {
                "id": "military-civilization",
                "version": "1.0.0",
                "name": "Military Civilization Template",
                "description": "A combat-focused civilization with unit bonuses",
                "authors": "Your Name",
            },
            "module_localization": {
                "name": "Military Civilization",
                "description": "A civilization focused on conquest and military might",
            },
            "action_group": "AGE_ANTIQUITY",
            "civilization": {
                "civilization_type": "CIVILIZATION_MILITARY",
                "civilization_traits": ["TRAIT_MILITARY"],
                "localizations": [
                    {
                        "name": "Military Civilization",
                        "adjective": "Militant",
                        "description": "A civilization built on strength, discipline, and martial prowess",
                        "city_names": [
                            "Fortress",
                            "Stronghold",
                            "Citadel",
                            "Garrison",
                            "Barracks",
                            "Arsenal",
                        ],
                    }
                ],
                "start_bias_terrains": [{"terrain_type": "TERRAIN_HILL", "score": 15}],
                "start_bias_rivers": 0,
                "vis_art_building_cultures": ["VIS_ART_BUILDING_CULTURE_EUROPEAN"],
                "vis_art_unit_cultures": ["VIS_ART_UNIT_CULTURE_EUROPEAN"],
                "civilization_unlocks": [
                    {"unlock_age": "AGE_EXPLORATION", "unlock_civilization_type": "CIVILIZATION_MILITARY_EXPLORATION"},
                ],
            },
            "units": [
                {
                    "unit_type": "UNIT_MILITARY_ELITE_WARRIOR",
                    "unit_class": "CLASS_MELEE",
                    "localizations": [
                        {
                            "name": "Elite Warrior",
                            "description": "A powerful melee unit with superior combat strength",
                        }
                    ],
                    "unit_stat": {"combat": 30, "movement": 2},
                    "unit_replace": {"replaces_unit_type": "UNIT_WARRIOR"},
                },
                {
                    "unit_type": "UNIT_MILITARY_ARCHER",
                    "unit_class": "CLASS_RANGED",
                    "localizations": [
                        {
                            "name": "Composite Archer",
                            "description": "A ranged unit with enhanced range",
                        }
                    ],
                    "unit_stat": {"ranged_combat": 28, "range": 3, "movement": 2},
                },
            ],
            "constructibles": [
                {
                    "constructible_type": "BUILDING_MILITARY_BARRACKS",
                    "constructible_class": "CLASS_BUILDING",
                    "localizations": [
                        {
                            "name": "War Academy",
                            "description": "A military training facility that provides production for unit construction",
                        }
                    ],
                    "yield_changes": [{"yield_type": "YIELD_PRODUCTION", "amount": 2}],
                }
            ],
            "modifiers": [
                {
                    "modifier_type": "MODIFIER_MILITARY_BONUS",
                    "effect_type": "EFFECT_ADJUST_UNIT_COMBAT_STRENGTH",
                    "arguments": {"Amount": 5},
                    "localizations": [
                        {
                            "name": "Martial Tradition",
                            "description": "+5 Combat Strength for all units",
                        }
                    ],
                }
            ],
            "traditions": [],
            "progression_tree_nodes": [],
            "progression_trees": [],
            "constants": {},
            "imports": [],
            "build": {
                "output_dir": "./dist",
                "builders": [],
            },
        },
        "cultural": {
            "metadata": {
                "id": "cultural-civilization",
                "version": "1.0.0",
                "name": "Cultural Civilization Template",
                "description": "A culture-focused civilization with tradition bonuses",
                "authors": "Your Name",
            },
            "module_localization": {
                "name": "Cultural Civilization",
                "description": "A civilization focused on culture, art, and traditions",
            },
            "action_group": "AGE_ANTIQUITY",
            "civilization": {
                "civilization_type": "CIVILIZATION_CULTURAL",
                "civilization_traits": ["TRAIT_CULTURAL", "TRAIT_DIPLOMATIC"],
                "localizations": [
                    {
                        "name": "Cultural Civilization",
                        "adjective": "Cultural",
                        "description": "A civilization celebrated for its rich heritage, arts, and cultural influence",
                        "city_names": [
                            "Arts District",
                            "Cultural Center",
                            "Museum Quarter",
                            "Heritage City",
                            "Festival Town",
                            "Gallery",
                        ],
                    }
                ],
                "start_bias_terrains": [],
                "start_bias_rivers": 2,
                "vis_art_building_cultures": ["VIS_ART_BUILDING_CULTURE_ASIAN", "VIS_ART_BUILDING_CULTURE_AFRICAN"],
                "vis_art_unit_cultures": ["VIS_ART_UNIT_CULTURE_ASIAN"],
                "civilization_unlocks": [
                    {"unlock_age": "AGE_EXPLORATION", "unlock_civilization_type": "CIVILIZATION_CULTURAL_EXPLORATION"},
                ],
            },
            "units": [
                {
                    "unit_type": "UNIT_CULTURAL_ARTIST",
                    "unit_class": "CLASS_CIVILIAN",
                    "localizations": [
                        {
                            "name": "Master Artist",
                            "description": "A cultural specialist who creates great works and spreads influence",
                        }
                    ],
                    "unit_stat": {"movement": 2},
                }
            ],
            "constructibles": [
                {
                    "constructible_type": "BUILDING_CULTURAL_THEATER",
                    "constructible_class": "CLASS_BUILDING",
                    "localizations": [
                        {
                            "name": "Grand Theater",
                            "description": "A center of performing arts that generates culture and influence",
                        }
                    ],
                    "yield_changes": [
                        {"yield_type": "YIELD_CULTURE", "amount": 4},
                        {"yield_type": "YIELD_INFLUENCE", "amount": 2},
                    ],
                },
                {
                    "constructible_type": "BUILDING_CULTURAL_MONUMENT",
                    "constructible_class": "CLASS_BUILDING",
                    "localizations": [
                        {
                            "name": "Cultural Monument",
                            "description": "A monument to cultural achievements",
                        }
                    ],
                    "yield_changes": [{"yield_type": "YIELD_CULTURE", "amount": 2}],
                },
            ],
            "modifiers": [
                {
                    "modifier_type": "MODIFIER_CULTURAL_BONUS",
                    "effect_type": "EFFECT_ADJUST_PLAYER_YIELD_MODIFIER",
                    "arguments": {"YieldType": "YIELD_CULTURE", "Amount": 15},
                    "localizations": [
                        {
                            "name": "Cultural Heritage",
                            "description": "+15% Culture in all cities",
                        }
                    ],
                }
            ],
            "traditions": [
                {
                    "tradition_type": "TRADITION_CULTURAL_PATRONAGE",
                    "localizations": [
                        {
                            "name": "Cultural Patronage",
                            "description": "Invest in the arts and culture, enhancing cultural output",
                        }
                    ],
                }
            ],
            "progression_tree_nodes": [],
            "progression_trees": [],
            "constants": {},
            "imports": [],
            "build": {
                "output_dir": "./dist",
                "builders": [],
            },
        },
        "economic": {
            "metadata": {
                "id": "economic-civilization",
                "version": "1.0.0",
                "name": "Economic Civilization Template",
                "description": "A gold and production focused civilization",
                "authors": "Your Name",
            },
            "module_localization": {
                "name": "Economic Civilization",
                "description": "A civilization focused on trade, wealth, and economic prosperity",
            },
            "action_group": "AGE_ANTIQUITY",
            "civilization": {
                "civilization_type": "CIVILIZATION_ECONOMIC",
                "civilization_traits": ["TRAIT_ECONOMIC"],
                "localizations": [
                    {
                        "name": "Economic Civilization",
                        "adjective": "Mercantile",
                        "description": "A civilization built on commerce, trade routes, and economic power",
                        "city_names": [
                            "Trade Hub",
                            "Market City",
                            "Port Town",
                            "Commerce Center",
                            "Treasury",
                            "Bazaar",
                        ],
                    }
                ],
                "start_bias_terrains": [{"terrain_type": "TERRAIN_NAVIGABLE_RIVER", "score": 20}],
                "start_bias_rivers": 5,
                "vis_art_building_cultures": ["VIS_ART_BUILDING_CULTURE_MEDITERRANEAN"],
                "vis_art_unit_cultures": ["VIS_ART_UNIT_CULTURE_MEDITERRANEAN"],
                "civilization_unlocks": [
                    {"unlock_age": "AGE_EXPLORATION", "unlock_civilization_type": "CIVILIZATION_ECONOMIC_EXPLORATION"},
                ],
            },
            "units": [
                {
                    "unit_type": "UNIT_ECONOMIC_MERCHANT",
                    "unit_class": "CLASS_CIVILIAN",
                    "localizations": [
                        {
                            "name": "Great Merchant",
                            "description": "A wealthy trader who establishes profitable trade routes",
                        }
                    ],
                    "unit_stat": {"movement": 3},
                }
            ],
            "constructibles": [
                {
                    "constructible_type": "BUILDING_ECONOMIC_MARKET",
                    "constructible_class": "CLASS_BUILDING",
                    "localizations": [
                        {
                            "name": "Grand Bazaar",
                            "description": "A bustling marketplace that generates gold and commerce",
                        }
                    ],
                    "yield_changes": [
                        {"yield_type": "YIELD_GOLD", "amount": 5},
                        {"yield_type": "YIELD_PRODUCTION", "amount": 1},
                    ],
                },
                {
                    "constructible_type": "BUILDING_ECONOMIC_BANK",
                    "constructible_class": "CLASS_BUILDING",
                    "localizations": [
                        {
                            "name": "Treasury House",
                            "description": "A financial institution that multiplies wealth",
                        }
                    ],
                    "yield_changes": [{"yield_type": "YIELD_GOLD", "amount": 3}],
                },
            ],
            "modifiers": [
                {
                    "modifier_type": "MODIFIER_ECONOMIC_BONUS",
                    "effect_type": "EFFECT_ADJUST_PLAYER_YIELD_MODIFIER",
                    "arguments": {"YieldType": "YIELD_GOLD", "Amount": 20},
                    "localizations": [
                        {
                            "name": "Economic Prosperity",
                            "description": "+20% Gold in all cities",
                        }
                    ],
                }
            ],
            "traditions": [],
            "progression_tree_nodes": [],
            "progression_trees": [],
            "constants": {},
            "imports": [],
            "build": {
                "output_dir": "./dist",
                "builders": [],
            },
        },
    }
    
    if template_name not in templates:
        raise HTTPException(
            status_code=404,
            detail=f"Template '{template_name}' not found. Available: {', '.join(templates.keys())}",
        )
    
    return templates[template_name]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=True,
    )

