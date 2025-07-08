import streamlit as st
import bcrypt

# --- Hashing ---
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

# --- Signup Function ---
def signup(cursor, conn):
    st.subheader("Create Account")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")

    if st.button("Register"):
        if new_user and new_pass:
            cursor.execute("SELECT * FROM users WHERE username = ?", (new_user,))
            if cursor.fetchone():
                st.error("Username already taken.")
            else:
                hashed_pw = hash_password(new_pass)
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_user, hashed_pw))
                conn.commit()
                st.success("Account created. Please log in.")
                st.session_state.page = "login"
        else:
            st.warning("❗ Please fill all fields.")

    if st.button("Back to Login"):
        st.session_state.page = "login"

# --- Login Function ---
def login(cursor, conn):
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result and check_password(password, result[0]):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            cursor.execute("REPLACE INTO sessions (username, authenticated) VALUES (?, 1)", (username,))
            conn.commit()
            st.success(f"Welcome, {username}!")
            return True
        else:
            st.error("Invalid credentials.")

        st.session_state.page = "signup"

    return False
