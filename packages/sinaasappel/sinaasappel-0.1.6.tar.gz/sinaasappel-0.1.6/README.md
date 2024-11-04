# sinaasappel
Useful utils

<p align="center">
<a href="https://pypi.org/project/sinaasappel" target="_blank">
    <img src="https://img.shields.io/pypi/v/sinaasappel?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/sinaasappel" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/sinaasappel?color=%2334D058" alt="Supported Python versions">
</a>
</p>

## Recursive sum

Use the following commands to calculate the sum of a nested list of ints:

```python
from sinaasappel import recursive_sum

list_sum = recursive_sum([1, 2, [3, [4]]])
print(list_sum)  # prints 10
```

