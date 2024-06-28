import sound2lissajous as s2l
import sounddevice as sd

def record_audio(samplerate=48000, duration=1.0, channels = 2, device=0):

    # test if the device is available and can record number of channels
    if not sd.query_devices(device, 'input')["max_input_channels"] >= channels:
        raise ValueError(f"Device {device} does not support {channels} channels")

    # Record audio from the microphone
    samples = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, device=device)

    # Wait for the recording to complete
    sd.wait()

    return samples


if __name__ == "__main__":
    import argparse
    import soundfile as sf
    import datetime

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='record  or WAV file to Lissajous visualization.', formatter_class=argparse.ArgumentDefaultsHelpFormatter, epilog="output files always have a timestamp added to their name.")
    # example usage
    # python rt2lissajous.py -x 800 -y 800 -d 300 -c "#000000" -f -b transparent -s 0 -n 1000 -o test -p -v -i 0 --srate 48000 --dur 1.0
    parser.add_argument("-x", '--width', type=int, default=800, help='Width of the output image')
    parser.add_argument("-y", '--height', type=int, default=800, help='Height of the output image')
    parser.add_argument("-d", '--dpi', type=int, default=300, help='DPI of the output image')
    parser.add_argument("-c", '--color', type=str, default="#000000", help='foreground color (hex code)')
    parser.add_argument("-f", '--fill', action='store_true', help='fill')
    parser.add_argument("-b", '--bgcolor', type=str, default='transparent', help='background color (hex code)')
    parser.add_argument("-s", '--skip', type=int, default=0, help='Number of samples to skip')
    parser.add_argument("-n", '--numsamples', type=int, default=-1, help='Number of samples to use. If not provided, all samples will be used.')
    parser.add_argument("-o", '--outname', type=str, help='Path to the output file without extension. If not provided, the output file will be a timestamp based name.')
    parser.add_argument("-p", '--renderpng', action='store_true', help='Render also to PNG file')
    parser.add_argument("-v", '--verbose', action='store_true', help='Print debug information')
    parser.add_argument("-i", '--device', type=int, default=0, help='Input device index.')
    parser.add_argument('--list-devices', action='store_true', help='List available input devices and exit')
    parser.add_argument('--srate', type=int, default=48000, help='Sample rate in Hz')
    parser.add_argument('--dur', type=float, default=1.0, help='Duration in seconds')
    args = parser.parse_args()


    # if device is -1, list available devices and their number of input channels
    if args.list_devices:
        print("Available input devices:")
        for i, dev in enumerate(sd.query_devices()):
            if dev["max_input_channels"] > 0:
                print(f"{i}\t({dev['max_input_channels']} ins): {dev['name']}")
        exit(0)

    # if outname is not provided, create a name based on the current date and time
    outname = f"{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}_{args.dur}s_{args.srate}Hz"
    if args.outname is not None:
        outname = args.outname + "_" + outname

    # Record audio
    # try recording audio and throw an error if it fails
    try:
        samples = record_audio(samplerate=args.srate, duration=args.dur, device=args.device)
    except Exception as e:
        print(f"Error recording audio: {e}")
        exit(1)

    # write audio to file
    sf.write(f"{outname}.wav", samples, args.srate)
    if args.verbose:
        print(f"Audio saved as {outname}.wav")

    # Create the chart
    chart = s2l.makeChart(samples, fill=args.fill, color=args.color, bgcolor=args.bgcolor, numsamples=args.numsamples, skip=args.skip)

    # Render the chart
    s2l.renderSVGChart(chart, outname, dpi=args.dpi, width=args.width, height=args.height)

    if args.verbose:
        print(f"Chart saved as {outname}.svg")

    if args.renderpng:
        s2l.renderPNGChart(chart, outname, dpi=args.dpi, width=args.width, height=args.height)
        if args.verbose:
            print(f"Chart saved as {outname}.png")
    


