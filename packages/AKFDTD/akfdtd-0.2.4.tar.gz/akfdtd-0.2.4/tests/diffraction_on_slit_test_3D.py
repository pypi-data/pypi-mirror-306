# pip install AKFDTD
from FDTD.fdtd3D import EM3D
from FDTD.display_fields3D import DisplayFields3D


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
    # Nx = 300
    # Ny = 201
    # Nz = 202
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
