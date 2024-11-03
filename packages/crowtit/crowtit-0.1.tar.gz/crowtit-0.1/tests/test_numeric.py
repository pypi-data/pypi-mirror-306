import pandas as pd

from crowtit.numeric import numeric_eda
from tests.utils import find_folder


def test_numeric_eda():
    df = pd.DataFrame({
        "col1": [1, 2, 3, 2],
        "col2": [0, -2, -3, -1],
        "col3": [1, 2, -1, 1],
    })
    fig = numeric_eda(
        df=df,
        columns=["col1", "col2", "col3"],
        max_n_cols=3,
        one_graph_size=3,
        color="darkred",
        font_size=6,
        log_scale=False,
    )
    artifact_folder = find_folder("tests_outputs")
    fig.savefig(f"{artifact_folder}/numeric_eda.png")
