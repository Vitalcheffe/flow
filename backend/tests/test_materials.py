"""Tests for material library."""

import pytest

from app.solvers.materials import get_material, list_materials, get_categories, MATERIALS


class TestMaterials:
    def test_get_steel(self):
        steel = get_material("steel_s235")
        assert steel is not None
        assert steel.youngs_modulus == 210e9

    def test_get_nonexistent(self):
        assert get_material("nonexistent") is None

    def test_list_all(self):
        all_mats = list_materials()
        assert len(all_mats) == len(MATERIALS)

    def test_list_by_category(self):
        metals = list_materials("metals")
        assert len(metals) > 0
        assert all(m.category == "metals" for m in metals)

    def test_categories(self):
        cats = get_categories()
        assert "metals" in cats
        assert "construction" in cats

    def test_all_have_required_fields(self):
        for key, mat in MATERIALS.items():
            assert mat.youngs_modulus > 0, f"{key} missing E"
            assert 0 < mat.poissons_ratio < 0.5, f"{key} invalid nu"
            assert mat.density > 0, f"{key} missing density"
