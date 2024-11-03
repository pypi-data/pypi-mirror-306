create

uv is an extremely fast Python package and project manager, written in Rust. A new tool to replace pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv, and more. However, it lacks the ability to manage virtual environments in a centralized location as it is done in conda. So, I am building a new tool uvn that relies on uv to add support for this feature.

I am now implementing my uvn create command that creates virtual environments but I am not sure which arguments are important to support in my tool. Here is the help message of uv venv:

```
Create a virtual environment

Usage: uv venv [OPTIONS] [PATH]

Arguments:
  [PATH]  The path to the virtual environment to create

Options:
      --no-project                                 Avoid discovering a project or workspace
      --seed                                       Install seed packages (one or more of: `pip`, `setuptools`, and `wheel`) into the virtual environment
      --allow-existing                             Preserve any existing files or directories at the target path
      --prompt <PROMPT>                            Provide an alternative prompt prefix for the virtual environment.
      --system-site-packages                       Give the virtual environment access to the system site packages directory
      --relocatable                                Make the virtual environment relocatable
      --index-strategy <INDEX_STRATEGY>            The strategy to use when resolving against multiple index URLs [env: UV_INDEX_STRATEGY=] [possible values: first-index, unsafe-first-match, unsafe-best-match]
      --keyring-provider <KEYRING_PROVIDER>        Attempt to use `keyring` for authentication for index URLs [env: UV_KEYRING_PROVIDER=] [possible values: disabled, subprocess]
      --allow-insecure-host <ALLOW_INSECURE_HOST>  Allow insecure connections to a host [env: UV_INSECURE_HOST=]
      --exclude-newer <EXCLUDE_NEWER>              Limit candidate packages to those that were uploaded prior to the given date [env: UV_EXCLUDE_NEWER=]
      --link-mode <LINK_MODE>                      The method to use when installing packages from the global cache [env: UV_LINK_MODE=] [possible values: clone, copy, hardlink, symlink]

Python options:
  -p, --python <PYTHON>                        The Python interpreter to use for the virtual environment. [env: UV_PYTHON=]
      --python-preference <PYTHON_PREFERENCE>  Whether to prefer uv-managed or system Python installations [env: UV_PYTHON_PREFERENCE=] [possible values: only-managed, managed, system, only-system]
      --no-python-downloads                    Disable automatic downloads of Python. [env: "UV_PYTHON_DOWNLOADS=never"]

Index options:
      --index <INDEX>                      The URLs to use when resolving dependencies, in addition to the default index [env: UV_INDEX=]
      --default-index <DEFAULT_INDEX>      The URL of the default package index (by default: <https://pypi.org/simple>) [env: UV_DEFAULT_INDEX=]
  -i, --index-url <INDEX_URL>              (Deprecated: use `--default-index` instead) The URL of the Python package index (by default: <https://pypi.org/simple>) [env: UV_INDEX_URL=]
      --extra-index-url <EXTRA_INDEX_URL>  (Deprecated: use `--index` instead) Extra URLs of package indexes to use, in addition to `--index-url` [env: UV_EXTRA_INDEX_URL=]
  -f, --find-links <FIND_LINKS>            Locations to search for candidate distributions, in addition to those found in the registry indexes [env: UV_FIND_LINKS=]
      --no-index                           Ignore the registry index (e.g., PyPI), instead relying on direct URL dependencies and those provided via `--find-links`

Cache options:
  -n, --no-cache               Avoid reading from or writing to the cache, instead using a temporary directory for the duration of the operation [env: UV_NO_CACHE=]
      --cache-dir <CACHE_DIR>  Path to the cache directory [env: UV_CACHE_DIR=]

Global options:
  -q, --quiet                      Do not print any output
  -v, --verbose...                 Use verbose output
      --color <COLOR_CHOICE>       Control colors in output [default: auto] [possible values: auto, always, never]
      --native-tls                 Whether to load TLS certificates from the platform's native certificate store [env: UV_NATIVE_TLS=]
      --offline                    Disable network access
      --no-progress                Hide all progress outputs [env: UV_NO_PROGRESS=]
      --directory <DIRECTORY>      Change to the given directory prior to running the command
      --project <PROJECT>          Run the command within the given project directory
      --config-file <CONFIG_FILE>  The path to a `uv.toml` file to use for configuration [env: UV_CONFIG_FILE=]
      --no-config                  Avoid discovering configuration files (`pyproject.toml`, `uv.toml`) [env: UV_NO_CONFIG=]
  -h, --help                       Display the concise help for this command
  -V, --version                    Display the uv version

Use `uv help venv` for more details.
```

