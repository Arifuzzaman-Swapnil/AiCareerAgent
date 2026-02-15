from flask import Blueprint, request, session, jsonify
from ..firebase_config import db
from ..openai_api import call_openai
from ..pdf_utils import extract_text_from_pdf
import json
import re
from datetime import datetime

ai_bp = Blueprint("ai", __name__, url_prefix="/api/tools")


# ─── Career Counselor ───────────────────────────────────────────────────────────

@ai_bp.route("/career", methods=["POST"])
def career_tool():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.get_json()
    resume_text = data.get("resume", "")

    if not resume_text.strip():
        return jsonify({"error": "Resume text is required"}), 400

    prompt = (
        "এই জীবনবৃত্তান্ত বিশ্লেষণ করো এবং বাংলা ভাষায় ৩টি উপযুক্ত ক্যারিয়ার সাজেস্ট করো।\n\n"
        "প্রতিটি ক্যারিয়ারের জন্য নিচের বিষয়গুলো অন্তর্ভুক্ত করো:\n"
        "১. ক্যারিয়ারের নাম ও কেন এটি উপযুক্ত\n"
        "২. শুরু থেকে শেষ পর্যন্ত বিস্তারিত রোডম্যাপ\n"
        "৩. প্রয়োজনীয় স্কিল ও রিসোর্স\n"
        "৪. আনুমানিক সময়সীমা\n\n"
        "সব কিছু সাবলীল বাংলায় লিখো।\n\n"
        "জীবনবৃত্তান্ত:\n" + resume_text[:8000]
    )

    try:
        suggestion = call_openai(
            prompt,
            system_prompt="তুমি একজন অভিজ্ঞ ক্যারিয়ার কাউন্সেলর। সবসময় বাংলায় উত্তর দাও। বিস্তারিত ও কার্যকর পরামর্শ দাও।"
        )

        user_id = session["user_id"]
        db.collection("users").document(user_id).set({
            "career_suggestions": suggestion,
            "career_updated_at": datetime.now().isoformat()
        }, merge=True)

        return jsonify({"success": True, "suggestion": suggestion})

    except Exception as e:
        return jsonify({"error": f"Career suggestion failed: {str(e)}"}), 500


# ─── Resume Summarizer ──────────────────────────────────────────────────────────

@ai_bp.route("/resume/summarize", methods=["POST"])
def resume_summarizer():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    file = request.files.get("resume_pdf")
    if not file or not file.filename.endswith(".pdf"):
        return jsonify({"error": "Please upload a valid PDF file"}), 400

    resume_text = extract_text_from_pdf(file.read())

    if not resume_text or resume_text.startswith("Error"):
        return jsonify({"error": "Could not extract text from PDF"}), 400

    prompt = (
        "এই জীবনবৃত্তান্তটি বিশ্লেষণ করো এবং বাংলা ভাষায় একটি সংক্ষিপ্ত ও প্রাসঙ্গিক সারাংশ তৈরি করো।\n\n"
        "সারাংশে অন্তর্ভুক্ত করো:\n"
        "১. প্রার্থীর প্রোফাইল সামারি (২-৩ বাক্য)\n"
        "২. মূল দক্ষতাসমূহ\n"
        "৩. শিক্ষাগত যোগ্যতা\n"
        "৪. কাজের অভিজ্ঞতার সারসংক্ষেপ\n"
        "৫. উল্লেখযোগ্য প্রোজেক্ট বা অর্জন\n\n"
        "জীবনবৃত্তান্ত:\n" + resume_text[:6000]
    )

    try:
        summary = call_openai(
            prompt,
            system_prompt="তুমি একজন পেশাদার রিজিউমি বিশ্লেষক। সবসময় বাংলায় সংক্ষিপ্ত ও কার্যকর সারাংশ তৈরি করো।"
        )

        user_id = session["user_id"]
        db.collection("users").document(user_id).set({
            "resume_summary": summary,
            "resume_text": resume_text
        }, merge=True)

        return jsonify({"success": True, "summary": summary})

    except Exception as e:
        return jsonify({"error": f"Summarization failed: {str(e)}"}), 500


# ─── Resume Feedback ─────────────────────────────────────────────────────────────

