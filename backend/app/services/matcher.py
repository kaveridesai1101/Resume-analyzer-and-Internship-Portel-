from typing import List, Dict

class MatchingEngine:
    def __init__(self):
        pass

    def calculate_score(self, resume_data: Dict, internship_data: Dict) -> Dict:
        """
        Calculates match score based on weighted criteria.
        Match Score = (Skill Match × 40%) + (Experience × 30%) + (Education × 15%) + (ATS × 10%) + (Keyword Match × 5%)
        """
        
        # 1. Skill Match (40%)
        resume_skills = set([s.lower() for s in resume_data.get("skills", [])])
        internship_skills = set([s.lower() for s in internship_data.get("required_skills", [])])
        
        if not internship_skills:
            skill_score = 0
        else:
            matches = resume_skills.intersection(internship_skills)
            skill_score = (len(matches) / len(internship_skills)) * 100

        # 2. Experience Match (30%)
        # Simplify: if experience matches or exceeds, 100%, else proportional
        # Placeholder logic
        experience_score = 80 # default for now
        
        # 3. Education Match (15%)
        education_score = 90 # default for now
        
        # 4. ATS Score (10%)
        ats_score = 85 # default
        
        # 5. Keyword Match (5%)
        keyword_score = 70 # default
        
        # Weighted Total
        total_score = (
            (skill_score * 0.40) +
            (experience_score * 0.30) +
            (education_score * 0.15) +
            (ats_score * 0.10) +
            (keyword_score * 0.05)
        )
        
        return {
            "total_score": round(total_score, 1),
            "breakdown": {
                "skill_match": round(skill_score, 1),
                "experience_match": experience_score,
                "education_match": education_score,
                "ats_score": ats_score,
                "keyword_match": keyword_score
            },
            "explanation": f"Matched {len(matches)} out of {len(internship_skills)} required skills.",
            "missing_skills": list(internship_skills - resume_skills)
        }
