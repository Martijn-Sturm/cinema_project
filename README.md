# Cinema project

Cinema project algorithms for the course Algorithms for decision support.

This project is made by Anne Lycia Cate, Esmee Dekker, Lucas Meijer, Zoril Oláh and Martijn Sturm.

## Installation

Before running the program make sure all the packages are installed by running the following statement.

```bash
pip install requirements.txt
```

## Usage

### Offline

To run the ILP algorithm for the Offline problem run the following statement in CMD.

```bash
python main_offline.py
```

To test the program on a different input file simply change the name of the input file in main_offline.py.

### Online

To run the algorithms for the Online problem run the following statement in CMD.

```bash
python main_online.py
```

To test the program on a different input file simply change the name of the input file in main_online.py.
Before running, uncomment the lines of code depending on which algorithm you want to use.

#### Analysis

If you want to reproduce the results of the analysis and simulation, [this notebook](https://github.com/Martijn-Sturm/cinema_project/blob/master/run_online_tests.ipynb) can be used. Be sure to adjust the number of cores on [line 23 (n_jobs)](https://github.com/Martijn-Sturm/cinema_project/blob/master/online_batch.py) depending on your machine.

### Extensions

The program contains the following extensions.

#### Balconies

To run the balcony extension run the following statement in CMD.

```bash
python main_balcony.py
```

To test the program on a different input file simply change the name of the input file in main_balcony.py.

#### VIPs

For the VIP extension an extra line needs to be added the input file as can be seen in the example below.

```bash
6
9
011101111
111101111
111101111
000000000
111101111
111101111
4 4 0 1 1 0 0 0
3 0 0 1 0 0 0 0
```

The first integer on the line is the number of VIP groups of size 1 that need to be seated, etc.

To run the extension run the following statement.

```bash
python main_offline.py
```

## Dependencies

* [pulp](https://github.com/coin-or/pulp) package
* [tabulate](https://pypi.org/project/tabulate/)
* [networkx](https://networkx.github.io/documentation/stable/index.html)
* [pandas](https://pandas.pydata.org/)
  * If analysis from notebooks will be run
* [joblib](https://joblib.readthedocs.io/en/latest/)
  * In case of running simulations in parallel on multiple cores
