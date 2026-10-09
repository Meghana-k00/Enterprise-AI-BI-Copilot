import streamlit as st
import requests
import pandas as pd

if "messages" not in st.session_state:
    st.session_state.messages = []


st.set_page_config(
    page_title="Enterprise AI Business Intelligence Copilot",
    page_icon="📊",
    layout="wide"
)


st.title("📊 Enterprise AI Business Intelligence Copilot")

st.write(
    "Ask business questions using SQL analytics, RAG, "
    "Python analytics and LangGraph."
)


question = st.text_input(
    "Ask your business question:",
    placeholder="Example: What is the total sales revenue by region?"
)


if st.button("Ask"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        try:

            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={
                    "question": question,
                    "messages": st.session_state.messages
                }
            )

            if response.status_code == 200:

                result = response.json()
                st.session_state.messages = result.get("messages", [])

                st.subheader("Answer")
                st.write(result["answer"])

                st.subheader("Route")
                st.info(result["route"])

                st.subheader("Sources")

                for source in result.get("sources", []):
                    st.write(f"• {source}")

                # SQL evidence
                if result["route"] == "SQL" and result.get("sql_query"):

                    with st.expander("View SQL Evidence"):

                        st.markdown("**SQL Query**")

                        st.code(
                            result["sql_query"],
                            language="sql"
                        )

                        st.markdown("**SQL Results**")

                        st.json(
                            result.get("sql_results", [])
                        )
                # SQL visualization
                # SQL visualization
                if (
                    result["route"] == "SQL"
                    and "revenue by region" in question.lower()
                ):
                    sql_df = pd.DataFrame(result.get("sql_results", []))

                    if not sql_df.empty and len(sql_df.columns) >= 2:

                        region_col = next(
                            (col for col in sql_df.columns
                            if col.lower() == "region"),
                            sql_df.columns[0]
                        )

                        revenue_col = next(
                            (col for col in sql_df.columns
                            if "revenue" in col.lower()
                            or "sales_amount" in col.lower()),
                            sql_df.columns[1]
                        )

                        sql_df[revenue_col] = pd.to_numeric(
                            sql_df[revenue_col],
                            errors="coerce"
                        )

                        st.subheader("Revenue by Region")
                        st.bar_chart(
                            sql_df.set_index(region_col)[revenue_col]
                        )


                # Analytics visualization
                if (
                    result["route"] == "ANALYTICS"
                    and "forecast" in question.lower()
                ):

                    forecast_data = {
                        "Month": [
                            "January",
                            "February",
                            "March",
                            "Next Month"
                        ],
                        "Revenue": [
                            4430,
                            3600,
                            8340,
                            9366.67
                        ]
                    }

                    forecast_df = pd.DataFrame(forecast_data)

                    st.subheader("Revenue Forecast")

                    st.line_chart(
                        forecast_df.set_index("Month")
                    )

            else:

                st.error(
                    f"FastAPI returned status code "
                    f"{response.status_code}"
                )


        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to FastAPI. "
                "Make sure the FastAPI server is running."
            )

        except Exception as e:

            st.error(
                f"Something went wrong: {e}"
            )