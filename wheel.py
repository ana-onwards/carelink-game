"""Spinning wheel component for Streamlit using HTML5 Canvas."""

import streamlit.components.v1 as components
import json


def render_wheel(items: list, target_index: int, wheel_id: str = "wheel", height: int = 520):
    """
    Render a spinning wheel that lands on target_index.
    
    items: list of dicts with 'label' and 'color' keys
    target_index: which item the wheel should land on
    wheel_id: unique ID for this wheel instance
    height: component height in pixels
    """
    items_json = json.dumps(items)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: transparent; 
            display: flex; 
            flex-direction: column;
            align-items: center; 
            justify-content: center;
            min-height: {height - 20}px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            overflow: hidden;
        }}
        .wheel-container {{
            position: relative;
            display: inline-block;
        }}
        canvas {{
            display: block;
        }}
        .pointer {{
            position: absolute;
            top: -8px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 16px solid transparent;
            border-right: 16px solid transparent;
            border-top: 35px solid #D4A056;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.4));
            z-index: 10;
        }}
        .center-circle {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: #1a1a2e;
            border: 3px solid #D4A056;
            z-index: 10;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .spin-btn {{
            display: block;
            margin-top: 20px;
            padding: 14px 48px;
            font-size: 18px;
            font-weight: 700;
            color: #1a1a2e;
            background: linear-gradient(135deg, #D4A056, #E8C47C);
            border: none;
            border-radius: 50px;
            cursor: pointer;
            letter-spacing: 1px;
            text-transform: uppercase;
            box-shadow: 0 4px 15px rgba(212, 160, 86, 0.4);
            transition: all 0.2s;
        }}
        .spin-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(212, 160, 86, 0.6);
        }}
        .spin-btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }}
        .result-banner {{
            margin-top: 16px;
            padding: 12px 24px;
            background: rgba(212, 160, 86, 0.15);
            border: 1px solid #D4A056;
            border-radius: 12px;
            color: #D4A056;
            font-size: 20px;
            font-weight: 700;
            text-align: center;
            opacity: 0;
            transition: opacity 0.5s;
        }}
        .result-banner.show {{
            opacity: 1;
        }}
    </style>
    </head>
    <body>
    <div class="wheel-container">
        <div class="pointer"></div>
        <canvas id="canvas_{wheel_id}" width="380" height="380"></canvas>
        <div class="center-circle"></div>
    </div>
    <button class="spin-btn" id="btn_{wheel_id}" onclick="spinWheel()">SPIN</button>
    <div class="result-banner" id="result_{wheel_id}"></div>

    <script>
    const items = {items_json};
    const targetIndex = {target_index};
    const canvas = document.getElementById('canvas_{wheel_id}');
    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 175;
    const numItems = items.length;
    const arcSize = (2 * Math.PI) / numItems;
    let currentAngle = 0;
    let spinning = false;

    function drawWheel(angle) {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw shadow
        ctx.save();
        ctx.shadowColor = 'rgba(0,0,0,0.3)';
        ctx.shadowBlur = 15;
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius + 2, 0, 2 * Math.PI);
        ctx.fillStyle = '#111';
        ctx.fill();
        ctx.restore();
        
        for (let i = 0; i < numItems; i++) {{
            const startAngle = angle + i * arcSize;
            const endAngle = startAngle + arcSize;
            
            // Segment
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, radius, startAngle, endAngle);
            ctx.closePath();
            ctx.fillStyle = items[i].color;
            ctx.fill();
            
            // Border
            ctx.strokeStyle = 'rgba(255,255,255,0.15)';
            ctx.lineWidth = 2;
            ctx.stroke();
            
            // Label
            ctx.save();
            ctx.translate(centerX, centerY);
            ctx.rotate(startAngle + arcSize / 2);
            ctx.fillStyle = '#FFFFFF';
            ctx.font = 'bold 13px -apple-system, sans-serif';
            ctx.textAlign = 'right';
            ctx.textBaseline = 'middle';
            
            // Text shadow for readability
            ctx.shadowColor = 'rgba(0,0,0,0.6)';
            ctx.shadowBlur = 3;
            ctx.fillText(items[i].label, radius - 18, 0);
            ctx.restore();
        }}
        
        // Outer ring
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius + 2, 0, 2 * Math.PI);
        ctx.strokeStyle = '#D4A056';
        ctx.lineWidth = 3;
        ctx.stroke();
    }}

    function spinWheel() {{
        if (spinning) return;
        spinning = true;
        document.getElementById('btn_{wheel_id}').disabled = true;
        
        // The pointer is at the TOP (12 o'clock = -PI/2)
        // We need the target segment's center to be at that position
        // Segment i center is at: angle + i * arcSize + arcSize/2
        // We want that to equal -PI/2 (mod 2PI)
        // So: finalAngle + targetIndex * arcSize + arcSize/2 = -PI/2 + 2*PI*k
        // finalAngle = -PI/2 - targetIndex * arcSize - arcSize/2 + 2*PI*k
        
        const targetAngle = -Math.PI/2 - targetIndex * arcSize - arcSize/2;
        // Add several full rotations for drama (6-9 full spins)
        const fullSpins = (6 + Math.random() * 3) * 2 * Math.PI;
        const finalAngle = targetAngle + fullSpins;
        
        const duration = 4000 + Math.random() * 1000; // 4-5 seconds
        const startTime = performance.now();
        const startAngle = currentAngle;
        const totalRotation = finalAngle - startAngle;
        
        function easeOutCubic(t) {{
            return 1 - Math.pow(1 - t, 3);
        }}
        
        function animate(now) {{
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = easeOutCubic(progress);
            
            currentAngle = startAngle + totalRotation * eased;
            drawWheel(currentAngle);
            
            if (progress < 1) {{
                requestAnimationFrame(animate);
            }} else {{
                // Done! Show result
                const resultEl = document.getElementById('result_{wheel_id}');
                resultEl.textContent = items[targetIndex].label;
                resultEl.classList.add('show');
                
                // Send result back to Streamlit
                setTimeout(() => {{
                    window.parent.postMessage({{
                        type: 'wheel_result',
                        wheelId: '{wheel_id}',
                        index: targetIndex,
                        label: items[targetIndex].label
                    }}, '*');
                }}, 800);
            }}
        }}
        
        requestAnimationFrame(animate);
    }}

    // Initial draw
    drawWheel(currentAngle);
    </script>
    </body>
    </html>
    """
    components.html(html, height=height, scrolling=False)


def render_card(title: str, subtitle: str, description: str, color: str, card_type: str = "DEPARTMENT"):
    """Render a nice-looking card reveal."""
    html = f"""
    <div style="
        max-width: 420px;
        margin: 20px auto;
        background: linear-gradient(145deg, #16213e, #1a1a2e);
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        border: 1px solid rgba(212, 160, 86, 0.2);
        animation: fadeIn 0.8s ease;
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
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            ">{title}</div>
            {"<div style='font-size: 14px; color: rgba(255,255,255,0.8); margin-top: 4px;'>" + subtitle + "</div>" if subtitle else ""}
        </div>
        <div style="
            padding: 24px;
            color: #E0E0E0;
            font-size: 15px;
            line-height: 1.6;
        ">{description}</div>
    </div>
    <style>
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
    """
    components.html(html, height=380, scrolling=False)
