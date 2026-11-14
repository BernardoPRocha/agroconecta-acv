import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from prepare_data import box

def test_box_coordinates():
    r=dict(width=100,height=200,xmin=10,ymin=20,xmax=50,ymax=100)
    r['class']='Tomato leaf'
    assert box(r)==[0,.3,.3,.4,.4]
    r['xmax']=101
    with pytest.raises(ValueError): box(r)

def test_actual_split_no_exact_or_near_leakage():
    import json
    p=Path(__file__).resolve().parents[1]/'data/tomato/manifest.json'
    if not p.exists(): pytest.skip('Dataset not prepared')
    items=json.loads(p.read_text())['items']
    for i,a in enumerate(items):
        for b in items[i+1:]:
            if a['split']==b['split']: continue
            assert a['pixel_sha256']!=b['pixel_sha256']
            assert (a['ahash']^b['ahash']).bit_count()>4
