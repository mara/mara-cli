"""Mara command line interface"""

import logging
import sys

import click

log = logging.getLogger(__name__)

RED = '\033[31m'
RESET = '\033[0m'


@click.group(help="""
The Mara ETL Framework is a Python framework to build data pipelines.

Contributed functionality (ETL runners, downloader,...) are available as subcommands.""")
@click.option('--debug', default=False, is_flag=True, help="Show debug output")
@click.option('--log-stderr', default=False, is_flag=True, help="Send log output to stderr")
def cli(debug: bool, log_stderr: bool):
    # --debug is consumed by the setup_commandline_commands but it's here to let it show up in help
    # and not cause parse errors
    pass


def setup_commandline_commands():
    """Needs to be run before click itself is run so the config which contributes click commands is available"""
    from ._mara_modules import import_mara_modules, get_contributed_functionality
    commandline_debug = '--debug' in sys.argv
    # makefiles expect all log in stdout. Send to stderr only if asked to
    log_stream = sys.stderr if '--log-stderr' in sys.argv else sys.stdout
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s, %(name)s: %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S',
                        stream=log_stream)

    if commandline_debug:
        logging.root.setLevel(logging.DEBUG)
        log.debug("Enabled debug output via commandline")

    # Import all installed mara packages
    import_mara_modules(log)

    known_names = []
    for module, command in get_contributed_functionality('MARA_CLICK_COMMANDS', click.Command):
        if command and 'callback' in command.__dict__ and command.__dict__['callback']:
            package = command.__dict__['callback'].__module__.rpartition('.')[0]
            # Give a package a chance to put all their commands as subcommands of the main package name.
            # For that to work we have to make sure we do not add multiple commands with the same name
            if isinstance(command, click.MultiCommand):
                if command.name.startswith('mara-'):
                    name = command.name[5:]
                else:
                    name = command.name
            else:
                name = package + '.' + command.name
            if name in known_names:
                callback = command.__dict__['callback']
                func_name = f"{callback.__module__}{callback.__name__}"
                raise RuntimeError(f"Attempting to add conflicting click.Commands for name '{name}': {func_name}")
            known_names.append(name)
            command.name = name
            cli.add_command(command)
    
    if not cli.commands:
        # Could not find any command in the installed modules
        print(RED + "No mara package is installed which provide commands" + RESET, file=sys.stderr)
        print("""
Please install the packages you want to use, e.g. by calling
              
    pip install mara-pipelines
""", file=sys.stderr)
        sys.exit(1)


def main():
    """'mara' console_scripts entry point"""
    setup_commandline_commands()
    args = sys.argv[1:]
    cli.main(args=args, prog_name='mara')


if __name__ == '__main__':
    main()
