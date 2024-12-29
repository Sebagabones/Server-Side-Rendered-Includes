# Server Side Rendered Includes
## Apache SSI's but like, simple

### TL:DR

SSRI is my solution to a very simple templating engine for plain HTML to have working include statements to bring HTML in from other files.

After reading [this](https://css-tricks.com/the-simplest-ways-to-handle-html-includes/), and not liking many of the options (Gulp seemed senisble, but was bit more than I wanted, as I didn't want to deal with gulp files), I found Apache Server Side Includes to be a 'sane' way to do what I wanted, except for one small problem; I could not get them to work properly. The best guide I found online was [here](https://joabj.com/Writing/Tech/Tuts/Apache/Apache-SSI.html), but when that didn't work I decided to make a solution that was pretty much Apache SSI, but where the include statements were pre-processed.

The include statement is simply a html comment on a line where you want the entire contents from the linked file to be "pasted" in, and uses the following format: `<!-- #include file="filename" optional comments -->` where `filename` is the filename including file extension (eg, `file.html`). In theory this would probably work if it was not on it's own line, but I haven't tested this.

Finally, I have only tested this on Linux, it probably works on MacOS, and probably doesn't work on Windows.

 ```help
 usage: ssri [-h] [-d] [-t TEMPLATES_DIR] [-o OUTPUT] [--no-warnings] [-v] [-c] inputFile [inputFile ...]
```

### Installation
Installation is easy, as this has no external dependencies (aside from Python) - either download the `ssri.py` file, or clone this repo (at some point I may put this on pip).

### Usage
There is a simple example setup in the `Example/` folder, which shows a simple way of using `ssri`, so this is more of a run through of the argument options:

`inputFile` is one or more files, or a directory (if the `-d` flag is passed).
`-h` prints out the help menu.
`-d` specifies a directory to run through recursively (this will grab all the files in any subdir, keep the order/layout).
`-t` specifies the directory to grab the templates from, if it is not provided it grabs templates from the input directory (or if the input was not a directory it uses the current directory).
`-o` is the directory to output the generated files to, if not provided it using the current directory.
`--no-warnings` silences any warnings, and just runs without worrying if it overwrites any files.
`-v` explains what the script is doing, turns on verbose mode
`-c` copies the entire source (input) directory to the output directory, the `-d` flag must be used, and only one directory may be provided 

#### Tips
By putting the output files into their own designated folder, so as long as you setup your webserver correctly, you can prevent the templates and source files from being accessed, by setting your webserver's root folder to be output folder.
If you want another example, go have a look at my personal website, which is using SSRI, the repository for that is [here](https://github.com/Sebagabones/mahoosivelygay). The command I use for templating this is `ssri -d staging -t templates -o sites`.

### Why?
I wanted something that worked without any dependencies, and didn't require learning a new markup style. The main goal for this was to be able to write pure plain HTML pages without using external libraries needing to be imported, and that didn't use JavaScript to load things in the browser. Could I have used something like NextJS for this? Probably - but I wanted something that would be very simple to use (albeit much less powerful).

Apache SSI seemed very cool for a few reasons - super simple markup (kinda - lack of documention made it a bit harder, but the basic idea was decent), and even if something went wrong, the browser always received valid HTML. One issue I had was that, well, it didn't work, or at least, I couldn't find a way to get it working (again, very little documentation), and while I also felt like server processing the HTML on request would add a small amount of overhead, the biggest reason I didn't spend more time on getting SSI to work was because I wanted a way to use other webservers without needing to change my HTML files.

I wanted to use PUG, but found that the html2pug converters didn't work well, and there were a few other issues I had with it, and I didn't want to learn another markup style and rewrite my website lol. Similarly with Gulp, I didn't want to have to deal with Gulp files.

Hence, I took a lot of inspiration from SSI, but decided that preprocessing the HTML would be easier.

In theory, this should work with most other libraries/backends, which is another benefit to it, as you would simply run this before starting the server. While it *kinda* works with big frameworks/libraries like React and Jinja, the only issue I can think of is currently only HTML files are copied to the output folder. I do plan to add an option that copies the entire input dir to the output dir, and only updates the HTML, which would solve this issue, and make it pretty flexible for other setups. Likewise, I will probably add an argument that allows you to select with files types you want to search in, allowing for more uses with `.jsx` files, and possibly CSS files ect.


### Use cases:
I mean - the main use case was for my website lol. That said, it could be useful for anyone teaching/learning HTML, as it is a very simple concept that allows for (static) components to be reused across different pages, and reduces the learning new things load on anyone using it when compared to Gulp/Pug/React/Jinja. Basically, it allows for someone to learn the fundementals of HTML/CSS without needing a backend, but for them to still be able to save time without needing to copy HTML to different files.

### Future plans.
As mentioned above. I do want to add an an option that copies the all the contents of the entire input folder to the output folder, and only updates the HTML.
Likewise, adding an argument that allows you to select with files types you want to search for include statements in is planned, as it would allow use with `.jsx` files, and possibly CSS files ect.
Another future addition would be to add in the ablity to nest include statements in template files. This *might* already work, but I have not tested it, and there is the potential to get stuck in a endless loop, so for the time being I would not recommend include statements inside templates. 
 

If there is demand/I have interest I may make this fully compatible with Apache SSI's, however for the time that isn't the case - if someone has good documentation on SSI options please let me know about it/send it to me, easiest way to do that is probably to raise an issue :)

Contributions are welcome, of course, just open a PR

