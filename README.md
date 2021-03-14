### Hexlet tests and linter status:
[![Actions Status](https://github.com/gato-naranja/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/gato-naranja/python-project-lvl3/actions)
### Project badges
[![Build Status](https://github.com/gato-naranja/python-project-lvl3/workflows/Build%20Status/badge.svg)](https://github.com/gato-naranja/python-project-lvl3/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/544d63de70128b4e237d/maintainability)](https://codeclimate.com/github/gato-naranja/python-project-lvl3/maintainability)
<a href="https://codeclimate.com/github/gato-naranja/python-project-lvl3/test_coverage"><img src="https://api.codeclimate.com/v1/badges/544d63de70128b4e237d/test_coverage" /></a>

**Page-Loader** is a command line utility that downloads pages from the internet and stores them on your computer. Along with the page it downloads all the resources (images, styles and js) allowing you to open the page without the Internet.

### INSTALL
installation example

<a href="https://asciinema.org/a/FQNfrqgBc0syCzdQ2aAwyMl3O" target="_blank"><img src="https://asciinema.org/a/FQNfrqgBc0syCzdQ2aAwyMl3O.svg" /></a>

### PAGE DOWNLOAD
To load the page to a local file you need to:
```
page-loader -o my_dir http://you.url
```
it will create a folder ***my_dir*** with the file ***you-url.html*** containing the downloaded page

<a href="https://asciinema.org/a/c09geKHMyVd6m9gVOXuSlFZOq" target="_blank"><img src="https://asciinema.org/a/c09geKHMyVd6m9gVOXuSlFZOq.svg" /></a>

Also, in the user directory ***my_dir*** in the ***you-url_files*** folder, page resources are downloaded, such as ***images, links and scripts***

<a href="https://asciinema.org/a/eSFrQdnOOkzCkU2Kz1hAKJWuS" target="_blank"><img src="https://asciinema.org/a/eSFrQdnOOkzCkU2Kz1hAKJWuS.svg" /></a>

### ERRORS
If you incorrectly specify the page address or the folder to save to, the corresponding error will be displayed
<a href="https://asciinema.org/a/8PB6ljWlF6YaOTakw7twCvOjl" target="_blank"><img src="https://asciinema.org/a/8PB6ljWlF6YaOTakw7twCvOjl.svg" /></a>
