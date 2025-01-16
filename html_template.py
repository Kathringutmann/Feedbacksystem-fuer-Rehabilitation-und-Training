def generate_html(knee_angle):
    """Generiert das HTML für die Anzeige des Kniegelenkswinkels."""
    return f"""
    <html>
    <head>
        <meta http-equiv="refresh" content="1">
        <style>
            body {{
                font-family: "Times New Roman", Times, serif;
                text-align: center;
                background-color: black;
                color: white;
            }}
            h1 {{
                color: white;
            }}
            .measurement {{
                margin: 20px;
                padding: 15px;
                background-color: black;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(255, 255, 255, 0.1);
            }}
            .angle {{
                font-size: 240px; /* Große Schrift für den Winkel */
                color: red;
                font-weight: bold;
            }}
            .unit {{
                font-size: 24px; /* Standardgröße für "Grad" */
                color: white;
                font-weight: normal;
            }}
        </style>
    </head>
    <body>
        <h1>Feedbacksystem fuer Rehabilitation und Training</h1>

        <div class="measurement">
            <h2>Kniegelenkswinkel:</h2>
            <!-- Große Zahl für den Winkel -->
            <div class="angle">{knee_angle:.1f}</div>
            <!-- Kleineres "Grad" ausgeschrieben -->
            <div class="unit">Grad</div>
        </div>
    </body>
    </html>
    """
