import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .st-emotion-cache-z5fcl4 {
        width: 100%;
        padding: 1rem 1rem;
        min-width: auto;
        max-width: initial;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Student Assignment Evaluation")

# Column name of the assignment or response data file 
assignid = "Roll No"

# Column name of student detail file
studid = "ID"
studname = "NAME"

def mainlogic(detail, assignments):
    studdetail = pd.read_excel(detail)
    ID = studdetail[f"{studid}"].values.tolist()
    lowercase = [x.lower() for x in ID]
    Name = studdetail[f"{studname}"].values.tolist()

    # Initialize an empty list to store assignment dataframes
    assignment_dfs = []

    # Read and process each assignment file
    for assignment in assignments:
        if assignment.name.endswith('.csv'):
            assignment_df = pd.read_csv(io.BytesIO(assignment.read()), encoding='latin1')
        elif assignment.name.endswith(('.xls', '.xlsx')):
            assignment_df = pd.read_excel(io.BytesIO(assignment.read()))
        else:
            st.toast(f"Unsupported file format for {assignment.name}")
            return

        assignment_dfs.append(assignment_df)

    # Initialize the report header and data
    reportheader = ["ID", "NAME"] + [f"ASSIGNMENT{i+1}" for i in range(len(assignments))]
    report = []

    for i in range(len(lowercase)):
        demo = [ID[i], Name[i]]
        
        for assignment_df in assignment_dfs:
            if lowercase[i] in assignment_df[f"{assignid}"].str.lower().values:
                demo.append('Yes')
            else:
                demo.append('No')

        report.append(demo)

    report = pd.DataFrame(report, columns=reportheader)
    st.dataframe(report, height=400, width=1200)

detail = st.file_uploader("Enter Student Detail File", type=["xlsx", "xls"])

assignments = st.file_uploader("Enter Assignment Files", type=["xlsx", "xls", "csv"], accept_multiple_files=True)

submit = st.button("Submit")

if submit:
    if detail and assignments:
        mainlogic(detail, assignments)
    else:
        st.toast("Please upload files in both fields!",icon="⚠️")
