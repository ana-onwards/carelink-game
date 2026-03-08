"""Project Bridge - Spin the Wheel Group Dynamics App."""

import streamlit as st
import random
import db
from cards import DEPARTMENTS, BEHAVIORS, BACKSTORY, MISSION_TEXT
from wheel import render_wheel, render_card

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
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global font */
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Login styling */
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
    
    /* Phase indicator */
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
    
    /* Progress bar */
    .progress-text {
        text-align: center;
        color: #888;
        font-size: 13px;
        margin-top: 8px;
    }
    
    /* Complete state */
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
    
    /* Secret text */
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
    
    /* Admin table */
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
    if "user" not in st.session_state:
        st.session_state.user = None
    if "page" not in st.session_state:
        st.session_state.page = "login"
    if "dept_spun" not in st.session_state:
        st.session_state.dept_spun = False
    if "behav_spun" not in st.session_state:
        st.session_state.behav_spun = False
    if "assigned_dept" not in st.session_state:
        st.session_state.assigned_dept = None
    if "assigned_behav" not in st.session_state:
        st.session_state.assigned_behav = None


def check_existing_assignment():
    """Check if user already has assignments (e.g., after page refresh)."""
    if st.session_state.user:
        assignment = db.get_assignment(st.session_state.user["id"])
        if assignment:
            if assignment["department_code"]:
                st.session_state.assigned_dept = assignment["department_code"]
                st.session_state.dept_spun = True
            if assignment["behavior_name"]:
                st.session_state.assigned_behav = assignment["behavior_name"]
                st.session_state.behav_spun = True


def show_login():
    """Render login page."""
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


def pick_random_available(items, taken, key_field):
    """Pick a random item that hasn't been taken yet."""
    available = [item for item in items if item[key_field] not in taken]
    if not available:
        return None
    return random.choice(available)


