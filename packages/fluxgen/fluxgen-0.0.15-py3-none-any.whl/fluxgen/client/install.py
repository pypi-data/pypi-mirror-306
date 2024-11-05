import fluxgen.command.install as install
import fluxgen.utils as utils


def main(args, parser, command, subparser):
    # This will raise an error if the member type (e.g., minicluster) is not known
    generator = install.FluxInstallScript()
    result = generator.render()

    # This is a preview only
    if args.dry_run:
        print(result)
        return

    print(f"Writing install script to {args.outfile}")

    # Write to file, and ensure is made executable
    utils.write_file(result, args.outfile, executable=True)
