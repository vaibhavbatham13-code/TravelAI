from email.utils import collapse_rfc2231_value

import streamlit as st
from script4  import app as travel_app
#====================
# PAGE CONFIG
# ====================

st.set_page_config(
    page_title="TravelAI  |Personal Travel Planner", page_icon="🛫",  layout="wide",initial_sidebar_state="collapsed")

# =====================
# PROFESSIONAL UI STYLE
# =====================

st.markdown("""
<style>
.main {
padding-top: 1rem;}
.hero {
padding: 2.2rem;
border-radius: 20px;
background: linear-gradient(135deg,#Of172a, #1e3a5f);
color: white;
margin-bottom: 2rem;
}
.hero1 {
front-size: 42px;
margin-bottom: 8px;
}

.hero p{
font-size: 18px;
opacity: 0.85;
}

.section-title {
font-size: 25px;
font-weight: 700;
margin-top: 20px;
margin-bottom: 15px;
}

.info-card {
padding: 20px;
border-radius: 16px;
background: rgba(128,128,128,0.8);
border: 1px solid rgba(128,128,128,0.2);
margin-bottom: 15px;
}

.result-card {
padding: 24px;
border-radius: 18px;
background: rgba(128,128,128,0.7);
border: 1px solid rgba(128,128,128,0.18);
margin-bottom: 20px;
}

.badge {
display:
inline-block;
padding: 6px 12 px;
border-radius: 20px;
background: rgba(59,130,246,0.15);
margin-right:6px;
margin-bottom:6px;
font-size:14px;
}

div.stButton > button {
width: 100%;
border-radius: 12px;
height: 3.2em;
font-size: 17px;
font--weight: 600;
}

</style>
""", unsafe_allow_html=True)

#===========
# HERO
# ============

st.markdown("""<div class="hero">
<h1> TravelAI</h1>
<p> Plan smarter with multiple AI agents working together to create your destination, itinerary, weather and budget plan.
</p>

</div>
""", unsafe_allow_html=True)

#==============
# TRIP INPUT
#===============

st.markdown('<div class="section-title"> Plan your Trip</div>',
            unsafe_allow_html=True)

destination = st.text_input("Destination",
                            placeholder="Example: Goa, Manali, Jaipur..")

col1, col2 = st.columns(2)

with col1:
    days = st.number_input("Number of days",
                       min_value=1,
                       max_value=30,
                       value=4)

with col2:
    budget = st.number_input("Total budget(rs)",
                              min_value=1000,
                              max_value=500000,
                              value=10000,
                              step=1000)


#===========
# PERSONALIZATION
#==============

st.markdown( '<div class="section-title">Personalize Your Trip</div>',unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    travel_style = st.selectbox(
        "Travel style",
        ["Budget",
         "Moderate",
         "Luxury",
         "Adventure",
         "Relaxed"]
    )

with col4:
    preference = st.multiselect("What do you enjoy?",
                                ["Beaches",
                                 "Nature",
                                 "History & Culture",
                                 "Food",
                                 "Adventure",
                                 "Shopping",
                                 "Photography",
                                 "Nightlife"],
                                default=["Nature"]
                                )
# ==============
# TRIP SUMMARY
# ===========

if destination:
    st.markdown('<div class="section-title"> Trip Summary</div>',
                unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Destination", destination)
    c2.metric("Duration",f"{days} days")
    c3.metric("Budget",f"{budget:,}")
    c4.metric("Style",travel_style)

#===========
# GENERATE PLAN
#=============

st.markdown("")
result = {}
if st.button("Generate My Personalized Travel Plan",
             use_container_width=True):

    if not destination:
        st.warning("Please enter a destination first.")

    else:
        with st.spinner("AI agents are collaborating to create your personalized trip..."):
            try:
                initial_state = {
                    "destination": destination,
                    "days" : int(days),
                    "budget": int(budget),
                    "travel_style": travel_style,
                    "preferences": preference,
                    "interests": preference,
                    "destination_plan": "",
                    "itinerary_plan": "",
                    "budget_plan": "",
                    "weather_plan": "",

                }

                result = travel_app.invoke(initial_state)
                st.success("Your personalized travel plan is ready!")

            except Exception as e:
                st.error(f"Something went wrong: {e}")

#======================
# RESULTS
#=============

st.markdown("___")
st.markdown(
    f"""<div class="result-card">
<h2> {destination} Travel Plan</h2>
<p>

<b> {days} days</b>.
<b>{budget:,}</b>.
<b>{travel_style}</b>
</p>
</div>
""",
    unsafe_allow_html=True
)
# PERSONALIZED BADGES
if preference:
    st.markdown("### Your interests")
    for p in preference:
        st.write(f" {p}")

#=============
# WEATHER
#===============

with st.expander("Weather & Location", expanded=True):
    st.write(
        result.get(
            "weather",
            "Weather information not available."
        )
    )
#============
# DESTINATION
#================

with st.expander (
    "Destinations & Attractions",
    expanded=True
):
    st.write(result.get("destination_plan",
                        "Destination information not available."
                        ))

#=============
# ITINERARY
# ===============
    st.write(
    result.get(
        "itinerary_plan",
        "itinerary information not available."
    ))
#===========
# BUDGET
# =========

with st.expander(
    "Budget Plan", expanded=True
):
    st.write(
        result.get(
            "budget_plan",
            "Budget information not available."
        )
    )

#============
# FINAL PLAN
#=============

st.markdown("---")
st.markdown(
    '<div class="section-title">Final Travel Plan</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="result-card">',
            unsafe_allow_html=True
            )


st.write(result.get("final_plan",
                    "Final travel plan not available."))

st.markdown("</div>",
            unsafe_allow_html=True)



#===========
# FOOTER
#==========

st.markdown("---")

st.caption(
    " Powered by LangGraph + Llama 3.2 | "
    "Multi_Agents AI Travel Planning System")
