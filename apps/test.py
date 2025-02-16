import marimo

__generated_with = "0.11.5"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md("HEllo world")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