@ai_bp.route("/resume/feedback", methods=["POST"])
def resume_feedback():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    file = request.files.get("resume_pdf")
    if not file or not file.filename.endswith(".pdf"):
        return jsonify({"error": "Please upload a valid PDF file"}), 400

    resume_text = extract_text_from_pdf(file.read())

    if not resume_text or resume_text.startswith("Error"):
        return jsonify({"error": "Could not extract text from PDF"}), 400

    prompt = (
        "তুমি একজন পেশাদার ক্যারিয়ার কোচ। নিচের জীবনবৃত্তান্ত বিশ্লেষণ করে JSON ফরম্যাটে ফিডব্যাক দাও।\n\n"
        "JSON ফরম্যাট (অবশ্যই valid JSON):\n"
        '{\n'
        '  "score": <0-100 এর মধ্যে একটি সংখ্যা>,\n'
        '  "feedback": "<বিস্তারিত ফিডব্যাক বাংলায়>",\n'
        '  "strengths": ["শক্তি ১", "শক্তি ২", ...],\n'
        '  "weaknesses": ["দুর্বলতা ১", "দুর্বলতা ২", ...],\n'
        '  "suggestions": ["সাজেশন ১", "সাজেশন ২", ...],\n'
        '  "score_reasons": ["স্কোর কমানোর কারণ ১", "কারণ ২", ...]\n'
        '}\n\n'
        "সততার সাথে মূল্যায়ন করো। সব কিছু বাংলায় লিখো।\n\n"
        "জীবনবৃত্তান্ত:\n" + resume_text[:7000]
    )

    try:
        response = call_openai(
            prompt,
            system_prompt="তুমি একজন পেশাদার রিজিউমি রিভিউয়ার। সবসময় valid JSON ফরম্যাটে উত্তর দাও। সততার সাথে মূল্যায়ন করো।",
            json_mode=True
        )

        result = json.loads(response)
        score = result.get("score", 0)
        feedback = result.get("feedback", "")
        strengths = result.get("strengths", [])
        weaknesses = result.get("weaknesses", [])
        suggestions = result.get("suggestions", [])
        score_reasons = result.get("score_reasons", [])

        user_id = session["user_id"]
        db.collection("users").document(user_id).set({
            "resume_feedback": feedback,
            "feedback_score": score
        }, merge=True)

        return jsonify({
            "success": True,
            "score": score,
            "feedback": feedback,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "suggestions": suggestions,
            "score_reasons": score_reasons
        })

    except json.JSONDecodeError:
        return jsonify({"error": "AI response could not be parsed"}), 500
    except Exception as e:
        return jsonify({"error": f"Feedback generation failed: {str(e)}"}), 500


# ─── Interview Prep Analysis ────────────────────────────────────────────────────

