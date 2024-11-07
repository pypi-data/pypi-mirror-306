======================================
Create it's own option
======================================

Generic regexp option: :class:`RegexpOption`
====================================================

Use `RegexpOption` to create custom option is very simple.

You just have to create an object that inherits from `RegexpOption` and that has the following class attributes:

- __slots__: with new data members (the values should always be `tuple()`)
- _type = with a name
- _regexp: with a compiled regexp

Here an example to an option that only accept string with on lowercase ASCII vowel characters:

.. literalinclude:: src/own_option.py
   :lines: 3-10
   :linenos:

Let's try our object:

>>> VowelOption('vowel', 'Vowel', 'aae')
<VowelOption object at 0x7feb2779c050>
>>> try:
...     VowelOption('vowel', 'Vowel', 'oooups')
... except ValueError as err:
...     print(err)
... 
"oooups" is an invalid string with vowel for "Vowel"

Create your own option
=================================

An option always inherits from `Option` object. This object has the following class attributes:

- __slots__: with new data members (the values should always be `tuple()`)
- _type = with a name

Here an example to a lipogram option:

.. literalinclude:: src/own_option2.py
   :lines: 3-12
   :linenos:

First of all we want to add a custom parameter to ask the minimum length (`min_len`) of the value:

.. literalinclude:: src/own_option2.py
   :lines: 13-17
   :linenos:

We have a first validation method. In this method, we verify that the value is a string and that there is no "e" on it:

.. literalinclude:: src/own_option2.py
   :lines: 19-26
   :linenos:

Even if user set warnings_only attribute, this method will raise.

Finally we add a method to valid the value length. If `warnings_only` is set to True, a warning will be emit:

.. literalinclude:: src/own_option2.py
   :lines: 28-40
   :linenos:

Let's test it:

1. the character "e" is in the value:

>>> try:
...    LipogramOption('lipo',
...                   'Lipogram',
...                   'I just want to add a quality string that has no bad characters')
... except ValueError as err:
...    print(err)
...
"I just want to add a quality string that has no bad characters" is an invalid lipogram for "Lipogram", Perec wrote a book without any "e", you could not do it in a simple sentence?

2. the character "e" is in the value and warnings_only is set to True:

>>> try:
...     LipogramOption('lipo',
...                    'Lipogram',
...                    'I just want to add a quality string that has no bad characters',
...                    warnings_only=True)
... except ValueError as err:
...     print(err)
...
"I just want to add a quality string that has no bad characters" is an invalid lipogram for "Lipogram", Perec wrote a book without any "e", you could not do it in a simple sentence?

3. the value is too short

>>> try:
...     LipogramOption('lipo',
...                    'Lipogram',
...                    'I just want to add a quality string that has no bad symbols')
... except ValueError as err:
...     print(err)
...
"I just want to add a quality string that has no bad symbols" is an invalid lipogram for "Lipogram", you must have at least 100 characters in the sentence

4. the value is too short and warnings_only is set to True:

>>> warnings.simplefilter('always', ValueWarning)
>>> with warnings.catch_warnings(record=True) as warn:
...    LipogramOption('lipo',
...                   'Lipogram',
...                   'I just want to add a quality string that has no bad symbols',
...                   warnings_only=True)
...    if warn:
...        print(warn[0].message)
...
attention, "I just want to add a quality string that has no bad symbols" could be an invalid lipogram for "Lipogram", it would be better to have at least 100 characters in the sentence

5. set minimum length to 50 characters, the value is valid:

>>> LipogramOption('lipo',
...                'Lipogram',
...                'I just want to add a quality string that has no bad symbols',
...                min_len=50)


