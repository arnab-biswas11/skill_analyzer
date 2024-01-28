from skills.pipeline.extract_skills.extract_skills import ExtractSkills
from collections import Counter

es = ExtractSkills(config_name="extract_skills_lightcast", local=True)
es.load()

# pip install git+https://github.com/nestauk/ojd_daps_skills.git@dev

class pull_skill:

    def __init__(self,
                 job_details) -> None:
        self.job_details = job_details

    def skill_ext(self):

        job_skills_matched = es.extract_skills(self.job_details)

        skill_counter = Counter()

        for entry in job_skills_matched:
            skills = entry['SKILL']
            for potential_skill, (hier_skill, identifier) in skills:
                # Determine whether to use the skill or the identifier
                skill_to_count = hier_skill if len(identifier) != 20 else potential_skill
                skill_counter[skill_to_count] += 1

        return skill_counter
