from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, CheckButtons, Button
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from .PEC3D_functions import rect_slit_func, hex_slit_func, hex_obstacle_func, rect_obstacle_func, circ_slit_func, \
    circ_obstacle_func, free_PEC_func
from .commons import cmap_spectral, wavelength_to_colormap, pause, wait

DEBUG = True


class Dropdown:
    def __init__(self, ax, options, update_func):
        self.options = options
        self.update_func = update_func
        self.current_option = options[0]

        # Create a button to toggle the dropdown
        self.button = Button(ax, self.current_option)
        self.button.on_clicked(self.toggle_dropdown)

        # Create a list of buttons for options
        self.option_axes = []
        self.option_buttons = []
        self.visible = False

        for i, option in enumerate(options):
            ax_option = plt.axes([0.3, 0.7 - i * 0.05, 0.4, 0.04])
            option_button = Button(ax_option, option)
            option_button.on_clicked(self.make_selection(option))
            self.option_axes.append(ax_option)
            self.option_buttons.append(option_button)
            ax_option.set_visible(False)  # Initially hide option buttons

    def toggle_dropdown(self, event):
        self.visible = not self.visible
        for ax in self.option_axes:
            ax.set_visible(self.visible)
        plt.draw()

    def make_selection(self, option):
        def select(event):
            self.current_option = option
            self.button.label.set_text(self.current_option)
            self.update_func(self.current_option)
            self.toggle_dropdown(event)  # Hide options after selection

        return select


