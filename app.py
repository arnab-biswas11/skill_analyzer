import streamlit as st
import pandas as pd
import altair as alt
import PyPDF2 as pdf

from src.data_extractor.web_scapper import web_scrap
from src.skill_extract import pull_skill

scrapped_data = None
extracted_skills = None

def web_scrap_jobs(sp_data,text_page_num, input_page_limit,input_role):
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
            if n_jobs>0:
                st.success(f"Scrapped {n_jobs} job listings successfully!")
            else:
                st.error(f"No ads with job title {input_role}, please re-enter a new role (example role: Data Analyst)")

    return jobs, jd_list

def extract_skills_from_scapped(jd_list):
            
    skill_list = pull_skill(jd_list).skill_ext()[1]
    skill_freq = pull_skill(jd_list).skill_ext()[0]

    top_skills = dict(skill_freq.most_common(10))
    skills_df = pd.DataFrame(list(top_skills.items()), 
                                columns=['Skill', 'Number of Job Ads'])

    return skill_list, skill_freq, skills_df

def plot(skills_df):
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

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

def main():

    st.sidebar.title("zoomJD - Automate the hunt for a right fit job")
    
    with st.sidebar:


        st.write("Welcome to the zoomJD app! \
                This tool helps you scrap data from \
                current job listings at www.seek.com.au \
                and visualise the most in demand skills for \
                the role of your choice.")
    
        st.markdown("---")
    
        st.write("To get started, enter the desired role, select \
                the page count and upload your resume (optional) in pdf format, then click 'Click to evaluate'. \
                Selecting a higher page count would take more time to \
                extract live job postings but would also extract more jobs!")

        st.markdown("---")
        
        st.write("The app is open source and is in WIP mode with more features being tested. Connect with me to discuss or provide feedback! https://www.linkedin.com/in/arnab-biswas-b6b064132/")


        st.write(" ")

    st.title("zoomJD")

    # Initialize session_state variables
    if 'confirmation_button' not in st.session_state:
        st.session_state.confirmation_button = False
        st.session_state.input_role = ""
        st.session_state.input_page_limit = ""

    # User inputs
    input_role = st.text_input("Enter role")
    input_page_limit = st.selectbox('Number of pages to be scrapped', ('1', '2', '5', '10', '20', 'all pages'))
    
    uploaded_file=st.file_uploader("Upload your resume in PDF format",type="pdf",help="Please uplaod the pdf")

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
                return_jobs = web_scrap_jobs(scrapped_data,text_page_num,input_page_limit,input_role)
                jobs = return_jobs[0]
                jd_list = return_jobs[1]
            
            st.markdown("---")

            if len(jd_list)>0:
                jobs_df = pd.DataFrame(jobs)
                header_df = pd.json_normalize(jobs_df['header'])
                jobs_df = pd.concat([jobs_df['url'], header_df], axis=1)

                with st.spinner("Visualising top skills from scanned job descriptions..."):

                    try:
                        extracted_skills = extract_skills_from_scapped(jd_list)
                        plot(extracted_skills[2])
                        jobs_df['extracted_skills'] = extracted_skills[0]

                    except Exception as e:
                        print(e)
                        st.error('No skills to extract, please retry with a different role')

                if uploaded_file is not None:

                    try:
                        cv_details=input_pdf_text(uploaded_file)
                        personal_skills = extract_skills_from_scapped([cv_details])[0][0]
                        jobs_df['matched_skills'] = jobs_df['extracted_skills'].apply(lambda x: list(set(x) & set(personal_skills)))
                        jobs_df['unmatched_skills'] = jobs_df['extracted_skills'].apply(lambda x: list(set(x) - set(personal_skills)))

                    except Exception as e:
                        print(e)
                        st.error('No skills to extract, please retry with a different role')

                
                st.download_button(
                    label='Download job details :anchor:',
                    data=jobs_df.to_csv(index=False, encoding='utf-8', errors='replace'),
                    file_name='jobs_details.csv',
                    mime='text/csv')
                
                try:
                    skill_freq = pd.DataFrame(list(extracted_skills[1].items()), columns=['Skill', 'Value'])
                    st.download_button(
                        label='Download skill frequency :anchor:',
                        data=skill_freq.to_csv(index=False, encoding='utf-8', errors='replace'),
                        file_name='skill_frequency.csv',
                        mime='text/csv')                    

                except Exception as e:
                    print(e)


            
# Run the app
if __name__ == "__main__":
    main()
