# Server Side Rendered Includes
## Apache SSI's but like, simple

### TL:DR

SSRI is my solution to a very simple templating engine for plain HTML to have working include statements to bring HTML in from other files.

After reading [this](https://css-tricks.com/the-simplest-ways-to-handle-html-includes/), and not liking many of the options (Gulp seemed senisble, but was bit more than I wanted, as I didn't want to deal with gulp files), I found Apache Server Side Includes to be a 'sane' way to do what I wanted, except for one small problem; I could not get them to work properly. The best guide I found online was [here](https://joabj.com/Writing/Tech/Tuts/Apache/Apache-SSI.html), but when that didn't work I decided to make a solution that was pretty much Apache SSI, but where the include statements were pre-processed.

The include statement is simply a html comment on a line where you want the entire contents from the linked file to be "pasted" in, and uses the following format: `<!-- #include file="filename" optional comments -->` where `filename` is the filename including file extension (eg, `file.html`). In theory this would probably work if it was not on it's own line, but I haven't tested this.

Finally, I have only tested this on Linux, it probably works on MacOS, and probably doesn't work on Windows.

 ```help
 usage: ssri.py [-h] [-d] [-t TEMPLATES_DIR] [-o OUTPUT] [--no-warnings] inputFile [inputFile ...]
```

### Installation
Installation is easy, as this has no external depedencies - either download the `ssri.py` file, or clone this repo (at some point I may put this on pip).

### Usage
There is a simple example setup in the `Example/` folder, which shows a simple way of using `ssri`, but a run through of the commands 



If you are old, or idk, use apache and don't wanna use something more than good old html and css but still want to template/include html from other files in your html you will have probably heard of Apache Server Side Includes.

Now, I have not been able to find a guide to get SSI's working for me, and after finding pug2html conversions to not work particually well, and not wanting to redo my plain html into a different component library, and liking the style of Apache SSI's, I decided to implement a very simple setup to build/render html files with include statements to their final form before being hosted

 ## Usage:
 ```help
 usage: ssri.py [-h] [-d] [-t TEMPLATES_DIR] [-o OUTPUT] [--no-warning] inputFile [inputFile ...]
```

If there is demand/I have interest I may make this fully compatible with Apache SSI's, however for the time being the format for includes is `<!-- #include file="file.html" -->` where file.html is a html file in same directory as the file (this will possibly be changed in the future if I get around to it to support more options)
