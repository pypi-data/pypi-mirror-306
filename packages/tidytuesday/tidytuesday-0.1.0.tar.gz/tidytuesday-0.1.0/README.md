# tidytuesdayPy

Download TidyTuesday data. Inspired by [tidytuesdayR](https://github.com/thebioengineer/tidytuesdayR).

## Usage

```python
from tidytuesday import TidyTuesday

tt = TidyTuesday("2021-04-06")
```

If you do not provide a date (_i.e._ just `TidyTuesday()`), then the latest TidyTuesday will be used. Note that this will not be good for reproducability in the future!

You can then access each data set from the data field using the filename, dropping the extension.

```python
df = tt.data["forest"]
```

You can also access the readme if one exists.

```python
print(tt.readme)
```

### Polars

If you want to use Polars, you can pass the module to the TidyTueday constructor via the optional mod argument as follows:

```python
import polars as pl

tt = TidyTuesday("2021-04-06", mod=pl)

tt.data["forest"] # is a pl.DataFrame
```

For future dataframe modules, you can pass as the mod argument any object/module that has a read_csv that returns an object.

The constructor also has an optional kwargs argument that allows you to pass a dictionary of kwargs to the read_csv method. For instance, this can be used to specify separators in pl.read_csv as follows:

```python
tt = TidyTuesday("2020-08-25", mod=pl, kwargs={"separator": "\t"}) # contains chopped.tsv

tt.data["chopped"] # is a pl.DataFrame
```

If using the default Pandas, sepcifying tab separation should not be needed.

## TODO

- Implement parsers for rds formats
- Documentation
