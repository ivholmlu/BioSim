"""
:mod:`randvis.graphics` provides graphics support for RandVis.

.. note::
   * This module requires the program ``ffmpeg`` or ``convert``
     available from `<https://ffmpeg.org>` and `<https://imagemagick.org>`.
   * You can also install ``ffmpeg`` using ``conda install ffmpeg``
   * You need to set the  :const:`_FFMPEG_BINARY` and :const:`_CONVERT_BINARY`
     constants below to the command required to invoke the programs
   * You need to set the :const:`_DEFAULT_FILEBASE` constant below to the
     directory and file-name start you want to use for the graphics output
     files.

"""

import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os

# Update these variables to point to your ffmpeg and convert binaries
# If you installed ffmpeg using conda or installed both softwares in
# standard ways on your computer, no changes should be required.
_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('../..', 'data')
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_IMG_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'   # alternatives: mp4, gif


class Graphics:
    """Provides graphics support for RandVis."""

    def __init__(self, img_dir=None, img_name=None, img_fmt=None, island_map=None,
                 heat_map1=None, heat_map2=None):
        """
        :param img_dir: directory for image files; no images if None
        :type img_dir: str
        :param img_name: beginning of name for image files
        :type img_name: str
        :param img_fmt: image file format suffix
        :type img_fmt: str
        """

        if img_name is None:
            img_name = _DEFAULT_GRAPHICS_NAME

        if img_dir is not None:
            self._img_base = os.path.join(img_dir, img_name)
        else:
            self._img_base = None

        self._img_fmt = img_fmt if img_fmt is not None else _DEFAULT_IMG_FORMAT

        self._img_ctr = 0
        self._img_step = 1

        # the following will be initialized by _setup_graphics
        self.island_map = island_map
        self._img_axis = None
        self._time_ax = None
        self._fig = None
        self._map_ax = None
        self._img_axis1 = None
        self._img_axis2 = None
        self._line_ax = None
        self._line1 = None
        self._line2 = None
        self._heat1_ax = None
        self._heat1_img = None
        self._heat1_map = heat_map1
        self._heat2_ax = None
        self._heat2_img = None
        self._heat2_map = heat_map2
        self._hist1_ax = None
        self._hist1_bins = None
        self._hist2_ax = None
        self._hist2_bins = None
        self._hist3_ax = None
        self._hist3_bins = None
        self.txt = None

    def set_bins(self, bins):
        pass

    def setup(self, final_step, img_step):
        """
        Prepare graphics.

        Call this before calling :meth:`update()` for the first time after
        the final time step has changed.

        :param final_step: last time step to be visualised (upper limit of x-axis)
        :param img_step: interval between saving image to file
        """

        self._img_step = img_step

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure()

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(3, 3, 1)
            rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                         'L': (0.0, 0.6, 0.0),  # dark green
                         'H': (0.5, 1.0, 0.5),  # light green
                         'D': (1.0, 1.0, 0.5)}  # light yellow

            map_rgb = [[rgb_value[column] for column in row]
                       for row in self.island_map.splitlines()]

            self._map_ax = self._fig.add_subplot(3, 3, 1)
            self._map_ax.imshow(map_rgb)
            self._map_ax.set_xticks(range(len(map_rgb[0])))
            self._map_ax.set_xticklabels(range(1, 1 + len(map_rgb[0])))
            self._map_ax.set_yticks(range(len(map_rgb)))
            self._map_ax.set_yticklabels(range(1, 1 + len(map_rgb)))
            self._map_ax.set_title('Map of Rossumoya')
            self._map_ax.axis('off')

            for ix, name in enumerate(('Water', 'Lowland',
                                       'Highland', 'Desert')):
                self._map_ax.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                                      edgecolor='none',
                                                      facecolor=rgb_value[name[0]]))

        if self._line_ax is None:
            self._line_ax = self._fig.add_subplot(3, 3, 3)
            self._line_ax.set_xlim(0, 300)
            self._line_ax.set_ylim(0, 10000)
            self._line_ax.set_title('Number of each species')

        if self._time_ax is None:
            self._time_ax = self._fig.add_axes([0.4, 0.8, 0.2, 0.2])
            self._time_ax.axis('off')
            template = 'Count: {:5d}'
            self.txt = self._time_ax.text(0.5, 0.5, template.format(0),
                           horizontalalignment='center',
                           verticalalignment='center',
                           transform=self._time_ax.transAxes)

        if self._heat1_ax is None:
            self._heat1_ax = self._fig.add_subplot(3, 3, 4)
            self._heat1_img = self._heat1_ax.imshow(self._heat1_map,
                                                    interpolation='nearest', vmin=0, vmax=200, cmap='plasma')
            plt.colorbar(self._heat1_img, ax=self._heat1_ax, orientation='vertical', cmap='plasma')

        if self._heat2_ax is None:
            self._heat2_ax = self._fig.add_subplot(3, 3, 6)
            self._heat2_img = self._heat2_ax.imshow(self._heat2_map,
                                                    interpolation='nearest', vmin=0, vmax=50, cmap='plasma')
            plt.colorbar(self._heat2_img, ax=self._heat2_ax, orientation='vertical', cmap='plasma')

        if self._hist1_ax is None:
            self._hist1_ax = self._fig.add_subplot(5, 3, 13)
            self._hist1_ax.set_title('Fitness')
            self._hist1_bins = np.linspace(0, 1, num=20)
            ax = plt.gca()
            ax.set_ylim((0, 2000))
            ax.set_yticks([1000, 2000])

        if self._hist2_ax is None:
            self._hist2_ax = self._fig.add_subplot(5, 3, 14)
            self._hist2_ax.set_title('Age')
            self._hist2_bins = np.linspace(0, 60, num=30)

        if self._hist3_ax is None:
            self._hist3_ax = self._fig.add_subplot(5, 3, 15)
            self._hist3_ax.set_title('Weight')
            self._hist3_bins = np.linspace(0, 60, num=20)

        # needs updating on subsequent calls to simulate()
        # add 1 so we can show values for time zero and time final_step
        self._line_ax.set_xlim(0, final_step + 1)
        self._line_ax.set_xlim(0, final_step + 1)

        if self._line1 is None and self._line2 is None:
            self._line1 = self._line_ax.plot(np.arange(final_step),
                                             np.full(final_step, np.nan), 'b-')[0]
            self._line2 = self._line_ax.plot(np.arange(final_step),
                                             np.full(final_step, np.nan), 'r-')[0]

    def _update_system_map(self, herbivores_arr, carnivores_arr):
        """Update the 2D-view of the system.
            :param herbivores_arr: numpy array containing the amount of herbivores in each cell
            :param carnivores_arr: numpy array containing the amount of carnivores in each cell
        """
        if self._img_axis1 is not None and self._img_axis2 is not None:
            self._heat1_map = self._img_axis1.set_data(herbivores_arr)
            self._heat2_map = self._img_axis2.set_data(carnivores_arr)
        else:
            self._img_axis1 = self._heat1_ax.imshow(self._heat1_map, interpolation='nearest',
                                                    vmin=0, vmax=200, cmap='plasma')
            self._img_axis2 = self._heat2_ax.imshow(self._heat2_map, interpolation='nearest',
                                                    vmin=0, vmax=50, cmap='plasma')

    def _update_line_graph(self, year, total_herbivores, total_carnivores):
        ydata_line1 = self._line1.get_ydata()
        ydata_line2 = self._line2.get_ydata()
        ydata_line1[year] = total_herbivores
        ydata_line2[year] = total_carnivores
        self._line1.set_ydata(ydata_line1)
        self._line2.set_ydata(ydata_line2)

    def _update_histograms(self, herbi_fitness, carni_fitness, herbi_age, carni_age,
                           herbi_weight, carni_weight):
        self._hist1_ax.hist(herbi_fitness, self._hist1_bins, color='b', histtype='step')
        self._hist1_ax.hist(carni_fitness, self._hist1_bins, color='r', histtype='step')
        self._hist2_ax.hist(herbi_age, self._hist2_bins, color='b', histtype='step')
        self._hist2_ax.hist(carni_age, self._hist2_bins, color='r', histtype='step')
        self._hist3_ax.hist(herbi_weight, self._hist3_bins, color='r', histtype='step')
        self._hist3_ax.hist(carni_weight, self._hist3_bins, color='b', histtype='step')

    def _update_headers(self):
        self._hist1_ax.cla()
        self._hist2_ax.cla()
        self._hist3_ax.cla()
        self._hist1_ax.set_title('Fitness')
        self._hist2_ax.set_title('Age')
        self._hist3_ax.set_title('Weight')


    def update(self, step, herbivores_arr, carnivores_arr, n_herbivores, n_carnivores,
               herbi_fitness, carni_fitness, herbi_age, carni_age,herbi_weight, carni_weight):
        """
        Updates graphics with current data and save to file if necessary.

        :param step: current time step
        """
        self._update_headers()
        template = 'Count: {:5d}'
        self.txt.set_text(template.format(step))
        self._update_system_map(herbivores_arr, carnivores_arr)
        self._update_line_graph(step, n_herbivores, n_carnivores)
        self._update_histograms(herbi_fitness, carni_fitness, herbi_age, carni_age,
                                herbi_weight, carni_weight)

        self._fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(1e-6)  # pause required to pass control to GUI

        self._save_graphics(step)

    def _save_graphics(self, step):
        """Saves graphics to file if file name given."""

        if self._img_base is None or step % self._img_step != 0:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1


    def make_movie(self, movie_fmt=None):
        """
        Creates MPEG4 movie from visualization images saved.

        .. :note:
            Requires ffmpeg for MP4 and magick for GIF

        The movie is stored as img_base + movie_fmt
        """

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt is None:
            movie_fmt = _DEFAULT_MOVIE_FORMAT

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_MAGICK_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)
