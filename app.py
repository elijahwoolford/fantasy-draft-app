import streamlit as st
import random
import time

def assign_numbers(teams):
    total_numbers = 10000
    assigned_numbers = {}

    # Ensuring equal distribution of total numbers
    remaining_numbers = list(range(total_numbers))

    for team, odds in teams.items():
        num_numbers = int(total_numbers * (odds / 100))
        assigned = random.sample(remaining_numbers, num_numbers)
        assigned_numbers[team] = assigned

        # Remove the assigned numbers from the remaining pool
        remaining_numbers = [num for num in remaining_numbers if num not in assigned]

    return assigned_numbers

def display_countdown(duration):
    placeholder = st.empty()
    for remaining in range(duration, 0, -1):
        placeholder.markdown(f"# {remaining} seconds")
        time.sleep(1)
    placeholder.empty()  # Clear the countdown message when done


def lottery_draw(assigned_numbers):
    draft_order = []
    all_numbers = sum(assigned_numbers.values(), [])
    drawn_numbers = []

    while len(draft_order) < len(assigned_numbers):
        drawn_number = random.choice(all_numbers)
        drawn_numbers.append(drawn_number)

        for team, numbers in assigned_numbers.items():
            if drawn_number in numbers:
                if team not in draft_order:  # Ensure each team is only added once
                    draft_order.append(team)
                # Once a team is selected, remove all its numbers
                all_numbers = [num for num in all_numbers if num not in numbers]
                break  # Move to next draw

    return drawn_numbers, draft_order


def main():
    background_image = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-image: url("https://img.freepik.com/free-vector/realistic-american-football-stadium_52683-54053.jpg?size=626&ext=jpg&ga=GA1.1.556143960.1713460190&semt=ais");
        background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
        background-position: center;  
        background-repeat: no-repeat;
    }
    </style>
    """

    st.markdown(background_image, unsafe_allow_html=True)

    # Header with an image next to the title
    header_col1, header_col2 = st.columns([1, 8])  # Adjust proportions as needed
    
    with header_col1:
        st.image("./sleeper.jpeg", width=50)  # Adjust the width to fit your design
    
    with header_col2:
        st.title("Fantasy Football Draft Lottery")
    
    st.markdown("---")  # Adds a horizontal line for visual separation

    # Main content area for team inputs and lottery logic
    teams = {}
    total_odds = 0

    for i in range(1, 5):  # Assuming input for 4 teams
        col1, col2 = st.columns([1, 2])
        with col1:
            team_name = st.text_input(f"Team {i} Name", key=f"name_{i}")
        with col2:
            odds = st.number_input(f"Team {i} Odds (%)", min_value=0, max_value=100, step=1, key=f"odds_{i}")

        if team_name and odds:  # Validate inputs are not empty
            teams[team_name] = odds
            total_odds += odds

    if st.button("Draw Lottery"):
        if len(teams) == 4 and total_odds == 100:
            display_countdown(10)

            assigned_numbers = assign_numbers(teams)
            drawn_numbers, draft_order = lottery_draw(assigned_numbers)

            # Reverse the draft order for dramatic display
            draft_order.reverse()

            # Placeholder for draft order reveal
            placeholder = st.empty()

            # Initially, create an empty list to hold the draft order text
            draft_order_text = []

            # Reveal each team with a dramatic pause
            for i, team in enumerate(draft_order):
                pick_num = len(draft_order) - i
                color = "#FFFFFF"  # White color
                font_size = "48px"  # Larger font size
                bold_text = "font-weight: bold;"  # Make text bold
                # Add the new pick at the beginning of the list
                draft_order_text.insert(0, f"<span style='color: {color}; font-size: {font_size}; {bold_text}'>Pick #{pick_num}: {team}</span>")
                # Update the placeholder with the new list, joined by newlines for clear separation
                placeholder.markdown("<br>".join(draft_order_text), unsafe_allow_html=True)
                time.sleep(2)

        else:
            st.error("Please ensure four teams are entered and total odds equal 100.")


if __name__ == "__main__":
    main()