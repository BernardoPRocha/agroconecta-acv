import argparse, json, shutil, hashlib
from pathlib import Path
from prepare_data import ROOT, NAMES, refresh_yaml

def main():
    p=argparse.ArgumentParser(); p.add_argument('--epochs',type=int,default=60)
    p.add_argument('--imgsz',type=int,default=640); p.add_argument('--batch',type=int,default=8)
    p.add_argument('--device',default='cpu'); p.add_argument('--name',default='tomato')
    p.add_argument('--threads',type=int,default=4); args=p.parse_args()
    import torch
    from ultralytics import YOLO
    torch.set_num_threads(args.threads)
    data=refresh_yaml(ROOT/'data/tomato')
    model=YOLO('yolov8n.pt')
    model.train(data=str(data),epochs=args.epochs,imgsz=args.imgsz,batch=args.batch,
                device=args.device,workers=0,seed=42,deterministic=True,patience=15,
                project=str(ROOT/'runs'),name=args.name,exist_ok=False,plots=True,
                close_mosaic=5,amp=False)
    best=Path(model.trainer.best)
    if not best.exists(): raise RuntimeError('Training did not produce best.pt')
    shutil.copy2(best,ROOT/'models/best.pt')
    meta={'classes':NAMES,'imgsz':args.imgsz,'epochs_requested':args.epochs,'epochs_completed':len((best.parent.parent/'results.csv').read_text().splitlines())-1,
          'source_run':str(best.parent.parent),'sha256':hashlib.sha256(best.read_bytes()).hexdigest(),
          'status':'trained_not_field_validated'}
    (ROOT/'models/metadata.json').write_text(json.dumps(meta,indent=2))
    print('Model saved to models/best.pt. Run scripts/evaluate.py next.')

if __name__=='__main__': main()
