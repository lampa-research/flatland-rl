🚂 Flatland
========

![Flatland](https://i.imgur.com/0rnbSLY.gif)

<p style="text-align:center">
<img alt="repository" src="https://gitlab.aicrowd.com/flatland/flatland/badges/master/pipeline.svg">
<img alt="discord" src="https://gitlab.aicrowd.com/flatland/flatland/badges/master/coverage.svg">
</p>

Flatland is a open-source toolkit for developing and comparing Multi Agent Reinforcement Learning algorithms in little (or ridiculously large!) gridworlds.

The base environment is a two-dimensional grid in which many agents can be placed, and each agent must solve one or more navigational tasks in the grid world. 

[The official documentation](http://flatland.aicrowd.com/) contains full details about the environment and problem statement

🏆 Challenges
---

This library was developed specifically for the AIcrowd [Flatland challenges](http://flatland.aicrowd.com/research/top-challenge-solutions.html) in which we strongly encourage you to take part in!

- [NeurIPS 2020 Challenge](https://www.aicrowd.com/challenges/neurips-2020-flatland-challenge/)
- [2019 Challegent](https://www.aicrowd.com/challenges/flatland-challenge)

📦 Setup
---

### Prerequisites

* Install [Anaconda](https://www.anaconda.com/distribution/)
* Create a new conda environment:

```console
$ conda create python=3.6 --name flatland-rl
$ conda activate flatland-rl
```

* Install the necessary dependencies:

```console
$ conda install -c anaconda tk  
```

### Stable Release

You can install Flatland from pip:

```console
$ pip install flatland-rl
```

This is the preferred method to install Flatland, as it will always install the most recent stable release.

### From sources

The Flatland code source is available from [AIcrowd gitlab](https://gitlab.aicrowd.com/flatland/flatland).

You can clone the public repository:
```console
$ git clone git@gitlab.aicrowd.com:flatland/flatland.git
```

Once you have a copy of the source, you can install it with:

```console
$ python setup.py install
```

### Test installation

Test that the installation works:

```console
$ flatland-demo
```

You can also run the full test suite:

```console
python setup.py test
```

👥 Credits
---

This library was developed by [SBB](https://www.sbb.ch/en/), [AIcrowd](https://www.aicrowd.com/) and [numerous contributors](http://flatland.aicrowd.com/misc/credits.html) and AIcrowd research fellows from the AIcrowd community. 

➕ Contributions
---
Please follow the [Contribution Guidelines](http://flatland-rl-docs.s3-website.eu-central-1.amazonaws.com/contributing.html) for more details on how you can successfully contribute to the project. We enthusiastically look forward to your contributions.

💬 Communication
---

* [Discord Channel](https://discord.com/invite/hCR3CZG)
* [Discussion Forum](https://discourse.aicrowd.com/c/neurips-2020-flatland-challenge)
* [Issue Tracker](https://gitlab.aicrowd.com/flatland/flatland/issues/)

🔗 Partners
---

<a href="https://sbb.ch" target="_blank" style="margin-right:25px"><img src="https://i.imgur.com/OSCXtde.png" alt="SBB" width="200"/></a> 
<a href="https://www.deutschebahn.com/" target="_blank" style="margin-right:25px"><img src="https://i.imgur.com/pjTki15.png" alt="DB"  width="200"/></a>
<a href="https://www.aicrowd.com" target="_blank"><img src="https://avatars1.githubusercontent.com/u/44522764?s=200&v=4" alt="AICROWD"  width="200"/></a>
