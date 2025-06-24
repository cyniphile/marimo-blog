# TODO:
- polish up multivariate gaussian interaction 
- some charts are still loading weirdly
- make mobile optimized
  - plot titles cut off
  - side scrolling wide things
  - plots dynamic width
  - make legends better
- make a gpt conversation deriving some that conditional distribution
- rewrite beginning of the blog post ("distribution over functions?")
  - read https://stats.stackexchange.com/questions/376141/what-is-a-distribution-over-functions
  - remember linear regression with epsilon noise term iid, plot those at each point
  - remember what functions are, remember what it is when we plot functions.
  - interactive point adding
  - review: is GP really "distribution over functions"? or a stochastic function over vectors?
- side by side comparison proofread
- https://docs.marimo.io/api/inputs/code_editor/
- all todos

- blog integration
  - comments
  - port other posts
  - favicons, etc

Low priority:
- caching, etc to make better load time
  - https://docs.marimo.io/api/layouts/lazy/#marimo.lazy


first gaussian basics


# Development
- Install `uv` with `pip install uv`
- Install packages with `uv install`
- Run marimo server `uv run marimo edit`

1. Add your marimo files to the `notebooks/` or `apps/` directory
   1. `notebooks/` notebooks are exported with `--mode edit`
   2. `apps/` notebooks are exported with `--mode run`
4. Go to repository **Settings > Pages** and change the "Source" dropdown to "GitHub Actions"

## Including data or assets
To include data or assets in your notebooks, add them to the `public/` directory.
For example, the `apps/charts.py` notebook loads an image asset from the `public/` directory.

```markdown
<img src="public/logo.png" width="200" />
```

And the `notebooks/penguins.py` notebook loads a CSV dataset from the `public/` directory.

```python
import polars as pl
df = pl.read_csv(mo.notebook_location() / "public" / "penguins.csv")
```

## 🧪 Testing

To test the export process, run `scripts/build.py` from the root directory.

```bash
python scripts/build.py
```

This will export all notebooks in a folder called `_site/` in the root directory. Then to serve the site, run:

```bash
python -m http.server -d _site
```

This will serve the site at `http://localhost:8000`.
