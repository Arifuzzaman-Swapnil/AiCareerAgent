from flask import Blueprint, request, session, render_template, redirect
from ..firebase_config import db
from ..groq_api import call_groq
from ..pdf_utils import extract_text_from_pdf
import json

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/tools/career", methods=["GET", "POST"])
def career_tool():
    if "user_id" not in session:
        return redirect("/")

    suggestion = None

    if request.method == "POST":
        resume_text = request.form["resume"]

        prompt = (
             "এই জীবনবৃত্তান্ত বিশ্লেষণ করো এবং বাংলা ভাষায় ৩টি উপযুক্ত ক্যারিয়ার সাজেস্ট করো:\n\n"
            "আমি কম্পিউটার সায়েন্সে গ্র্যাজুয়েট। পাইথন, মেশিন লার্নিং, ওয়েব ডেভেলপমেন্টে দক্ষ। "
            "আমি বিভিন্ন প্রজেক্টে কাজ করেছি যেমন রিয়েল টাইম চ্যাট অ্যাপ, AI বেসড রেজুমে অ্যানালাইসার।"
        )

        try:
            suggestion = call_groq(prompt)

            # Save suggestion in Firebase
            user_id = session["user_id"]
            doc_ref = db.collection("users").document(user_id)
            doc_ref.set({
                "career_suggestions": suggestion
            }, merge=True)

        except Exception as e:
            suggestion = "Error fetching suggestions: " + str(e)

    return render_template("tools/career.html", suggestion=suggestion)

@ai_bp.route("/tools/resume", methods=["GET", "POST"])
def resume_summarizer():
    if "user_id" not in session:
        return redirect("/")

    summary = None

    if request.method == "POST":
        file = request.files["resume_pdf"]
        if file and file.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(file.read())

            prompt = (
                "এই জীবনবৃত্তান্তটি বিশ্লেষণ করো এবং বাংলা ভাষায় একটি সংক্ষিপ্ত ও প্রাসঙ্গিক সারাংশ তৈরি করো:\n\n"
                + resume_text[:5000]  # সর্বোচ্চ 5000 ক্যারেক্টার পাঠানো
            )

            try:
                summary = call_groq(prompt)

                # Firestore এ সেভ করুন
                user_id = session["user_id"]
                db.collection("users").document(user_id).set({
                    "resume_summary": summary,
                    "resume_text": resume_text
                }, merge=True)

            except Exception as e:
                summary = "❌ Error: " + str(e)

    return render_template("tools/summarizer.html", summary=summary)

@ai_bp.route("/tools/interview_upload", methods=["GET", "POST"])
def generate_interview_questions():
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]
    message = None

    if request.method == "POST":
        file = request.files["resume_pdf"]
        if file and file.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(file.read())

            prompt = (
                "তুমি একজন অভিজ্ঞ টেকনিক্যাল ইন্টারভিউ প্রস্তুতকারক। নিচের জীবনবৃত্তান্ত বিশ্লেষণ করো এবং:\n"
                "- ৩০টি MCQ প্রশ্ন তৈরি করো স্কিল এবং প্রজেক্ট অনুযায়ী। প্রতিটি প্রশ্নে ৪টি অপশন দাও।\n"
                "- ২০টি লজিক্যাল প্রশ্ন তৈরি করো।\n\n"
                "জীবনবৃত্তান্ত:\n" + resume_text[:7000]
            )

            try:
                response = call_groq(prompt)

                # Split MCQ and Logic
                parts = response.split("Logical Questions:")
                mcq_block = parts[0].replace("MCQ Questions:", "").strip()
                logic_block = parts[1].strip() if len(parts) > 1 else ""

                # Parse MCQs
                mcqs = []
                for q_block in mcq_block.split("\n\n"):
                    lines = q_block.strip().split("\n")
                    if len(lines) >= 2:
                        question = lines[0].strip()
                        options = [opt.strip("ABCD. ") for opt in lines[1:5]]
                        mcqs.append({"question": question, "options": options})

                logic_questions = [q.strip() for q in logic_block.split("\n") if q.strip()]

                db.collection("users").document(user_id).set({
                    "mcq_questions": mcqs,
                    "logic_questions": logic_questions
                }, merge=True)

                message = "✅ প্রশ্ন তৈরি হয়েছে! এখন প্র্যাকটিস করুন।"

            except Exception as e:
                message = "❌ Error: " + str(e)

    return render_template("tools/interview_upload.html", message=message)

@ai_bp.route("/tools/interview", methods=["GET"])
def interview_practice():
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]
    doc = db.collection("users").document(user_id).get()
    data = doc.to_dict() if doc.exists else {}

    mcqs = data.get("mcq_questions", [])
    logic_questions = data.get("logic_questions", [])

    return render_template("tools/interview.html", mcqs=mcqs, logic=logic_questions)

@ai_bp.route("/tools/feedback", methods=["GET", "POST"])
def resume_feedback():
    if "user_id" not in session:
        return redirect("/")

    feedback = None
    score = None

    if request.method == "POST":
        file = request.files["resume_pdf"]
        if file and file.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(file.read())

            prompt = (
                "আপনি একজন পেশাদার ক্যারিয়ার কোচ। নিচের জীবনবৃত্তান্ত বিশ্লেষণ করে বিস্তারিত ফিডব্যাক দিন:\n"
                "- দুর্বলতা ও শক্তি নির্দেশ করুন।\n"
                "- উন্নতির সুযোগ এবং সাজেশন দিন।\n"
                "- ১০০ এর মধ্যে একটি সামগ্রিক স্কোর দিন।\n\n"
                "জীবনবৃত্তান্ত:\n" + resume_text[:7000]
            )

            try:
                response = call_groq(prompt)

                # এখানে আমরা ধরে নিচ্ছি Groq রেসপন্স এর শেষে স্কোর আছে
                # উদাহরণ: "Feedback: .... Score: 85"
                import re
                score_match = re.search(r"Score[:\s]*([0-9]{1,3})", response)
                score = int(score_match.group(1)) if score_match else None
                feedback = response

                user_id = session["user_id"]
                db.collection("users").document(user_id).set({
                    "resume_feedback": feedback,
                    "feedback_score": score
                }, merge=True)

            except Exception as e:
                feedback = "❌ Error: " + str(e)

    return render_template("tools/feedback.html", feedback=feedback, score=score)