I am building a modern Python library manged by `pyproject.toml` using src-layout. I want some help in packaging it. My setup is very similar to the following guide from `packaging.python.org`:

```rst
.. _creating-command-line-tools:

=========================================
Creating and packaging command-line tools
=========================================

This guide will walk you through creating and packaging a standalone command-line application
that can be installed with :ref:`pipx`, a tool creating and managing :term:`Python Virtual Environments <Virtual Environment>`
and exposing the executable scripts of packages (and available manual pages) for use on the command-line.

Creating the package
====================

First of all, create a source tree for the :term:`project <Project>`. For the sake of an example, we'll
build a simple tool outputting a greeting (a string) for a person based on arguments given on the command-line.

.. todo:: Advise on the optimal structure of a Python package in another guide or discussion and link to it here.

This project will adhere to :ref:`src-layout <src-layout-vs-flat-layout>` and in the end be alike this file tree,
with the top-level folder and package name ``greetings``:

::

    .
    ├── pyproject.toml
    └── src
        └── greetings
            ├── cli.py
            ├── greet.py
            ├── __init__.py
            └── __main__.py

The actual code responsible for the tool's functionality will be stored in the file :file:`greet.py`,
named after the main module:

.. code-block:: python

    import typer
    from typing_extensions import Annotated


    def greet(
        name: Annotated[str, typer.Argument(help="The (last, if --gender is given) name of the person to greet")] = "",
        gender: Annotated[str, typer.Option(help="The gender of the person to greet")] = "",
        knight: Annotated[bool, typer.Option(help="Whether the person is a knight")] = False,
        count: Annotated[int, typer.Option(help="Number of times to greet the person")] = 1
    ):
        greeting = "Greetings, dear "
        masculine = gender == "masculine"
        feminine = gender == "feminine"
        if gender or knight:
            salutation = ""
            if knight:
                salutation = "Sir "
            elif masculine:
                salutation = "Mr. "
            elif feminine:
                salutation = "Ms. "
            greeting += salutation
            if name:
                greeting += f"{name}!"
            else:
                pronoun = "her" if feminine else "his" if masculine or knight else "its"
                greeting += f"what's-{pronoun}-name"
        else:
            if name:
                greeting += f"{name}!"
            elif not gender:
                greeting += "friend!"
        for i in range(0, count):
            print(greeting)

The above function receives several keyword arguments that determine how the greeting to output is constructed.
Now, construct the command-line interface to provision it with the same, which is done
in :file:`cli.py`:

.. code-block:: python

    import typer

    from .greet import greet


    app = typer.Typer()
    app.command()(greet)


    if __name__ == "__main__":
        app()

The command-line interface is built with typer_, an easy-to-use CLI parser based on Python type hints. It provides
auto-completion and nicely styled command-line help out of the box. Another option would be :py:mod:`argparse`,
a command-line parser which is included in Python's standard library. It is sufficient for most needs, but requires
a lot of code, usually in ``cli.py``, to function properly. Alternatively, docopt_ makes it possible to create CLI
interfaces based solely on docstrings; advanced users are encouraged to make use of click_ (on which ``typer`` is based).

Now, add an empty :file:`__init__.py` file, to define the project as a regular :term:`import package <Import Package>`.

The file :file:`__main__.py` marks the main entry point for the application when running it via :mod:`runpy`
(i.e. ``python -m greetings``, which works immediately with flat layout, but requires installation of the package with src layout),
so initizalize the command-line interface here:

.. code-block:: python

	if __name__ == "__main__":
	    from greetings.cli import app
	    app()

.. note::

    In order to enable calling the command-line interface directly from the :term:`source tree <Project Source Tree>`,
    i.e. as ``python src/greetings``, a certain hack could be placed in this file; read more at
    :ref:`running-cli-from-source-src-layout`.


``pyproject.toml``
------------------

The project's :term:`metadata <Pyproject Metadata>` is placed in :term:`pyproject.toml`. The :term:`pyproject metadata keys <Pyproject Metadata Key>` and the ``[build-system]`` table may be filled in as described in :ref:`writing-pyproject-toml`, adding a dependency
on ``typer`` (this tutorial uses version *0.12.3*).

For the project to be recognised as a command-line tool, additionally a ``console_scripts`` :ref:`entry point <entry-points>` (see :ref:`console_scripts`) needs to be added as a :term:`subkey <Pyproject Metadata Subkey>`:

.. code-block:: toml

	[project.scripts]
	greet = "greetings.cli:app"

Now, the project's source tree is ready to be transformed into a :term:`distribution package <Distribution Package>`,
which makes it installable.

.. _click: https://click.palletsprojects.com/
.. _docopt: https://docopt.readthedocs.io/en/latest/
.. _typer: https://typer.tiangolo.com/
```

My case deviates from this in that I want to put the CLI app as an extra because my library depnends only on builtin modules while the CLI depends on typer, rich, and shellingham. How can I specify a cli extra for my library and how to structure my folder?

---

To package your project with an optional CLI extra, you can follow these steps:

### 1. Folder Structure

