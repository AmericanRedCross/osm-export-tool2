# -*- coding: utf-8 -*-
import argparse
import logging
import subprocess32 as subprocess

logger = logging.getLogger(__name__)


class MBTiles(object):
    """
    Generate MBTiles.
    """

    def __init__(
        self,
        bbox=None,
        source=None,
        max_zoom=None,
        min_zoom=None,
        out=None,
        job_name=None,
        debug=False,
    ):
        """
        Initialize the MBTiles utility.

        Args:
            bbox: the bounding box to extract (w,s,e,n)
            source: tilelive source URI
            min_zoom: min zoom
            max_zoom: max zoom
            out: output file
            job_name: the name of the export job
            debug: turn on/off debug logging
        """
        self.bbox = bbox
        self.source = source
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.out = out
        self.debug = debug

    def generate(self, ):
        """
        Generate an MBTiles archive.
        """
        generate_cmd = [
            'tl',
            'copy',
            '-q',
            '-b',
            self.bbox,
            '-z',
            str(self.min_zoom),
            '-Z',
            str(self.max_zoom),
            self.source,
            'mbtiles://' + self.out,
        ]

        if self.debug:
            print 'Running: %s' % generate_cmd

        returncode = subprocess.call(
            generate_cmd,
            timeout=60 * 60,
        )

        if returncode != 0:
            raise Exception("tl failed with return code: {0}".format(returncode))

        if self.debug:
            print 'tl returned: %s' % returncode

        return self.out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates MBTiles')
    parser.add_argument('-b', '--bbox', required=True, dest="bbox",
                        help='Bounding box (w,s,e,n)')
    parser.add_argument('-z', '--min-zoom', required=True, dest="min_zoom", help='Min zoom')
    parser.add_argument('-Z', '--max-zoom', required=True, dest="max_zoom", help='Max zoom')
    parser.add_argument('-s', '--source', required=True, dest="source", help='Source URI')
    parser.add_argument('-o', '--output', required=True, dest="out", help='Target file')
    parser.add_argument('-d', '--debug', action="store_true", help="Turn on debug output")
    args = parser.parse_args()
    mbtiles = MBTiles(**vars(args))
    mbtiles.generate()
