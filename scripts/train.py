"""Treinamento YOLO para o recorte de folhas de tomate do PlantDoc."""

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from prepare_data import NAMES, ROOT, refresh_yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=60)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--name", default="tomato")
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()

    import torch
    from ultralytics import YOLO

    torch.set_num_threads(args.threads)
    dataset_yaml = refresh_yaml(ROOT / "data/tomato")
    model = YOLO("yolov8n.pt")
    model.train(
        data=str(dataset_yaml),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        workers=0,
        seed=42,
        deterministic=True,
        patience=15,
        project=str(ROOT / "runs"),
        name=args.name,
        exist_ok=False,
        plots=True,
        close_mosaic=5,
        amp=False,
    )

    checkpoint = Path(model.trainer.best)
    if not checkpoint.exists():
        raise RuntimeError("Training did not produce best.pt")

    destination = ROOT / "models/best.pt"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(checkpoint, destination)
    source_run = checkpoint.parent.parent
    results = source_run / "results.csv"
    epochs_completed = len(results.read_text().splitlines()) - 1
    metadata = {
        "classes": NAMES,
        "imgsz": args.imgsz,
        "epochs_requested": args.epochs,
        "epochs_completed": epochs_completed,
        "source_run": source_run.relative_to(ROOT).as_posix(),
        "sha256": hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
        "status": "trained_not_field_validated",
    }
    (ROOT / "models/metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("Model saved to models/best.pt. Run scripts/evaluate.py next.")


if __name__ == "__main__":
    main()
