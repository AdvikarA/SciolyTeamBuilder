import streamlit as st
import pandas as pd

def main():
    st.title("SciOly Team Builder")

    # Input section
    st.sidebar.header("Input People and Events")
    people_data = input_people_data()

    # Team A and Team B tables
    team_a_table, team_b_table = initialize_tables()

    # Team counters
    team_a_counter, team_b_counter = initialize_counters()

    # Display tables
    st.header("Team A")
    st.table(team_a_table)

    st.header("Team B")
    st.table(team_b_table)

    # Display counters
    st.sidebar.header("Team Counters")
    st.sidebar.text(f"Team A: {team_a_counter}/15")
    st.sidebar.text(f"Team B: {team_b_counter}/15")

    # Drag and Drop
    dragged_person = st.sidebar.selectbox("Drag a person to a team:", [""] + list(people_data.keys()))
    target_team = st.sidebar.selectbox("Select Team:", ["", "Team A", "Team B"])

    if st.sidebar.button("Assign to Team"):
        if dragged_person and target_team:
            assign_to_team(dragged_person, target_team, team_a_table, team_b_table, team_a_counter, team_b_counter, people_data)

def input_people_data():
    st.sidebar.subheader("Add People and Events")

    people_data = {}

    while True:
        person_name = st.sidebar.text_input("Person Name:")
        if not person_name:
            break

        events = st.sidebar.text_input("Events (comma-separated):").split(",")
        people_data[person_name] = [event.strip() for event in events]

    return people_data

def initialize_tables():
    team_a_table = pd.DataFrame(index=range(24), columns=["Slot 1", "Slot 2"])
    team_b_table = pd.DataFrame(index=range(24), columns=["Slot 1", "Slot 2"])
    return team_a_table, team_b_table

def initialize_counters():
    return 0, 0

def assign_to_team(person, target_team, team_a_table, team_b_table, team_a_counter, team_b_counter, people_data):
    if target_team == "Team A" and team_a_counter < 15:
        assign_to_table(person, team_a_table, team_a_counter, people_data)
        team_a_counter += 1
    elif target_team == "Team B" and team_b_counter < 15:
        assign_to_table(person, team_b_table, team_b_counter, people_data)
        team_b_counter += 1

def assign_to_table(person, team_table, team_counter, people_data):
    events = people_data[person]

    for i, event in enumerate(events):
        if team_table.iloc[team_counter * 2, i] == "":
            team_table.iloc[team_counter * 2, i] = person
            break
        elif team_table.iloc[team_counter * 2 + 1, i] == "":
            team_table.iloc[team_counter * 2 + 1, i] = person
            break

if __name__ == "__main__":
    main()
