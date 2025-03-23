import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Faculty Productivity Dashboard", page_icon=":globe_with_meridians:", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS ---
custom_css = """
<style>
/* Overall background and font styling */
body {
    background: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Main header styling */
h1, h2, h3, h4, h5 {
    color: #333;
    text-align: center;
    margin-bottom: 20px;
}

/* Tab styling */
.stTabs [data-baseweb=tab] {
    background-color: #ffffff;
    border: none;
    border-bottom: 2px solid #ccc;
    margin-right: 1rem;
    padding: 0.5rem 1rem;
    font-weight: 600;
    color: #333;
}
.stTabs [data-baseweb=tab]:hover {
    background-color: #e0e0e0;
}
.stTabs [data-baseweb=tab][aria-selected="true"] {
    border-bottom: 3px solid #ff4b4b;
    color: #ff4b4b;
}

/* Card styling for profile and metrics */
.card {
    background: #ffffff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    border: 1px solid #ddd;
}
.card-header {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 10px;
    color: #ff4b4b;
    border-bottom: 1px solid #ddd;
    padding-bottom: 10px;
}

/* Button styling */
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 20px;
    font-weight: 600;
    margin-top: 10px;
}
.stButton>button:hover {
    background-color: #e03e3e;
}

/* Chart container styling */
.chart-container {
    background: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    border: 1px solid #ddd;
}

/* Sidebar styling */
.sidebar .sidebar-content {
    background: #ff4b4b;
    color: white;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
}
.sidebar .sidebar-content .stSelectbox, .sidebar .sidebar-content .stSlider {
    color: #333;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

@st.cache_data
def load_data():
    faculty_info = pd.read_csv("data/processed/faculty_info.csv")
    Performance_trends = pd.read_csv("data/processed/Performance_trends.csv")
    Prfess_Development = pd.read_csv("data/processed/Prfess_Development.csv")
    Research_output = pd.read_csv("data/processed/Research_output.csv")
    Self_asses = pd.read_csv("data/processed/Self_asses.csv")
    Service = pd.read_csv("data/processed/Service.csv")
    Teaching_metrics = pd.read_csv("data/processed/Teaching_metrics.csv")
    Workload_and_Resource_Allocation = pd.read_csv("data/processed/Workload_and_Resource_Allocation.csv")
    return faculty_info, Performance_trends, Prfess_Development, Research_output, Self_asses, Service, Teaching_metrics, Workload_and_Resource_Allocation

faculty_info, Performance_trends, Prfess_Development, Research_output, Self_asses, Service, Teaching_metrics, Workload_and_Resource_Allocation = load_data()

# --- Sidebar for Filters ---
with st.sidebar:
    st.markdown("<h2>Filters</h2>", unsafe_allow_html=True)
    selected_department = st.selectbox("Select Department", faculty_info["Department"].unique())
    selected_faculty = st.selectbox("Select Faculty Member",
                                    faculty_info[faculty_info["Department"] == selected_department]
                                    ["Faculty_Name"].unique())

# --- Define Tabs ---
tabs = st.tabs(
    ["Profile", "Teaching Metrics", "Research Output", "Professional Development", "Workload", "Predictive Analysis"]
)

with tabs[0]:
    faculty_data = faculty_info[faculty_info["Faculty_Name"] == selected_faculty].iloc[0]
    performance_data = Performance_trends[Performance_trends["Department"] == faculty_data["Department"]]
    profess_data = Prfess_Development[Prfess_Development["Faculty_Name"] == selected_faculty]
    research_data = Research_output[Research_output["Faculty_Name"] == selected_faculty]
    self_asses_data = Self_asses[Self_asses["Faculty_Name"] == selected_faculty]
    service_data = Service[Service["Faculty_Name"] == selected_faculty]
    teaching_data = Teaching_metrics[Teaching_metrics["Faculty_Name"] == selected_faculty]
    workload_data = Workload_and_Resource_Allocation[Workload_and_Resource_Allocation["Faculty_ID"] == faculty_data["Faculty_ID"]]

     # --- Basic Information ---
    st.markdown("### Basic Information")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("data/processed/logo.jpg", width=150) # Replace with your image path
    with col2:
        st.markdown(f"""
                    <p><strong>Name:</strong> {faculty_data['Faculty_Name']}</p>
                    <p><strong>Department:</strong> {faculty_data['Department']}</p>
                    <p><strong>Designation:</strong> {faculty_data['designation']}</p>
                    <p><strong>Experience:</strong> {faculty_data['experience_years']} years</p>
                    <p><strong>Specialization:</strong> {faculty_data['specialization']}</p>
                """, unsafe_allow_html=True)
    # Calculate Scores
    teaching_score = round(performance_data["Teaching_Score"].mean(), 1)
    research_score = round(performance_data["Research_Score"].mean(), 1)
    service_score = round(performance_data["Service_Score"].mean(), 1)

    # Display the card with performance summary
    # Calculate Scores
    teaching_score = round(performance_data["Teaching_Score"].mean(), 1)
    research_score = round(performance_data["Research_Score"].mean(), 1)
    service_score = round(performance_data["Service_Score"].mean(), 1)

    # Display the card with performance summary
    st.markdown(
        f"""
        <div class='card' style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);'>
            <div class='card-header' style='font-size: 20px; font-weight: bold; margin-bottom: 10px;'>
                Quick Performance Summary
            </div>
            <div class='card-body'>
                <div style="display: flex; justify-content: space-around;">
                    <div style="text-align: center;">
                        <p><b>Teaching Score</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{teaching_score}</p>
                    </div>
                    <div style="text-align: center;">
                        <p><b>Research Score</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{research_score}</p>
                    </div>
                    <div style="text-align: center;">
                        <p><b>Service Score</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{service_score}</p>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Extract workload values
    teaching_hours = workload_data["Teaching_Hours_Per_Week"].values[0]
    research_hours = workload_data["Research_Hours_Per_Week"].values[0]
    admin_hours = workload_data["Administrative_Hours_Per_Week"].values[0]

    # Display the card with workload summary
    st.markdown(
        f"""
        <div class='card' style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);'>
            <div class='card-header' style='font-size: 20px; font-weight: bold; margin-bottom: 10px;'>
                Current Workload Summary
            </div>
            <div class='card-body'>
                <div style="display: flex; justify-content: space-around;">
                    <div style="text-align: center;">
                        <p><b>Teaching Hours/Week</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{teaching_hours}</p>
                    </div>
                    <div style="text-align: center;">
                        <p><b>Research Hours/Week</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{research_hours}</p>
                    </div>
                    <div style="text-align: center;">
                        <p><b>Admin Hours/Week</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{admin_hours}</p>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Latest Achievements & Awards (Inside a Single Card) ---
    if not research_data.empty:
        publications = research_data['Publications_Count'].values[0]
        patents_filed = research_data['Patents_Filed'].values[0]
        patents_granted = research_data['Patents_Granted'].values[0]
    else:
        publications = patents_filed = patents_granted = "No Data"

    st.markdown(
        f"""
        <div class='card' style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; 
                                box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-top: 20px;'>
            <div class='card-header' style='font-size: 20px; font-weight: bold; margin-bottom: 10px;'>
                Latest Achievements & Awards
            </div>
            <div class='card-body' style="font-size: 16px;">
                <ul style="padding-left: 20px;">
                    <li><b>Publications:</b> {publications}</li>
                    <li><b>Patents Filed:</b> {patents_filed}</li>
                    <li><b>Patents Granted:</b> {patents_granted}</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Teaching Metrics Tab
with tabs[1]:
    # st.markdown("<div class='card'>", unsafe_allow_html=True)
    # st.markdown("<div class='card-header'>📚 Teaching Metrics</div>", unsafe_allow_html=True)

    # st.write("teaching_data", teaching_data)  # holder
    # Displaying teaching performance
    if not teaching_data.empty:
        courses_taught = teaching_data["Courses_Taught"].values[0]
        feedback_score = teaching_data["Student_Feedback_Score"].values[0]
        teaching_hours = teaching_data["Teaching_Hours_Per_Week"].values[0]

        st.markdown(
            f"""
            <div class='card' style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 15px;'>
                <div class='card-header' style='font-size: 20px; font-weight: bold; margin-bottom: 10px; text-align: center;'>
                    📊 Teaching Performance
                </div>
                <div class='card-body' style="display: flex; justify-content: space-around; text-align: center;">
                    <div>
                        <p><b>Courses Taught</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{courses_taught}</p>
                    </div>
                    <div>
                        <p><b>Student Feedback Score</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{feedback_score}</p>
                    </div>
                    <div>
                        <p><b>Teaching Hours/Week</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{teaching_hours}</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Alternative Box Plot for Student Feedback Trends
        # Line Chart for Pass Percentage Trends
        st.subheader("📈 Pass Percentage Trends by Class Size")
        fig = px.scatter(
            Teaching_metrics,
            x="Class_Size",
            y="Pass_Percentage",
            color="Department",
            size="Courses_Taught",
            title="Pass Percentage vs Class Size by Department",
            trendline="ols"
        )

        # Customize layout
        fig.update_layout(
            yaxis=dict(title="Pass Percentage", range=[50, 100]),
            xaxis=dict(title="Class Size"),
            template="plotly_dark"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Research Output Tab
with tabs[2]:
    # st.markdown("<div class='card'>", unsafe_allow_html=True)
    # st.markdown("<div class='card-header'>📖 Research Output</div>", unsafe_allow_html=True)

    #st.write("research_data", research_data) #placeholder

    if not research_data.empty:
        publications = research_data["Publications_Count"].values[0]
        patents_filed = research_data["Patents_Filed"].values[0]
        patents_granted = research_data["Patents_Granted"].values[0]

        st.markdown(
            f"""
            <div class='card' style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 15px;'>
                <div class='card-header' style='font-size: 20px; font-weight: bold; margin-bottom: 10px; text-align: center;'>
                    📚 Research Performance
                </div>
                <div class='card-body' style="display: flex; justify-content: space-around; text-align: center;">
                    <div>
                        <p><b>Publications</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{publications}</p>
                    </div>
                    <div>
                        <p><b>Patents Filed</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{patents_filed}</p>
                    </div>
                    <div>
                        <p><b>Patents Granted</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{patents_granted}</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if not research_data.empty:
            research_grants = research_data["Research_Grants_Received"].values[0]

            st.markdown(
                f"""
                <div class='card' style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 15px; text-align: center;'>
                    <div class='card-header' style='font-size: 20px; font-weight: bold; margin-bottom: 10px;'>
                        💰 Research Funding & Grants
                    </div>
                    <div class='card-body'>
                        <p><b>Total Research Grants Received</b></p>
                        <p style="font-size: 24px; font-weight: bold; color: #2E8B57;">${research_grants:,.2f}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Bar chart for research papers over the years
        #st.write("Research_output", Research_output)  # Placeholder

        if not Research_output.empty:
            st.subheader("📊 Research Publications Over the Years")

            # Improved Bar Chart for Yearly Publications
            fig = px.bar(
                Research_output,
                x="Year",
                y="Publications_Count",
                title="Publications Per Year",
                labels={"Publications_Count": "Number of Publications"},
                text=Research_output["Publications_Count"],  # Display numbers on bars
                color="Publications_Count",
                color_continuous_scale="Blues",
                height=500  # Increased height for better visibility
            )

            fig.update_traces(textposition="outside")  # Ensure text is visible outside bars
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Publications Count",
                template="plotly_white"
            )

            # Display Chart
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No research data available for this faculty member.")

        st.markdown("</div>", unsafe_allow_html=True)
# Professional Development Tab
with tabs[3]:
    if not profess_data.empty:
        workshops_attended = profess_data["Workshops_Attended"].values[0]
        certifications_earned = profess_data["Certifications_Earned"].values[0]

        st.markdown(
            f"""
            <div class='card' style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 15px;'>
                <div class='card-header' style='font-size: 20px; font-weight: bold; margin-bottom: 10px; text-align: center;'>
                    🎓 Professional Development
                </div>
                <div class='card-body' style="display: flex; justify-content: space-around; text-align: center;">
                    <div>
                        <p><b>Workshops Attended</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{workshops_attended}</p>
                    </div>
                    <div>
                        <p><b>Certifications Earned</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{certifications_earned}</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Certifications Timeline
        st.subheader("📅 Certifications Earned Over Time")
        fig = px.bar(Prfess_Development, x="Year", y="Faculty_Development_Programs_Attended", title="Certification Growth")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No professional development data available.")

    st.markdown("</div>", unsafe_allow_html=True)

# Workload and Resource Allocation Tab
with tabs[4]:
    # st.markdown("<div class='card'>", unsafe_allow_html=True)
    # st.markdown("<div class='card-header'>⚖️ Workload & Resource Allocation</div>", unsafe_allow_html=True)

    #st.write("workload_data", workload_data)  # Placeholder
    if not workload_data.empty:
        teaching_hours = workload_data["Teaching_Hours_Per_Week"].values[0]
        research_hours = workload_data["Research_Hours_Per_Week"].values[0]
        admin_hours = workload_data["Administrative_Hours_Per_Week"].values[0]
        total_hours = workload_data["Total_Weekly_Hours"].values[0]

        st.markdown(
            f"""
            <div class='card' style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 15px;'>
                <div class='card-header' style='font-size: 20px; font-weight: bold; margin-bottom: 10px; text-align: center;'>
                    ⏳ Workload Summary
                </div>
                <div class='card-body' style="display: flex; justify-content: space-around; text-align: center;">
                    <div>
                        <p><b>Teaching Hours/Week</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{teaching_hours}</p>
                    </div>
                    <div>
                        <p><b>Research Hours/Week</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{research_hours}</p>
                    </div>
                    <div>
                        <p><b>Administrative Hours/Week</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{admin_hours}</p>
                    </div>
                    <div>
                        <p><b>Total Weekly Hours</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{total_hours}</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Bar Chart for Workload Distribution
        st.subheader("📊 Workload Distribution")
        workload_bar = px.bar(
            x=["Teaching", "Research", "Administration"],
            y=[workload_data["Teaching_Hours_Per_Week"].values[0],
               workload_data["Research_Hours_Per_Week"].values[0],
               workload_data["Administrative_Hours_Per_Week"].values[0]],
            labels={"x": "Workload Category", "y": "Hours"},
            title="Workload Breakdown",
            text_auto=True,
            color_discrete_sequence=["#1f77b4"]
        )
        st.plotly_chart(workload_bar, use_container_width=True)

        # Research Funding Gauge Chart
        st.subheader("💰 Research Funding Allocation")
        funding_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=workload_data["Research_Funding_Received"].values[0],
            title={"text": "Research Funding (₹)"},
            gauge={"axis": {"range": [0, max(workload_data["Research_Funding_Received"]) + 5000]}}
        ))
        st.plotly_chart(funding_gauge, use_container_width=True)
    else:
        st.warning("No workload data available.")

    st.markdown("</div>", unsafe_allow_html=True)



# Predictive Analysis Tab
with tabs[5]:
    # st.markdown("<div class='card'>", unsafe_allow_html=True)
    # st.markdown("<div class='card-header'>🔮 Predictive Analysis</div>", unsafe_allow_html=True)

    st.subheader("📉 Predicting Future Performance Trends")
    st.write("This section will include machine learning predictions for faculty productivity.")

    # Placeholder for ML model results
    if not performance_data.empty:
        # Calculate predicted scores using a simple scaling factor
        predicted_teaching_score = round(performance_data["Teaching_Score"].mean() * 1.05, 1)
        predicted_research_score = round(performance_data["Research_Score"].mean() * 1.1, 1)
        predicted_service_score = round(performance_data["Service_Score"].mean() * 1.02, 1)

        # Display the predicted scores inside a styled card
        st.markdown(
            f"""
            <div class='card' style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 15px;'>
                <div class='card-header' style='font-size: 20px; font-weight: bold; margin-bottom: 10px; text-align: center;'>
                    🔮 Model Predicted Score for Next Semester
                </div>
                <div class='card-body' style="display: flex; justify-content: space-around; text-align: center;">
                    <div>
                        <p><b>Predicted Teaching Score</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{predicted_teaching_score}</p>
                    </div>
                    <div>
                        <p><b>Predicted Research Score</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{predicted_research_score}</p>
                    </div>
                    <div>
                        <p><b>Predicted Service Score</b></p>
                        <p style="font-size: 24px; font-weight: bold;">{predicted_service_score}</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ Insufficient data for predictive analysis.")

    st.markdown("</div>", unsafe_allow_html=True)

