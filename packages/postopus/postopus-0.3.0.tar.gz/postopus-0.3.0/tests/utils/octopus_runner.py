from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from string import Template

import pytest

_filename = Path(__file__).name


class OctopusRunner:
    def __init__(self, cmd: str):
        """
        Initialize the octopus runner.

        Parameters
        ----------
        cmd
            Command line string to invoke octopus,
            e.g. `OctopusRunner(cmd="octopus")` if octopus
            is directly available as binary.
        """
        self._cmd = cmd
        self._version = None

    def run(
        self,
        inputfiles: list[Path] | Path,
        run_path: Path,
        additional_files: list[Path] | Path | None = None,
        parameters: dict[str, str] | None = None,
    ) -> Path:
        """Run octopus for the given input files in the given path.

        Octopus is only invoked, if the given input files are newer
        than the last run.

        Parameters
        ----------
        inputfiles:
            List of input files that should be used to run octopus.
            The path to the files should be given as absolut path.
        run_path:
            Path to the directory where octopus should be run.
        additional_files:
            Optional list of additional files that should be placed
            in the run directory other than the input file (e.g. benzene.xyz).
        parameters:
            Optional dict which can be used to replace content in the input
            file.

        Warnings
        --------
        Removing an input file wont be detected.
        """
        # Allow passing single path as input file
        if isinstance(inputfiles, Path):
            inputfiles = [inputfiles]
        if isinstance(additional_files, Path):
            additional_files = [additional_files]
        # Handle default parameter
        if additional_files is None:
            additional_files = list()
        if parameters is None:
            parameters = dict()

        # Check if there is already an up-to-date run of octopus.
        if not self._is_rerun_required(inputfiles, run_path):
            return run_path

        # Purge existing data and recreate folder
        if run_path.exists():
            shutil.rmtree(run_path)
        run_path.mkdir()
        # Place gitignore file to avoid commiting the data
        (run_path / ".gitignore").write_text(f"# created by {_filename}\n*")

        # Provide additional files
        # (only works at top level of the octopus run directory)
        for f in additional_files:
            shutil.copy(f, run_path)

        # Run octopus for the different input files
        for inputfile in inputfiles:
            self._do_run(inputfile, run_path, parameters)

        return run_path

    def run_simple(
        self,
        basedir: Path,
        input_files: list[str] | str,
        additional_files: list[str] | str | None = None,
    ) -> Path:
        """Perform the run in {basedir}/run
        using input files {basedir}/{input_files[i]}.

        In comparison to `run` the input files should be given
        as relative path of `basedir`, not as absolut path.
        >>> basedir = Path("path/to/folder")
        >>> octopus_runner.run_simple(basedir, input_files=["inp_gs", "inp_td"])

        Instead of
        >>> basedir = Path("path/to/folder")
        >>> octopus_runner.run(
        ...     inputfiles=[basedir / "inp_gs", basedir / "inp_td"],
        ...     run_path=basedir / "run",
        ... )

        Parameters
        ----------
        basedir
            Path with the input files.
            As runpath `basedir / "run"` will be used.
        input_files
            List of the input files that are used to run octopus.
            The input files must be provided inside the directory
            given by `basedir`.
        additional_files
            Optional list of additional files that should be placed
            in the run directory other than the input file (e.g. benzene.xyz).
            These files must be provided inside the directory
            given by `basedir`.
        """
        # Allow passing simple string
        if isinstance(input_files, str):
            input_files = [input_files]
        if isinstance(additional_files, str):
            additional_files = [additional_files]
        # Handle default parameter
        if additional_files is None:
            additional_files = list()

        run_path = basedir / "run"
        input_files_fullpath = [basedir / inp_file for inp_file in input_files]
        additional_files_fullpath = [basedir / f for f in additional_files]
        return self.run(
            input_files_fullpath, run_path, additional_files=additional_files_fullpath
        )

    @property
    def octopus_version(self) -> tuple[int]:
        return self._get_available_octopus_version()

    def _do_run(
        self, inputfile: Path, run_path: Path, parameters: dict[str, str]
    ) -> None:
        """Run octopus for the given input file."""
        inp = run_path / "inp"
        self._prepare_input_file(inputfile, inp, parameters)
        # leave all input files with the original name in the directory
        # for debug purposes.
        if inp != run_path / inputfile.name:
            shutil.copy(inp, run_path / inputfile.name)
        self._invoke(run_path)

    @staticmethod
    def _prepare_input_file(
        inputfile: Path, target: Path, parameters: dict[str, str]
    ) -> None:
        if not parameters:
            shutil.copy(inputfile, target)
            return

        template_raw = inputfile.read_text()
        template = Template(template_raw)
        file_content = template.substitute(**parameters)
        target.write_text(file_content)

    def _is_rerun_required(self, inputfiles: list[Path], run_path: Path) -> bool:
        oct_status_finished = self._get_oct_status_finished_file_path(run_path)
        if not oct_status_finished.exists():
            return True
        if self._get_available_octopus_version() != self._get_used_octopus_version(
            run_path
        ):
            return True
        newest_inputfile_timestamp = max(
            self._get_last_modified_timestamp(f) for f in inputfiles
        )
        last_run = self._get_last_modified_timestamp(oct_status_finished)
        return newest_inputfile_timestamp > last_run

    def _get_available_octopus_version(self) -> tuple[int]:
        if self._version is None:
            version_output = subprocess.check_output(
                "octopus -v", shell=True, encoding="iso-8859-1"
            ).split(" ")
            # The "encoding='iso-8859-1'" is necessary as binder cannot handle utf-8 standard properly.
            version_num = tuple(int(part) for part in version_output[1].split("."))
            self._version = version_num
        return self._version

    @staticmethod
    def _get_used_octopus_version(run_path: Path) -> tuple[int] | None:
        try:
            with open(run_path / "exec" / "parser.log") as parser_data:
                for line in parser_data:
                    if "Octopus version" in line:
                        return tuple(int(part) for part in line.split()[-1].split("."))

        except FileNotFoundError:
            print(
                "The used Octopus version could not be determined, as the parser.log file was not found."
            )
        return None

    @staticmethod
    def _get_last_modified_timestamp(file_: Path) -> float:
        return file_.stat().st_mtime

    @staticmethod
    def _get_oct_status_finished_file_path(run_path: Path) -> Path:
        return run_path / "exec" / "oct-status-finished"

    def _invoke(self, path: Path):
        p = subprocess.run(self._cmd, cwd=path)
        if p.returncode != 0:
            raise RuntimeError(f"Failed to run `{self._cmd}` in {path}")


@pytest.fixture(scope="session")
def octopus_runner() -> OctopusRunner:
    return OctopusRunner(cmd="octopus")
