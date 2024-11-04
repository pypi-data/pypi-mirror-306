import unittest
from unittest.mock import patch, MagicMock, mock_open
import offlix_installer.installer
import subprocess


class TestDockerServiceManager(unittest.TestCase):

    @patch('builtins.print')
    def test_display_ascii_banner(self, mock_print):
        offlix_installer.installer.display_ascii_banner()
        mock_print.assert_called_once_with("""
     ______    _______   _______  ___        __     ___  ___  
   /    " \  /"     "| /"     "||"  |      |" \   |"  \/"  | 
  // ____  \(: ______)(: ______)||  |      ||  |   \   \  /  
 /  /    ) :)\/    |   \/    |  |:  |      |:  |    \\  \/   
(: (____/ // // ___)   // ___)   \  |___   |.  |    /\.  \   
 \        / (:  (     (:  (     ( \_|:  \  /\  |\  /  \   \  
  \_____/   \__/      \__/      \_______)(__\_|_)|___/\___|
                                                              
    """)  # Replace with the actual banner text

    @patch('builtins.input', side_effect=['no', 'yes'])
    @patch('time.sleep', return_value=None)
    def test_prompt_user_to_stop_streaming(self, mock_sleep, mock_input):
        from threading import Event
        stop_event = Event()
        offlix_installer.installer.prompt_user_to_stop_streaming(stop_event)
        self.assertTrue(stop_event.is_set())

    # @patch('subprocess.run')
    # @patch('os.path.isfile', return_value=True)
    # def test_start_service_install(self, mock_isfile, mock_run):
    #     mock_run.return_value = MagicMock()
    #     offlix_installer.installer.start_service('TestService', 'test.yaml', 'docker compose', 'install')
    #     mock_run.assert_called_once()

    # @patch('subprocess.run')
    # @patch('os.path.isfile', return_value=True)
    # def test_start_service_uninstall(self, mock_isfile, mock_run):
    #     mock_run.return_value = MagicMock()
    #     offlix_installer.installer.start_service('TestService', 'test.yaml', 'docker compose', 'uninstall')
    #     mock_run.assert_called_once()

    # @patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'command'))
    # @patch('os.path.isfile', return_value=True)
    # def test_start_service_invalid_action(self, mock_isfile, mock_run):
    #     with patch('builtins.print') as mock_print:
    #         offlix_installer.installer.start_service('InvalidService', 'test.yaml', 'docker compose', 'install')
    #         mock_print.assert_called_with('Failed to install InvalidService. Please check test.yaml and try again. ❗')

    @patch('docker.from_env')
    def test_get_service_env_success(self, mock_docker):
        mock_container = MagicMock()
        mock_container.attrs = {'Config': {'Env': ['KEY1=VALUE1', 'KEY2=VALUE2']}}
        mock_docker.return_value.containers.list.return_value = [mock_container]

        result = offlix_installer.installer.get_service_env('TestService')
        self.assertEqual(result, {'KEY1': 'VALUE1', 'KEY2': 'VALUE2'})

    @patch('docker.from_env')
    def test_get_service_env_no_container(self, mock_docker):
        mock_docker.return_value.containers.list.return_value = []
        result = offlix_installer.installer.get_service_env('TestService')
        self.assertEqual(result, {})



if __name__ == '__main__':
    unittest.main()