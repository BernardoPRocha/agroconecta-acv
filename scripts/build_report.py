"""Gera um relatório técnico complementar com métricas e evidências reais.

O documento acadêmico de entrega é mantido separadamente em
``reports/Relatorio_Tecnico_ACV_AgroConecta.pdf``. Este gerador usa
somente os dados presentes no repositório e não sobrescreve a entrega.

Requer: ``pip install -r requirements-report.txt``.
"""

import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Image,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
OUTPUT = REPORTS / "Relatorio_Tecnico_ACV_GERADO.pdf"
VIDEO_URL = "https://www.youtube.com/watch?v=KIRmYhAmrdI"
REPOSITORY_URL = "https://github.com/BernardoPRocha/agroconecta-acv"

DARK_GREEN = colors.HexColor("#19372e")
GREEN = colors.HexColor("#166047")
PALE_GREEN = colors.HexColor("#edf4ef")

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="ACVTitle",
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=30,
        textColor=DARK_GREEN,
        spaceAfter=16,
    )
)
styles.add(
    ParagraphStyle(
        name="ACVHeading",
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=20,
        textColor=GREEN,
        spaceBefore=14,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="ACVBody",
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        textColor=DARK_GREEN,
        spaceAfter=9,
    )
)
styles.add(
    ParagraphStyle(
        name="ACVSmall",
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=DARK_GREEN,
    )
)


def p(value, style="ACVBody"):
    return Paragraph(value, styles[style])


def tabular(rows, widths):
    table = Table(
        [[p(escape(str(value)), "ACVSmall") for value in row] for row in rows],
        colWidths=widths,
        hAlign="LEFT",
        repeatRows=1,
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PALE_GREEN),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#dce6dd")),
            ]
        )
    )
    return table


def add_optional_image(story, image_path, max_width=430, max_height=230):
    """Inclui a figura somente quando seus arquivos estão presentes."""
    if not image_path.exists():
        return False
    image_width, image_height = ImageReader(str(image_path)).getSize()
    scale = min(max_width / image_width, max_height / image_height)
    story.append(Image(str(image_path), image_width * scale, image_height * scale))
    story.append(Spacer(1, 10))
    return True


def page_footer(canvas, document):
    canvas.setStrokeColor(GREEN)
    canvas.line(45, 42, 550, 42)
    canvas.setFillColor(DARK_GREEN)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(45, 28, "AgroConecta | Applied Computer Vision | Global Solution 2026.2")
    canvas.drawRightString(550, 28, str(document.page))


