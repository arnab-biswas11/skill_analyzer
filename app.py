import streamlit as st
from collections import Counter
import pandas as pd
import concurrent.futures
import altair as alt
from src.data_extractor.web_scapper import web_scrap
from src.data_extractor.skill_extract import pull_skill


scrapped_data = None
extracted_skills = None

def web_scrap_jobs(sp_data,text_page_num, page_num_option):
    jobs = []
    prog = 0
    progress_bar_container = st.empty()
    progress_bar = progress_bar_container.progress(0)

    with st.spinner("Scrapping seek.com.au for jobs..."):
        try:
            while True:
                job = next(sp_data)

                if (page_num_option == '1-5' and job[2] > 5) \
                        or (page_num_option == '1-10' and job[2] > 10) \
                        or (page_num_option == '1-15' and job[2] > 15) \
                        or (page_num_option == '1-25' and job[2] > 25):
                    
                    text_page_num.text("")
                    progress_bar_container.empty()
                    n_jobs = len(jobs)
                    st.success(f"Scrapped {n_jobs} job listings successfully!")
                    break

                jobs.append(job[0])
                text_page = "Scanning page " + str(job[2])
                text_page_num.text(text_page)
                progress_bar.progress((prog + 1) / job[1])
                prog += 1
                if prog >= job[1]:
                    prog = 0

        except StopIteration as e:
            text_page_num.text("")
            progress_bar_container.empty()
            n_jobs = len(jobs)
            st.success(f"Scrapped {n_jobs} job listings successfully!")

    return jobs

def main():
    st.title("Skill Analyzer")

    # Initialize session_state variables
    if 'confirmation_button' not in st.session_state:
        st.session_state.confirmation_button = False
        st.session_state.user_input = ""
        st.session_state.page_num_option = ""

    # User inputs
    user_input = st.text_input("Enter role:")
    page_num_option = st.selectbox('Select page count', ('1-5', '1-10', '1-15', '1-25', 'all pages'))

    # Confirmation button
    confirmation_button = st.button("Click to evaluate")

    # Reset confirmation button if user changes inputs
    if user_input != st.session_state.user_input or page_num_option != st.session_state.page_num_option:
        st.session_state.confirmation_button = False

    if confirmation_button:
        if user_input and page_num_option:
            st.session_state.confirmation_button = True
            st.session_state.user_input = user_input
            st.session_state.page_num_option = page_num_option

    # user_input = st.text_input("Enter role:")
    # page_num_option = st.selectbox( 'Select page count',
    # ('1-5', '1-10', '1-15', '1-25', 'all pages'),
    # index=None)

    # if user_input and page_num_option:
            global scrapped_data, extracted_skills  

            if scrapped_data is None:
                scrapped_data = web_scrap(job_title=user_input).extract_jobs()
                text_page_num = st.text("")
                jobs = web_scrap_jobs(scrapped_data,text_page_num, page_num_option)

            jobs_df = pd.DataFrame(jobs)
            header_df = pd.json_normalize(jobs_df['header'])
            jobs_df = pd.concat([jobs_df['url'], header_df], axis=1)

            st.download_button(
                label='Download web scapped jobs as CSV',
                data=jobs_df.to_csv(index=False, encoding='utf-8', errors='replace'),
                file_name='jobs_data.csv',
                mime='text/csv')

            data = pull_skill(job_details=jobs)

            prog = 0
            progress_bar_container = st.empty()
            progress_bar = progress_bar_container.progress(0)

            # Count occurrences of each skill
            skill_counts = Counter()

            top_skills = dict(skill_counts.most_common(10))
            skills_df = pd.DataFrame(list(top_skills.items()), columns=['Skill', 'Number of Job Ads'])

            # Create Altair chart
            chart = alt.Chart(skills_df).mark_bar().encode(
                x=alt.X('Skill:O', sort=alt.EncodingSortField(field='Number of Job Ads', op='sum', order='descending')),
                y='Number of Job Ads:Q'
            ).properties(
                title='Top 10 Skills in Job Ads',
                width=alt.Step(80)
            )

            dp_chart = st.altair_chart(chart, use_container_width=True)
            n_jobs = len(jobs)
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for skill_job in data.job_iter_batch(user_input):
                    skill_counts.update(skill_job)
                    top_skills = dict(skill_counts.most_common(10))
                    skills_df = pd.DataFrame(list(top_skills.items()), columns=['Skill', 'Number of Job Ads'])

                    chart = alt.Chart(skills_df).mark_bar().encode(
                        x=alt.X('Skill:O', sort=alt.EncodingSortField(field='Number of Job Ads', op='sum', order='descending')),
                        y='Number of Job Ads:Q'
                    ).properties(
                        title='Top 10 Skills in Job Ads',
                        width=alt.Step(80)
                    )

                    dp_chart.altair_chart(chart, use_container_width=True)

                    progress_bar.progress((prog + 1) / n_jobs)
                    prog += 1

