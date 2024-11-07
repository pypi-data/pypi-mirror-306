![Logo Rougail](logo.png "logo rougail")

# Rougail

## Description

Rougail is a free full-featured configuration manager library written in python3.

The configuration is describe in YAML dictionary files.

Those dictionaries are converted into [Tiramisu](https://framagit.org/tiramisu/tiramisu) objects.

Rougail can be incorporated with other technologies and stacks regardless of whether they’re written in Python or not.

## Simple example

Create a directory:

```bash
# mkdir dict
```

## Dictionary

A dictionary is a variables description file.

Create the file `dict/dictionary.yml`:

```yml
---
version: 1.1
# describe a variable my_first_variable
# and a family with a variable my_second_variable
my_first_variable: my_value
my_family:
  my_second_variable: 1
```

## Generate variable

### With commandline:

```bash
# rougail -m dict
Variables:
┣━━ 📓 my_first_variable: my_value
┗━━ 📂 my_family
    ┗━━ 📓 my_second_variable: 1

```

### With default value:

Here is a python3 example file:

```python
from rougail import Rougail, RougailConfig
from pprint import pprint

RougailConfig['dictionaries_dir'] = ['dict']
rougail = Rougail()
config = rougail.run()
pprint(config.value.get(), sort_dicts=False)
```

The result is:

```json
{<TiramisuOption path="rougail">: {<TiramisuOption path="rougail.my_first_variable">: 'my_value',
                                   <TiramisuOption path="rougail.my_family">: {<TiramisuOption path="rougail.my_family.my_second_variable">: 1}}}
```

### With modified value


Use [Tiramisu](https://framagit.org/tiramisu/tiramisu) API to change values:

```python
from rougail import Rougail, RougailConfig
from pprint import pprint

RougailConfig['dictionaries_dir'] = ['dict']
rougail = Rougail()
config = rougail.get_config()
config.option('rougail.my_first_variable').value.set('modified_value')
config.option('rougail.my_family.my_second_variable').value.set(2)
pprint(config.value.get(), sort_dicts=False)
```

The destination file is generated with new values:

```json
{<TiramisuOption path="rougail">: {<TiramisuOption path="rougail.my_first_variable">: 'modified_value',
                                   <TiramisuOption path="rougail.my_family">: {<TiramisuOption path="rougail.my_family.my_second_variable">: 2}}}
```

# Link

* [Documentation](https://rougail.readthedocs.io/en/latest/)
* [Licence ](LICENSE)

# Related projects

* [Tiramisu](https://forge.cloud.silique.fr/gnunux/tiramisu)
* [Risotto](https://cloud.silique.fr/gitea/risotto/risotto)
