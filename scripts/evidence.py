"""Registra previsões e audita correspondências no conjunto de teste PlantDoc.

A auditoria usa confiança 0,4, IoU 0,5 e pareamento guloso por classe.
Essas contagens não substituem as métricas mAP calculadas na avaliação.
"""

import json
import time
from pathlib import Path

from PIL import Image, ImageDraw

from prepare_data import NAMES, ROOT


def iou(a, b):
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])
    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    union = max(1e-9, area_a + area_b - intersection)
    return intersection / union


def main():
    import torch
    from ultralytics import YOLO

    torch.set_num_threads(4)
    model = YOLO(str(ROOT / "models/best.pt"))
    metadata = json.loads((ROOT / "models/metadata.json").read_text())
    manifest = json.loads((ROOT / "data/tomato/manifest.json").read_text())
    test_items = [item for item in manifest["items"] if item["split"] == "test"]

    output_dir = ROOT / "reports/predictions"
    output_dir.mkdir(parents=True, exist_ok=True)
    audit = []

    for item in test_items:
        image_path = ROOT / "data/tomato/images/test" / (item["key"] + ".jpg")
        with Image.open(image_path) as image:
            width, height = image.size

        started = time.perf_counter()
        result = model.predict(
            str(image_path),
            imgsz=metadata["imgsz"],
            conf=0.4,
            device="cpu",
            verbose=False,
        )[0]
        elapsed_ms = (time.perf_counter() - started) * 1000

        predictions = [
            {
                "class_id": int(box.cls.item()),
                "confidence": float(box.conf.item()),
                "bbox": box.xyxy[0].tolist(),
            }
            for box in result.boxes
        ]
        reference = [
            {
                "class_id": box[0],
                "bbox": [
                    (box[1] - box[3] / 2) * width,
                    (box[2] - box[4] / 2) * height,
                    (box[1] + box[3] / 2) * width,
                    (box[2] + box[4] / 2) * height,
                ],
            }
            for box in item["boxes"]
        ]

        matched = set()
        true_positives = 0
        for predicted in sorted(predictions, key=lambda row: -row["confidence"]):
            candidates = [
                (iou(predicted["bbox"], truth["bbox"]), index)
                for index, truth in enumerate(reference)
                if index not in matched and predicted["class_id"] == truth["class_id"]
            ]
            overlap, index = max(candidates, default=(0, -1))
            if overlap >= 0.5:
                matched.add(index)
                true_positives += 1

        false_positives = len(predictions) - true_positives
        false_negatives = len(reference) - true_positives

        result.save(filename=str(output_dir / f"{item['key']}_prediction.jpg"))
        with Image.open(image_path) as image:
            image = image.convert("RGB")
            drawing = ImageDraw.Draw(image)
            for truth in reference:
                drawing.rectangle(truth["bbox"], outline="blue", width=3)
                drawing.text(
                    (truth["bbox"][0], truth["bbox"][1]),
                    NAMES[truth["class_id"]],
                    fill="blue",
                )
            image.save(output_dir / f"{item['key']}_ground_truth.jpg")

        audit.append(
            {
                "image": f"{item['key']}.jpg",
                "original_filename": item["source_name"],
                "tp": true_positives,
                "fp": false_positives,
                "fn": false_negatives,
                "latency_ms": elapsed_ms,
                "ground_truth": reference,
                "predictions": predictions,
            }
        )

    summary = {
        "confidence": 0.4,
        "iou": 0.5,
        "note": "Class-aware greedy matching; not the mAP calculation.",
        "model_sha256": metadata["sha256"],
        "tp": sum(row["tp"] for row in audit),
        "fp": sum(row["fp"] for row in audit),
        "fn": sum(row["fn"] for row in audit),
        "images": audit,
    }
    (ROOT / "reports/prediction_audit.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    worst_cases = sorted(
        (row for row in audit if row["fp"] + row["fn"] > 0),
        key=lambda row: -(row["fp"] + row["fn"]),
    )[:5]

    sections = [
        "# Auditoria automática de erros no teste",
        "",
        "Critérios: confiança 0,4 e IoU 0,5, com pareamento por classe. "
        "TP, FP e FN são relativos às anotações, que podem conter omissões. "
        "A análise visual dos casos documentados está em `reports/REVISAO_ERROS.md`.",
        "",
    ]
    for number, case in enumerate(worst_cases, 1):
        sections.extend(
            [
                f"## Caso {number}: {case['original_filename']}",
                "",
                f"Arquivo: `{case['image']}`. "
                f"TP={case['tp']}; FP={case['fp']}; FN={case['fn']}.",
                "",
                "As caixas e classes previstas não correspondem integralmente às anotações. "
                "Referência e predição em `reports/predictions/`. "
                "Escala, iluminação e anotações incompletas são hipóteses, "
                "não causas comprovadas.",
                "",
            ]
        )

    (ROOT / "reports/ERROS_REAIS.md").write_text(
        "\n".join(sections), encoding="utf-8"
    )
    print({name: summary[name] for name in ("tp", "fp", "fn")})


if __name__ == "__main__":
    main()
