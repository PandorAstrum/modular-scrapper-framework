# Modular Scrapper Framework
> A procedural scrapper framework built upon scrapy to escalate and
modify scrapping on the fly.

[![Python Version][python-image]][python-url]
[![Scrapy Version][scrapy-image]][scrapy-url]


This is a CLI scrapper framework wrapper built over scrapy framework
User can modify and adjust anything or everything about a spider or crawler from the command
lines by typing appropriate flags

This product is built on WIN 10 (64 bit). for further dev make sure you use 64 bit architecture

## Installation & Setup for Development

###### Download (Extras):
- [GIT CLI](https://git-scm.com/downloads)
- [VS CODE](https://code.visualstudio.com/)

###### Project Setup:
Windows (cmd):

If you have git installed :

```bash
> git clone https://github.com/PandorAstrum/modular-scrapper-framework

> cd <directory\of\cloned\git\folder>

> pip install -r requirements.txt
```
If you dont have git then simply download from this repo as a zip and extracted into a folder

```bash
> cd <directory\of\cloned\git\folder>

> pip install -r requirements.txt
```
###### Run & Test:

Need to fill up Unit test here

## Folder Structures:


(project root folder)

    ├── core (folder)                    # contains the modular system
    │   ├── commands (folder)            # contains list of commands for the CLI
    │   └── questionnaire (folder)       # questions list for the CLI
    │
    ├── general (folder)                 # contains scrapy system
    │   └── spiders (folder)             # contains the actual spiders
    │
    ├── utility (folder)                 # contains some helpful functions
    │
    └── run.py                           # main file to run (CLI)


## Usage example

A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

* Demo all the commands here one by one

To compile the project run:
```
some commands
```

To migrate the project run:
```
some commands
```

To test the project run:
```
some commands
```


## Release History

* 0.4.0
    * CHANGE: Update docs (module code remains unchanged)
* 0.3.0
    * editable parameters exposing for modularity
* 0.2.0
    * scrapper integration
* 0.1.0
    * command tools integration
* 0.0.1
    * Work in progress

## Meta

Ashiquzzaman Khan – [@dreadlordn](https://twitter.com/dreadlordn)

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/PandorAstrum/modular-scrapper-framework](https://github.com/PandorAstrum/modular-scrapper-framework)

## Contributing

1. Fork it (<https://github.com/PandorAstrum/modular-scrapper-framework/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[python-image]: https://img.shields.io/badge/Python-3.6-yellowgreen.svg?style=flat-square
[python-url]: https://www.python.org/

[scrapy-image]: https://img.shields.io/badge/scrapy-1.6-orange.svg?style=flat-square
[scrapy-url]: https://www.npmjs.com/

[travis-image]: https://travis-ci.org/PandorAstrum/_vault.svg?branch=master
[travis-url]: https://travis-ci.org/PandorAstrum/_vault

[appveyor-image]: https://ci.appveyor.com/api/projects/status/8dxrtild5jew79pq?svg=true
[appveyor-url]: https://ci.appveyor.com/project/PandorAstrum/vault

[ReadTheDoc]: https://github.com/yourname/yourproject/wiki

<!-- Header Pictures and Other media-->
[header-pic]: header.png
