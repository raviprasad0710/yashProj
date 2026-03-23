# import streamlit as st

# # Initialize the view state if it doesn't exist
# if "auth_mode" not in st.session_state:
#     st.session_state.auth_mode = "login"

# @st.dialog("Authentication")
# def auth_dialog(): 
#     if st.session_state.auth_mode == "login":
#         st.subheader("Login")
#         st.text_input("Username", key="login_user")
#         st.text_input("Password", type="password", key="login_pass")
        
#         if st.button("Log In", use_container_width=True):
#             # Add your database validation logic here
#             st.success("Logged in!")
#             st.rerun()  # Closes dialog and reruns the full app
            
#         st.markdown("---")
#         if st.button("Don't have an account? Sign Up"):
#             st.session_state.auth_mode = "signup"
#             st.rerun(scope="fragment") # Reruns only the dialog to switch views

#     else:
#         st.subheader("Create Account")
#         st.text_input("Username", key="signup_user")
#         st.text_input("Email", key="signup_email")
#         st.text_input("Password", type="password", key="signup_pass")
        
#         if st.button("Sign Up", use_container_width=True):
#             # Add your database insertion logic here
#             st.success("Account created! Please log in.")
#             st.session_state.auth_mode = "login"
#             st.rerun(scope="fragment")
            
#         st.markdown("---")
#         if st.button("Already have an account? Log In"):
#             st.session_state.auth_mode = "login"
#             st.rerun(scope="fragment")

# # Main App UI
# if st.button("Open Login/Signup"):
#     auth_dialog()


# import streamlit as st

# # 1. Setup & Initial State
# ROWS, COLS = 5, 8
# BOOKED_SEATS = ["A3", "B5", "C1"]

# if "selected" not in st.session_state:
#     st.session_state.selected = set()

# def toggle_seat(seat_id):
#     if seat_id in st.session_state.selected:
#         st.session_state.selected.remove(seat_id)
#     else:
#         st.session_state.selected.add(seat_id)

# st.title("🎬 Movie Seat Selection")

# # 2. THE LEGEND SECTION
# st.write("### Legend")
# l1, l2, l3, _ = st.columns([1, 1, 1, 5]) # _ is a spacer to keep legend items left
# with l1:
#     st.button("💺", key="L1", help="Available", use_container_width=True)
#     st.caption("Available")
# with l2:
#     st.button("💺", key="L2", type="primary", help="Selected", use_container_width=True)
#     st.caption("Selected")
# with l3:
#     st.button("✖️", key="L3", disabled=True, help="Booked", use_container_width=True)
#     st.caption("Booked")

# st.divider()
# st.markdown("<h4 style='text-align: center; border-bottom: 3px solid #555;'>SCREEN</h4>", unsafe_allow_html=True)

# # 3. SEAT GRID
# for r in range(ROWS):
#     row_char = chr(65 + r)
#     cols = st.columns(COLS)
#     for c in range(COLS):
#         seat_id = f"{row_char}{c+1}"
#         with cols[c]:
#             if seat_id in BOOKED_SEATS:
#                 st.button("✖️", key=seat_id, disabled=True)
#             else:
#                 is_active = seat_id in st.session_state.selected
#                 st.button(
#                     label=seat_id,
#                     key=seat_id,
#                     # Uses "primary" for selected, "secondary" (default) for available
#                     type="primary" if is_active else "secondary",
#                     on_click=toggle_seat,
#                     args=(seat_id,),
#                     use_container_width=True
#                 )

# # 4. SUMMARY
# st.divider()
# selection_list = sorted(list(st.session_state.selected))
# st.write(f"**Selected:** {', '.join(selection_list) if selection_list else 'None'}")
# st.write(f"**Total:** ${len(selection_list) * 12}")

# import streamlit as st

# if st.button("cick me"):
#     if st.sidebar.button("Go to Admin Page"):
#         st.switch_page("pages/admin.py")
#         st.rerun()
#     def home():
#         st.write("Home Page")

#     def settings():
#         st.write("Settings Page")

