import hashlib
import os
from pathlib import Path
import unittest
import sys
from unittest.mock import patch
from cloud.run import validate
from cloud.webui_entry import prepare_packages

TOKEN='offline_only_A9xB7yC5zD3wE1vF8uG6tH4sJ2rK0qM'


class WebUIConfigurationTests(unittest.TestCase):
    def test_target_bootstrap_processes_trusted_pth_files_only_when_called(self):
        target=Path(__file__).resolve().parents[1]
        before=list(sys.path)
        try:
            with patch('cloud.webui_entry.site.addsitedir') as add:
                prepare_packages(target)
                add.assert_called_once_with(str(target))
                self.assertEqual(sys.path[0],str(target))
        finally:sys.path[:]=before

    def test_upstream_slim_bytes_are_preserved(self):
        source=Path(__file__).resolve().parents[1]/'webui/requirements-slim.txt'
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),
            '6dc3e004a3935f4bcc19f804f791e536c1f4be381049d866f842b2c2e4a88509')

    def test_slim_host_uses_trusted_origin_and_secure_operator_cookies(self):
        env={'AGENT_API_TOKEN':TOKEN,'PUBLIC_ORIGIN':'https://synthetic.example.invalid',
             'WEBUI_SECRET_KEY':TOKEN,'DATABASE_URL':'postgresql://synthetic.invalid/db',
             'WEBUI_ADMIN_EMAIL':'operator@example.invalid','WEBUI_ADMIN_PASSWORD':'synthetic-password-not-for-use'}
        with patch.dict(os.environ,env,clear=True):
            validate('openwebui')
            self.assertEqual(os.environ['CORS_ALLOW_ORIGIN'],env['PUBLIC_ORIGIN'])
            self.assertEqual(os.environ['USE_SLIM_DOCKER'],'true')
            self.assertEqual(os.environ['ENABLE_SIGNUP'],'false')
            self.assertEqual(os.environ.get('WEBUI_AUTH_COOKIE_SECURE'),'true')
            self.assertEqual(os.environ.get('WEBUI_AUTH_COOKIE_SAME_SITE'),'strict')
