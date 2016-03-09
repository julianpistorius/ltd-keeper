"""Tests for the builds API."""

import pytest

from app.exceptions import ValidationError


def test_builds(client):
    # Add a sample product
    p = {'slug': 'lsst_apps',
         'doc_repo': 'https://github.com/lsst/pipelines_docs.git',
         'title': 'LSST Science Pipelines',
         'domain': 'pipelines.lsst.io',
         'bucket_name': 'bucket-name'}
    r = client.post('/products/', p)
    assert r.status == 201

    prod_url = client.get('/products/lsst_apps').json['self_url']

    # Initially no builds
    r = client.get('/products/lsst_apps/builds/')
    assert r.status == 200
    assert len(r.json['builds']) == 0

    # Add a build
    b1 = {'slug': 'b1',
          'github_requester': 'jonathansick',
          'git_refs': ['master']}
    r = client.post('/products/lsst_apps/builds/', b1)
    assert r.status == 201
    assert r.json['product_url'] == prod_url
    assert r.json['slug'] == b1['slug']
    assert r.json['date_created'] is not None
    assert r.json['date_ended'] is None
    assert r.json['uploaded'] is False

    # Re-add build with same slug; should fail
    with pytest.raises(ValidationError):
        r = client.post('/products/lsst_apps/builds/', b1)

    # List builds
    r = client.get('/products/lsst_apps/builds/')
    assert r.status == 200
    assert len(r.json['builds']) == 1

    # Get build
    r = client.get('/builds/1')
    assert r.status == 200
    assert r.json['bucket_name'] == 'bucket-name'
    assert r.json['bucket_root_dir'] == 'lsst_apps/builds/b1'

    # Register upload
    r = client.post('/builds/1/uploaded', {})
    assert r.status == 200

    r = client.get('/builds/1')
    assert r.json['uploaded'] is True

    # Deprecate build
    r = client.delete('/builds/1')
    assert r.status == 200

    r = client.get('/builds/1')
    assert r.json['product_url'] == prod_url
    assert r.json['slug'] == b1['slug']
    assert r.json['date_created'] is not None
    assert r.json['date_ended'] is not None

    # Build no longer in listing
    r = client.get('/products/lsst_apps/builds/')
    assert r.status == 200
    assert len(r.json['builds']) == 0

    # Add some auto-slugged builds
    b2 = {'git_refs': ['master']}
    r = client.post('/products/lsst_apps/builds/', b2)
    assert r.status == 201
    assert r.json['slug'] == '1'

    b3 = {'git_refs': ['master']}
    r = client.post('/products/lsst_apps/builds/', b3)
    assert r.status == 201
    assert r.json['slug'] == '2'

    # Add a build missing 'git_refs'
    b4 = {'slug': 'bad-build'}
    with pytest.raises(ValidationError):
        r = client.post('/products/lsst_apps/builds/', b4)

    # Add a build with a badly formatted git_refs
    b5 = {'slug': 'another-bad-build',
          'git_refs': 'master'}
    with pytest.raises(ValidationError):
        r = client.post('/products/lsst_apps/builds/', b5)
