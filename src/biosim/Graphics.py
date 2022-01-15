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

    def __init__(self, img_dir=None, img_name=None, img_fmt=None):
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
        self._fig = None
        self._map1_ax = None
        self._map2_ax = None
        self._img_axis = None
        self._img2_axis = None
        self._pop_ax = None
        self._pop_line1 = None
        self._pop_line2 = None
        # self._histogram1 = None
        # self._histogram2 = None
        # self._histogram3 = None

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
        # HEATMAP 1
        if self._map1_ax is None:
            self._map1_ax = self._fig.add_subplot(1, 2, 1)
            self._img_axis = None

        # Add right subplot for line graph of mean.
        # POPULASJONSPLOT
        if self._pop_ax is None:
            self._pop_ax = self._fig.add_subplot(1, 2, 2)
            self._pop_ax.set_ylim(0, 10**4)

        # needs updating on subsequent calls to simulate()
        # add 1 so we can show values for time zero and time final_step
        self._pop_ax.set_xlim(0, final_step + 1)

        if (self._pop_line1 and self._pop_line2) is None:
            line_plot1 = self._pop_ax.plot(np.arange(0, final_step + 1),
                                           np.full(final_step + 1, np.nan))
            self._pop_line1 = line_plot1[0]

            line_plot2 = self._pop_ax.plot(np.arange(0, final_step + 1),
                                           np.full(final_step + 1, np.nan))
            self._pop_line2 = line_plot2[0]

        else:
            x_data, y_data1 = self._pop_line1.get_data()
            _, y_data2 = self._pop_line2.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._pop_line1.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data1, y_new)))
                self._pop_line2.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data2, y_new)))

    def _update_line_graph(self, year, n_herbivores, n_carnivores):
        y_data1 = self._pop_line1.get_ydata()
        y_data2 = self._pop_line2.get_ydata()
        y_data1[year] = n_herbivores
        y_data2[year] = n_carnivores

        self._pop_line1.set_ydata(y_data1)
        self._pop_line2.set_ydata(y_data2)

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

