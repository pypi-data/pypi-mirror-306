# VDMA-LIF JSON Parsers

JSON parsers and models for the VDMA - LIF (Layout Interchange Format), which is used for defining track layouts and exchanging information between the integrator of driverless transport vehicles and a third-party master control system.

The models are generated from a json schema which can be found in the [vdma-lif repository](https://github.com/continua-systems/vdma-lif.git)

## Install

```bash
pip install vmda_lif
```

## Usage

### Read schema from file
```python
from vdma_lif.parser import LIFParser
schema = LIFParser.from_file("example.lif.json")
```

### Read schema from string
```python
from vdma_lif.parser import LIFParser
schema = LIFParser.from_json(schame_str)
```

### Convert into json
```
LIFParser.to_json(schema)
```

### Write schema to file:
```python
LIFParser.to_file(schema, "example.lif.json")
```

## License

This project is licensed under the **MIT License**.

This `README.md` file provides all the necessary information to understand the repository's purpose, how to set up and use the parsers, and how to contribute.

Let me know if you need any further adjustments!

## Maintainers

This repository is maintained by Continua Systems GmbH. For any inquiries, please contact us at:

    Website: https://continua.systems
    Email: info@continua.systems