Here is a few examples of the things that I have in mind:
- Always enable --no-project so it will not be part of my arguments.
- Expose --seed and keep it not enabled by default
- Ignore --help and --version
- ...

Can you write the help message for uv create and list the enforced options that will be passed by default and hidden from the user?


---


Here’s a suggested help message for your `uvn create` command, assuming it wraps and extends `uv venv` while adding centralized environment management functionality.

### `uvn create` Help Message

```plaintext
Create a managed virtual environment in a centralized location

Usage: uvn create [OPTIONS] [ENV_NAME]

Arguments:
  [ENV_NAME]          The name of the virtual environment to create in the central directory

Options:
      --seed <SEED>                Install seed packages (`pip`, `setuptools`, `wheel`) into the virtual environment (default: no seeds installed)
      --prompt <PROMPT>            Custom prompt prefix for the virtual environment
      --system-site-packages       Allow the virtual environment to access system site packages
      --relocatable                Make the virtual environment relocatable
  -p, --python <PYTHON>            Specify the Python interpreter for the environment
      --index <INDEX>              Additional package index URLs for dependency resolution
      --default-index <URL>        Default package index URL (default: https://pypi.org/simple)
  -f, --find-links <URL>           Additional URLs to search for packages
      --no-index                   Ignore registry indexes, relying on URLs from `--find-links`
  -n, --no-cache                   Disable the cache for this operation
      --cache-dir <DIR>            Specify a custom cache directory
  -q, --quiet                      Suppress all output
  -v, --verbose                    Enable verbose output
      --offline                    Disable network access
      --no-progress                Suppress progress display
  -h, --help                       Show help message

Environment Management:
      --list                       List all managed virtual environments
      --delete <ENV_NAME>          Delete a specific managed environment
```

### Enforced Options

These options are enforced by default in `uvn` and hidden from users:

1. `--no-project` — Ensures environments are always isolated from any project/workspace configuration.
2. `--directory` — Points to the centralized location where environments are managed.
3. `--no-config` — Skips configuration file discovery to maintain uniformity.


---

Why do we have the option to specify --index and --find-link when all we are doing is just creating an environment without installing any packages (except for --seed)? I am planning to ignore --system-site-packages and --relocatable as well. Also, what does --no-cache do? My guess is that these are general options that got carried from other commands that are of no to little use for our case.

---

You’re absolutely right; many of these options are not directly relevant for a command focused solely on creating a virtual environment without installing additional packages. Here’s a breakdown:

1. **`--index`, `--default-index`, `--find-links`, `--no-index`**: These are indeed package-resolution options, relevant only when packages are being installed. Since `uvn create` primarily creates an environment without package installation, these can be ignored unless you plan to install seed packages (e.g., `pip`, `setuptools`, `wheel`). Even then, `--default-index` should suffice if seed packages are pulled from standard sources.

2. **`--system-site-packages`**: Controls access to global site packages, often used for special cases where dependencies aren’t isolated. Ignoring this option by default is sensible unless you anticipate specific needs for global access.

3. **`--relocatable`**: This makes a virtual environment moveable, a feature useful when transferring environments between systems. Since centralized management doesn’t typically require portability, it’s reasonable to ignore this option.

4. **`--no-cache`**: This disables cache reading/writing, potentially relevant if Python needs to be downloaded (e.g., if a specified Python version is missing). For most use cases, `--no-cache` can be ignored, as it mainly affects package installation.

5. **General Options**: You’re correct; many options are general-purpose flags included across multiple commands for flexibility. For `uvn create`, you can hide these to streamline the interface.

### Recommended `uvn create` Options

The minimal options for `uvn create` would then include:

- `--seed`: Optionally installs basic packages.
- `--prompt`: Allows custom environment prompts.
- `-p, --python`: Specifies Python version, if required.

---

  -p, --python <PYTHON>            Specify the Python interpreter for the environment
      --seed <SEED>                Install seed packages (`pip`, `setuptools`, `wheel`) into the virtual environment (default: no seeds installed)
      --prompt <PROMPT>            Custom prompt prefix for the virtual environment
      --default-index <URL>        Default package index URL (default: https://pypi.org/simple)
  -q, --quiet                      Suppress all output
