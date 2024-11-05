# TODO: Cannot move this block in a `if TYPE_CHECKING` guard. Need to figure out what's
#  going on there
#  https://gitlab.com/octopus-code/postopus/-/merge_requests/213#note_1661879451
from pathlib import Path

import pandas as pd

from postopus.files.file import File


class XYZFile(File):
    EXTENSIONS = [".xyz"]

    def __init__(self, filepath: Path):
        """
        Enable Postopus to read XYZ data, as written by Octopus.
        https://openbabel.org/wiki/XYZ_%28format%29
        To write XYZ output, 'inp' files must set 'OutputFormat' to 'xyz'.

        Parameters
        ----------
        filepath : Path
            path to the file in XYZ format
        """
        self.filepath = filepath

    def _readfile(self):
        """
        Read numpy by default
        """
        raise NotImplementedError

    def numpy(self):
        try:
            self._numpydata
        except AttributeError:
            # self._numpydata = numpy.loadtxt(self.filepath, skiprows=2,
            # dtype={"names": ("Atom", "X", "Y", "Z"),
            # "formats": ("S2", "f4", "f4", "f4")})
            self._numpydata = self.pandas().to_numpy()
        return self._numpydata

    def pandas(self):
        try:
            self._pandasdata
        except AttributeError:
            if isinstance(self.filepath, list):
                # In this case the input is a list containing the lines from
                # the 'Coordinates' block in the 'inp' file
                from io import StringIO

                cleaned = []
                for line in strfromconf:
                    cleaned.append(
                        line.replace(" ", "").replace('"', "").replace("'", "")
                    )
                self.filepath = StringIO("\n".join(cleaned))
                self._pandasdata = pd.read_table(
                    self.filepath, delimiter="|", names=("Atom", "X", "Y", "Z")
                )
            else:
                self._pandasdata = pd.read_table(
                    self.filepath,
                    skiprows=2,
                    names=("Atom", "X", "Y", "Z"),
                    delim_whitespace=True,
                )
        return self._pandasdata


"""
    TESTING STUFF
    TESTING STUFF
"""
if __name__ == "__main__":
    # TODO: Make this use an example from inside the repo
    xyz = XYZFile("/home/bremerda/git/postopus-tmp-dev/benzene/benzene.xyz")
    print(xyz.pandas())
    print(xyz.numpy())

    strfromconf = [
        '"C" |           0 |          0 |           0',
        '"H" |  CH/sqrt(3) | CH/sqrt(3) |  CH/sqrt(3)',
        '"H" | -CH/sqrt(3) |-CH/sqrt(3) |  CH/sqrt(3)',
        '"H" |  CH/sqrt(3) |-CH/sqrt(3) | -CH/sqrt(3)',
        '"H" | -CH/sqrt(3) | CH/sqrt(3) | -CH/sqrt(3)',
    ]
    xyz2 = XYZFile(strfromconf)
    print(xyz2.pandas())
