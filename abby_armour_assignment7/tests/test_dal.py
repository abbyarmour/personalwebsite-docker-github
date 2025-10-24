import os
import tempfile
import sqlite3
from DAL import DAL


def test_add_and_get_projects():
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    try:
        dal = DAL(path)
        # DB should start empty
        rows = dal.get_all_projects()
        assert rows == []

        # Add a project and verify it appears
        new_id = dal.add_project('T', 'D', 'img.png')
        assert isinstance(new_id, int) and new_id > 0

        rows = dal.get_all_projects()
        assert len(rows) == 1
        row = rows[0]
        # rows are returned as tuples (id, Title, Description, ImageFileName)
        assert row[1] == 'T'
        assert row[2] == 'D'
        assert row[3] == 'img.png'

        # Add another and ensure ordering is DESC by id
        dal.add_project('T2', 'D2', 'img2.png')
        rows = dal.get_all_projects()
        assert len(rows) == 2
        assert rows[0][1] == 'T2'

        # Delete a project
        dal.delete_project(new_id)
        rows = dal.get_all_projects()
        assert all(r[0] != new_id for r in rows)

    finally:
        try:
            os.remove(path)
        except OSError:
            pass
