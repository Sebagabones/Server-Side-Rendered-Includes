# Apache SSI's but like, simple

If you are old, or idk, use apache and don't wanna use something more than good old html and css but still want to template/include html from other files in your html you will have probably heard of Apache Server Side Includes.

Now, I have not been able to find a guide to get SSI's working for me, and after finding pug2html conversions to not work particually well, and not wanting to redo my plain html into a different component library, and liking the style of Apache SSI's, I decided to implement a very simple setup to build/render html files with include statements to their final form before being hosted

If there is demand/I have interest I may make this fully compatible with Apache SSI's, however for the time being the format for includes is `<!--#include file="file.html"-->` where file.html is a html file in same directory as the file (this will possibly be changed in the future if I get around to it to support more options)
