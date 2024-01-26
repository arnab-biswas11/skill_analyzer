import streamlit as st
import pandas as pd
import altair as alt
from src.data_extractor.web_scapper import web_scrap
from src.data_extractor.skill_extract import pull_skill

scrapped_data = None
extracted_skills = None

def web_scrap_jobs(sp_data,text_page_num, input_page_limit):
    jobs = []
    jd_list = []
    prog = 0
    progress_bar_container = st.empty()
    progress_bar = progress_bar_container.progress(0)

    with st.spinner("Scrapping seek.com.au for jobs..."):
        try:
            while True:
                job = next(sp_data)

                if (input_page_limit == '1' and job[2] > 1) \
                        or (input_page_limit == '2' and job[2] > 2) \
                        or (input_page_limit == '5' and job[2] > 5) \
                        or (input_page_limit == '10' and job[2] > 10) \
                        or (input_page_limit == '20' and job[2] > 20):
                    
                    text_page_num.text("")
                    progress_bar_container.empty()
                    n_jobs = len(jobs)
                    st.success(f"Scrapped {n_jobs} job listings successfully!")
                    break

                jobs.append(job[0])
                jd_list.append(job[0]['header']['job_desc'])
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

    return jobs, jd_list

def extract_skills_from_scapped(jd_list):
            
    data = pull_skill(jd_list).skill_ext()

    top_skills = dict(data.most_common(10))
    skills_df = pd.DataFrame(list(top_skills.items()), 
                                columns=['Skill', 'Number of Job Ads'])

    # Create Altair chart
    chart = alt.Chart(skills_df).mark_bar().encode(
        x=alt.X('Skill:O', 
                sort=alt.EncodingSortField(field='Number of Job Ads', 
                                            op='sum', order='descending')),
        y='Number of Job Ads:Q'
    ).properties(
        title='Top Skills in Job Ads'
    )

    st.altair_chart(chart, use_container_width=True)
            


def main():

    st.title("Skill Analyzer")

    st.write("Welcome to the Skill Analyzer app! \
             This tool helps you scrap data from \
             current job listings at www.seek.com.au \
              and visualise the most in demand skills for \
              the role of your choice.")

    st.write("To get started, enter the desired role and select \
              the page count, then click 'Click to evaluate'. \
             Selecting a higher page count would take more time to \
             extract live job postings but would also extract more jobs!")

    st.markdown("---")

    # Initialize session_state variables
    if 'confirmation_button' not in st.session_state:
        st.session_state.confirmation_button = False
        st.session_state.input_role = ""
        st.session_state.input_page_limit = ""

    # User inputs
    input_role = st.text_input("Enter role:")
    input_page_limit = st.selectbox('Select page count', ('1', '2', '5', '10', '20', 'all pages'))
    
    # Confirmation button
    confirmation_button = st.button("Click to evaluate")

    st.markdown("---")

    # Reset confirmation button if user changes inputs
    if input_role != st.session_state.input_role \
        or input_page_limit != st.session_state.input_page_limit:
        st.session_state.confirmation_button = False

    if confirmation_button:
        if input_role and input_page_limit:
            st.session_state.confirmation_button = True
            st.session_state.input_role = input_role
            st.session_state.input_page_limit = input_page_limit

            global scrapped_data, extracted_skills  

            if scrapped_data is None:
                scrapped_data = web_scrap(job_title=input_role).extract_jobs()
                text_page_num = st.text("")
                return_jobs = web_scrap_jobs(scrapped_data,text_page_num,input_page_limit)
                jobs = return_jobs[0]
                jd_list = return_jobs[1]

            jobs_df = pd.DataFrame(jobs)
            header_df = pd.json_normalize(jobs_df['header'])
            jobs_df = pd.concat([jobs_df['url'], header_df], axis=1)

            st.write("Download web scapped jobs as CSV")
            st.download_button(
                label=':anchor:',
                data=jobs_df.to_csv(index=False, encoding='utf-8', errors='replace'),
                file_name='jobs_data.csv',
                mime='text/csv')
            
            st.markdown("---")

            with st.spinner("Visualising top skills from scanned job descriptions..."):
                extract_skills_from_scapped(jd_list)


# Run the app
if __name__ == "__main__":
    main()
