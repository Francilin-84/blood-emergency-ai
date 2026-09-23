
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Blood AI Emergency System",
    page_icon="🩸",
    layout="wide"
)
# ============================================================
# LOGIN / AUTHENTICATION
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_role" not in st.session_state:
    st.session_state.user_role = ""

if not st.session_state.logged_in:

    st.title("🩸 RED STREAM")
    st.subheader("Blood Emergency Management System")

    st.markdown("### 🔐 User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    role = st.selectbox(
        "Select Role",
        ["Hospital", "Blood Bank", "Admin"]
    )

    if st.button("🔑 Login", use_container_width=True):

        demo_users = {
            "hospital": ("hospital123", "Hospital"),
            "bloodbank": ("blood123", "Blood Bank"),
            "admin": ("admin123", "Admin")
        }

        if username in demo_users:
            correct_password, correct_role = demo_users[username]

            if password == correct_password and role == correct_role:
                st.session_state.logged_in = True
                st.session_state.user_role = role
                st.rerun()
            else:
                st.error("❌ Incorrect username, password or role.")
        else:
            st.error("❌ User not found.")

    st.info(
        "Demo accounts: hospital / hospital123 | "
        "bloodbank / blood123 | admin / admin123"
    )

    st.stop()

# =========================================================
# TITLE
# =========================================================

st.title("🩸 AI-Based Emergency Blood Demand Prediction")
st.subheader("🚨 Smart Donor Coordination System")

st.info(
    "Prototype for emergency blood-demand prediction and donor coordination. "
    "Final medical eligibility, donor eligibility and transfusion decisions "
    "must be made by authorized healthcare professionals."
)

# =========================================================
# SAMPLE DONOR DATA
# =========================================================

donors = pd.DataFrame({
    "Donor": [
        "Arun", "Priya", "Kumar", "Divya",
        "Rahul", "Meena", "Vijay", "Anitha"
    ],

    "Blood_Group": [
        "O+", "O+", "A+", "B+",
        "O-", "AB+", "B+", "A+"
    ],

    "Distance_km": [
        2.1, 4.5, 1.8, 3.2,
        6.4, 2.7, 5.1, 4.0
    ],

    "Location": [
        "Vaniyambadi",
        "Ambur",
        "Vaniyambadi",
        "Tirupattur",
        "Ambur",
        "Vaniyambadi",
        "Tirupattur",
        "Ambur"
    ],

    "Phone": [
        "9000000001",
        "9000000002",
        "9000000003",
        "9000000004",
        "9000000005",
        "9000000006",
        "9000000007",
        "9000000008"
    ],

    "Available": [
        "Yes", "Yes", "Yes", "No",
        "Yes", "Yes", "Yes", "Yes"
    ]
})

# =========================================================
# BLOOD BANK STOCK
# =========================================================

blood_stock = {
    "A+": 12,
    "A-": 4,
    "B+": 15,
    "B-": 3,
    "AB+": 7,
    "AB-": 2,
    "O+": 18,
    "O-": 5
}

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("🚨 Emergency Request")

blood_group = st.sidebar.selectbox(
    "Required Blood Group",
    list(blood_stock.keys())
)

units_required = st.sidebar.number_input(
    "Units Required",
    min_value=1,
    max_value=20,
    value=2
)

emergency_level = st.sidebar.selectbox(
    "Emergency Level",
    ["Critical", "High", "Medium", "Low"]
)

hospital = st.sidebar.text_input(
    "Hospital",
    "ABC General Hospital"
)

# =========================================================
# STOCK CALCULATION
# =========================================================

current_stock = blood_stock[blood_group]

shortage = max(
    units_required - current_stock,
    0
)

# =========================================================
# DASHBOARD
# =========================================================

st.header("📊 Emergency Blood Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Stock",
    f"{current_stock} units"
)

col2.metric(
    "Requested",
    f"{units_required} units"
)

col3.metric(
    "Shortage",
    f"{shortage} units"
)

