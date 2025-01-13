import re

def extract_skills(resume_text, skill_list):
    # Convert text to lowercase for consistency
    resume_text = resume_text.lower()
    matched_skills = [skill for skill in skill_list if skill.lower() in resume_text]
    return matched_skills

# Example usage
resume = """I am skilled in Python, data analysis, and web development."""
skills = ["Python", "Machine Learning", "Web Development", "Data Analysis"]
print(extract_skills(resume, skills))
# Output: ['Python', 'Web Development', 'Data Analysis']