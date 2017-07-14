
| [Website](http://links.otrenav.com/website) | [Twitter](http://links.otrenav.com/twitter) | [LinkedIn](http://links.otrenav.com/linkedin)  | [GitHub](http://links.otrenav.com/github) | [GitLab](http://links.otrenav.com/gitlab) | [CodeMentor](http://links.otrenav.com/codementor) |

---

# Audio cross-correlation analysis

- Omar Trejo
- August, 2016

## Objective

The first time I worked on this project it was to Downsample WAV files and to
provide cross-correlation analysis. The second time I worked on these was to add
support for HDF5 file format.

## How to use this scripts

The documentation for each script is within itself. Here
I'll only explain the general procedure to use them.

1.  Put the two audio files in the the "audio" directory which is
    located in the root directory for these scripts. Let's assume
    one is called "test_audio_original.wav" and the other one
    is called "test_audio_delayed.wav".

2.  Downsample both audio files to the desired sample rate. Keep
    in mind that the desired sample rate should be at most the
    same than the lowest of the sample rates for the two files.

    `$ python downsample.py ./audio/test_original.wav 8192`
    `$ python downsample.py ./audio/test_delayed.wav  8192`

    For each command you will see some output showing the information
    of it's original audio file as well as the downsampled version.

    The results will be stored as:

    `./results/test_original_downsampled_to_8192.wav`
    `./results/test_delayed_downsampled_to_8192.wav`

    These two files have the same sample rate and are usable
    for correlation analysis. Two graphs will be created for
    each of those two files showing the signal before and
    after downsampling.

3. Perform the correlation analysis on the two file that resulted
   from the last step. You can do so by doing:

   `$ python analysis.py ./results/test_original_downsampled_to_8192.wav
                         ./results/test_delayed_downsampled_to_8192.wav`

    The command should be a single continuous line (it's been split in the
    example to facilitate reading it.

    This command will create a graph that shows the correlation analysis (it
    will be stored in the "results" directory and will print the correlation
    data to the terminal.

---

> "The best ideas are common property."
>
> —Seneca
