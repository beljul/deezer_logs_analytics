Deezer logs analytic module repository (Python 2.7)
========================
This project is a logs parser in order to analyze data from Deezer. The aim is to compute the market share by provider.

##Installation
There is a MakeFile you can use in order to install all you need for this module.

Download and install dependencies:

`make init`

Install the deezer module:

`make install`

Launch the test suite:

`make test`
##How to use this module?
To use the parse function inside deezer module you have to give it the directory where all the logs are saved.
```
import deezer

deezer.parse('/directory/where/logs/are')
```

Then a directory results_YYYYMMDD will be created in your /directory/where/logs/are, and you will find each file for each provider inside.
##What's next?
We began by implemented a multi-processing algorithm. However for the moment it's limited and we have to implement the shared memory variables to perform it.
