from flask import Blueprint, Flask, request, session, render_template, redirect, jsonify
from ..firebase_config import db
from ..groq_api import call_groq
from ..pdf_utils import extract_text_from_pdf
import json
import re
from datetime import datetime
import PyPDF2  # PDF text extraction এর জন্য
import io

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
             "আমার জীবন বৃত্তান্ত অত্যন্ত সাবলিল আর সহজ ভাষায় বুঝিয়ে দাও এই বিষয়ের উপরে। আমি কিভাবে তোমার দেওয়া ক্যারিয়ারে আগিয়ে যাবো? আমাকে একদম শুরু থেকে শেষ পর্যন্ত রোড ম্যাপ দাও। আমাকে সব কিছু বাঙলায় দাও" +resume_text
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
    analysis = None

    if request.method == "POST":
        file = request.files["resume_pdf"]
        if file and file.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(file.read())

            prompt = (
                "তুমি একজন অভিজ্ঞ ক্যারিয়ার কোচ এবং ইন্টারভিউ প্রস্তুতকারক। নিচের জীবনবৃত্তান্ত বিশ্লেষণ করে বিস্তারিত বিবরণ দাও বাংলা ভাষায়:\n\n"
                
                "১. কিল বিশ্লেষণ:\n"
                "   - প্রতিটি স্কিলের জন্য সম্ভাব্য ইন্টারভিউ প্রশ্ন এবং উত্তর দাও। প্রতিটার জন্য ৫টা করে প্রশ্ন-উত্তর দাও।\n"
                "   - টেকনিক্যাল স্কিল গুলোর গভীর ব্যাখ্যা দাও\n"
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
                "   - প্রতিটি স্কিল এবং প্রোজেক্টের জন্য STAR (Situation, Task, Action, Result) method ব্যবহার করে উত্তর দেওয়ার কৌশল\n\n"
                
                "দয়া করে সব কিছু বাংলায় এবং বিস্তারিত ভাবে লিখো যেন ইন্টারভিউতে সহজে উত্তর দিতে পারি।\n\n"
                "জীবনবৃত্তান্ত:\n" + resume_text[:7000]
            )

            try:
                analysis = call_groq(prompt)

                # Firestore এ সেভ করুন
                db.collection("users").document(user_id).set({
                    "interview_analysis": analysis,
                    "resume_text": resume_text
                }, merge=True)

            except Exception as e:
                analysis = "❌ Error: " + str(e)

    return render_template("tools/interview_upload.html", analysis=analysis)

@ai_bp.route("/tools/feedback", methods=["GET", "POST"])
def resume_feedback():
    if "user_id" not in session:
        return redirect("/")

    feedback = None
    score = None

    def bangla_to_english_number(text):
        bangla_digit_map = {
            '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4',
            '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9'
        }
        return ''.join(bangla_digit_map.get(char, char) for char in text)

    if request.method == "POST":
        file = request.files["resume_pdf"]
        if file and file.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(file.read())

            prompt = (
                "আপনি একজন পেশাদার ক্যারিয়ার কোচ। নিচের জীবনবৃত্তান্ত বিশ্লেষণ করে বিস্তারিত ফিডব্যাক দিন বাংলা ভাষায় এবং কোনো লিখা বোল্ড করার কোনো দরকার নেই।:\n"
                "- দুর্বলতা ও শক্তি নির্দেশ করুন।\n"
                "- উন্নতির সুযোগ এবং সাজেশন দিন।\n"
                "- স্কিল গুলা হোট করে লিস্ট দিন।\n"
                "- আমার পিডিএফকে এনালাইসিস করে সততার সাথে ১০০ এর মধ্যে একটি সামগ্রিক স্কোর দিন। এরকম ফরমেটে একটি লাইন দিন যেমন: 'score: 85/100' অথবা 'স্কোর: 85/100'। দয়া করে শুধু স্কোরটি ইংরেজি সংখ্যায় লিখুন।\n\n"
                "- স্কোর কি কি কারনে কমিয়েছেন পয়েন্ট করে বিবরণ দিন।\n"
                "- জীবনবৃত্তান্ত:\n" + resume_text[:7000]
            )

            try:
                response = call_groq(prompt)

                # ✅ স্কোর extract করা
                import re
                match = re.search(r"(?:score|স্কোর)[:\s]*([০১২৩৪৫৬৭৮৯0-9]{1,3})", response, re.IGNORECASE)
                if match:
                    raw_score = match.group(1)
                    english_score = bangla_to_english_number(raw_score)
                    score = int(english_score)
                else:
                    score = None

                feedback = response

                # ✅ Firestore এ সেভ করুন
                user_id = session["user_id"]
                db.collection("users").document(user_id).set({
                    "resume_feedback": feedback,
                    "feedback_score": score
                }, merge=True)

            except Exception as e:
                feedback = "❌ Error: " + str(e)

    return render_template("tools/feedback.html", feedback=feedback, score=score)

# Interview related routes - Add these to your existing ai_routes.py
# ai_routes.py তে এই route টি add করুন (অন্য routes এর সাথে)
@ai_bp.route("/tools/interview", methods=["GET"])
def interview_practice():
    """Resume-based interview practice page"""
    if "user_id" not in session:
        return redirect("/")
    
    return render_template("tools/interview.html")

@ai_bp.route("/tools/interview/generate", methods=["POST"])
def generate_interview_question():
    """Generate MCQ questions based on uploaded resume"""
    if "user_id" not in session:
        return jsonify({"error": "User not authenticated"}), 401

    try:
        file = request.files["resume_pdf"]
        if not file or not file.filename.endswith(".pdf"):
            return jsonify({"error": "Please upload a valid PDF file"}), 400

        user_id = session["user_id"]
        resume_text = extract_text_from_pdf(file.read())

        # Enhanced prompt for generating technical MCQ questions
        mcq_prompt = f"""
        আপনি একজন এক্সপার্ট টেকনিক্যাল ইন্টারভিউয়ার। নিচের জীবনবৃত্তান্ত বিশ্লেষণ করে ৩০টি কঠিন টেকনিক্যাল MCQ প্রশ্ন তৈরি করুন।

        নির্দেশনা:
        1. প্রতিটি প্রশ্নে ৪টি অপশন থাকবে
        2. প্রশ্নগুলো resume এর skills, projects এবং experience এর উপর ভিত্তি করে হবে
        3. প্রশ্নগুলো কঠিন এবং গভীর technical জ্ঞান পরীক্ষা করবে
        4. প্রতিটি skill এবং project এর জন্য advanced level প্রশ্ন করুন
        5. Problem-solving এবং conceptual understanding এর প্রশ্ন থাকবে
        6. সব প্রশ্ন বাংলায় এবং technical terms ইংরেজিতে থাকবে

        JSON Format (অবশ্যই valid JSON হতে হবে):
        {{
            "questions": [
                {{
                    "question": "প্রশ্নের টেক্সট",
                    "options": ["অপশন ১", "অপশন ২", "অপশন ৩", "অপশন ৪"],
                    "correct_answer": 0,
                    "explanation": "কেন এই উত্তরটি সঠিক - বিস্তারিত ব্যাখ্যা"
                }}
            ]
        }}

        Resume Text:
        {resume_text[:10000]}
        
        অবশ্যই ৩০টি প্রশ্ন তৈরি করুন এবং valid JSON format এ response দিন।
        """

        # Generate MCQ questions
        mcq_response = call_groq(mcq_prompt)
        
        # Parse JSON response with better error handling
        try:
            mcq_data = clean_json_response(mcq_response)
            questions = mcq_data.get("questions", [])
            
            # Validate questions
            if not questions or len(questions) < 20:
                # If we don't get enough questions, generate more
                fallback_questions = generate_fallback_questions(resume_text)
                questions.extend(fallback_questions)
            
            # Ensure we have exactly 30 questions
            if len(questions) > 30:
                questions = questions[:30]
            elif len(questions) < 30:
                # Generate additional questions if needed
                additional_questions = generate_additional_questions(resume_text, 30 - len(questions))
                questions.extend(additional_questions)
            
            # Save to Firestore
            db.collection("users").document(user_id).set({
                "interview_questions": questions,
                "resume_text": resume_text,
                "question_generated_at": datetime.now().isoformat()
            }, merge=True)
            
            return jsonify({
                "success": True,
                "questions": {
                    "mcq": questions,
                    "logic": []
                },
                "total_questions": len(questions)
            })
            
        except Exception as json_error:
            # If JSON parsing fails, generate fallback questions
            fallback_questions = generate_fallback_questions(resume_text)
            
            # Save fallback questions
            db.collection("users").document(user_id).set({
                "interview_questions": fallback_questions,
                "resume_text": resume_text,
                "question_generated_at": datetime.now().isoformat()
            }, merge=True)
            
            return jsonify({
                "success": True,
                "questions": {
                    "mcq": fallback_questions,
                    "logic": []
                },
                "total_questions": len(fallback_questions)
            })
            
    except Exception as e:
        return jsonify({"error": f"Error generating questions: {str(e)}"}), 500

@ai_bp.route("/tools/interview/questions", methods=["GET"])
def get_existing_questions():
    """Get existing interview questions for the user"""
    if "user_id" not in session:
        return jsonify({"error": "User not authenticated"}), 401

    try:
        user_id = session["user_id"]
        doc = db.collection("users").document(user_id).get()
        
        if doc.exists:
            data = doc.to_dict()
            questions = data.get("interview_questions", [])
            
            return jsonify({
                "success": True,
                "questions": {
                    "mcq": questions,
                    "logic": []
                }
            })
        else:
            return jsonify({
                "success": True,
                "questions": {
                    "mcq": [],
                    "logic": []
                }
            })
            
    except Exception as e:
        return jsonify({"error": f"Error fetching questions: {str(e)}"}), 500

@ai_bp.route("/tools/interview/submit", methods=["POST"])
def submit_interview():
    """Submit interview answers and calculate score"""
    if "user_id" not in session:
        return jsonify({"error": "User not authenticated"}), 401

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
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "explanation": question.get("explanation", "")
            })
        
        # Calculate percentage
        percentage = round((correct_answers / total_questions) * 100, 2) if total_questions > 0 else 0
        
        # Save results
        result_data = {
            "interview_results": {
                "score": correct_answers,
                "total": total_questions,
                "percentage": percentage,
                "answers": answer_details,
                "submitted_at": datetime.now().isoformat()
            }
        }
        
        db.collection("users").document(user_id).set(result_data, merge=True)
        
        return jsonify({
            "success": True,
            "score": correct_answers,
            "total": total_questions,
            "percentage": percentage,
            "details": answer_details
        })
        
    except Exception as e:
        return jsonify({"error": f"Error submitting interview: {str(e)}"}), 500

@ai_bp.route("/tools/interview/results", methods=["GET"])
def get_interview_results():
    """Get interview results for the user"""
    if "user_id" not in session:
        return jsonify({"error": "User not authenticated"}), 401

    try:
        user_id = session["user_id"]
        doc = db.collection("users").document(user_id).get()
        
        if doc.exists:
            data = doc.to_dict()
            results = data.get("interview_results", {})
            
            return jsonify({
                "success": True,
                "results": results
            })
        else:
            return jsonify({
                "success": True,
                "results": {}
            })
            
    except Exception as e:
        return jsonify({"error": f"Error fetching results: {str(e)}"}), 500

# Helper functions
def clean_json_response(response_text):
    """Clean and validate JSON response from AI"""
    try:
        # Remove markdown formatting
        cleaned = response_text.strip()
        if cleaned.startswith('```json'):
            cleaned = cleaned[7:]
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]
        
        # Try to parse JSON
        data = json.loads(cleaned)
        return data
    except:
        raise Exception("Invalid JSON response")

def generate_fallback_questions(resume_text):
    """Generate fallback questions if AI response fails"""
    # Extract key skills and technologies from resume
    common_skills = ['Python', 'JavaScript', 'React', 'Node.js', 'Django', 'Flask', 'MongoDB', 'MySQL', 'Git', 'AWS']
    
    questions = []
    
    # Generate basic questions for common skills
    for i, skill in enumerate(common_skills):
        if skill.lower() in resume_text.lower():
            questions.append({
                "question": f"{skill} এর ক্ষেত্রে আপনার অভিজ্ঞতা কেমন?",
                "options": [
                    "খুবই ভালো",
                    "ভালো",
                    "মাঝারি",
                    "শুরুর দিকে"
                ],
                "correct_answer": 0,
                "explanation": f"{skill} সম্পর্কে গভীর জ্ঞান থাকা প্রয়োজন।"
            })
    
    # Add more generic technical questions to reach 30
    generic_questions = [
        {
            "question": "Object-Oriented Programming এর মূল নীতি কয়টি?",
            "options": ["৩টি", "৪টি", "৫টি", "৬টি"],
            "correct_answer": 1,
            "explanation": "OOP এর ৪টি মূল নীতি: Encapsulation, Inheritance, Polymorphism, Abstraction"
        },
        {
            "question": "Database এ Index এর কাজ কী?",
            "options": ["Data store করা", "Query speed বাড়ানো", "Security দেওয়া", "Backup নেওয়া"],
            "correct_answer": 1,
            "explanation": "Index database query এর speed বৃদ্ধি করে।"
        },
        {
            "question": "REST API এর HTTP method গুলো কী কী?",
            "options": ["GET, POST", "GET, POST, PUT", "GET, POST, PUT, DELETE", "সব গুলো"],
            "correct_answer": 3,
            "explanation": "REST API তে GET, POST, PUT, DELETE, PATCH সহ আরো method ব্যবহার হয়।"
        }
    ]
    
    questions.extend(generic_questions)
    
    # Ensure we have 30 questions
    while len(questions) < 30:
        questions.append({
            "question": f"প্রশ্ন {len(questions) + 1}: সফটওয়্যার ডেভেলপমেন্টে কোন বিষয়টি সবচেয়ে গুরুত্বপূর্ণ?",
            "options": ["Code quality", "Performance", "Security", "সব গুলো"],
            "correct_answer": 3,
            "explanation": "সফটওয়্যার ডেভেলপমেন্টে সব বিষয়ই গুরুত্বপূর্ণ।"
        })
    
    return questions[:30]

def generate_additional_questions(resume_text, count_needed):
    """Generate additional questions if needed"""
    additional_questions = []
    
    for i in range(count_needed):
        additional_questions.append({
            "question": f"অতিরিক্ত প্রশ্ন {i + 1}: আপনার প্রোজেক্টে কী ধরনের চ্যালেঞ্জ মোকাবেলা করেছেন?",
            "options": [
                "Technical challenges",
                "Team collaboration",
                "Time management",
                "সব ধরনের চ্যালেঞ্জ"
            ],
            "correct_answer": 3,
            "explanation": "প্রোজেক্টে সব ধরনের চ্যালেঞ্জ মোকাবেলা করতে হয়।"
        })
    
    return additional_questions

# Additional utility function for PDF text extraction
def extract_text_from_pdf(pdf_content):
    """Extract text from uploaded PDF file"""
    try:
        # You'll need to implement this based on your PDF library
        # Common libraries: PyPDF2, pdfplumber, or python-docx for PDF
        import PyPDF2
        import io
        
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"