# streamlit-table-select-cell

Streamlit component that allows you to select|click a cell in a table and get its rowId and columnIndex.
This is very useful when you want to dig into the detail of a cell in a pivoted dataframe.

## Installation instructions

```sh
pip install streamlit-table-select-cell
```

## Example

```python
import streamlit as st
import pandas as pd
from st_table_select_cell import st_table_select_cell

st.subheader("Example of st_table_select_cell")

data = pd.DataFrame({'Dataset':['energy','traffic','syn'], 'Test':['ehistory','snapshot','aggmax'], 'PG': [3,6,9], 'TG':[2,5,7]})
st.dataframe(data)

selectedCell = st_table_select_cell(data)
st.write(selectedCell)

if selectedCell:
    rowId = selectedCell['rowId']
    colIndex = selectedCell['colIndex']
    st.info('cell "{}" selected at row {} and col {} ({})'.format(
        data.iat[int(rowId), colIndex], rowId, colIndex, data.columns[colIndex]))
    st.write('selected row data: ', data.iloc[int(rowId)].to_dict())
else:
    st.warning('no select')
```

## Notes
version 0.3.3 only compatible with streamlit 1.30.0
version 0.3.4 is tested and compatible with streamlit 1.37.0 or higher