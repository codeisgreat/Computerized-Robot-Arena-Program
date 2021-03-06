#!/usr/local/bin/python2.7
# encoding: utf-8
'''
The CLI wrapper 

main is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2014 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

# =======
# IMPORTS
# =======

import sys
import os

import importlib.machinery
'''
Used for dynamically loading the provided scripts.

For a short explanation of how this is being used, see:
http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
'''

import logging
''' Import logging module. '''

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from game import Game
from set import Set

# ======================
# VERSIONING INFORMATION
# ======================

__all__ = []
__version__ = '0.1.3'
__date__ = '2014-03-05'
__updated__ = '2014-03-18'

# ==================
# DEGUGGING SETTINGS
# ==================

DEBUG = True
LOG_LEVEL = logging.DEBUG
TESTRUN = False
PROFILE = False

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def importModule(path):
    loader = importlib.machinery.SourceFileLoader("script", path)
    return loader.load_module("script")

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by DePaul CSS on %s.
  Copyright 2014 DePaul Computer Science Society. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        
        # =========================
        # CONFIGURE ARGUMENT PARSER
        # =========================
        
        # initialize argument parser object
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        
        # add arguments to parser
        # arguments are expected in the order they are added,
        # so ordering here matters.
        
        # add verbose argument
        parser.add_argument("-v", "--verbosity", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        
        # add version argument
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
#         parser.add_argument('-p', '--paths', help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="path", nargs='+')
        parser.add_argument("script1", help="The python file containing the first behavior script.")
        parser.add_argument("script2", help="The python file containing the second behavior script.")

        # =====================
        # PROCESS CLI ARGUMENTS
        # =====================

        # Process arguments
        args = parser.parse_args()
        
        # retrieve CLI verbosity value
        level = logging.WARNING
        if args.verbose is not None:
            if args.verbose == 1:
                level = logging.INFO
            elif args.verbose >= 2:
                level = logging.DEBUG
        
        # now ignore CLI verbosity value and set verbosity according to debug settings
        if DEBUG:
            level = LOG_LEVEL
        
            
        logging.basicConfig(format='%(levelname)s:%(message)s', level=level)
        
        # retrieve script1 argument
        script1 = args.script1
        script2 = args.script2
        
        logging.info('{}, {}'.format(script1, script2))
        
        # ======================
        # CONFIGURE AND RUN GAME
        # ======================
        
        # load the scripts
        scripts = {}
        scripts['{}_0'.format(script1)] = importModule(script1).robotBehavior()
        scripts['{}_1'.format(script2)] = importModule(script2).robotBehavior()
        
        logging.debug(scripts)

        # create game object
        runner = Set(scripts, decay = .99, maximumGames = 0)
        
        print(runner.scoreBoard)

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append('-vv')
#     if TESTRUN:
#         import doctest
#         doctest.testmod()
#     if PROFILE:
#         import cProfile
#         import pstats
#         profile_filename = 'main_profile.txt'
#         cProfile.run('main()', profile_filename)
#         statsfile = open("profile_stats.txt", "wb")
#         p = pstats.Stats(profile_filename, stream=statsfile)
#         stats = p.strip_dirs().sort_stats('cumulative')
#         stats.print_stats()
#         statsfile.close()
#         sys.exit(0)
    sys.exit(main())