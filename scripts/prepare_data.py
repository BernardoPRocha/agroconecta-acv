"""Download a pinned PlantDoc subset, validate boxes and prevent duplicate leakage."""
import argparse, collections, concurrent.futures, csv, hashlib, io, json, random, shutil, time
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REV = '4730a233a555b30ee98e0879c63ad25d82407455'
BASE = f'https://raw.githubusercontent.com/pratikkayal/PlantDoc-Object-Detection-Dataset/{REV}/'
CLASSES = {'Tomato leaf': 0, 'Tomato Early blight leaf': 1, 'Tomato leaf late blight': 2}
NAMES = ['tomate_saudavel', 'pinta_preta', 'requeima']

def fetch(url):
    for attempt in range(3):
        try:
            with urlopen(url, timeout=40) as r: return r.read()
        except Exception:
            if attempt == 2: raise
            time.sleep(attempt + 1)

def box(row):
    w, h = float(row['width']), float(row['height'])
    x1,y1,x2,y2 = (float(row[k]) for k in ['xmin','ymin','xmax','ymax'])
    if not (w > 0 and h > 0 and 0 <= x1 < x2 <= w and 0 <= y1 < y2 <= h):
        raise ValueError('invalid bounding box')
    return [CLASSES[row['class']], (x1+x2)/2/w, (y1+y2)/2/h, (x2-x1)/w, (y2-y1)/h]

def image_signature(im):
    thumb = im.resize((16,16)).convert('L')
    values = list(thumb.get_flattened_data()); mean = sum(values)/len(values)
    return sum((v >= mean) << i for i,v in enumerate(values))

def download(item, cache):
    split, name, rows = item
    key = hashlib.sha256((split+'/'+name).encode()).hexdigest()[:20]
    path = cache / (key+'.jpg')
    try:
        boxes = [box(r) for r in rows]
        url = BASE + split.upper() + '/' + quote(name, safe='')
        if not path.exists():
            raw = fetch(url)
            with Image.open(io.BytesIO(raw)) as img:
                img.convert('RGB').save(path, quality=95)
        with Image.open(path) as img:
            img.load(); im = img.convert('RGB')
            # CSV dimensions must agree in aspect ratio; proportional rescaling is allowed.
            w,h = im.size; cw,ch = float(rows[0]['width']),float(rows[0]['height'])
            if abs(w/h-cw/ch) > 0.02: raise ValueError('image/annotation aspect ratio mismatch')
            digest = hashlib.sha256(im.tobytes()).hexdigest()
            ahash = image_signature(im)
        return dict(source_split=split, source_name=name, key=key, boxes=boxes,
                    pixel_sha256=digest, ahash=ahash, url=url)
    except Exception as e:
        return dict(source_split=split,source_name=name,error=str(e))

def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',default=str(ROOT/'data/tomato'))
    args=p.parse_args(); out=Path(args.output).resolve()
    if (out/'manifest.json').exists():
        print('Dataset already prepared. Use a different --output to rebuild.'); return
    cache=ROOT/'data/cache'; cache.mkdir(parents=True,exist_ok=True)
    items=[]; skipped=[]
    for split in ['test','train']:
        raw=fetch(BASE+split+'_labels.csv'); (cache/(split+'_labels.csv')).write_bytes(raw)
        groups=collections.defaultdict(list)
        for row in csv.DictReader(io.StringIO(raw.decode())): groups[row['filename']].append(row)
        for name,rows in sorted(groups.items()):
            if not any(r['class'] in CLASSES for r in rows): continue
            if any(r['class'] not in CLASSES for r in rows):
                skipped.append({'name':name,'reason':'mixed labels outside scope'}); continue
            items.append((split,name,rows))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results=list(pool.map(lambda x:download(x,cache),items))
    errors=[r for r in results if 'error' in r]; accepted=[]; duplicates=[]
    # Test has priority. Remove exact/near duplicates before any training/validation split.
    for r in results:
        if 'error' in r: continue
        match=next((a for a in accepted if a['pixel_sha256']==r['pixel_sha256'] or
                    (a['ahash']^r['ahash']).bit_count()<=4),None)
        if match:
            duplicates.append({'removed':r['source_name'],'kept':match['source_name']}); continue
        accepted.append(r)
    buckets=collections.defaultdict(list)
    for r in accepted:
        if r['source_split']=='test': r['split']='test'
        else: buckets[tuple(sorted(set(b[0] for b in r['boxes'])))].append(r)
    rng=random.Random(42)
    for rows in buckets.values():
        rng.shuffle(rows); n=max(1,round(len(rows)*.2)) if len(rows)>1 else 0
        for i,r in enumerate(rows): r['split']='val' if i<n else 'train'
    counts={}; out.mkdir(parents=True,exist_ok=True)
    for split in ['train','val','test']:
        for folder in ['images','labels']: (out/folder/split).mkdir(parents=True,exist_ok=True)
        rows=[r for r in accepted if r['split']==split]
        count=collections.Counter(b[0] for r in rows for b in r['boxes'])
        if set(count)!=set(range(3)): raise RuntimeError(f'{split}: missing class; inspect source/errors')
        counts[split]={'images':len(rows),'boxes':{NAMES[k]:v for k,v in count.items()}}
        for r in rows:
            shutil.copyfile(cache/(r['key']+'.jpg'),out/'images'/split/(r['key']+'.jpg'))
            (out/'labels'/split/(r['key']+'.txt')).write_text('\n'.join(
                str(b[0])+' '+' '.join(f'{v:.7f}' for v in b[1:]) for b in r['boxes'])+'\n')
    manifest={'source':BASE,'revision':REV,'seed':42,'counts':counts,'errors':errors,
              'excluded_mixed':skipped,'duplicates_removed':duplicates,'items':accepted}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
    # Absolute path regenerated on each machine by refresh_yaml().
    refresh_yaml(out)
    (ROOT/'reports/dataset_audit.json').write_text(json.dumps({k:v for k,v in manifest.items() if k!='items'},indent=2))
    (cache/'LICENSE.txt').write_bytes(fetch(BASE+'LICENSE.txt'))
    print(json.dumps(counts,indent=2)); print('Failed downloads/invalid images:',len(errors))

def refresh_yaml(out):
    out=Path(out).resolve()
    (out/'data.yaml').write_text('path: '+json.dumps(str(out))+'\ntrain: images/train\nval: images/val\ntest: images/test\nnames:\n'+''.join(f'  {i}: {n}\n' for i,n in enumerate(NAMES)))
    return out/'data.yaml'

if __name__=='__main__': main()
