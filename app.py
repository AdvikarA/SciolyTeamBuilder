import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

EVENTS = ["Air trajectory", "ANP", "Astro", "Chem Lab", "Codes", "Detector", "Disease", "DP", "Ecology",
          "Expdes", "Fermi", "Flight", "4n6", "Forestry", "Fossils", "Geomapping", "Microbe", "Robot Tour",
          "Scrambler", "Tower", "Wind Power", "WiDi", "Optics"]

def main():
    st.title("SciOly Team Builder")

    if 'people_data' not in st.session_state:
        st.session_state.people_data = {}

    if 'team_a_table' not in st.session_state:
        st.session_state.team_a_table = pd.DataFrame(index=EVENTS, columns=["Spot 1", "Spot 2"])

    if 'team_b_table' not in st.session_state:
        st.session_state.team_b_table = pd.DataFrame(index=EVENTS, columns=["Spot 1", "Spot 2"])

    if 'team_a_counter' not in st.session_state:
        st.session_state.team_a_counter = 0

    if 'team_b_counter' not in st.session_state:
        st.session_state.team_b_counter = 0

    # Input section
    st.sidebar.header("Input People and Events")
    input_people_data()

    # Display tables
    st.header("Team A")
    display_table(st.session_state.team_a_table, "Team A")

    st.header("Team B")
    display_table(st.session_state.team_b_table, "Team B")

    # Display counters
    st.sidebar.header("Team Counters")
    st.sidebar.text(f"Team A: {st.session_state.team_a_counter}/15")
    st.sidebar.text(f"Team B: {st.session_state.team_b_counter}/15")

    # Drag and Drop
    dragged_person = st.sidebar.selectbox("Drag a person to a team:", [""] + list(st.session_state.people_data.keys()))
    target_team = st.sidebar.selectbox("Select Team:", ["", "Team A", "Team B"])
    
    if dragged_person:
        selected_events = st.sidebar.multiselect("Select Events:", [""] + st.session_state.people_data[dragged_person])

    if st.sidebar.button("Assign to Team"):
        if dragged_person and target_team and selected_events:
            assign_to_team(dragged_person, target_team, selected_events)

def input_people_data():
    st.sidebar.subheader("Add People and Events")

    person_counter = 0

    while True:
        person_counter += 1
        person_name = st.sidebar.text_input(f"Person {person_counter} Name:")
        if not person_name:
            break

        events = st.sidebar.multiselect(f"Events for {person_name}:", EVENTS)
        st.session_state.people_data[person_name] = events

def assign_to_table(person, selected_event, team_table, team_counter):
    for spot in ["Spot 1", "Spot 2"]:
        if pd.isna(team_table.loc[selected_event, spot]):
            team_table.loc[selected_event, spot] = person
            st.sidebar.success(f"{person} assigned to {selected_event} in {spot} for the team.")
            return
    st.sidebar.error(f"No available slots for {person} in {selected_event}.")

def assign_to_team(person, target_team, selected_events):
    if target_team == "Team A" and st.session_state.team_a_counter < 15:
        for eventss in selected_events:
            assign_to_table(person, eventss, st.session_state.team_a_table, st.session_state.team_a_counter)
        st.session_state.team_a_counter += 1
    elif target_team == "Team B" and st.session_state.team_b_counter < 15:
        for eventss in selected_events:
            assign_to_table(person, eventss, st.session_state.team_b_table, st.session_state.team_b_counter)
        st.session_state.team_b_counter += 1

def display_table(team_table, team_name):
    table_html = generate_table_html(team_table, team_name)
    components.html(table_html, height=400, scrolling=True)

def generate_table_html(team_table, team_name):
    table_style = f"""
        <style>
            table {{
                font-size: 14px;
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 20px;
            }}
            th, td {{
                padding: 10px;
                text-align: center;
                border: 1px solid #dddddd;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    """
    table_html = team_table.to_html(classes='table')
    table_html = table_html.replace('<table border="1" class="dataframe table">', f'<table class="table">{table_style}')
    return f"<h3>{team_name}</h3>{table_html}"

if __name__ == "__main__":
    main()
