from pygal.style import Style
from pygal import Config
from pygal import XY


def makeChart(snd, fill=False, color="#000", bgcolor="transparent", numsamples=1000, skip=0):

    # Normalize the data
    snd = (snd / 2) + [0.5, 0.5]
    # print(snd.min(), snd.max())

    config = Config()
    config.show_legend = False
    config.human_readable = False
    config.fill = fill
    config.show_y_guides = False
    config.show_x_guides = False
    config.show_dots = False
    config.range = (0, 1)
    config.xrange = (0, 1)

    background = bgcolor

    style = Style(
        background= background,
        plot_background= background,
        foreground= background,
        foreground_strong= background,
        foreground_subtle= background,
        opacity='.1',
        transition='0ms',
        colors=(color, color)
    )

    chart = XY(config, style=style)
    # Add the data points to the chart
    limit = (numsamples + skip) if numsamples > 0 else len(snd)
    chart.add('Lissajous', [(x[0], x[1]) for x in snd[skip:limit]], interpolate='cubic')
    return chart

def renderSVGChart(chart, name, dpi=300, width=3000, height=3000):
  # path for svg file based on the input file
  svgpath = name + '.svg'
  chart.render_to_file(svgpath, dpi=dpi, width=width, height=height)

def renderPNGChart(chart, name, dpi=300, width=3000, height=3000):
  pngpath = name + '.png'
  chart.render_to_png(pngpath, dpi=dpi, width=width, height=height)


if __name__ == "__main__":
    import argparse
    import soundfile as sf

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Convert AIFF or WAV file to Lissajous visualization.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-x", '--width', type=int, default=800, help='Width of the output image')
    parser.add_argument("-y", '--height', type=int, default=800, help='Height of the output image')
    parser.add_argument("-d", '--dpi', type=int, default=300, help='DPI of the output image')
    parser.add_argument("-c", '--color', type=str, default="#000000", help='foreground color (hex code)')
    parser.add_argument("-f", '--fill', action='store_true', help='fill')
    parser.add_argument("-b", '--bgcolor', type=str, default='transparent', help='background color (hex code)')
    parser.add_argument("-s", '--skip', type=int, default=0, help='Number of samples to skip')
    parser.add_argument("-n", '--numsamples', type=int, default=-1, help='Number of samples to use')
    parser.add_argument("-o", '--outname', type=str, help='Path to the output file without extension. If not provided, the output file will have the same name as the input file')
    parser.add_argument("-p", '--renderpng', action='store_true', help='Render also to PNG file')
    parser.add_argument("-v", '--verbose', action='store_true', help='Print debug information')
    parser.add_argument('infile', type=str, help='Path to the sound file')
    args = parser.parse_args()

    filename = args.infile

    # if outname is not provided, use the same name as the input file
    if args.outname is None:
        # path for svg file based on the input file
        outname = filename.split('.')[0]
    else:
        outname = args.outname

    # Load soundfile
    # try reading the file and throw an error if it fails
    try:
        snd, sr = sf.read(filename)
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        exit(1)

    if args.verbose:
        print(f"Loaded {filename} with {len(snd)} samples at {sr} Hz")

    # Create the chart
    chart = makeChart(snd, fill=args.fill, color=args.color, bgcolor=args.bgcolor, numsamples=args.numsamples, skip=args.skip)

    # Render the chart
    renderSVGChart(chart, outname, dpi=args.dpi, width=args.width, height=args.height)

    if args.verbose:
        print(f"Chart saved as {outname}.svg")

    if args.renderpng:
        renderPNGChart(chart, outname, dpi=args.dpi, width=args.width, height=args.height)
        if args.verbose:
            print(f"Chart saved as {outname}.png")


# example usage:
# python sound2lissajous.py -x 800 -y 800 -d 300 -c "#000000" -f -b "transparent" -s 0 -n 1000 -o lissajous -p -v sound.wav

# for loop including all wav and aiff files in the current directory


