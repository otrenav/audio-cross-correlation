# -*- coding: utf-8 -*-

"""
Analysis of audio data

August, 2016

Functionality
-------------
- Cross-correlation to identify time delay

Inputs
------
- audio_file_input_one : str
      Should point to a WAV file
- audio_file_input_two : str
      Should point to a WAV file

Outputs
-------
- correlation_graph : PNG
      A graph will be created everytime the `.graph()`
      method is called and it will be be stored with
      the name of the two filenames supplied concatenated
      and appending "_correlation.png" at the end

Results are stored in the `./results/` directory

Dependencies
------------
- scikits.audiolab depends on libsndfile:
      http://www.mega-nerd.com/libsndfile/#Download
      After downloading, go to the directory that contains
      the source code (where the `INSTALL` file is located),
      and execute this in order:
          1. $ ./configure
          2. $ ./make
          3. $ ./sudo make install

Execution
---------
It's assumed that the script is called from the terminal
with two arguments (the paths to the audio files):

$ python ./analysis.py /path/audio_file_one.wav /path/audio_file_two.wav

If the current directory structure is used:

$ python ./code/analysis.py \
         ./audio/audio_file_one.wav \
         ./audio/audio_file_two.wav

Notes
-----
- Third and following arguments are ignored
- Results are stored in the `./results/` directory
- If you get the:
  `IOError: [Errno 2] No such file or directory: './results/...`
  exception then you need to create the `results` directory
  where this script is stored.

Tests
-----

The code has been tested with:

- $ python ./code/analysis.py \
      ./results/test_original_downsampled_to_8192.wav \
      ./results/test_delayed_downsampled_to_8192.wav

- $ python ./code/analysis.py \
      ./results/test_clean_downsampled_to_8192.wav \
      ./results/test_with_white_noise_downsampled_to_8192.wav

- $ python ./code/analysis.py \
      ./results/test_white_noise_downsampled_to_8192.wav \
      ./results/test_white_noise_downsampled_to_8192.wav

Everything seems to be working correctly

Author
------
- Omar Trejo (otrenav@gmail.com)
"""

import os
import sys
import numpy
import scipy.signal
import scikits.audiolab
import matplotlib
import matplotlib.pyplot

matplotlib.use('agg')


