"""Save genuine test predictions and an automatic FP/FN audit at conf=.4, IoU=.5."""
import json,time
from pathlib import Path
from PIL import Image,ImageDraw
from prepare_data import ROOT,NAMES

def iou(a,b):
    x1,y1=max(a[0],b[0]),max(a[1],b[1]);x2,y2=min(a[2],b[2]),min(a[3],b[3])
    intersection=max(0,x2-x1)*max(0,y2-y1)
    return intersection/max(1e-9,(a[2]-a[0])*(a[3]-a[1])+(b[2]-b[0])*(b[3]-b[1])-intersection)

def main():
    import torch
    from ultralytics import YOLO
    torch.set_num_threads(4)
    model=YOLO(str(ROOT/'models/best.pt'))
    meta=json.loads((ROOT/'models/metadata.json').read_text())
    rows=[r for r in json.loads((ROOT/'data/tomato/manifest.json').read_text())['items'] if r['split']=='test']
    output=ROOT/'reports/predictions';output.mkdir(exist_ok=True)
    audit=[]
    for row in rows:
        path=ROOT/'data/tomato/images/test'/(row['key']+'.jpg')
        with Image.open(path) as im: w,h=im.size
        start=time.perf_counter()
        pred=model.predict(str(path),imgsz=meta['imgsz'],conf=.4,device='cpu',verbose=False)[0]
        elapsed=1000*(time.perf_counter()-start)
        predicted=[{'class_id':int(b.cls.item()),'confidence':float(b.conf.item()),'bbox':b.xyxy[0].tolist()} for b in pred.boxes]
        ground=[{'class_id':b[0],'bbox':[(b[1]-b[3]/2)*w,(b[2]-b[4]/2)*h,(b[1]+b[3]/2)*w,(b[2]+b[4]/2)*h]} for b in row['boxes']]
        matches=set();tp=0
        for p in sorted(predicted,key=lambda d:-d['confidence']):
            candidates=[(iou(p['bbox'],g['bbox']),i) for i,g in enumerate(ground) if i not in matches and p['class_id']==g['class_id']]
            overlap,i=max(candidates,default=(0,-1))
            if overlap>=.5:matches.add(i);tp+=1
        fp=len(predicted)-tp;fn=len(ground)-tp
        # Predicted image only. Ground truth stored separately to distinguish it clearly.
        pred.save(filename=str(output/(row['key']+'_prediction.jpg')))
        with Image.open(path) as im:
            im=im.convert('RGB');draw=ImageDraw.Draw(im)
            for g in ground:
                draw.rectangle(g['bbox'],outline='blue',width=3)
                draw.text((g['bbox'][0],g['bbox'][1]),NAMES[g['class_id']],fill='blue')
            im.save(output/(row['key']+'_ground_truth.jpg'))
        audit.append({'image':row['key']+'.jpg','original_filename':row['source_name'],'tp':tp,'fp':fp,'fn':fn,
                      'latency_ms':elapsed,'ground_truth':ground,'predictions':predicted})
    summary={'confidence':.4,'iou':.5,'note':'Class-aware greedy matching; not the mAP calculation.',
             'model_sha256':meta['sha256'],'tp':sum(r['tp'] for r in audit),'fp':sum(r['fp'] for r in audit),
             'fn':sum(r['fn'] for r in audit),'images':audit}
    (ROOT/'reports/prediction_audit.json').write_text(json.dumps(summary,indent=2))
    errors=sorted([r for r in audit if r['fp']+r['fn']>0],key=lambda r:-(r['fp']+r['fn']))[:5]
    text='# Análise automática de até cinco erros reais\n\nConfiança 0,4 e IoU 0,5; pareamento por classe. Falsos positivos/negativos são relativos às anotações da base, que também podem conter erros. Revisão humana ainda necessária.\n\n'
    for i,r in enumerate(errors,1):
        text+=f"## Caso {i}: {r['original_filename']}\n\nArquivo: `{r['image']}`. TP={r['tp']}; FP={r['fp']}; FN={r['fn']}.\n\n"
        text+='Observação: o modelo não reproduziu integralmente as caixas e classes anotadas. As imagens de referência e previsão estão em `reports/predictions`. Iluminação, escala, confusão entre classes e anotações inconsistentes são hipóteses a verificar, não causas comprovadas.\n\n'
    (ROOT/'reports/ERROS_REAIS.md').write_text(text)
    print({k:summary[k] for k in ['tp','fp','fn']})

if __name__=='__main__':main()
