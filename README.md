# Modular Scrapper Framework
> A procedural scrapper framework built upon scrapy to escalate and
modify scrapping on the fly.

[![Python Version][python-image]][python-url]
[![Scrapy Version][scrapy-image]][scrapy-url]


This is a CLI scrapper framework wrapper built over scrapy framework
User can modify and adjust anything or everything about a spider or crawler from the command
line interface by typing appropriate flags

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


(project root)

    ├── core (folder)                    # contains the modular system
    │   ├── commands (folder)            # contains  commands for the CLI
    │   │   ├── command_lines.py         # command line interfaces (command Pattern)
    │   │   └── scrapper.py              # main scrapper commands
    │   │
    │   ├── operations (folder)          # contains list of operation to pass in commands
    │   │   ├── abc_operation.py         # operation interfaces
    │   │   ├── base_operation.py        # base operation (Status,Edit,Run,Deploy)
    │   │   ├── deploy_operation.py      # deploy operation
    │   │   ├── edit_operation.py        # editing operation
    │   │   ├── run_operation.py         # spider run operation (calls from run_scrapper.py)
    │   │   └── scrapper_settings_operation.py         # edit spider settings operation
    │   │
    │   └── questionnaire (folder)       # questions list for the CLI
    │       ├── abc_question.py          # question interface (Strategy Pattern)
    │       └── scrapy_questions.py      # delegates all question for the spiders
    │
    ├── general (folder)                 # contains scrapy system
    │   └── spiders (folder)             # contains the actual spiders
    │       ├── items.py
    │       ├── middlewares.py
    │       ├── pipelines.py
    │       ├── run_scrapper.py         # functions for starting spider (product/price)
    │       ├── settings.py             # spider settings
    │       └── settings.json           # spider settings in json **
    │
    ├── utility (folder)                 # contains some helpful functions
    │
    └── run.py                           # main file to run (CLI)


## Usage example


 From cmd or bash

- To Run the CLI:
```cs
python run.py
```

Calling From Outside of the CLI

This functions can be found in `run_scrapper.py` file

**function**
```cs
scrape_product(_spider_name, _settings_file)
```
Scrape the product
<br>
*parameters*
```cs
_spider_name = "ArteriorsHome" <string>
_settings_file = "C:\Users\Desktop\Project\general\settings.josn" <path>
```
<br>

**function**
```cs
scrape_price(_spider_name, _settings_file, _username, _password, _customerid)
```
Scrape the price
<br>
*parameters*
```cs
_spider_name = "ArteriorsHome" <string>
_settings_file = "C:\Users\Desktop\Project\general\settings.josn" <path>
_username = "something@somthing.net" <string>
_password = "********" <string>
_customerid = "elon123" <string>
```
<br>

**function**
```cs
deploy_to_scrappingHub(_spider_name, _settings_file, _username, _password, _customerid, _apiKey, _projectid)
```
Deploy with scrapping Hub
<br>
*parameters*
```cs
_spider_name = "ArteriorsHome" <string>
_settings_file = "C:\Users\Desktop\Project\general\settings.josn" <path>
_username = "something@somthing.net" <string>
_password = "********" <string>
_customerid = "elon123" <string>
_apikey = "3f001jk11789eervt" <string> can be found on scrapping hub dashboard
_projectid = "331705" <string> can be found on scrapping hub dashboard
```
<br>
<br>
<br>

## Worked So far
- [x] (CLI framework to execute spider standalone)
- [ ] (Scrapyd server deployment)
<br>

- [x] (abhomeinc = products)
- [x] (abhomeinc = prices)
<br>

- [x] (arteriorshome = products)
- [x] (arteriorshome = prices)
<br>

- [ ] (bernhardt = products)
- [ ] (bernhardt = prices)
<br>

- [ ] (centuryfurniture = products)
- [ ] (centuryfurniture = prices)
<br>

- [ ] (cowtan = products)
- [ ] (cowtan = prices)
<br>

- [x] (curreycodealers = products)
- [x] (curreycodealers = prices)
<br>

- [ ] (hookerfurniture = products)
- [ ] (hookerfurniture = prices)
<br>

- [x] (noirfurniturela = products)
- [ ] (noirfurniturela = prices)
<br>

- [x] (reginaandrew = products)
- [ ] (reginaandrew = prices)
<br>

- [ ] (surya = products)
- [ ] (surya = prices)
<br>

- [ ] (vanguardfurniture = products)
- [ ] (vanguardfurniture = prices)
<br>


## Release History

* 0.9.0
    * ADD: Deployment to third party system added (Docker + Scrapping Hub)
* 0.8.0
    * FIX: operations, spider file name with and price json customer id
* 0.7.0
    * ADD: All operations added
* 0.6.0
    * ADD: Detection change System
* 0.5.0
    * ADD: Two variations of running spiders (Login/ Without Login)
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
