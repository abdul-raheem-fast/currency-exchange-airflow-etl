from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).parent
OUTPUT = ROOT / "Currency_Exchange_Airflow_ETL_Report.pdf"


def add_page_number(canvas, document):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 0.4 * inch, f"Page {document.page}")
    canvas.restoreState()


def scaled_image(path, max_width=7.0 * inch, max_height=5.0 * inch):
    image = Image(str(path))
    scale = min(max_width / image.imageWidth, max_height / image.imageHeight)
    image.drawWidth = image.imageWidth * scale
    image.drawHeight = image.imageHeight * scale
    return image


def build_report():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleCenter",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=20,
            leading=25,
            textColor=colors.HexColor("#17365D"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubtitleCenter",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontSize=12,
            leading=18,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading2"],
            textColor=colors.HexColor("#17365D"),
            spaceBefore=12,
            spaceAfter=6,
        )
    )

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
        title="Currency Exchange Airflow ETL Pipeline",
        author="M. Abdul Raheem",
    )

    story = [
        Spacer(1, 0.45 * inch),
        Paragraph("Building Airflow ETL Pipeline", styles["TitleCenter"]),
        Spacer(1, 0.15 * inch),
        Paragraph("Currency Exchange Rates to MongoDB", styles["SubtitleCenter"]),
        Spacer(1, 0.45 * inch),
        Table(
            [
                ["Name", "M. Abdul Raheem"],
                ["Roll No.", "23L-0588"],
                ["Section", "BCS-7A"],
                ["Repository", "github.com/abdul-raheem-fast/currency-exchange-airflow-etl"],
            ],
            colWidths=[1.35 * inch, 5.65 * inch],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#D9EAF7")),
                    ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#17365D")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.grey),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("PADDING", (0, 0), (-1, -1), 8),
                ]
            ),
        ),
        Spacer(1, 0.35 * inch),
        Paragraph("1. Objective", styles["Section"]),
        Paragraph(
            "The project implements a daily Apache Airflow ETL pipeline that "
            "extracts EUR exchange rates from the Frankfurter API, transforms "
            "the response into the required document schema, and loads the "
            "records into MongoDB.",
            styles["BodyText"],
        ),
        Paragraph("2. Pipeline Implementation", styles["Section"]),
        Table(
            [
                ["Task", "Implementation"],
                ["Extract", "Calls Frankfurter API for USD, GBP, and JPY; pushes raw_rates through named XCom."],
                ["Transform", "Creates one document per currency with base, target, rate, date, source, and retrieval timestamp."],
                ["Load", "Reads transformed_rates through named XCom and inserts documents into currency_db.exchange_rates."],
            ],
            colWidths=[1.1 * inch, 5.9 * inch],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("PADDING", (0, 0), (-1, -1), 7),
                ]
            ),
        ),
        Paragraph("Task dependency: extract >> transform >> load", styles["BodyText"]),
        Paragraph("3. Transformed Data Schema", styles["Section"]),
        Paragraph(
            '<font name="Courier">{"base_currency": "EUR", "target_currency": "USD", '
            '"exchange_rate": 1.15, "rate_date": "2026-11-04", '
            '"source": "Frankfurter API", "retrieved_at": "2026-11-05T07:15:00"}</font>',
            styles["BodyText"],
        ),
        Paragraph("4. Infrastructure", styles["Section"]),
        Paragraph(
            "The Astro Airflow project includes MongoDB 7.0 and Mongo Express "
            "Docker services. MongoDB uses the persistent mongo_data volume. "
            "Both services are connected to the Airflow network, and Mongo "
            "Express is available on port 8081. Docker image metadata labels "
            "include maintainer, description, and version.",
            styles["BodyText"],
        ),
        Paragraph("5. Requirements Checklist", styles["Section"]),
        Table(
            [
                ["Requirement", "Status"],
                ["Frankfurter API extraction", "Completed"],
                ["Three Airflow tasks", "Completed"],
                ["Named XCom transfer", "Completed"],
                ["Transformation schema", "Completed"],
                ["MongoDB load", "Completed"],
                ["Mongo Express service", "Completed"],
                ["Docker networking and persistent storage", "Completed"],
                ["GitHub repository", "Completed"],
            ],
            colWidths=[5.7 * inch, 1.3 * inch],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.grey),
                    ("TEXTCOLOR", (1, 1), (1, -1), colors.HexColor("#087F23")),
                    ("ALIGN", (1, 1), (1, -1), "CENTER"),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]
            ),
        ),
        PageBreak(),
        Paragraph("6. Runtime Evidence: Airflow", styles["Section"]),
        Paragraph(
            "The Airflow grid confirms one successful DAG run and three successful tasks.",
            styles["BodyText"],
        ),
        Spacer(1, 0.15 * inch),
        scaled_image(ROOT / "airflow-success.png"),
        PageBreak(),
        Paragraph("7. Runtime Evidence: Mongo Express", styles["Section"]),
        Paragraph(
            "Mongo Express confirms that the exchange_rates collection contains "
            "the transformed EUR to GBP, JPY, and USD documents.",
            styles["BodyText"],
        ),
        Spacer(1, 0.15 * inch),
        scaled_image(ROOT / "mongodb-records.png"),
        Paragraph("8. Submission Items", styles["Section"]),
        Paragraph(
            "Submit this PDF report, the GitHub repository link, and the project "
            "source code. The repository contains the DAG, Docker configuration, "
            "tests, README, and report source.",
            styles["BodyText"],
        ),
    ]

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(OUTPUT)


if __name__ == "__main__":
    build_report()
