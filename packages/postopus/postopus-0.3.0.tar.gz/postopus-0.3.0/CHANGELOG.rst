=========
Changelog
=========

Version 0.3.0
=============

Release date: *upcoming*

* The user interface was reworked. To access the data of any output, the call operator must be used now.
  For example ``run.default.scf.convergence`` becomes ``run.default.scf.convergence()``,
  ``run.default.scf.density.get_all("z=0")`` becomes ``run.default.scf.density("z=0")``.
  The methods ``get``, ``iget`` and ``get_converged`` do not exist anymore
  (use e.g. ``run.default.scf.density("z=0").isel(step=-1)`` instead of ``run.default.scf.density.get_converged("z=0")``).
* Field data (e.g. `density`) is now prodided as lazy loadable array. This means that no data is accessed when running
  ``data = run.default.scf.density("z=0")`` — only when ``data.values`` is used the files (and only the selected files) are
  accessed (note that other libraries might access the values too, e.g. ``data.plot()`` will call ``data.values`` internally).
* The outputs of the different wave function state was unified into one output. E.g. ``run.default.td.wf_st0001(source)``
  becomes ``run.default.td.wf(source).sel(st=1)``.
* Most of the internal components were refactored, see `MR 212 <https://gitlab.com/octopus-code/postopus/-/merge_requests/212>`__,
  `MR 204 <https://gitlab.com/octopus-code/postopus/-/merge_requests/204>`__
  and `MR 244 <https://gitlab.com/octopus-code/postopus/-/merge_requests/244>`__
  for details.
* ASE is installed properly when using ``pip install postopus``, executing
  ``pip install git+https://gitlab.com/ase/ase.git@master`` manually is not required anymore.

Version 0.2.0
=============

Release date: Aug 30, 2023

* Octopus test data is now created on the fly during each CI pipeline. The invoke task
  `generatePytestData` was created for this purpose.  Needed inp files are
  stored in the `tests/data` folder. We are no longer downloading the test data from the test
  data repo. All the inp files were changed to generate lighter test data and different values.
  All the tests were changed accordingly. This makes it easy to combine different octopus
  versions with different python versions. Supported in the pipelines now: py 3.8 - 3.10,
  octopus: 12.0 - 12.2. Almost all tutorials generate the data on the fly now.
* Now we are able to read vtk vector fields within static/ and output_iter/ correctly.
* Added nestedRun objects. This is documented and tested.
* Added `Application Examples` chapter to documentation.

Version 0.1.0
=============

Release date: Feb 6, 2023

* First alpha version of postopus.
* Supports reading of "cube", "xsf", "vtk", "x=0", "y=0", "z=0", "x=0,y=0", "x=0,z=0", "y=0,z=0", "ncdf", and "nc" field octopus output files.
* The field data is stored in the dictionary `run.systemname.calculationmode.fieldname` for `ScalarFields` and `run.systemname.calculationmode.fieldname(.dimension)` for `VectorFields`. It can be retrieved by using any of the `get()` methods. Depending on the situation, we can use: `get()`, `iget()`, `get_converged()`, or `get_all()`. These methods will return an `xarray` object, also with units support (as strings).
* Comprehensive tutorials on how to use the `xarray` objects for analyzing data and visualizing it, also in combination with other libraries like `holoviews` or `xrft`.
* Supports the reading of many table-like and unstructured files without extension stored in td.general and static folders. The data is stored in the dictionary `run.systemname.calculationmode.filename`. The return type will be either a `pandas.DataFrame` or a string depending on the file type. We do not need to use any of the `get()` methods for files without extensions.
