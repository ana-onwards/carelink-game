"""Project Bridge - Card Reveal Group Dynamics App."""

import streamlit as st
import random
import db
from cards import DEPARTMENTS, BEHAVIORS, BACKSTORY, MISSION_TEXT
from wheel import render_card

# Page config
st.set_page_config(
    page_title="Project Bridge",
    page_icon="🌉",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .login-header {
        text-align: center;
        padding: 40px 0 20px;
    }
    .login-header h1 {
        font-size: 2.4em;
        font-weight: 800;
        color: #D4A056;
        margin-bottom: 4px;
    }
    .login-header p {
        color: #888;
        font-size: 1em;
    }
    
    .phase-badge {
        display: inline-block;
        padding: 6px 16px;
        background: rgba(212, 160, 86, 0.15);
        border: 1px solid rgba(212, 160, 86, 0.3);
        border-radius: 20px;
        color: #D4A056;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 16px;
    }
    
    .progress-text {
        text-align: center;
        color: #888;
        font-size: 13px;
        margin: 8px 0 16px;
    }
    
    .secret-reminder {
        text-align: center;
        color: #D4A056;
        font-size: 18px;
        font-weight: 600;
        padding: 16px;
        margin-top: 20px;
        border: 2px dashed rgba(212, 160, 86, 0.3);
        border-radius: 12px;
    }
    
    .complete-card {
        text-align: center;
        padding: 30px;
        background: rgba(212, 160, 86, 0.08);
        border: 1px solid rgba(212, 160, 86, 0.2);
        border-radius: 16px;
        margin: 20px 0;
    }
    .complete-card h2 {
        color: #D4A056;
        margin-bottom: 8px;
    }
    .complete-card p {
        color: #aaa;
        font-size: 15px;
    }
    
    .admin-table {
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
    }
    .admin-table th {
        background: rgba(212, 160, 86, 0.2);
        color: #D4A056;
        padding: 10px 12px;
        text-align: left;
        font-size: 12px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .admin-table td {
        padding: 10px 12px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        color: #ccc;
        font-size: 14px;
    }
    .status-waiting { color: #666; }
    .status-partial { color: #E8871E; }
    .status-complete { color: #4CAF50; }
</style>
""", unsafe_allow_html=True)


def init_session():
    """Initialize session state."""
    defaults = {
        "user": None,
        "page": "login",
        "dept_assigned": False,
        "behav_assigned": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def check_existing_assignment():
    """Restore state if user already has assignments (e.g., page refresh)."""
    if st.session_state.user:
        assignment = db.get_assignment(st.session_state.user["id"])
        if assignment:
            if assignment["department_code"]:
                st.session_state.dept_assigned = True
            if assignment["behavior_name"]:
                st.session_state.behav_assigned = True


def assign_random_department(user_id: int):
    """
    Atomically pick and assign a random available department.
    Retries up to 8 times with small random delay if there's a race condition.
    """
    import time
    for attempt in range(8):
        taken = db.get_taken_departments()
        available = [d for d in DEPARTMENTS if d["code"] not in taken]
        if not available:
            return None
        pick = random.choice(available)
        success = db.assign_department(user_id, pick["code"], pick["name"])
        if success:
            return pick
        # Small random backoff before retry
        time.sleep(random.uniform(0.05, 0.15))
    return None


def assign_random_behavior(user_id: int):
    """
    Atomically pick and assign a random available behavior.
    Retries up to 8 times with small random delay if there's a race condition.
    """
    import time
    for attempt in range(8):
        taken = db.get_taken_behaviors()
        available = [b for b in BEHAVIORS if b["name"] not in taken]
        if not available:
            return None
        pick = random.choice(available)
        success = db.assign_behavior(user_id, pick["name"])
        if success:
            return pick
        time.sleep(random.uniform(0.05, 0.15))
    return None


# ============================================================
# PAGES
# ============================================================

def show_login():
    """Login page."""
    st.markdown("""
    <div class="login-header">
        <h1>🌉 Project Bridge</h1>
        <p>Group Dynamics Exercise</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="director1")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Enter", use_container_width=True)

            if submitted:
                if username == "facilitator":
                    admin_pwd = st.secrets.get("admin_password", "facilitator")
                    if password == admin_pwd:
                        st.session_state.page = "admin"
                        st.rerun()
                    else:
                        st.error("Invalid password.")
                else:
                    user = db.authenticate(username, password)
                    if user:
                        st.session_state.user = user
                        st.session_state.page = "dashboard"
                        check_existing_assignment()
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")


def show_dashboard():
    """Main dashboard - reveal buttons + cards."""
    user = st.session_state.user
    user_id = user["id"]
    assignment = db.get_assignment(user_id)
    progress = db.get_progress()

    # Header
    st.markdown(f"""
    <div style="text-align: center; padding: 16px 0 8px;">
        <div style="color: #888; font-size: 13px;">Welcome,</div>
        <div style="color: #D4A056; font-size: 22px; font-weight: 700;">{user['display_name']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── BOTH ASSIGNED: show final state ──
    if assignment["department_code"] and assignment["behavior_name"]:
        st.markdown("""
        <div class="secret-reminder">
            🤫 Don't reveal your roles to anyone!
        </div>
        """, unsafe_allow_html=True)

        dept = next(d for d in DEPARTMENTS if d["code"] == assignment["department_code"])
        behav = next(b for b in BEHAVIORS if b["name"] == assignment["behavior_name"])

        render_card(dept["code"], dept["name"], dept["description"], dept["color"], "DEPARTMENT")
        render_card(behav["name"], None, behav["description"], behav["color"], "BEHAVIOR")

        st.markdown("""
        <div class="complete-card">
            <h2>You're Ready</h2>
            <p>Stay in character. The CEO will be back soon.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── DEPARTMENT NOT YET ASSIGNED ──
    if not assignment["department_code"]:
        st.markdown(
            '<div style="text-align:center;">'
            '<span class="phase-badge">Phase 1 — Your Department</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="progress-text">'
            f'{progress["departments_assigned"]} of {progress["total"]} directors have revealed'
            f'</div>',
            unsafe_allow_html=True,
        )

        if st.button("🎴  Reveal Your Department", use_container_width=True, key="reveal_dept"):
            result = assign_random_department(user_id)
            if result:
                st.session_state.dept_assigned = True
                st.rerun()
            else:
                st.error("All departments have been assigned. Ask the facilitator to reset.")
        return

    # ── DEPARTMENT ASSIGNED, BEHAVIOR NOT YET ──
    if assignment["department_code"] and not assignment["behavior_name"]:
        # Show their department card
        dept = next(d for d in DEPARTMENTS if d["code"] == assignment["department_code"])
        render_card(dept["code"], dept["name"], dept["description"], dept["color"], "DEPARTMENT")

        st.markdown("---")

        st.markdown(
            '<div style="text-align:center;">'
            '<span class="phase-badge">Phase 2 — Your Behavior Role</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="progress-text">'
            f'{progress["behaviors_assigned"]} of {progress["total"]} directors have revealed'
            f'</div>',
            unsafe_allow_html=True,
        )

        if st.button("🎴  Reveal Your Behavior", use_container_width=True, key="reveal_behav"):
            result = assign_random_behavior(user_id)
            if result:
                st.session_state.behav_assigned = True
                st.rerun()
            else:
                st.error("All behaviors have been assigned. Ask the facilitator to reset.")
        return


def show_admin():
    """Facilitator admin panel."""
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 10px;">
        <div style="color: #D4A056; font-size: 28px; font-weight: 800;">🌉 Project Bridge</div>
        <div style="color: #888; font-size: 14px;">Facilitator Panel</div>
    </div>
    """, unsafe_allow_html=True)

    # Backstory
    with st.expander("📖 Company Backstory & Mission", expanded=False):
        st.markdown(BACKSTORY)
        st.markdown("---")
        st.markdown("**Read this aloud to participants:**")
        st.markdown(f"*\"{MISSION_TEXT}\"*")

    # Progress metrics
    progress = db.get_progress()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Departments", f"{progress['departments_assigned']}/{progress['total']}")
    with col2:
        st.metric("Behaviors", f"{progress['behaviors_assigned']}/{progress['total']}")
    with col3:
        complete = min(progress['departments_assigned'], progress['behaviors_assigned'])
        st.metric("Fully Ready", f"{complete}/{progress['total']}")

    # Assignment table
    st.markdown("### Assignment Board")
    assignments = db.get_all_assignments()

    table_html = '<table class="admin-table"><thead><tr>'
    table_html += '<th>Director</th><th>Department</th><th>Behavior</th><th>Status</th>'
    table_html += '</tr></thead><tbody>'

    for a in assignments:
        dept_display = f"{a['department_code']} — {a['department_name']}" if a['department_code'] else "—"
        behav_display = a['behavior_name'] if a['behavior_name'] else "—"

        if a['department_code'] and a['behavior_name']:
            status = '<span class="status-complete">✓ Ready</span>'
        elif a['department_code']:
            status = '<span class="status-partial">◐ In progress</span>'
        else:
            status = '<span class="status-waiting">○ Waiting</span>'

        table_html += (
            f'<tr>'
            f'<td><strong>{a["display_name"]}</strong><br>'
            f'<span style="color:#666;font-size:12px;">{a["username"]}</span></td>'
            f'<td>{dept_display}</td>'
            f'<td>{behav_display}</td>'
            f'<td>{status}</td>'
            f'</tr>'
        )

    table_html += '</tbody></table>'
    st.markdown(table_html, unsafe_allow_html=True)

    # Controls
    st.markdown("### Controls")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset All Assignments", use_container_width=True, type="secondary"):
            st.session_state.confirm_reset = True

    with col2:
        if st.button("↻ Refresh", use_container_width=True):
            st.rerun()

    if st.session_state.get("confirm_reset", False):
        st.warning("Are you sure? This will clear all assignments.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, reset everything", use_container_width=True, type="primary"):
                db.reset_all()
                st.session_state.confirm_reset = False
                st.rerun()
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.confirm_reset = False
                st.rerun()

    # Logout
    st.markdown("---")
    if st.button("← Back to Login", key="admin_logout"):
        st.session_state.page = "login"
        st.rerun()


# ============================================================
# MAIN
# ============================================================

init_session()

# Restore state on refresh
if st.session_state.user:
    check_existing_assignment()

# Route
if st.session_state.page == "login":
    show_login()
elif st.session_state.page == "admin":
    show_admin()
elif st.session_state.page == "dashboard":
    if st.session_state.user is None:
        st.session_state.page = "login"
        st.rerun()
    else:
        show_dashboard()
        st.markdown("---")
        if st.button("← Logout", key="user_logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
