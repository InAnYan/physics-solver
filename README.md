# Physics word problem solver

## The task

Develop a program that solves physics problems stated in natural language.
The program should provide a structured solution that is correct and precise.

## Modeling

1. Transform the source text into problem representation.

There are three main types of physics problems in text books:

- Theoretical: `Why we do not observe the daily rotation of the earth in everyday life?`.
- Converting the value in one measure unit to another.
  `The car is traveling at a speed of 108 kilometers per hour. Represent this speed in meters per second.`.
- Comparing two physical values.
  `Which speed is bigger: 10 meters per second or 10 kilometers per hour?`.
- Comparing some physics value relative to the change of other value.
  `How would the time change if the speed is changed by factor of 2?`.
  (BAD EXAMPLE. TODO: FIND EXAMPLE)
- Problems of finding some physics value.
  `The car drove for 40 minutes at a speed of 144 kilometers per hour. How far did the car travel?`

Values:

3 operations on units:

- Simplification: kg*m/m = kg
- Deduction (?): kg*m/c^-2 = N
- Reduction (?): g -> k

Each arithmetic operation guarantees that the result is: simplified, deduced and reduced.

## Results

### Limitation

1. Static problems. That do not involve changing of something. Like motion.
   `The boy let go of the ball at a height of 1.5 m, and when the ball bounced
   off the floor, he caught it at a height of 1 м. How far did the ball travel?
   At what distance from the the ball was caught?`
   (TODO: CHECK THE CORRECTNESS OF TRANSLATION)
2. Problems where we should draw something.
3. Problems that involve some constants. Like the length of the equator. So values should be listed explicitly.
   `A tennis ball during a competition flies 15 meters in half a second. seconds. How fast is the ball traveling?`.
   `Find the volume of mercury weighing 2 kilograms.`.
   (Perfect examples)

- Problems where named entities are involved. Like human step.
  `How fast is a person walking if he takes three steps in 2 seconds? The length of one step is 80 cm.`.
- Problems with several values. (Telegram)
- In comparison problems: the program needs specific changes.
- We represent physics concepts as variables. But in the real world it is vice versa. Ambiguity: c - speed of light,
  capacitance.

SVO
number then measurement unit
measurement unit in specific syntax
accepts only text
For different objects different area formula.
cant solve equations

A problem:
Автобус проїхав 1,5 км за 1 хв. Який шлях подолає автобус за 1,5 год?

TODO: ADD FORMULAS FOR DIFFERENT FIELDS.
TODO: FIND MORE TASKS FOR FINDING VALUES.

Sometimes we need to find unknown value and also represent it in some unit.

Bad quantities parsing

The History of the Calculus and the Development of Computer Algebra Systems

Problem with Haskell - it is too strict

Compare these two quantities ...
Find the force and convert it to the kilograms....

Variables are determined only by one word

TODO: CONTEXT!!!!

WE rely on that there is always a question sentence in the task. So there is QUESTION NOUN VERB pattern.