#     # Define pages
#     pg = st.navigation([
#         st.Page(home, title="Home", icon="🏠"),
#         st.Page(settings, title="Settings", icon="⚙️")
#     ])

#     # Run the selected page
#     pg.run()
# elif st.button("hide me"):
#     pass

# # Use the sidebar to create a navigation switch
# with st.sidebar:
#     selection = st.radio("Go to", ["Home", "Data Analysis", "Settings"])

# # Main area content changes based on the sidebar selection
# if selection == "Home":
#     st.title("Welcome Home")
# elif selection == "Data Analysis":
#     st.title("Analyze Your Data")
# elif selection == "Settings":
#     st.title("App Settings")

# import streamlit as st

# # Some condition (e.g., a toggle or a validation)
# can_execute = False 

# # The button is "active" visually, but clicking does nothing
# if st.button("Click Me") and can_execute:
#     st.success("Action Performed!")
# else:
#     if st.session_state.get('clicked_button'): # Optional feedback
#         st.warning("Button clicked, but action is blocked.")

# import streamlit as st
# from datetime import datetime

# # Datetime Picker
# event_time = st.datetime_input("Schedule your event", datetime(2026, 2, 26, 12, 0))
# st.write("Event scheduled for:", event_time)

# import streamlit as st
# import datetime

# # Time Picker
# meeting_time = st.time_input("Meeting time", datetime.time(8, 45))
# st.write("Meeting scheduled for:", meeting_time)


# import streamlit as st
# import datetime

# # Basic Date Picker
# birthday = st.date_input("When's your birthday", datetime.date(2000, 1, 1))
# st.write("Your birthday is:", birthday)

# # Date Range Picker
# start_date = st.date_input("Select vacation range", (datetime.date(2026, 1, 1), datetime.date(2026, 1, 7)))

# import streamlit as st
# import datetime

# # Function to define the dialog content
# @st.dialog("Schedule Event", dismissible=True)
# def schedule_event_dialog():
#     st.write("Enter the date and time for your event:")
    
#     # Use st.datetime_input for combined date and time
#     event_datetime = st.datetime_input("Select date and time", value="now")

#     # Use session state to store the result
#     if st.button("Submit"):
#         st.session_state["event_datetime"] = event_datetime
#         st.rerun() # Rerun the main app to close the dialog and update the value

# # Main app logic
# if "event_datetime" not in st.session_state:
#     st.session_state["event_datetime"] = None

# st.title("Event Scheduler")
# # Button to open the dialog
# if st.button("Open Scheduling Dialog"):
#     schedule_event_dialog()

# # Display the selected date and time
# if st.session_state["event_datetime"]:
#     st.success(f"Event scheduled for: {st.session_state['event_datetime']}")
# else:
#     st.info("No event scheduled yet.")


# import streamlit as st
# import datetime

# with st.popover("Select date and time"):
#     st.markdown("Choose your desired time") 
#     # You can use st.date_input and st.time_input separately within the popover
#     selected_date = st.date_input("Date", datetime.date.today())
#     selected_time = st.time_input("Time", datetime.datetime.now().time())
    
#     # Store the results in session state for use outside the popover
#     st.session_state["selected_date"] = selected_date
#     st.session_state["selected_time"] = selected_time

# # Display the selected date and time in the main app
# if "selected_date" in st.session_state and "selected_time" in st.session_state:
#     st.write("Selected date:", st.session_state["selected_date"])
#     st.write("Selected time:", st.session_state["selected_time"])

# import streamlit as st
# # import datetime
# from datetime import datetime, timedelta

# # Get the current date and time
# current_datetime = datetime.now()

# st.write("### Current Date and Time")
# # Display the full datetime object
# st.write(current_datetime)

# st.write("### Formatted Date and Time")
# # Display the date and time in a specific format (e.g., DD/MM/YYYY HH:MM:SS)
# formatted_datetime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
# st.write(formatted_datetime)
# min_date = datetime.now() 
# st.write(min_date)

