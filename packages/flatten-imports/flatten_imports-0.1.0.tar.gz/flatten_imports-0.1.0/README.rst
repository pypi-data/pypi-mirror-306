.. code-block:: bash

   echo 'from x import a, b, c' | flatten-imports | black-macchiato


.. code-block:: bash

   from x import a
   from x import b
   from x import c



Flattening your imports is helpful:

- reducing the risk of merge conflicts
- making it easier to see what imports are used
- more linter friendly (linter errors are easier to see on a line basis)


Quick Start
-----------

.. code-block:: bash

   pip install flatten-imports
