==================================
Bonus: Let's create a quiz!
==================================

Creating our quiz
==================================

Of course Tiramisu is great to handle options, but here's a little thing you can
do if you're just bored and don't know what to do.

So, let's create a quiz.

First, as always, let's import everything we need from Tiramisu and create our options:

.. literalinclude:: src/quiz.py
   :lines: 1-6
   :linenos:

We make a dictionary with all questions, proposals and answer:

.. literalinclude:: src/quiz.py
   :lines: 20-35
   :linenos:

Now build our Config.

We have to create question option.

Just after, we're going to define the correct answer in a second option.

The answer is frozen so that when it is set, it cannot change.

And finally a last option that will verify if the answer is correct.

 .. literalinclude:: src/quiz.py
   :lines: 38-59
   :linenos:

The `verif` option will us a function that will verify if the answer given by the user
(which will become the value of `question`) is the same as the correct answer (which is the value
of `answer`). Here is this function (of course you have to declare at the begining of your code,
before your options) :

.. literalinclude:: src/quiz.py
   :lines: 12-13
   :linenos:

Pretty simple.

At least we're done with our questions. Let's just create one last option.
This option calculate the result of the students' answers:

.. literalinclude:: src/quiz.py
   :lines: 16-17, 62-65
   :linenos:

Now we just have to create our OptionDescription and Config (well it's a MetaConfig
here, but we'll see this later)...

.. literalinclude:: src/quiz.py
   :lines: 66, 9, 67
   :linenos:

... and add some loops to run our quiz!

.. literalinclude:: src/quiz.py
   :lines: 70-104
   :linenos:

Display results for teacher:

.. literalinclude:: src/quiz.py
   :lines: 107-117
   :linenos:


Now let's play !

.. literalinclude:: src/quiz.py
   :lines: 120-132

Download the :download:`full code <src/quiz.py>`

Hey, that was easy ! Almost like I already knew the answers... Oh wait...

Get players results
==================================

Now that you have your quiz, you can play with friends! And what's better than playing
with friends? Crushing them by comparing your scores of course!
You may have noticed that the previous code had some storage instructions. Now we can
create a score board that will give each player's latest score with their errors !

We created a meta config that will be used as a base for all configs we will create :
each time a new player name will be entered, a new config will be created, with the new player's
name as it's session id. This way, we can see every player's result !

So, earlier, we created a MetaConfig, and set the storage on sqlite3, so our data will
not be deleted after the quiz stops to run.

Let's run the script:

  | Who are you? (a student | a teacher): a student
  | Enter a name: my name
  | Question 1: what does the cat say?
  | woof | meow
  | Your answer: meow
  | Correct answer!
  | 
  | Question 2: what do you get by mixing blue and yellow?
  | green | red | purple
  | Your answer: green
  | Correct answer!
  | 
  | Question 3: where is Bryan?
  | at school | in his bedroom | in the kitchen
  | Your answer: at school
  | Wrong answer... the correct answer was: in the kitchen
  | 
  | Question 4: which one has 4 legs and 2 wings?
  | a wyvern | a dragon | a wyrm | a drake
  | Your answer: a dragon
  | Correct answer!
  | 
  | Question 5: why life?
  | because | I don't know | good question
  | Your answer: good question
  | Correct answer!
  | 
  | Correct answers: 4 out of 5

When the quiz runs, we will create a new Config in our MetaConfig:

 .. literalinclude:: src/quiz.py
   :lines: 70-75
   :linenos:
   :emphasize-lines: 3

All results are store in this config (so in the database). So we need to reload those previous config:

 .. literalinclude:: src/quiz.py
   :lines: 120-124
   :linenos:
   :emphasize-lines: 4

Later, a teacher ca display all those score:

  | Who are you? (a student | a teacher): a teacher
  | ==================== my name ==========================
  | Question 1: correct answer
  | Question 2: correct answer
  | Question 3: wrong answer: at school
  | Question 4: correct answer
  | Question 5: correct answer
  | my name's score: 4 out of 5

You've got everything now, so it's your turn to create your own questions and play with
your friends !