# st.write("Choose time:")
# start = st.datetime_input("Start",value=min_date)
# format_start=start.strftime("%Y-%m-%d %H:%M:%S")
# end = st.datetime_input("End", datetime(2026, 2, 26, 12, 0))
# format_end=end.strftime("%Y-%m-%d %H:%M:%S")
# st.write("Seat booked from:", format_start)
# st.write("Seat booked to:", format_end)

# import streamlit as st
# from datetime import datetime, timedelta

# # 1. Setup initial boundaries
# min_date = datetime.now()
# max_date_limit = min_date + timedelta(days=60)

# st.write("### Choose time range:")

# # 2. Start Date Input
# # We use min_date as the default value to match the min_value
# start = st.datetime_input(
#     "Start", 
#     value=min_date,
#     min_value=min_date, 
#     max_value=max_date_limit
# )

# 3. End Date Input 
# IMPORTANT: The min_value for 'End' is now the 'start' variable itself
# # This prevents the user from picking an end date before the start date
# end = st.datetime_input(
#     "End", 
#     value=start + timedelta(hours=1), # Default to 1 hour after start
#     min_value=start, 
#     max_value=max_date_limit
# )

# # 4. Formatting for display or database
# format_start = start.strftime("%Y-%m-%d %H:%M:%S")
# format_end = end.strftime("%Y-%m-%d %H:%M:%S")

# # Display the selection
# st.info(f"**Selected Range:** {format_start} **to** {format_end}")

# import streamlit as st
# import pandas as pd
# from datetime import datetime

# # Configure page settings
# st.set_page_config(
#     page_title="SeatMaster - Seating Management",
#     page_icon="💺",
#     layout="wide"
# )

# # Sidebar Navigation
# with st.sidebar:
#     st.title("💺 SeatMaster")
#     st.markdown("---")
#     page = st.radio("Navigation", ["Dashboard", "Book a Seat", "Floor Map", "Admin Panel"])
#     st.info("System Status: Online")


# if page == "Dashboard":
#     st.title("Occupancy Dashboard")
    
#     # Header Metrics
#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("Total Seats", "250")
#     col2.metric("Available", "112", delta="12%")
#     col3.metric("Reserved", "138", delta="-5%")
#     col4.metric("Maintenance", "5", delta_color="inverse")

#     st.markdown("---")

#     # Layout for Charts and Quick Actions
#     left_col, right_col = st.columns([2, 1])

#     with left_col:
#         st.subheader("Daily Occupancy Trend")
#         # Example data for a trend chart
#         chart_data = pd.DataFrame({
#             "Time": ["08:00", "10:00", "12:00", "14:00", "16:00"],
#             "Occupancy": [20, 85, 120, 138, 90]
#         })
#         st.area_chart(chart_data.set_index("Time"))

#     with right_col:
#         st.subheader("Quick Actions")
#         if st.button("🚀 Rapid Booking", use_container_width=True):
#             st.toast("Redirecting to booking page...")
        
#         with st.expander("Recent Activity"):
#             st.write("✅ Seat A-12 reserved by John D.")
#             st.write("⚠️ Seat C-04 marked for cleaning")
#             st.write("✅ Seat B-21 released")

# # Simple 5x5 seating grid preview
# st.subheader("Floor Preview (Zone A)")
# for row in ["A", "B", "C", "D", "E"]:
#     cols = st.columns(5)
#     for i, col in enumerate(cols):
#         seat_id = f"{row}{i+1}"
#         col.button(seat_id, key=seat_id, use_container_width=True)



# import streamlit as st

# def show_floor_map():
#     st.subheader("📍 Interactive Floor Map - Zone A")
    
#     # Legend
#     col_l1, col_l2, col_l3 = st.columns(3)
#     col_l1.markdown("🟦 **Available**")
#     col_l2.markdown("🟥 **Occupied**")
#     col_l3.markdown("🟧 **Selected**")
#     st.write("")

#     # Mock Data: Occupied seats
#     occupied_seats = ["A3", "B1", "B2", "D4", "E5"]
    
