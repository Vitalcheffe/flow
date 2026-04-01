"""
Material Library

Common engineering materials with standard properties.
"""

from dataclasses import dataclass


@dataclass
class MaterialProperties:
    name: str
    category: str
    youngs_modulus: float  # Pa
    poissons_ratio: float
    density: float  # kg/m3
    yield_strength: float  # Pa
    thermal_conductivity: float  # W/(m*K)
    specific_heat: float  # J/(kg*K)
    thermal_expansion: float  # 1/K


# Material database
MATERIALS = {
    "steel_s235": MaterialProperties(
        name="Structural Steel S235",
        category="metals",
        youngs_modulus=210e9,
        poissons_ratio=0.3,
        density=7850,
        yield_strength=235e6,
        thermal_conductivity=50,
        specific_heat=460,
        thermal_expansion=12e-6,
    ),
    "steel_s355": MaterialProperties(
        name="Structural Steel S355",
        category="metals",
        youngs_modulus=210e9,
        poissons_ratio=0.3,
        density=7850,
        yield_strength=355e6,
        thermal_conductivity=50,
        specific_heat=460,
        thermal_expansion=12e-6,
    ),
    "aluminum_6061": MaterialProperties(
        name="Aluminum 6061-T6",
        category="metals",
        youngs_modulus=68.9e9,
        poissons_ratio=0.33,
        density=2700,
        yield_strength=276e6,
        thermal_conductivity=167,
        specific_heat=896,
        thermal_expansion=23.1e-6,
    ),
    "copper": MaterialProperties(
        name="Copper (C11000)",
        category="metals",
        youngs_modulus=117e9,
        poissons_ratio=0.34,
        density=8940,
        yield_strength=69e6,
        thermal_conductivity=391,
        specific_heat=385,
        thermal_expansion=16.5e-6,
    ),
    "titanium_ti6al4v": MaterialProperties(
        name="Titanium Ti-6Al-4V",
        category="metals",
        youngs_modulus=113.8e9,
        poissons_ratio=0.33,
        density=4430,
        yield_strength=880e6,
        thermal_conductivity=6.7,
        specific_heat=526,
        thermal_expansion=8.6e-6,
    ),
    "concrete_c30": MaterialProperties(
        name="Concrete C30/37",
        category="construction",
        youngs_modulus=33e9,
        poissons_ratio=0.2,
        density=2400,
        yield_strength=30e6,
        thermal_conductivity=1.4,
        specific_heat=880,
        thermal_expansion=10e-6,
    ),
    "glass": MaterialProperties(
        name="Float Glass",
        category="construction",
        youngs_modulus=70e9,
        poissons_ratio=0.22,
        density=2500,
        yield_strength=33e6,
        thermal_conductivity=1.0,
        specific_heat=840,
        thermal_expansion=9e-6,
    ),
    "abs_plastic": MaterialProperties(
        name="ABS Plastic",
        category="polymers",
        youngs_modulus=2.0e9,
        poissons_ratio=0.35,
        density=1040,
        yield_strength=40e6,
        thermal_conductivity=0.2,
        specific_heat=1400,
        thermal_expansion=80e-6,
    ),
}


def get_material(key: str) -> MaterialProperties | None:
    """Get material by key."""
    return MATERIALS.get(key)


def list_materials(category: str | None = None) -> list[MaterialProperties]:
    """List available materials, optionally filtered by category."""
    if category:
        return [m for m in MATERIALS.values() if m.category == category]
    return list(MATERIALS.values())


def get_categories() -> list[str]:
    """Get unique material categories."""
    return list(set(m.category for m in MATERIALS.values()))
