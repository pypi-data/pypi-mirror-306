import jax.numpy as jnp

from evox import use_state


def plot_dec_space(
    population_history,
    **kwargs,
):
    """A Built-in plot function for visualizing the population of single-objective algorithm.
    Use plotly internally, so you need to install plotly to use this function.

    If the problem is provided, we will plot the fitness landscape of the problem.
    """
    try:
        import plotly
        import plotly.express as px
        import plotly.graph_objects as go
    except ImportError:
        raise ImportError("The plot function requires plotly to be installed.")

    all_pop = jnp.concatenate(population_history, axis=0)
    x_lb = jnp.min(all_pop[:, 0])
    x_ub = jnp.max(all_pop[:, 0])
    x_range = x_ub - x_lb
    x_lb = x_lb - 0.1 * x_range
    x_ub = x_ub + 0.1 * x_range
    y_lb = jnp.min(all_pop[:, 1])
    y_ub = jnp.max(all_pop[:, 1])
    y_range = y_ub - y_lb
    y_lb = y_lb - 0.1 * y_range
    y_ub = y_ub + 0.1 * y_range

    frames = []
    steps = []
    for i, pop in enumerate(population_history):
        frames.append(
            go.Frame(
                data=[
                    go.Scatter(
                        x=pop[:, 0],
                        y=pop[:, 1],
                        mode="markers",
                        marker={"color": "#636EFA"},
                    ),
                ],
                name=str(i),
            )
        )
        step = {
            "label": i,
            "method": "animate",
            "args": [
                [str(i)],
                {
                    "frame": {"duration": 200, "redraw": False},
                    "mode": "immediate",
                    "transition": {"duration": 200},
                },
            ],
        }
        steps.append(step)

    sliders = [
        {
            "currentvalue": {"prefix": "Generation: "},
            "pad": {"t": 50},
            "pad": {"b": 1, "t": 10},
            "len": 0.8,
            "x": 0.2,
            "y": 0,
            "yanchor": "top",
            "xanchor": "left",
            "steps": steps,
        }
    ]

    fig = go.Figure(
        data=frames[0].data,
        layout=go.Layout(
            legend={
                "x": 1,
                "y": 1,
                "xanchor": "auto",
                "xanchor": "auto",
            },
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
            sliders=sliders,
            xaxis={"range": [x_lb, x_ub]},
            yaxis={"range": [y_lb, y_ub]},
            updatemenus=[
                {
                    "type": "buttons",
                    "buttons": [
                        {
                            "args": [
                                None,
                                {
                                    "frame": {"duration": 200, "redraw": False},
                                    "fromcurrent": True,
                                    "transition": {
                                        "duration": 200,
                                        "easing": "linear",
                                    },
                                    "mode": "immediate",
                                },
                            ],
                            "label": "Play",
                            "method": "animate",
                        },
                        {
                            "args": [
                                [None],
                                {
                                    "frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0},
                                    "mode": "immediate",
                                },
                            ],
                            "label": "Pause",
                            "method": "animate",
                        },
                    ],
                    "x": 0.2,
                    "xanchor": "right",
                    "y": 0,
                    "yanchor": "top",
                    "direction": "left",
                    "pad": {"r": 10, "t": 30},
                },
            ],
            **kwargs,
        ),
        frames=frames,
    )

    return fig


def plot_obj_space_1d(fitness_history, animation=True, **kwargs):
    if animation:
        return plot_obj_space_1d_animation(fitness_history, **kwargs)
    else:
        return plot_obj_space_1d_no_animation(fitness_history, **kwargs)


def plot_obj_space_1d_no_animation(fitness_history, **kwargs):
    try:
        import plotly
        import plotly.express as px
        import plotly.graph_objects as go
    except ImportError:
        raise ImportError("The plot function requires plotly to be installed.")

    min_fitness = [jnp.min(x) for x in fitness_history]
    max_fitness = [jnp.max(x) for x in fitness_history]
    median_fitness = [jnp.median(x) for x in fitness_history]
    avg_fitness = [jnp.mean(x) for x in fitness_history]
    generation = jnp.arange(len(fitness_history))

    fig = go.Figure(
        [
            go.Scatter(x=generation, y=min_fitness, mode="lines", name="Min"),
            go.Scatter(x=generation, y=max_fitness, mode="lines", name="Max"),
            go.Scatter(x=generation, y=median_fitness, mode="lines", name="Median"),
            go.Scatter(x=generation, y=avg_fitness, mode="lines", name="Average"),
        ],
        layout=go.Layout(
            legend={
                "x": 1,
                "y": 1,
                "xanchor": "auto",
                "xanchor": "auto",
            },
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
        ),
    )

    return fig