class DisplayFields3D:
    N_cycles = 500

    # accumulation_type:
    # 0: the absolute value of the Poynting vector
    # 1: the x-component of the Poynting vector
    # 2: the y-component of the Poynting vector
    # 3: the z-component of the Poynting vector
    accumulation_type = 0

    def __init__(self, fields3D,
                 displayed_wavelengths=(1., 5., 10.),
                 displayed_slit_widths=(1., 5., 10.),
                 user_PEC_func=None,  # lambda hx, hy, hz, x0, y0, z0: None
                 slit_position_init=0,
                 slit_screen_thickness=0,
                 show_Poynting: bool = False, show_PML: bool = False):
        self.fields3D = fields3D
        self.show_Poynting = show_Poynting
        self.show_PML = show_PML
        if user_PEC_func is not None:
            self.user_PEC_func = user_PEC_func
        else:
            self.user_PEC_func = rect_slit_func
        self.slit_position_init = slit_position_init
        self.slit_screen_thickness = slit_screen_thickness

        wavelength_min, wavelength_init, wavelength_max = displayed_wavelengths
        # Normalize the wavelength to be between 0 and 1 for colormap
        self.norm = mcolors.Normalize(vmin=wavelength_min, vmax=wavelength_max)

        slit_width_min, slit_width_init, slit_width_max = displayed_slit_widths

        # create a matplotlib window to display the 2D field distribution, the output field intensity,
        # and two sliders (for wavelength and for slit width)
        self.fig, (self.ax1, self.ax2, self.ax3, self.ax4) = plt.subplots(4, 1, figsize=(5, 7))

        # display fields
        x = self.fields3D.get_x(self.show_PML)
        y = self.fields3D.get_y(self.show_PML)
        z = self.fields3D.get_z(self.show_PML)

        # Initial calculations
        self.slitwidth_y = self.slitwidth_z = slit_width_init
        self.fields3D.set_PEC(
            self.user_PEC_func(self.slit_screen_thickness, self.slitwidth_y, self.slitwidth_z, self.slit_position_init, 0, 0))
        self.start_update()

        if self.show_Poynting:
            cm = wavelength_to_colormap(wavelength_init, self.norm)

            out_field = self.fields3D.get_accumulate_S(show_PML=self.show_PML)
            self.im1 = self.ax1.imshow(
                out_field[:, :, out_field.shape[2] // 2],
                extent=(y.min(), y.max(), x.max(), x.min()),
                cmap=cm,
                origin='upper',
            )
            self.im2 = self.ax2.imshow(
                out_field[:, out_field.shape[1] // 2, :],
                extent=(z.min(), z.max(), x.max(), x.min()),
                cmap=cm,
                origin='upper',
            )
            self.im3 = self.ax3.imshow(
                out_field[self.fields3D.out_pos, :, :],
                extent=(z.min(), z.max(), y.max(), y.min()),
                cmap=cm,
                origin='upper',
            )
            self.set_3D_lims(out_field)

            out_field = self.fields3D.get_Ez(show_PML=self.show_PML)
            self.im4, = self.ax4.plot(x, out_field[:, self.fields3D.Ny // 2, self.fields3D.Nz // 2])
        else:
            out_field = self.fields3D.get_Ez(self.show_PML)
            self.im1 = self.ax1.imshow(
                out_field[:, :, out_field.shape[2] // 2],
                extent=(y.min(), y.max(), x.max(), x.min()),
                cmap='RdBu',
                origin='upper',
                vmin=-2, vmax=2
            )
            self.im2 = self.ax2.imshow(
                out_field[:, out_field.shape[1] // 2, :],
                extent=(z.min(), z.max(), x.max(), x.min()),
                cmap='RdBu',
                origin='upper',
                vmin=-2, vmax=2
            )
            out_field = self.fields3D.get_out_intensity(self.show_PML)
            self.im3 = self.ax3.imshow(
                out_field,
                extent=(z.min(), z.max(), y.max(), y.min()),
                cmap='RdBu',
                origin='upper',
                vmin=0, vmax=2
            )
            self.im4, = self.ax4.plot(x, out_field[:, self.fields3D.Ny // 2, self.fields3D.Nz // 2])

        # Add a title and labels
        # self.ax1.set_xlabel('y-axis')
        self.ax1.set_xticks([])  # Remove x-axis ticks
        self.ax1.set_xlabel('')  # Remove x-axis label
        self.ax1.set_ylabel('x-axis')
        self.ax2.set_yticks([])  # Remove y-axis ticks
        self.ax2.set_ylabel('')  # Remove y-axis label
        self.ax2.set_xlabel('z-axis')
        self.ax3.set_xlabel('y-axis')
        self.ax3.set_ylabel('z-axis')
        self.ax4.set_xlabel('x-axis')
        self.ax4.set_ylabel('Ez')
        self.ax4.set_ylim([-2, 2])

        # slices position
        zy_ratio = (z.max() - z.min()) / (y.max() - y.min())
        self.ax1.set_position([-0.02, 0.55, 0.7, 0.4])  # [left, bottom, width, height]
        out = self.ax1.get_position()
        wy = out.x1 - out.x0
        wz = wy * zy_ratio
        self.ax2.set_position([out.x1 + 0.05, out.y0, wz, out.y1 - out.y0])
        self.ax3.set_position([out.x0, out.y0 + 0.02 - wz, wy, wz])
        self.ax4.set_position([out.x1 + 0.12, out.y0 - 0.75*wz, 0.9*wy, 0.5*wz])

        # Create a slider axis and slider widget
        slider_ax1 = plt.axes([0.2, 0.1, 0.6, 0.05], facecolor='lightgoldenrodyellow')
        self.wavelength_slider = Slider(slider_ax1, 'wavelength', wavelength_min, wavelength_max, valinit=wavelength_init)
        # Create an array representing the colormap gradient
        gradient = np.linspace(wavelength_min, wavelength_max, cmap_spectral.N).reshape(1, -1)  # 1D gradient
        slider_ax1.imshow(gradient, aspect='auto', cmap=cmap_spectral, extent=[wavelength_min, wavelength_max, 0, 1])
        self.wavelength_slider.poly.set_facecolor(cmap_spectral(self.norm(wavelength_init)))
        # Connect the slider to the update function
        self.wavelength_slider.on_changed(self.slider_update_wavelength)

        slider_ax2 = plt.axes([0.25, 0.05, 0.55, 0.05], facecolor='red')
        self.slitwidth_slider = Slider(slider_ax2, 'slit width', slit_width_min, slit_width_max, valinit=slit_width_init)
        # Connect the slider to the update function
        self.slitwidth_slider.on_changed(self.slider_update_slit_width)

        slider_ax3 = plt.axes([0.25, 0.0, 0.55, 0.05], facecolor='blue')
        self.slitheight_slider = Slider(slider_ax3, 'slit height', slit_width_min, slit_width_max, valinit=slit_width_init)
        # Connect the slider to the update function
        self.slitheight_slider.on_changed(self.slider_update_slit_height)

        # Create a CheckButtons widget
        poynting_ax = plt.axes([0.02, 0.16, 0.47, 0.04])  # Position for the checkbox
        self.poynting_check = CheckButtons(poynting_ax, ['display energy flow'], [self.show_Poynting])
        # Connect the CheckButtons widget with the toggle function
        self.poynting_check.on_clicked(self.toggle_poynting)

        # Create a dropbox widget for slits/obstacles
        dropdown = Dropdown(plt.axes([0.51, 0.16, 0.47, 0.04]),
                            ['Rectangle slit',
                             'Hexagonal slit',
                             'Circular slit',
                             'Rectangle obstacle',
                             'Hexagonal obstacle',
                             'Circular obstacle',
                             'Free space'],
                            self.plot_function)

        # Animation setup
        self.ani = FuncAnimation(self.fig, self.update, frames=100, interval=5)

    def plot_function(self, selected_option):
        self.slitwidth_slider.ax.set_visible(True)
        self.slitheight_slider.ax.set_visible(False)
        if selected_option == 'Free space':
            self.user_PEC_func = free_PEC_func
            self.slitwidth_slider.ax.set_visible(False)

        elif selected_option == 'Rectangle slit':
            self.user_PEC_func = rect_slit_func
            self.slitheight_slider.ax.set_visible(True)
            self.slitwidth_slider.label.set_text("slit width")
            self.slitheight_slider.label.set_text("slit height")

        elif selected_option == 'Hexagonal slit':
            self.user_PEC_func = hex_slit_func
            self.slitwidth_slider.label.set_text("slit radius")

        elif selected_option == 'Circular slit':
            self.user_PEC_func = circ_slit_func
            self.slitwidth_slider.label.set_text("slit radius")

        elif selected_option == 'Rectangle obstacle':
            self.user_PEC_func = rect_obstacle_func
            self.slitheight_slider.ax.set_visible(True)
            self.slitwidth_slider.label.set_text("obstacle width")
            self.slitheight_slider.label.set_text("obstacle height")

        elif selected_option == 'Hexagonal obstacle':
            self.user_PEC_func = hex_obstacle_func
            self.slitwidth_slider.label.set_text("obstacle radius")

        elif selected_option == 'Circular obstacle':
            self.user_PEC_func = circ_obstacle_func
            self.slitwidth_slider.label.set_text("obstacle radius")

        self.update_PEC()

    def show(self):
        """
        display matplotlib plot
        """
        plt.show()
        # plt.pause(0)

    def set_3D_lims(self, out_field):
        # Autoscale to update color limits
        # self.im1.autoscale()
        # self.im2.autoscale()
        # self.im3.autoscale()
        field_min = out_field.min()
        field_max = out_field.max()
        print(f"S min = {field_min}, S max = {field_max}")
        if field_min > -1e-3:
            self.im1.set_clim((0, 1.1 * field_max))
            self.im2.set_clim((0, 1.1 * field_max))
            self.im3.set_clim((0, 1.1 * field_max))
        else:
            S = max(abs(field_min), abs(field_max))
            self.im1.set_clim((-S, S))
            self.im2.set_clim((-S, S))
            self.im3.set_clim((-S, S))

    def update_ax1_2(self):
        """
        update axes 1, 2 and 3 if show_Poynting
        """
        if self.show_Poynting:
            out_field = self.fields3D.get_accumulate_S(self.show_PML)
            if out_field is not None:
                self.im1.set_data(out_field[:, :, out_field.shape[2] // 2])
                self.im2.set_data(out_field[:, out_field.shape[1] // 2, :])
                self.im3.set_data(out_field[self.fields3D.out_pos, :, :])
                self.set_3D_lims(out_field)
        else:
            out_field = self.fields3D.get_Ez(self.show_PML)
            self.im1.set_data(out_field[:, :, out_field.shape[2] // 2])
            self.im2.set_data(out_field[:, out_field.shape[1] // 2, :])

    def update_ax3(self):
        """
        update ax3
        """
        if not self.show_Poynting:
            out_field = self.fields3D.get_out_intensity(self.show_PML)
            self.im3.set_data(out_field)

    def update_ax4(self):
        """
        update ax3
        """
        out_field = self.fields3D.get_Ez(show_PML=self.show_PML)[:,
                    self.fields3D.Ny // 2 + 0 * (self.fields3D.pml_width + 2),
                    self.fields3D.Nz // 2 + 0 * (self.fields3D.pml_width + 2)]
        self.im4.set_ydata(out_field)
        # self.ax4.relim()  # Recalculate limits based on new data
        # self.ax4.autoscale_view()  # Rescale the view

    def update(self, n):
        """
        Time-stepping loop
        """
        self.fields3D.update()
        if self.show_Poynting:
            if self.fields3D.n_step % self.fields3D.Nt == 0:
                # check calculation saturation
                if self.fields3D.dS < 10:
                    self.ani.event_source.stop()  # Pause the animation
                else:
                    self.update_ax1_2()
            self.update_ax4()
        else:
            self.update_ax1_2()
            if self.fields3D.n_step % self.fields3D.Nt == 0:
                self.update_ax3()
            self.update_ax4()

    @wait
    def start_update(self):
        if DEBUG:
            print("start_update")

        if self.show_Poynting:
            # Update the fields until saturation
            self.fields3D.set_accumulate_S(accumulation_type=self.accumulation_type)
            self.fields3D.start_until(None)
            self.fields3D.do_n(self.fields3D.Nt+1)
        else:
            self.fields3D.set_accumulate_S(accumulation_type=-1)
            self.fields3D.start_until(self.N_cycles)

    @pause
    def slider_update_wavelength(self, val):
        """
        Update wavelength slider
        """
        if self.show_Poynting:
            # Update the colormap
            new_cmap = wavelength_to_colormap(val, self.norm)
            self.im1.set_cmap(new_cmap)
            self.im2.set_cmap(new_cmap)
            self.im3.set_cmap(new_cmap)

        # Get the color from the colormap
        color = cmap_spectral(self.norm(val))
        self.wavelength_slider.poly.set_facecolor(color)

        # Update the wavelength
        self.fields3D.set_wavelength(wavelength=val)
        # Update the fields
        self.start_update()
        self.update_ax1_2()

    def update_PEC(self):
        self.fields3D.set_PEC(
            self.user_PEC_func(self.slit_screen_thickness, self.slitwidth_y, self.slitwidth_z, self.slit_position_init,
                               0, 0))
        # Update the fields
        self.start_update()
        self.update_ax1_2()

    @pause
    def slider_update_slit_width(self, val):
        # change slit
        self.slitwidth_y = val
        self.update_PEC()

    @pause
    def slider_update_slit_height(self, val):
        # change slit
        self.slitwidth_z = val
        self.update_PEC()
        
    @pause
    def toggle_poynting(self, label):
        """
        Define the function to toggle the visibility of the plot lines
        """
        status = self.poynting_check.get_status()  # Get the status of the checkboxes
        if status[0]:
            self.show_Poynting = True
            self.fields3D.set_accumulate_S(accumulation_type=self.accumulation_type)
            self.fields3D.do_n(self.fields3D.Nt+1)
            new_cmap = wavelength_to_colormap(self.fields3D.wavelength, self.norm)
            # Update the colormap
            self.im1.set_cmap(new_cmap)
            self.im2.set_cmap(new_cmap)
            self.im3.set_cmap(new_cmap)
            # self.im1.set_clim(0, 1)
            # self.im2.set_clim(0, 1)
            # self.im3.set_clim(0, 1)
            self.update_ax1_2()
        else:
            self.show_Poynting = False
            self.fields3D.set_accumulate_S(accumulation_type=-1)
            self.im1.set_clim(-2, 2)
            self.im2.set_clim(-2, 2)
            self.im3.set_clim(0, 2)
            self.im1.set_cmap('RdBu')  # Update the colormap
            self.im2.set_cmap('RdBu')  # Update the colormap
            self.im3.set_cmap('RdBu')  # Update the colormap