Keep the main library and CLI separated, as follows:

```plaintext
.
├── pyproject.toml
└── src
    └── your_library
        ├── core.py  # Main library code (only standard modules)
        ├── __init__.py
        ├── cli.py  # CLI code (uses typer, rich, etc.)
        └── __main__.py
```

### 2. Define Extras in `pyproject.toml`

In `pyproject.toml`, use `optional-dependencies` to specify dependencies needed for the CLI:

```toml
[project]
name = "your_library"
version = "0.1.0"
description = "A Python library with an optional CLI."
dependencies = []

[project.optional-dependencies]
cli = ["typer", "rich", "shellingham"]

[project.scripts]
your_tool = "your_library.cli:app"  # CLI entry point
```

### Explanation:

- **`[project.optional-dependencies]`**: Defines the `cli` extra that includes `typer`, `rich`, and `shellingham`.
- **`[project.scripts]`**: Registers a CLI entry point (`your_tool`) to the `cli.py` application, available only if the `cli` extra is installed.

### Usage

To install only the library:
```bash
pip install .
```

To install the library with the CLI:
```bash
pip install .[cli]
```

### Additional Considerations

1. **Testing CLI**: Ensure `cli.py` handles cases when dependencies are unavailable.
2. **Readme**: Document the `cli` extra for users

---

Can I do this instead:

```plaintext
.
├── pyproject.toml
└── src
    ├── greet_cli.py # CLI code (uses typer, rich, etc.)
    └── greet.py # Main library code (only standard modules)
```

so that they are considered two different packages and I don't need to handle dependencies unavailability? How would my pyproject.toml look like in this case? If not, how can I handle the dependencies checks?

---

Yes, you can structure your project so that the CLI and library are treated as separate packages. This avoids the need for dependency checks within the code. Here’s how to set up the folder structure and `pyproject.toml`:

### Updated Folder Structure

Separate the library (`greet`) and CLI (`greet_cli`) as independent packages:

```plaintext
.
├── pyproject.toml
└── src
    ├── greet.py       # Main library code (only standard modules)
    └── greet_cli.py   # CLI code (depends on typer, rich, shellingham)
```

### `pyproject.toml` Configuration

In `pyproject.toml`, define `greet` as the main library package and `greet_cli` as a separate CLI package with its own dependencies:

```toml
[project]
name = "greet"
version = "0.1.0"
description = "A Python library with an optional CLI."
dependencies = []

# Optional dependencies for CLI, placed under the 'cli' extra
[project.optional-dependencies]
cli = ["typer", "rich", "shellingham"]

# Define CLI as a separate entry point
[project.scripts]
greet-cli = "greet_cli:app"
```

### Explanation

- **`greet.py`**: Main library, which only depends on standard modules.
- **`greet_cli.py`**: Contains CLI code that depends on external libraries.
- **`cli` extra**: Users can install CLI dependencies with `pip install .[cli]`.

### Installing and Running

To install only the library:
```bash
pip install .
```

To install with CLI support:
```bash
pip install .[cli]
```

With this approach, you avoid dependency issues because `greet_cli.py` is only accessible if the `cli` extra is installed. 

### Alternative: Handling Dependency Checks

If you prefer to have the CLI in the same package, use a `try-except` block in `greet_cli.py` to handle missing dependencies gracefully:

```python
try:
    import typer
    import rich
    import shellingham
except ImportError as e:
    print(f"Required package missing: {e.name}. Install with `pip install greet[cli]`")
    raise SystemExit(1)

# Define your CLI application using the imported modules
app = typer.Typer()

# CLI command functions go here
```

---

Which is more proper, your version or this? 

```python
try:
    import typer
    import rich
    import shellingham
except ImportError as e:
    raise SystemExit(f"Required package missing: {e.name}. Install with `pip install greet[cli]`") from e
```

What is the best option here and how can I pass the retcode? (I don't want to but I am curious)

---

Your version is indeed cleaner and more Pythonic because it leverages the `raise ... from e` syntax, which preserves the original traceback. Here’s a comparison of both approaches with a few considerations:

### Best Option for Dependency Checks

The preferred version is:

```python
try:
    import typer
    import rich
    import shellingham
except ImportError as e:
    raise SystemExit(f"Required package missing: {e.name}. Install with `pip install greet[cli]`") from e
```

### Reasons

- **Conciseness**: Directly raising `SystemExit` with an informative message in a single line is simpler and more readable.
- **Traceback Preservation**: `raise ... from e` keeps the original `ImportError` traceback, which is helpful for debugging in complex setups.
- **Default Exit Code**: `SystemExit` defaults to `1`, which is standard for indicating an error in CLI applications.

### Setting a Custom Return Code

If you need a specific exit code, pass it as the second argument to `SystemExit`:

```python
try:
    import typer
    import rich
    import shellingham
except ImportError as e:
    raise SystemExit(f"Required package missing: {e.name}. Install with `pip install greet[cli]`", 42) from e
```

In this case, `42` would be the return code. However, `1` is generally recommended for error exits to maintain standard conventions unless you have a specific reason for a different code.
