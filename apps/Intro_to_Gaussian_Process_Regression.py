import marimo

__generated_with = "0.11.2"
app = marimo.App()


@app.cell
def _():
    # @title
    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objs as go
    import scipy as sp
    import seaborn as sns
    from IPython.core.display import HTML
    from IPython.display import display
    from matplotlib import pyplot as plt
    from plotly.subplots import make_subplots
    from wigglystuff import Matrix

    np.random.seed(42)
    return (
        HTML,
        Matrix,
        alt,
        display,
        go,
        make_subplots,
        mo,
        np,
        pd,
        plt,
        px,
        sns,
        sp,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # The First Blog Post You Should Read about Gaussian Processes (With Interactive Plots) 

        Is this the 10th blog post you've read about Gaussian Processes and still don't understand them?

        When I set out to learn about Gaussian Processes (really Gaussian Process Regression), I ended up jumping around between many different resources that weren't quite dumbed down enough for me, and it took hours before the core idea hit me. I'm writing this post to get you to core idea in ~30 minutes using interactive plots.

        After that, I'd encourage you to read the references at the end for more details and rigor, and they should make more sense.

        > To understand this post, you should have a basic understanding of linear algebra and statistics.

        > The code to generate this post is hidden, and not necessary for understanding the concepts. But if you know python/numpy you might find it helpful to look under the hood.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Why Gaussian Process Regression?

        I've always been intrigued by Gaussian Processes regression. It has a certain air of mystery about it...one of those models for the cool kids. GPR is supposed to be "beautiful", but also pretty hard to understand. All I knew about it was the following: 

        1. It's a non-linear regression model 
        1. It also does built-in modeling of uncertainties (cool!)

        The following plot from the sci-kit learn documentation shows the output of GP regression model. Note the beautifully curved uncertainty bands. Where does all this come from?

        ![](https://scikit-learn.org/0.17/_images/plot_gp_regression_001.png)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        <!-- I was recently looking at a cool dataset: a list of about 30k different COVID antibodies, each one with a repeated measurement of how well it stuck to COVID spike particles. The better an antibody sticks, the better it is at fighting COVID (more or less). Importantly, each different antibody was measured for its binding strength three times, and the measurements were noisy. So we have a problem with:

        1. Nonlinear relationships 
        1. Noisy data (uncertainty is important!) 
        1. Dataset not huge.

        Finally I have a reason to learn about GPs (and level up how cool I am on Twitter)!  -->

        ## GP Regression: The One Line Definition
        Turns out GP regression can be described in one (somewhat loaded) line:

        **GP Regression: A Multivariate Gaussian Distribution over functions, conditioned on some training data.**

        Hmm. Maybe not so terrible? But how does this connect to the idea of "a nonlinear regression that models uncertainty"?

        Let's unpack this definition bit by bit, starting with "distribution over functions".
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Prequel: Distributions over Functions

        We all know linear regression; it has the form $y = \beta_0 + \beta_1 x$. We have some data $x$ and $y$, and we want to find the $\beta_0$ and $\beta_1$ that describe a line of best fit. We can do this using OLS (ordinary least squares), and we end up with a linear function $f(x) = \beta_0 + \beta_1 x$, that for any $x$ gives us a prediction for $y$.

        But what if we want some notion of the uncertainty of our prediction?

        For example, look at the two plots below:
        """
    )
    return


@app.cell
def _(np, plt, sns):
    _fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    x_reg = np.linspace(-3, 3, 10)
    NOISE_VARIANCE = 1
    y_noise = x_reg + np.random.normal(0, NOISE_VARIANCE, 10)
    LOW_NOISE_VARIANCE = 0.1
    y_low_noise = x_reg + np.random.normal(0, LOW_NOISE_VARIANCE, 10)
    sns.regplot(x=x_reg, y=y_noise, ax=ax1, ci=None).set_title("a")
    sns.regplot(x=x_reg, y=y_low_noise, ax=ax2, ci=None).set_title("b")
    return (
        LOW_NOISE_VARIANCE,
        NOISE_VARIANCE,
        ax1,
        ax2,
        x_reg,
        y_low_noise,
        y_noise,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""

        TODO: reindex to be better
        Even though the data on the left is much more noisy, both linear regressions model the data with the sample simple line. There's no measure of uncertainty. Let's try to add some.

        What if (just for fun) we assumed $\beta_0$ and $\beta_1$ were actually random variables, and that they are normally distributed with variance equal to the variance in the data? Then our linear regression equation would look like this:

        $$
        y = B_0 + B_1 x
        $$

        where we've converted our betas to random variables as follows:

        $$
        B_0 \sim N(\beta_0, \sigma^2)
        $$

        $$
        B_1 \sim N(\beta_1, \sigma^2)
        $$

        This reads "$B_0$ is a random variable distributed according to a Gaussian with mean $\beta_0$ and variance $\sigma^2$".
        We'll set $\sigma^2$ to be the variance of the data about the best fit line (the variance of the residuals). For the plots a and b above, then we'd have:

        $$
        y_a = B_{0a} + B_{1a} x
        $$

        $$
        y_b = B_{0b} + B_{1b} x
        $$

        where $B_0$ and $B_1$ are gaussians with variance equal to the variance of the residuals in each case: $\sigma^2_a$ and $\sigma^2_b$


        Now that the betas are random variables, let's sample from them, and plot the resulting lines:

        (Click the "New Sample" button below)
        """
    )
    return


@app.cell
def _(get_fig):
    get_fig()
    return


@app.cell
def _(
    LOW_NOISE_VARIANCE,
    NOISE_VARIANCE,
    go,
    make_subplots,
    mo,
    np,
    x_reg,
    y_low_noise,
    y_noise,
):
    # Initial parameters
    beta_0 = 0
    beta_1 = 1
    beta_1_1 = np.corrcoef(x_reg, y_noise)[0, 1] * np.std(y_noise) / np.std(x_reg)

    # Define warm and cool color schemes
    colors_subplot1 = ['#ff4d4d', '#ff8533', '#ffcc00', '#ff6b6b', '#ff9966']  # Warm colors
    colors_subplot2 = ['#4d4dff', '#33cc33', '#6666ff', '#00cccc', '#9933ff']  # Cool colors

    # Helper function to calculate figure height based on number of traces
    def calculate_figure_height(num_traces):
        base_height = 400  # Base height for plot
        legend_rows = max(1, (num_traces - 4) // 2)  # Number of additional legend rows needed
        legend_height = 40 + (legend_rows * 20)  # Base legend height + height per row
        return base_height + legend_height

    # Prepare figure and traces
    _fig = make_subplots(rows=1, cols=2, subplot_titles=("a", "b"))
    _fig.update_yaxes(range=[-5, 5], fixedrange=True)
    _fig.update_xaxes(range=[-3, 3], fixedrange=True)

    # Initial height calculation
    initial_height = calculate_figure_height(4)  # Start with 4 traces

    # Update layout with side-by-side grouped legend
    _fig.update_layout(
        height=initial_height,
        legend=dict(
            entrywidth=0.25,
            entrywidthmode="fraction",
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            bgcolor="white",
            bordercolor="LightGrey",
            borderwidth=0,
            itemsizing='constant',
            itemwidth=30,
            groupclick="toggleitem",
            valign='middle',
            xref='container',
            yref='container',
            traceorder="grouped",
            font=dict(size=10),
        ),
        margin=dict(l=4, r=3, t=80, b=80),
    )

    # Lines based on initial betas
    line_1 = x_reg * beta_1_1 + beta_0
    line_2 = x_reg * beta_1 + beta_0

    # Create scatter/line plots for first column with first color scheme
    scatter_fig = go.Scatter(
        x=x_reg, 
        y=y_noise, 
        mode="markers", 
        marker=dict(size=10, color=colors_subplot1[0]), 
        name="Noisy Data",
        legendgroup="Plot A",
        showlegend=True
    )
    line_fig = go.Scatter(
        x=x_reg, 
        y=line_1, 
        mode="lines", 
        line=dict(color=colors_subplot1[1]), 
        name="True Fit Noisy",
        legendgroup="Plot A",
        showlegend=True
    )
    _fig.add_trace(scatter_fig, row=1, col=1)
    _fig.add_trace(line_fig, row=1, col=1)

    # Create scatter/line plots for second column with second color scheme
    scatter_fig2 = go.Scatter(
        x=x_reg, 
        y=y_low_noise, 
        mode="markers", 
        marker=dict(size=10, color=colors_subplot2[0]), 
        name="Low Noise Data",
        legendgroup="Plot B",
        showlegend=True
    )
    line_fig2 = go.Scatter(
        x=x_reg, 
        y=line_2, 
        mode="lines", 
        line=dict(color=colors_subplot2[1]), 
        name="True Fit Low Noise",
        legendgroup="Plot B",
        showlegend=True
    )
    _fig.add_trace(scatter_fig2, row=1, col=2)
    _fig.add_trace(line_fig2, row=1, col=2)

    get_fig, set_fig = mo.state(_fig)

    def add_plot_to_fig(_):
        fig = get_fig()
        beta_0_rand = np.random.normal(beta_0, NOISE_VARIANCE, 1)
        beta_1_rand = np.random.normal(beta_1_1, NOISE_VARIANCE, 1)
        beta_0_rand2 = np.random.normal(beta_0, LOW_NOISE_VARIANCE, 1)
        beta_1_rand2 = np.random.normal(beta_1, LOW_NOISE_VARIANCE, 1)

        line_data = x_reg * beta_1_rand + beta_0_rand
        line_data2 = x_reg * beta_1_rand2 + beta_0_rand2

        # Add new line to left subplot with first color scheme and legend group
        color_idx = len(fig.data) % len(colors_subplot1)
        new_data = {
            "type": "scatter",
            "x": x_reg,
            "y": line_data,
            "mode": "lines",
            "line": {"color": colors_subplot1[color_idx]},
            "xaxis": "x",
            "yaxis": "y",
            "name": f"$B_{{0a}}: {beta_0_rand[0]:.2f}, B_{{1a}}: {beta_1_rand[0]:.2f}$",
            "legendgroup": "Plot A",
        }
        fig.add_trace(new_data, row=1, col=1)

        # Add new line to right subplot with second color scheme and legend group
        color_idx = len(fig.data) % len(colors_subplot2)
        fig.add_trace(
            {
                "type": "scatter",
                "x": x_reg,
                "y": line_data2,
                "mode": "lines",
                "line": {"color": colors_subplot2[color_idx]},
                "xaxis": "x2",
                "yaxis": "y2",
                "name": f"$B_{{0b}}: {beta_0_rand2[0]:.2f}, B_{{1b}}: {beta_1_rand2[0]:.2f}$",
                "legendgroup": "Plot B",
            },
            row=1,
            col=2,
        )
        
        # Update figure height based on new number of traces
        new_height = calculate_figure_height(len(fig.data))
        fig.update_layout(height=new_height)
        
        set_fig(fig)
        return

    button = mo.ui.button(value=0, on_click=add_plot_to_fig, label="New Sample", kind="neutral")

    def reset(_):
        fig = get_fig()
        fig["data"] = fig["data"][:4]
        # Reset height to initial value
        fig.update_layout(height=calculate_figure_height(4))
        set_fig(fig)

    clear_button = mo.ui.button(value=0, on_click=reset, label="Reset", kind="danger")

    mo.hstack([button, clear_button])
    return (
        add_plot_to_fig,
        beta_0,
        beta_1,
        beta_1_1,
        button,
        calculate_figure_height,
        clear_button,
        colors_subplot1,
        colors_subplot2,
        get_fig,
        initial_height,
        line_1,
        line_2,
        line_fig,
        line_fig2,
        reset,
        scatter_fig,
        scatter_fig2,
        set_fig,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Each time you click the button, a new sample $\beta_0, \beta_1$ are drawn from the distributions of $B_0$ and $B_1$ (one set of betas for the noisy data on the left and one set for the less noisy on the right), and the corresponding lines are plotted.

        Notice what we've created: it's a distribution over _functions_. Each sample from  $y = B_0 + B_1 x$ is a different function $f(x)$. Also notice that as you sample more and more, the "spread" or uncertainty of the original fit becomes more and more apparent. You can also see that the uncertainty is higher in the noisier data.

        > This framework is just to develop for intuition for distributions over functions. For a more rigorous take, check out the bayesian linear regression section [here](https://gaussianprocess.org/gpml/chapters/RW.pdf#page=26&zoom=100,240,358).

        Returning to our original definition, we've checked off one core idea:

        **GP Regression: A Multivariate Gaussian <font color="#32a852">Distribution over functions</font>, conditioned on some training data.**

        What if we want to model a non-linear relationship? Now we're getting closer to the core idea of GPs. But of course, before we get to Gaussian processes, we have to talk about Gaussians.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Gaussians...and Multivariate Gaussians!

        The Gaussian, the bell curve, the normal distribution, we've seen it before. It's defined by 

        $$
        Y \sim N(\mu, \sigma^2)
        $$

        where $\mu$ is the mean and $\sigma^2$ is the variance. You can play around with the parameters of the distribution below. Each time you change the sliders, 10,000 samples are drawn from the distribution and plotted as a histogram.
        """
    )
    return


@app.cell
def _(get_fig_hist):
    get_fig_hist()
    return


@app.cell
def _(go, mo, np):
    # 1. Create the initial figure

    SIZE = 5000
    START = -10
    END = 10
    x = np.random.normal(0, 1, size=SIZE)
    hist_trace = go.Histogram(
        x=x, xbins=dict(start=START, end=END, size=0.1)  # whatever bin width you want
    )
    fig_hist = go.Figure(hist_trace)
    fig_hist.update_layout(
        title="Normal Distribution Histogram (µ=0.00, σ=1.00)",
        xaxis=dict(title="Value", range=[START, END], fixedrange=True),
        yaxis=dict(title="Count"),
    )

    # 2. Store the figure and the slider states
    get_fig_hist, set_fig_hist = mo.state(fig_hist)
    fig_hist.update_layout(
        title="Normal Distribution Histogram (µ=0.00, σ=1.00)",
        xaxis=dict(title="Value", range=[START, END], fixedrange=True),
        yaxis=dict(
            title="Count", range=[0, int(SIZE * 0.1)], fixedrange=True
        ),  # Adjust the y-axis range as needed
    )
    mean_state, set_mean_state = mo.state(0.0)
    variance_state, set_variance_state = mo.state(1.0)

    # 3. Function that updates the figure
    def update_histogram():
        fig = get_fig_hist()  # retrieve current figure from state
        x_new = np.random.normal(mean_state(), variance_state(), size=SIZE)
        fig.data[0].x = x_new
        fig.update_layout(
            title=(
                f"Normal Distribution Histogram (µ={mean_state():.2f}, "
                f"σ={variance_state():.2f})"
            )
        )
        set_fig_hist(fig)  # store the updated figure

    # 4. Handlers for slider changes
    def on_mean_change(m):
        set_mean_state(m)
        update_histogram()

    def on_variance_change(v):
        set_variance_state(v)
        update_histogram()

    # 5. Create the sliders
    mean_slider = mo.ui.slider(
        value=mean_state(), start=-5, stop=5, step=0.1, on_change=on_mean_change, label="Mean"
    )
    variance_slider = mo.ui.slider(
        value=variance_state(),
        start=0.1,
        stop=5,
        step=0.1,
        on_change=on_variance_change,
        label="Variance",
    )

    # 6. Lay out sliders and the figure
    mo.hstack([mean_slider, variance_slider])
    return (
        END,
        SIZE,
        START,
        fig_hist,
        get_fig_hist,
        hist_trace,
        mean_slider,
        mean_state,
        on_mean_change,
        on_variance_change,
        set_fig_hist,
        set_mean_state,
        set_variance_state,
        update_histogram,
        variance_slider,
        variance_state,
        x,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        What about multivariate Gaussians? That is, a Gaussian distribution but with more than one variable. They are basically the same thing, but instead of having a single mean and variance, there's there's a mean vector and a covariance matrix. 


        So while a single Gaussian is this:

        $$
        Y \sim N(\mu, \sigma^2)
        $$

        Where $\mu$ is the mean and $\sigma$ is the variance, a multivariate Gaussian is this:

        $$
        \textbf{Y} \sim N(\boldsymbol{\mu}, \Sigma)
        $$

        Where $\boldsymbol{\mu}$ is a vector of means, $\Sigma$ is a covariance matrix.

        $$
        \boldsymbol{\mu} = \begin{bmatrix}
        \mu_1 \\
        \mu_2 \\
        \vdots \\
        \mu_n
        \end{bmatrix},
        $$

        $$
        \qquad
        \Sigma = \begin{bmatrix}
        \sigma_{11} & \sigma_{12} & \dots & \sigma_{1n} \\
        \sigma_{21} & \sigma_{22} & \dots & \sigma_{2n} \\
        \vdots & \vdots & \ddots & \vdots \\
        \sigma_{n1} & \sigma_{n2} & \dots & \sigma_{nn}
        \end{bmatrix}.
        $$

        In the above expressions, $\mu_i$ is the mean of the $i$ th component of $\textbf{Y}$

        In this case when we sample from $\textbf{Y}$, we get a vector $\textbf{Y} = [Y_1, Y_2, \dots, Y_n]^T$,  instead of just a single valueWhat about multivariate Gaussians? That is, a Gaussian distribution but with more than one variable. They are basically the same thing, but instead of having a single mean and variance, there's there's a mean vector and a covariance matrix. 

        So while a single Gaussian is this:

        $$
        Y \sim N(\mu, \sigma^2)
        $$

        Where $\mu$ is the mean and $\sigma$ is the variance, a multivariate Gaussian is this:

        $$
        \textbf{Y} \sim N(\boldsymbol{\mu}, \Sigma)
        $$

        Where $\boldsymbol{\mu}$ is a vector of means, $\Sigma$ is a covariance matrix.

        $$
        \boldsymbol{\mu} = \begin{bmatrix}
        \mu_1 \\
        \mu_2 \\
        \vdots \\
        \mu_n
        \end{bmatrix},
        $$

        $$
        \qquad
        \Sigma = \begin{bmatrix}
        \sigma_{11} & \sigma_{12} & \dots & \sigma_{1n} \\
        \sigma_{21} & \sigma_{22} & \dots & \sigma_{2n} \\
        \vdots & \vdots & \ddots & \vdots \\
        \sigma_{n1} & \sigma_{n2} & \dots & \sigma_{nn}
        \end{bmatrix}.
        $$

        In the above expressions, $\mu_i$ is the mean of the $i$ th component of $\textbf{Y}$

        In this case when we sample from $\textbf{Y}$, we get a vector $\textbf{Y} = [Y_1, Y_2, \dots, Y_n]^T$,  instead of just a single value
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Nothing too crazy right? Well, except that the multivariate normal distribution has a covariance _matrix_, not just a variance.

        In the covariance matrix we specify not only the variance of each variable, but also the covariance between each variable and every other. Each of the $n$ variables in a multivariate Gaussian can be correlated with each other. Below is an overhead view of a bunch of samples for a 2D multivariate Gaussian distribution. You can interactively change the covariance matrix to see how it affects the distribution.
        """
    )
    return


@app.cell
def _(Matrix, alt, mo, np, pd):
    x_orig = np.random.multivariate_normal(np.array([0, 0]), np.array([[1, 0], [0, 1]]), 2500)
    df_orig = pd.DataFrame({"x": x_orig[:, 0], "y": x_orig[:, 1]})

    mat = mo.ui.anywidget(Matrix(matrix=np.eye(2), mirror=True, step=0.1))
    arr = mo.ui.anywidget(Matrix(rows=1, cols=2, mirror=True, step=0.1))
    x_sim = np.random.multivariate_normal(
        np.array(arr.matrix).reshape(-1), np.array(mat.matrix), 2500
    )
    df_sim = pd.DataFrame({"x": x_sim[:, 0], "y": x_sim[:, 1]})

    chart_sim = alt.Chart(df_sim).mark_point().encode(x="x", y="y")

    mo.vstack([mo.hstack([arr, mat, chart_sim])])
    return arr, chart_sim, df_orig, df_sim, mat, x_orig, x_sim


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Note that if you change the diagonal elements, the variance of one or the other variable will change (look at the scale of axes). If you change the off-diagonal elements, the covariance between the two variables will change. 

        You also probably saw that the matrix has to be symmetric and with positive diagonals. Why? Well think about what covariance is: its how two variables vary together. It doesn't make sense for Cov(X,Y) != Cov(Y,X). And it doesn't make sense for Cov(X,X) — that is, Var(X) — to be negative.

        Also note that while the combined joint distribution changes form, each of the individual distributions is still a Gaussian. That is to say, the distribution of $X_1$ is still a gaussian, and the distribution of $X_2$ is still a Gaussian. The only thing that changes is the covariance between the two variables.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Gaussian Distribution Over Functions

        So far we've visualized a multivariate Gaussian of just two variables, but you can imagine taking this into many many dimensions. That is to say, many many Gaussian random variables that may or may not be correlated with each other according to some big covariance matrix.

        In order to think about more than two dimensions, we'll need to visualize our distributions differently. Let's start with a 1-D Gaussian. We'll draw samples from the distribution and plot them below:
        """
    )
    return


@app.cell
def _(get_fig2):
    get_fig2()
    return


@app.cell
def _(go, mo, np):
    # 1) Create and store an initial figure in Marimo state
    initial_fig = go.Figure(
        data=[go.Scatter(mode="markers")],
        layout=go.Layout(title="Samples from a 1-D Gaussian Distribution"),
    )
    get_fig2, set_fig2 = mo.state(initial_fig)
    get_clicks2, set_clicks2 = mo.state(0)

    # 2) Define the callbacks that change the figure
    def add_sample(_):
        """Add a new random sample (1 point) to the figure."""
        fig = get_fig2()
        # We just stack data on top of the existing figure
        x = ["1"]
        y = np.random.normal(size=1)
        scatter = go.Scatter(x=x, y=y, mode="markers", name=f"Sample {get_clicks2()}")
        fig.add_trace(scatter)
        set_fig2(fig)  # update our global figure state
        set_clicks2(get_clicks2()+1)

    def clear_data(_):
        """Clear all the data from the figure."""
        fig = get_fig2()
        fig.data = []
        set_fig2(fig)
        set_clicks2(0)

    # 3) Create the UI buttons, each calling its respective callback
    btn_new_sample = mo.ui.button(
        value=0, 
        on_click=add_sample, 
        label="New Sample", 
        kind="neutral"
    )
    btn_clear = mo.ui.button(
        value=get_clicks2(), 
        on_click=clear_data, 
        label="Clear", 
        kind="danger"
    )

    # 4) Lay out the two buttons and the figure
    mo.hstack([btn_new_sample, btn_clear])
    return (
        add_sample,
        btn_clear,
        btn_new_sample,
        clear_data,
        get_clicks2,
        get_fig2,
        initial_fig,
        set_clicks2,
        set_fig2,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Each new sample is drawn from a normal distribution with mean 0 and variance 1.

        What if we want to sample from a multivariate normal distribution? Well, this time $\textbf{Y}$ is a _vector_ of random variables. If $\textbf{Y}$ is 2-d then $\textbf{Y} = [Y_1, Y_2]^T$, so each sample is a vector of two values which we'll plot each on their own part of the X-axis.
        """
    )
    return


@app.cell
def _(get_fig_2d):
    get_fig_2d()
    return


@app.cell
def _(go, mo, np):
    # 2D Figure: "Samples from a 2-D Gaussian Distribution"
    init_scatter_2d = go.Scatter(mode="markers")
    init_layout_2d = go.Layout(title="Samples from a 2-D Gaussian Distribution")
    init_fig_2d = go.Figure(data=[init_scatter_2d], layout=init_layout_2d)

    get_fig_2d, set_fig_2d = mo.state(init_fig_2d)
    get_clicks_2d, set_clicks_2d = mo.state(0)

    def add_sample_2d(_):
        fig_2d = get_fig_2d()
        x_2d = ["1", "2"]
        y_2d = np.random.normal(size=2)
        new_scatter_2d = go.Scatter(
            x=x_2d,
            y=y_2d,
            mode="markers",
            name=f"Sample {get_clicks_2d()}"
        )
        fig_2d.add_trace(new_scatter_2d)
        set_fig_2d(fig_2d)
        set_clicks_2d(get_clicks_2d() + 1)

    def clear_data_2d(_):
        fig_2d = get_fig_2d()
        fig_2d.data = []
        set_fig_2d(fig_2d)
        set_clicks_2d(0)

    btn_new_sample_2d = mo.ui.button(
        value=0,
        on_click=add_sample_2d,
        label="New Sample",
        kind="neutral"
    )
    btn_clear_2d = mo.ui.button(
        value=get_clicks_2d(),
        on_click=clear_data_2d,
        label="Clear",
        kind="danger"
    )

    mo.hstack([btn_new_sample_2d, btn_clear_2d])
    return (
        add_sample_2d,
        btn_clear_2d,
        btn_new_sample_2d,
        clear_data_2d,
        get_clicks_2d,
        get_fig_2d,
        init_fig_2d,
        init_layout_2d,
        init_scatter_2d,
        set_clicks_2d,
        set_fig_2d,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""So now each time we sample from a bivariate normal distribution, we get a vector of two numbers, which we plot as two connected points. Now let's look at a 3-D Gaussian,  $\textbf{Y}_{3D} = [Y_1, Y_2, Y_3]^T$,""")
    return


@app.cell
def _(get_fig_3d):
    get_fig_3d()
    return


@app.cell
def _(go, mo, np):
    # 3D Figure: "Samples from a 3-D Gaussian Distribution"
    init_scatter_3d = go.Scatter(mode="markers")
    init_layout_3d = go.Layout(title="Samples from a 3-D Gaussian Distribution")
    init_fig_3d = go.Figure(data=[init_scatter_3d], layout=init_layout_3d)

    get_fig_3d, set_fig_3d = mo.state(init_fig_3d)
    get_clicks_3d, set_clicks_3d = mo.state(0)

    def add_sample_3d(_):
        fig_3d = get_fig_3d()
        x_3d = ["1", "2", "3"]
        y_3d = np.random.normal(size=3)
        new_scatter_3d = go.Scatter(
            x=x_3d,
            y=y_3d,
            mode="markers",
            name=f"Sample {get_clicks_3d()}"
        )
        fig_3d.add_trace(new_scatter_3d)
        set_fig_3d(fig_3d)
        set_clicks_3d(get_clicks_3d() + 1)

    def clear_data_3d(_):
        fig_3d = get_fig_3d()
        fig_3d.data = []
        set_fig_3d(fig_3d)
        set_clicks_3d(0)

    btn_new_sample_3d = mo.ui.button(
        value=0,
        on_click=add_sample_3d,
        label="New Sample",
        kind="neutral"
    )
    btn_clear_3d = mo.ui.button(
        value=get_clicks_3d(),
        on_click=clear_data_3d,
        label="Clear",
        kind="danger"
    )

    mo.hstack([btn_new_sample_3d, btn_clear_3d])
    return (
        add_sample_3d,
        btn_clear_3d,
        btn_new_sample_3d,
        clear_data_3d,
        get_clicks_3d,
        get_fig_3d,
        init_fig_3d,
        init_layout_3d,
        init_scatter_3d,
        set_clicks_3d,
        set_fig_3d,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Now let's take it to an extreme: a 100-D Gaussian! $\textbf{Y}_{100D} = [Y_1, Y_2, Y_3, \dots, Y_{100}]^T$, so every sample is a vector of 100 random values.""")
    return


@app.cell
def _(get_fig_100d):
    get_fig_100d()
    return


@app.cell
def _(go, mo, np):
    # 100D Figure: "Samples from a 100-D Gaussian Distribution"
    init_scatter_100d = go.Scatter(mode="markers")
    init_layout_100d = go.Layout(title="Samples from a 100-D Gaussian Distribution")
    init_fig_100d = go.Figure(data=[init_scatter_100d], layout=init_layout_100d)

    get_fig_100d, set_fig_100d = mo.state(init_fig_100d)
    get_clicks_100d, set_clicks_100d = mo.state(0)

    def add_sample_100d(_):
        fig_100d = get_fig_100d()
        x_vals_100d = np.arange(100)
        y_vals_100d = np.random.normal(size=100)
        new_scatter_100d = go.Scatter(
            x=x_vals_100d,
            y=y_vals_100d,
            mode="markers",
            name=f"Sample {get_clicks_100d()}"
        )
        fig_100d.add_trace(new_scatter_100d)
        set_fig_100d(fig_100d)
        set_clicks_100d(get_clicks_100d() + 1)

    def connect_samples_100d(_):
        fig_100d = get_fig_100d()
        for trace in fig_100d.data:
            trace["mode"] = "lines+markers"
        set_fig_100d(fig_100d)

    def clear_data_100d(_):
        fig_100d = get_fig_100d()
        fig_100d.data = []
        set_fig_100d(fig_100d)
        set_clicks_100d(0)

    btn_new_sample_100d = mo.ui.button(
        value=0,
        on_click=add_sample_100d,
        label="New Sample",
        kind="neutral"
    )
    btn_connect_100d = mo.ui.button(
        label="Connect Samples",
        on_click=connect_samples_100d,
        kind="neutral"
    )
    btn_clear_100d = mo.ui.button(
        value=get_clicks_100d(),
        on_click=clear_data_100d,
        label="Clear",
        kind="danger"
    )

    mo.hstack([btn_new_sample_100d, btn_connect_100d, btn_clear_100d])
    return (
        add_sample_100d,
        btn_clear_100d,
        btn_connect_100d,
        btn_new_sample_100d,
        clear_data_100d,
        connect_samples_100d,
        get_clicks_100d,
        get_fig_100d,
        init_fig_100d,
        init_layout_100d,
        init_scatter_100d,
        set_clicks_100d,
        set_fig_100d,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Cool, so now we can visualize samples from a 100-D Gaussian in this kinda of weird way. How is this useful? And how does this relate to a Gaussian Process regression?

        You'll notice the above plot has a "Connect Samples" button. If you click it, each variable in a given sample gets connected to the next. Try it out!

        Do these connected samples remind you of anything? Maybe a certain class of elementary mathematical objects?

        If you thought "functions" then you are getting what I'm going for here. Each sample from the 100-D Gaussian is starting to look like some curve where, for any x-coordinate (which is just the index of the vector output of the multivariate gaussian) you can look up a y-value. So this kinda-sorta function can be defined as 

        $$
        f(x) = Y_{x}
        $$

        given a multivariate Gaussian $Y = [Y_1, Y_2, Y_3, \dots, Y_{x}]^T \sim N(\boldsymbol{\mu}, \Sigma)$.

        But remember what each different colored curve is: it's a sample from a multivariate normal distribution. It's almost like the 100-D Gaussian specifies a _distribution over functions_...

        <img src="https://i.kym-cdn.com/entries/icons/original/000/007/630/conspiracykeanu.jpg" width="340" height="200" />

        _Almost_. The 100-D Gaussian really only specifies a distribution over 100 discrete values, so it's not quite a distribution over functions $f(x)$ that can take _any_ value of $x$. Hold that thought for now, we'll return to this later. 

        But first you might have some questions. Remember, the above plot was made by taking a few samples from 100-D gaussian, $\textbf{Y}_{100D} \sim N(\boldsymbol{\mu}, \Sigma)$

        But I didn't tell you what $\boldsymbol{\mu}$ and $\Sigma$ were. Well, I actually used a mean vector of all zeros:

        $$
        \boldsymbol{\mu} =  \begin{bmatrix}
        0 \\
        0 \\
        \vdots \\
        0
        \end{bmatrix},
        $$

        and for the covariance matrix I simply used the Identity matrix.

        $$
        \Sigma = \begin{bmatrix}
        1 & 0 & \dots & 0 \\
        0 & 1 & \dots & 0 \\
        \vdots & \vdots & \ddots & \vdots \\
        0 & 0 & \dots & 1
        \end{bmatrix}.
        $$

        Since this covariance matrix is really big, let's visualize it with a heatmap:
        """
    )
    return


@app.cell
def _(np, plt, sns):
    # @title
    sns.heatmap(np.identity(100))
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""This means that each of the variables in our multivariate normal distribution are.....???? (hover over the text below to see the answer)""")
    return


@app.cell
def _(HTML):
    # @title
    HTML(
        """
    <span class="hover-text">Hover for answer</span>:

    <span class="hidden-text">INDEPENDENT!</span>

    <style>
      .hidden-text {
        display: none;
      }

      .hover-text:hover + .hidden-text {
        display: inline;
        font: 50px;
      }
    </style>
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        No variable has any covariance with any other, so you than think of this multivariate Gaussian as simply 100 separate Gaussians, each with mean = 0 and variance 1. This is why the curves we plotted above are so all over the place: each point is randomly bouncing up and down with no influence from its neighbors.

        What if we add some non-zero values to the covariance matrix that are off-diagonal? 

        >Remember the diagonal elements of the matrix at row and column $i$ is $Cov(Y_i, Y_i) = Var(Y_i)$ while the off-diagonal elements at $i,j$ are $Cov(Y_i, Y_j)$. 

        For example, check out the covariance matrix below:
        """
    )
    return


@app.cell
def _(np, pairwise_rbf, pd, slider_l, sns):
    _xa = np.arange(0, 100, 1).reshape(1, -1).T
    _xb = np.arange(0, 100, 1).reshape(1, -1).T
    C = pd.DataFrame(pairwise_rbf(_xa, _xb, slider_l.value))
    sns.heatmap(C).set_title(f"$ℓ$={slider_l.value}")
    return (C,)


@app.cell
def _(mo):
    slider_l = mo.ui.slider(start=1, stop=10, value=5, label="Value of ℓ")
    slider_l
    return (slider_l,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        It looks very similar, but it's "fuzzier" around the diagonal. Think about what type of values you would expect from a Gaussian with this covariance matrix.

        Try playing around with the l slider TODO:

        It's saying that variables near each other are more correlated than variables far away. For example variable 1 is more correlated with variable 2 than it is with variable 100. Let visualize some samples from a 100-d Gaussian with this new covariance matrix. But before you hit the "sample" button, what do you think these new curves will look like?
        """
    )
    return


@app.cell
def _(get_fig_fuzzy):
    get_fig_fuzzy()
    return


@app.cell
def _(go, mo, np, pairwise_rbf, slider_l):
    # 1) Create an initial figure
    init_scatter_fuzzy = go.Scatter(mode="markers")
    init_layout_fuzzy = go.Layout(
        title='Samples from a 100-D Gaussian Distribution with "Fuzzy" Covariance'
    )
    init_fig_fuzzy = go.Figure(data=[init_scatter_fuzzy], layout=init_layout_fuzzy)

    # 2) Store the figure in Marimo's state, plus a sample-count state
    get_fig_fuzzy, set_fig_fuzzy = mo.state(init_fig_fuzzy)
    get_clicks_fuzzy, set_clicks_fuzzy = mo.state(0)

    def add_sample_fuzzy(_):
        """Add a new random sample using a 'fuzzy' covariance matrix."""
        fig_fuzzy = get_fig_fuzzy()
        x = np.linspace(0, 100, 100)
        cov = pairwise_rbf(x.reshape(-1, 1), x.reshape(-1, 1), l=slider_l.value)
        y = np.random.multivariate_normal(mean=np.zeros(100), cov=cov, size=1)[0]
        sample_num = get_clicks_fuzzy()
        new_scatter_fuzzy = go.Scatter(
            x=x,
            y=y,
            mode="lines+markers",
            name=f"Sample {sample_num}",
        )
        fig_fuzzy.add_trace(new_scatter_fuzzy)
        set_fig_fuzzy(fig_fuzzy)
        set_clicks_fuzzy(sample_num + 1)

    def clear_data_fuzzy(_):
        """Clear all data from the fuzzy-covariance figure."""
        fig_fuzzy = get_fig_fuzzy()
        fig_fuzzy.data = []
        set_fig_fuzzy(fig_fuzzy)
        set_clicks_fuzzy(0)

    # 3) Create the UI buttons
    btn_new_sample_fuzzy = mo.ui.button(
        label="New Sample",
        on_click=add_sample_fuzzy,
        kind="neutral"
    )
    btn_clear_fuzzy = mo.ui.button(
        value=get_clicks_fuzzy(),
        on_click=clear_data_fuzzy,
        label="Clear",
        kind="danger"
    )

    # 4) Layout: Place the buttons side-by-side and display the figure
    mo.hstack([btn_new_sample_fuzzy, btn_clear_fuzzy])
    return (
        add_sample_fuzzy,
        btn_clear_fuzzy,
        btn_new_sample_fuzzy,
        clear_data_fuzzy,
        get_clicks_fuzzy,
        get_fig_fuzzy,
        init_fig_fuzzy,
        init_layout_fuzzy,
        init_scatter_fuzzy,
        set_clicks_fuzzy,
        set_fig_fuzzy,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Cool! They are now much smoother. This is because the variables near each other are more correlated, so nearby points are more likely to be similar. This smooths out the curves.

        Now we can see that by changing the covariance matrix, we can control the shape of the functions that our multivariate normal distribution produces.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ### Making these "functions" into Functions
        We've been throwing around the word "functions" a lot now, but we still never resolved the problem that these samples are really just 100-D vectors. Sure we can connect the points with little lines, but that's not the same as a function. How do we get a distribution over true functions?

        The answer lies in how we define the covariance and mean of our multivariate Gaussian. So far we've been manually inputting some mean vector and covariance matrix. Since these are objects with discrete, finite elements, we can't really think of the distributions they define as functions. But what if we could redefine these objects (the mean and covariance) as functions? 

        Mathematically:

        $$
        \boldsymbol{\mu} = m(\textbf{x}) \\
        \Sigma = k(\textbf{x, x})
        $$

        Now for whatever $x$ we are interested in, we can sample from a multivariate Gaussian with mean $m(\textbf{x})$ and covariance $k(\textbf{x, x})$. This is one of those mathematical tricks that's so simple it's hard to understand, or maybe feels like cheating, so let's go through an example. 

        Say we want to sample from a few specific real number $\textbf{x} = [-\pi, \pi, 2\pi]^T$ (some multiples of pi, as in 3.141...). First let's define a mean function $m(\textbf{x})$. We can use anything we like, so let's so something really simple: $m(\textbf{x}) = \textbf{x}$. 

        For the covariance function $k(\textbf{x, x})$, we need a function of x that generates a symmetric matrix with a positive diagonal (otherwise it would not be a valid covariance). Again let's just do something really simple: $k(\textbf{x}, \textbf{x}) = \operatorname{diag}(\textbf{x} \odot \textbf{x} )$, where we take $\odot$ to mean the element-wise product of $\textbf{x}$ with $\textbf{x}$.

        > You maybe be wondering, "why define the covariance function as $k(\textbf{x, x})$ instead of simply $k(\textbf{x})$?". The reason is that covariance functions in general calculate a covariance between two vectors that are not necessarily the same. Here we are just calculating the covariance of $\textbf{x}$ with itself, but this will not always be the case...

        So if we put out test vector into these functions we get:

        $$
        \boldsymbol{\mu} = m(\textbf{x}) = \textbf{x} = [-\pi, \pi, 2\pi]^T\\
        $$

        $$
        \Sigma = k(\textbf{x}, \textbf{x}) = \operatorname{diag}(\textbf{x}\odot\textbf{x}) = \begin{bmatrix}
        (-\pi)^2 & 0 & 0 \\
        0 & (\pi)^2 & 0 \\
        0 & 0 & (2\pi)^2
        \end{bmatrix}
        $$

        Now we can sample from a multivariate Gaussian at these specific values of $x$:
        """
    )
    return


@app.cell
def _(get_fig_real):
    get_fig_real()
    return


@app.cell
def _(go, mo, np):
    # Define the index points, mean function, and covariance function
    x_specific = np.array([-np.pi, np.pi, 2 * np.pi])
    _m = lambda x: x
    _k = lambda x: np.diag(x**2)

    # 1) Create a figure with an initial (empty) scatter trace
    init_scatter_real = go.Scatter(mode="markers")
    init_layout_real = go.Layout(title="Samples from a Multivariate Gaussian at Real-Valued Indices")
    init_fig_real = go.Figure(data=[init_scatter_real], layout=init_layout_real)

    # 2) Use Marimo state to keep track of the figure and click count
    get_fig_real, set_fig_real = mo.state(init_fig_real)
    get_clicks_real, set_clicks_real = mo.state(0)

    # 3) Define the callbacks
    def add_sample_real(_):
        fig_real = get_fig_real()
        # Build covariance and mean
        cov = _k(x_specific)
        mean = _m(x_specific)
        # Draw one sample from the multivariate normal
        y = np.random.multivariate_normal(mean=mean, cov=cov, size=1)[0]

        sample_num = get_clicks_real()
        new_scatter_real = go.Scatter(
            x=x_specific,
            y=y,
            mode="lines+markers",
            name=f"Sample {sample_num}",
        )
        fig_real.add_trace(new_scatter_real)

        set_fig_real(fig_real)
        set_clicks_real(sample_num + 1)

    def clear_data_real(_):
        fig_real = get_fig_real()
        fig_real.data = []
        set_fig_real(fig_real)
        set_clicks_real(0)

    # 4) Build UI: two buttons + the figure
    btn_new_sample_real = mo.ui.button(
        label="New Sample",
        on_click=add_sample_real,
        kind="neutral"
    )
    btn_clear_real = mo.ui.button(
        value=get_clicks_real(),
        on_click=clear_data_real,
        label="Clear",
        kind="danger"
    )

    mo.hstack([btn_new_sample_real, btn_clear_real])
    return (
        add_sample_real,
        btn_clear_real,
        btn_new_sample_real,
        clear_data_real,
        get_clicks_real,
        get_fig_real,
        init_fig_real,
        init_layout_real,
        init_scatter_real,
        set_clicks_real,
        set_fig_real,
        x_specific,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""But now that we've defined our mean and covariance functions, we can sample from a multivariate Gaussian at any value of $x$ we want. For example, let's sample at 100 evenly spaced real values of $x$ between -1 and 1. All we do is plug these values into our mean and covariance functions, and then sample from the resulting multivariate Gaussian.""")
    return


@app.cell
def _(get_fig_100real):
    get_fig_100real()
    return


@app.cell
def _(go, mo, np):
    # We assume you've already defined:
    x_real_big = np.linspace(-1, 1, 100)
    # m = lambda x: x
    # k = lambda x: np.diag(x**2)
    m = lambda x: x
    k = lambda x: np.diag(x**2)

    # 1) Create the initial figure
    init_scatter_100_real = go.Scatter(mode="markers")
    init_layout_100_real = go.Layout(
        title="Samples from a 100-D Multivariate Gaussian at Real-Valued Indices"
    )
    init_fig_100_real = go.Figure(data=[init_scatter_100_real], layout=init_layout_100_real)

    # 2) Store the figure and a sample counter in Marimo's state
    get_fig_100real, set_fig_100real = mo.state(init_fig_100_real)
    get_clicks_100real, set_clicks_100real = mo.state(0)

    def add_sample_100real(_):
        """Draw one random sample from a 100-D Gaussian (diag covariance = x^2)."""
        fig_100r = get_fig_100real()
        sample_num = get_clicks_100real()

        # Build covariance and mean from the user-defined functions
        cov_100 = k(x_real_big)
        mean_100 = m(x_real_big)
        # Draw a single 100-D sample
        y_samp = np.random.multivariate_normal(mean=mean_100, cov=cov_100, size=1)[0]

        new_scatter_100r = go.Scatter(
            x=x_real_big,
            y=y_samp,
            mode="lines+markers",
            name=f"Sample {sample_num}",
        )
        fig_100r.add_trace(new_scatter_100r)

        set_fig_100real(fig_100r)
        set_clicks_100real(sample_num + 1)

    def clear_data_100real(_):
        """Remove all existing traces."""
        fig_100r = get_fig_100real()
        fig_100r.data = []
        set_fig_100real(fig_100r)
        set_clicks_100real(0)

    # 3) Create the UI: Two buttons + the figure
    btn_new_sample_100real = mo.ui.button(
        label="New Sample",
        on_click=add_sample_100real,
        kind="neutral"
    )

    btn_clear_100real = mo.ui.button(
        label="Clear",
        on_click=clear_data_100real,
        kind="danger"
    )

    mo.hstack([btn_new_sample_100real, btn_clear_100real])
    return (
        add_sample_100real,
        btn_clear_100real,
        btn_new_sample_100real,
        clear_data_100real,
        get_clicks_100real,
        get_fig_100real,
        init_fig_100_real,
        init_layout_100_real,
        init_scatter_100_real,
        k,
        m,
        set_clicks_100real,
        set_fig_100real,
        x_real_big,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Now we've truly got a distribution over functions!

        If we want the distribution at _any_ value $x$, we can just plug it in to the mean and covariance functions and voila! We just need to define a mean and valid covariance function that we like, and we can sample from a multivariate Gaussian at any value of $x$ we want. 

        By the way, "covariance functions" are usually referred to by a fancy name: **kernel functions**. Remember this plot of a covariance matrix from earlier?
        """
    )
    return


@app.cell
def _(C, slider_l, sns):
    sns.heatmap(C).set_title(f"$ℓ$={slider_l.value}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        This covariance we actually generated by using a specific kernel function called the squared exponential kernel, a.k.a. the Gaussian kernel a.k.a the radial basis function (RBF) kernel. I'll refer to it as the RBF kernel for this post.

        It's defined as:	

        $$
        k(\textbf{x}) = \exp\left(-\frac{1}{2ℓ^2} ||\textbf{x} - \textbf{x}||^2\right)
        $$

        where $||\textbf{x} - \textbf{x}||^2$ is the element-wise squared difference matrix between each element of $x$ with each other element, and $ℓ$ is an adjustable parameter. 

        No need to worry about the math here too closely. The important thing to note is that the RBF kernel is a function of $\textbf{x}$ that generates a positive semidefinite matrix. It's covariance function, a.k.a. kernel, and it happens to be one of the most useful kernels in the real-world.
        """
    )
    return


@app.cell
def _(mo, np, sns, sp):
    # Example output for an RBF kernel, given a simple vector x_test
    def pairwise_rbf(xa, xb, l=5.0):
        sq_norm = (-0.5/l**2) * sp.spatial.distance.cdist(xa, xb, 'sqeuclidean')
        return np.exp(sq_norm)

    x_test = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
    rbf_output = pairwise_rbf(x_test, x_test, l=1)

    mo.show_code(sns.heatmap(rbf_output, annot=True))
    return pairwise_rbf, rbf_output, x_test


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Using this kernel function, lets sample from a multivariate Gaussian at 100 evenly spaced real values of $x$ between -10 and 10. But this time you can adjust the slider to change the value of the kernel's $l$ parameter and see how it changes the shape of the covariance matrix and the resulting distribution over functions.""")
    return


@app.cell
def _(get_fig_double):
    get_fig_double()
    return


@app.cell
def _(go, make_subplots, mo, np, pairwise_rbf):
    # --- Setup the subplot figure with two columns ---
    # (Left: "Function Samples", Right: "Covariance Matrix")
    fig_double_subplots = make_subplots(
        rows=1, 
        cols=2, 
        subplot_titles=("Function Samples", "Covariance Matrix")
    )

    # 1) Prepare our initial data: an RBF covariance heatmap in col=2, an empty scatter in col=1
    _xa = np.linspace(-1, 1, 100).reshape(-1, 1)
    init_cov = pairwise_rbf(_xa, _xa, l=0.5)  # initial value of l=0.5
    heatmap_init = go.Heatmap(z=np.rot90(init_cov), showscale=False)
    scatter_init2 = go.Scatter(mode="lines", x=[], y=[])

    fig_double_subplots.add_trace(heatmap_init, row=1, col=2)
    fig_double_subplots.add_trace(scatter_init2, row=1, col=1)
    fig_double_subplots.update_yaxes(range=[-5, 5], fixedrange=True, row=1, col=1)

    # Convert subplots to a final figure
    init_fig_double = go.Figure(fig_double_subplots)

    # 2) Store the figure and relevant parameters in Marimo's state
    get_fig_double, set_fig_double = mo.state(init_fig_double)
    # Keep track of the RBF parameter l, the covariance matrix, and a sample counter
    get_l_param, set_l_param = mo.state(0.5)
    get_cov_double, set_cov_double = mo.state(init_cov)
    get_sample_count_double, set_sample_count_double = mo.state(0)

    # 3) Define the callback functions
    def on_slider_change(new_l):
        """
        When the slider for 'l' changes, update the covariance heatmap
        in the right subplot and store the new matrix for future samples.
        """
        fig_d = get_fig_double()
        set_l_param(new_l)
        # Recompute covariance
        new_cov = pairwise_rbf(_xa, _xa, l=new_l)
        set_cov_double(new_cov)
        # Update the heatmap trace (which should be the first data item)
        # We keep it in row=1, col=2, so that is data[0].
        fig_d.data[0].z = np.rot90(new_cov)
        set_fig_double(fig_d)

    def add_new_sample(_):
        """
        Generate a new random function sample from the current covariance
        and plot it in the left subplot (row=1, col=1).
        """
        fig_d = get_fig_double()
        sample_num = get_sample_count_double()
        current_cov = get_cov_double()

        # Draw one random sample from the current covariance
        y_samp = np.random.multivariate_normal(
            mean=np.zeros(len(_xa)), 
            cov=current_cov, 
            size=1
        )[0]

        # Append a new trace on the left
        new_trace = go.Scatter(
            x=_xa.ravel(),
            y=y_samp,
            mode="lines",
            name=f"ℓ={get_l_param():.2f}",
            xaxis="x", 
            yaxis="y"
        )
        fig_d.add_trace(new_trace, row=1, col=1)

        set_fig_double(fig_d)
        set_sample_count_double(sample_num + 1)

    def clear_figure(_):
        """
        Reset the figure to just the heatmap (data[0]) and 
        one empty scatter (data[1]) on the left subplot.
        Also reset the sample counter.
        """
        fig_d = get_fig_double()
        # Keep only the first two traces:
        #  - data[0] is the heatmap
        #  - data[1] is the empty scatter
        fig_d.data = fig_d.data[:2]

        # Optionally re-initialize the second trace to be truly empty
        fig_d.data[1] = go.Scatter(mode="lines", x=[], y=[])

        set_fig_double(fig_d)
        set_sample_count_double(0)

    # 4) Build the UI: slider + two buttons + the figure

    # -- Slider for the RBF kernel parameter 'l' --
    slider_l2 = mo.ui.slider(
        value=get_l_param(),
        start=0.01,
        stop=1.0,
        step=0.01,
        on_change=on_slider_change,
        label="RBF Kernel Parameter (ℓ)"
    )

    # -- "New Sample" button --
    btn_new_sample_double = mo.ui.button(
        label="New Sample",
        on_click=add_new_sample,
        kind="neutral"
    )

    # -- "Clear" button --
    btn_clear_double = mo.ui.button(
        label="Clear",
        on_click=clear_figure,
        kind="danger"
    )

    # Display them: 
    #   1) The slider
    #   2) The buttons in a horizontal row
    #   3) The figure

    mo.hstack([btn_new_sample_double, slider_l2, btn_clear_double])
    return (
        add_new_sample,
        btn_clear_double,
        btn_new_sample_double,
        clear_figure,
        fig_double_subplots,
        get_cov_double,
        get_fig_double,
        get_l_param,
        get_sample_count_double,
        heatmap_init,
        init_cov,
        init_fig_double,
        on_slider_change,
        scatter_init2,
        set_cov_double,
        set_fig_double,
        set_l_param,
        set_sample_count_double,
        slider_l2,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Conditioning on Data

        Wow, we've come a long way. Let's regroup here and remember our original definition of a Gaussian Process Regression.

        **GP Regression: <font color="#32a852">A Multivariate Gaussian Distribution over functions</font>, conditioned on some training data.**

        > In fact this highlighted part above is the definition of a Gaussian Process. But we want "Gaussian Process Regression". (People sometimes use the two to mean the same thing, but technically GP is the distribution and GPR is the regression problem.)

        We're more than half-way done! But we still need to condition it on some training data. Right now we're just sampling these pretty functions, but they are completely random. 

        Conditioning means we want the probability of some outcome given some data. Mathematically we write this as:

        $$
        p(y | x)
        $$

        that is, the probability of some outcome $y$ given some other data $x$. 

        Let's take a simple toy problem as a concrete example:

        Say we are trying to predict the cost of a house along a particular road. At one end of the road, there is a nuclear power plant (yikes!). We have some data on the cost of some of the houses on this road, but we want to predict the cost of a house at any location. Let's look at the data first:
        """
    )
    return


@app.cell
def _(np, pd):
    # @title
    X = np.array(
        [
            [9.34825241e00],
            [9.67438030e00],
            [1.17250505e01],
            [5.99427279e00],
            [1.07375146e01],
            [3.87950162e00],
            [2.71045131e00],
            [7.35740185e00],
            [9.13638194e00],
            [1.05863164e01],
            [7.42074188e00],
            [1.20328572e01],
            [5.15531137e00],
            [3.24806136e-01],
            [1.32962952e-03],
        ]
    )
    y = np.array(
        [
            [295011.54177245],
            [291803.4301587],
            [302340.03191297],
            [254244.52812629],
            [288037.40660445],
            [225340.17067212],
            [235462.67258466],
            [291158.36183822],
            [297052.11645609],
            [287514.83630223],
            [292359.62730391],
            [310157.34073017],
            [233483.05286424],
            [209630.56264745],
            [200039.88887763],
        ]
    )
    DOMAIN = (0, 4 * np.pi)
    X_axis = np.linspace(DOMAIN[0], DOMAIN[1], 100).reshape(1, -1).T
    y_true = (0.1 * np.sin(X_axis) + 1) * 200000 + X_axis * 10000
    X_test = np.linspace(DOMAIN[0], DOMAIN[1], 100).reshape(1, -1).T
    df = pd.DataFrame(y.flatten(), index=X.flatten(), columns=["Cost of a house"]).sort_index()
    df.index.name = "Distance from the Nuclear Power Plant (miles)"
    df.plot(style="o", color="red")
    return DOMAIN, X, X_axis, X_test, df, y, y_true


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Right away we see a couple things. Housing costs are not just linearly increasing as we get further away from the plant; there seem to be a few dips. Maybe there is a prison 5 miles away from the plant; who knows. Regardless, we probably want some non-linear model for this data. 

        The main question at hand is given this known cost data, what is the expected cost of a house at another location $x$?

        To state this mathematically, we want some function structured as follows:

        $$
        p(\textbf{c} | \textbf{x})
        $$

        That is, we want the probability distribution of cost of a house $c$, given its distance $x$ from the nuclear plant. Since we've been thinking about multivariate Gaussian, let's make an assumption that the distribution above follows a multivariate Gaussian.

        $$
        p(\textbf{c} | \textbf{x}) \sim N(m(\textbf{x}), k(\textbf{x}, \textbf{x}))
        $$

        Where $k(\textbf{x}, \textbf{x})$ is the covariance function, and $m(\textbf{x})$ is the mean function. For now we'll just assume that the mean function is zero, and for the covariance function we'll use the RBF kernel. 

        Why these? Remember the RBF function's effect above: it sort of "smooths" out the data. This makes sense to model housing prices, because it's reasonable to expect that houses near each other will have similar prices. 

        > But why is the mean function zero? A: trust me bro. It just works out in practice that mean = 0 is usually good enough to model the data. For example sklearn's GP implementation doesn't even let you specify a mean function. For more on this see [Section 2.7 here](http://gaussianprocess.org/gpml/chapters/RW2.pdf).

        We really need the following if we want to condition on the known data:

        $$
        p(\textbf{c} | \textbf{x}, \textbf{c}_{\text{known}}, \textbf{x}_{\text{known}})
        $$

        Putting this into words, we want the probability distribution of prices of a house, given its location _and_ given the prices of houses at some other locations.

        Let's assume that the known data also came from the same multivariate Gaussian distribution as the unknown. So we can write:


        $$
        p(\textbf{c}_{\text{known}}| \textbf{x}_{\text{known}}) \sim N(0, k(\textbf{x}_{\text{known}}, \textbf{x}_{\text{known}}))
        $$

        And for the unknown data, remember we had:

        $$
        p(\textbf{c} | \textbf{x}) \sim N(0, k(\textbf{x}, \textbf{x}))
        $$

        Notice that we've assumed both the known data and the unknown data come from multivariate Gaussians. What if we just combined them into one big multivariate gaussian? We could basically just stack the distributions on top of each other to form a big "mother" Gaussian.

        $$
        p(\begin{bmatrix} \textbf{c} \\ \textbf{c}_{\text{known}} \end{bmatrix} | \begin{bmatrix} \textbf{x} \\ \textbf{x}_{\text{known}} \end{bmatrix}) \sim N\left(\begin{bmatrix}0 \\ 0\end{bmatrix}, \begin{bmatrix}k(\textbf{x}, \textbf{x}) & k(\textbf{x}, \textbf{x}_{\text{known}}) \\ k(\textbf{x}_{\text{known}}, \textbf{x}) & k(\textbf{x}_{\text{known} }, \textbf{x}_{\text{known}})\end{bmatrix}\right)
        $$

        The one wrinkle here is the covariance function. For the off-diagonal elements, we need to use the covariance function between the unknown data and the known data. So _now_ we see why the kernel function is written as $k(\textbf{x}, \textbf{x})$; in this case we need to compute the covariance between two different vectors of data to fill in the off-diagonal blocks of the covariance matrix above.

        Now question is can we massage the beast above into a probability distribution conditioned on the known data? Like so:

        $p(\textbf{c} | \textbf{x}, \textbf{c}_{\text{known}}, \textbf{x}_{\text{known}}) \sim ???$

        The answer is yes. It's the following:

        $$
        p(\textbf{c} | \textbf{x}, \textbf{c}_{\text{known}}, \textbf{x}_{\text{known}}) \sim N\left(m(\textbf{x}) + k(\textbf{x}, \textbf{x}_{\text{known}})k(\textbf{x}_{\text{known}})^{-1}(\textbf{c}_{\text{known}} - m(\textbf{x}_{\text{known}})), k(\textbf{x}) - k(\textbf{x}, \textbf{x}_{\text{known}})k(\textbf{x}_{\text{known}})^{-1}k(\textbf{x}_{\text{known}}, \textbf{x})\right)
        $$

        > Please don't get mad at me for just giving you the answer. It's a kind of complicated derivation, and I don't want us to get bogged down. If you want to go through it, see this section of [Gaussian Processes for Machine Learning](http://gaussianprocess.org/gpml/chapters/RW.pdf#page=218&zoom=100,240,358). 
        >
        > For now, just accept that there's a nice closed form solution to this problem. 

        Wait, uh, so we're done? 

        **GP Regression: <font color="#32a852">A Multivariate Gaussian Distribution over functions, conditioned on some training data.</font>**

        We're done! We've got a nice closed form distribution over functions conditioned on some data.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Actually Fitting a Regression Model

        Using our conditional distribution above, we can plug in our known house costs to create a conditional distribution of functions. Then we can sample from this distribution at, say, 100 evenly spaced distance from 0 to 12 miles away from the nuclear plant.

        We have 15 known cost data points. This means that $\textbf{c}_{\text{known}}$ and $\textbf{x}_{\text{known}}$ is are vectors of length 15. We want to predicted prices at 100 evenly spaced points, so $\textbf{x}$ and $\textbf{c}$ are vectors of length 100. 

        Plugging this into the conditional distribution above, we can now sample from the conditional distribution of functions:

        > Note: we're using the RBF kernel here with parameter $ℓ$ set to 1.0.
        """
    )
    return


@app.cell
def _(pairwise_rbf, sp):
    def gp_posterior(y_train, X_train, X_test, l=1.0):
        """
        Given known data (y_train, X_train), and some unknown input values(X_test)
        calculate the conditional mean vector (mu_2__1) and conditional covariance matrix
        (sigma_2__1) of a Gaussian process with RBF kernel.
        """
        sigma_11 = pairwise_rbf(X_train, X_train, l=l)
        sigma_21 = pairwise_rbf(X_train, X_test, l=l).T
        sigma_22 = pairwise_rbf(X_test, X_test, l=l)
        sigma_12 = sigma_21.T
        mu_2__1 = (sigma_21 @ sp.linalg.inv(sigma_11) @ y_train).flatten()
        sigma_2__1 = sigma_22 - sigma_21 @ sp.linalg.inv(sigma_11) @ sigma_12
        return (mu_2__1, sigma_2__1)
    return (gp_posterior,)


@app.cell
def _(get_fig_housing):
    get_fig_housing()
    return


@app.cell
def _(X, X_test, go, gp_posterior, mo, np, y):
    # We'll assume y, X, X_test, and gp_posterior(...) are already defined above.
    # y is the original housing data, X the known inputs, X_test the test inputs.

    # Normalize y
    _y_norm = (y - y.mean()) / y.std()
    mu, sigma = gp_posterior(_y_norm, X, X_test, l=1)  # gp_posterior returns mean & covariance

    # 1) Create initial figure with known housing data
    scatter_known = go.Scatter(
        x=X.T[0],
        y=y.T[0],
        mode="markers",
        marker=dict(color="red", size=12),
        name="Known Data"
    )
    layout_housing = go.Layout(
        title="Samples from a Gaussian Process Conditioned on Known Housing Data",
        xaxis_title="Distance from the Nuclear Power Plant (miles)",
        yaxis_title="Cost of a house ($)",
    )
    init_fig_housing = go.Figure(data=[scatter_known], layout=layout_housing)

    # 2) Wrap the figure and a sample counter in Marimo's state
    get_fig_housing, set_fig_housing = mo.state(init_fig_housing)
    get_clicks_housing, set_clicks_housing = mo.state(0)

    def add_sample_housing(_):
        """
        Draw a random sample from the GP posterior (mu, sigma),
        un-normalize it, and add it to the figure as a new trace.
        """
        fig_housing = get_fig_housing()
        current_clicks = get_clicks_housing()

        # Draw a single sample from the posterior (100D)
        # Then "un-normalize" it back to actual scale
        yp = (
            np.random.multivariate_normal(mean=mu, cov=sigma, size=1)[0] * y.std() 
            + y.mean()
        )
        new_scatter = go.Scatter(
            x=X_test.T[0], 
            y=yp, 
            mode="lines+markers",
            name=f"Sample {current_clicks}"
        )
        fig_housing.add_trace(new_scatter)

        set_fig_housing(fig_housing)
        set_clicks_housing(current_clicks + 1)

    def clear_data_housing(_):
        """
        Reset the figure to only contain the original known data trace.
        Reset the sample counter to zero.
        """
        fig_housing = get_fig_housing()
        # Keep only the first trace (the known data)
        fig_housing.data = fig_housing.data[:1]
        set_fig_housing(fig_housing)
        set_clicks_housing(0)

    # 3) Create the UI: two buttons + the figure
    btn_new_sample_housing = mo.ui.button(
        label="New Sample",
        on_click=add_sample_housing,
        kind="neutral"
    )
    btn_clear_housing = mo.ui.button(
        label="Clear",
        on_click=clear_data_housing,
        kind="danger"
    )

    # 4) Display everything
    mo.hstack([btn_new_sample_housing, btn_clear_housing])
    return (
        add_sample_housing,
        btn_clear_housing,
        btn_new_sample_housing,
        clear_data_housing,
        get_clicks_housing,
        get_fig_housing,
        init_fig_housing,
        layout_housing,
        mu,
        scatter_known,
        set_clicks_housing,
        set_fig_housing,
        sigma,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Heck yeah! This looks like a Gaussian process regression! Clearly the samples from the distribution are conditioned on known data, because all the functions we sample pass through the known data points. But in between the known data points the functions are free to somewhat randomly vary, giving us an idea of the uncertainty. How smoothly the functions vary is determined by the covariance function, which in this case is the RBF kernel.

        In the plot below, I've taken 1000 samples from this conditioned distribution (a.k.a. "posterior predictive distribution") and plotted them. I also reveal the real function that I used to generate the fake housing data (in black).
        """
    )
    return


@app.cell
def _(X, X_axis, X_test, gp_posterior, np, pd, y, y_true):
    _y_norm = (y - y.mean()) / y.std()
    mu_1, sigma_1 = gp_posterior(_y_norm, X, X_test, l=1)
    y_hat = np.random.multivariate_normal(mu_1, sigma_1, size=1000) * y.std() + y.mean()
    df_1 = (
        pd.DataFrame(y_hat.T, index=X_test.flatten())
        .sort_index()
        .plot(alpha=0.01, legend=False, color="blue")
    )
    df_1.set_ylabel("Price")
    df_1.set_xlabel("Blocks away from the Nuclear Power Plant")
    pd.DataFrame(
        y_true.flatten(), index=X_axis.flatten(), columns=["Underlying Function"]
    ).sort_index().plot(ax=df_1, color="#e802e4", linewidth=2)
    (
        pd.DataFrame(y.flatten(), index=X.flatten(), columns=["Known Data"])
        .sort_index()
        .plot(ax=df_1, style="o", color="red")
    )
    return df_1, mu_1, sigma_1, y_hat


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Remember what there blue lines are: they are samples from a multivariate gaussian conditioned on the known data points, and sampled at 1000 evenly spaced points between 0 and 12. We used the complicated formula above to find the conditional mean vector and conditional covariance matrix, and then sampled from a distribution using that mean and covariance.

        Below are some heatmaps of the _conditional_ covariance matrix and _conditional_ mean vector (conditioned on the known housing data) that specify the predictive multivariate gaussian distribution.

        Think for a moment about why this conditional mean and covariance makes sense.
        """
    )
    return


@app.cell
def _(X_test, mu_1, pd, plt, sigma_1, sns, y):
    ix = X_test.flatten().round(2)
    sns.heatmap(pd.DataFrame(sigma_1, index=ix, columns=ix)).set_title(
        "Conditional Covariance Matrix"
    )
    plt.show()
    _ = sns.heatmap(pd.DataFrame((mu_1 * y.std() + y.mean()).reshape(-1, 1), index=ix)).set_title(
        "Conditional Mean Vector"
    )
    return (ix,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Outro

        You should now have the core ideas of Gaussian processes regression. If you still have some questions, like:

        - "how do we choose a kernel function?" 
        - "how do we choose the best parameters for the kernel function?" 
        - "do you really have to sample 1000s of functions to get the confidence intervals?"
        - "what if the training data is intrinsically noisy (the price of houses has some variance at a given location)
          "
        - "what if there are many features in my training data?"
        - "but I heard GPs are expensive to train?" 

        then you should check out the resources below, which should be easier to understand now that you have the basics.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## References

        ### Tutorials and Guides
        - **[Gaussian Process Tutorial](https://peterroelants.github.io/posts/gaussian-process-tutorial/)** - Really awesome set of blog posts that teaches GPs using Python. I basically took this post and made it more verbose. The other posts in the series go into more detail about the process of fitting a GP and optimizing the kernel and hyperparameters. 

        - **[Visual Exploration of Gaussian Processes](https://distill.pub/2019/visual-exploration-gaussian-processes/)** - More detailed, with beautiful interactive visualizations.

        - **[Fitting Gaussian Process Models in Python](https://www.dominodatalab.com/blog/fitting-gaussian-process-models-python)** - Practical guide focused on implementing GPs using scikit-learn and other Python libraries.

        ### Advanced Reading
        - **[Gaussian Processes for Machine Learning](http://gaussianprocess.org/gpml/chapters/)** - _The book_ on GPs, with probably all the detail you'll ever need.
        """
    )
    return


if __name__ == "__main__":
    app.run()
