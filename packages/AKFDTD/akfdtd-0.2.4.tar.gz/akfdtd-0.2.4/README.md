# AK FDTD

version=0.2.2

author Alexander V. Korovin [a.v.korovin73@gmail.com], [Homepage](http://avkor.epizy.com)

## Overview

**AK FDTD** is a Python package designed for simple finite difference time domain (FDTD) simulation in open space. It allows you to test slit diffraction.

**2D case**

![slit diffraction](https://github.com/Darkhyp/FDTD_python/raw/main/images/slit_diffraction2d.PNG)

**3D case**

![slit diffraction](https://github.com/Darkhyp/FDTD_python/raw/main/images/slit_diffraction3d.PNG)

An example of light diffraction on a slit located in the center of the computational domain. Light falls on a screen with a slit from above (the speed of light is taken as unity). The intensity graph is a time-averaged square of the field.


## Features

- **PML**: implementation of perfectly matched boundary layers.

## Installation

You can install **AKFDTD** using `pip`. To install the latest version from PyPI, use:

```bash
pip install AKFDTD
```

## Work with object in 2D case

- **EM2D(Lx, Ly, Nx, Ny, wavelength)**: initialization of the simulator object, where **Lx** is the x dimension of the simulation domain, **Ly** is the y dimension of the simulation domain, **Nx** is the number of sampling points along the x axis, **Ny** is the number of sampling points along the y axis, **wavelength** is the wavelength of the incoming plane wave.

- **.set_slit(condition_func)**(optional): method to set slit(s) by condition function, **condition_func** is the function of two arguments (f(x,y)) to set zeros in the electric field (PEC).

- **.start_until(N_cycles)**(optional): method for performing **N_cycles** simulation cycles necessary to avoid observing the wave start from above.

- **.update()**: method of updating fields over time (one simulation cycle).

- **.get_x(show_PML)**: method to get x coordinates with or without PML region (default is **show_PML**=False).

- **.get_y(show_PML)**: method to get y coordinates with or without PML region (default is **show_PML**=False).

- **.get_Ez(show_PML)**: method for obtaining the z-component of the electric field with or without the PML region (default is **show_PML**=False).

## Test in 2D

```python
from FDTD.fdtd2D import EM2D
from FDTD.display_fields2D import DisplayFields2D


if __name__ == "__main__":
    # display PML region
    show_PML = False
    # show_PML = True

    # display absolute value of the Poynting vector
    show_Poynting = True
    # show_Poynting = False

    # display of the field distribution along the center of the calculation area
    show_xy = False
    # show_xy = True

    # incoming plane wave wavelength
    wavelength_init = 3
    wavelength_min = 1
    wavelength_max = 5

    # simulation domain
    Lx = 30
    Ly = 20
    Nx = 200
    Ny = 151

    # slit width
    slit_width_init = 3
    slit_width_min = 1
    slit_width_max = 10
    slit_position_init = -Lx/2 + 8
    slit_screen_thickness = 0.5

    # create FDTD domain and initialize fields3D
    fields = EM2D(Lx=Lx, Ly=Ly, Nx=Nx, Ny=Ny, wavelength=wavelength_init)

    # Initial condition
    N_cycles = 500
    N_cycles = 1

    display_fields = DisplayFields2D(
        fields,
        displayed_wavelengths=(wavelength_min, wavelength_init, wavelength_max),
        displayed_slit_widths=(slit_width_min, slit_width_init, slit_width_max),
        slit_position_init=slit_position_init,
        slit_screen_thickness=slit_screen_thickness,
        show_Poynting=show_Poynting, show_PML=show_PML, show_xy=show_xy)
    display_fields.N_cycles = N_cycles
    display_fields.show()
```

## Test in 3D

```python
from FDTD.fdtd3D import EM3D
from FDTD.display_fields import DisplayFields3D


if __name__ == "__main__":
    # display PML region
    show_PML = False
    # show_PML = True

    # display absolute value of the Poynting vector
    show_Poynting = True
    # show_Poynting = False

    # incoming plane wave wavelength
    wavelength_init = 3.
    wavelength_min = 1.
    wavelength_max = 5.

    # simulation domain
    Lx = 30
    Ly = 20
    Lz = 20
    Nx = 200
    Ny = 151
    Nz = 152

    # slit width
    slit_width_init = 3
    slit_width_min = 1
    slit_width_max = 10
    slit_position_init = -Lx/2 + 8
    slit_screen_thickness = 0.5

    # create FDTD domain and initialize fields3D
    fields = EM3D(Lx=Lx, Ly=Ly, Lz=Lz, Nx=Nx, Ny=Ny, Nz=Nz, wavelength=wavelength_init)

    # Initial condition
    N_cycles = 500
    # N_cycles = 1

    DisplayFields3D.N_cycles = N_cycles
    display_fields = DisplayFields3D(
        fields,
        displayed_wavelengths=(wavelength_min, wavelength_init, wavelength_max),
        displayed_slit_widths=(slit_width_min, slit_width_init, slit_width_max),
        slit_position_init=slit_position_init,
        slit_screen_thickness=slit_screen_thickness,
        show_Poynting=show_Poynting, show_PML=show_PML)
    display_fields.show()

```
