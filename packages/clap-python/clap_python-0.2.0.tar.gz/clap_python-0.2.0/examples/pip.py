from clap_python import App, Arg, ClapPyException, MutuallyExclusiveGroup, SubCommand
from clap_python.complete import autocomplete


def cli() -> App:
    """The pip-like command line interface."""
    return (
        App("pip")
        .arg(
            SubCommand("install")
            .arg(Arg("requirement-specifier").required(False))
            .arg(
                Arg("-r", "--requirement")
                .value_name("requirements file")
                .help(
                    "Install from the given requirements file. This option can be used multiple times."
                )
            )
            .arg(
                Arg("-e", "--editable")
                .value_name("--editable <path/url>")
                .help(
                    'Install a project in editable mode (i.e. setuptools "develop mode") from a local project path or a VCS url.'
                )
            )
            .arg(
                Arg("--user").help(
                    "Install to the Python user install directory for your platform. Typically ~/.local/, or %APPDATA%\Python on Windows. (See the Python documentation for site.USER_BASE for full details.)"
                )
            )
        )
        .arg(
            SubCommand("uninstall")
            .help_heading("Uninstall Options")
            .arg(
                Arg("-r", "--requirement")
                .value_name("--requirement <file>")
                .help(
                    "Uninstall all the packages listed in the given requirements file.  This option can be used multiple times."
                )
            )
            .arg(
                Arg("-y", "--yes").help(
                    "Don't ask for confirmation of uninstall deletions."
                )
            )
            .help_heading("General Options")
            .arg(
                Arg("--debug").help(
                    "Let unhandled exceptions propagate outside the main subroutine, instead of logging them to stderr."
                )
            )
        )
        .arg(
            SubCommand("list")
            .arg(Arg("-o", "--outdated").help("List outdated packages"))
            .arg(Arg("-e", "--editable").help("List editable projects."))
            .arg(Arg("--user").help("Only output packages installed in user-site."))
        )
    )


# Placeholder for argument handling logic
if __name__ == "__main__":
    import json

    app = cli()
    autocomplete(app)
    args = app.parse_args()
    print(json.dumps(args, indent=4))