class Analysis(object):

    def __init__(self, audio_one, audio_two):
        self.audio_input_file_one = audio_one
        self.audio_input_file_two = audio_two
        self._read_audio_data('one')
        self._read_audio_data('two')

    def correlation(self):
        self.correlation = scipy.signal.fftconvolve(
            self.audio_input_data_one,
            self.audio_input_data_two,
            mode='full'
        )

    def graph(self):
        spaces = self._get_linear_spaces()
        figure, (graph_one, graph_two) = matplotlib.pyplot.subplots(2, 1)
        graph_one.set_title('Signals')
        graph_one.set_xlabel('Seconds')
        graph_one.set_ylabel('Signal')
        graph_one.plot(
            spaces['one'], self.audio_input_data_one, 'blue',
            spaces['two'], self.audio_input_data_two, 'red'
        )
        graph_two.set_title('Correlation')
        graph_two.set_xlabel('Lag (seconds)')
        graph_two.set_ylabel('Power')
        graph_two.plot(
            spaces['three'], self.correlation, 'black'
        )
        figure.tight_layout()
        png_path = self._get_png_file_output()
        os.makedirs(os.path.dirname(png_path), exist_ok=True)
        figure.savefig(png_path)

    def print_data(self, which_data):
        """Print data

        Inputs
        ------
        - which_data : str
              Either 'one' or 'two' should be sent

        Any functions to print data should be put here
        """
        print('*' * 70)
        print('* Which data: {}'.format(which_data))
        print('*' * 70)
        self._print_format(which_data)
        self._print_encoding(which_data)
        self._print_sample_rate(which_data)
        self._print_number_of_channels(which_data)
        self._print_number_of_samples(which_data)
        print('*' * 70)

    def print_results(self):
        # Sample rate is the same for both audio files
        sample_rate = int(self.audio_input_sample_rate_one)
        mc = numpy.max(abs(self.correlation))
        amc = numpy.argmax(abs(self.correlation))
        amc = self._adjust_to_seconds(amc, sample_rate)
        print('*' * 70)
        print('* Results')
        print('*' * 70)
        print('Max absolute correlation: {}'.format(mc))
        print('Arg max absolute correlation (lag): {} seconds'.format(amc))
        print('*' * 70)

    def _adjust_to_seconds(self, arg_max_corr, sample_rate):
        #
        # TODO: Verify this formula
        # --------------------------
        # The objective is to adjust from samples to seconds
        # to know the lag between the two audio files.
        # I believe that if the two audio files are the same,
        # the correlation should be maxed at lag == 0. This
        # was tested with white noise.
        #
        arg_max_corr = (
            (arg_max_corr - len(self.correlation)/2) /
            float(sample_rate)
        )
        return(arg_max_corr)

    def _read_audio_data(self, which_data):
        audio_file = getattr(self, "audio_input_file_{}".format(which_data))
        try:
            sound_file = scikits.audiolab.Sndfile(audio_file, 'r')
        except Exception as e:
            raise ValueError(
                "Could not open {}.\n".format(audio_file) +
                "Full Python exception: {}.\n".format(e)
            )
        names = self._get_names(which_data)
        setattr(self, names['format'], sound_file.format)
        setattr(self, names['encoding'], sound_file.encoding)
        setattr(self, names['sample_rate'], sound_file.samplerate)
        setattr(self, names['samples'], sound_file.nframes)
        setattr(self, names['channels'], sound_file.channels)
        setattr(self, names['data'], sound_file.read_frames(
            getattr(self, names['samples'])
        ))

    def _get_linear_spaces(self):
        spaces = {}
        spaces['one'] = numpy.linspace(
            0,
            len(self.audio_input_data_one) /
            int(self.audio_input_sample_rate_one),
            num=len(self.audio_input_data_one)
        )
        spaces['two'] = numpy.linspace(
            0,
            len(self.audio_input_data_two) /
            int(self.audio_input_sample_rate_two),
            num=len(self.audio_input_data_two)
        )
        spaces['three'] = numpy.linspace(
            -len(self.correlation) /
            (2 * int(self.audio_input_sample_rate_one)),
            len(self.correlation) /
            (2 * int(self.audio_input_sample_rate_one)),
            num=len(self.correlation)
        )
        return(spaces)

    def _get_names(self, which_data):
        names = {}
        names['data'] = self._get_name('data', which_data)
        names['format'] = self._get_name('format', which_data)
        names['encoding'] = self._get_name('encoding', which_data)
        names['sample_rate'] = self._get_name('sample_rate', which_data)
        names['samples'] = self._get_name('number_of_samples', which_data)
        names['channels'] = self._get_name('number_of_channels', which_data)
        return(names)

    def _get_name(self, attribute, which_data):
        base = "audio_input"
        return("{}_{}_{}".format(base, attribute, which_data))

    def _print_sample_rate(self, which_data):
        print_this = getattr(
            self, self._get_name('sample_rate', which_data)
        )
        print("Sample rate: {}".format(print_this))

    def _print_format(self, which_data):
        print_this = getattr(
            self, self._get_name('format', which_data)
        )
        print("{}".format(print_this))

    def _print_encoding(self, which_data):
        print_this = getattr(
            self, self._get_name('encoding', which_data)
        )
        print("Encoding: {}".format(print_this))

    def _print_number_of_samples(self, which_data):
        print_this = getattr(
            self, self._get_name('number_of_samples', which_data)
        )
        print("Number of samples: {}".format(print_this))

    def _print_number_of_channels(self, which_data):
        print_this = getattr(
            self, self._get_name('number_of_channels', which_data)
        )
        print("Number of channels: {}".format(print_this))

    def _get_png_file_output(self):
        return("./results/" + self._get_file_name() + "_correlation.png")

    def _get_file_name(self):
        """Get file name

        WARNING: Assumes that input file name does not have dots
        int its file name. For example, `test_audio.wav` is fine,
        but `test.audio.wav` is not fine and will cause problems
        """
        file_name_one = self.audio_input_file_one.split("/")[-1].split(".")[0]
        file_name_two = self.audio_input_file_two.split("/")[-1].split(".")[0]
        file_name = file_name_one + "_vs_" + file_name_two
        return(file_name)


def main(argv):

    if len(argv) < 2:
        raise ValueError(
            "Needs `audio_file_input_one` and `audio_file_input_two` " +
            "arguments (see code instructions)"
        )

    audio_file_input_one = argv[0]
    audio_file_input_two = argv[1]

    analysis = Analysis(audio_file_input_one, audio_file_input_two)

    analysis.print_data('one')
    analysis.print_data('two')
    analysis.correlation()
    analysis.graph()
    analysis.print_results()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
