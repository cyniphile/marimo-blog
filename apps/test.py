import marimo

__generated_with = "0.14.6"
app = marimo.App(width="full")


@app.cell
def _(alt, arr, df_orig, mat, mo, np, pd):
    x_sim = np.random.multivariate_normal(
        np.array(arr.matrix).reshape(-1), 
        np.array(mat.matrix), 
        2500
    )
    df_sim = pd.DataFrame({"x": x_sim[:, 0], "y": x_sim[:, 1]})

    chart_sim = (
        alt.Chart(df_sim).mark_point().encode(x="x", y="y") + 
        alt.Chart(df_orig).mark_point(color="gray").encode(x="x", y="y")
    )

    mo.vstack([
        mo.md("""
    ."""),
        mo.hstack([arr, mat, chart_sim])
    ])
    return


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd
    return alt, mo, np, pd


@app.cell
def _(mo, np):
    from wigglystuff import Matrix

    mat = mo.ui.anywidget(Matrix(matrix=np.eye(2), mirror=True, step=0.1))
    arr = mo.ui.anywidget(Matrix(rows=1, cols=2, mirror=True, step=0.1))
    return arr, mat


@app.cell
def _(np, pd):
    x_orig = np.random.multivariate_normal(np.array([0, 0]), np.array([[1, 0], [0, 1]]), 2500)
    df_orig = pd.DataFrame({"x": x_orig[:, 0], "y": x_orig[:, 1]})
    return (df_orig,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
