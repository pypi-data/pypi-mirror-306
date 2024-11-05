Mastering the Piece
===================

This tutorial covers the ``examples/myapp.py`` application to help you get
started with writing world-class masterpieces.

Prerequisites
-------------


Fetch the Masterpiece core framework and the plugin:

.. code-block:: bash

    git clone https://gitlab.com/juham/masterpiece.git
    git clone https://gitlab.com/juham/masterpiece_plugin.git

Navigate to the `masterpiece/example` folder and open the example
application in your favorite editor (Emacs, anyone?):

.. code-block:: bash

    emacs examples/myhome.py

Importing Masterpiece Classes
-----------------------------

The first lines of code import the classes used as building blocks in
`myapp.py`.

.. code-block:: python

    from masterpiece import Application, MasterPiece, Composite, TreeVisualizer

Notice what is **not** imported: the `masterpiece_plugin`. Masterpiece plugins
"know" their applications rather than the other way around.

Factory Method Pattern
----------------------

The framework supports the "factory method pattern" — a class identifier-based
instantiation. All imported classes are automatically registered, meaning they
can be instantiated as follows:

.. code-block:: python

    # myapp = MyApp()
    myapp = cls.instantiate('MyApp')

This approach decouples implementation from the interface!

Tip: The factory method pattern is one of the most important patterns for
creating scalable and reusable software. Classes can be replaced with
different implementations via configuration, allowing plugins to be written
and plugged in without modifying existing (tested) code.

Application Identifier
^^^^^^^^^^^^^^^^^^^^^^

The main function initializes the application with an appropriate
"application identifier," a string that describes the software's purpose.

.. code-block:: python

   def main() -> None:
       MyHome.init_app_id("myhome")

This identifier determines where the application reads its configuration
(files and registry settings) and enables plugins to be written for
applications.

Note: The application identifier is **not** the application name! It’s
something shared by all related applications, for example, representing a
software "family" or company if multiple applications share the same
architecture.

Loading Plugins
^^^^^^^^^^^^^^^

If desired, load plugins with:

.. code-block:: python

    MyHome.load_plugins()

The plugin discovery uses Python's `importlib.metadata` API. Every Masterpiece
project can define project entry points in its `pyproject.toml` file:

.. code-block:: python

    [project.entry-points."masterpiece.plugins"]

Then, a plugin can define its entry points in `pyproject.toml` as well:

.. code-block:: python

    helloworld_plugin = "masterpiece_plugin:HelloWorld"

This example shows that the `masterpiece_plugin` was written for any
Masterpiece application, relying only on core Masterpiece framework features.

Applications should (in fact, **must**) introduce application-specific
entry points to allow plugins tailored to them.

Configuring Application
^^^^^^^^^^^^^^^^^^^^^^^

Application configuration involves setting class attributes, done either
through class-specific configuration files or startup arguments, and loaded
with:

.. code-block:: python

    Application.load_configuration()

Configuration files are found in:

.. code-block:: bash

    ~/.[app_id]/[configuration]/[classname].[ext]

where `[app_id]` is the application identifier. `[configuration]` is `config`
by default but can be changed with the `--config` startup switch, allowing
different configurations (e.g., production vs. test).

Each class has a configuration file (`[classname]`) with format-specific
extension (`[ext]`), usually `JSON`. YAML is also supported, and plugins can
introduce more formats. Select the desired one with:

.. code-block:: bash

    python myapp.py --application_serialization_format 'YamlFormat'

This demonstrates the factory method pattern, where implementations are
chosen through configuration.

If there are no configuration files, the application can generate default ones
with:

.. code-block:: bash

    python myapp.py --init

This creates a new set of configuration files at `~/.myapp/config/`, using
default values.

Creating the Application
^^^^^^^^^^^^^^^^^^^^^^^^

Once classes have the desired properties, the main function can instantiate
them:

.. code-block:: python

    home = MyHome("home")

This creates a `MyHome` application instance named "home".

Serialization
^^^^^^^^^^^^^

Class configuration files and startup arguments control the initial
properties of objects created, but those properties become run-time data
after creation.

This run-time data, represented by instance attributes, can be saved and
restored later through "serialization" and "deserialization".