#     # Define Rows and Columns for the grid
#     rows = ["A", "B", "C", "D", "E"]
#     cols_per_row = 6

#     # Create the Grid
#     for row_label in rows:
#         cols = st.columns(cols_per_row)
#         for i in range(cols_per_row):
#             seat_id = f"{row_label}{i+1}"
            
#             # Check status and style accordingly
#             if seat_id in occupied_seats:
#                 # Occupied Seat (Disabled)
#                 cols[i].button(seat_id, key=seat_id, disabled=True, type="secondary", use_container_width=True)
#             else:
#                 # Available Seat
#                 if cols[i].button(seat_id, key=seat_id, type="primary", use_container_width=True):
#                     st.session_state['selected_seat'] = seat_id
#                     st.toast(f"Seat {seat_id} selected!")

#     # Selection Summary
#     if 'selected_seat' in st.session_state:
#         st.success(f"Selected Seat: **{st.session_state['selected_seat']}**")
#         if st.button("Confirm Booking"):
#             st.balloons()
#             st.success("Booking Confirmed!")

# # Call the function in your main app logic
# show_floor_map()
######################################################################################3

# import streamlit as st

# def show_dept_map():
#     st.title("🏢 Department Floor Plan")
    
#     # 1. Department Tabs
#     tab_it, tab_hr, tab_finance = st.tabs(["💻 IT Department", "👥 HR & Admin", "💰 Finance"])

#     # Mock data for booked seats
#     booked_seats = ["IT-02", "HR-05", "FIN-01"]

#     # Function to build a grid for a department
#     def create_seat_grid(dept_code, rows, cols, color_type):
#         st.write(f"### {dept_code} Seating Zone")
        
#         # UI Legend
#         st.caption(f"Status: {color_type.capitalize()} coded zone")
        
#         for r in range(rows):
#             columns = st.columns(cols)
#             for c in range(cols):
#                 seat_id = f"{dept_code}-{r}{c+1}"
#                 is_booked = seat_id in booked_seats
                
#                 # Button label with Icon
#                 label = f"💺 {seat_id}"
                
#                 if columns[c].button(
#                     label, 
#                     key=seat_id, 
#                     disabled=is_booked,
#                     use_container_width=True,
#                     type="primary" if not is_booked else "secondary"
#                 ):
#                     st.session_state['selected_seat'] = seat_id
#                     st.toast(f"Selected {seat_id}")

#     # 2. Populate Tabs with specific grid sizes
#     with tab_it:
#         create_seat_grid("IT", rows=4, cols=5, color_type="Blue")
        
#     with tab_hr:
#         create_seat_grid("HR", rows=3, cols=4, color_type="Green")
        
#     with tab_finance:
#         create_seat_grid("FIN", rows=3, cols=3, color_type="Yellow")

#     # 3. Booking Sidebar/Footer
#     if 'selected_seat' in st.session_state:
#         with st.expander("📝 Confirm Selection", expanded=True):
#             st.write(f"You have selected: **{st.session_state['selected_seat']}**")
#             dept = st.session_state['selected_seat'].split("-")[0]
#             st.info(f"Note: This seat is located in the **{dept}** wing.")
            
#             if st.button("Confirm Reservation", use_container_width=True):
#                 st.success(f"Seat {st.session_state['selected_seat']} reserved successfully!")
#                 st.balloons()

# show_dept_map()


# import streamlit as st
# import plotly.express as px
# from PIL import Image

# # 1. Load the blueprint
# uploaded_file = st.file_uploader("Choose an image...")
# if uploaded_file is not None:
#     image = Image.open(uploaded_file)
#     st.image(image, caption='Uploaded Image')
#     # img = Image.open("office_layout.png")
#     width, height = image.size 

# # 2. Define seat data (x, y are pixel locations)
# seats = [
#     {"seat": "A1", "x": 100, "y": 200, "status": "Available"},
#     {"seat": "A2", "x": 150, "y": 300, "status": "Occupied"}
# ]

