import sys
import json
import argparse

from pathlib import Path

from npdep_client.args.Args import Args
from npdep_client.output.Output import Output
from npdep_client.registration.Registration import Registration

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

    # Load configuration
    f = open(args.config)
    c = json.load(f)

    # Create UUID for registration of compromised system
    homeDir = str(Path.home())
    registration = Registration(homeDir)

    # Get module name and options
    if("options" in c and "modulePath" in c["options"]):
        modulePath = c["options"]["modulePath"]
    else:
        modulePath = None
        
    sourcingOptions = c["sourcing"]["module"]["options"]
    sourcingModuleName = c["sourcing"]["module"]["name"]
    transferOptions = c["transfer"]["module"]["options"]
    transferModuleName = c["transfer"]["module"]["name"]

    # Initialize loader
    loader = Loader()
    
    if(modulePath != ""):
        out.printLoadingFromModulePath(modulePath, sourcingModuleName, transferModuleName)
        SourcingModuleClass = loader.getModuleClassFromPath(sourcingModuleName, modulePath)
        TransferModuleClass = loader.getModuleClassFromPath(transferModuleName, modulePath)
    else:
        out.printLoadingFromSitePkgs(sourcingModuleName, transferModuleName)
        SourcingModuleClass = loader.getModuleClassFromSitePkgs(sourcingModuleName)
        TransferModuleClass = loader.getModuleClassFromSitePkgs(transferModuleName)

    # Create Sourcing Instance
    s = SourcingModuleClass(sourcingOptions, registration)
    
    # Call the init method of the sourcing module
    s.init()
    # Call the get method of the sourcing module to trigger 
    # specific data discovery and collection capabilities
    data = s.get()
    # Call the end method of the sourcing module
    s.end()

    # Create Transfer Instance
    t = TransferModuleClass(transferOptions, registration)

    # Call the init method of the transfer module
    t.init()
    # Transfer the data with the specific transfer module
    t.send(data)
    # Call the end method of the transfer module
    t.end()

    out.printExecutionTime()

if __name__ == "__main__":
    sys.exit(main())