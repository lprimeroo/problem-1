# problem-1

## Install

The shell commands mentioned below install `pipenv`, clone the repository, and setup a Python 3.7 virtual environment along with installing all the Python packages.

```sh
pip install pipenv
git clone https://github.com/saru95/problem-1; cd problem-1/
pipenv install; pipenv shell
```

## Execution

The mining script is present within the folder `argument_commits/`. To use it as a module, follow `example.py` and just run,

```sh
python example.py # or you_file_name.py
```

```py
from argument_commits import ArgumentCommits

# The constructor takes in a list of git URLs.
c = ArgumentCommits(urls=['https://github.com/google/guava', ....])

# This routine finds the commits where a function argument was added to a Java file.
c.find_commits_with_additional_parameters()

# This routine writes the result of the routine above to a CSV file. It takes in the name of the file as the argument.
c.write_to_csv(filename='')
```

## Samples

As a test the script was run on 2 famous repositories:

1. RxJava:
    * Total Number of Commits: ~5471
    * Time taken: ~50 mins.
    * Link: https://github.com/ReactiveX/RxJava
    * CSV Generated: https://www.dropbox.com/s/w1i8h5s897msiky/RxJava.csv?dl=0 (the CSV file was too big for Github)

2. ZXing:
    * Total Number of Commits: ~3475
    * Time taken: 
    * Link: https://github.com/zxing/zxing
    * CSV Generated:  (the CSV file was too big for Github)
