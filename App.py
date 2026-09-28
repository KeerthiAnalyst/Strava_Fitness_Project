import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Strava Fitness & Wellness Analytics",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS - BLACK + ORANGE THEME
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #0B0B0B;
        color: #F5F5F5;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #2A2A2A;
    }

    /* Main title */
    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #FF8C00;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #BBBBBB;
        margin-bottom: 25px;
    }

    /* Section headings */
    .section-title {
        color: #FF8C00;
        font-size: 25px;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* KPI cards */
    .metric-card {
        background-color: #151515;
        border: 1px solid #303030;
        border-left: 5px solid #FF8C00;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 10px;
    }

    .metric-title {
        color: #AAAAAA;
        font-size: 14px;
        font-weight: 500;
    }

    .metric-value {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: 700;
        margin-top: 5px;
    }

    /* Insight box */
    .insight-box {
        background-color: #151515;
        border: 1px solid #303030;
        border-radius: 10px;
        padding: 18px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .insight-box h4 {
        color: #FF8C00;
        margin-bottom: 8px;
    }

    .insight-box p {
        color: #DDDDDD;
        line-height: 1.6;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        color: #BBBBBB;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FF8C00;
    }

    /* Buttons */
    .stButton > button {
        background-color: #FF8C00;
        color: #000000;
        border: none;
        border-radius: 7px;
        font-weight: 600;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid #303030;
    }

    /* Divider */
    hr {
        border-color: #333333;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    activity = pd.read_csv("Activity.csv")
    sleep = pd.read_csv("sleep.csv")
    weight = pd.read_csv("weight.csv")

    # Convert dates
    activity["ActivityDate"] = pd.to_datetime(
        activity["ActivityDate"],
        errors="coerce"
    )

    sleep["SleepDay"] = pd.to_datetime(
        sleep["SleepDay"],
        errors="coerce"
    )

    weight["Date"] = pd.to_datetime(
        weight["Date"],
        errors="coerce"
    )

    return activity, sleep, weight


try:
    activity, sleep, weight = load_data()

except FileNotFoundError:
    st.error(
        "CSV files not found. Make sure the three CSV files are in the same folder as app.py."
    )
    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    "<h2 style='color:#FF8C00;'>🏃 Fitness Analytics</h2>",
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    "<p style='color:#BBBBBB;'>Dashboard Filters</p>",
    unsafe_allow_html=True
)


# User filter
user_list = sorted(activity["Id"].unique())

selected_users = st.sidebar.multiselect(
    "Select User ID",
    options=user_list,
    default=[]
)


# Date filter
min_date = activity["ActivityDate"].min().date()
max_date = activity["ActivityDate"].max().date()

date_range = st.sidebar.date_input(
    "Activity Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_activity = activity.copy()

if selected_users:
    filtered_activity = filtered_activity[
        filtered_activity["Id"].isin(selected_users)
    ]


if len(date_range) == 2:

    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])

    filtered_activity = filtered_activity[
        (filtered_activity["ActivityDate"] >= start_date)
        & (filtered_activity["ActivityDate"] <= end_date)
    ]


# Sleep filtering
filtered_sleep = sleep.copy()

if selected_users:
    filtered_sleep = filtered_sleep[
        filtered_sleep["Id"].isin(selected_users)
    ]


# Weight filtering
filtered_weight = weight.copy()

if selected_users:
    filtered_weight = filtered_weight[
        filtered_weight["Id"].isin(selected_users)
    ]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    "<div class='main-title'>Strava Fitness & Wellness Analytics</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Understanding user activity, sleep and weight behaviour through data</div>",
    unsafe_allow_html=True
)
# =========================================================
# BUSINESS PROBLEM & OBJECTIVES
# =========================================================

