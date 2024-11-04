# `apk-exporter`

apk-exporter is a Prometheus exporter for monitoring `apk-tools`.
It provides metrics like installed, upgradable, and orphaned packages,
which can be exported to a Prometheus Pushgateway or written to a text file to
be parsed by node-exporter.

## Requirements

- Python 3.8 or higher
- `prometheus_client` python library
- `apk` package manager

## Usage

Run `apk_exporter.py` regulary (for example every hour).

Use `--textfile` to export as a text file, or use `--pushgateway` to push to a
gateway. See `--help` for all options.

### Import text file to node-exporter

Add the destination folder (/tmp by default) as the `node_exporter` arguments,
like this: `--collector.textfile.directory /tmp`.

If you're using a node-exporter OpenRC service, you can add the arguments to
`/etc/conf.d/node-exporter`:

```
ARGS="--collector.textfile.directory /tmp"
```