def show_dashboard():
    """Render the main dashboard with wheel spins."""
    user = st.session_state.user
    
    # Header
    st.markdown(f"""
    <div style="text-align: center; padding: 16px 0 8px;">
        <div style="color: #888; font-size: 13px;">Welcome back,</div>
        <div style="color: #D4A056; font-size: 22px; font-weight: 700;">{user['display_name']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Progress
    progress = db.get_progress()
    
    # Check if both spins are done
    if st.session_state.dept_spun and st.session_state.behav_spun:
        show_complete()
        return

    # PHASE 1: Department spin
    if not st.session_state.dept_spun:
        st.markdown('<div style="text-align:center;"><span class="phase-badge">Phase 1 — Your Department</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="progress-text">{progress["departments_assigned"]} of {progress["total"]} directors have spun</div>', unsafe_allow_html=True)

        # Pre-pick a department for this user
        if "pending_dept" not in st.session_state:
            taken = db.get_taken_departments()
            dept = pick_random_available(DEPARTMENTS, taken, "code")
            if dept:
                st.session_state.pending_dept = dept
            else:
                st.error("All departments have been assigned!")
                return

        dept = st.session_state.pending_dept
        dept_items = [{"label": d["code"] + " — " + d["name"], "color": d["color"]} for d in DEPARTMENTS]
        target_idx = next(i for i, d in enumerate(DEPARTMENTS) if d["code"] == dept["code"])

        # Show wheel with spin button embedded in it
        if st.button("🎰 Spin for your Department!", use_container_width=True, key="spin_dept"):
            success = db.assign_department(user["id"], dept["code"], dept["name"])
            if success:
                st.session_state.assigned_dept = dept["code"]
                st.session_state.dept_spun = True
                st.session_state.show_dept_animation = True
                if "pending_dept" in st.session_state:
                    del st.session_state.pending_dept
                st.rerun()
            else:
                if "pending_dept" in st.session_state:
                    del st.session_state.pending_dept
                st.rerun()

    # Department animation + card reveal
    elif st.session_state.dept_spun and not st.session_state.behav_spun and st.session_state.get("show_dept_animation", False):
        dept_code = st.session_state.assigned_dept
        dept = next(d for d in DEPARTMENTS if d["code"] == dept_code)
        
        st.markdown('<div style="text-align:center;"><span class="phase-badge">Your Department</span></div>', unsafe_allow_html=True)
        
        dept_items = [{"label": d["code"] + " — " + d["name"], "color": d["color"]} for d in DEPARTMENTS]
        target_idx = next(i for i, d in enumerate(DEPARTMENTS) if d["code"] == dept_code)
        render_wheel(dept_items, target_idx, wheel_id="dept_result", height=460)
        
        render_card(dept["code"], dept["name"], dept["description"], dept["color"], "DEPARTMENT")
        
        if st.button("Continue to Behavior Spin →", use_container_width=True, key="continue_behav"):
            st.session_state.show_dept_animation = False
            st.rerun()

    # PHASE 2: Behavior spin
    elif st.session_state.dept_spun and not st.session_state.behav_spun:
        # Show current department assignment
        dept_code = st.session_state.assigned_dept
        dept = next(d for d in DEPARTMENTS if d["code"] == dept_code)
        st.markdown(f"""
        <div style="text-align:center; padding: 8px; margin-bottom: 8px;">
            <span style="color: #888; font-size: 13px;">Your department:</span>
            <span style="color: {dept['color']}; font-weight: 700; font-size: 15px; margin-left: 8px;">{dept['code']} — {dept['name']}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="text-align:center;"><span class="phase-badge">Phase 2 — Your Behavior Role</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="progress-text">{progress["behaviors_assigned"]} of {progress["total"]} directors have spun</div>', unsafe_allow_html=True)

        # Pre-pick a behavior
        if "pending_behav" not in st.session_state:
            taken = db.get_taken_behaviors()
            behav = pick_random_available(BEHAVIORS, taken, "name")
            if behav:
                st.session_state.pending_behav = behav
            else:
                st.error("All behavior roles have been assigned!")
                return

        behav = st.session_state.pending_behav
        behav_items = [{"label": b["name"], "color": b["color"]} for b in BEHAVIORS]
        target_idx = next(i for i, b in enumerate(BEHAVIORS) if b["name"] == behav["name"])

        if st.button("🎰 Spin for your Behavior!", use_container_width=True, key="spin_behav"):
            success = db.assign_behavior(user["id"], behav["name"])
            if success:
                st.session_state.assigned_behav = behav["name"]
                st.session_state.behav_spun = True
                st.session_state.show_behav_animation = True
                if "pending_behav" in st.session_state:
                    del st.session_state.pending_behav
                st.rerun()
            else:
                if "pending_behav" in st.session_state:
                    del st.session_state.pending_behav
                st.rerun()

    # Behavior animation + card reveal
    elif st.session_state.behav_spun and st.session_state.get("show_behav_animation", False):
        behav_name = st.session_state.assigned_behav
        behav = next(b for b in BEHAVIORS if b["name"] == behav_name)
        
        st.markdown('<div style="text-align:center;"><span class="phase-badge">Your Behavior Role</span></div>', unsafe_allow_html=True)
        
        behav_items = [{"label": b["name"], "color": b["color"]} for b in BEHAVIORS]
        target_idx = next(i for i, b in enumerate(BEHAVIORS) if b["name"] == behav_name)
        render_wheel(behav_items, target_idx, wheel_id="behav_result", height=460)
        
        render_card(behav["name"], None, behav["description"], behav["color"], "BEHAVIOR")
        
        if st.button("I'm Ready →", use_container_width=True, key="complete"):
            st.session_state.show_behav_animation = False
            st.rerun()


def show_complete():
    """Show final state with both cards."""
    dept_code = st.session_state.assigned_dept
    behav_name = st.session_state.assigned_behav
    dept = next(d for d in DEPARTMENTS if d["code"] == dept_code)
    behav = next(b for b in BEHAVIORS if b["name"] == behav_name)

    st.markdown("""
    <div class="secret-reminder">
        🤫 Don't reveal your roles to anyone!
    </div>
    """, unsafe_allow_html=True)

    render_card(dept["code"], dept["name"], dept["description"], dept["color"], "DEPARTMENT")
    render_card(behav["name"], None, behav["description"], behav["color"], "BEHAVIOR")

    st.markdown("""
    <div class="complete-card">
        <h2>You're Ready</h2>
        <p>Stay in character. The CEO will be back soon.</p>
    </div>
    """, unsafe_allow_html=True)


def show_admin():
    """Render facilitator admin panel."""
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 10px;">
        <div style="color: #D4A056; font-size: 28px; font-weight: 800;">🌉 Project Bridge</div>
        <div style="color: #888; font-size: 14px;">Facilitator Panel</div>
    </div>
    """, unsafe_allow_html=True)

    # Backstory expander
    with st.expander("📖 Company Backstory & Mission", expanded=False):
        st.markdown(BACKSTORY)
        st.markdown("---")
        st.markdown("**Read this aloud to participants:**")
        st.markdown(f"*\"{MISSION_TEXT}\"*")

    # Progress
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
            status = '<span class="status-partial">◐ Spinning...</span>'
        else:
            status = '<span class="status-waiting">○ Waiting</span>'

        table_html += f'<tr><td><strong>{a["display_name"]}</strong><br><span style="color:#666;font-size:12px;">{a["username"]}</span></td>'
        table_html += f'<td>{dept_display}</td><td>{behav_display}</td><td>{status}</td></tr>'

    table_html += '</tbody></table>'
    st.markdown(table_html, unsafe_allow_html=True)

    # Controls
    st.markdown("### Controls")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset All Assignments", use_container_width=True, type="secondary"):
            st.session_state.confirm_reset = True

    if hasattr(st.session_state, 'confirm_reset') and st.session_state.confirm_reset:
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

    # Auto-refresh
    with col2:
        if st.button("↻ Refresh", use_container_width=True):
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

# Check for existing assignments on load
if st.session_state.user and not st.session_state.dept_spun:
    check_existing_assignment()

# Route to the right page
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

        # Logout at the bottom
        st.markdown("---")
        if st.button("← Logout", key="user_logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
