from pathlib import Path

import pytest

from postopus.utils import parser_log_retrieve_value


@pytest.fixture
def parser_log_path1(tmpdir: Path) -> Path:
    """Create a parser.log example file on demand"""
    path = Path(tmpdir / "parser1.log")

    content = """# Octopus parser started
ExperimentalFeatures = 1
Debug = 8
DebugTrapSignals = 1		# default
Walltime = 0		# default
RestartWriteTime = 5		# default
ReportMemory = 0		# default
CalculationMode = 3
stdout = "-"		# default
stderr = "-"		# default
WorkDir = "."		# default
FlushMessages = 0		# default
ProfilingMode = 0		# default
UnitsOutput = 0		# default
UnitsXYZFiles = 1		# default
DisableAccel = 1		# default
FFTOptimize = 1		# default
FFTPreparePlan = 0		# default
FFTLibrary = 1		# default
NFFTGuruInterface = 0		# default
NFFTCutoff = 6		# default
NFFTOversampling = 2		# default
NFFTPrecompute = 16		# default
PNFFTCutoff = 6		# default
PNFFTOversampling = 2		# default
Opened block 'Systems'
Systems[0][0] = "Maxwell"
Systems[0][1] = 2
Dimensions = 3		# default
PeriodicDimensions = 0		# default
Maxwell.BoxShape = 4
Opened block 'Maxwell.Lsize'
Maxwell.Lsize[0][0] = 50
Maxwell.Lsize[0][1] = 50
Maxwell.Lsize[0][2] = 20
Closed block 'Maxwell.Lsize'
SymmetriesCompute = 1		# default
Opened block 'Maxwell.Spacing'
Maxwell.Spacing[0][0] = 0.25
Maxwell.Spacing[0][1] = 0.25
Maxwell.Spacing[0][2] = 0.25
Closed block 'Maxwell.Spacing'
CurvMethod = 1		# default
DerivativesStencil = 1		# default
DerivativesOrder = 4		# default
ParallelizationOfDerivatives = 2		# default
MeshIndexType = 1		# default
StatesPack = 1		# default
RiemannSilbersteinSign = 1		# default
Opened block 'MaxwellFieldsCoordinate'
MaxwellFieldsCoordinate[0][0] = 0
MaxwellFieldsCoordinate[0][1] = 0
MaxwellFieldsCoordinate[0][2] = -5
Closed block 'MaxwellFieldsCoordinate'
Systems[1][0] = "Medium"
Systems[1][1] = 6
LinearMediumBoxShape = 2
LinearMediumBoxFile = "small_thick_m4_offsetversion.off"
CheckPointsMediumFromFile = 1
Opened block 'LinearMediumProperties'
LinearMediumProperties[0][0] = 30
LinearMediumProperties[0][1] = 1
LinearMediumProperties[0][2] = 0
LinearMediumProperties[0][3] = 0
Closed block 'LinearMediumProperties'
LinearMediumEdgeProfile = 1		# default
Closed block 'Systems'
ReorderRanks = 0		# default
Maxwell.ParDomains = -1
Maxwell.ParStates = 0
ParKPoints = -1		# default
ParOther = 0		# default
ParallelizationNumberSlaves = 0		# default
MeshOrder = 3		# default
MeshPartitionVirtualSize = 32		# default
MeshPartitionPackage = 2		# default
MeshPartitionStencil = 1		# default
RestartWrite = 0
MeshUseTopology = 0		# default
MeshLocalOrder = 1		# default
PartitionPrint = 1		# default
OperateDouble = 1		# default
OperateComplex = 1		# default
OperateSingle = 0		# default
OperateComplexSingle = 0		# default
NLOperatorCompactBoundaries = 0		# default
Opened block 'MaxwellOutput'
MaxwellOutput[0][0] = 1
MaxwellOutputInterval = 10
OutputFormat = 36
MaxwellOutput[1][0] = 2
MaxwellOutputInterval = 10
OutputFormat = 36
MaxwellOutput[2][0] = 11
MaxwellOutputInterval = 10
OutputFormat = 36
MaxwellOutput[3][0] = 10
MaxwellOutputInterval = 10
OutputFormat = 36
Closed block 'MaxwellOutput'
MaxwellOutputIterDir = "output_iter"		# default
MaxwellRestartWriteInterval = 50		# default
MaxwellHamiltonianOperator = 2
ExternalCurrent = 0		# default
MaxwellMediumCalculation = 1		# default
StatesPack = 1		# default
TimeZero = 0		# default
Dimensions = 3		# default
PeriodicDimensions = 0		# default
FromScratch = 0		# default
TDPropagationTime = 0.842626
Maxwell.TDSystemPropagator = 4
Maxwell.TDTimeStep = 0.00105328
InteractionTiming = 1		# default
TDSystemPropagator = 0		# default
Medium.TDTimeStep = 0.000526641
InteractionTiming = 1		# default
TDMaxwellTDRelaxationSteps = 0		# default
TDMaxwellKSRelaxationSteps = 0		# default
MaxwellTDIntervalSteps = 1		# default
Opened block 'MaxwellBoundaryConditions'
MaxwellBoundaryConditions[0][0] = 4
MaxwellBoundaryConditions[0][1] = 4
MaxwellBoundaryConditions[0][2] = 4
Closed block 'MaxwellBoundaryConditions'
MaxwellTDETRSApprox = 0		# default
MaxwellTDOperatorMethod = 1		# default
MaxwellTDSCFThreshold = 1e-06		# default
MaxwellPlaneWavesInBox = 0		# default
TDExponentialMethod = 3		# default
TDExpOrder = 4		# default
Opened block 'MaxwellAbsorbingBoundaries'
MaxwellAbsorbingBoundaries[0][0] = 2
MaxwellAbsorbingBoundaries[0][1] = 2
MaxwellAbsorbingBoundaries[0][2] = 2
Closed block 'MaxwellAbsorbingBoundaries'
MaxwellABWidth = 3
MaxwellABPMLPower = 2
MaxwellABPMLReflectionError = 1e-16
MaxwellABWidth = 3
MaxwellABPMLPower = 2
MaxwellABPMLReflectionError = 1e-16
MaxwellABWidth = 3
MaxwellABPMLPower = 2
MaxwellABPMLReflectionError = 1e-16
Opened block 'MaxwellIncidentWaves'
MaxwellIncidentWaves[0][0] = 1
MaxwellIncidentWaves[0][1] = (1, 0)
MaxwellIncidentWaves[0][2] = (0, 1)
MaxwellIncidentWaves[0][3] = (0, 0)
MaxwellIncidentWaves[0][4] = "plane_waves_function"
Opened block 'MaxwellFunctions'
MaxwellFunctions[0][0] = "plane_waves_function"
MaxwellFunctions[0][1] = 10006
MaxwellFunctions[0][2] = 0
MaxwellFunctions[0][3] = 0
MaxwellFunctions[0][4] = 2.0944
MaxwellFunctions[0][5] = 0
MaxwellFunctions[0][6] = 0
MaxwellFunctions[0][7] = -30
MaxwellFunctions[0][8] = 10
Closed block 'MaxwellFunctions'
Closed block 'MaxwellIncidentWaves'
MaxwellTDOutput = 262153
# Octopus parser ended
"""

    with open(path, "tw") as f:
        f.write(content)

    return path


