# -*- coding: utf-8 -*-

"""
Downsampling of audio files

August, 2016

Functionality
-------------
- Downsample an audio file to a given rate
- Print the data with sample rate information
- Graph the signal for the current data
- Output the file into a WAV file

Inputs
------
- audio_file_path : str
      Accepted file formats are WAV
- new_sample_rate : int
      Should be a power of two

Outputs
-------
- new_audio_file : WAV
      Will have the same name as the original one with
      an appended `_downsampled` in its name
- graph : PNG
      Any graph produced will be saved with the name
      of the file name and an appended integer indicating
      the number of the graph to reproduce the process
      visually

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
with two arguments (the path to the audio file and the
desired sampling rate):

$ python ./downsampling.py /path/to/the/audio_file.wav 2048

If the current directory structure is used:

$ python ./code/downsampling.py ./audio/audio_file.wav 2048

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

- $ python ./code/downsampling.py ./audio/test_audio_original.wav 8192
- $ python ./code/downsampling.py ./audio/test_audio_delayed.wav 8192
- $ python ./code/downsampling.py ./audio/test_audio_clean.wav 8192
- $ python ./code/downsampling.py ./audio/test_audio_with_white_noise.wav 8192
- $ python ./code/downsampling.py ./audio/test_audio_white_noise.wav 8192

Everything seems to be working correctly

Author
------
- Omar Trejo (otrenav@gmail.com)
"""

import sys
import numpy
import scipy.signal
import scikits.audiolab
import matplotlib
import matplotlib.pyplot

matplotlib.use('agg')


