
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from utils.data import wrangling

import plotly.express as px

colors = px.colors.sequential.Turbo


def plot_time_series(
        data,
        *variables,
        timestamp=None,
        mode=None,
        secondary_y=True,
        time_resample=False,
        file_path=None,
        renderer=None,
        title=None,
        y_title=None,
        y_title_secondary=None,
        hovertemplate=None,
        text=None,
        opacity=None,
    ):

    if timestamp is None:
        timestamp = "read_at"

    variable_1 = variables[0]
    if len(variables) > 1:
        variable_2 = variables[1:]
    else:
        variable_2 = []

    df = data.copy()

    if time_resample:
        df = wrangling.time_resample(df)

    df.sort_values(by=timestamp, inplace=True)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=df[timestamp],
            y=df[variable_1],
            name=variable_1,
            mode=mode,
            # marker=dict(size=3),
            line=dict(width=2), #, color="orange")
            opacity=0.5,
            text=text,
            hovertemplate=hovertemplate,
        ),
        secondary_y=False,
    )

    for i, variable in enumerate(variable_2):
        fig.add_trace(
            go.Scatter(
                x=df[timestamp],
                y=df[variable],
                name=variable,
                mode=mode,
                # marker=dict(size=3),
                line=dict(width=2), #, color=colors[i])
                opacity=0.5,
                text=text,
                hovertemplate=hovertemplate,
            ),
            secondary_y=secondary_y,
        )

    fig.update_xaxes(title_text=timestamp, rangeslider_visible=True)

    fig.update_layout(
        title=title,
        yaxis_title=y_title,
        legend_title="Variables:",
        # font=dict(
        #     family="Courier New, monospace",
        #     size=15,
        #     color="RebeccaPurple"
        # )
    )

    if secondary_y:
        fig.update_yaxes(title_text=y_title_secondary, secondary_y=True)


    if file_path:
        fig.write_html(file_path)

    if renderer == "browser":
        fig.show(renderer="browser")
        return
    else:
        return fig


def plot_time_series_by_segment(data, variable_to_plot, variable_to_segment, timestamp=None, mode=None, renderer=None):

    if timestamp is None:
        timestamp = "read_at"

    df = data.copy()

    df.sort_values(by=timestamp, inplace=True)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for segment, df_to_plot in df.groupby(variable_to_segment):
        fig.add_trace(
            go.Scatter(
                x=df_to_plot[timestamp],
                y=df_to_plot[variable_to_plot],
                name=str(segment),
                mode=mode,
                line=dict(width=3), #, color="orange")
                marker=dict(size=3),
                opacity=0.5
            ),
            secondary_y=False,
        )

    fig.update_layout(
        title=variable_to_plot
    )

    if renderer == "browser":
        fig.show(renderer="browser")
        return
    else:
        return fig
