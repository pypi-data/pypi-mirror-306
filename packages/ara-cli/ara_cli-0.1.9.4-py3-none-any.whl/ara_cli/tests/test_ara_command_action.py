import pytest
from unittest.mock import patch, MagicMock

# Import the function to be tested
from ara_cli.ara_command_action import read_action

# Define a test class or function
@pytest.mark.parametrize("classifier, artefact_name, classifier_title, content, file_path", [
    ("valid_classifier", "valid_artefact", "Valid Classifier Title", "Artefact content", "/path/to/artefact"),
    ("another_classifier", "another_artefact", "Another Classifier Title", "Another artefact content", "/another/path"),
])
def test_read_action(classifier, artefact_name, classifier_title, content, file_path, capsys):
    with patch('ara_cli.classifier.Classifier') as MockClassifier, \
         patch('ara_cli.artefact_reader.ArtefactReader') as MockArtefactReader:

        MockClassifier.get_artefact_title.return_value = classifier_title

        mock_reader_instance = MagicMock()
        mock_reader_instance.read_artefact.return_value = (content, file_path)
        MockArtefactReader.return_value = mock_reader_instance

        mock_args = MagicMock()
        mock_args.classifier = classifier
        mock_args.parameter = artefact_name

        read_action(mock_args)

        captured = capsys.readouterr()

        expected_output = f" - {classifier_title} {file_path}:\n{content}\n\n"
        assert captured.out == expected_output
