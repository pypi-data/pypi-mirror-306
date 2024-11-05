from collections import defaultdict
from pathlib import Path

from postopus.octopus_run import Run


class nestedObjects(defaultdict):
    """Handle nested objects created from a directory tree

    The objects can be accessed with nested dictionaries where the keys are
    given by the directory names at the corresponding level.

    Moreover, there is a convenience access with . notation.

    Example for accessing data:
      Folder structure:
      ./
        run1/
          gs/
          td/
        run2/
          gs/
          td/
      >>> n = nestedObjects.from_cwd(Run)
      >>> run1_gs = n["run1"]["gs"]
      >>> run2_td = n.run2.td
    """

    # this enables convenience access with . notation
    __getattr__ = defaultdict.get

    def __dir__(self):
        """Enable tab completion"""
        return super().__dir__() + list(self.keys())

    def __init__(self, path=None, initialize=None):
        """Initialize object for given path and initialization function

        path is expected to be a Path object. All paths below this
        that contain an "exec" folder will be taken into account.

        The initialize function should take a Path object and return
        and object that is then stored at the leaf level of the tree.
        """
        super().__init__()
        self.default_factory = nestedObjects
        if path is not None:
            path_list = [d.parent for d in path.glob("**/exec")]
            self._initialize_data(path_list, initialize)

    @classmethod
    def from_pathlist(cls, path_list, initialize):
        """Create the object from a list of paths"""
        self = cls()
        self._initialize_data(path_list, initialize)
        return self

    @classmethod
    def from_cwd(cls, initialize):
        """Create the object from the current working directory"""
        return cls(Path("."), initialize)

    def _initialize_data(self, path_list, initialize):
        """Internal routine for initializing the data"""
        for path in path_list:
            self.set_nested(path.parts, initialize(path))

    def get_nested(self, key_list):
        """Get object for a list of keys from the nested dict structure"""
        result = self
        for key in key_list:
            result = result[key]
        return result

    def set_nested(self, key_list, value):
        """Set object for a list of keys from the nested dict structure"""
        self.get_nested(key_list[:-1])[key_list[-1]] = value

    def get_path(self, path):
        """Get object for a given path"""
        return self.get_nested(path.parts)

    def flat_list(self):
        """Return flat list of objects"""
        results = []
        for k, v in self.items():
            if isinstance(v, nestedObjects):
                results += v.flat_list()
            else:
                results.append(v)
        return results

    def flat_dict(self):
        """Return flat dictionary of path -> object"""
        return self._flat_dict_implementation()

    def _flat_dict_implementation(self, path=None):
        """Internal implementation for the flat dictionary"""
        results = {}
        for k, v in self.items():
            # for the first level of recursion we need to create a path
            # from the key
            if path is None:
                new_path = Path(k)
            else:
                # for the other levels, we append to the path
                new_path = path / k
            if isinstance(v, nestedObjects):
                results.update(v._flat_dict_implementation(new_path))
            else:
                results[new_path] = v
        return results

    def apply(self, function):
        """Apply the function to all elements in the tree"""
        result = nestedObjects()
        for path, v in self.flat_dict().items():
            result.set_nested(path.parts, function(v))
        return result


class nestedRuns(nestedObjects):
    """Class for handling postopus Run objects in a nested folder hierarchy

    Example for aggregating convergence results:
        Folder structure:
        bla/
          spacing_0.1/
          spacing_0.2/
          spacing_0.4/
        >>> import pandas as pd
        >>> n = nestedRuns()
        >>> convergence = n.apply(lambda x: x.default.scf.convergence)
        >>> df = pd.concat(convergence)
        >>> converged = df.groupby(level=0).tail(1).droplevel(1)

        Now converged is a pandas dataframe with only the last line of each
        convergence table for each spacing folder. With some additional pandas
        magic, one obtains a dataframe with the spacing as a float in the
        index:
        >>> idx = converged.index.map(lambda x: float(x[-4:]))
        >>> spacing = converged.set_index(idx).sort_index()

        Now one can plot the total energy:
        >>> import matplotlib.pyplot as plt
        >>> plt.plot(spacing.index, spacing.energy)
    """

    def __init__(self, path=Path(".")):
        super().__init__(path, Run)
