# Sound2Lissajous
*2024, Till Bovermann*

![](yellow.gif)

Python scripts that generate a Lissajous curve from sound signals. 
The Lissajous curve is generated by plotting the left channel on the x-axis and the right channel on the y-axis.

## Install

Best to use a virtual environment to install the required dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

After activating the virtual environment, you can install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### sound2lissajous.py

The `sound2lissajous.py` script generates a Lissajous curve from a sound file.
See the help message for more information:

```bash
python sound2lissajous.py -h
```

Example usage:

```bash
python sound2lissajous.py sound.wav
```

returns an svg file with the Lissajous curve, named after the input file.

### rt2lissajous.py

The `rt2lissajous.py` script captures a stereo signal from the input device and generates a Lissajous curve in real-time.
Apart from arguments specofoc to r/t capturing, it takes the same arguments as `sound2lissajous.py`.

Example usage:

```bash
python rt2lissajous.py
```

returns a wav file with the recorded audio and the Lissajous curve, both named with the current timestamp.

## Dependencies

The scripts depend on the following Python packages:

+ [sounddevice](https://pypi.org/project/sounddevice/)
+ [soundfile](https://pypi.org/project/soundfile/)
+ [numpy](https://numpy.org/)
+ [pygal](https://www.pygal.org/)


They are listed in the `requirements.txt` file and installed with the `pip` command mentioned above.