with st.expander("📌 Business Problem & Analysis Objectives", expanded=True):

    st.markdown(
        """
        <div class="insight-box">

        <h4>Business Problem</h4>

        <p>
        A fitness tracking platform collects user activity, sleep, and weight/BMI data but needs 
        to understand how users behave, track their fitness activities, and engage with the platform.
        </p>

        <h4>Analysis Objectives</h4>

        <p>
        This analysis explores user activity levels, tracker usage,
        sleep patterns, calories burned, and weight/BMI behaviour to
        identify meaningful trends that can support user engagement
        and wellness initiatives.
        </p>

        <h4>Key Questions</h4>

        <p>
        • How active are users based on their daily activity?<br>
        • How consistent are users with their fitness tracking?<br>
        • What patterns can be observed between activity and sleep?<br>
        • How are daily steps related to calories burned?<br>
        • What patterns can be observed in weight and BMI data?
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# KPI CALCULATIONS
# =========================================================

# =========================================================
# KPI CALCULATIONS
# =========================================================

total_users = filtered_activity["Id"].nunique()

avg_steps = filtered_activity["TotalSteps"].mean()

avg_calories = filtered_activity["Calories"].mean()

avg_sleep_minutes = filtered_sleep["TotalMinutesAsleep"].mean()

avg_sleep_hours = avg_sleep_minutes / 60 if pd.notna(avg_sleep_minutes) else 0


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">TOTAL USERS</div>
            <div class="metric-value">{total_users:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">AVG DAILY STEPS</div>
            <div class="metric-value">{avg_steps:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">AVG CALORIES</div>
            <div class="metric-value">{avg_calories:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">AVG SLEEP</div>
            <div class="metric-value">{avg_sleep_hours:.1f} hrs</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Activity",
    "😴 Sleep",
    "⚖️ Weight & BMI",
    "💡 Insights"
])


# =========================================================
# ACTIVITY TAB
# =========================================================

with tab1:

    st.markdown(
        "<div class='section-title'>Activity Overview</div>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # Average steps by user
    # -----------------------------------------------------

    with col1:

        user_steps = (
            filtered_activity
            .groupby("Id")["TotalSteps"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.barh(
            user_steps.index.astype(str),
            user_steps.values
        )

        ax.set_title("Top 10 Users by Average Daily Steps")
        ax.set_xlabel("Average Steps")
        ax.set_ylabel("User ID")

        ax.invert_yaxis()

        fig.patch.set_facecolor("#0B0B0B")
        ax.set_facecolor("#0B0B0B")

        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")

        st.pyplot(fig)

        plt.close(fig)


    # -----------------------------------------------------
    # Activity level
    # -----------------------------------------------------

    with col2:

        activity_levels = pd.DataFrame({
            "Activity Level": [
                "Very Active",
                "Moderately Active",
                "Light Active",
                "Sedentary"
            ],
            "Minutes": [
                filtered_activity["VeryActiveMinutes"].mean(),
                filtered_activity["FairlyActiveMinutes"].mean(),
                filtered_activity["LightlyActiveMinutes"].mean(),
                filtered_activity["SedentaryMinutes"].mean()
            ]
        })

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.bar(
            activity_levels["Activity Level"],
            activity_levels["Minutes"]
        )

        ax.set_title("Average Daily Activity Minutes")
        ax.set_ylabel("Minutes")
        ax.tick_params(axis="x", rotation=20)

        fig.patch.set_facecolor("#0B0B0B")
        ax.set_facecolor("#0B0B0B")

        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")

        st.pyplot(fig)

        plt.close(fig)


    # -----------------------------------------------------
    # Steps vs Calories
    # -----------------------------------------------------

    st.markdown(
        "<div class='section-title'>Steps vs Calories</div>",
        unsafe_allow_html=True
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.scatter(
        filtered_activity["TotalSteps"],
        filtered_activity["Calories"],
        alpha=0.5
    )

    ax.set_title("Daily Steps vs Calories Burned")
    ax.set_xlabel("Total Steps")
    ax.set_ylabel("Calories")

    fig.patch.set_facecolor("#0B0B0B")
    ax.set_facecolor("#0B0B0B")

    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")

    st.pyplot(fig)

    plt.close(fig)


# =========================================================
# SLEEP TAB
# =========================================================

with tab2:

    st.markdown(
        "<div class='section-title'>Sleep Analysis</div>",
        unsafe_allow_html=True
    )

    sleep_col1, sleep_col2 = st.columns(2)


    # -----------------------------------------------------
    # Sleep distribution
    # -----------------------------------------------------

    with sleep_col1:

        sleep_hours = filtered_sleep["TotalMinutesAsleep"] / 60

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.hist(
            sleep_hours.dropna(),
            bins=15
        )

        ax.set_title("Distribution of Sleep Duration")
        ax.set_xlabel("Hours Asleep")
        ax.set_ylabel("Number of Records")

        fig.patch.set_facecolor("#0B0B0B")
        ax.set_facecolor("#0B0B0B")

        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")

        st.pyplot(fig)

        plt.close(fig)


    # -----------------------------------------------------
    # Sleep vs time in bed
    # -----------------------------------------------------

    with sleep_col2:

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.scatter(
            filtered_sleep["TotalTimeInBed"] / 60,
            filtered_sleep["TotalMinutesAsleep"] / 60,
            alpha=0.5
        )

        ax.set_title("Time in Bed vs Actual Sleep")
        ax.set_xlabel("Time in Bed (Hours)")
        ax.set_ylabel("Sleep (Hours)")

        fig.patch.set_facecolor("#0B0B0B")
        ax.set_facecolor("#0B0B0B")

        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")

        st.pyplot(fig)

        plt.close(fig)


    # -----------------------------------------------------
    # Sleep and activity
    # -----------------------------------------------------

    st.markdown(
        "<div class='section-title'>Sleep vs Activity</div>",
        unsafe_allow_html=True
    )

    activity_sleep = pd.merge(
        filtered_activity[
            ["Id", "ActivityDate", "TotalSteps", "Calories"]
        ],
        filtered_sleep[
            ["Id", "SleepDay", "TotalMinutesAsleep"]
        ],
        left_on=["Id", "ActivityDate"],
        right_on=["Id", "SleepDay"],
        how="inner"
    )

    if not activity_sleep.empty:

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.scatter(
            activity_sleep["TotalSteps"],
            activity_sleep["TotalMinutesAsleep"] / 60,
            alpha=0.5
        )

        ax.set_title("Daily Steps vs Sleep Duration")
        ax.set_xlabel("Total Steps")
        ax.set_ylabel("Sleep Hours")

        fig.patch.set_facecolor("#0B0B0B")
        ax.set_facecolor("#0B0B0B")

        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")

        st.pyplot(fig)

        plt.close(fig)

    else:

        st.info("No matching activity and sleep records for the selected filters.")


# =========================================================
# WEIGHT & BMI TAB
# =========================================================

with tab3:

    st.markdown(
        "<div class='section-title'>Weight & BMI Analysis</div>",
        unsafe_allow_html=True
    )

    if filtered_weight.empty:

        st.info("No weight records available for the selected users.")

    else:

        weight_col1, weight_col2 = st.columns(2)


        # -------------------------------------------------
        # BMI distribution
        # -------------------------------------------------

        with weight_col1:

            bmi_data = filtered_weight["BMI"].dropna()

            fig, ax = plt.subplots(figsize=(8, 5))

            ax.hist(
                bmi_data,
                bins=15
            )

            ax.set_title("BMI Distribution")
            ax.set_xlabel("BMI")
            ax.set_ylabel("Number of Records")

            fig.patch.set_facecolor("#0B0B0B")
            ax.set_facecolor("#0B0B0B")

            ax.tick_params(colors="white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.title.set_color("white")

            st.pyplot(fig)

            plt.close(fig)


        # -------------------------------------------------
        # Weight vs BMI
        # -------------------------------------------------

        with weight_col2:

            fig, ax = plt.subplots(figsize=(8, 5))

            ax.scatter(
                filtered_weight["WeightKg"],
                filtered_weight["BMI"],
                alpha=0.7
            )

            ax.set_title("Weight vs BMI")
            ax.set_xlabel("Weight (Kg)")
            ax.set_ylabel("BMI")

            fig.patch.set_facecolor("#0B0B0B")
            ax.set_facecolor("#0B0B0B")

            ax.tick_params(colors="white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.title.set_color("white")

            st.pyplot(fig)

            plt.close(fig)


        # -------------------------------------------------
        # Weight summary
        # -------------------------------------------------

        st.markdown(
            "<div class='section-title'>Weight Summary</div>",
            unsafe_allow_html=True
        )

        weight_summary = filtered_weight[
            ["Id", "WeightKg", "BMI"]
        ].dropna(subset=["WeightKg"])

        st.dataframe(
            weight_summary,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# INSIGHTS TAB
# =========================================================

with tab4:

    st.markdown(
        "<div class='section-title'>Key Business Insights</div>",
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # Activity insight
    # -----------------------------------------------------

    if avg_steps < 5000:

        activity_message = (
            f"The average daily step count is {avg_steps:,.0f}. "
            "This indicates that a substantial portion of tracked activity "
            "may come from lower daily movement levels."
        )

    elif avg_steps < 10000:

        activity_message = (
            f"The average daily step count is {avg_steps:,.0f}. "
            "Users show a moderate level of daily movement, leaving room "
            "for further engagement with activity goals."
        )

    else:

        activity_message = (
            f"The average daily step count is {avg_steps:,.0f}. "
            "The tracked users demonstrate relatively high daily movement."
        )


    st.markdown(
        f"""
        <div class="insight-box">
            <h4>🏃 Activity Behaviour</h4>
            <p>{activity_message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # Sleep insight
    # -----------------------------------------------------

    sleep_message = (
        f"Average recorded sleep is approximately {avg_sleep_hours:.1f} hours. "
        "Comparing sleep duration with activity data can help identify "
        "different behaviour patterns among tracked users."
    )

    st.markdown(
        f"""
        <div class="insight-box">
            <h4>😴 Sleep Behaviour</h4>
            <p>{sleep_message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # Weight insight
    # -----------------------------------------------------

    if not filtered_weight.empty:

        avg_bmi = filtered_weight["BMI"].mean()

        weight_message = (
            f"The available weight records show an average BMI of "
            f"{avg_bmi:.1f}. Weight data is available for fewer users "
            "than activity data, so conclusions should be interpreted "
            "with the smaller sample in mind."
        )

    else:

        weight_message = (
            "Weight records are not available for the selected users."
        )


    st.markdown(
        f"""
        <div class="insight-box">
            <h4>⚖️ Weight & BMI</h4>
            <p>{weight_message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # Business recommendations
    # -----------------------------------------------------

    st.markdown(
        "<div class='section-title'>Potential Business Actions</div>",
        unsafe_allow_html=True
    )

    recommendations = [
        "Use personalized activity goals to encourage consistent daily movement.",
        "Combine activity and sleep behaviour to create more meaningful user segments.",
        "Use progress tracking and achievement features to encourage continued engagement.",
        "Monitor users with declining activity patterns and consider targeted engagement messages.",
        "Treat weight/BMI insights separately because the available weight dataset is much smaller."
    ]

    for recommendation in recommendations:

        st.markdown(
            f"""
            <div class="insight-box">
                <p>• {recommendation}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#777777; padding:10px;">
        Fitness & Wellness Analytics | Python • SQL • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
