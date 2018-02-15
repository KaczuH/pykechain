import time
from unittest import skip

import pytest

from pykechain.enums import ServiceExecutionStatus
from pykechain.exceptions import NotFoundError
from tests.classes import TestBetamax

# new in 1.13
class TestServices(TestBetamax):
    def test_retrieve_services(self):
        self.assertTrue(self.client.services())

    def test_retrieve_single_service(self):
        services = self.client.services()
        self.assertTrue(services)
        service_1 = services[0]

        self.assertEqual(self.client.service(pk=service_1.id), service_1)

    def test_retrieve_service_by_name(self):
        service_name = 'Debug pykechain'
        service = self.client.service(name=service_name)
        self.assertTrue(service)
        self.assertEqual(service.name, service_name)

    @pytest.mark.skipif("os.getenv('TRAVIS', False)",
                        reason="Skipping tests when using Travis, as Service Execution cannot be provided")
    def test_debug_service_execute(self):
        service_name = 'Debug pykechain'
        service = self.client.service(name=service_name)

        service_execution = service.execute()
        self.assertTrue(service_execution.status in ServiceExecutionStatus.values())
        if service_execution.status in (ServiceExecutionStatus.LOADING, ServiceExecutionStatus.RUNNING):
            # sleep 2000 ms
            time.sleep(2)
            service_execution.refresh()
            self.assertTrue(service_execution.status in ServiceExecutionStatus.values())
        self.assertFalse(service_execution.status == ServiceExecutionStatus.FAILED,
                         "The service execution is status 'FAILED', please upload working debugging scripts before "
                         "running the tests")

    def test_update_service(self):
        service_name = 'Debug pykechain'
        service = self.client.service(name=service_name)
        version_before = str(service.version)

        version_after = '-latest'
        service.edit(version=version_after)
        self.assertEqual(service.version, version_after)

        # destroy
        service.edit(version=version_before)

    def test_service_refresh_from_kechain(self):
        service_name = 'Debug pykechain'
        service = self.client.service(name=service_name)
        version_before = str(service.version)

        version_after = '-latest'
        service.edit(version=version_after)
        service.refresh()
        self.assertEqual(service.version, version_after)

        # destroy
        service.edit(version=version_before)

    def test_create_and_delete_service(self):
        service_name = 'new service'
        new_service = self.client.create_service(service_name, scope=self.project.id)

        self.assertTrue(new_service.name, service_name)
        self.assertTrue(new_service)

        # destroy
        new_service.delete()
        with self.assertRaisesRegex(NotFoundError, 'No service fits criteria'):
            self.client.service(pk=new_service.id)

# new in 1.13class TestServiceExecutions(TestBetamax):
    def test_retrieve_service_executions(self):
        self.assertTrue(self.client.service_executions())

    def test_retrieve_single_service_execution(self):
        service_executions = self.client.service_executions()
        self.assertTrue(service_executions)
        service_execution_1 = service_executions[0]

        self.assertEqual(self.client.service_execution(pk=service_execution_1.id), service_execution_1)

    @pytest.mark.skipif("os.getenv('TRAVIS', False)",
                        reason="Skipping tests when using Travis, as Service Execution cannot be provided")
    def test_debug_service_execution_terminate(self):
        service_name = 'Debug pykechain'
        service = self.client.service(name=service_name)

        service_execution = service.execute()
        service_execution.refresh()
        self.assertEqual(service_execution.status, ServiceExecutionStatus.LOADING)
        time.sleep(1)
        service_execution.refresh()
        self.assertEqual(service_execution.status, ServiceExecutionStatus.RUNNING)
        service_execution.terminate()

        self.assertFalse(service_execution.status == ServiceExecutionStatus.FAILED,
                         "The service execution is status 'FAILED', please upload working debugging scripts before "
                         "running the tests")
