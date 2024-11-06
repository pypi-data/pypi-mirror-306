# FAIR Wizard Integration SDK

*Integrate FAIR Wizard within your environment easily*

[![Docs](https://img.shields.io/badge/docs-Documentation-informational)](https://integration-sdk.fair-wizard.com)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/fair-wizard/fair-wizard-integration-sdk)](https://github.com/fair-wizard/fair-wizard-integration-sdk/releases)
[![LICENSE](https://img.shields.io/github/license/fair-wizard/fair-wizard-integration-sdk)](LICENSE)

## Usage

### Installation

To install the SDK, you can simply install it via pip from PyPI:

```bash
pip install fair-wizard-integration-sdk
```

Alternatively, you can install it via pip from GitHub repository directly:

```bash
pip install git+https://github.com/fair-wizard/fair-wizard-integration-sdk.git#egg=fair-wizard-integration-sdk
pip install https://github.com/numpy/numpy/releases/download/vX.Y.Z/fair_wizard_integration_sdk-X.Y.Z.tar.gz
```

Alternatively, you can clone the repository and install it locally:

```bash
git clone git@github.com:fair-wizard/fair-wizard-integration-sdk.git
cd fair-wizard-integration-sdk

git checkout develop
git checkout vX.Y.Z

pip install .
```

### Local Development (and Testing)

You can check [examples](./examples) and [tests](./tests) for how to use the SDK.

We also recommend reading the documentation for further details.

### Documentation

To generate the documentation, run the following command:

```bash
cd docs
pip install -r requirements.txt
make html
```

The documentation will be generated in the `docs/_build/html` directory.

## License

This project is licensed under the Apache License v2.0 - see the
[LICENSE](LICENSE) file for more details.
