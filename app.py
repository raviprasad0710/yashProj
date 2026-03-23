import re
import time
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from PIL import Image
import plotly.graph_objects as go
from datetime import date, timedelta
import json

from Database.db import (
    create_users_table, get_all_users, signup_user, login_user_db, get_booked, get_booked_seats,
    get_booked_dates, book_seat_db, remove_booked_db, deleted_booking_overdue,get_db_connection
)

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None

def login_user(username_or_email, password):
    return login_user_db(username_or_email, password)

def remove_booked(user_id):
    remove_booked_db(user_id)
    st.toast("Removed", icon="❌")
    time.sleep(1)




# def book_seat(user_id,username,seat_id,start_time,end_time):
def book_seat(user_id, username, seat_id, selected_dates):
    success, error = book_seat_db(user_id, username, seat_id, selected_dates)
    if success:
        st.toast(f"Seat {seat_id} booked for {username}!", icon="✅")
        time.sleep(1.3)
    else:
        st.write(error)
        st.error("Seat already taken.")
    st.rerun()




st.title("💺 SeatMaster")
# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None



create_users_table()
deleted_booking_overdue()



if not st.session_state.logged_in:
    # Signup and Login forms
    col1, col2 = st.columns(2)

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"
    
    with col1:
        if st.session_state.auth_mode == "signup":
            st.subheader("Signup")
            with st.form("signup_form"):
                username = st.text_input("Username")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                role = st.selectbox("Role", ["user", "admin"])
                submitted = st.form_submit_button("Signup")
                if submitted:
                    if not username.strip():
                        st.error("Username cannot be empty.")
                    elif len(username.strip()) < 3:
                        st.error("Username must be at least 3 characters.")
                    elif not is_valid_email(email):
                        st.error("Please enter a valid email address (e.g. name@example.com).")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters.")
                    elif password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        if signup_user(username.strip(), email.strip().lower(), password, role):
                            st.success("Account created! Please log in.")
                        else:
                            st.error("Username or email already exists.")
            if st.button("Already a member? Sign in?"):
                st.session_state.auth_mode = "login"
                st.rerun()
    

        if st.session_state.auth_mode == "login":
            st.write("hello")
            st.subheader("Login")
            with st.form("login_form"):
                username_or_email = st.text_input("Username or Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login")
                if submitted:
                    if not username_or_email.strip():
                        st.error("Please enter your username or email.")
                    elif "@" in username_or_email and not is_valid_email(username_or_email):
                        st.error("That doesn't look like a valid email address.")
                    elif len(password) == 0:
                        st.error("Please enter your password.")
                    else:
                        user = login_user(username_or_email.strip(), password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user = user
                            st.success("Logged in successfully!")
                            st.rerun()
                        else:
                            st.error("Invalid credentials. Check your username/email and password.")
            if st.button("Not a member? Sign Up?"):
                st.session_state.auth_mode = "signup"
                st.rerun()
else:

    st.set_page_config(
    page_title="SeatMaster - Seating Management",
    page_icon="💺",
    layout="wide"
    )

    # Sidebar Navigation
    with st.sidebar:
        st.title("💺 SeatMaster")
        # st.write("---")

        # Custom horizontal line with 5px top and bottom margin
        st.markdown('<hr style="margin: 5px 0px;">', unsafe_allow_html=True)

        st.sidebar.header(f"Welcome {st.session_state.user['username']}")



    
    # Role-based authorization
    if st.session_state.user['role'] == 'admin':

        ADMIN_OPTIONS = ["Dashboard", "Users", "Bookings", "Floor Map Editor", "Account"]

        if "admin_nav" in st.session_state and st.session_state["admin_nav"] in ADMIN_OPTIONS:
            st.session_state["admin_radio"] = st.session_state["admin_nav"]
            del st.session_state["admin_nav"]

        with st.sidebar:
            admin_selection = st.radio("Admin Panel", ADMIN_OPTIONS, key="admin_radio")
            st.info("System Status: Online")

        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

        # ── Admin Dashboard ──────────────────────────────────────
        if admin_selection == "Dashboard":
            st.subheader("Admin Dashboard")

            all_bookings = get_booked()
            all_users = get_all_users()
            today = date.today()

            def seat_booked_today(dates_json):
                try:
                    dates_list = json.loads(dates_json) if isinstance(dates_json, str) else (dates_json or [])
                    return today in [date.fromisoformat(d) for d in dates_list]
                except:
                    return False

            total_seats = 32
            occupied_today = [b for b in all_bookings if seat_booked_today(b[3])]

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Users", len(all_users))
            c2.metric("Total Bookings", len(all_bookings))
            c3.metric("Occupied Today", len(occupied_today))
            c4.metric("Available Today", total_seats - len(occupied_today))

            st.markdown("---")
            left, right = st.columns([2, 1])

            with left:
                st.subheader("Seat demand — next 14 days")
                day_counts = []
                for i in range(14):
                    d = today + timedelta(days=i)
                    d_str = d.strftime("%Y-%m-%d")
                    count = sum(
                        1 for b in all_bookings
                        if d_str in (json.loads(b[3]) if isinstance(b[3], str) else (b[3] or []))
                    )
                    day_counts.append({"Date": d.strftime("%b %d"), "Booked": count, "Available": total_seats - count})
                st.bar_chart(pd.DataFrame(day_counts).set_index("Date"))

            with right:
                st.subheader("Today's occupancy")
                fig_pie = go.Figure(data=[go.Pie(
                    labels=["Occupied", "Available"],
                    values=[len(occupied_today), total_seats - len(occupied_today)],
                    hole=0.55,
                    marker_colors=["#E24B4A", "#639922"],
                    textinfo="percent", showlegend=True
                )])
                fig_pie.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=220,
                                    legend=dict(orientation="h", y=-0.1))
                st.plotly_chart(fig_pie, use_container_width=True)

        # ── Users Management ─────────────────────────────────────
        elif admin_selection == "Users":
            st.subheader("User Management")

            all_users = get_all_users()

            # Search
            search = st.text_input("Search by username or email", placeholder="Type to filter...")
            filtered = [u for u in all_users if search.lower() in u[1].lower() or search.lower() in u[2].lower()] if search else all_users

            st.caption(f"{len(filtered)} user(s) found")

            for u in filtered:
                uid, uname, uemail, urole = u
                with st.expander(f"👤 {uname}  —  {urole}"):
                    c1, c2 = st.columns(2)
                    c1.write(f"**ID:** {uid}")
                    c1.write(f"**Email:** {uemail}")
                    c2.write(f"**Role:** {urole}")

                    col_del, col_role = st.columns(2)
                    with col_role:
                        new_role = st.selectbox("Change role", ["user", "admin"],
                                                index=0 if urole == "user" else 1,
                                                key=f"role_{uid}")
                        if st.button("Update role", key=f"upd_{uid}"):
                            conn = get_db_connection()
                            cursor = conn.cursor()
                            cursor.execute("UPDATE users SET role=%s WHERE id=%s", (new_role, uid))
                            conn.commit()
                            conn.close()
                            st.toast(f"Role updated to {new_role}", icon="✅")
                            st.rerun()

                    with col_del:
                        st.markdown("")
                        st.markdown("")
                        if st.button("🗑️ Delete user", key=f"del_{uid}", type="secondary"):
                            conn = get_db_connection()
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM users WHERE id=%s", (uid,))
                            cursor.execute("DELETE FROM booked_seats WHERE user_id=%s", (uid,))
                            conn.commit()
                            conn.close()
                            st.toast(f"Deleted {uname}", icon="❌")
                            st.rerun()

            st.markdown("---")

            # Export users
            if all_users:
                df_users = pd.DataFrame(all_users, columns=["ID", "Username", "Email", "Role"])
                csv = df_users.to_csv(index=False).encode('utf-8')
                st.download_button("⬇️ Export users as CSV", csv, "users.csv", "text/csv")

        # ── Bookings Management ──────────────────────────────────
        elif admin_selection == "Bookings":
            st.subheader("Booking Management")

            all_bookings = get_booked()
            today = date.today()

            # Filter controls
            f1, f2 = st.columns(2)
            with f1:
                filter_user = st.text_input("Filter by username", placeholder="All users")
            with f2:
                filter_date = st.date_input("Filter by date", value=None, key="filter_date")

            rows_data = []
            for b in all_bookings:
                try:
                    dates_list = json.loads(b[3]) if isinstance(b[3], str) else (b[3] or [])
                    dates_str = ", ".join(sorted(dates_list))
                    future = [d for d in dates_list if date.fromisoformat(d) >= today]
                except:
                    dates_str = str(b[3])
                    future = []

                # Apply filters
                if filter_user and filter_user.lower() not in b[1].lower():
                    continue
                if filter_date and str(filter_date) not in dates_list:
                    continue

                rows_data.append({
                    "User ID": b[0],
                    "Username": b[1],
                    "Seat": b[2],
                    "Booked dates": dates_str,
                    "Upcoming days": len(future)
                })

            if rows_data:
                df = pd.DataFrame(rows_data)
                st.dataframe(df, use_container_width=True, hide_index=True)

                # Export
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("⬇️ Export bookings as CSV", csv, "bookings.csv", "text/csv")

                st.markdown("---")
                st.markdown("#### Cancel a booking")
                usernames = [r["Username"] for r in rows_data]
                to_cancel = st.selectbox("Select user booking to cancel", usernames, key="cancel_sel")
                if st.button("Cancel booking", type="secondary"):
                    match = next((b for b in all_bookings if b[1] == to_cancel), None)
                    if match:
                        remove_booked(match[0])
                        st.rerun()
            else:
                st.info("No bookings match your filter.")

        # ── Floor Map Editor ─────────────────────────────────────
        elif admin_selection == "Floor Map Editor":
            st.subheader("Floor Map Editor")

            from Database.db import (
                create_seat_positions_table, save_seat_position,
                get_seat_positions, delete_seat_position
            )
            create_seat_positions_table()

            image_path = "C:/Users/Raviraj/Downloads/officespace.jpg"
            image = Image.open(image_path)
            img_array = np.array(image)
            img_w = img_array.shape[1]
            img_h = img_array.shape[0]

            existing = get_seat_positions()
            ex_labels = [r[0] for r in existing]
            ex_x = [r[1] for r in existing]
            ex_y = [r[2] for r in existing]

            left_col, right_col = st.columns([2, 1])

            with left_col:
                st.caption("The map shows all saved desks. Use the controls on the right to add new ones.")

                fig_editor = go.Figure()
                fig_editor.add_layout_image(
                    dict(source=image, xref="x", yref="y", x=0, y=0,
                        sizex=img_w, sizey=img_h,
                        sizing="stretch", opacity=1, layer="below")
                )

                if ex_x:
                    fig_editor.add_trace(go.Scatter(
                        x=ex_x, y=ex_y,
                        mode='markers+text',
                        marker=dict(color='deepskyblue', size=14,
                                    line=dict(color='white', width=2)),
                        text=ex_labels,
                        textposition="top center",
                        textfont=dict(color='white', size=10),
                        hovertemplate="%{text}<br>x=%{x}, y=%{y}<extra></extra>",
                    ))
                else:
                    # Dummy invisible trace so chart renders
                    fig_editor.add_trace(go.Scatter(
                        x=[0], y=[0], mode='markers',
                        marker=dict(color='rgba(0,0,0,0)', size=1),
                        hoverinfo='skip'
                    ))

                fig_editor.update_xaxes(showgrid=False, zeroline=False,
                                        range=[0, img_w], visible=False)
                fig_editor.update_yaxes(showgrid=False, zeroline=False,
                                        range=[img_h, 0], scaleanchor="x", visible=False)
                fig_editor.update_layout(
                    width=700, height=500,
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=False
                )

                # Use hover to find coordinates — show them as user moves mouse
                st.plotly_chart(fig_editor, key="map_preview", use_container_width=False)
                st.caption("Hover over the map to find x,y coordinates shown in the Plotly toolbar (bottom right of chart).")

            with right_col:
                st.markdown("#### Add a desk")
                st.caption(f"Image size: {img_w} × {img_h} px")

                new_seat_id = st.text_input("Desk name", placeholder="e.g. Desk 33", key="new_seat_id")

                x_val = st.number_input("X coordinate", min_value=0, max_value=img_w,
                                        value=img_w // 2, step=1, key="x_input")
                y_val = st.number_input("Y coordinate", min_value=0, max_value=img_h,
                                        value=img_h // 2, step=1, key="y_input")

                # Live preview dot
                fig_preview = go.Figure()
                fig_preview.add_layout_image(
                    dict(source=image, xref="x", yref="y", x=0, y=0,
                        sizex=img_w, sizey=img_h,
                        sizing="stretch", opacity=1, layer="below")
                )
                # Show existing desks faded
                if ex_x:
                    fig_preview.add_trace(go.Scatter(
                        x=ex_x, y=ex_y, mode='markers',
                        marker=dict(color='rgba(135,206,235,0.4)', size=10),
                        hoverinfo='skip', showlegend=False
                    ))
                # Show new position in red
                fig_preview.add_trace(go.Scatter(
                    x=[x_val], y=[y_val], mode='markers+text',
                    marker=dict(color='red', size=16,
                                line=dict(color='white', width=2)),
                    text=[new_seat_id or "New desk"],
                    textposition="top center",
                    textfont=dict(color='white', size=10),
                    hoverinfo='skip', showlegend=False
                ))
                fig_preview.update_xaxes(showgrid=False, zeroline=False,
                                        range=[0, img_w], visible=False)
                fig_preview.update_yaxes(showgrid=False, zeroline=False,
                                        range=[img_h, 0], scaleanchor="x", visible=False)
                fig_preview.update_layout(
                    height=300, margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=False
                )
                st.plotly_chart(fig_preview, key="pos_preview", use_container_width=True)

                if st.button("Save desk", type="primary", use_container_width=True):
                    if not new_seat_id.strip():
                        st.warning("Enter a desk name first.")
                    elif new_seat_id.strip() in ex_labels:
                        st.warning(f"{new_seat_id.strip()} already exists. It will be updated.")
                        save_seat_position(new_seat_id.strip(), x_val, y_val)
                        st.success("Updated!")
                        st.rerun()
                    else:
                        save_seat_position(new_seat_id.strip(), x_val, y_val)
                        st.success(f"Saved {new_seat_id.strip()} at ({x_val}, {y_val})")
                        st.rerun()

            st.markdown("---")

            if existing:
                st.markdown("#### Saved desks")
                df_desks = pd.DataFrame(existing, columns=["Desk Name", "X", "Y"])
                st.dataframe(df_desks, use_container_width=True, hide_index=True)

                st.markdown("#### Remove a desk")
                to_delete = st.selectbox("Select desk to remove", ex_labels, key="del_seat")
                if st.button("Delete desk", type="secondary"):
                    delete_seat_position(to_delete)
                    st.success(f"Deleted {to_delete}")
                    st.rerun()
            else:
                st.info("No desks saved yet.")

        # ── Admin Account ────────────────────────────────────────
        elif admin_selection == "Account":
            today = date.today()
            all_bookings = get_booked()
            all_users = get_all_users()

            st.markdown(f"## 👤 {st.session_state.user['username']}")
            st.markdown("---")

            col_info, col_stats = st.columns([1, 1])

            with col_info:
                st.markdown("#### Account Info")
                st.markdown(f"""
                <div style="background:#1a1a2e;border-radius:12px;padding:1.2rem 1.5rem;border:0.5px solid #444;">
                    <p style="font-size:13px;color:#aaa;margin:0 0 4px;">Username</p>
                    <p style="font-size:18px;font-weight:500;margin:0 0 16px;color:white;">{st.session_state.user['username']}</p>
                    <p style="font-size:13px;color:#aaa;margin:0 0 4px;">Email</p>
                    <p style="font-size:18px;font-weight:500;margin:0 0 16px;color:white;">{st.session_state.user['email']}</p>
                    <p style="font-size:13px;color:#aaa;margin:0 0 4px;">Role</p>
                    <p style="font-size:18px;font-weight:500;margin:0;color:white;">Admin</p>
                </div>
                """, unsafe_allow_html=True)

            with col_stats:
                st.markdown("#### System Overview")

                def seat_booked_today(dates_json):
                    try:
                        dates_list = json.loads(dates_json) if isinstance(dates_json, str) else (dates_json or [])
                        return today in [date.fromisoformat(d) for d in dates_list]
                    except:
                        return False

                occupied_today = [b for b in all_bookings if seat_booked_today(b[3])]

                st.markdown(f"""
                <div style="background:#1a1a2e;border-radius:12px;padding:1.2rem 1.5rem;border:0.5px solid #444;">
                    <p style="font-size:13px;color:#aaa;margin:0 0 4px;">Total users</p>
                    <p style="font-size:18px;font-weight:500;margin:0 0 16px;color:white;">{len(all_users)}</p>
                    <p style="font-size:13px;color:#aaa;margin:0 0 4px;">Total active bookings</p>
                    <p style="font-size:18px;font-weight:500;margin:0 0 16px;color:white;">{len(all_bookings)}</p>
                    <p style="font-size:13px;color:#aaa;margin:0 0 4px;">People in office today</p>
                    <p style="font-size:18px;font-weight:500;margin:0;color:white;">{len(occupied_today)}</p>
                </div>
                """, unsafe_allow_html=True)

    elif st.session_state.user['role'] == 'user':

            # def home():
            #         st.write("Coming soon")

            # def account():
        # With this:
        NAV_OPTIONS = ["Dashboard", "My Account", "Book a seat", "Floor Map"]

        # If a navigation override was requested, sync it to the radio key BEFORE rendering
        if "nav_selection" in st.session_state and st.session_state["nav_selection"] in NAV_OPTIONS:
            st.session_state["nav_radio"] = st.session_state["nav_selection"]
            del st.session_state["nav_selection"]  # clear after applying

        with st.sidebar:
            selection = st.radio("Go to", NAV_OPTIONS, key="nav_radio")
            st.info("System Status: Online") 
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.success("Logged out successfully!")
            st.rerun()

        if selection == "Dashboard":
            st.subheader("Occupancy Dashboard")

            # --- Fetch live data once ---
            all_bookings = get_booked()
            today = date.today()

            def seat_booked_today(dates_json):
                try:
                    dates_list = json.loads(dates_json) if isinstance(dates_json, str) else (dates_json or [])
                    return today in [date.fromisoformat(d) for d in dates_list]
                except:
                    return False

            total_seats = 32
            maintenance = 0

            # Today-specific counts
            # st.write(st.session_state)
            occupied_today = [b for b in all_bookings if seat_booked_today(b[3])]
            my_booking_today = [b for b in occupied_today if b[0] == st.session_state.user["id"]]
            occupied_count = len(occupied_today)
            available_count = total_seats - occupied_count
            occupancy_pct = int((occupied_count / total_seats) * 100)

            # --- Metric Cards ---
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Seats", total_seats)
            col2.metric("Available Today", available_count)
            col3.metric("Reserved Today", occupied_count, delta=f"{occupancy_pct}%")
            col4.metric("Under Maintenance", maintenance, delta_color="inverse")

            st.markdown("---")

            left_col, right_col = st.columns([2, 1])

            with left_col:
                # --- Occupancy by day (next 14 days) ---
                st.subheader("Seat demand — next 14 days")

                day_counts = []
                for i in range(14):
                    d = today + timedelta(days=i)
                    d_str = d.strftime("%Y-%m-%d")
                    count = 0
                    for b in all_bookings:
                        try:
                            dates_list = json.loads(b[3]) if isinstance(b[3], str) else (b[3] or [])
                            if d_str in dates_list:
                                count += 1
                        except:
                            pass
                    day_counts.append({"Date": d.strftime("%b %d"), "Booked": count, "Available": total_seats - count})

                chart_df = pd.DataFrame(day_counts).set_index("Date")
                st.bar_chart(chart_df)

            with right_col:
                # --- My Booking Status ---
                st.subheader("My booking")
                if my_booking_today:
                    b = my_booking_today[0]
                    st.success(f"You have **{b[2]}** booked today.")
                    try:
                        dates_list = json.loads(b[3]) if isinstance(b[3], str) else (b[3] or [])
                        future = sorted([d for d in dates_list if date.fromisoformat(d) >= today])
                        if future:
                            st.caption("Your upcoming booked dates:")
                            for d in future:
                                st.write(f"• {date.fromisoformat(d).strftime('%A, %b %d')}")
                    except:
                        pass
                else:
                    my_any = [b for b in all_bookings if b[0] == st.session_state.user["id"]]
                    if my_any:
                        b = my_any[0]
                        try:
                            dates_list = json.loads(b[3]) if isinstance(b[3], str) else (b[3] or [])
                            future = sorted([d for d in dates_list if date.fromisoformat(d) >= today])
                            st.info(f"No booking today, but **{b[2]}** is booked for {len(future)} upcoming date(s).")
                            for d in future:
                                st.write(f"• {date.fromisoformat(d).strftime('%A, %b %d')}")
                        except:
                            pass
                    else:
                        st.warning("You have no active bookings.")
                        if st.button("Book a seat now ↗"):
                            st.session_state["nav_selection"] = "Book a seat"
                            st.rerun()

            st.markdown("---")

            # --- Who's in today table ---
            left2, right2 = st.columns([2, 1])

            with left2:
                st.subheader("Who's in today")
                if occupied_today:
                    rows_data = []
                    for b in occupied_today:
                        try:
                            dates_list = json.loads(b[3]) if isinstance(b[3], str) else (b[3] or [])
                            future_count = len([d for d in dates_list if date.fromisoformat(d) >= today])
                        except:
                            future_count = 0
                        rows_data.append({
                            "Name": b[1],
                            "Seat": b[2],
                            "Booked days remaining": future_count
                        })
                    st.dataframe(pd.DataFrame(rows_data), use_container_width=True, hide_index=True)
                else:
                    st.info("No one has booked for today yet.")

            with right2:
                # --- Occupancy donut via plotly ---
                st.subheader("Today's occupancy")
                fig_pie = go.Figure(data=[go.Pie(
                    labels=["Occupied", "Available"],
                    values=[occupied_count, available_count],
                    hole=0.55,
                    marker_colors=["#E24B4A", "#639922"],
                    textinfo="percent",
                    showlegend=True
                )])
                fig_pie.update_layout(
                    margin=dict(l=0, r=0, t=0, b=0),
                    height=220,
                    legend=dict(orientation="h", y=-0.1)
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                st.caption(f"{occupancy_pct}% occupied today")

            

        elif selection == "My Account":
            today = date.today()
            all_bookings = get_booked()
            my_booking = next((b for b in all_bookings if b[0] == st.session_state.user["id"]), None)

            def parse_dates(dates_json):
                try:
                    dates_list = json.loads(dates_json) if isinstance(dates_json, str) else (dates_json or [])
                    return sorted([date.fromisoformat(d) for d in dates_list if date.fromisoformat(d) >= today])
                except:
                    return []

            # Header
            st.markdown(f"## 👤 {st.session_state.user['username']}")
            st.markdown("---")

            # Account Info Card
            col_info, col_booking = st.columns([1, 1])

            with col_info:
                st.markdown("#### Account Info")
                st.markdown(f"""
                <div style="background:#1a1a2e;border-radius:12px;padding:1.2rem 1.5rem;border:0.5px solid #444;">
                    <p style="font-size:13px;color:#aaa;margin:0 0 4px;">Username</p>
                    <p style="font-size:18px;font-weight:500;margin:0 0 16px;color:white;">{st.session_state.user['username']}</p>
                    <p style="font-size:13px;color:#aaa;margin:0 0 4px;">Email</p>
                    <p style="font-size:18px;font-weight:500;margin:0 0 16px;color:white;">{st.session_state.user['email']}</p>
                    <p style="font-size:13px;color:#aaa;margin:0 0 4px;">Role</p>
                    <p style="font-size:18px;font-weight:500;margin:0;color:white;">{st.session_state.user['role'].capitalize()}</p>
                </div>
                """, unsafe_allow_html=True)

            with col_booking:
                st.markdown("#### Current Booking")
                if my_booking:
                    future_dates = parse_dates(my_booking[3])
                    booked_today = today in [date.fromisoformat(d) for d in (json.loads(my_booking[3]) if isinstance(my_booking[3], str) else [])]
                    st.markdown(f"""
                    <div style="background:#1a1a2e;border-radius:12px;padding:1.2rem 1.5rem;border:0.5px solid #444;">
                        <p style="font-size:13px;color:#aaa;margin:0 0 4px;">Seat</p>
                        <p style="font-size:26px;font-weight:600;margin:0 0 12px;color:white;">{my_booking[2]}</p>
                        <span style="background:{'#1a6b3a' if booked_today else '#5a4a00'};color:{'#5dca8a' if booked_today else '#f5c518'};padding:4px 12px;border-radius:20px;font-size:12px;">
                            {'✅ Active today' if booked_today else '📅 Upcoming only'}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("")
                    if st.button("🗑️ Remove booking", type="secondary", use_container_width=True):
                        remove_booked(my_booking[0])
                        st.rerun()
                else:
                    st.markdown("""
                    <div style="background:#1a1a2e;border-radius:12px;padding:1.2rem 1.5rem;border:0.5px solid #444;text-align:center;">
                        <p style="color:#aaa;margin:0;">No active booking</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("")
                    if st.button("Book a seat ↗", use_container_width=True):
                        st.session_state["nav_selection"] = "Book a seat"
                        st.rerun()

            st.markdown("---")

            # Upcoming Dates
            st.markdown("#### Upcoming Dates")
            if my_booking:
                future_dates = parse_dates(my_booking[3])
                if future_dates:
                    cols_dates = st.columns(min(len(future_dates), 4))
                    for idx, d in enumerate(future_dates):
                        is_today = d == today
                        with cols_dates[idx % 4]:
                            bg = "#1a3a1a" if is_today else "#1e1e2e"
                            border = "#2d7a2d" if is_today else "#333"
                            label = "Today" if is_today else d.strftime("%A")
                            st.markdown(f"""
                            <div style="background:{bg};border:0.5px solid {border};border-radius:8px;
                                        padding:10px 14px;margin-bottom:8px;text-align:center;">
                                <p style="color:{'#5dca8a' if is_today else '#ccc'};font-weight:500;margin:0 0 4px;">{label}</p>
                                <p style="color:#888;font-size:12px;margin:0;">{d.strftime('%b %d, %Y')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("No upcoming dates.")
            else:
                st.info("Book a seat to see your schedule here.")

            st.markdown("---")

            # Stats
            st.markdown("#### Your stats")
            s1, s2, s3 = st.columns(3)

            if my_booking:
                future_dates = parse_dates(my_booking[3])
                total_booked = len(future_dates)
                days_until_next = (future_dates[0] - today).days if future_dates else 0
            else:
                total_booked = 0
                days_until_next = "-"

            s1.metric("Upcoming booked days", total_booked)
            s2.metric("Days until next booking", days_until_next)
            s3.metric("Total people in office today",
                    len([b for b in all_bookings if today in parse_dates(b[3])]))
            
            
        elif selection == "Book a seat":
            # st.write(st.session_state)

            custom_css = """
            <style>
            /* Target the H1 element which is what st.title renders as */
            h1 {
                color: red; /* Default color */
                transition: color 0.3s; /* Smooth transition for color change */
            }

            h1:hover {
                color: #a8a7a7 !important; /* Color on hover (e.g., blue) */
                cursor: pointer; /* Change cursor to pointer to indicate interactivity */
            }

            # /* Optional: Add a simple underline effect on hover */
            # h1:hover::after {
            #     content: '';
            #     display: block;
            #     width: 0;
            #     height: 2px;
            #     background: red;
            #     transition: width 0.3s;
            # }

            h1:hover::after {
                width: 100%;
            }
            </style> 
            """

            # Inject the custom CSS into the Streamlit app
            st.markdown(custom_css, unsafe_allow_html=True)

            # 3. Custom CSS for "Red" Booked Seats
            # Streamlit primary buttons are usually blue. We target disabled buttons to look red.
            st.markdown("""
                <style>
                /* Style for disabled (booked) buttons */
                button[disabled] {
                    background-color: #808080 !important;
                    color: white !important;
                    border: none !important;
                    opacity: 1 !important;
                }
                </style>
                """, unsafe_allow_html=True)

            # 4. App UI
            # init_db()
            

            booked_seats = get_booked_seats()
            # rows = ["A", "B", "C", "D"]
            # cols = 6
            rows = ["A", "B", "C", "D"]
            cols = 8 # Adjust based on your layout
            desk_num = 1 # Start the counter
            

            # Get the current date and time
            now = datetime.now()

            # st.write(f"Today's date: {converted_today}")
            # st.write(f"Current datetime: {now}")




            alreadySelected=get_booked()
            # st.write(alreadySelected)
            for i in range(len(alreadySelected)):
                if alreadySelected[i][0] == st.session_state.user["id"]:
                    st.write("Your current booked seat is","[",alreadySelected[i][2],"]","for",
                             alreadySelected[i][3])
                    # st.write(alreadySelected)
                    


                    if st.button("Remove booking."): 
                        user_id=alreadySelected[i][0]
                        remove_booked(user_id)
                        st.rerun()
                    
            
                    break
            
            else:

                col1, col2, col3,_ = st.columns([2.8,1,1,4])
                with col1:
                    st.write("#### Choose your seat:")                
                with col2:
                    st.button("💺", type="primary")
                    st.caption("Available")
                with col3:
                    st.button("💺",disabled=True)
                    st.caption("Booked")
                

                for r in rows:
                    cols_ui = st.columns(cols) 
                    for c in range(cols):
                        if desk_num <= 32:
                            seat_label = f"Desk {desk_num}"
                            # st.write(seat_label)

                            # seat_id = f"{r}{c}"
                            is_booked = seat_label in booked_seats
                            
                            @st.dialog("Confirm Selection")
                            def show_confirmation(item_name, username):
                                st.write(f"Are you sure to book seat {item_name} for {username}?")
                                st.write("### Choose time range:")

                                # Directly use the selected seat name — no loop needed
                                seat_to_be = st.session_state.get('selected', '')
                                booked_dates = get_booked_dates(seat_to_be)

                                all_dates = [date.today() + timedelta(days=i) for i in range(14)]

                                # Also exclude dates the current user already has booked on ANY seat
                                already_booked = get_booked()
                                my_booked_dates = set()
                                for b in already_booked:
                                    if b[0] == st.session_state.user["id"]:
                                        try:
                                            dl = json.loads(b[3]) if isinstance(b[3], str) else (b[3] or [])
                                            for d in dl:
                                                my_booked_dates.add(date.fromisoformat(d))
                                        except:
                                            pass

                                # Remove dates already booked by others on this seat AND dates user already has booked
                                available_options = [
                                    d for d in all_dates
                                    if d not in booked_dates and d not in my_booked_dates
                                ]

                                if not available_options:
                                    st.warning("No available dates — either this seat is fully booked or you already have bookings on all upcoming dates.")
                                else:
                                    selected = st.multiselect(
                                        "Select available dates:",
                                        options=available_options,
                                        format_func=lambda x: x.strftime("%A, %b %d"),
                                        key=f"dates_{st.session_state.get('selected', 'default')}"
                                    )
                                    if st.button("Confirm"):
                                        if not selected:
                                            st.warning("Please select at least one date.")
                                        else:
                                            userid = st.session_state.user["id"]
                                            username = st.session_state.user['username']
                                            seat = st.session_state.selected
                                            book_seat(userid, username, seat, selected)
                            with cols_ui[c]:
                                if st.button(seat_label, key=seat_label,
                                                    disabled=is_booked,                                                                                                 #    type="primary", 
                                                    # type="secondary" if st.session_state.is_primary else "primary",
                                                    type="primary",
                                                    # on_click=toggle_type,
                                                    use_container_width=True,
                                                    args=(seat_label,)):
                                    # book_seat(seat_id,userid)
                                    st.session_state.selected=seat_label
                                    # st.write(seat_id)
                                    show_confirmation(st.session_state.selected,st.session_state.user['username'])
                            desk_num += 1 # Increment for the next button
        elif selection == "Floor Map":
            # st.write(st.session_state)

            today = date.today()

            st.markdown("""
                <style>
                /* Target the drag layer of the Plotly chart to show a pointer cursor */
                .js-plotly-plot .plotly .nsewdrag {
                    cursor: pointer !important;
                }
                /* Optional: also change cursor for the individual points/markers */
                .js-plotly-plot .plotly .cursor-crosshair {
                    cursor: pointer !important;
                }
                </style>
            """, unsafe_allow_html=True)
            # st.write("Office floor map")
            image_path = "C:/Users/Raviraj/Downloads/officespace.jpg"
            image = Image.open(image_path)
            img_array = np.array(image)


            # 4. Define points (x, y coordinates)
            # Note: Ensure these points exist within the image dimensions
            x_coords = [45, 109, 103, 78, 142, 167, 31, 62, 97, 132, 171, 206, 45, 117, 189,
                        503, 325, 505, 582, 634, 668, 630, 630, 584, 505, 544, 580, 632, 706, 704, 708, 706]

            y_coords = [278, 224, 337, 308, 252, 278, 46, 47, 46, 52, 46, 49, 169, 168, 166,
                        76, 515, 136, 79, 135, 201, 280, 338, 304, 303, 236, 136, 76, 74, 136, 337, 278 ]
            


           

            booked = get_booked()
            labels = [f"Desk {i+1}" for i in range(len(x_coords))]
            today = date.today()

            def seat_booked_today(dates_json):
                try:
                    dates_list = json.loads(dates_json) if isinstance(dates_json, str) else (dates_json or [])
                    return today in [date.fromisoformat(d) for d in dates_list]
                except:
                    return False

            # Build today-aware sets
            my_bookings_today = [
                item[2] for item in booked
                if item[1] == st.session_state.user["username"] and seat_booked_today(item[3])
            ]
            others_booked_today = [
                item[2] for item in booked
                if item[1] != st.session_state.user["username"] and seat_booked_today(item[3])
            ]

            colors = [
                "deepskyblue" if label in my_bookings_today      # your seat booked for today
                else "red"    if label in others_booked_today     # someone else booked for today
                else "limegreen"                                  # free today (even if booked on other dates)
                for label in labels
            ]
                

            col1, col2, col3,col4= st.columns([1.5,1,1,1]) 
            with col1:
                st.write("#### Choose your seat:")                 
            with col2:
                st.button("🔵 Your Seat") 
            with col3:
                st.button("🟢 Available today") 
            with col4:
                st.button("🔴 Booked today")

            fig = go.Figure()

            # 1. Add background image
            fig.add_layout_image(
                dict(source=image, xref="x", yref="y", x=0, y=0,
                    sizex=img_array.shape[1], sizey=img_array.shape[0],
                    sizing="stretch", opacity=1, layer="below")
            )

            hover_texts = []
            for label in labels:
                # Find who has this seat booked today
                occupant = None
                for item in booked:
                    if item[2] == label and seat_booked_today(item[3]):
                        occupant = item[1]  # user_name is index 1
                        break
                
                if label in my_bookings_today:
                    hover_texts.append(f"<b>{label}</b><br>👤 {occupant} (You)<br>🔵 Your seat today")
                elif label in others_booked_today:
                    hover_texts.append(f"<b>{label}</b><br>👤 {occupant}<br>🔴 Occupied today")
                else:
                    hover_texts.append(f"<b>{label}</b><br>🟢 Available today")


            # 2. Add clickable, hovering dots
            fig.add_trace(go.Scatter(
                x=x_coords, y=y_coords, mode='markers',
                marker=dict(color=colors, size=12),
                text=hover_texts,
                hovertemplate="%{text}<extra></extra>",
            ))

            # # 3. Configure axes and display
            fig.update_xaxes(showgrid=False, zeroline=False, range=[0, img_array.shape[1]])
            fig.update_yaxes(showgrid=False, zeroline=False, range=[img_array.shape[0], 0], scaleanchor="x")
            fig.update_layout(width=800, height=600, margin=dict(l=0, r=0, t=0, b=0))

            # Add a unique key and set on_select to 'rerun'
            # st.plotly_chart(fig)


            @st.dialog("Confirm Selection")
            def vote_dialog():
                point_index = event["selection"]["points"][0]["point_index"]
                selected_label = labels[point_index]
                username = st.session_state.user['username']
                st.write(f"Are you sure to book seat {selected_label} for {username}?")

                st.write("### Choose time range:")

                all_dates = [date.today() + timedelta(days=i) for i in range(14)]
                booked_dates = get_booked_dates(selected_label)
                available_options = [d for d in all_dates if d not in booked_dates]

                if not available_options:
                    st.warning("This seat is fully booked for the next 14 days.")
                else:
                    selected = st.multiselect(
                        "Select available dates:",
                        options=available_options,
                        format_func=lambda x: x.strftime("%A, %b %d"),
                        key=f"floor_dates_{selected_label}"
                    )
                    if st.button("Confirm"):
                        if not selected:
                            st.warning("Please select at least one date.")
                        else:
                            userid = st.session_state.user["id"]
                            username = st.session_state.user['username']
                            seat = selected_label
                            book_seat(userid, username, seat, selected)



            event = st.plotly_chart(fig, key="floor_map", on_select="rerun")
            

            # Check if a point was clicked
            already_booked = get_booked()
            # st.write(already_booked)
            user_already_has_booking = any(
            item[0] == st.session_state.user["id"]
            for item in already_booked
            )
            for i in range(len(already_booked)): 
                if user_already_has_booking:
                    if already_booked[i][0] == st.session_state.user["id"]:
                        if st.button("Remove booking.", key=f"remove_{i}"):
                                user_id=already_booked[i][0]
                                # st.write(st.session_state.user["id"])
                                # st.write(already_booked)
                                remove_booked(user_id)
                                st.rerun()
                        break
            
            if event and "selection" in event and len(event["selection"]["points"]) > 0:
                # 1. Identify which desk was clicked
                point_index = event["selection"]["points"][0]["point_index"]
                selected_label = labels[point_index]

                # --- LOGIC RULES ---
                # With this:
                if user_already_has_booking:
                    st.toast("⚠️ You already have a booking. Please remove it before booking a new seat.")

                else:
                    # Open dialog regardless — booked dates are filtered inside vote_dialog()
                    vote_dialog()


                