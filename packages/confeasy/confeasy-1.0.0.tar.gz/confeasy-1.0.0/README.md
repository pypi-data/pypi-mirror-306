# confeasy

Application configuration inspired by Microsoft.Extensions.Configuration (.NET).

The main idea is to have the following workflow:
1) Define one or more configuration sources from where the actual configuration is created (or downloaded).
2) Build the configuration. This basically means put everything into a big flat dictionary
   where lastly defined sources could override values from previous ones if they match on the configuration key.
3) Use resulting configuration:
   a. Directly, picking up individual values by their key.
   b. Bind all or portion of the configuration to a strongly typed class instance (typically a dataclass)
      and use this instance instead of the configuration itself. The benefit is better intellisense in IDEs
      and more decoupling.

## Getting started

Install the package.

```shell
poetry add confeasy
# or similar command for your package manager of choice
```

In python, usually around application start:
```python

# DbOptions class is an illustrative example of strongly typed configuration.
class DbOptions:
    def __init__(self):
        self.connnection_string: str = ""
        self.max_connections: int = 100

from confeasy import Builder
from confeasy.jsonfile import JsonFile
from confeasy.tomlfile import TomlFile
from confeasy.envars import EnvironmentVariables
from confeasy.cmdline import CommandLine

# Order of the configuration sources matters; later sources can overwrite values from earlier ones.
builder = (Builder()
           .add_source(JsonFile()
                       .required("settings.json")
                       .optional("setting.local.json"))
           .add_source(TomlFile()
                       .optional("other_settings.toml"))
           .add_source(EnvironmentVariables("MYAPP_"))
           .add_source(CommandLine()))

config = builder.build()

# Bind configuration to a class instance and pass the instance to other objects.
options = config.bind(DbOptions(), prefix="db")

# OR pick up individual values:
db_conn_str = config.get_value("db.connection_string")
```

## Out-of-the-box configuration sources

* JSON files
* TOML files
* INI files
* command line arguments
* environment variables

## Additional configuration sources

* **confeasy.azure_appc** - using [Azure AppConfiguration][azure] service; [PyPI][appc_pypi] | [source][appc_gh]

## Development

For developer related information, check [Developer Guide](developer.md).

**Note:**
* YAML files will not be supported unless a parsing module is available in the standard library.


[azure]: https://learn.microsoft.com/en-us/azure/azure-app-configuration/overview
[appc_gh]: https://github.com/jdvor/confeasy-azure-appc
[appc_pypi]: https://pypi.org/project/confeasy.azure_appc