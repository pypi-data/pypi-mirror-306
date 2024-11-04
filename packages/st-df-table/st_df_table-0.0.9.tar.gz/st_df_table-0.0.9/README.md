# Streamlit dataframe display
alternative to `st.table` with configuration displaying Pandas DataFrame


![PyPI - Version](https://img.shields.io/pypi/v/st-df-table)
![PyPI - License](https://img.shields.io/pypi/l/st-df-table)
![PyPI - Downloads](https://img.shields.io/pypi/dm/st-df-table)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/st-df-table)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/st-df-table)
![PyPI - Format](https://img.shields.io/pypi/format/st-df-table)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/st-df-table)

## Installation instructions

```sh
pip install st-df-table
```

## Usage instructions

```python

import pandas as pd
from st_df_table import st_table

data = {
    "Column A": [1, 2, 3, 4, 5, 6],
    "Column C": [True, False, True, False, True, False],
    "Column B": ["A", "B", "C", "F", "G", "H"],
}

df = pd.DataFrame(data)
st_table(df)

```
![table-1](https://raw.githubusercontent.com/mysiar-org/st-table/refs/heads/master/doc/table1.png)

```python
st_table(
    df,
    head_align="left",
    data_align="left",
    head_bg_color="red",
    head_color="blue",
    head_font_weight="normal",
    border_color="red",
    border_width="3",
)
```
![table-2](https://raw.githubusercontent.com/mysiar-org/st-table/refs/heads/master/doc/table2.png)

```python
st_table(
    df,
    head_align="right",
    data_align="right",
    data_bg_color="green",
    data_color="yellow",
    data_font_weight="bold",
    bordered=False,
    sortable=False,
)
```
![table-3](https://raw.githubusercontent.com/mysiar-org/st-table/refs/heads/master/doc/table3.png)

```python
import string
import numpy as np
import pandas as pd
from st_df_table import st_table

df = pd.DataFrame(
    {
        "Column A": list(range(1, 101)),
        "Column B": np.random.choice(list(string.ascii_uppercase), size=100),
        "Column C": np.random.rand(100),
    }
)

st_table(
    df,
    border_width=4,
    border_color="red",
    paginated=True,
    pagination_size_per_page=7,
    pagination_bar_size=4,
    pagination_text_color="blue",
    pagination_bg_color="yellow",
    pagination_border_color="green",
    pagination_active_color="yellow",
)

```
![table-4](https://raw.githubusercontent.com/mysiar-org/st-table/refs/heads/master/doc/table4.png)

## Cloud example
[https://mysiar-org-st-table-st-df.streamlit.app/](https://mysiar-org-st-table-st-df.streamlit.app/)