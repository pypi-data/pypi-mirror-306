import pandas as pd

from crowtit.categorical import categorical_eda
from tests.utils import find_folder


def test_categorical_eda():
    df = pd.DataFrame({
        "col1": ["A", "A", "A", "B", "B", "C", None],
        "col2": ["A", "D", "D", "D", "A", "B", None],
    })
    fig = categorical_eda(
        df=df,
        columns=["col1", "col2"],
        max_n_cols=2,
        one_graph_size=3,
        color="darkred",
        n_top=10,
        font_size=6,
    )
    artifact_folder = find_folder("tests_outputs")
    fig.savefig(f"{artifact_folder}/categorical_eda.png")
