# refreshrate
A Python package that fetches your monitor refresh rate.

## Installation
Install the package via pip:

```bash
pip install refreshrate
```

## Usage
To use `refreshrate` in your project:

```python
import refreshrate

# Get the monitor's refresh rate
rate = refreshrate.get()

if rate:
    print(f"Your monitor's refresh rate is {rate} Hz.")
else:
    print("Could not retrieve the refresh rate.")
```