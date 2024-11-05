# Angstrom vs Atomic Units

This uses the benzene example as a baseline.
Use outputs `OutputFormat = cube + xcrysden + dx + axis_x + plane_z + netcdf +
vtk`
Change between `Angstrom` and `Bohr` units with `UnitsOutput =
eV_Angstrom`/`UnitsOutput = atomic`.

Comparisons were conducted with `density` output. Using `density` also has an impact
on the field values, as they are refered to the unit of length (because unit is
"something by volume"/"something/volume").

# Notes
ase.units:
- ase.units.Bohr = 0.5291772105638411
- ase.units.Angstrom = 1.0

ase.units.Bohr is the conversion factor to convert Angstrom to Bohr.
(Bohr => Angstrom) would be factor 1,88973. Angstrom to Bohr =>
`1A * 1,88973 = 1A / ase.units.Bohr = 1b`

CUBE (http://paulbourke.net/dataformats/cube/)
- If the sign of the number of voxels in a dimension is positive then the units are
  Bohr, if negative then Angstroms.

XCRYSDEN (http://www.xcrysden.org/doc/XSF.html)
- all coordinates are in ANGSTROMS units
- all forces are in Hartree/ANGSTROM units

# Results with `UnitsOutput = atomic`
These values were retrieved from the output files. One would expect to find all
values in the output in atomic units.

## CUBE
Number of voxels positive => Bohr
Values indicate Bohr

| Output  | Values                               | Therefore must be unit |
|:--------|:-------------------------------------|:-----------------------|
| ORIGIN  | `-13.322569  -13.889487   -9.354144` | Bohr                   |
| SPACING | `0.283459, 0.283459, 0.283459`       | Bohr                   |


## VTK
| Output  | Values                              | Therefore must be unit |
|:--------|:------------------------------------|:-----------------------|
| ORIGIN  | `-13.322569, -13.889487, -9.354144` | Bohr                   |
| SPACING | `0.283459, 0.283459, 0.283459`      | Bohr                   |

## NetCDF
| Output  | Values                         | Therefore must be unit |
|:--------|:-------------------------------|:-----------------------|
| ORIGIN  | `-9.35414, -13.8895, -13.3226` | Bohr                   |
| SPACING | `0.283459, 0.283459, 0.283459` | Bohr                   |

## XCrySDen
| Output  | Values                              | Therefore must be unit                                                                                                             |
|:--------|:------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------|
| ORIGIN  | `26.645138, 27.778974, 18.708289`   | This cube is not centered around 0, 0, 0. If we center the cube, result is (-13.322569, -13.889487, -9.3541445) and therefore Bohr |

## Plane_z
| Output  | Values                                           | Therefore must be unit |
|:--------|:-------------------------------------------------|:-----------------------|
| ORIGIN  | `-1.33225692368438E+001, -3.96842487905985E+000` | Bohr                   |



# Results with `UnitsOutput = eV_Angstrom`
These values were retrieved from the output files. One would expect to find all
values in the output in atomic units.

## CUBE
| Output  | Values                              | Therefore must be unit |
|:--------|:------------------------------------|:-----------------------|
| ORIGIN  | `-13.322569, -13.889487, -9.354144` | Bohr                   |
| SPACING | `0.283459, 0.283459, 0.283459`      | Bohr                   |


## VTK
| Output  | Values                            | Therefore must be unit |
|:--------|:----------------------------------|:-----------------------|
| ORIGIN  | `-7.050000, -7.350000, -4.950000` | Angstrom               |
| SPACING | `0.150000, 0.150000, 0.150000`    | Angstrom               |

## NetCDF
| Output  | Values                | Therefore must be unit |
|:--------|:----------------------|:-----------------------|
| ORIGIN  | `-4.95, -7.35, -7.05` | Angstrom               |
| SPACING | `0.15, 0.15, 0.15`    | Angstrom               |

## XCrySDen
| Output  | Values                           | Therefore must be unit                                                                                                  |
|:--------|:---------------------------------|:------------------------------------------------------------------------------------------------------------------------|
| ORIGIN  | `14.100000, 14.700000, 9.900000` | This cube is not centered around 0, 0, 0. If we center the cube, result is (-7.05, -7.35, -4.95) and therefore Angstrom |

## Plane_z
| Output  | Values                                           | Therefore must be unit |
|:--------|:-------------------------------------------------|:-----------------------|
| ORIGIN  | `-7.05000000000000E+000, -2.10000000000000E+000` | Angstrom               |
