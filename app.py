import base64

import cv2
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html
from dash.exceptions import PreventUpdate

from convex_hull import Point, compute_convex_hull

app = Dash(__name__)


def generate_blank_image(width, height):
    blank_image = np.ones((height, width, 3), dtype=np.uint8) * 255  # White image
    return blank_image


WIDTH = 1024
HEIGHT = 1024
BLANK_IMAGE = generate_blank_image(WIDTH, HEIGHT)
# Convert the NumPy array to base64
_, buffer = cv2.imencode(".png", cv2.cvtColor(BLANK_IMAGE, cv2.COLOR_BGR2RGB))
BLANK_IMAGE_BASE64 = base64.b64encode(buffer).decode("utf-8")

# Initial empty fig.
default_figure = go.Figure()
default_figure.update_layout(autosize=False, width=WIDTH, height=HEIGHT)
default_figure.add_trace(
    go.Image(
        source=f"data:image/png;base64,{BLANK_IMAGE_BASE64}",
        # x0=0,
        # y0=0,
        opacity=1.0,
    )
)

app.layout = html.Div(
    [
        html.H1(id="h1", children="Convex Hull", style={"textAlign": "center"}),
        html.Button("Reset points", id="reset-button", n_clicks=0),
        dcc.Graph(id="graph-content", figure=default_figure),
    ]
)

points = []


@callback(
    Output("graph-content", "figure"),
    Input("graph-content", "clickData"),
)
def update_graph(click_data):
    """Plots points and convex hull around them.
    """
    if click_data is None:
        raise PreventUpdate

    point = click_data["points"][0]
    x, y = point["x"], point["y"]
    points.append(Point(x, y))
    convex_hull = compute_convex_hull(points)

    convex_hull_x_values = [p.x for p in convex_hull]
    convex_hull_y_values = [p.y for p in convex_hull]
    if len(convex_hull) > 0:
        convex_hull_x_values.append(convex_hull[0].x)
        convex_hull_y_values.append(convex_hull[0].y)

    x_values = [p.x for p in points]
    y_values = [p.y for p in points]

    fig = go.Figure()
    fig.update_layout(autosize=False, width=1024, height=1024)
    fig.add_trace(
        go.Image(
            source=f"data:image/png;base64,{BLANK_IMAGE_BASE64}",
            # x0=0,
            # y0=0,
            opacity=1.0,
        )
    )

    if len(convex_hull_x_values) > 0:
        fig.add_trace(
            px.line(x=convex_hull_x_values, y=convex_hull_y_values, markers=True).data[
                0
            ]
        )
    if len(x_values) > 0:
        fig.add_trace(px.scatter(x=x_values, y=y_values).data[0])

    return fig


@callback(
    Output("graph-content", "figure", allow_duplicate=True),
    Input("reset-button", "n_clicks"),
    prevent_initial_call=True,
)
def reset_figure(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    points.clear()
    return default_figure


if __name__ == "__main__":
    app.run(debug=True)
