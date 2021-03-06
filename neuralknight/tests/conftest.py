from neuralknight.models.board import Board
from os import environ
from pyramid.testing import DummyRequest, setUp, tearDown
from neuralknight.models.meta import Base
from pytest import fixture


@fixture
def configuration(request):
    """
    Create database models for testing purposes.
    """
    config = setUp(settings={
        'sqlalchemy.url': environ.get(
            'TEST_DATABASE_URL', 'postgres://localhost:5432/neuralknight')
    })
    config.include('neuralknight.models')
    config.include('neuralknight.routes')
    yield config
    tearDown()


@fixture
def db_session(configuration, request):
    """
    Create a database session for interacting with the test database.
    """
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)
    yield session
    session.transaction.rollback()
    Base.metadata.drop_all(engine)


@fixture
def dummy_request(db_session):
    """
    Create a dummy GET request with a dbsession.
    """
    return DummyRequest(dbsession=db_session)


@fixture
def dummy_post_request(db_session):
    """
    Create a dummy POST request with a dbsession.
    """
    return DummyRequest(dbsession=db_session, post={})


@fixture
def start_board():
    return Board()
