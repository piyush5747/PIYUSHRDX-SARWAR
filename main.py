from flask import Flask, request, redirect, url_for, render_template_string, session
import requests

app = Flask(__name__)
app.secret_key = "supersecurekey"  # सेशन के लिए

# ✅ आपके सेट किए गए यूजरनेम और पासवर्ड
VALID_CREDENTIALS = {
    "PIYUSH": "RDX560"
}

# 🔗 आपका असली वेबपेज जो पासवर्ड प्रोटेक्शन के बाद खुलेगा
PROTECTED_URL = "https://convo-yy8h.onrender.com"

# 📌 CSS डिजाइन
css = """
<style>
    body {
        background-color: #222;
        font-family: Arial, sans-serif;
        text-align: center;
        color: white;
    }
    .container {
        margin-top: 100px;
        padding: 20px;
        background-color: #333;
        border-radius: 10px;
        box-shadow: 0px 0px 10px 0px gray;
        width: 300px;
        display: inline-block;
    }
    input {
        padding: 10px;
        margin: 10px;
        width: 90%;
        background: black;
        color: white;
        border: 1px solid #555;
    }
    button {
        padding: 10px;
        background-color: red;
        color: white;
        border: none;
        cursor: pointer;
        width: 100%;
    }
    button:hover {
        background-color: darkred;
    }
</style>
"""

# 🔒 **लॉगिन पेज**
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # ✅ पासवर्ड चेक करो
        if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
            session["user"] = username
            return redirect(url_for("protected_page"))  # 🔗 लॉगिन के बाद प्रोटेक्टेड पेज पर जाएं
        else:
            return "❌ Access Denied! गलत यूज़रनेम या पासवर्ड", 401

    return render_template_string(f"""
        {css}
        <div class="container">
            <h2>🔒 Secure Login</h2>
            <form method="post">
                <input type="text" name="username" placeholder="Username" required><br>
                <input type="password" name="password" placeholder="Password" required><br>
                <button type="submit">Login</button>
            </form>
        </div>
    """)

# ✅ **प्रोटेक्टेड पेज (Render लिंक को एक्सेस करेगा)**
@app.route("/protected")
def protected_page():
    if "user" not in session:
        return redirect(url_for("login"))  # 🔄 अगर लॉगिन नहीं किया है, तो पहले लॉगिन पेज पर भेजो

    # 🔗 असली वेब पेज का कंटेंट लाओ
    response = requests.get(PROTECTED_URL)
    return response.text  # वेब पेज का HTML ओपन करो

# 🔓 **लॉगआउट पेज**
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


