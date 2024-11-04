# fluxgen

> install and configure Flux Framework

![PyPI - Version](https://img.shields.io/pypi/v/fluxgen)

This small library makes it easy to generate install scripts and configuration to get flux up and running!
We will run this in the context of a JobSet, with the goal to generate the scripts necessary to install flux, etc.

🚧 Under Construction! 🚧

## Usage

Here is an example for using fluxgen to generate an install script for a worker.

```bash
fluxgen create --brokers flux-sample[0-10] command arg1 arg2
```

And the lead broker:

```bash
fluxgen create --lead-broker --brokers flux-sample[0-10] command arg1 arg2
```

Just preview:

```bash
fluxgen create --lead-broker --brokers flux-sample[0-10] --dry-run command arg1 arg2
```

## License

HPCIC DevTools is distributed under the terms of the MIT license.
All new contributions must be made under this license.

See [LICENSE](https://github.com/converged-computing/cloud-select/blob/main/LICENSE),
[COPYRIGHT](https://github.com/converged-computing/cloud-select/blob/main/COPYRIGHT), and
[NOTICE](https://github.com/converged-computing/cloud-select/blob/main/NOTICE) for details.

SPDX-License-Identifier: (MIT)

LLNL-CODE- 842614
