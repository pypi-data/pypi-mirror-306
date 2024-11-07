==================================
Validator
==================================

What are validator?
==================================

Validator is a functionnality that allow you to call a function to determine if an option is valid.

To define validator we have to use :doc:`calculation` object.
The function have to raise a `ValueError` object if the value is not valid. It could emit a warning when raises a `ValueWarning`.

Validator with options
=============================

Here an example, where we want to ask a new password to an user. This password should not be weak. The password will be asked twice and must match.

First of all, import necessary object:

.. literalinclude:: src/validator.py
   :lines: 3-7
   :linenos:

Create a first function to valid that the password is not weak:

.. literalinclude:: src/validator.py
   :lines: 10-14
   :linenos:

Secondly create a function to valid password length. The password must be longer than the value of `min_len` and should be longer than the value of `recommand_len`.

In first case, function raise `ValueError`, this value is incorrect.

In second case, function raise `ValueWarning`, the value is valid but discouraged:

.. literalinclude:: src/validator.py
   :lines: 17-23
   :linenos:

Thirdly create a function that verify that the login name is not a part of password (password `foo2aZ$` if not valid for user `foo`):

.. literalinclude:: src/validator.py
   :lines: 26-28
   :linenos:

Now we can creation an option to ask user login:

.. literalinclude:: src/validator.py
   :lines: 36-37
   :linenos:

Create a calculation to launch `is_password_conform`. This function will be use in a new option and must validate this new option. So we use the object `ParamSelfOption` has parameter to retrieve the value of current option:

.. literalinclude:: src/validator.py
   :lines: 39-41
   :linenos:

Create a second calculation to launch `password_correct_len` function. We want set 8 as `min_len` value and 12 as `recommand_len` value:

.. literalinclude:: src/validator.py
   :lines: 43-46
   :linenos:

Create a third calculation to launch `user_not_in_password` function. For this function, we use keyword argument. This function normaly raise `ValueError` but in this case we want demoting this error as a simple warning. So we add `warnings_only` parameter:

.. literalinclude:: src/validator.py
   :lines: 48-51
   :linenos:

So now we can create first password option that use those calculations:

.. literalinclude:: src/validator.py
   :lines: 54-58
   :linenos:

A new function is created to conform that password1 and password2 match:

.. literalinclude:: src/validator.py
   :lines: 31-33
   :linenos:

And now we can create second password option that use this function:

.. literalinclude:: src/validator.py
   :lines: 60-64
   :linenos:

Finally we create optiondescription and config:

.. literalinclude:: src/validator.py
   :lines: 66-70
   :linenos:

Now we can test this `Config`:

.. literalinclude:: src/validator.py
   :lines: 72-77
   :linenos:

The tested password is too weak, so value is not set.
The error is: `Error: "aAbBc" is an invalid string for "Password", please choose a stronger password, try a mix of letters, numbers and symbols`.

The password is part of error message. In this case it's a bad idea. So we have to remove `prefix` to the error message:

.. literalinclude:: src/validator.py
   :lines: 79-85
   :linenos:

Now the error is: `Error: please choose a stronger password, try a mix of letters, numbers and symbols`.

Let's try with a password not weak but too short:

.. literalinclude:: src/validator.py
   :lines: 87-93
   :linenos:

The error is: `Error: use 8 characters or more for your password`.

Now try a password with 8 characters:

.. literalinclude:: src/validator.py
   :lines: 95-104
   :linenos:

Warning is display but password is store:

`Warning: it would be better to use more than 12 characters for your password`

`The password is "aZ$1bN:2"`

Try a password with the login as part of it:

.. literalinclude:: src/validator.py
   :lines: 106-115
   :linenos:

Warning is display but password is store:
`Warning: the login must not be part of the password`
`The password is "aZ$1bN:2u@1Bjuser"`

Now try with a valid password but that doesn't match:

.. literalinclude:: src/validator.py
   :lines: 117-124
   :linenos:

An error is displayed: `Error: those passwords didn't match, try again`.

Finally try a valid password:

.. literalinclude:: src/validator.py
   :lines: 126-133
   :linenos:

As expected, we have `The password for "user" is "aZ$1bN:2u@1Bj"`.

Validator with a multi option
================================

Assume we ask percentage value to an user. The sum of values mustn't be higher than 100% and shouldn't be lower than 100%.

Let's start by importing the objects:

.. literalinclude:: src/validator_multi.py
   :lines: 1-4
   :linenos:

Continue by writing the validation function:

.. literalinclude:: src/validator_multi.py
   :lines: 7-12
   :linenos:

And create a simple config:

.. literalinclude:: src/validator_multi.py
   :lines: 15-19
   :linenos:

Now try with bigger sum:

.. literalinclude:: src/validator_multi.py
   :lines: 22-29
   :linenos:

The result is:

`Error: the total 110% is bigger than 100%`

`The value is "[]"`

Let's try with lower sum:

.. literalinclude:: src/validator_multi.py
   :lines: 31-39
   :linenos:

The result is:

`Warning: the total 90% is lower than 100%`

`The value is "[20, 70]"`

Finally with correct value:

.. literalinclude:: src/validator_multi.py
   :lines: 41-44
   :linenos:

The result is:

`The value is "[20, 80]"`

Validator with a follower option
==================================

Assume we want distribute something to differents users. The sum of values mustn't be higher than 100%.

First, import all needed objects:

.. literalinclude:: src/validator_follower.py
   :lines: 1-4
   :linenos:

Let's start to write a function with three arguments:

- the first argument will have all values set for the follower
- the second argument will have only last value set for the follower
- the third argument will have the index

.. literalinclude:: src/validator_follower.py
   :lines: 7-12
   :linenos:

Continue by creating a calculation:

.. literalinclude:: src/validator_follower.py
   :lines: 15-17
   :linenos:

And instanciate differents option and config:

.. literalinclude:: src/validator_follower.py
   :lines: 20-26
   :linenos:

Add two value to the leader:

.. literalinclude:: src/validator_follower.py
   :lines: 29
   :linenos:

The user user1 will have 20%:

.. literalinclude:: src/validator_follower.py
   :lines: 30
   :linenos:

If we try to set 90% to user2:

.. literalinclude:: src/validator_follower.py
   :lines: 33-38
   :linenos:

This error occured: `Error: the value 90 (at index 1) is too big, the total is 110%`

No problem with 80%:

.. literalinclude:: src/validator_follower.py
   :lines: 40-41
   :linenos:
