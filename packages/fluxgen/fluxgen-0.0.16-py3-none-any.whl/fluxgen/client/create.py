import fluxgen.command.create as create
import fluxgen.utils as utils


def main(args, parser, command, subparser):
    # Assemble options we know are important
    options = {
        "lead-broker": args.lead_broker,
        "linkname": args.linkname,
        "command": command or None,
        "brokers": args.brokers,
        "subdomain": args.subdomain,
    }

    # This will raise an error if the member type (e.g., minicluster) is not known
    generator = create.FluxInstallScript()
    result = generator.render(**options)

    # This is a preview only
    if args.dry_run:
        print(result)
        return

    print(f"Writing install script to {args.outfile}")

    # Write to file, and ensure is made executable
    utils.write_file(result, args.outfile, executable=True)
