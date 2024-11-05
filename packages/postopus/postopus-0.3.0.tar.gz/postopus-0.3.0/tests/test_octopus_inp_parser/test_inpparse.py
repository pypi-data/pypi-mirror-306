from pathlib import Path

from postopus.octopus_inp_parser.inpparse import Parser


def test_input_parsing_multiple_systems(celestial_bodies_run: Path):
    # Comparison data for testing
    check_keys = [
        "CalculationMode",
        "ExperimentalFeatures",
        "FromScratch",
        "stdout",
        "stderr",
        "Dimensions",
        "Systems",
        "SolarSystem.Systems",
        "Interactions",
        "Earth.ParticleMass",
        "Earth.ParticleInitialPosition",
        "Earth.ParticleInitialVelocity",
        "Moon.ParticleMass",
        "Moon.ParticleInitialPosition",
        "Moon.ParticleInitialVelocity",
        "Sun.ParticleMass",
        "Sun.ParticleInitialPosition",
        "Sun.ParticleInitialVelocity",
        "TDSystemPropagator",
        "sampling",
        "days",
        "seconds_per_day",
        "TDTimeStep",
        "TDPropagationTime",
    ]
    check_systems = [
        "SolarSystem",
        "SolarSystem.Sun",
        "SolarSystem.Earth",
        "SolarSystem.Moon",
        "default",
    ]
    particlemass_sun = "1.98855e30"

    inp = Parser(celestial_bodies_run / "inp")
    assert list(inp.fields_raw) == check_keys
    assert list(inp.systems) == check_systems
    # test multisystem parsing
    assert inp.systems["default"]["Sun.ParticleMass"] == particlemass_sun


def test_input_parsing_default_system(methane_run: Path):
    inp = Parser(methane_run / "inp")
    assert inp.systems["default"]["_systemtype"] == "electronic"