# # 3. Create the interactive plot
# fig = px.scatter(seats, x="x", y="y", hover_name="seat", color="status") 
# fig.update_layout(
#     images=[dict(source=image, xref="x", yref="y", x=0, y=height, sizex=width, sizey=height, layer="below")],
#     xaxis=dict(showgrid=False, range=[0, width]),
#     yaxis=dict(showgrid=False, range=[0, height])
# )

# st.plotly_chart(fig)



#################################################################################################

# import streamlit as st
# import pandas as pd

# # 1. Page Configuration
# st.set_page_config(page_title="My Account | SeatManager", layout="wide")

# # 2. Mock Data Initialization (In a real app, fetch from a database)
# if 'user' not in st.session_state:
#     st.session_state.user = {
#         "name": "Alex Rivera",
#         "id": "EMP-8842",
#         "dept": "Engineering",
#         "email": "alex.r@company.com"
#     }

# # 3. Sidebar Navigation
# st.sidebar.title("SeatManager")
# st.sidebar.button("Book a New Seat")
# st.sidebar.button("Logout", type="primary")

# # 4. Profile Header Section
# col1, col2 = st.columns([1, 4])
# with col1:
#     st.image("https://cdn-icons-png.flaticon.com", width=120)
# with col2:
#     st.title(f"Welcome, {st.session_state.user['name']}")
#     st.caption(f"{st.session_state.user['dept']} | ID: {st.session_state.user['id']}")

# st.divider()

# # 5. Booking Statistics (KPI Cards)
# stat1, stat2, stat3 = st.columns(3)
# stat1.metric("Active Bookings", "3", delta="1 new")
# stat2.metric("Favorite Zone", "Quiet Zone B")
# stat3.metric("Monthly Usage", "85%", delta="5%")

# # 6. Content Tabs
# tab1, tab2, tab3 = st.tabs(["📅 Upcoming Reservations", "📜 History", "⚙️ Settings"])

# with tab1:
#     st.subheader("Your Scheduled Seats")
#     # Mock dataframe for display
#     bookings = pd.DataFrame({
#         "Date": ["2024-03-01", "2024-03-03", "2024-03-05"],
#         "Seat ID": ["A-102", "B-204", "A-105"],
#         "Building": ["Main HQ", "East Wing", "Main HQ"],
#         "Status": ["Confirmed", "Confirmed", "Pending"]
#     })
#     st.dataframe(bookings, use_container_width=True)
    
#     if st.button("Cancel Next Booking"):
#         st.warning("Are you sure you want to cancel seat A-102?")

# with tab2:
#     st.write("Displaying past 30 days of seating activity...")
#     st.info("No past records found for this month.")

# with tab3:
#     st.subheader("User Preferences")
#     st.toggle("Receive email reminders 24h before booking", value=True)
#     st.selectbox("Preferred Floor", ["Floor 1", "Floor 2 (Quiet)", "Floor 3"])
#     if st.button("Save Changes"):
#         st.success("Preferences updated!")

# import streamlit as st

# # --- Session State Management ---
# # Initialize session state variables for user settings if they don't exist
# if 'username' not in st.session_state:
#     st.session_state['username'] = 'johndoe' 
# if 'email' not in st.session_state:
#     st.session_state['email'] = 'j.doe@example.com'
# if 'notifications' not in st.session_state:
#     st.session_state['notifications'] = True
# if 'theme' not in st.session_state:
#     st.session_state['theme'] = 'Light'

# def save_settings():
#     """Callback function to handle form submission and update session state."""
#     st.session_state['username'] = st.session_state['input_username']
#     st.session_state['email'] = st.session_state['input_email']
#     st.session_state['notifications'] = st.session_state['input_notifications']
#     st.session_state['theme'] = st.session_state['input_theme']
#     st.success("Settings saved successfully!")

# # --- Account Settings Frontend ---

# st.title("Account Settings")

# st.write("Update your personal information and preferences below.")

# # Use st.form for a cohesive settings section
# with st.form(key='account_settings_form'):
#     st.subheader("Profile Information")
    
