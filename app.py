import streamlit as st
import pandas as pd

EVENTS = ["Air trajectory", "ANP", "Astro", "Chem Lab", "Codes", "Detector", "Disease", "DP", "Ecology",
          "Expdes", "Fermi", "Flight", "4n6", "Forestry", "Fossils", "Geomapping", "Microbe", "Robot Tour",
          "Scrambler", "Tower", "Wind Power", "WiDi", "Optics"]

def main():
    global team_a_counter, team_b_counter

    st.title("SciOly Team Builder")

    # Input section
    st.sidebar.header("Input People and Events")
    people_data = input_people_data()

    # Initialize tables if not already in session state
    if 'team_a_table' not in st.session_state:
        st.session_state.team_a_table, st.session_state.team_b_table = initialize_tables()

    # Team counters
    team_a_counter, team_b_counter = initialize_counters()

    # Display tables
    st.header("Team A")
    st.table(st.session_state.team_a_table)

    st.header("Team B")
    st.table(st.session_state.team_b_table)

    # Display counters
    st.sidebar.header("Team Counters")
    st.sidebar.text(f"Team A: {team_a_counter}/15")
    st.sidebar.text(f"Team B: {team_b_counter}/15")

    # Drag and Drop
    dragged_person = st.sidebar.selectbox("Drag a person to a team:", [""] + list(people_data.keys()))
    target_team = st.sidebar.selectbox("Select Team:", ["", "Team A", "Team B"])
    selected_events = st.sidebar.multiselect("Select Events:", [""] + EVENTS)

    if st.sidebar.button("Assign to Team"):
        if dragged_person and target_team and selected_events:
            assign_to_team(dragged_person, target_team, selected_events, people_data)

def input_people_data():
    st.sidebar.subheader("Add People and Events")

    people_data = {}
    person_counter = 0

    while True:
        person_counter += 1
        person_name = st.sidebar.text_input(f"Person {person_counter} Name:")
        if not person_name:
            break

        events = st.sidebar.multiselect(f"Events for {person_name}:", EVENTS)
        people_data[person_name] = events

    return people_data

def initialize_tables():
    team_a_table = pd.DataFrame(index=EVENTS, columns=["Spot 1", "Spot 2"])
    team_b_table = pd.DataFrame(index=EVENTS, columns=["Spot 1", "Spot 2"])
    return team_a_table, team_b_table

def initialize_counters():
    return 0, 0

def assign_to_table(person, selected_event, people_data):
    target_team_table = st.session_state.team_a_table if target_team == "Team A" else st.session_state.team_b_table

    for spot in ["Spot 1", "Spot 2"]:
        if pd.isna(target_team_table.loc[selected_event, spot]):
            target_team_table.loc[selected_event, spot] = person
            st.sidebar.success(f"{person} assigned to {selected_event} in {spot} for the team.")
            
            # Update the table in the session state
            if target_team == "Team A":
                st.session_state.team_a_table = target_team_table
            else:
                st.session_state.team_b_table = target_team_table
            
            return
    st.sidebar.error(f"No available slots for {person} in {selected_event}.")
def assign_to_team(person, target_team, selected_events, people_data):
    if target_team == "Team A" and team_a_counter < 15:
        for eventss in selected_events:      
            assign_to_table(person, eventss, people_data)
        team_a_counter += 1
    elif target_team == "Team B" and team_b_counter < 15:
        for eventss in selected_events:      
            assign_to_table(person, eventss, people_data)
        team_b_counter += 1


if __name__ == "__main__":
    main()