@ai_bp.route("/interview/prep", methods=["POST"])
def interview_prep():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    file = request.files.get("resume_pdf")
    if not file or not file.filename.endswith(".pdf"):
        return jsonify({"error": "Please upload a valid PDF file"}), 400

    resume_text = extract_text_from_pdf(file.read())

    if not resume_text or resume_text.startswith("Error"):
        return jsonify({"error": "Could not extract text from PDF"}), 400

    prompt = (
        "তুমি একজন অভিজ্ঞ ক্যারিয়ার কোচ এবং ইন্টারভিউ প্রস্তুতকারক। নিচের জীবনবৃত্তান্ত বিশ্লেষণ করে বিস্তারিত বিবরণ দাও বাংলা ভাষায়:\n\n"
        "১. স্কিল বিশ্লেষণ:\n"
        "   - প্রতিটি স্কিলের জন্য ৫টি করে সম্ভাব্য ইন্টারভিউ প্রশ্ন এবং উত্তর দাও\n"
        "   - টেকনিক্যাল স্কিলগুলোর গভীর ব্যাখ্যা দাও\n"
        "   - প্রতিটি স্কিলে কী কী জানা প্রয়োজন তা বলো\n\n"
        "২. প্রোজেক্ট বিশ্লেষণ:\n"
        "   - প্রতিটি প্রোজেক্ট নিয়ে বিস্তারিত আলোচনা করো\n"
        "   - প্রোজেক্ট থেকে যেসব প্রশ্ন আসতে পারে তা উল্লেখ করো\n"
        "   - প্রোজেক্টের চ্যালেঞ্জ এবং সমাধান নিয়ে আলোচনা করো\n\n"
        "৩. ইন্টারভিউ প্রস্তুতি:\n"
        "   - এই রিজিউমের ভিত্তিতে সবচেয়ে গুরুত্বপূর্ণ প্রশ্নগুলো কী হতে পারে\n"
        "   - কোন কোন বিষয়ে আরও পড়াশোনা করতে হবে\n"
        "   - দুর্বল পয়েন্টগুলো কী এবং কীভাবে উন্নতি করা যাবে\n\n"
        "৪. ব্যবহারিক পরামর্শ:\n"
        "   - কোম্পানির ধরন অনুযায়ী কীভাবে নিজেকে উপস্থাপন করবে\n"
        "   - প্রতিটি স্কিল এবং প্রোজেক্টের জন্য STAR method ব্যবহার করে উত্তর দেওয়ার কৌশল\n\n"
        "দয়া করে সব কিছু বাংলায় এবং বিস্তারিতভাবে লিখো।\n\n"
        "জীবনবৃত্তান্ত:\n" + resume_text[:8000]
    )

    try:
        analysis = call_openai(
            prompt,
            system_prompt="তুমি একজন অভিজ্ঞ টেকনিক্যাল ইন্টারভিউয়ার ও ক্যারিয়ার কোচ। বিস্তারিত ও কার্যকর ইন্টারভিউ প্রস্তুতি গাইড তৈরি করো বাংলায়।"
        )

        user_id = session["user_id"]
        db.collection("users").document(user_id).set({
            "interview_analysis": analysis,
            "resume_text": resume_text
        }, merge=True)

        return jsonify({"success": True, "analysis": analysis})

    except Exception as e:
        return jsonify({"error": f"Interview prep failed: {str(e)}"}), 500


# ─── Generate MCQ Questions ─────────────────────────────────────────────────────

@ai_bp.route("/interview/generate", methods=["POST"])
def generate_interview_questions():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    file = request.files.get("resume_pdf")
    if not file or not file.filename.endswith(".pdf"):
        return jsonify({"error": "Please upload a valid PDF file"}), 400

    resume_text = extract_text_from_pdf(file.read())

    if not resume_text or resume_text.startswith("Error"):
        return jsonify({"error": "Could not extract text from PDF"}), 400

    user_id = session["user_id"]

    prompt = (
        "তুমি একজন এক্সপার্ট টেকনিক্যাল ইন্টারভিউয়ার। নিচের জীবনবৃত্তান্ত বিশ্লেষণ করে ৩০টি কঠিন টেকনিক্যাল MCQ প্রশ্ন তৈরি করো।\n\n"
        "নির্দেশনা:\n"
        "1. প্রতিটি প্রশ্নে ৪টি অপশন থাকবে\n"
        "2. প্রশ্নগুলো resume এর skills, projects এবং experience এর উপর ভিত্তি করে হবে\n"
        "3. প্রশ্নগুলো কঠিন এবং গভীর technical জ্ঞান পরীক্ষা করবে\n"
        "4. Problem-solving এবং conceptual understanding এর প্রশ্ন থাকবে\n"
        "5. সব প্রশ্ন বাংলায় এবং technical terms ইংরেজিতে থাকবে\n"
        "6. correct_answer হলো সঠিক অপশনের index (0-3)\n\n"
        "JSON ফরম্যাট:\n"
        '{\n'
        '  "questions": [\n'
        '    {\n'
        '      "question": "প্রশ্নের টেক্সট",\n'
        '      "options": ["অপশন ১", "অপশন ২", "অপশন ৩", "অপশন ৪"],\n'
        '      "correct_answer": 0,\n'
        '      "explanation": "কেন এই উত্তরটি সঠিক - বিস্তারিত ব্যাখ্যা"\n'
        '    }\n'
        '  ]\n'
        '}\n\n'
        "অবশ্যই ৩০টি প্রশ্ন তৈরি করো।\n\n"
        "Resume:\n" + resume_text[:10000]
    )

    try:
        response = call_openai(
            prompt,
            system_prompt="তুমি একজন এক্সপার্ট টেকনিক্যাল ইন্টারভিউয়ার। অবশ্যই valid JSON ফরম্যাটে ৩০টি MCQ প্রশ্ন তৈরি করো।",
            json_mode=True
        )

        result = json.loads(response)
        questions = result.get("questions", [])

        # Validate each question
        validated_questions = []
        for q in questions:
            if (isinstance(q, dict)
                    and "question" in q
                    and "options" in q
                    and isinstance(q["options"], list)
                    and len(q["options"]) == 4
                    and "correct_answer" in q
                    and isinstance(q["correct_answer"], int)
                    and 0 <= q["correct_answer"] <= 3):
                validated_questions.append({
                    "question": q["question"],
                    "options": q["options"],
                    "correct_answer": q["correct_answer"],
                    "explanation": q.get("explanation", "")
                })

        if len(validated_questions) < 10:
            return jsonify({"error": "Could not generate enough valid questions. Please try again."}), 500

        # Save to Firestore
        db.collection("users").document(user_id).set({
            "interview_questions": validated_questions,
            "resume_text": resume_text,
            "question_generated_at": datetime.now().isoformat()
        }, merge=True)

        return jsonify({
            "success": True,
            "questions": validated_questions,
            "total_questions": len(validated_questions)
        })

    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse AI response. Please try again."}), 500
    except Exception as e:
        return jsonify({"error": f"Question generation failed: {str(e)}"}), 500