#     # Text input for username
#     st.text_input("Username", 
#                   value=st.session_state['username'], 
#                   key='input_username')
    
#     # Text input for email
#     st.text_input("Email Address", 
#                   value=st.session_state['email'], 
#                   key='input_email')
    
#     st.subheader("Preferences")

#     # Checkbox for email notifications
#     st.checkbox("Enable email notifications", 
#                 value=st.session_state['notifications'], 
#                 key='input_notifications')
    
#     # Selectbox for theme preference
#     st.selectbox("Choose Theme", 
#                  ['Light', 'Dark', 'System default'], 
#                  index=['Light', 'Dark', 'System default'].index(st.session_state['theme']),
#                  key='input_theme')

#     # Submit button
#     submit_button = st.form_submit_button(label='Save Changes', on_click=save_settings)

# # Optional: Display current session state for verification (for development)
# st.sidebar.subheader("Current Session State (Dev)")
# st.sidebar.write(st.session_state)


# import streamlit as st
# import time

# st.title("Countdown Timer")

# # Create a placeholder for the timer
# timer_placeholder = st.empty()

# # Define the countdown duration in seconds
# # Example: 2 minutes = 120 seconds
# total_seconds = 120

# if st.button("Start Timer"):
#     for secs in range(total_seconds, -1, -1):
#         # Calculate minutes and seconds
#         mm, ss = divmod(secs, 60)
#         # Format and update the placeholder
#         timer_placeholder.metric("Time Remaining", f"{mm:02d}:{ss:02d}")
#         time.sleep(1)
#     st.write("Time's up!")


# import streamlit as st

# # 1. Initialize session state
# if 'show_button' not in st.session_state:
#     st.session_state.show_button = True

# # 2. Define a callback function to hide the button
# def hide_button_on_click():
#     st.session_state.show_button = False

# st.title("Hide Button Example")

# # 3. Conditionally render the button
# if st.session_state.show_button:
#     st.button("Click to hide me", on_click=hide_button_on_click)
# else:
#     st.write("The button is now hidden.")

# import streamlit as st
# from streamlit_image_coordinates import streamlit_image_coordinates
# from PIL import Image

# # Load your image
# image_path = "C:/Users/Raviraj/Downloads/officespace.jpg"
# img = Image.open(image_path)

# st.title("Click the image to get coordinates")

# # Display the image and capture clicks
# # It returns a dictionary: {"x": value, "y": value} or None if no click yet
# value = streamlit_image_coordinates(img, key="office_click")

# if value is not None:
#     st.write(f"You clicked at: X = {value['x']}, Y = {value['y']}")
    
#     # Optional: Logic to store these points for your Matplotlib overlay
#     if "clicked_points" not in st.session_state:
#         st.session_state.clicked_points = []
    
#     st.session_state.clicked_points.append((value['x'], value['y']))
#     st.write("All points captured:", st.session_state.clicked_points)


# import streamlit as st

# # 1. Background image with container
# st.markdown("""
# <style>
# .bg-container {
#     position: relative;
#     background-image: url('YOUR_IMAGE_URL');
#     background-size: contain;
#     width: 800px; /* Adjust to image width */
#     height: 600px; /* Adjust to image height */
# }
# .stButton {
#     position: absolute;
# }
# </style>
# """, unsafe_allow_html=True)

# # 2. Add content to the container
# st.markdown('<div class="bg-container">', unsafe_allow_html=True) 

# # 3. Position buttons using x (left) and y (top)
# st.markdown('<style>div.stButton:nth-child(1){right: 50px; left: 400px;}</style>', unsafe_allow_html=True)
# if st.button("Button 1"):
#     st.write("Clicked 1")

# st.markdown('<style>div.stButton:nth-child(2){bottom: 300px; left: 100px;}</style>', unsafe_allow_html=True)
# if st.button("Button 2"):
#     st.write("Clicked 2")

# st.markdown('</div>', unsafe_allow_html=True)


# import streamlit as st 

