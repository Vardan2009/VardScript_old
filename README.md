# VardScript
![logo_fullwhite](https://github.com/Vardan2009/VardScript/assets/70532109/b67d43f4-d64e-4be5-9a35-ed08ed4acaa7)
A simple yet functional programming language, written in python

Please note that the code is still unfinished, and may have some small errors

# How To Use
Create a .vard file and write code in it
To Compile the code, open the .py file with your file location as an argument:
```
py vardscript.py path/to/file.vard
```

# Comments
In Vardscript, comments are denoted by a colon, comments are ignored by the interpreter.
```
:this is a comment
```

# Output
There are two ways of displaying output in VardScript:

## 1. 'out' statement
```
out "Hello World!"
```
The 'out' statement is used to output a given string without appending a newline character.

## 2. 'ln_out' statement
```
ln_out "Hello World!"
```
The 'ln_out' statement is used to output a given string and append a newline character.

# Variables

In VardScript, there are 2 variable types:

## Numeric Variables
Numeric variables hold numerical values, such as integers or floating-point numbers.
```
&e = 10
```

## String Variables
String variables store text data.
```
&e = "Some Text Here"
```

# Functions
Functions in Vardscript allow you to encapsulate blocks of code for reuse.

## Defining Functions
```
func my_function()
    : Some code here
endfunc
```
## Calling Functions
```
my_function()
```

# Conditional Statements

Vardscript supports conditional statements. The basic syntax for 'if' statements is as follows:

## IF Statement
```
if 1==1 then
    ln_out "condition is true"
endif
```

## IF-ELSE Statement
### WARNING: IF-ELSE STATEMENTS ARE TEMPORARILY REMOVED
```
if 1==2 then
    ln_out "condition is true"
else
    ln_out "condition is false"
endif
```

You can use "== (equal) " "> (greater than)" "< (lesser than)" "$= (not equal)"

# While Loops
Looping constructs allow you to repeat code blocks as long as a certain condition is met. In Vardscript, you can use the 'while' loop:

```
&counter = 0

while &counter until 10 then
    ln_out "This will print 10 Times!"
endwhile
```

You can also initialize the loop variable and specify a different number of iterations:

```
&counter = 5

while &counter until 10 then
    ln_out "Now, This will print 5 Times, because starting value is 5"
endwhile
```

# Input
In Vardscript, you can ask input from the user and assign it to a variable
```
input "What is your name?:" &name

out "Hello,"
out &name
ln_out "!"

```

# Parsing Variables
In Vardscript, the "parse" function allows you to convert a variable from one data type to another. This can be particularly useful when you need to change the type of a variable to perform specific operations or comparisons.

## Syntax
```
parse source_variable (t_num or t_str)
```

## Example
(the typeof statement just outputs the variable type as "STRING" or "NUM")
```
&number = "23"
parse &number t_num
typeof &number : t_num is now a numerical variable
```
# 'os' Statement
The VardScript programming language provides a convenient way to execute operating system (OS) commands directly from your code. This feature allows you to interact with the underlying operating system and execute various commands, such as running shell commands, scripts, or system utilities.

## Syntax

```
os "command"
```

## Example

```
:example, printing text
os "echo Hello World!" :if using Windows


:example, clearing screen
os "cls" :if using windows
os "clear" :if using linux
```

# Thread Sleep
the 'sleep' statement delays the execution of the code
## Syntax
```
sleep *amount*
```
## Example
```
sleep 100
ln_out "e"
```

# Get System Time
the 'time' statement gets the system time

```
time "format"
```
## Example
```
time "%H:%M"
```

# Generating Random Numbers
In VardScript, rand x,y and nrand functions are used for generating random numbers

## 'nrand' statement
The 'nrand' statement generates a number from 0 to 1
```
&random = nrand
ln_out &random
```

## 'rand' statement
The 'rand' statement generates a number from a given range
```
&random = rand 1,10
ln_out &random
```


### Created by Vardan2009
