import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
import concurrent.futures


nlp = spacy.load("en_core_web_lg")
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

class pull_skill:

    def __init__(self,
                 job_details) -> None:
        self.job_details = job_details

    def skill_extract(self, job_description, role):

        keyword_doc = nlp(role.lower())
        skills = skill_extractor.annotate(job_description)        
        skill_set = set(
            [entry["doc_node_value"] 
             for entry in skills["results"]["full_matches"] + skills["results"]["ngram_scored"]
             if keyword_doc.similarity(nlp(entry["doc_node_value"].lower())) < 0.7]
             )

        return skill_set

    def job_iter_batch(self, role):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Process job descriptions in batches concurrently
            future_to_job = {executor.submit(self.skill_extract, job['header']['job_desc'], role): job for job in self.job_details}
            for future in concurrent.futures.as_completed(future_to_job):
                try:
                    skills = future.result()
                    yield skills
                except Exception as e:
                    # Handle any exceptions during skill extraction
                    print(f"Exception occurred: {e}")

