
import pytest
from elysia_engine.hypersphere import (
    CelestialHierarchy,
    TesseractCoord,
    HypersphereMemory,
    SoulProtocol,
    MemoryPattern
)
from elysia_engine.tensor import SoulTensor

def test_celestial_hierarchy():
    """Test that the 7 Angels/Demons mapping is correct."""
    # Test Angels (Positive)
    assert "Angel Rank 7" in CelestialHierarchy.analyze_frequency(7.0)
    assert "Angel Rank 1" in CelestialHierarchy.analyze_frequency(1.0)
    assert "High Frequency" in CelestialHierarchy.analyze_frequency(5.0)

    # Test Demons (Negative)
    assert "Demon Rank 7" in CelestialHierarchy.analyze_frequency(-7.0)
    assert "Demon Rank 1" in CelestialHierarchy.analyze_frequency(-1.0)
    assert "Low Frequency" in CelestialHierarchy.analyze_frequency(-5.0)

    # Test Neutral
    assert "Human/Void" in CelestialHierarchy.analyze_frequency(0.0)

def test_tesseract_coord_conversion():
    """Test that Tesseract coordinates convert to Quaternions correctly."""
    coord = TesseractCoord(w=1.0, x=0.5, y=7.0, z=-1.0)
    quat = coord.to_quaternion()

    assert quat.w == 1.0
    assert quat.x == 0.5
    assert quat.y == 7.0
    assert quat.z == -1.0

def test_soul_protocol():
    """Test the Tesseract-Soul Protocol helper functions."""
    # Boundary Check
    assert SoulProtocol.boundary_check(5.0) == 5.0
    assert SoulProtocol.boundary_check(-1.0) == 0.0 # Clamping

    # Frequency Scan
    assert SoulProtocol.frequency_scan(1.0) == 7.0 # +1.0 sentiment -> +7 Angel
    assert SoulProtocol.frequency_scan(-1.0) == -7.0 # -1.0 sentiment -> -7 Demon

    # Trajectory
    z, x = SoulProtocol.map_trajectory(1.0, 0.5)
    assert z == 1.0
    assert x == 0.5

def test_hypersphere_fractal_storage():
    """Test storing a Hypersphere inside another Hypersphere (Fractal)."""
    # Create the Inner Universe (Microcosm)
    inner_memory = HypersphereMemory()
    inner_soul = SoulTensor(amplitude=1.0, frequency=7.0, phase=0.0)
    inner_coord = TesseractCoord(w=0, x=0, y=7, z=0)
    inner_memory.store("Angel Core", inner_coord, inner_soul)

    # Create the Outer Universe (Macrocosm)
    outer_memory = HypersphereMemory()
    outer_soul = SoulTensor(amplitude=10.0, frequency=0.0, phase=0.0)
    outer_coord = TesseractCoord(w=10, x=0, y=0, z=0)

    # Store the Inner Universe into the Outer
    pattern = outer_memory.store(
        content=inner_memory,
        coord=outer_coord,
        soul_tensor=outer_soul,
        topology="Fractal",
        name="Inner Heaven"
    )

    # Retrieve and verify
    retrieved = outer_memory.query(outer_coord, radius=0.1)[0]
    assert isinstance(retrieved.content, HypersphereMemory)
    assert retrieved.content.patterns[0][1].content == "Angel Core"
    assert "Fractal" in retrieved.summary
