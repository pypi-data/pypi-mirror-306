import pandas as pd

from vizdata.eda import ExploratoryDataAnalysis


def test_pair_generator():
    df = pd.DataFrame({
        "a": [1, 2, 3],
        "b": ["A", "B", "C"],
    })
    eda = ExploratoryDataAnalysis(df=df)
    eda.cat_futures_eda(one_graph_size=3)
    eda.numeric_futures_eda(log_scale=False, one_graph_size=3)
    # eda.heat_map(one_graph_size=3, sample_count=len(df))
