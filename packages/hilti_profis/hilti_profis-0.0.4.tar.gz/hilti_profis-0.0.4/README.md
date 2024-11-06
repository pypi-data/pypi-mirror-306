<!--- Heading --->
<div align="center">
  <h1>Hilti Profis</h1>
  <p>
    Python binding for generating `.pe` files, for use with <a href="https://www.hilti.ca/content/hilti/W1/CA/en/business/business/engineering/profis-engineering.html">Hilti-Profis software</a>.
  </p>
<h4>
    <a href="https://github.com/rpakishore/Hilti-Profis">Documentation</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/Hilti-Profis/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/Hilti-Profis/issues/">Request Feature</a>
  </h4>
</div>
<br />

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/rpakishore/Hilti-Profis)
![GitHub last commit](https://img.shields.io/github/last-commit/rpakishore/Hilti-Profis)
[![tests](https://github.com/rpakishore/Hilti-Profis/actions/workflows/test.yml/badge.svg)](https://github.com/rpakishore/Hilti-Profis/actions/workflows/test.yml)
![PyPI - Version](https://img.shields.io/pypi/v/hilti_profis)

<!-- Table of Contents -->
<h2>Table of Contents</h2>

- [1. About the Project](#1-about-the-project)
  - [1.1. Features](#11-features)
- [2. Getting Started](#2-getting-started)
  - [2.1. Prerequisites](#21-prerequisites)
  - [2.2. Dependencies](#22-dependencies)
  - [2.3. Installation](#23-installation)
    - [2.3.1. From github](#231-from-github)
    - [2.3.2. From Pypi](#232-from-pypi)
  - [2.4. Development](#24-development)
- [3. Usage](#3-usage)
- [6. License](#6-license)
- [7. Contact](#7-contact)

<!-- About the Project -->
## 1. About the Project

<!-- Features -->
### 1.1. Features

- Create new custom `.pe` files
- Modify part/whole of existing `.pe` file
- Add load cases to anchor design

<!-- Getting Started -->
## 2. Getting Started

<!-- Prerequisites -->
### 2.1. Prerequisites

Python 3.11 or above

### 2.2. Dependencies

Create the virutual environment and install dependencies

```bash
  pip install flit
```

<!-- Installation -->
### 2.3. Installation

#### 2.3.1. From github

Get the latest version directly from github

```bash
  git clone https://github.com/rpakishore/Hilti-Profis.git
  cd Hilti-Profis
  pip install flit
  flit install --deps production
```

#### 2.3.2. From Pypi

```bash
  pip install hilti_profis
```

### 2.4. Development

Download the git and install via flit

```bash
  git clone https://github.com/rpakishore/Hilti-Profis.git
  cd Hilti-Profis
  pip install flit
  flit install --pth-file
```

<!-- Usage -->
## 3. Usage

```python
from hilti_profis.main import PE

anchor = PE(basefile=None)  #Optionally provide an existing `.pe` file to import default values

#Change/Add values
anchor.Model['ProjectName'] = 'TestProject'

anchor.Model.Loads.Combos.delete_existing()     #Delete Existing Load Combinations
anchor.Model.Loads.Combos.add(Fx=1, Fy=1, Fz=2, Mx=1, My=2, Mz=3, LoadType='Seismic', Comment='LC1')    #Forces in N
anchor.Model.Loads.Combos.add(Fx=1000, Fy=1000, Fz=2000, Mx=1000, My=2000, Mz=3000, LoadType='Seismic', Comment='LC2')    #Forces in N; Moments in N-mm

anchor.Model.apply()            #Apply the changes
anchor.xml_content()            #Get contents of `.pe` file
anchor.save('nosync-test.pe')   #Save file to destination
```
<!-- License -->
## 6. License

See [LICENSE](/LICENSE) for more information.

<!-- Contact -->
## 7. Contact

Arun Kishore - [@rpakishore](mailto:pypi@rpakishore.co.in)

Project Link: [https://github.com/rpakishore/Hilti-Profis](https://github.com/rpakishore/Hilti-Profis)