def test_retrieve_value_from_parser_log(parser_log_path1: Path):
    p = parser_log_path1

    assert parser_log_retrieve_value(p, "MaxwellTDOutput") == "262153"

    assert parser_log_retrieve_value(p, "CalculationMode") == "3"

    assert parser_log_retrieve_value(p, "CalculationMode", conversion=int) == 3

    assert (
        parser_log_retrieve_value(p, "Medium.TDTimeStep", conversion=float)
        == 0.000526641
    )

    # check for non-existing entries
    with pytest.raises(ValueError):
        _ = parser_log_retrieve_value(p, "ThisDoesNotExist")

    # reading of strings works as well, but note that quotes are returned as well
    assert (
        parser_log_retrieve_value(p, "LinearMediumBoxFile")
        == '"small_thick_m4_offsetversion.off"'
    )

    # can we deal with duplicate entries? (Meant to report first item found)
    assert parser_log_retrieve_value(p, "OutputFormat") == "36"

    # Matrix notation entries can be retrieved line by line
    assert parser_log_retrieve_value(p, "Maxwell.Lsize[0][0]") == "50"

    # Matrix notation entries cannot be retrieved as matrix:
    with pytest.raises(ValueError):
        _ = parser_log_retrieve_value(p, "Maxwell.Lsize")

    # Deal with '# default' comments:
    # The line in the input reads: "    SymmetriesCompute = 1		# default"

    assert (
        parser_log_retrieve_value(p, "SymmetriesCompute", ignore_comment=False)
        == "1		# default"
    )
    assert parser_log_retrieve_value(p, "SymmetriesCompute") == "1"

    # another example
    assert parser_log_retrieve_value(p, "stdout") == '"-"'
