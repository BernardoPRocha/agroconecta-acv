import io
from types import SimpleNamespace
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app, decode

@pytest.fixture
def client(monkeypatch,tmp_path):
    monkeypatch.setenv('MODEL_PATH',str(tmp_path/'absent.pt'))
    with TestClient(app) as c: yield c

def png():
    f=io.BytesIO();Image.new('RGB',(100,50),'green').save(f,format='PNG');return f.getvalue()

def test_missing_model_is_not_a_prediction(client):
    assert client.get('/health').json()['model_ready'] is False
    assert client.get('/ready').status_code==503
    assert client.post('/api/predict',files={'file':('x.png',png())}).status_code==503

def test_page_and_assets(client):
    assert client.get('/').status_code==200
    assert client.get('/static/app.js').status_code==200

def test_invalid_and_oversized_images(client):
    app.state.model=object()
    assert client.post('/api/predict',files={'file':('a.jpg',b'not image')}).status_code==415
    assert client.post('/api/predict',files={'file':('a.jpg',b'x'*(8*1024*1024+1))}).status_code==413
    assert client.post('/api/predict?confidence=2',files={'file':('x.png',png())}).status_code==422

def test_no_detection_is_inconclusive(client):
    app.state.model=SimpleNamespace(predict=lambda *a,**kw:[SimpleNamespace(boxes=[])])
    r=client.post('/api/predict',files={'file':('x.png',png())})
    assert r.status_code==200
    assert r.json()['status']=='inconclusive'
    assert (r.json()['width'],r.json()['height'])==(100,50)

def test_decode_exif_orientation():
    im=Image.new('RGB',(80,40)); exif=im.getexif();exif[274]=6
    f=io.BytesIO();im.save(f,format='JPEG',exif=exif)
    assert decode(f.getvalue()).size==(40,80)
