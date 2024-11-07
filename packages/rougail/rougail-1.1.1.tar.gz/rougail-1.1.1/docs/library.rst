`Rougail`'s library description
=================================

Rougail is a configuration management library that allows you to load variables in a simple and convenient way.

In the following examples, we will use a specific configuration of Rougail.
You will find all the configuraiton options in :doc:`configuration`.

To load the configuration you must import the `RougailConfig` class and set the `dictionaries_dir` values:

.. code-block:: python

    from rougail import RougailConfig

    RougailConfig['dictionaries_dir'] = ['dict']

Let's convert a dictionary
-----------------------------

As a reminder, a :term:`dictionary` is a set of instructions that will allow us to create :term:`families` and :term:`variables`.

Let's start by creating a simple dictionary.

Here is a first :file:`dict/00-base.yml` dictionary:

.. code-block:: yaml

    ---
    version: '1.1'
    my_variable:
      default: my_value

Then, let's create the :term:`Tiramisu` objects via the following script:

.. code-block:: python
    :caption: the `script.py` file content

    from rougail import Rougail, RougailConfig

    RougailConfig['dictionaries_dir'] = ['dict']
    rougail = Rougail()
    config = rougail.get_config()
    print(config.value.get())

Let's execute `script.py`:

.. code-block:: bash

    $ python3 script.py
    {'rougail.my_variable': 'my_value'}

Let's convert an extra dictionary
-------------------------------------

.. index:: extras

The default namespace for variables and families is `rougail`. It is possible to define other namespaces. These additional namespaces are called `extras`.

.. FIXME: faire une page pour les extras

Additional namespaces are defined during configuration.

For example, here's how to add an `example` namespace:

.. code-block:: python

    RougailConfig['extra_dictionaries']['example'] = ['extras/']

Then let's create an extra :term:`dictionary` :file:`extras/00-base.yml`:

.. code-block:: yaml
   :caption: the :file:`extras/00-base.yml` file content
    ---
    version: '1.1'
    my_variable_extra:
      default: my_value_extra

Then, let's create the :term:`Tiramisu` objects via the following :file:`script.py` script:

.. code-block:: python
    :caption: the :file:`script.py` file content

    from rougail import Rougail, RougailConfig

    RougailConfig['dictionaries_dir'] = ['dict']
    RougailConfig['extra_dictionaries']['example'] = ['extras/']
    rougail = Rougail()
    config = rougail.get_config()
    print(config.value.dict())

Let's execute `script.py`:

.. code-block:: bash

    $ python3 script.py
    {'rougail.my_variable': 'my_value', 'example.my_variable_extra': 'my_value_extra'}

Let's create a custom function
----------------------------------

We create the complementary :term:`dictionary` named :file:`dict/01-function.yml` so that the  `my_variable_jinja` variable is :term:`calculated`:

.. code-block:: yaml

    ---
    version: '1.1'
    my_variable_jinja:
      type: "string"
      default:
        type: jinja
        jinja: "{{ return_no() }}"

Then let's define the :func:`return_no` function in :file:`functions.py`:

.. code-block:: python
   :caption: the :file:`functions.py` content

   def return_no():
       return 'no'

Then, let's create the :term:`Tiramisu` objects via the following script:

.. code-block:: python
    :caption: the `script.py` file content

    from rougail import Rougail, RougailConfig

    RougailConfig['dictionaries_dir'] = ['dict']
    RougailConfig['extra_dictionaries']['example'] = ['extras/']
    RougailConfig['functions_file'] = 'functions.py'
    rougail = Rougail()
    config = rougail.get_config()
    print(config.value.dict())

Let's execute `script.py`:

.. code-block:: bash

    $ python3 script.py
    {'rougail.my_variable': 'my_value', 'rougail.my_variable_jinja': 'no', 'example.my_variable_extra': 'my_value_extra'}

The value of the `my_variable_extra` variable is calculated, and it's value comes from the :func:`return_no` function.

Create your own type
----------------------

A variable has a type. This type enables the variable to define the values that are accepted by this variable.

There is a series of default types, but obviously not all cases are taken.

It's possible to create your own type.

Here an example to a lipogram option (in a string, we cannot use "e" character):

.. code-block:: python
    :caption: the `lipogram.py` file content

    from tiramisu import StrOption
    class LipogramOption(StrOption):
        __slots__ = tuple()
        _type = 'lipogram'

        def validate(self,
                     value):
            super().validate(value)
            # verify that there is any 'e' in the sentense
            if 'e' in value:
                raise ValueError('Perec wrote a book without any "e", you could not do it in a simple sentence?')

To add the new lipogram type in Rougail:

.. code-block:: python
    >>> from rougail import Rougail, RougailConfig
    >>> RougailConfig['dictionaries_dir'] = ['dict']
    >>> RougailConfig['custom_types']['lipogram'] = LipogramOption

Now, we can use lipogram type.
Here is a :file:`dict/00-base.yml` dictionary:

.. code-block:: yaml
    ---
    version: '1.1'
    var:
      type: lipogram

.. code-block:: python
    >>> rougail = Rougail()
    >>> config = rougail.get_config()
    >>> config.option('rougail.var').value.set('blah')
    >>> config.option('rougail.var').value.set('I just want to add a quality string that has no bad characters')
    [...]
    tiramisu.error.ValueOptionError: "I just want to add a quality string that has no bad characters" is an invalid lipogram for "var", Perec wrote a book without any "e", you could not do it in a simple sentence?

Upgrade dictionnaries to upper version
----------------------------------------

All dictionnaries has a format version number.
When a new format version is proposed, it is possible to automatically convert the files to the new version.

We create a term:`dictionary` named :file:`dict/01-upgrade.yml` with version 1.0:

.. code-block:: yaml

    ---
    version: '1.1'
    my_variable:
      multi: true
    my_dyn_family:
      type: "dynamic"
      variable: my_variable
      a_variable:


.. code-block:: python
    >>> from rougail import RougailUpgrade, RougailConfig
    >>> RougailConfig['dictionaries_dir'] = ['dict']
    >>> upgrade = RougailUpgrade()
    >>> upgrade.load_dictionaries('dict_converted')

The term:`dictionary` named :file:`dict_converted/01-upgrade.yml` is in version 1.1:

.. code-block:: yaml

   version: '1.1'
   my_variable:
     multi: true
   my_dyn_family:
     type: dynamic
     a_variable: null
     dynamic:
       type: variable
       variable: my_variable
       propertyerror: false
