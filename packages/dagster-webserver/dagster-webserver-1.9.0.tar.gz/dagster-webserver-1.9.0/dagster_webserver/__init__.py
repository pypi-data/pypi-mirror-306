from dagster._core.libraries import DagsterLibraryRegistry

from dagster_webserver.version import __version__

DagsterLibraryRegistry.register("dagster-webserver", __version__)
