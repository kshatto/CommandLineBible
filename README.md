# CommandLineBible
Using the command line, scrape simple ESV text of any Scripture passage from http://esv.literalword.com, sending it to the console and the clipboard.

On Windows, you can create a batch file and put it in a folder that is part of your PATH. Call it something like CLBible.bat:

  @[Path 1] [Path 2] %*
  @pause
  
Instead of "[Path 1]", put the path to your Python executable that includes all the project dependencies.
This can be a virtual environment like:
  C:\Python\.virtualenvs\CommandLineBible\\Scripts\python.exe

Instead of "[Path 2]", put the path to the main.py of this project. Could be something like:
  C:\Python\CommandLineBible\main.py

Then you can simply go to a Run window or command prompt and type:
  clbible [Scripture reference]

Instead of "[Scripture reference]", put any Scripture reference that works in the search box of http://esv.literalword.com.
For example:
  clbible luke 4:14-21
  
will give you verses 14 through 21 of chapter 4 of the book of Luke, in plain text.

It will print to the console window, and also automatically be copied to the clipboard, ready to be pasted anywhere you like.
