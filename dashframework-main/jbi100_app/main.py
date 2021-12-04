from dash import Dash


app = Dash(
    __name__,
    # assets_external_path="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css"
)
app.title = "JBI100 Template"
# app.scripts.config.serve_locally = False