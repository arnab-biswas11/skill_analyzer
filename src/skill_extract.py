from src.skills.extract_skills import ExtractSkills
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
                # skill_to_count = hier_skill if len(identifier) != 20 else potential_skill
                skill_counter[potential_skill] += 1

        return skill_counter
    
# x = pull_skill(["Your career in healthcare made personal At Medibank we've recently unified our health services under one brand - Amplar Health.  With over 1000 employees, our nurses, GPs and other amazing allied health professionals our focus is on improving healthcare experiences and championing greater access, choice, and control for people in Australia when it comes to managing their health.   The Opportunity Are you someone passionate about creating and maintaining best in-class preventative health programs? If so, we have a new and exciting opportunity to join our team at Amplar health!!! To better support the prevention ambition for Medibank, Amplar Health's Prevention Hub has recently been established.  As a key member of the Amplar Health Prevention Squad, the Product Owner, will work closely with the Prevention Squad/Hub, Health Operations, Business Development, Marketing, Customer Experience, Tech & Ops including Digital, amongst other stakeholders. As a Product owner you will act as subject matter expert in a portfolio of preventative health programs. You will drive the design, development, re-design, and improvement of the preventative health programs, develop and execute a portfolio strategy, including growth strategy that can lead to maximising our Prevention Health programs to make them commercially successful. For the right person, the role could be based anywhere with flexibility to work in the office or from home as needed. Come and join a dynamic and talented team that is looking to change the way of delivering health care in Australia! About You  key to this role someone with proven experience in managing, designing, and delivering health programs, including digital/clinician-based programs. You will have exceptional product expertise and extensive networks and influence in the broader health and digital ecosystem. You will have significant experience in both commercial and start up environments. Excellent project management and prioritisation skills with the ability to juggle multiple competing priorities.   Our much-loved PerksAlong with joining an outstanding organisation that is transforming the delivery of healthcare, working at Amplar health also means:    Great work life balance Impressive, 35% subsidised Medibank/ahm health insurance (which can also include your pets, cars, upcoming travel, and house!)!  Right now, our employees also have a 25% discount on travel insurance.  14-weeks paid parental leave for all eligible employees, regardless of whether you are the primary or secondary carer - in fact, we're the proud winners of the number one workplace for dads.  Feel Good Health Hub - a digital platform for your mobile that gives you access to a range of clinical health and wellbeing services at your fingertips - the ease in booking appointments with trusted professionals such as a health & wellbeing check in.  Great Discounts - as an employee you can access various discounts across a range of partners including Apple, Samsung, Telstra, HP, SpecSavers, Cinema & Theme park tickets (Spendless), Wyndham Travel and more.   Learn more about Amplar Health at https://amplarhealth.com.au We celebrate diversity of thought because we want to make better decisions for our customers and our people. As we work towards our goal of making health personal, we value the knowledge and contribution of Aboriginal and Torres Strait Islanders.  We're also committed to supporting better accessibility for our customers and our people. We encourage you to talk to us about any adjustment or additional support you may require.  Employees in face-to-face healthcare roles will be required to be fully vaccinated for COVID-19 as a condition of employment. "]).skill_ext()
# print(x)
