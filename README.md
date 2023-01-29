# The Smart Calculator

_The project is a part of the Python core track made by [JetBrains Academy and Hyperskill](https://hyperskill.org/projects/74?track=2)._

The calculator supports operations such as 
- addition, 
- subtraction, 
- multiplication,
- division 

as well as __parentheses__ and __variables__.

When working with variables you have to keep in mind that:
- The name of a variable can contain __only latin letters__.
- A variable can have a name consisting of more than one letter.
- A variable name is __case-sensitive__.
- The value can be an __integer__, __float__ or a value of another __variable__.
- Assigning a new value to an existing variable will rewrite the previous value.
- Type the name of a variable to print its value.

Examples of work:
```commandline
> n = 32
> 33 + 20 + 11 + 49 - 32 - 9 + 1 - 80 + 4
-3
> 33 + 20 + 11 + 49 - n - 9 + 1 - 80 + 4
-3
> c = n 
> c = 2
>   c   
2
> 11 - 13 + c
0
> a=12
>-a
-12
> a=2
> b=a
> -(3-1)+a*4/(b-1)
6
> /exit
Bye!
```

Some examples of the exception testing:
```commandline
> /start
Unknown command
> var1 = 1
Invalid identifier
> c = 7 - 1 = 5
Invalid assignment
> variable = f
Unknown variable
> variable = 777 
>  Variable
Unknown variable
> 8 * (2 + 3
Invalid expression
> 4 + 5)
Invalid expression
> 2 ************ 2
Invalid expression
> 2 // 2
Invalid expression
```
 
