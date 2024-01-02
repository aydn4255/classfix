
def app():
    import streamlit as st
    import random
    import string
    import json
    import uuid

    # File to store user and class data
    DATA_FILE = "user_class_data.json"

    # Load user and class data from file
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"users": {}, "classrooms": {}}

    # Function to generate a random code
    def generate_random_code():
        code_length = 6
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(code_length))

# Function to save user and class data to file
    def save_data():
        with open(DATA_FILE, "w") as file:
            json.dump(data, file)

    def render_home_page():
        st.title("Classroom Home Page")

        user_id = st.session_state.user_id

        if user_id:
            user_data = data["users"].get(user_id, {})
            user_classrooms = user_data.get("joined_classes", [])
            if not user_classrooms:
                st.warning("You haven't joined any classrooms yet.")
            else:
                st.write("Your Classrooms:")
                for classroom_code in user_classrooms:
                    classroom_data = data["classrooms"].get(classroom_code, {})
                    st.write(f"Classroom Code: {classroom_code}")
                    st.write(f"Subject: {classroom_data.get('subject', 'Unknown')}")
                    if st.button(f"Go to {classroom_data['subject']}", key=f"go_to_{classroom_code}"):
                        render_classroom_page(classroom_code)

        # Creating new classroom
            new_classroom_name = st.text_input("Enter the name of the new classroom:")
            if st.button("Create Classroom") and new_classroom_name:
                code = generate_random_code()
                data["classrooms"][code] = {"id": len(data["classrooms"]) + 1, "subject": new_classroom_name, "posts": [], "owner": user_id}
                data["users"][user_id].setdefault("created_classes", []).append(code)
                st.success(f"Classroom '{new_classroom_name}' created successfully!")
                save_data()
        else:
            st.warning("You need to log in to view your classrooms.")

# Function for a specific classroom page
    def render_classroom_page(classroom_code):
        classroom_data = data["classrooms"].get(classroom_code, None)
        if classroom_data is not None:
            st.title(classroom_data["subject"])

        # Display posts for the classroom
            st.subheader("Classroom Posts")
            for post in classroom_data["posts"]:
                st.write(post)

        # Message box
            new_post = st.text_area("Post your message:")
            if st.button("Post"):
                classroom_data["posts"].append(new_post)
                st.success("Message posted successfully!")
                save_data()

# Function for user authentication and setup
    def authenticate_user():
        if "user_id" not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())
            data["users"][st.session_state.user_id] = {"created_classes": [], "joined_classes": []}
            save_data()

# Main application logic
    def main():
        authenticate_user()

        page = st.sidebar.selectbox("Select a page", ["Home"] + list(data["classrooms"].keys()))

        if page == "Home":
            render_home_page()
        elif page in data["classrooms"]:
            render_classroom_page(page)


    main()

