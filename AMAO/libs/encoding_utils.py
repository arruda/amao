# -*- coding: utf-8 -*-
"""
    libs.encoding_utils
    ~~~~~~~~~~~~~~

    force encoding of a file
    
    :copyright: (c) 2012 by arruda.
"""

import os
import shutil

def convert_to_utf8(filename):
    # gather the encodings you think that the file may be
    # encoded inside a tuple
    encodings = ('ascii','iso-8859-1', 'iso-8859-7', 'windows-1253','macgreek')

    f = open(filename, 'r').read()

    # now start iterating in our encodings tuple and try to
    # decode the file
    for enc in encodings:
        try:
            # try to decode the file with the first encoding
            # from the tuple.
            # if it succeeds then it will reach break, so we
            # will be out of the loop (something we want on
            # success).
            # the data variable will hold our decoded text
            data = f.decode(enc)
            print "encoded with:%s" % enc
            break
        except Exception, e:
            # if the first encoding fail, then with the continue
            # keyword will start again with the second encoding
            # from the tuple an so on.... until it succeeds.
            # if for some reason it reaches the last encoding of
            # our tuple without success, then exit the program.
            if enc == encodings[-1]:
                raise e
            continue

    # now get the absolute path of our filename and append .bak
    # to the end of it (for our backup file)
    fpath = os.path.abspath(filename)
    newfilename = fpath + '.bak'
    # and make our backup file with shutil
    shutil.copy(filename, newfilename)

    # and at last convert it to utf-8
    f = open(filename, 'w')
    try:
        f.write(data.encode('utf-8'))
    except Exception, e:
        raise e
    finally:
        f.close()

