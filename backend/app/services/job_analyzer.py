# import spacy

class JobAnalyzer:
    def __init__(self):
        # self.nlp = spacy.load("en_core_web_sm")
        pass

    def analyze(self, description: str) -> dict:
        # doc = self.nlp(description)
        
        # Placeholder extraction
        # Simple extraction based on keywords (to be enhanced)
        tokens = description.lower().split()
        unique_tokens = list(set(tokens))
        
        return {
            "title": "Extracted Title", # simplified
            "required_skills": unique_tokens[:5], # Mock top 5 words as skills
            "preferred_skills": unique_tokens[5:10],
            "experience_level": "Mid-Senior" # Placeholder
        }
