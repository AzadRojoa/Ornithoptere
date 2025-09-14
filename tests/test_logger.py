"""
Tests unitaires pour le module Logger
"""
import unittest
import sys
import os
import tempfile
from unittest.mock import patch, mock_open

# Ajouter le répertoire source au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

class TestLogger(unittest.TestCase):
    
    def setUp(self):
        """Setup pour chaque test"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        self.temp_filename = self.temp_file.name
        self.temp_file.close()
    
    def tearDown(self):
        """Cleanup après chaque test"""
        try:
            os.unlink(self.temp_filename)
        except FileNotFoundError:
            pass
    
    def test_init_default_filename(self):
        """Test l'initialisation avec le nom de fichier par défaut"""
        from logger import Logger
        logger = Logger()
        self.assertEqual(logger.filename, "log.txt")
    
    def test_init_custom_filename(self):
        """Test l'initialisation avec un nom de fichier personnalisé"""
        from logger import Logger
        logger = Logger("custom.log")
        self.assertEqual(logger.filename, "custom.log")
    
    @patch('logger.time.localtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_log_method(self, mock_file, mock_time):
        """Test la méthode log"""
        # Mock du timestamp
        mock_time.return_value = (2024, 9, 14, 10, 30, 45, 5, 258, 0)
        
        from logger import Logger
        logger = Logger("test.log")
        logger.log("INFO", "Test message")
        
        mock_file.assert_called_once_with("test.log", "a")
        mock_file().write.assert_called_once_with("[2024-09-14 10:30:45] INFO: Test message\n")
    
    @patch('logger.time.localtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_debug_method(self, mock_file, mock_time):
        """Test la méthode debug"""
        mock_time.return_value = (2024, 9, 14, 10, 30, 45, 5, 258, 0)
        
        from logger import Logger
        logger = Logger("test.log")
        logger.debug("Debug message")
        
        mock_file().write.assert_called_once_with("[2024-09-14 10:30:45] DEBUG: Debug message\n")
    
    @patch('logger.time.localtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_info_method(self, mock_file, mock_time):
        """Test la méthode info"""
        mock_time.return_value = (2024, 9, 14, 10, 30, 45, 5, 258, 0)
        
        from logger import Logger
        logger = Logger("test.log")
        logger.info("Info message")
        
        mock_file().write.assert_called_once_with("[2024-09-14 10:30:45] INFO: Info message\n")
    
    @patch('logger.time.localtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_warning_method(self, mock_file, mock_time):
        """Test la méthode warning"""
        mock_time.return_value = (2024, 9, 14, 10, 30, 45, 5, 258, 0)
        
        from logger import Logger
        logger = Logger("test.log")
        logger.warning("Warning message")
        
        mock_file().write.assert_called_once_with("[2024-09-14 10:30:45] WARNING: Warning message\n")
    
    @patch('logger.time.localtime')
    @patch('builtins.open', new_callable=mock_open)
    def test_error_method(self, mock_file, mock_time):
        """Test la méthode error"""
        mock_time.return_value = (2024, 9, 14, 10, 30, 45, 5, 258, 0)
        
        from logger import Logger
        logger = Logger("test.log")
        logger.error("Error message")
        
        mock_file().write.assert_called_once_with("[2024-09-14 10:30:45] ERROR: Error message\n")
    
    @patch('builtins.open', side_effect=IOError("File error"))
    @patch('builtins.print')
    def test_log_file_error(self, mock_print, mock_file):
        """Test le comportement quand il y a une erreur de fichier"""
        from logger import Logger
        logger = Logger("test.log")
        logger.log("INFO", "Test message")
        
        mock_print.assert_called_once_with("Logger error:", mock_file.side_effect)
    
    @patch('logger.time.localtime')
    def test_timestamp_formatting(self, mock_time):
        """Test le formatage du timestamp"""
        # Test avec des valeurs à un chiffre pour vérifier le padding
        mock_time.return_value = (2024, 1, 5, 8, 7, 3, 5, 258, 0)
        
        from logger import Logger
        
        with patch('builtins.open', mock_open()) as mock_file:
            logger = Logger("test.log")
            logger.info("Test")
            
            mock_file().write.assert_called_once_with("[2024-01-05 08:07:03] INFO: Test\n")

if __name__ == '__main__':
    unittest.main()