To initialize from a serialization file specified via
`--application_serialization_file [anyfile].[ext]`:

.. code-block:: python

    # Reconstruct the application from the given serialization file
    home.deserialize()

The last operation when the application shuts down could be:

.. code-block:: python

    # Save the current application state to file
    home.serialize()

This enables applications to be restarted later in the state they were
when closed.

Running the Application
^^^^^^^^^^^^^^^^^^^^^^^

Applications perform operations in the `run()` method.

.. code-block:: python

    home.run()

For example, `myapp.py` prints out the instances in the application:

.. code-block:: text

    home
        ├─ grid
        ├─ downstairs
        │   └─ kitchen
        │       ├─ oven
        │       └─ fridge
        ├─ garage
        │   └─ EV charger
        └─ Hello World - A Plugin

The Application Class
^^^^^^^^^^^^^^^^^^^^^

Masterpiece is object-oriented, meaning that components should be proper
classes. For instance, `MyApp`:

.. code-block:: python

    class MyApp(Application):
        # class attributes
        solar: float = 0.0
        color: str = "yellow"

        def __init__(self, name: str = "myhome") -> None:
            super().__init__(name)
            # instance attributes
            self.create_home()
            self.install_plugins()

    [snip]

`MyHome` inherits from `Application`, gaining features like plugin support,
class attribute configuration, serialization, and startup argument handling.

Configure public class attributes (`solar` and `color`) via the
`~/.myhome/config/MyApp.json` file:

.. code-block:: text

    {
        "solar": 10.0,
        "color": "yellow"
    }

or via startup arguments:

.. code-block:: bash

    myhome --myapp_solar 20 --myapp_color "red"

Configuration priority:

1. Startup arguments, if defined
2. Configuration files, if present
3. Hard-coded values

Modeling Reality
^^^^^^^^^^^^^^^^

Real-world objects are hierarchical. The Masterpiece framework models this
with the `Composite` class, allowing `MasterPiece` or `Composite` objects to
be added as children. Application classes can also be a `Composite`.

Methods like `create_power_grid()` demonstrate this:

.. code-block:: python

    def create_power_grid(self):
        grid = MasterPiece("grid")
        self.add(grid)

The method inserts 'grid' object into the application as a children.

This creates an "ownership tree," where the application can robustly manage resources
and serialize the hierarchy.

Visualizing the Hierarchy
^^^^^^^^^^^^^^^^^^^^^^^^^

The `run()` method has two parts:

.. code-block:: python

    def run(self) -> None:
        super().run()
        self.print()

    def print(self):
        visualizer = TreeVisualizer(self.color)
        visualizer.print_tree(self)

This demonstrates inheritance: applications can derive from `MyApp` to
customize features.

The `print()` method uses the `TreeVisualizer` class to traverse and display
the instance hierarchy:

.. code-block:: python

    def visualize_node(node: MasterPiece, context: TreeVisualizer) -> bool:
        # visualize the node
       [snip]

    visualizer = TreeVisualizer(self.color)
    self.do(visualize_node, visualizer)


    
Payload Objects
^^^^^^^^^^^^^^^

Each Masterpiece class, including applications, can host "payload"
objects. Payload objects, if subclasses of `MasterPiece`, are serialized and
handled automatically.

Always pass `run()` to the superclass:

.. code-block:: python

    def run(self) -> None:
        super().run()  # important
        self.print()

even if payloads aren’t used in this first tutorial.


Implementing Plugins
^^^^^^^^^^^^^^^^^^^^

Another important feature we haven't touched much in this first tutorial is **plugins**.

The framework encourages focusing on **plugins** rather than traditional
applications. Applications should implement only the minimal infrastructure
required, leaving features to be handled as plugins.

Each feature should be implemented as an independent plugin, which can be
installed or uninstalled as needed.

A well-designed plugin should be self-contained, adding a specific feature to
the application. If you install the plugin, the application gains that feature.
Uninstalling it should leave no trace of the feature within the application.

For example, a plugin that adds a new serialization format, like `XmlFormat`,
can be installed to make the format available:

.. code-block:: bash

   anyapp --application_serialization_format XmlFormat

The next tutorial covers this topic in depth:
`Implementing Plugins <docs/source/plugintutorial.rst>`_
