import streamlit as st
import os
from track_results.results_parser import ResultsParser

st.title("Track Meet Results Parser")

st.write("Upload one or more meet result PDFs and filter by team name.")

uploaded_files = st.file_uploader("Choose PDF files", type=["pdf"], accept_multiple_files=True)
team_name = st.text_input("Team name to filter results", "")

if uploaded_files and team_name:
    all_results = []
    for uploaded_file in uploaded_files:
        # Save uploaded file to a temp location
        temp_path = os.path.join("/tmp", uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())
        parser = ResultsParser(temp_path)
        results = parser.parse_results()
        all_results.extend(results)
        os.remove(temp_path)
    # Filter by team
    team_results = [r for r in all_results if team_name.lower() in r.team.lower()]
    award_results = [r for r in team_results if hasattr(r, 'needs_award') and r.needs_award()]
    st.subheader(f"All Results for '{team_name}' ({len(team_results)})")
    for r in team_results:
        st.write(str(r))
    st.subheader(f"Award Results for '{team_name}' ({len(award_results)})")
    for r in award_results:
        st.write(str(r))
    # Download buttons
    if team_results:
        all_text = "\n".join(str(r) for r in team_results)
        st.download_button("Download All Results", all_text, file_name=f"{team_name}_all_results.txt")
    if award_results:
        award_text = "\n".join(str(r) for r in award_results)
        st.download_button("Download Award Results", award_text, file_name=f"{team_name}_award_results.txt")
else:
    st.info("Please upload PDF files and enter a team name.")