# Run the app
if __name__ == "__main__":
    main()

# def main():
#     st.title("Skill Analyzer")
#     user_input = st.text_input("Enter role:")

#     if user_input:

#         text_page_num = st.text("Scanning page 1")

#         scrapped_data = web_scrap(job_title=user_input).extract_jobs()

#         prog = 0
#         jobs = []

#         progress_bar_container = st.empty()
#         progress_bar = progress_bar_container.progress(0)

#         with st.spinner("Scapping seek.com.au for jobs..."):

#             try:
#                 while True:
#                     job = next(scrapped_data)
#                     jobs.append(job[0])

#                     text_page = "Scanning page "+ str(job[2])
#                     text_page_num.text(text_page)

#                     progress_bar.progress((prog + 1) / job[1])
#                     prog+=1
#                     if prog>= job[1]:
#                         prog=0

#             except StopIteration as e:
#                 text_page_num.text("")
#                 progress_bar_container.empty()
#                 n_jobs = len(jobs)
#                 scrapped_text = "Scrapped " + str(n_jobs) + " job listings successfully! Analyzing top 10 demanded skills"

#                 st.success(scrapped_text)

#         jobs_df = pd.DataFrame(jobs)
#         header_df = pd.json_normalize(jobs_df['header'])
#         jobs_df = pd.concat([jobs_df, header_df], axis=1)

#         button_jobs = st.button('Click here if you would like to download the web scapped jobs')

#         if button_jobs:
#             st.download_button(
#                 label='Download CSV',
#                 data=jobs_df.to_csv(index=False),
#                 file_name='jobs_data.csv',
#                 mime='text/csv')

#         button_skill = st.button('Click here if you would like to visualize skills')

#         if button_skill:
#             data = pull_skill(job_details=jobs)

#             # Batch processing
#             prog = 0
#             progress_bar_container = st.empty()
#             progress_bar = progress_bar_container.progress(0)

#             # Count occurrences of each skill
#             skill_counts = Counter()

#             top_skills = dict(skill_counts.most_common(10))
#             skills_df = pd.DataFrame(list(top_skills.items()), columns=['Skill', 'Number of Job Ads'])

#             # Create Altair chart
#             chart = alt.Chart(skills_df).mark_bar().encode(
#                 x=alt.X('Skill:O', sort=alt.EncodingSortField(field='Number of Job Ads', op='sum', order='descending')),
#                 y='Number of Job Ads:Q'
#             ).properties(
#                 title='Top 10 Skills in Job Ads',
#                 width=alt.Step(80)
#             )

#             dp_chart = st.altair_chart(chart, use_container_width=True)
            
#             with concurrent.futures.ThreadPoolExecutor() as executor:
#                 for skill_job in data.job_iter_batch():
#                     # skills.append(skill_job)
                    
#                     # Update skill_counts after each iteration
#                     skill_counts.update(skill_job)

#                     # Update the DataFrame for Seaborn
#                     top_skills = dict(skill_counts.most_common(10))
#                     skills_df = pd.DataFrame(list(top_skills.items()), columns=['Skill', 'Number of Job Ads'])

#                     chart = alt.Chart(skills_df).mark_bar().encode(
#                         x=alt.X('Skill:O', sort=alt.EncodingSortField(field='Number of Job Ads', op='sum', order='descending')),
#                         y='Number of Job Ads:Q'
#                     ).properties(
#                         title='Top 10 Skills in Job Ads',
#                         width=alt.Step(80)
#                     )

#                     dp_chart.altair_chart(chart, use_container_width=True)

#                     progress_bar.progress((prog + 1) / n_jobs)
#                     prog += 1

