#!/usr/bin/python3
"""
apk-exporter is a Prometheus exporter for monitoring apk-tools. It provides
metrics like installed, upgradable, and orphaned packages, which can be
exported to a Prometheus Pushgateway or written to a text file to be parsed
by node-exporter.
"""
import argparse
import subprocess
import os
import sys

import prometheus_client as prometheus

registry = prometheus.CollectorRegistry()

installed_packages = prometheus.Gauge(
    "apk_installed_packages",
    "The current number of installed packages",
    registry=registry,
)
upgradeable_packages = prometheus.Gauge(
    "apk_upgradable_packages",
    "The current number of updateable packages",
    registry=registry,
)
orphaned_packages = prometheus.Gauge(
    "apk_orphaned_packages",
    "The current number of orphan packages",
    registry=registry,
)


def apk(arguments: list[str]) -> list[str]:
    "Calls apk with arguments and returns a list of output lines"
    args = ["apk"]
    args.extend(arguments)
    cmd = subprocess.run(
        args, capture_output=True, encoding="utf-8", check=True
    )  # noqa: E501
    return cmd.stdout.splitlines()


def update():
    "Runs 'apk update' on  the host system"
    os.system("apk update")


def collect():
    "Collects all informations and sets them"
    installed_packages.set(len(apk(["list", "-I"])))
    upgradeable_packages.set(len(apk(["list", "-u"])))
    orphaned_packages.set(len(apk(["list", "-O"])))


def get_args():
    "Gets the program's arguments"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--textfile-dir",
        help="Set the directory of the prometheus textfile",
        default="/tmp",
    )
    parser.add_argument(
        "--textfile",
        help="Weather to write a textfile",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--pushgateway",
        help="Weather to export to a pushgateway",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--pushgateway-server", help="Gateway to export metrics to"
    )  # noqa: E501
    parser.add_argument(
        "--pushgateway-job",
        help="Job for the pushgateway server",
        default="apk_exporter",
    )
    parser.add_argument(
        "--update",
        help="Weather to update APK repository indexes before exporting",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    return parser.parse_args()


def main():
    "Main program"
    args = get_args()

    if args.update:
        update()

    collect()

    if args.textfile:
        file = os.path.join(args.textfile_dir, "apk.prom")
        prometheus.write_to_textfile(file, registry)
        print(f"Wrote to {file}")

    if args.pushgateway:
        prometheus.push_to_gateway(
            args.pushgateway_server, args.pushgateway_job, registry
        )
        print(f"Pushed to {args.pushgateway_server} ({args.pushgateway_job})")

    if not args.textfile and not args.pushgateway:
        print("Nothing to do")
        sys.exit(1)


if __name__ == "__main__":
    main()