col4.metric(
    "Emergency",
    emergency_level
)

# =========================================================
# SHORTAGE ALERT
# =========================================================

if shortage > 0:

    st.error(
        f"🚨 BLOOD SHORTAGE DETECTED: "
        f"{shortage} additional {blood_group} unit(s) required."
    )

else:

    st.success(
        f"✅ Sufficient {blood_group} stock available for this request."
    )

# -----------------------------
# AI DEMAND PREDICTION
# -----------------------------

st.header("🤖 AI Blood Demand Prediction")

# Create synthetic historical demand data for demonstration
np.random.seed(42)

days = np.arange(1, 101)

# Base historical demand with gradual trend
historical_demand = (
    10
    + 0.08 * days
    + np.random.normal(0, 2, 100)
)

X = days.reshape(-1, 1)
y = historical_demand

# Train Random Forest model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# Predict next day
next_day = np.array([[101]])
base_prediction = model.predict(next_day)[0]

# Emergency-level adjustment
emergency_multiplier = {
    "Critical": 1.30,
    "High": 1.20,
    "Medium": 1.10,
    "Low": 1.00
}

predicted_demand = (
    base_prediction *
    emergency_multiplier[emergency_level]
)

# Blood-group adjustment
blood_group_multiplier = {
    "A+": 1.00,
    "A-": 0.85,
    "B+": 1.05,
    "B-": 0.80,
    "AB+": 0.70,
    "AB-": 0.60,
    "O+": 1.15,
    "O-": 0.75
}

predicted_demand *= blood_group_multiplier[blood_group]

# Display prediction
col1, col2, col3 = st.columns(3)

col1.metric(
    "AI Predicted Demand",
    f"{predicted_demand:.1f} units"
)

col2.metric(
    "Current Stock",
    f"{blood_stock[blood_group]} units"
)

predicted_shortage = max(
    predicted_demand - blood_stock[blood_group],
    0
)

col3.metric(
    "Predicted Shortage",
    f"{predicted_shortage:.1f} units"
)

# -----------------------------
# DEMAND TREND CHART
# -----------------------------

st.subheader("📈 Historical Demand Trend")

chart_df = pd.DataFrame({
    "Day": days,
    "Historical Demand": historical_demand
})

chart_df = chart_df.set_index("Day")

st.line_chart(chart_df)

# -----------------------------
# PREDICTION RESULT
# -----------------------------

if predicted_shortage > 0:

    st.error(
        f"🚨 Potential shortage detected for {blood_group}. "
        f"Approximately {predicted_shortage:.1f} additional units "
        f"may be required."
    )

else:

    st.success(
        f"✅ Current {blood_group} stock may be sufficient "
        f"for the predicted demand."
    )

# -----------------------------
# AI EXPLANATION
# -----------------------------

with st.expander("🧠 How does the AI prediction work?"):

    st.write(
        "The system analyzes historical blood-demand patterns "
        "using a Random Forest regression model."
    )

    st.write(
        "The prediction is then adjusted according to the "
        "selected blood group and emergency level."
    )

    st.write(
        "Finally, predicted demand is compared with current "
        "blood-bank stock to identify possible shortages."
    )

    st.caption(
        "Note: Historical demand data in this prototype is "
        "synthetic demonstration data."
    )

# =========================================================
# SMART DONOR MATCHING
# =========================================================

st.header("🩸 Smart Donor Matching")

compatible_donors = donors[
    (donors["Blood_Group"] == blood_group) &
    (donors["Available"] == "Yes")
].copy()

