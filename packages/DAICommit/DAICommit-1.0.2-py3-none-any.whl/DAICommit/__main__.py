from optparse import OptionParser, OptionGroup
from colorama import init, just_fix_windows_console
from git import Repo

init()
just_fix_windows_console()

from .utills import outro

VERSION = "1.0.2"

def main():
    parser = OptionParser(
        usage="usage: %prog [flags...] <command>",
        description="Auto-generate impressive commits in 1 second. Killing lame commits with AI 🤯🔫",
        add_help_option=False
    )

    parser.add_option(
        "-y", "--yes", action="store_true", dest="yes", help="Skip commit confirmation prompt"
    )

    parser.add_option(
        "-f", "--fgm", action="store_true", dest="fgm", help="Using the entire emoji list"
    )

    group = OptionGroup(parser, "Flags")
    group.add_option(
        "-h", "--help", action="store_true", dest="help", help="Show help"
    )
    group.add_option(
        "-v", "--version", action="store_true", dest="show_version", help="Show version"
    )
    parser.add_option_group(group)

    (options, args) = parser.parse_args()

    if options.show_version:
        print(f"DAICommit v{VERSION}")
        return

    if options.help:
        parser.print_help()
        print("\nCommands:")
        print("  config          Configure AICommit")
        print("  hook            Set up git hook")
        return

    try:
        command = args[0]
    except IndexError:
        command = 'commit'

    if command == 'commit':
        try:
            Repo()
        except Exception:
            outro('To get started, initialize git using the `git init` command', 'red')
            exit(0)
        from .commands import commit
        commit(False, options.fgm, options.yes)
    elif command == "config":
        from .commands import config
        config()
    elif command == "hook":
        print("Setting up git hook...")
    else:
        print(f"Unknown command: {command}")
        print("Use -h or --help for usage information.")

if __name__ == "__main__":
    main()
