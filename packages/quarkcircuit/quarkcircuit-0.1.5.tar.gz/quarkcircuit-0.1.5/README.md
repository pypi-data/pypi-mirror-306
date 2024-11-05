# QuarkCircuit

[![PyPI - Python Version](https://img.shields.io/badge/python-3.10-pink.svg)](https://pypi.org/project/quarkcircuit/)
[![Downloads](https://static.pepy.tech/badge/quarkcircuit)](https://pepy.tech/project/quarkcircuit)
[![API](https://img.shields.io/badge/API-quarkcircuit-green.svg)](https://quarkstudio.readthedocs.io/en/latest/modules/quark/circuit/)

<!-- TOC --->
- [QuarkCircuit](#quarkcircuit)
  - [What is QuarkCircuit](#what-is-quarkcircuit)
  - [Installation](#installation)
  - [First experience](#first-experience)
    - [Plot a quantum circuit](#plot-a-quantum-circuit)
    - [Transpile to basic gates](#transpile-to-basic-gates)
  - [Tutorials](#tutorials)
  - [License](#license)
<!-- /TOC -->

## What is QuarkCircuit 

QuarkCircuit is a software package that offers a clean and concise circuit visualization feature, along with a simple transpilation functionality.


## Installation

```
pip install quarkcircuit
```

## First experience

### Plot a quantum circuit

```bash
from quark.circuit import QuantumCircuit

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0,1)
qc.cx(0,2)
qc.barrier()
qc.measure_all()
qc.draw()
```

<img src="image-3.png" alt="description" height="170">

<table ><tr><td bgcolor=MistyRose >Note: For better circuit display, please set your chrome or VS Code to a monospaced font, such as "Consolas".</td></tr></table>


### Transpile to basic gates

```bash
from quark.circuit import Transpile
qct = Transpile(qc, physical_qubit_list = [98,99,100]).run(optimize_level=1)
qct.draw_simply()
```
<img src="image-4.png" alt="description" height="160">


## Tutorials

It will be added in the future.

## License

[MIT](LICENSE)