# ─── Get Existing Questions ──────────────────────────────────────────────────────

@ai_bp.route("/interview/questions", methods=["GET"])
def get_existing_questions():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    try:
        user_id = session["user_id"]
        doc = db.collection("users").document(user_id).get()

        if doc.exists:
            data = doc.to_dict()
            questions = data.get("interview_questions", [])
            return jsonify({"success": True, "questions": questions})

        return jsonify({"success": True, "questions": []})

    except Exception as e:
        return jsonify({"error": f"Error fetching questions: {str(e)}"}), 500


# ─── Submit Interview Answers ────────────────────────────────────────────────────

@ai_bp.route("/interview/submit", methods=["POST"])
def submit_interview():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    try:
        user_id = session["user_id"]
        data = request.get_json()
        mcq_answers = data.get("mcq_answers", [])

        # Get stored questions
        doc = db.collection("users").document(user_id).get()
        if not doc.exists:
            return jsonify({"error": "No questions found"}), 400

        user_data = doc.to_dict()
        questions = user_data.get("interview_questions", [])

        if not questions:
            return jsonify({"error": "No questions found"}), 400

        # Calculate score
        correct_answers = 0
        total_questions = len(questions)
        answer_details = []

        for i, question in enumerate(questions):
            user_answer = mcq_answers[i] if i < len(mcq_answers) else -1
            correct_answer = question.get("correct_answer", 0)
            is_correct = user_answer == correct_answer

            if is_correct:
                correct_answers += 1

            answer_details.append({
                "question": question.get("question", ""),
                "options": question.get("options", []),
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "explanation": question.get("explanation", "")
            })

        percentage = round((correct_answers / total_questions) * 100, 2) if total_questions > 0 else 0

        # Save results
        db.collection("users").document(user_id).set({
            "interview_results": {
                "score": correct_answers,
                "total": total_questions,
                "percentage": percentage,
                "submitted_at": datetime.now().isoformat()
            },
            "mcq_score": correct_answers,
            "mcq_total": total_questions
        }, merge=True)

        return jsonify({
            "success": True,
            "score": correct_answers,
            "total": total_questions,
            "percentage": percentage,
            "details": answer_details
        })

    except Exception as e:
        return jsonify({"error": f"Error submitting interview: {str(e)}"}), 500


# ─── Get Interview Results ───────────────────────────────────────────────────────

@ai_bp.route("/interview/results", methods=["GET"])
def get_interview_results():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    try:
        user_id = session["user_id"]
        doc = db.collection("users").document(user_id).get()

        if doc.exists:
            data = doc.to_dict()
            results = data.get("interview_results", {})
            return jsonify({"success": True, "results": results})

        return jsonify({"success": True, "results": {}})

    except Exception as e:
        return jsonify({"error": f"Error fetching results: {str(e)}"}), 500
