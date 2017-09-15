import os
import pytest
from envparse import env

from pykechain import get_project
from pykechain.enums import KechainEnv
from pykechain.exceptions import ClientError, APIError
from tests.classes import TestBetamax
from tests.utils import TEST_TOKEN, TEST_URL, TEST_SCOPE_NAME, TEST_SCOPE_ID


PSEUDO_TOKEN = 'aabbccddeeffgg0011223344556677889900'
PSEUDO_PASSWORD = 'abc123!@#'
PSEUDO_SCOPE_ID = 'eeb0937b-da50-4eb2-8d74-f36259cca96e'


@pytest.mark.skipif("os.getenv('TRAVIS', False)", reason="Skipping tests when using Travis, as not Auth can be provided")
class TestGetProjectHelperNotForTravis(TestBetamax):
    def test_get_project__not_for_travis(self):
        os.environ[KechainEnv.KECHAIN_FORCE_ENV_USE]="false"
        project = get_project(TEST_URL, token=TEST_TOKEN, scope=TEST_SCOPE_NAME)
        self.assertEqual(project.name, TEST_SCOPE_NAME)

    def test_get_project__force_env_use(self):
        """Test the get_project by using KECHAIN_FORCE_ENV_USE=True"""
        #setup
        saved_environment = dict(os.environ)

        os.environ['KECHAIN_FORCE_ENV_USE']=str(True)
        self.assertTrue(env.bool(KechainEnv.KECHAIN_FORCE_ENV_USE))

        with self.assertRaisesRegex(ClientError, "should be provided as environment variable"):
            project=get_project()

        os.environ['KECHAIN_URL'] = TEST_URL
        with self.assertRaisesRegex(ClientError, "should be provided as environment variable"):
            project=get_project()


        os.environ['KECHAIN_TOKEN'] = TEST_TOKEN
        with self.assertRaisesRegex(ClientError, "should be provided as environment variable"):
            project=get_project()

        # os.environ['KECHAIN_SCOPE'] = TEST_SCOPE_NAME
        with self.assertRaises(APIError):
            project=get_project(url='http://whatever', token=PSEUDO_TOKEN)


        # teardown
        #
        os.unsetenv('KECHAIN_URL')
        os.unsetenv('KECHAIN_TOKEN')
        os.unsetenv('KECHAIN_SCOPE')
        os.unsetenv('KECHAIN_FORCE_ENV_USE')
        for k, v in saved_environment.items():
            os.environ[k] = v

    def test_test_get_project_with_scope_id__not_for_travis(self):
        project = get_project(TEST_URL, token=TEST_TOKEN, scope_id=TEST_SCOPE_ID)
        self.assertEqual(project.name, TEST_SCOPE_NAME)

    def test_get_project_from_env__not_for_travis(self):
        # setup
        saved_environment = dict(os.environ)
        os.environ['KECHAIN_URL'] = TEST_URL
        os.environ['KECHAIN_TOKEN'] = TEST_TOKEN
        os.environ['KECHAIN_SCOPE'] = TEST_SCOPE_NAME

        # do test
        project = get_project()
        self.assertEqual(project.name, os.environ['KECHAIN_SCOPE'])

        # teardown
        os.unsetenv('KECHAIN_URL')
        os.unsetenv('KECHAIN_TOKEN')
        os.unsetenv('KECHAIN_SCOPE')
        for k, v in saved_environment.items():
            os.environ[k] = v


class TestGetProjectHelper(TestBetamax):
    ERROR_MESSAGE_REGEX = "Error: insufficient arguments"

    def test_project_raises_error__no_auth(self):
        with self.assertRaisesRegex(ClientError, self.ERROR_MESSAGE_REGEX):
            get_project(url=TEST_URL)

    def test_project_raises_error__token_and_no_scope(self):
        with self.assertRaisesRegex(ClientError, self.ERROR_MESSAGE_REGEX):
            get_project(url=TEST_URL, token=TEST_TOKEN)

    def test_project_raises_error__no_pass(self):
        with self.assertRaisesRegex(ClientError, self.ERROR_MESSAGE_REGEX):
            get_project(url=TEST_URL, username='auser', scope='Scope')

    def test_project_raises_error__auth_and_no_scope(self):
        with self.assertRaisesRegex(ClientError, self.ERROR_MESSAGE_REGEX):
            get_project(url=TEST_URL, username='auser', password=PSEUDO_PASSWORD)

    def test_project_raises_error__scope_id_and_no_pass(self):
        with self.assertRaisesRegex(ClientError, self.ERROR_MESSAGE_REGEX):
            get_project(url=TEST_URL, username='auser', scope_id=PSEUDO_SCOPE_ID)

    def test_project_raises_error__auth_and_no_url(self):
        with self.assertRaisesRegex(ClientError, self.ERROR_MESSAGE_REGEX):
            get_project(username='auser', password=PSEUDO_PASSWORD, scope_id=PSEUDO_SCOPE_ID)

    def test_project_raises_error__token_and_no_url(self):
        with self.assertRaisesRegex(ClientError, self.ERROR_MESSAGE_REGEX):
            get_project(token=PSEUDO_TOKEN, scope_id=PSEUDO_SCOPE_ID)