if len(compatible_donors) > 0:

    # ---------------------------------------------
    # PRIORITY SCORE
    # ---------------------------------------------

    compatible_donors["Priority_Score"] = (
        100 / (compatible_donors["Distance_km"] + 1)
    )

    # Emergency priority
    if emergency_level == "Critical":
        compatible_donors["Priority_Score"] *= 1.5

    elif emergency_level == "High":
        compatible_donors["Priority_Score"] *= 1.25

    compatible_donors = compatible_donors.sort_values(
        "Priority_Score",
        ascending=False
    )

    st.success(
        f"✅ {len(compatible_donors)} compatible donor(s) found."
    )

    # ---------------------------------------------
    # DONOR TABLE
    # ---------------------------------------------

    display_df = compatible_donors[
        [
            "Donor",
            "Blood_Group",
            "Distance_km",
            "Location",
            "Phone",
            "Available",
            "Priority_Score"
        ]
    ].copy()

    display_df["Priority_Score"] = display_df[
        "Priority_Score"
    ].round(2)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # =================================================
    # TOP DONOR
    # =================================================

    top_donor = compatible_donors.iloc[0]

    st.subheader("⭐ Recommended Donor to Contact First")

    d1, d2, d3, d4 = st.columns(4)

    d1.metric(
        "Donor",
        top_donor["Donor"]
    )

    d2.metric(
        "Distance",
        f"{top_donor['Distance_km']} km"
    )

    d3.metric(
        "Location",
        top_donor["Location"]
    )

    d4.metric(
        "Priority",
        f"{top_donor['Priority_Score']:.2f}"
    )

    # =================================================
    # DONOR REQUEST
    # =================================================

   # ============================================================
# DONOR REQUEST & RESPONSE TRACKING
# ============================================================

# Create a unique key for the currently recommended donor
# ============================================================
# DONOR REQUEST & RESPONSE TRACKING
# ============================================================

# Create a key for the current blood group
donor_flow_key = blood_group

# Initialize donor selection
if st.session_state.get("donor_flow_key") != donor_flow_key:
    st.session_state.donor_flow_key = donor_flow_key
    st.session_state.active_donor_index = 0
    st.session_state.donor_request_sent = False
    st.session_state.donor_response = "Not Requested"


# Get the currently selected donor
active_donor_index = st.session_state.active_donor_index

