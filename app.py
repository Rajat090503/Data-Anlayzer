from flask import Flask, render_template, request, flash, send_file, url_for
import os
import pandas as pd
import plotly.express as px
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "uploads"
HISTORY_FOLDER = os.path.join(UPLOAD_FOLDER, "history")
os.makedirs(HISTORY_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
chart_history = []  


@app.route("/", methods=["GET", "POST"])
def index():
    preview, columns, chart_html = None, None, None
    try:
        if "file" in request.files:  
            file = request.files["file"]
            if file and (file.filename.endswith(".csv") or file.filename.endswith(".xlsx")):
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], "current.csv")
                df = pd.read_csv(file) if file.filename.endswith(".csv") else pd.read_excel(file)
                df.to_csv(filepath, index=False)

                preview = df.head().to_html(classes="table table-bordered")
                columns = list(df.columns)
            else:
                flash("Only .csv or .xlsx files are allowed!", "danger")

        elif "chart_type" in request.form:  
            x_col = request.form.get("x_column")
            y_col = request.form.get("y_column")
            chart_type = request.form.get("chart_type")

            df = pd.read_csv(os.path.join(app.config["UPLOAD_FOLDER"], "current.csv"))

            fig = None
            if chart_type == "bar":
                fig = px.bar(df, x=x_col, y=y_col)
            elif chart_type == "line":
                fig = px.line(df, x=x_col, y=y_col)
            elif chart_type == "pie":
                fig = px.pie(df, names=x_col, values=y_col)
            elif chart_type == "box":
                fig = px.box(df, x=x_col, y=y_col)
            elif chart_type == "scatter":
                fig = px.scatter(df, x=x_col, y=y_col)
            elif chart_type == "histogram":
                fig = px.histogram(df, x=x_col)
            elif chart_type == "area":
                fig = px.area(df, x=x_col, y=y_col)
            elif chart_type == "heatmap":
                corr = df.corr(numeric_only=True)
                fig = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Heatmap")

            if fig:
                chart_html = fig.to_html(full_html=False)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                png_path = os.path.join(HISTORY_FOLDER, f"chart_{timestamp}.png")
                html_path = os.path.join(HISTORY_FOLDER, f"chart_{timestamp}.html")

                try:
                    fig.write_image(png_path)  # requires kaleido
                except Exception as e:
                    flash(f"Warning: PNG not saved ({e})", "warning")

                fig.write_html(html_path)

                chart_history.append({
                    "time": timestamp,
                    "png": png_path,
                    "html": html_path,
                    "type": chart_type,
                    "x": x_col,
                    "y": y_col
                })

            preview = df.head().to_html(classes="table table-bordered")
            columns = list(df.columns)

    except Exception as e:
        flash(f"Something went wrong: {e}", "danger")

    return render_template("index.html", 
                           preview=preview, 
                           columns=columns, 
                           chart_html=chart_html, 
                           chart_history=chart_history, 
                           active_page="home")


@app.route("/history")
def history():
    return render_template("history.html", history=chart_history, active_page="history")


@app.route("/download/<filetype>/<timestamp>")
def download_chart(filetype, timestamp):
    for chart in chart_history:
        if chart["time"] == timestamp and filetype in chart:
            return send_file(chart[filetype], as_attachment=True)
    flash("Chart not found!", "danger")
    return render_template("history.html", history=chart_history, active_page="history")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
