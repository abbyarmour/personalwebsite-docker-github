import os
import tempfile
from app import app, dal as global_dal
from DAL import DAL


def setup_test_db():
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    dal = DAL(path)
    return dal, path


def test_projects_page_shows_projects(monkeypatch):
    dal, path = setup_test_db()
    try:
        # add a project
        dal.add_project('Title1', 'Desc1', 'img1.png')

        # monkeypatch the global dal in app to use our test dal
        monkeypatch.setattr('app.dal', dal)

        client = app.test_client()
        resp = client.get('/projects')
        assert resp.status_code == 200
        data = resp.get_data(as_text=True)
        assert 'Title1' in data
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def test_contact_post_adds_project(monkeypatch):
    dal, path = setup_test_db()
    try:
        monkeypatch.setattr('app.dal', dal)
        client = app.test_client()
        resp = client.post('/contact', data={
            'Title': 'FromForm',
            'Description': 'DescForm',
            'ImageFileName': 'imgform.png'
        }, follow_redirects=True)
        assert resp.status_code == 200
        text = resp.get_data(as_text=True)
        # After posting, it redirects to projects which should contain the new title
        assert 'FromForm' in text
    finally:
        try:
            os.remove(path)
        except OSError:
            pass
