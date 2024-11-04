class Args():
    # parser: argparse instance
    def addArguments(parser):
        parser.add_argument("--config", "-c", type=str, required=True, help="Path to Configuration File")
        parser.add_argument("--logfile", "-l", type=str, default=".", help="Path to Log File")
        parser.add_argument("--purge", "-u", type=str, help="The given path (all files/subfolders) will be wiped. npdep-server is not starting, if this options is given.")  