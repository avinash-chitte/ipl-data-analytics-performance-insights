"""
match_predictor.py — IPL Intelligence Hub
Page 6: Live win probability predictor with ML evaluation, feature importance, and model metrics.
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

from src.styles import render_kpi_card, chart_header, section_divider, update_plotly_layout
from src.ml_model import get_trained_model


def render(df: pd.DataFrame, filtered_df: pd.DataFrame):
    """Render the Match Predictor page."""

    st.markdown("""
    <div style="margin-bottom:0.5rem;">
        <h2 style="margin:0; font-weight:800; color:#fafafa;">Match Win Predictor</h2>
        <p style="margin:0; font-size:0.82rem; color:#71717a;">
            ML-powered chase probability engine with model evaluation and feature analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

    section_divider()

    # Train model
    model = get_trained_model(df)

    tab_predict, tab_eval = st.tabs(["🎯 Predict", "📊 Model Evaluation"])

    # ── Tab 1: Interactive Predictor ──
    with tab_predict:
        c_in1, c_in2 = st.columns(2)

        with c_in1:
            target = st.number_input("Target Score", min_value=50, max_value=300, value=180, key="pred_target")
            curr_score = st.number_input("Current Score", min_value=0, max_value=300, value=120, key="pred_score")
            wickets = st.slider("Wickets Lost", 0, 9, 3, key="pred_wkts")

        with c_in2:
            overs = st.slider("Overs Bowled", 0.0, 19.5, 14.0, step=0.1, key="pred_overs")
            o_int = int(overs)
            b_int = min(int((overs - o_int) * 10), 6)
            balls_remaining = max(120 - (o_int * 6 + b_int), 0)
            runs_needed = max(target - curr_score, 0)
            rrr = (runs_needed * 6) / max(balls_remaining, 1)
            balls_played = 120 - balls_remaining
            crr = (curr_score * 6) / max(balls_played, 1)

            st.markdown(f"""
            <div style="background:#111114; border:1px solid #1e1e24; border-radius:10px;
                        padding:1rem 1.2rem; margin-top:0.5rem;">
                <div style="display:flex; justify-content:space-between; gap:1rem;">
                    <div>
                        <span style="color:#71717a; font-size:0.72rem; text-transform:uppercase; font-weight:600;">
                            Balls Left</span><br>
                        <span style="color:#fafafa; font-size:1.3rem; font-weight:700;">{balls_remaining}</span>
                    </div>
                    <div>
                        <span style="color:#71717a; font-size:0.72rem; text-transform:uppercase; font-weight:600;">
                            Runs Needed</span><br>
                        <span style="color:#fafafa; font-size:1.3rem; font-weight:700;">{runs_needed}</span>
                    </div>
                    <div>
                        <span style="color:#71717a; font-size:0.72rem; text-transform:uppercase; font-weight:600;">
                            Req. RR</span><br>
                        <span style="color:#fafafa; font-size:1.3rem; font-weight:700;">{rrr:.2f}</span>
                    </div>
                    <div>
                        <span style="color:#71717a; font-size:0.72rem; text-transform:uppercase; font-weight:600;">
                            Curr. RR</span><br>
                        <span style="color:#fafafa; font-size:1.3rem; font-weight:700;">{crr:.2f}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        predict_btn = st.button("🚀  Calculate Win Probability", use_container_width=True, type="primary")

        if predict_btn or "last_pred" in st.session_state:
            result = model.predict_live(runs_needed, balls_remaining, wickets, rrr, crr)
            st.session_state.last_pred = result
            prob = result["probability"]

            section_divider()

            r1, r2 = st.columns([1, 1])

            with r1:
                # Probability display card
                prob_color = "#22c55e" if prob >= 0.6 else ("#f59e0b" if prob >= 0.4 else "#ef4444")
                conf_color = {"High": "#22c55e", "Medium": "#f59e0b", "Low": "#ef4444"}.get(
                    result["confidence"], "#71717a"
                )
                st.markdown(f"""
                <div style="text-align:center; padding:2rem; background:#111114;
                            border:1px solid #1e1e24; border-radius:12px;">
                    <div style="font-size:0.75rem; color:#71717a; font-weight:600;
                                text-transform:uppercase; letter-spacing:0.06em;">
                        Chasing Team Win Probability
                    </div>
                    <div style="font-size:4rem; font-weight:900; color:{prob_color};
                                letter-spacing:-0.03em; margin:0.3rem 0;">
                        {prob*100:.1f}%
                    </div>
                    <div style="display:inline-flex; gap:0.8rem; align-items:center;">
                        <span style="background:rgba(37,99,235,0.12); color:#2563eb;
                                     padding:4px 12px; border-radius:6px; font-size:0.78rem; font-weight:600;">
                            {result['situation']}
                        </span>
                        <span style="background:rgba(255,255,255,0.05); color:{conf_color};
                                     padding:4px 12px; border-radius:6px; font-size:0.78rem; font-weight:600;">
                            Confidence: {result['confidence']}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with r2:
                # Gauge chart
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=prob * 100,
                    number=dict(suffix="%", font=dict(size=36, color="#fafafa")),
                    domain=dict(x=[0, 1], y=[0, 1]),
                    gauge=dict(
                        axis=dict(range=[0, 100], tickfont=dict(color="#71717a")),
                        bar=dict(color="#2563eb"),
                        bgcolor="#111114",
                        bordercolor="#1e1e24",
                        steps=[
                            dict(range=[0, 35], color="rgba(239,68,68,0.12)"),
                            dict(range=[35, 65], color="rgba(245,158,11,0.12)"),
                            dict(range=[65, 100], color="rgba(34,197,94,0.12)"),
                        ],
                    ),
                ))
                fig_gauge.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter", color="#fafafa"),
                    height=240,
                    margin=dict(l=30, r=30, t=30, b=10),
                )
                st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

    # ── Tab 2: Model Evaluation ──
    with tab_eval:
        metrics = model.metrics

        # Metric KPIs
        mk1, mk2, mk3, mk4, mk5 = st.columns(5)
        with mk1:
            render_kpi_card("Accuracy", f"{metrics.get('accuracy', 0)}%")
        with mk2:
            render_kpi_card("Precision", f"{metrics.get('precision', 0)}%")
        with mk3:
            render_kpi_card("Recall", f"{metrics.get('recall', 0)}%")
        with mk4:
            render_kpi_card("F1 Score", f"{metrics.get('f1', 0)}%")
        with mk5:
            render_kpi_card("ROC-AUC", f"{metrics.get('roc_auc', 0):.4f}",
                            f"{metrics.get('train_size', 0):,} train · {metrics.get('test_size', 0):,} test",
                            "neutral")

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        c_roc, c_fi = st.columns(2)

        # ROC Curve
        with c_roc:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            chart_header("ROC Curve", "Receiver Operating Characteristic — model discrimination ability")

            roc = model.roc_data
            fig_roc = go.Figure()
            fig_roc.add_trace(go.Scatter(
                x=roc["fpr"], y=roc["tpr"],
                mode="lines", name=f"AUC = {metrics.get('roc_auc', 0):.4f}",
                line=dict(color="#2563eb", width=2.5),
                fill="tozeroy", fillcolor="rgba(37,99,235,0.08)",
            ))
            fig_roc.add_trace(go.Scatter(
                x=[0, 1], y=[0, 1],
                mode="lines", name="Random",
                line=dict(color="#71717a", width=1, dash="dash"),
            ))
            update_plotly_layout(
                fig_roc, height=380,
                xaxis_title="False Positive Rate",
                yaxis_title="True Positive Rate",
                legend=dict(x=0.55, y=0.1),
            )
            st.plotly_chart(fig_roc, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

        # Feature Importance
        with c_fi:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            chart_header("Feature Importance", "Model coefficient magnitudes — which factors matter most")

            importance = model.get_feature_importance()
            if len(importance) > 0:
                colors = ["#22c55e" if c > 0 else "#ef4444" for c in importance["Coefficient"]]
                fig_fi = go.Figure()
                fig_fi.add_trace(go.Bar(
                    x=importance["Abs_Importance"],
                    y=importance["Label"],
                    orientation="h",
                    marker_color=colors,
                    marker_cornerradius=4,
                    text=importance["Coefficient"].round(3),
                    textposition="outside",
                    textfont=dict(size=11, color="#a1a1aa"),
                ))
                update_plotly_layout(fig_fi, height=380, xaxis_title="|Coefficient|")
                st.plotly_chart(fig_fi, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

        # Confusion Matrix
        if hasattr(model, "conf_matrix"):
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            chart_header("Confusion Matrix", "Prediction accuracy breakdown on test set (2023-2025)")

            cm = np.array(model.conf_matrix)
            labels = ["Chase Lost", "Chase Won"]

            fig_cm = go.Figure(data=go.Heatmap(
                z=cm, x=labels, y=labels,
                colorscale=[[0, "#0c0c0f"], [1, "#2563eb"]],
                text=cm, texttemplate="%{text}",
                textfont=dict(size=16, color="#fafafa"),
                showscale=False,
                hovertemplate="Actual: %{y}<br>Predicted: %{x}<br>Count: %{z}<extra></extra>",
            ))
            update_plotly_layout(
                fig_cm, height=350,
                xaxis_title="Predicted",
                yaxis_title="Actual",
                yaxis=dict(autorange="reversed"),
            )
            st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)