# # Example coordinates: (x=30%, y=50%)
# st.markdown("""
#     <style>
#     .img-container {
#         position: relative;
#         width: 100%;
#         max-width: 600px;
#     }
#     .img-container img {
#         width: 100%;
#         height: auto;
#     }
#     .custom-btn {
#         position: absolute;
#         top: 60%; /* Y-axis */ 
#         left: 30%; /* X-axis */
#         transform: translate(-50%, -50%);
#         padding: 10px 20px;
#         background-color: #ff4b4b;
#         color: white;
#         border: none;
#         border-radius: 5px;
#         cursor: pointer;
#     }
#     </style>
#     <div class="img-container">
#         <img src="https://placeholder.com" alt="Background">
#         <button class="custom-btn" onclick="alert('Clicked!')">Button 1</button>
#     </div> 
# """, unsafe_allow_html=True)



# import streamlit as st
# from PIL import Image
# import numpy as np
# import matplotlib.pyplot as plt

# st.write("Office floor map")
# image_path = "C:/Users/Raviraj/Downloads/officespace.jpg"
# image = Image.open(image_path)
# img_array = np.array(image)

# fig, ax = plt.subplots()
# ax.imshow(img_array)

# x_coords = [45, 109, 103, 78, 142, 167, 31, 62, 97, 132, 171, 206, 45, 117, 189,
#             503, 581, 505, 582, 634, 668, 630, 630, 584, 505, 544, 580, 632, 706, 704, 708, 706]

# y_coords = [278, 224, 337, 308, 252, 278, 46, 47, 46, 52, 46, 49, 169, 168, 166,
#             76, 75, 136, 76, 135, 201, 280, 338, 304, 303, 236, 136, 76, 74, 136, 337, 278]

# # 1. Define availability (Example: first 10 are available, rest are reserved)
# # In a real app, this list would come from your database
# availability = [True if i < 10 else False for i in range(len(x_coords))]

# # 2. Map availability to colors
# colors = ['green' if available else 'red' for available in availability]

# # 3. Pass the 'colors' list to the 'c' parameter
# ax.scatter(x_coords, y_coords, c=colors, s=40)

# # Optional: Hide axes for a cleaner look
# ax.axis('off')

# st.pyplot(fig)




# import plotly.graph_objects as go
# import streamlit as st

# # Assuming img_array, x_coords, y_coords, and image are defined
# # Create labels and colors based on your data
# labels = [f"Desk {i+1}" for i in range(len(x_coords))]
# colors = ["green" if i < 10 else "red" for i in range(len(x_coords))]

# fig = go.Figure()

# # 1. Add background image
# fig.add_layout_image(
#     dict(source=image, xref="x", yref="y", x=0, y=0,
#          sizex=img_array.shape[1], sizey=img_array.shape[0],
#          sizing="stretch", opacity=1, layer="below")
# )

# # 2. Add clickable, hovering dots
# fig.add_trace(go.Scatter(
#     x=x_coords, y=y_coords, mode='markers',
#     marker=dict(color=colors, size=12),
#     text=labels, hoverinfo='text'
# ))

# # 3. Configure axes and display
# fig.update_xaxes(showgrid=False, zeroline=False, range=[0, img_array.shape[1]])
# fig.update_yaxes(showgrid=False, zeroline=False, range=[img_array.shape[0], 0], scaleanchor="x")
# fig.update_layout(width=800, height=600, margin=dict(l=0, r=0, t=0, b=0))

# # Add a unique key and set on_select to 'rerun'
# st.plotly_chart(fig)
# event = st.plotly_chart(fig, key="floor_map", on_select="rerun")

# # Check if a point was clicked
# if event and "selection" in event and len(event["selection"]["points"]) > 0:
#     point_index = event["selection"]["points"][0]["point_index"]
#     selected_label = labels[point_index]
#     st.write(f"You clicked on: **{selected_label}**")
    
#     # You can now add logic here, like opening a booking form
#     if st.button(f"Reserve {selected_label}"):
#         st.success(f"{selected_label} has been reserved!")

