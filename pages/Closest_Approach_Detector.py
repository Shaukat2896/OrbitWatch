import streamlit as st
from services import asset_utils
from services import data_manager as dm
from services import collision_engine

st.set_page_config(
    page_title="OrbitWatch",
    page_icon="🛰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

asset_utils.set_background("assets/earth_background.jpg")

st.markdown(
    """
    <h1 style='text-align:center; color:white;'>
        Closest Approach Detector
    </h1>
    """,
    unsafe_allow_html=True,
)

# Load dataframe
all_df = dm.load_all_dataframe()
df = dm.load_dataframe(all_df)

with st.container(border=True):

    satellite_name = st.selectbox(
        "Select Satellite",
        df["Satellite Name"].tolist()
    )

    hours = st.number_input(
        "Prediction Window (Hours)",
        min_value=1,
        max_value=168,
        value=1
    )

    predict = st.button(
        "Predict Collision",
        use_container_width=True
    )

if predict:

    # Find NORAD ID
    selected_norad = int(
        df.loc[
            df["Satellite Name"] == satellite_name,
            "NORAD ID"
        ].iloc[0]
    )

    with st.spinner("Checking nearby objects (It may take a few minutes)..."):

        results = collision_engine.closest_objects_detector(
            selected_norad,
            hours
        )
    st.markdown("---")

    st.subheader("Prediction Results")

    if len(results) == 0:

        st.success("No nearby objects found / Unable to locate the object.")

    else:

        for obj in results:

            if obj["Risk"] == "Safe":
                color = "green"
            elif obj["Risk"] == "Low":
                color = "yellow"
            elif obj["Risk"] == "Medium":
                color = "orange"
            else:
                color = "red"

            with st.container(border=True):

                st.markdown(
                    f"### 🛰 {obj['Satellite Name']}"
                )

                c1, c2 = st.columns(2)

                with c1:

                    st.metric(
                        "Minimum Distance",
                        f"{obj['Distance']:.2f} km"
                    )

                    st.write(
                        f"**NORAD ID:** {obj['NORAD']}"
                    )

                with c2:

                    st.markdown(
                        f"**Risk:** :{color}[{obj['Risk']}]"
                    )

                    st.write(
                        f"**Closest Time:** {obj['Time']}"
                    )
st.divider()
st.subheader("Important Note")
st.info("The satellites change paths because of collision risk. So, the maximum chance of getting risk is very low.")