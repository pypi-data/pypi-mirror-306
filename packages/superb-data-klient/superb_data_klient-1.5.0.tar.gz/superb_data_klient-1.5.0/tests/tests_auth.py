import os
import sys
import unittest
import webbrowser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import superbdataklient as sdk
from superbdataklient import ClientInitializationError


class AuthenticationTestSDKClient(unittest.TestCase):
    env = 'sdk-dev'

    def test_get_organization_all(self):
        """
        instantiating a SDKClient should raise EnvironmentError in a no-browser-environment
        """
        try:
            webbrowser.get()
        except webbrowser.Error:
            with self.assertRaises(ClientInitializationError):
                sdk.SDKClient(env=self.env)


if __name__ == '__main__':
    unittest.main()
