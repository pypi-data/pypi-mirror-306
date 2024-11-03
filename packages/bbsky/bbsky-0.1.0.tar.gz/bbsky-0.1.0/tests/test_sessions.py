from collections import OrderedDict
from unittest.mock import Mock

import pytest

from bbsky.config import SkyConfig
from bbsky.sessions import SyncSessionManager, SyncUserSession, User
from bbsky.tokens import OAuth2Token


@pytest.fixture
def config() -> SkyConfig:
    return Mock(spec=SkyConfig)


@pytest.fixture
def oauth_token() -> OAuth2Token:
    return Mock(spec=OAuth2Token)


@pytest.fixture
def user(oauth_token) -> User:
    return User(user_id="test_user", token=oauth_token)


@pytest.fixture
def session_manager(config: SkyConfig) -> SyncSessionManager:
    return SyncSessionManager(config=config, max_sessions=10)


def create_user(user_id: str) -> User:
    """Helper function to create test users"""
    return User(user_id=user_id, token=Mock(spec=OAuth2Token))


class TestSyncSessionManager:
    def test_init(self, session_manager: SyncSessionManager, config: SkyConfig) -> None:
        """Test initialization of session manager"""
        assert isinstance(session_manager.sessions, OrderedDict)
        assert session_manager.config == config
        assert len(session_manager.sessions) == 0

    def test_add_session(self, session_manager: SyncSessionManager, user: User):
        """Test adding a new session"""
        session_manager.add_session(user)
        assert session_manager.has_session(user.user_id)
        session = session_manager.get_session(user.user_id)
        assert isinstance(session, SyncUserSession)
        assert session.user == user
        assert session.config == session_manager.config

    def test_max_sessions(self, session_manager: SyncSessionManager):
        """Test that oldest sessions are removed when max capacity is reached"""
        # Add max_sessions + 1 sessions
        for i in range(session_manager.max_sessions + 1):
            user = create_user(f"user_{i}")
            session_manager.add_session(user)

        # Check that we only have max_sessions sessions
        assert len(session_manager.sessions) == session_manager.max_sessions

        # Verify the first user was removed (FIFO)
        assert not session_manager.has_session("user_0")
        # Verify the last user was added
        assert session_manager.has_session(f"user_{session_manager.max_sessions}")

    def test_find_session(self, session_manager, user):
        """Test finding existing and non-existing sessions"""
        # Test non-existing session
        assert session_manager.find_session("nonexistent") is None

        # Test existing session
        session_manager.add_session(user)
        session = session_manager.find_session(user.user_id)
        assert isinstance(session, SyncUserSession)
        assert session.user == user

    def test_get_session(self, session_manager, user):
        """Test getting sessions with error handling"""
        # Test getting non-existent session raises error
        with pytest.raises(ValueError, match="No session found for user ID: nonexistent"):
            session_manager.get_session("nonexistent")

        # Test getting existing session
        session_manager.add_session(user)
        session = session_manager.get_session(user.user_id)
        assert isinstance(session, SyncUserSession)
        assert session.user == user

    def test_has_session(self, session_manager, user):
        """Test session existence checking"""
        assert not session_manager.has_session(user.user_id)
        session_manager.add_session(user)
        assert session_manager.has_session(user.user_id)

    def test_remove_session(self, session_manager, user):
        """Test removing sessions"""
        session_manager.add_session(user)
        assert session_manager.has_session(user.user_id)

        session_manager.remove_session(user.user_id)
        assert not session_manager.has_session(user.user_id)

        # Verify removing non-existent session raises KeyError
        with pytest.raises(KeyError):
            session_manager.remove_session("nonexistent")

    def test_clear_sessions(self, session_manager):
        """Test clearing all sessions"""
        # Add multiple sessions
        for i in range(3):
            user = create_user(f"user_{i}")
            session_manager.add_session(user)

        assert len(session_manager.sessions) == 3

        session_manager.clear_sessions()
        assert len(session_manager.sessions) == 0

    def test_session_reuses_client(self):
        """Test that the same client is reused for the same user"""
        from bbsky.data_cls import URL

        session_manager = SyncSessionManager(
            config=SkyConfig(
                client_id="cool-client",
                client_secret="super-secret",
                redirect_uri=URL("https://example.com"),
                subscription_key="sk-1234",
            ),
            max_sessions=10,
        )
        token = OAuth2Token(
            access_token="super-secret-token",
            refresh_token="refresh-token",
            expires_in=3600,
            refresh_token_expires_in=3600,
            token_type="Bearer",
            environment_id="env-1234",
            environment_name="Test Environment",
            legal_entity_id="legal-1234",
            legal_entity_name="Test Legal Entity",
            user_id="cool-user",
            email="cool-user@gmail.com",
            family_name="Lawrence",
            given_name="Thomas",
            mode="test",
        )
        test_user = User(user_id="cool-user", token=token)
        session_manager.add_session(user=test_user)
        session1 = session_manager.get_session(user_id=test_user.user_id)
        resp1 = session1.get(endpoint="constituent/v1/constituents")

        headers_used_in_session1_request = resp1.request.headers
        assert "Authorization" in headers_used_in_session1_request
        assert headers_used_in_session1_request["Authorization"] == f"Bearer {token.access_token}"
        assert "Bb-Api-Subscription-Key" in headers_used_in_session1_request
        assert headers_used_in_session1_request["Bb-Api-Subscription-Key"] == "sk-1234"

        session2 = session_manager.get_session(test_user.user_id)
        assert session1.client is session2.client

        resp2 = session2.get(endpoint="crm-conmg/constituents/search")

        headers_used_in_session2_request = resp2.request.headers
        assert headers_used_in_session1_request == headers_used_in_session2_request
