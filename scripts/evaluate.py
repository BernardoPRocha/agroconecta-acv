import argparse,json
from prepare_data import ROOT,refresh_yaml

def main():
    p=argparse.ArgumentParser();p.add_argument('--device',default='cpu');args=p.parse_args()
    import torch
    from ultralytics import YOLO
    torch.set_num_threads(4)
    meta=json.loads((ROOT/'models/metadata.json').read_text())
    model=YOLO(str(ROOT/'models/best.pt'))
    m=model.val(data=str(refresh_yaml(ROOT/'data/tomato')),split='test',imgsz=meta['imgsz'],
                device=args.device,workers=0,batch=8,plots=True,project=str(ROOT/'runs'),name='test')
    results={'split':'test','model_sha256':meta['sha256'],'metrics':{k:float(v) for k,v in m.results_dict.items()},
             'per_class':{model.names[int(c)]:dict(zip(['precision','recall','map50','map50_95'],map(float,m.box.class_result(i)))) for i,c in enumerate(m.box.ap_class_index)},
             'speed_ms_per_image':m.speed,'output_directory':str(m.save_dir),
             'note':'Offline dataset evaluation; not proof of field reliability or browser FPS.'}
    (ROOT/'reports/test_metrics.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