class Downsample(object):

    def __init__(self, audio_input_file, new_sample_rate):
        self.new_sample_rate = new_sample_rate
        self.audio_input_file = audio_input_file
        self.audio_output_file = self._get_audio_output_file()
        self._set_output_metadata()
        self._read_audio_data()

    def print_data(self, which_data):
        """Print data

        Inputs
        ------
        - which_data : str
              Either 'input' or 'output' should be sent

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

    def downsample(self):
        self._check_valid_new_sample_rate()
        self._open_and_setup_output_file()
        self._perform_downsample()
        self._write_and_close_output_file()

    def graph_signal(self, which_data):
        # matplotlib.rcsetup.all_backends  # Available backends
        # matplotlib.pyplot.switch_backend('agg')  # Switch backend
        matplotlib.pyplot.figure()
        matplotlib.pyplot.ylabel('Signal')
        matplotlib.pyplot.xlabel('Seconds')
        matplotlib.pyplot.title('Signal graph for: ' + which_data)
        if which_data == 'input':
            time = numpy.linspace(
                0,
                len(self.audio_input_data) / int(self.audio_input_sample_rate),
                num=len(self.audio_input_data)
            )
            matplotlib.pyplot.plot(time, self.audio_input_data)
        elif which_data == 'output':
            time = numpy.linspace(
                0,
                len(self.audio_to_write) / int(self.new_sample_rate),
                num=len(self.audio_to_write)
            )
            matplotlib.pyplot.plot(time, self.audio_to_write)
        matplotlib.pyplot.savefig(self._get_png_file_output(which_data))

    def _perform_downsample(self):
        """Perform downsample

        To test, uncomment the commented line and comment the rest. This
        will avoid doing the dowsampling and will save the audio just as
        it was retrieved. Needs to be done in conjunction with the
        corresponding adjustment for `_open_and_setup_output_file()`.
        """
        # self.audio_to_write = self.audio_input_data
        number_of_samples = int(round(
            len(self.audio_input_data) *
            float(self.new_sample_rate) /
            float(self.audio_input_sample_rate)
        ))
        self.audio_to_write = scipy.signal.resample(
            self.audio_input_data,
            number_of_samples
        )

    def _open_and_setup_output_file(self):
        """Open and setup output file

        To test, uncomment the commented line and comment the line directly
        below it. This will avoid using the new sample rate and will leave
        the original sample rate when saved. Needs to be done in conjuction
        with the corresponding adjustment for `perform_downsample()`.
        """
        try:
            self.audio_output = scikits.audiolab.Sndfile(
                self.audio_output_file, 'w',
                self.audio_input_format,
                int(self.audio_input_number_of_channels),
                # int(self.audio_input_sample_rate)
                int(self.new_sample_rate)
            )
        except Exception as e:
            raise ValueError(
                "Could not prepare {}.\n".format(self.audio_output_file) +
                "Full Python exception: {}.\n".format(e)
            )

    def _write_and_close_output_file(self):
        self.audio_output.write_frames(self.audio_to_write)
        self._set_updated_output_metadata()
        self.audio_output.close()

    def _read_audio_data(self):
        try:
            sound_file = scikits.audiolab.Sndfile(self.audio_input_file, 'r')
        except Exception as e:
            raise ValueError(
                "Could not open {}.\n".format(self.audio_input_file) +
                "Full Python exception: {}.\n".format(e)
            )
        self.audio_input_format = sound_file.format
        self.audio_input_encoding = sound_file.encoding
        self.audio_input_sample_rate = sound_file.samplerate
        self.audio_input_number_of_samples = sound_file.nframes
        self.audio_input_number_of_channels = sound_file.channels
        self.audio_input_data = sound_file.read_frames(
            self.audio_input_number_of_samples
        )

    def _check_valid_new_sample_rate(self):
        if int(self.new_sample_rate) > int(self.audio_input_sample_rate):
            raise ValueError(
                "New sample rate ({}) ".format(
                    self.new_sample_rate
                ) +
                "is higher than original sample rate ({})".format(
                    self.audio_input_sample_rate
                )
            )

    def _print_sample_rate(self, which_data):
        print_this = self._what_to_print(
            which_data,
            self.audio_input_sample_rate,
            self.audio_output_sample_rate
        )
        print("Sample rate: {}".format(print_this))

    def _print_format(self, which_data):
        print_this = self._what_to_print(
            which_data,
            self.audio_input_format,
            self.audio_output_format
        )
        print("{}".format(print_this))

    def _print_encoding(self, which_data):
        print_this = self._what_to_print(
            which_data,
            self.audio_input_encoding,
            self.audio_output_encoding
        )
        print("Encoding: {}".format(print_this))

    def _print_number_of_samples(self, which_data):
        if which_data == 'input':
            print_this = self.audio_input_number_of_samples
        else:
            print_this = 'Not supported yet by Audiolab'
        print("Number of samples: {}".format(print_this))

    def _print_number_of_channels(self, which_data):
        print_this = self._what_to_print(
            which_data,
            self.audio_input_number_of_channels,
            self.audio_output_number_of_channels
        )
        print("Number of channels: {}".format(print_this))

    def _what_to_print(self, which_data, input_data, output_data):
        if which_data == "input":
            print_this = input_data
        elif which_data == "output":
            print_this = output_data
        return(print_this)

    def _set_output_metadata(self):
        """Set output metadata"

        It needs to be set as it will not exist at
        the beginning and the print functions will fail
        """
        self.audio_output_data = ''
        self.audio_output_format = ''
        self.audio_output_encoding = ''
        self.audio_output_sample_rate = ''
        self.audio_output_number_of_samples = ''
        self.audio_output_number_of_channels = ''

    def _set_updated_output_metadata(self):
        self.audio_output_format = self.audio_output.format
        self.audio_output_encoding = self.audio_output.encoding
        self.audio_output_sample_rate = self.audio_output.samplerate
        self.audio_output_number_of_channels = self.audio_output.channels

        # Not yet supported by Audiolab
        # self.audio_output_number_of_samples = self.audio_output.nframes

    def _get_audio_output_file(self):
        return(
            "./results/" +
            self._get_file_name() +
            "_downsampled_to_" +
            self.new_sample_rate +
            ".wav"
        )

    def _get_png_file_output(self, which_data):
        return(
            "./results/" +
            self._get_file_name() +
            "_downsampled_to_" +
            self.new_sample_rate +
            "_" + which_data +
            ".png"
        )

    def _get_file_name(self):
        """Get file name

        WARNING: Assumes that input file name does not have dots
        int its file name. For example, `test_audio.wav` is fine,
        but `test.audio.wav` is not fine and will cause problems
        """
        return(self.audio_input_file.split("/")[-1].split(".")[0])


def main(argv):

    if len(argv) < 2:
        raise ValueError(
            "Needs `audio_input_file` and `new_sample_rate` " +
            "arguments (see code instructions)"
        )

    audio_input_file = argv[0]
    new_sample_rate = argv[1]

    downsample = Downsample(audio_input_file, new_sample_rate)

    downsample.print_data('input')
    downsample.graph_signal('input')

    downsample.downsample()

    downsample.print_data('output')
    downsample.graph_signal('output')


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
