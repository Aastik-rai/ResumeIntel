def calculate_score(skills, experience, projects, ats):
    if skills<0 or skills>100:
        return("invalid score")
    if experience<0 or experience>100:
            return("invalid experience")
    if projects<0 or projects>100:
            return("invalid projects")
    if ats<0 or ats>100:
            return("invalid ats")
    return(skills*0.4)+(experience*0.25)+(projects*0.20)+(ats*0.15)