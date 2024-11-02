Masterpiece™  (**Development Status 1 - Planning**)
====================================================

Try to be Nice
--------------

Welcome to **Masterpiece™** - Quite a Piece of Work!

Masterpiece™ is a **Python framework** designed for creating modular, scalable, plugin-aware, multi-threaded, and 
object-oriented applications with a hierarchical structure. If you appreciate these design concepts, look no further; 
you've come to the right place! For universes that are not hierarchical by nature, you might find a different 
framework that suits you better.

Project Status and Current State
--------------------------------

Here’s what is currently available:

* **Package Infrastructure**: The basic Python package setup is finalized and configured with `pyproject.toml`.
* **Classes**: The existing classes have been finalized. 
* **Example Application**: The example application `examples/myhome.py` prints out its instance structure when run. 
  Despite its simplicity, it demonstrates the structure of a typical scalable and fully configurable software.
* **Plugin Project**: A separate plugin project named `masterpiece_plugin` plugs in a "Hello World" greeting to 
  `myhome.py`, demonstrating a minimal yet fully functional plugin.
* **Bug-Free Status**: Absolutely bug-free — just kidding! There are no known bugs remaining, as far as I can tell.

What is currently not available:

* **Threads**: This will be the topic for the next milestone.

Multi-threading in Python might make some developers raise an eyebrow, but I trust the community will address 
that Global Interpreter Lock (GIL) concern.

Goals
-----

Have fun while learning the Python ecosystem! The ultimate enjoyment, with a sprinkling of practicality, will be 
achieved by cranking the Fun-O-Meter™ up to 11. Coding should feel like a rollercoaster ride—minus the screaming 
and the long lines.

* **First-Time Excellence**: We aim to build a framework that's reliable, correct, and efficient from the start, 
  and fun—because what’s a framework without a little joy?
* **Robustness**: A minimal yet robust API providing developers with total control over everything.
* **Productivity**: Totally reusable code to achieve maximum functionality with a minimal amount of code (read: money).

Packages
--------

Masterpiece introduces two Python packages:

1. **Masterpiece (core framework)**:  
   This is the core framework for building plugin-aware, multi-threaded applications. It includes a simple yet 
   fully functional application to help you get started and serves as a plugin-aware reference application 
   that can be scaled up to any size.

2. **Masterpiece Plugin (plugin example)**:  
   This is a basic plugin example that demonstrates how to create third-party plugins for applications built 
   using Masterpiece. It’s as simple as saying **"Hello, World!"**, literally, yet it serves as a representative 
   reference plugin, providing a skeleton for industry-proof applications.

**Note**: This project contains only the core framework. The plugin is provided as a separate project 
`masterpiece_plugin <https://gitlab.com/juham/masterpiece_plugin>`_.

Example Usage
-------------

**Step 1**: Install Masterpiece and run the example application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To install the core framework:

.. code-block:: bash

    pip install masterpiece

Then, navigate to the example folder and run the application:

.. code-block:: bash

    python examples/myhome.py

The application will print out its instance hierarchy. This is a minimal starting point for developing your own 
multi-threaded, plugin-based, scalable applications.

**Example output**:

.. code-block:: text

    home
        ├─ grid
        ├─ downstairs
        │   └─ kitchen
        │       ├─ oven
        │       └─ fridge
        └─ garage
            └─ EV charger

**Step 2**: Install the Masterpiece Plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To extend the application with the **masterpiece_plugin**:

.. code-block:: bash

    pip install masterpiece_plugin

Run the application again:

.. code-block:: bash

    python examples/myhome.py

You'll now see a new object in the instance hierarchy, along with a friendly "Hello, World!" object.

**Example output**:

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

The application also demonstrates the usage of startup arguments:

.. code-block:: text

    examples/myhome.py --init --solar 10 --color red

- The ``--init`` argument tells the application to create configuration files for all classes in the application.
- The ``--solar`` argument creates an instance of a solar power plant with a specified peak power of 10 kW.
- The ``--color`` argument can be used for setting the color for the tree diagram.

The above class properties (and many more) can also be defined in the class configuration files. By default, 
the configuration files are created in the ``~/.myhome/config`` folder, as determined by the ``application id`` 
and ``--config [anyname]``.

For example, ``--config simulation`` will use the configuration files stored in the ``~/.myhome/simulation/`` 
folder.

Contributing
------------

Please check out the `Issue Board <https://gitlab.com/juham/masterpiece/-/boards>`_ for tracking progress 
and tasks.

About the Project
-----------------

The framework is essentially a tree container, allowing any payload to be integrated into its hierarchy. It 
supports configuration, serialization, the factory method pattern, a plugin API, and many other features for 
every object in its hierarchy. Generic tree traversal functionality allows any interaction to be applied to the 
tree, from serialization to any application-specific functionality.

Just like life on Earth, all components of this framework trace their lineage back to a single ancestor: the 
'Masterpiece' core. Evolution, but in code! (Okay, this might be a bit too deep...)

The name 'Masterpiece' was chosen to reflect a commitment to fine-grained modular design, with a touch of humor.

Developer Documentation
-----------------------

As a C/C++ boomer, Doxygen was naturally my tool of choice. However, I ditched it in favor of Python's native 
tool, Sphinx. The migration wasn’t exactly pure joy—I encountered severe management problems along the way—but 
it's all good now. The documentation still looks like a piece of work, but it's improving.

For full documentation and usage details, see the full documentation at `Documentation Index <docs/build/html/index.html>`_ 
(The docs may look rough; I’m still unraveling Sphinx's mysteries).

Special Thanks
--------------

Big thanks to the generous support of [Mahi.fi](https://mahi.fi) for helping bring this framework to life.
