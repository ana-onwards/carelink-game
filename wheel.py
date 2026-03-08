"""Card reveal components for Streamlit - dramatic card flip, no wheel."""

import streamlit.components.v1 as components


def render_card(title: str, subtitle: str, description: str, color: str, card_type: str = "DEPARTMENT"):
    """Render a card with a reveal animation."""
    html = f"""
    <div style="
        max-width: 420px;
        margin: 16px auto;
        background: #FFFFFF;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.06);
        animation: cardReveal 0.6s ease;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    ">
        <div style="
            background: {color};
            padding: 20px;
            text-align: center;
        ">
            <div style="
                font-size: 10px;
                letter-spacing: 2px;
                color: rgba(255,255,255,0.7);
                margin-bottom: 6px;
                text-transform: uppercase;
            ">{card_type} ROLE</div>
            <div style="
                font-size: 26px;
                font-weight: 800;
                color: white;
                text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            ">{title}</div>
            {"<div style='font-size: 14px; color: rgba(255,255,255,0.8); margin-top: 4px;'>" + subtitle + "</div>" if subtitle else ""}
        </div>
        <div style="
            padding: 24px;
            color: #3D3929;
            font-size: 15px;
            line-height: 1.6;
        ">{description}</div>
    </div>
    <style>
        @keyframes cardReveal {{
            0% {{ opacity: 0; transform: scale(0.9) translateY(20px); }}
            50% {{ opacity: 1; transform: scale(1.02) translateY(-4px); }}
            100% {{ opacity: 1; transform: scale(1) translateY(0); }}
        }}
    </style>
    """
    components.html(html, height=350, scrolling=True)
