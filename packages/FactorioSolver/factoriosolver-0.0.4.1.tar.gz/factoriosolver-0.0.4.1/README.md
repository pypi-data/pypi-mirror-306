# FactorioSolver

Python helper to produce production graphs from the game recipes. Default data is Factorio 2.0. Space Exploration data also available.

## Source

`https://gitlab.com/Santerre/factoriosolver`

## Installation

`pyhon -m pip install FactorioSolver`

## Basic usage

To print a production graph, use : 
```py
import FactorioSolver.FactorioSolver as fs
fs.print_production({"automation-science-pack": 1})
```