if active_donor_index < len(compatible_donors):

    active_donor = compatible_donors.iloc[active_donor_index]


    # --------------------------------------------------------
    # CURRENT DONOR
    # --------------------------------------------------------

    st.subheader("📱 Donor Coordination")

    if active_donor_index == 0:
        st.info(
            f"⭐ First priority donor: "
            f"**{active_donor['Donor']}**"
        )
    else:
        st.info(
            f"🔄 Next priority donor selected: "
            f"**{active_donor['Donor']}**"
        )

    st.write(
        f"🩸 Blood Group: **{active_donor['Blood_Group']}**"
    )

    st.write(
        f"📍 Distance: **{active_donor['Distance_km']} km**"
    )

    st.write(
        f"📌 Location: **{active_donor['Location']}**"
    )

    st.write(
        f"⭐ Priority Score: "
        f"**{active_donor['Priority_Score']:.2f}**"
    )


    # --------------------------------------------------------
    # REQUEST DONATION
    # --------------------------------------------------------

    if not st.session_state.donor_request_sent:

        if st.button(
            f"🩸 Request Donation From {active_donor['Donor']}",
            key=f"request_{active_donor_index}"
        ):

            st.session_state.donor_request_sent = True
            st.session_state.donor_response = "Awaiting Response"

            st.success(
                f"📨 Donation request sent to "
                f"**{active_donor['Donor']}**."
            )

            st.warning(
                f"🟡 Awaiting response from "
                f"**{active_donor['Donor']}**."
            )

            st.rerun()


    # --------------------------------------------------------
    # RESPONSE TRACKING
    # --------------------------------------------------------

    if st.session_state.donor_request_sent:

        st.subheader("📱 Donor Response Tracking")

        response = st.session_state.donor_response


        # ----------------------------------------------------
        # AWAITING RESPONSE
        # ----------------------------------------------------

        if response == "Awaiting Response":

            st.warning(
                f"🟡 **Awaiting Response** from "
                f"**{active_donor['Donor']}**"
            )

            st.write(
                "For this prototype, the donor response "
                "can be simulated below."
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✅ Simulate Accept",
                    key=f"accept_{active_donor_index}"
                ):

                    st.session_state.donor_response = "Accepted"
                    st.rerun()


            with col2:

                if st.button(
                    "❌ Simulate Decline",
                    key=f"decline_{active_donor_index}"
                ):

                    st.session_state.donor_response = "Declined"
                    st.rerun()


        # ----------------------------------------------------
        # ACCEPTED
        # ----------------------------------------------------

        elif response == "Accepted":

            st.success(
                f"🟢 **{active_donor['Donor']} accepted "
                f"the donation request.**"
            )

            st.write(
                f"📍 Location: {active_donor['Location']}"
            )

            st.write(
                "🏥 Hospital can proceed with the "
                "next coordination step."
            )


        # ----------------------------------------------------
        # DECLINED
        # ----------------------------------------------------

        elif response == "Declined":

            st.error(
                f"🔴 **{active_donor['Donor']} declined "
                f"the donation request.**"
            )

            # Check whether another donor is available
            next_index = active_donor_index + 1

            if next_index < len(compatible_donors):

                next_donor = compatible_donors.iloc[next_index]

                st.warning(
                    f"🔄 **Next priority donor selected:** "
                    f"{next_donor['Donor']}"
                )

                st.write(
                    f"📍 Distance: {next_donor['Distance_km']} km"
                )

                st.write(
                    f"📌 Location: {next_donor['Location']}"
                )

                if st.button(
                    "➡️ Continue With Next Donor",
                    key=f"next_donor_{next_index}"
                ):

                    st.session_state.active_donor_index = next_index
                    st.session_state.donor_request_sent = False
                    st.session_state.donor_response = "Not Requested"

                    st.rerun()

            else:

                st.error(
                    "❌ No more compatible donors are "
                    "available in the current list."
                )


    # --------------------------------------------------------
    # PROTOTYPE NOTICE
    # --------------------------------------------------------

    st.caption(
        "⚠️ Prototype response tracking only. "
        "Actual donor communication, donor eligibility, "
        "and medical decisions must follow authorized "
        "hospital/blood-bank procedures."
    )
else:

    st.error(
        f"❌ No currently available exact {blood_group} donor found."
    )

# =========================================================
# EMERGENCY ALERT
# =========================================================

st.header("🔔 Emergency Donor Alert")

if st.button("🚨 Send Emergency Alerts"):

    if len(compatible_donors) > 0:

        st.success(
            f"Emergency alert simulated for "
            f"{len(compatible_donors)} compatible donor(s)."
        )

        for donor in compatible_donors["Donor"]:

            st.write(
                f"📱 Alert sent to **{donor}**"
            )

    else:

        st.warning(
            "No compatible donors available for alert."
        )

# =========================================================
# BLOOD STOCK
# =========================================================

st.header("📦 Blood Bank Stock")

stock_df = pd.DataFrame(
    list(blood_stock.items()),
    columns=["Blood Group", "Units"]
)

st.bar_chart(
    stock_df.set_index("Blood Group")
)

# -----------------------------
# EMERGENCY REQUEST HISTORY
# -----------------------------

st.header("🏥 Emergency Request History")

if "request_history" not in st.session_state:
    st.session_state.request_history = []

if st.button("➕ Record Emergency Request"):

    request = {
        "Hospital": hospital,
        "Blood Group": blood_group,
        "Units": units_required,
        "Emergency": emergency_level,
        "Predicted Demand": round(predicted_demand, 1),
        "Shortage": round(shortage, 1),
        "Status": "Critical" if shortage > 0 else "Stock Available"
    }

    st.session_state.request_history.append(request)

    st.success("✅ Emergency request recorded successfully!")

if st.session_state.request_history:

    history_df = pd.DataFrame(
        st.session_state.request_history
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No emergency requests recorded yet."
    )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🩸 AI Blood Emergency Coordination Prototype | "
    "Uses synthetic demonstration data"   
)
