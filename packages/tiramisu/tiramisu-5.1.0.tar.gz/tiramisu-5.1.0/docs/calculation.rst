==================================
Calculation
==================================

Calculation is a generic object that allow you to call an external function.

Simple calculation
==================================

It's structure is the following :

.. literalinclude:: src/calculation.py
   :lines: 1-5
   :linenos:

Positional and keyword arguments
=========================================

Function's arguments are also specified in this object.
Let's see with a positional argument and a keyword argument:

.. literalinclude:: src/calculation.py
   :lines: 8-10
   :linenos:

The function `a_function_with_parameters` will be call with the positional argument `value1` to `my value 1` and the keyword argument `value2` to `my value 2`.
So when this function will be executed, it will return `my value 1 my value 2`.

Let's see with two positional arguments:

.. literalinclude:: src/calculation.py
   :lines: 13-15
   :linenos:

As we have several positional arguments, the first Params' argument is a tuple.
This example will return strictly same result has previous example. 

Option has an argument
=========================================

In previous examples, we use ParamValue arguments, which could contain random value. But this value is static and cannot be change.

It could be interesting to use an existant option has an argument:

.. literalinclude:: src/calculation.py
   :lines: 18-21
   :linenos:

As long as option1 is at its default value, the function will return `1`. If we set option1 to `12`, the function will return `12`.

Pay attention to the properties when you use an option.
This example will raise a ConfigError:

.. literalinclude:: src/calculation.py
   :lines: 24-27
   :linenos:

It's up to you to define the desired behavior.

If you want the option to be transitively disabled just set the raisepropertyerror argument to True:

.. literalinclude:: src/calculation.py
   :lines: 29-31
   :linenos:

If you want to remove option in argument, just set the notraisepropertyerror argument to True:

.. literalinclude:: src/calculation.py
   :lines: 33-35
   :linenos:

In this case, option1 will not pass to function. You have to set a default value to this argument.
So, function will return `None`.

In these examples, the function only accesses to the value of the option. But no additional information is given.
It is possible to add the parameter `todict` to `True` to have the description of the option in addition to its value.

.. literalinclude:: src/calculation.py
   :lines: 37-39
   :linenos:

This function will return `the option first option has value 1`.

Multi option has an argument
=========================================

An option could be a multi. Here is an example:

.. literalinclude:: src/calculation.py
   :lines: 46-49
   :linenos:

In this case the function will return the complete list. So `[1]` in this example.

Leader or follower option has an argument
============================================

An option could be a leader:

.. literalinclude:: src/calculation.py
   :lines: 51-57
   :linenos:

If the calculation is used in a standard multi, it will return `[1]`.
If the calculation is used in a follower, it will return `1`.

An option could be a follower:

.. literalinclude:: src/calculation.py
   :lines: 59-65
   :linenos:

If the calculation is used in a standard multi, it will return `[2]`.
If the calculation is used in a follower, it will return `2`.

If the calculation is used in a follower we can also retrieve the actual follower index:

.. literalinclude:: src/calculation.py
   :lines: 67-73
   :linenos:

Context has an argument
=========================================

It is possible to recover a copy of the context directly in a function. On the other hand, the use of the context in a function is a slow action which will haunt the performances. Use it only in case of necessity:

.. literalinclude:: src/calculation.py
   :lines: 42-44
   :linenos:
