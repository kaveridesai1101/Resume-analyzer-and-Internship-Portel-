# import spacy (Disabled due to Py3.14 incompatibility)

class ResumeParser:
    def __init__(self):
        # self.nlp = spacy.load("en_core_web_sm")
        pass

    def parse(self, text: str) -> dict:
        # doc = self.nlp(text)
        
        # Enhanced regex-based extraction since Spacy is unavailable
        import re
        
        data = {
            "name": "Candidate",
            "email": "",
            "phone": "",
            "skills": [],
            "soft_skills": [],
            "missing_skills": [],
            "experience": [], 
            "education": [],
            "score": 0,
            "summary": "Resume analyzed successfully.",
            "improvement_tips": [],
            "career_insights": [],
            "skill_strengths": {}
        }
        
        # Extract Email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
        if email_match:
            data["email"] = email_match.group(0)
            
        # Extract Phone
        phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        if phone_match:
            data["phone"] = phone_match.group(0)
            
        # Extract Technical Skills
        common_skills = ["python", "java", "react", "javascript", "typescript", "sql", "aws", "docker", "kubernetes", "fastapi", "django", "flask", "node.js", "html", "css", "tailwind", "rest api", "graphql", "redux", "git", "ci/cd", "agile"]
        found_skills = []
        lower_text = text.lower()
        for skill in common_skills:
            if skill in lower_text:
                skill_name = skill.title() if len(skill) > 3 else skill.upper()
                found_skills.append(skill_name)
                # Heuristic strength
                data["skill_strengths"][skill_name] = "High" if lower_text.count(skill) > 2 else "Medium"
        
        data["skills"] = list(set(found_skills))
        
        # Soft Skills
        soft_skills_list = ["communication", "teamwork", "leadership", "problem solving", "critical thinking", "adaptability", "management", "creativity"]
        found_soft = []
        for ss in soft_skills_list:
            if ss in lower_text:
                found_soft.append(ss.title())
        data["soft_skills"] = found_soft if found_soft else ["Soft skills not clearly mentioned in resume"]
        
        # Experience Breakdown (Heuristic)
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        # Look for patterns like "Software Engineer at Google (2020-2022)"
        for line in lines:
            if " at " in line or " - " in line:
                if any(role in line.lower() for role in ["engineer", "developer", "manager", "analyst", "intern"]):
                    data["experience"].append({
                        "role": line.split(" at ")[0] if " at " in line else line.split(" - ")[0],
                        "company": line.split(" at ")[1] if " at " in line else "Various",
                        "duration": "Duration specified" if any(char.isdigit() for char in line) else "Not specified",
                        "clarity": "Roles are clearly defined with measurable results" if len(line) > 40 else "Experience lacks quantified impact"
                    })
        
        if not data["experience"]:
            data["experience"].append({"role": "Not Detected", "company": "Not Detected", "duration": "-", "clarity": "Experience section missing or unclear"})

        # Education Section (Heuristic)
        edu_keywords = ["university", "college", "institute", "bachelor", "master", "phd", "degree", "school"]
        for line in lines:
            if any(k in line.lower() for k in edu_keywords):
                data["education"].append({
                    "institution": line,
                    "degree": "Degree detected",
                    "field": "Field detected"
                })
        if not data["education"]:
            data["education"].append({"institution": "Not Detected", "degree": "-", "field": "-"})

        # Improvement Tips
        tips = []
        if len(found_skills) < 5: tips.append("Improve keyword usage for better ATS compatibility")
        if not found_soft: tips.append("Include more soft skills relevant to your field")
        if len(data["experience"]) < 2: tips.append("Add measurable achievements to your experience section")
        data["improvement_tips"] = tips if tips else ["Your resume looks solid! Focus on quantifying achievements."]

        # Career Insights
        insights = []
        if "AWS" not in data["skills"]: insights.append("Certifications to consider: AWS Certified Solutions Architect")
        if "TypeScript" not in data["skills"]: insights.append("Skills to improve: Modern TypeScript patterns")
        insights.append("Experience gaps to address: Project management experience")
        data["career_insights"] = insights

        # Final Score
        base_score = 50
        skill_boost = min(len(found_skills) * 5, 25)
        exp_boost = min(len(data["experience"]) * 10, 20)
        data["score"] = base_score + skill_boost + exp_boost
        
        if data["score"] > 80:
            data["summary"] = "Outstanding profile! Your technical stack is very robust."
        elif data["score"] > 60:
            data["summary"] = "Strong profile. Adding a few more modern cloud skills could help you stand out."
        else:
            data["summary"] = "Decent start. Consider highlighting more specific technical keywords."

        # Extract Name
        if lines:
            data["name"] = lines[0]

        return data

        return data
