from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import pandas as pd
import pickle
from datetime import datetime
from feature_extractor import extract_features
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
import re

from database import (
    create_db,
    save_scan,
    get_all_scans,
    delete_record_by_id,
    delete_all_records,
    delete_old_records
)

app = Flask(__name__)
app.secret_key = "replace_this_with_a_random_secret"

# ----------------------------------
# Create database if not exists
# ----------------------------------
create_db()

# ----------------------------------
# Load ML model
# ----------------------------------
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# ----------------------------------
# URL Validation
# ----------------------------------
def is_valid_url(url):
    pattern = re.compile(
        r'^(https?:\/\/)?'          # http:// or https://
        r'([a-zA-Z0-9-]+\.)+'       # domain
        r'[a-zA-Z]{2,}'             # extension
        r'(\/.*)?$'                 # path (optional)
    )
    return re.match(pattern, url) is not None

# ----------------------------------
# Home Page
# ----------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")

        if not url:
            flash("Please enter a URL", "error")
            return redirect(url_for("index"))

        if not is_valid_url(url):
            flash("Invalid URL format. Please enter a valid website URL.", "error")
            return redirect(url_for("index"))

        # Feature extraction
        features = extract_features(url)
        input_df = pd.DataFrame([features])

        # Prediction
        prediction_numeric = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)[0]
        classes = model.classes_

        # Correct probability mapping
        if classes[0] == 0:  # 0 = Phishing, 1 = Legit
            phishing_score = round(proba[0] * 100, 2)
            legit_score = round(proba[1] * 100, 2)
        else:
            phishing_score = round(proba[1] * 100, 2)
            legit_score = round(proba[0] * 100, 2)

        confidence = max(phishing_score, legit_score)

        result_text = "Legitimate ✅" if prediction_numeric == 1 else "Phishing ⚠️"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save to database
        save_scan(url, result_text, phishing_score, legit_score, timestamp)

        return render_template(
            "result.html",
            prediction=result_text,
            confidence=confidence,
            phishing_score=phishing_score,
            legit_score=legit_score,
            url_scanned=url,
            timestamp=timestamp
        )

    return render_template("index.html")

# ----------------------------------
# Download PDF
# ----------------------------------
@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    url = request.form.get("url_scanned", "")
    prediction = request.form.get("prediction", "")
    confidence = request.form.get("confidence", "")
    phishing_score = request.form.get("phishing_score", "0")
    legit_score = request.form.get("legit_score", "0")
    timestamp = request.form.get("timestamp", "")

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(300, 750, "PhishGuard.AI - Scan Report")

    result_color = colors.red if "Phishing" in prediction else colors.green

    y = 700
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawString(50, y, f"Scanned URL: {url}")

    y -= 25
    c.drawString(50, y, f"Time: {timestamp}")

    y -= 25
    c.setFillColor(result_color)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Result: {prediction}")

    y -= 25
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawString(50, y, f"Confidence: {confidence}%")

    y -= 25
    c.setFillColor(colors.red if float(phishing_score) > float(legit_score) else colors.black)
    c.drawString(50, y, f"Phishing Score: {phishing_score}%")

    y -= 25
    c.setFillColor(colors.green if float(legit_score) > float(phishing_score) else colors.black)
    c.drawString(50, y, f"Legitimate Score: {legit_score}%")

    c.showPage()
    c.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True,
                     download_name="scan_report.pdf",
                     mimetype="application/pdf")

# ----------------------------------
# History Page
# ----------------------------------
@app.route("/history")
def history():
    rows = get_all_scans()
    return render_template("history.html", scans=rows)

# ----------------------------------
# Delete Routes
# ----------------------------------
@app.route("/delete/<int:record_id>")
def delete_one(record_id):
    delete_record_by_id(record_id)
    flash("Record deleted successfully!", "success")
    return redirect("/history")

@app.route("/delete_all")
def delete_all():
    delete_all_records()
    flash("All records deleted!", "success")
    return redirect("/history")

@app.route("/delete_old/<int:days>")
def delete_old(days):
    delete_old_records(days)
    flash(f"Records older than {days} days deleted!", "success")
    return redirect("/history")

# ----------------------------------
if __name__ == "__main__":
    app.run(debug=True)
