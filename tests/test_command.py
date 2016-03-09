import pytest
from git_resolutions import install, publish, check, cli
from conftest import shell


def test_clean(clean):
    # project track origin
    # rr-cache is not configured

    with pytest.raises(RuntimeError):
        check(clean)
    install(clean)
    check(clean)
    publish(clean)


def test_fresh(fresh):
    # project does not track origin
    # rr-cache is not configured

    with pytest.raises(RuntimeError):
        install(fresh)

    with pytest.raises(RuntimeError):
        publish(fresh)


def test_mixmatch(mixmatch):
    # project and rr-cache track different repositories

    with pytest.raises(RuntimeError):
        publish(mixmatch)

    with pytest.raises(RuntimeError):
        install(mixmatch)

    install(mixmatch, force=True)
    publish(mixmatch)


def test_merge(merge_repository):
    # test a merge

    result = merge(merge_repository, 'i18n-world')
    assert result is False
    merge_repository.resolve()
    publish(mixmatch)
