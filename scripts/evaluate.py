"""Avalia o detector no conjunto de teste reservado do PlantDoc."""

import argparse
import json

from prepare_data import ROOT, refresh_yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()

    import torch
    from ultralytics import YOLO

    torch.set_num_threads(4)
    metadata = json.loads((ROOT / "models/metadata.json").read_text())
    model = YOLO(str(ROOT / "models/best.pt"))
    result = model.val(
        data=str(refresh_yaml(ROOT / "data/tomato")),
        split="test",
        imgsz=metadata["imgsz"],
        device=args.device,
        workers=0,
        batch=8,
        plots=True,
        project=str(ROOT / "runs"),
        name="test",
    )

    per_class = {}
    for index, class_id in enumerate(result.box.ap_class_index):
        values = result.box.class_result(index)
        per_class[model.names[int(class_id)]] = dict(
            zip(
                ("precision", "recall", "map50", "map50_95"),
                map(float, values),
            )
        )

    metrics = {
        "split": "test",
        "model_sha256": metadata["sha256"],
        "metrics": {name: float(value) for name, value in result.results_dict.items()},
        "per_class": per_class,
        "speed_ms_per_image": result.speed,
        "output_directory": result.save_dir.relative_to(ROOT).as_posix(),
        "note": "Offline dataset evaluation; not proof of field reliability or browser FPS.",
    }
    output = ROOT / "reports/test_metrics.json"
    output.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