# import streamlit as st
# rows = ["A", "B", "C", "D"]
# cols = 8 # Adjust based on your layout
# desk_num = 1 # Start the counter

# for r in rows:
#     cols_ui = st.columns(cols) 
#     for c in range(cols):
#         # Stop at 30 if you only want 30 desks
#         if desk_num <= 30:
#             seat_label = f"Desk {desk_num}"
            
#             with cols_ui[c]:
#                 if st.button(seat_label, key=seat_label):
#                     # Your click logic here
#                     st.write(seat_label)
            
#             desk_num += 1 # Increment for the next button

# import streamlit as st
# import streamlit_authenticator as stauth
# import yaml
# from yaml.loader import SafeLoader
# import pymysql

# # 1. Database Connection
# def get_db_connection():
#     return pymysql.connect(
#         host="localhost",
#         user="root",
#         password="root",
#         database="crud",
#         port=3306
#     )

# # 2. Fetch User Data from MySQL
# def fetch_users():
#     conn = get_db_connection()
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     cursor.execute("SELECT username, password FROM users")
#     rows = cursor.fetchall()
#     conn.close()
    
#     # Format for streamlit-authenticator
#     credentials = {"usernames": {}}
#     for row in rows:
#         credentials["usernames"][row['username']] = {
#             "name": row['username'],
#             "password": row['password'] # Must be pre-hashed in DB
#         }
#     return credentials

# # 3. Initialize Authenticator
# credentials = fetch_users()

# # Cookie settings allow persistence on refresh
# authenticator = stauth.Authenticate(
#     credentials,
#     cookie_name='my_auth_cookie',
#     key='signature_key_here', # Random string to sign the cookie
#     cookie_expiry_days=30     # Keep logged in for 30 days
# )

# # 4. Render Login Widget
# # This function checks the cookie first; if valid, it logs the user in automatically
# name, authentication_status, username = authenticator.login(location='main')

# # 5. Handle Logic Based on Status
# if st.session_state["authentication_status"]:
#     # --- LOGGED IN ---
#     st.sidebar.title(f"Welcome {st.session_state['name']}")
#     authenticator.logout('Logout', 'sidebar')
    
#     st.title("Main Dashboard")
#     st.write("This content stays visible even if you refresh the page!")

# elif st.session_state["authentication_status"] is False:
#     st.error('Username/password is incorrect')
# elif st.session_state["authentication_status"] is None:
#     st.warning('Please enter your username and password')


import streamlit as st
from datetime import date, timedelta

# Generate a list of dates (e.g., the next 30 days)
available_dates = [date.today() + timedelta(days=i) for i in range(30)]

selected_dates = st.multiselect(
    "Select dates for seat booking:",
    options=available_dates,
    format_func=lambda x: x.strftime("%A, %d %B %Y")
)

st.write("You selected:", selected_dates)


import streamlit as st

if 'selected_dates' not in st.session_state:
    st.session_state.selected_dates = []

# Use a single date picker as an "adder"
new_date = st.date_input("Pick a date to add to your selection:")

if st.button("Add Date"):
    if new_date not in st.session_state.selected_dates:
        st.session_state.selected_dates.append(new_date)

# Display and allow removal of dates
st.write("### Currently Selected Dates:") 
for d in st.session_state.selected_dates:
    col1, col2 = st.columns([3, 1])
    col1.write(d.strftime("%Y-%m-%d"))
    if col2.button("Remove", key=str(d)):
        st.session_state.selected_dates.remove(d)
        st.rerun()


import streamlit as st
from datetime import date, timedelta 

# 1. Your list of all possible dates (e.g., next 14 days)
all_dates = [date.today() + timedelta(days=i) for i in range(14)]

# 2. Your list of already selected/booked dates (from your database)
booked_dates = [date.today() + timedelta(days=2), date.today() + timedelta(days=5)]

# 3. Filter the options to ONLY show available dates
available_options = [d for d in all_dates if d not in booked_dates]

selected = st.multiselect(
    "Select available dates:",
    options=available_options,
    format_func=lambda x: x.strftime("%A, %b %d")
)

