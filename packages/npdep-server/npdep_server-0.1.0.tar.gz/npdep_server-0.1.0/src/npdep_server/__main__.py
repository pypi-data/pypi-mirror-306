import sys
import json
import argparse

from npdep_server.args.Args import Args
from npdep_server.output.Output import Output
from npdep_server.logger.Logger import Logger
from npdep_server.util.Util import Util

from npdep_common.loader.Loader import Loader

def main(args_=None):
    """The main routine."""
    if args_ is None:
        args_ = sys.argv[1:]

    parser = argparse.ArgumentParser()
    Args.addArguments(parser)
    args = parser.parse_args()

    # Creates Output instance for printing header and footer of console output
    out = Output()
    out.printHeader()

    if(args.purge):
            Util.purge(args.purge)
    else:
        # Load configuration
        f = open(args.config)
        c = json.load(f)

        # Initialize loader
        loader = Loader()

        # Initialise logger
        logger = Logger(args.logfile)

        # Get Module Names
        modules = c["modules"]

        # Check if there is a special module path
        if("options" in c and "modulePath" in c["options"]):
            modulePath = c["options"]["modulePath"]
        else:
            modulePath = None

        # Start modules
        for module in modules:
            moduleClass = None

            if(modulePath != ""):
                out.printLoadingFromModulePath(module["name"], modulePath)
                ModuleClass = loader.getModuleClassFromPath(modulePath, module["name"])    
            else:
                out.printLoadingFromSitePkgs(module["name"])
                ModuleClass = loader.getModuleClassFromSitePkgs( module["name"])
            
            classInstance = ModuleClass(module["options"], logger)
            classInstance.start()
            logger.log("Module: " + module["name"] + " started, Options: " + str(module["options"])) 

    out.printUpRunning()

if __name__ == "__main__":
    sys.exit(main())