from __future__ import annotations

from typing import TYPE_CHECKING

from postopus.datacontainers.util.convenience_dict import ConvenienceDict

from .output_proxy import OutputProxy

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from postopus.output_collector import CalcModeFiles, OutputField

    from .system import System


class CalculationModes(ConvenienceDict):
    """
    Class that build a dict of all outputs present in a system for a given
    CalculationMode output.

    Parameters
    ----------
    mode
        Name of the calculation mode in the output. Naming like in Octopus'
        output (e. g. 'td', 'scf', ...)
    outputs_in_mode
        outputs contained in the given calculation mode for this system
    systemdir
        directory in the filesystem which contains the output (folder 'output_iter')
        for one of the simulated systems in a run with Octopus
    systemname
        Name of the system, as found in OutputCollector.
    """

    # Set name of dict in ConvenienceDict
    __dict_name__ = "outputs"

    def __init__(
        self,
        mode: str,
        outputs_in_mode: CalcModeFiles,
        parent: System,
        systemdir: Path,
        systemname: str,
    ) -> None:
        # Init system dict in super
        super().__init__()

        self.parent = parent
        self.mode = mode
        self.systemdir = systemdir

        self.outputs = {}

        # Some field information are used for other fields. Preload those.
        outputs_to_preload = ["convergence"]
        for output in outputs_to_preload:
            if output in outputs_in_mode:
                self._load(output, outputs_in_mode[output])

        for output_name, output_field in outputs_in_mode.items():
            self._load(output_name, output_field)

    def __repr__(self) -> str:
        return "\n".join(self._repr_gen())

    def _repr_gen(self) -> Iterator[str]:
        yield f"{self.__class__.__name__}({self.mode!r}):"

        if self.mode == "scf":
            step_count = self.convergence().index[-1]
            yield f"Ground state calculation (finished after {step_count} steps)"
        elif self.mode == "td":
            energy = self.outputs.get("energy")
            if energy is not None:
                E = energy()
                step_count = E.index[-1]
                time = E.t[step_count]
                yield f"Time dependent simulation ({step_count} steps, total time: {time})"

        yield f"Found {len(self.outputs)} outputs:"
        for field in sorted(self.outputs.keys()):
            yield f"    {field}"

    def _load(self, output_name: str, output: OutputField) -> None:
        # skip if field was already preloaded
        if output_name in self.outputs:
            return

        output = OutputProxy(self, output)
        self.outputs[output_name] = output
