# Super simple example usecase

So, my inital pages are in `src/`, with my template file in `templates/`, which is just my footer.

So, if we run `ssri -d src -o pages -t templates`, we create a directory called `pages`, which contains the output files.

You should be able to see the difference, but basically this just sets up a way to quickly copy template HTML components into various pages. If you want to setup the before example as shown below, simply remove the `pages` directory. 

### Before

``` sh
.
├── README.md
├── src
│   ├── index.html
│   └── secondaryPage.html
└── templates
    └── footer.html
```

### After

``` sh
.
├── pages
│   ├── index.html
│   └── secondaryPage.html
├── README.md
├── src
│   ├── index.html
│   └── secondaryPage.html
└── templates
    └── footer.html
```

By putting the output files into their own folder means, provided your webserver is setup correctly, you can prevent the templates, and src files being accessed, by setting your root folder to be `pages` in this example. 
