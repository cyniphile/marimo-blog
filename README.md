# TODO:
- what is max covariance of a matrix given it's variance
- double variance plot legend cut off
- make mobile optimized
  - matrices can't be changed
  - disable chart zooming
- make a gpt conversation deriving the conditional distribution
- full proofread
- all code todos
- blog integration
  - claude code
  - comments
  - port other posts
  - favicons, etc

Low priority:
- caching, etc to make better load time
  - https://docs.marimo.io/api/layouts/lazy/#marimo.lazy

# Development
- Install `uv` with `pip install uv`
- Install packages with `uv install`
- Run marimo server and watch for changes made in your editor  
  - `uv run marimo edit --watch`

1. Add your marimo files to the `notebooks/` or `apps/` directory
   1. `notebooks/` notebooks are exported with `--mode edit`
   2. `apps/` notebooks are exported with `--mode run`
2. Go to repository **Settings > Pages** and change the "Source" dropdown to "GitHub Actions"

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
