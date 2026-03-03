from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, send_file
from config import Config
from models import db, User, Resume
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from ai_service import generate_resume_text, generate_cover_letter
from pdf_service import generate_pdf
from resume_analyzer import analyze_resume
import os

app = Flask(__name__)
app.config.from_object(Config)

# Upload folder
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# -------------------- HOME --------------------

@app.route("/")
def home():
    return render_template("index.html")


# -------------------- REGISTER --------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        if User.query.filter_by(email=email).first():
            return "Email already registered."

        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


# -------------------- LOGIN --------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))

        return "Invalid email or password"

    return render_template("login.html")


# -------------------- DASHBOARD --------------------

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# -------------------- PROFILE --------------------

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_user.phone = request.form.get("phone")
        current_user.linkedin = request.form.get("linkedin")
        current_user.github = request.form.get("github")
        current_user.location = request.form.get("location")
        current_user.bio = request.form.get("bio")

        photo = request.files.get("profile_photo")

        if photo and photo.filename != "":
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)
            current_user.profile_photo = filename

        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("profile.html")

@app.route("/view_profile")
@login_required
def view_profile():
    return render_template("view_profile.html", user=current_user)
# -------------------- CREATE RESUME --------------------

@app.route("/resume", methods=["GET", "POST"])
@login_required
def resume():
    if request.method == "POST":
        new_resume = Resume(
            user_id=current_user.id,
            skills=request.form["skills"],
            education=request.form["education"],
            experience=request.form["experience"],
            projects=request.form["projects"]
        )

        db.session.add(new_resume)
        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template("resume_form.html")


# -------------------- RESUME HISTORY --------------------

@app.route("/resume_history")
@login_required
def resume_history():
    resumes = Resume.query.filter_by(user_id=current_user.id)\
        .order_by(Resume.created_at.desc()).all()

    return render_template("resume_history.html", resumes=resumes)


# -------------------- GENERATE AI RESUME --------------------

@app.route("/generate_ai_resume")
@login_required
def generate_ai_resume():
    resume = Resume.query.filter_by(user_id=current_user.id)\
        .order_by(Resume.created_at.desc()).first()

    if not resume:
        return "Please create resume first."

    data = {
        "name": current_user.name,
        "email": current_user.email,
        "phone": current_user.phone,
        "linkedin": current_user.linkedin,
        "github": current_user.github,
        "skills": resume.skills,
        "education": resume.education,
        "experience": resume.experience,
        "projects": resume.projects
    }

    ai_resume = generate_resume_text(data)
    score, suggestions = analyze_resume(data)

    return render_template(
        "ai_resume.html",
        ai_resume=ai_resume,
        score=score,
        suggestions=suggestions,
        user=current_user
    )


# -------------------- DOWNLOAD RESUME PDF --------------------

@app.route("/download_resume")
@login_required
def download_resume():
    resume = Resume.query.filter_by(user_id=current_user.id)\
        .order_by(Resume.created_at.desc()).first()

    if not resume:
        return "No resume found."

    data = {
        "name": current_user.name,
        "email": current_user.email,
        "phone": current_user.phone,
        "linkedin": current_user.linkedin,
        "github": current_user.github,
        "skills": resume.skills,
        "education": resume.education,
        "experience": resume.experience,
        "projects": resume.projects
    }

    resume_text = generate_resume_text(data)
    file_path = f"resume_{current_user.id}.pdf"

    generate_pdf(file_path, resume_text, current_user)

    return send_file(file_path, as_attachment=True)


# -------------------- COVER LETTER --------------------

@app.route("/generate_cover_letter", methods=["GET", "POST"])
@login_required
def generate_cover_letter_route():
    resume = Resume.query.filter_by(user_id=current_user.id)\
        .order_by(Resume.created_at.desc()).first()

    if not resume:
        return "Please create resume first."

    if request.method == "POST":
        job_role = request.form["job_role"]
        company_name = request.form["company_name"]

        data = {
            "name": current_user.name,
            "email": current_user.email,
            "skills": resume.skills,
            "education": resume.education,
            "experience": resume.experience,
            "projects": resume.projects
        }

        cover_letter = generate_cover_letter(data, job_role, company_name)

        return render_template(
            "cover_letter_result.html",
            cover_letter=cover_letter
        )

    return render_template("cover_letter.html")


# -------------------- PORTFOLIO BUILDER --------------------

@app.route("/generate_portfolio")
@login_required
def generate_portfolio():
    resume = Resume.query.filter_by(user_id=current_user.id)\
        .order_by(Resume.created_at.desc()).first()

    if not resume:
        return "Please create resume first."

    return render_template(
        "portfolio.html",
        user=current_user,
        resume=resume
    )


# -------------------- LOGOUT --------------------

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# -------------------- RUN APP --------------------

if __name__ == "__main__":
    app.run(debug=True)