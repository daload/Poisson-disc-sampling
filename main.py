import argparse
import poisson_disc_sampling as pds

parser = argparse.ArgumentParser()
parser.add_argument('-x', '--width', type=int, help='an integer for width of the domain')
parser.add_argument('-y', '--height', type=int, help='an integer for height of the domain')
parser.add_argument('-k', type=int, help='an integer for the number of points around each reference point '
                                         'as candidates for a new sample point')
parser.add_argument('-r', '--radius', type=float, help='a float for the minimum distance between samples')
args = vars(parser.parse_args())

w = args['width'] if args['width'] != None else 60
h = args['height'] if args['height'] != None else 45
k = args['k'] if args['k'] != None else 30
r = args['radius'] if args['radius'] != None else 1.7
pds.pds(w, h, k, r)