def plot_obj_space_1d_animation(fitness_history, **kwargs):
    try:
        import plotly
        import plotly.express as px
        import plotly.graph_objects as go
    except ImportError:
        raise ImportError("The plot function requires plotly to be installed.")

    min_fitness = [jnp.min(x) for x in fitness_history]
    max_fitness = [jnp.max(x) for x in fitness_history]
    median_fitness = [jnp.median(x) for x in fitness_history]
    avg_fitness = [jnp.mean(x) for x in fitness_history]
    generation = jnp.arange(len(fitness_history))

    frames = []
    steps = []
    for i in range(len(fitness_history)):
        frames.append(
            go.Frame(
                data=[
                    go.Scatter(
                        x=generation[: i + 1],
                        y=min_fitness[: i + 1],
                        mode="lines",
                        name="Min",
                        showlegend=True,
                    ),
                    go.Scatter(
                        x=generation[: i + 1],
                        y=max_fitness[: i + 1],
                        mode="lines",
                        name="Max",
                    ),
                    go.Scatter(
                        x=generation[: i + 1],
                        y=median_fitness[: i + 1],
                        mode="lines",
                        name="Median",
                    ),
                    go.Scatter(
                        x=generation[: i + 1],
                        y=avg_fitness[: i + 1],
                        mode="lines",
                        name="Average",
                    ),
                ],
                name=str(i),
            )
        )

        step = {
            "label": i,
            "method": "animate",
            "args": [
                [str(i)],
                {
                    "frame": {"duration": 200, "redraw": False},
                    "mode": "immediate",
                    "transition": {"duration": 200},
                },
            ],
        }
        steps.append(step)

    sliders = [
        {
            "currentvalue": {"prefix": "Generation: "},
            "pad": {"b": 1, "t": 10},
            "len": 0.8,
            "x": 0.2,
            "y": 0,
            "yanchor": "top",
            "xanchor": "left",
            "steps": steps,
        }
    ]
    lb = min(min_fitness)
    ub = max(max_fitness)
    fit_range = ub - lb
    lb = lb - 0.05 * fit_range
    ub = ub + 0.05 * fit_range
    fig = go.Figure(
        data=frames[-1].data,
        layout=go.Layout(
            legend={
                "x": 1,
                "y": 1,
                "xanchor": "auto",
                "xanchor": "auto",
            },
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
            sliders=sliders,
            xaxis={"range": [0, len(fitness_history)], "autorange": False},
            yaxis={"range": [lb, ub], "autorange": False},
            updatemenus=[
                {
                    "type": "buttons",
                    "buttons": [
                        {
                            "args": [
                                None,
                                {
                                    "frame": {"duration": 200, "redraw": False},
                                    "fromcurrent": True,
                                },
                            ],
                            "label": "Play",
                            "method": "animate",
                        },
                        {
                            "args": [
                                [None],
                                {
                                    "frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                },
                            ],
                            "label": "Pause",
                            "method": "animate",
                        },
                    ],
                    "x": 0.2,
                    "xanchor": "right",
                    "y": 0,
                    "yanchor": "top",
                    "direction": "left",
                    "pad": {"r": 10, "t": 30},
                },
            ],
            **kwargs,
        ),
        frames=frames,
    )

    return fig


def plot_obj_space_2d(fitness_history, problem_pf=None, sort_points=False, **kwargs):
    try:
        import plotly
        import plotly.express as px
        import plotly.graph_objects as go
    except ImportError:
        raise ImportError("The plot function requires plotly to be installed.")
    all_fitness = jnp.concatenate(fitness_history, axis=0)
    x_lb = jnp.min(all_fitness[:, 0])
    x_ub = jnp.max(all_fitness[:, 0])
    x_range = x_ub - x_lb
    x_lb = x_lb - 0.05 * x_range
    x_ub = x_ub + 0.05 * x_range
    y_lb = jnp.min(all_fitness[:, 1])
    y_ub = jnp.max(all_fitness[:, 1])
    y_range = y_ub - y_lb
    y_lb = y_lb - 0.05 * y_range
    y_ub = y_ub + 0.05 * y_range

    frames = []
    steps = []
    if problem_pf is not None:
        pf_scatter = go.Scatter(
            x=problem_pf[:, 0],
            y=problem_pf[:, 1],
            mode="markers",
            marker={"color": "#FFA15A", "size": 2},
            name="Pareto Front",
        )

    for i, fit in enumerate(fitness_history):
        # it will make the animation look nicer
        if sort_points:
            indices = jnp.lexsort(fit.T)
            fit = fit[indices]
        scatter = go.Scatter(
            x=fit[:, 0],
            y=fit[:, 1],
            mode="markers",
            marker={"color": "#636EFA"},
            name="Population",
        )
        if problem_pf is not None:
            frames.append(go.Frame(data=[pf_scatter, scatter], name=str(i)))
        else:
            frames.append(go.Frame(data=[scatter], name=str(i)))

        step = {
            "label": i,
            "method": "animate",
            "args": [
                [str(i)],
                {
                    "frame": {"duration": 200, "redraw": False},
                    "mode": "immediate",
                    "transition": {"duration": 200},
                },
            ],
        }
        steps.append(step)

    sliders = [
        {
            "currentvalue": {"prefix": "Generation: "},
            "pad": {"b": 1, "t": 10},
            "len": 0.8,
            "x": 0.2,
            "y": 0,
            "yanchor": "top",
            "xanchor": "left",
            "steps": steps,
        }
    ]
    fig = go.Figure(
        data=frames[0].data,
        layout=go.Layout(
            legend={
                "x": 1,
                "y": 1,
                "xanchor": "auto",
                "xanchor": "auto",
            },
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
            sliders=sliders,
            xaxis={"range": [x_lb, x_ub], "autorange": False},
            yaxis={"range": [y_lb, y_ub], "autorange": False},
            updatemenus=[
                {
                    "type": "buttons",
                    "buttons": [
                        {
                            "args": [
                                None,
                                {
                                    "frame": {"duration": 200, "redraw": False},
                                    "fromcurrent": True,
                                    "transition": {
                                        "duration": 200,
                                        "easing": "linear",
                                    },
                                },
                            ],
                            "label": "Play",
                            "method": "animate",
                        },
                        {
                            "args": [
                                [None],
                                {
                                    "frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                },
                            ],
                            "label": "Pause",
                            "method": "animate",
                        },
                    ],
                    "x": 0.2,
                    "xanchor": "right",
                    "y": 0,
                    "yanchor": "top",
                    "direction": "left",
                    "pad": {"r": 10, "t": 30},
                },
            ],
            **kwargs,
        ),
        frames=frames,
    )

    return fig


def plot_obj_space_3d(fitness_history, sort_points=False, problem_pf=None, **kwargs):
    try:
        import plotly
        import plotly.express as px
        import plotly.graph_objects as go
    except ImportError:
        raise ImportError("The plot function requires plotly to be installed.")

    all_fitness = jnp.concatenate(fitness_history, axis=0)
    x_lb = jnp.min(all_fitness[:, 0])
    x_ub = jnp.max(all_fitness[:, 0])
    x_range = x_ub - x_lb
    x_lb = x_lb - 0.05 * x_range
    x_ub = x_ub + 0.05 * x_range

    y_lb = jnp.min(all_fitness[:, 1])
    y_ub = jnp.max(all_fitness[:, 1])
    y_range = y_ub - y_lb
    y_lb = y_lb - 0.05 * y_range
    y_ub = y_ub + 0.05 * y_range

    z_lb = jnp.min(all_fitness[:, 2])
    z_ub = jnp.max(all_fitness[:, 2])
    z_range = z_ub - z_lb
    z_lb = z_lb - 0.05 * z_range
    z_ub = z_ub + 0.05 * z_range

    frames = []
    steps = []
    for i, fit in enumerate(fitness_history):
        # it will make the animation look nicer
        if sort_points:
            indices = jnp.lexsort(fit.T)
            fit = fit[indices]

        scatter = go.Scatter3d(
            x=fit[:, 0],
            y=fit[:, 1],
            z=fit[:, 2],
            mode="markers",
            marker={"color": "#636EFA", "size": 2},
        )
        frames.append(go.Frame(data=[scatter], name=str(i)))

        step = {
            "label": i,
            "method": "animate",
            "args": [
                [str(i)],
                {
                    "frame": {"duration": 200},
                    "mode": "immediate",
                    "transition": {"duration": 200, "easing": "linear"},
                },
            ],
        }
        steps.append(step)

    sliders = [
        {
            "currentvalue": {"prefix": "Generation: "},
            "pad": {"b": 10, "t": 50},
            "len": 0.5,
            "x": 0.3,
            "y": 0,
            "yanchor": "top",
            "xanchor": "left",
            "steps": steps,
        }
    ]
    fig = go.Figure(
        data=frames[0].data,
        layout=go.Layout(
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
            sliders=sliders,
            scene={
                "xaxis": {"range": [x_lb, x_ub], "autorange": False},
                "yaxis": {"range": [y_lb, y_ub], "autorange": False},
                "zaxis": {"range": [z_lb, z_ub], "autorange": False},
                "aspectmode": "cube",
            },
            scene_camera={
                "eye": {"x": 2, "y": 0.5, "z": 0.5},
            },
            updatemenus=[
                {
                    "type": "buttons",
                    "buttons": [
                        {
                            "args": [
                                None,
                                {
                                    "frame": {"duration": 200},
                                    "fromcurrent": True,
                                },
                            ],
                            "label": "Play",
                            "method": "animate",
                        },
                        {
                            "args": [
                                [None],
                                {
                                    "frame": {"duration": 0},
                                    "mode": "immediate",
                                },
                            ],
                            "label": "Pause",
                            "method": "animate",
                        },
                    ],
                    "x": 0.3,
                    "xanchor": "right",
                    "y": 0,
                    "yanchor": "top",
                    "direction": "left",
                    "pad": {"r": 10, "t": 87},
                },
            ],
            **kwargs,
        ),
        frames=frames,
    )

    return fig
