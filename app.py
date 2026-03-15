from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def home():
    profile = {
        "name": "Yash",
        "role": "Cloud and DevOps Engineer",
        "experience": "3.5 years",
        "about": (
            "I build reliable cloud infrastructure, automate delivery pipelines, "
            "and help teams ship faster with stable systems."
        ),
        "skills": [
            "AWS and cloud infrastructure",
            "CI/CD pipelines",
            "Docker and container workflows",
            "Linux administration",
            "Infrastructure automation",
            "Monitoring and deployment support",
        ],
        "email": "yash@example.com",
        "phone": "+91 98765 43210",
        "location": "India",
    }
    return render_template("index.html", profile=profile)


if __name__ == "__main__":
    app.run(debug=True)