def main():
    metrics = json.loads((REPORTS / "test_metrics.json").read_text(encoding="utf-8"))
    audit = json.loads((REPORTS / "dataset_audit.json").read_text(encoding="utf-8"))
    metadata = json.loads((ROOT / "models/metadata.json").read_text(encoding="utf-8"))
    model_metrics = metrics["metrics"]
    story = []

    story.append(p("GLOBAL SOLUTION 2026.2 · FIAP", "ACVSmall"))
    story.append(Spacer(1, 12))
    story.append(p("AgroConecta — Análise de folhas", "ACVTitle"))
    story.append(
        p(
            "Relatório técnico complementar de visão computacional. "
            "Triagem visual experimental de folhas de tomate com YOLOv8n, "
            "Python e FastAPI."
        )
    )
    story.append(
        tabular(
            [
                ["Integrantes do grupo", "RM"],
                ["Bernardo Rocha", "99209"],
                ["Eric Rodrigues", "550249"],
                ["Renato Izumi", "99242"],
            ],
            [380, 125],
        )
    )
    story.append(p("Escopo", "ACVHeading"))
    story.append(
        p(
            "O detector apresenta caixas ao redor de folhas classificadas como "
            "aparência saudável, possível pinta-preta ou possível requeima. "
            "As detecções não localizam necessariamente cada lesão e não "
            "equivalem a diagnóstico agronômico definitivo."
        )
    )
    story.append(p("Dados e treinamento", "ACVHeading"))
    counts = audit["counts"]
    story.append(
        tabular(
            [
                ["Conjunto", "Imagens"],
                ["Treino", counts["train"]["images"]],
                ["Validação", counts["val"]["images"]],
                ["Teste", counts["test"]["images"]],
            ],
            [380, 125],
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        p(
            f"Modelo: YOLOv8n; épocas concluídas: <b>{metadata['epochs_completed']}</b>; "
            f"resolução: <b>{metadata['imgsz']} px</b>; batch: <b>8</b>; "
            "semente: <b>42</b>; treinamento registrado em CPU. "
            "Fonte: PlantDoc Object Detection Dataset."
        )
    )
    story.append(
        p(
            f"A preparação removeu {len(audit['duplicates_removed'])} imagens "
            "duplicadas ou aproximadamente duplicadas, "
            f"excluiu {len(audit['excluded_mixed'])} imagens com classes fora do escopo "
            "e registrou divergências de anotação."
        )
    )

    story.append(p("Avaliação do modelo", "ACVHeading"))
    names = [
        ("Precisão", "metrics/precision(B)"),
        ("Recall", "metrics/recall(B)"),
        ("mAP@50", "metrics/mAP50(B)"),
        ("mAP@50:95", "metrics/mAP50-95(B)"),
    ]
    story.append(
        tabular(
            [["Métrica", "Conjunto de teste"]]
            + [[label, f"{model_metrics[key] * 100:.1f}%"] for label, key in names],
            [380, 125],
        )
    )
    story.append(Spacer(1, 10))
    story.append(
        p(
            "As métricas descrevem a qualidade de detecção sobre um conjunto de "
            "teste limitado. Os valores não correspondem a uma taxa de acerto "
            "de diagnósticos agrícolas."
        )
    )
    for label, value in metrics["per_class"].items():
        display = {
            "tomate_saudavel": "Aparência saudável",
            "pinta_preta": "Pinta-preta",
            "requeima": "Requeima",
        }.get(label, label)
        story.append(
            p(f"{escape(display)} — mAP@50: {value['map50'] * 100:.1f}%", "ACVSmall")
        )

    story.append(p("Exemplo visual da avaliação", "ACVHeading"))
    image_path = REPORTS / "predictions/c85286e8013a50d23839_prediction.jpg"
    shown = add_optional_image(story, image_path)
    if shown:
        story.append(
            p(
                "Previsão registrada para uma imagem de teste com divergência "
                "entre as classes previstas e a anotação de referência.",
                "ACVSmall",
            )
        )
    else:
        story.append(
            p(
                "As imagens de referência e predição do teste estão armazenadas "
                "em reports/predictions/.",
                "ACVSmall",
            )
        )

    story.append(p("Aplicação e integração", "ACVHeading"))
    story.append(
        p(
            "O servidor FastAPI recebe fotos pelo endpoint POST /api/predict. "
            "A inferência devolve caixas em pixels, categoria, confiança e latência. "
            "A interface também captura quadros da câmera; uploads são "
            "processados em memória. Endpoints auxiliares: /health, /ready e /docs."
        )
    )
    story.append(p("Limitações", "ACVHeading"))
    story.append(
        p(
            "O detector pode confundir doenças e omitir folhas. O conjunto de "
            "teste contém 27 imagens, sem validação agronômica em campo. "
            "A câmera física foi demonstrada com fotografia exibida em outra tela. "
            "Uma imagem sem detecções é inconclusiva, não necessariamente saudável."
        )
    )
    story.append(p("Materiais e referências", "ACVHeading"))
    story.append(
        p(
            f'<link href="{REPOSITORY_URL}" color="#166047">Repositório AgroConecta ACV</link>'
            " — código, testes, pesos e evidências."
        )
    )
    story.append(
        p(f'<link href="{VIDEO_URL}" color="#166047">Vídeo final de demonstração</link>')
    )
    story.append(
        p(
            "Singh et al. (2020). PlantDoc: A Dataset for Visual Plant Disease Detection. "
            "DOI: 10.1145/3371158.3371196. "
            "Ultralytics YOLOv8: docs.ultralytics.com/models/yolov8/."
        )
    )
    story.append(
        p(
            "PlantDoc: licença declarada CC BY 4.0 na origem; verificar direitos "
            "de terceiros para imagens individuais. Ultralytics: obrigações "
            "AGPL-3.0 ou comerciais conforme a forma de distribuição."
        )
    )

    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=(595.28, 841.89),
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=60,
        title="AgroConecta — Relatório técnico ACV (gerado)",
        author="Grupo AgroConecta",
    )
    document.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()
