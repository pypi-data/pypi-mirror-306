import pytest
import random
from unittest.mock import patch, mock_open
from fortunes.get_quotes_by_author import get_quotes_by_author
from fortunes.send_email import send_fortune_email
from fortunes.random_fortune import get_fortune_cookie
from fortunes.getMultipleFortunes import getMultipleFortunes


def test_get_fortune_cookie_deterministic_output():
    # Mock content for the 'fortune.txt' file
    mock_fortunes = "Good things come to those who wait.%Patience is a virtue.%Hard work pays off."

    with patch('fortunes.random_fortune.importlib.resources.open_text', mock_open(read_data=mock_fortunes)):
        with patch('fortunes.random_fortune.random.choice') as mock_random_choice:
            # Set the mocked random.choice to return the first fortune for consistency
            mock_random_choice.return_value = "Good things come to those who wait."

            result = get_fortune_cookie()
            
            # Verify the output is a formatted string containing the selected fortune and a lucky number
            assert isinstance(result, str)
            assert "🔮 Your Fortune: Good things come to those who wait." in result
            
            # Extract the lucky number and check it falls within the range 0–99
            lucky_number = int(result.split("🍀 Your Lucky Number: ")[1])
            assert 0 <= lucky_number <= 99

def test_get_fortune_cookie_randomness():
    # Provide multiple fortunes to check for varied output
    mock_fortunes = "Fortune favors the bold.%Patience is a virtue.%Hard work pays off."

    with patch('fortunes.random_fortune.importlib.resources.open_text', mock_open(read_data=mock_fortunes)):
        # Call the function multiple times and collect results
        results = {get_fortune_cookie() for _ in range(10)}

        # Ensure that multiple unique fortunes are returned, indicating randomness
        assert len(results) > 1  # Expect at least two different fortunes among the results
def test_get_multiple_fortunes_basic():
    # Mock the content of fortune.txt with multiple fortunes
    mock_fortunes = "Fortune 1 % Fortune 2 % Fortune 3"
    
    with patch('fortunes.getMultipleFortunes.importlib.resources.open_text', mock_open(read_data=mock_fortunes)):
        with patch('fortunes.getMultipleFortunes.random.choice', side_effect=["Fortune 1", "Fortune 2", "Fortune 3"]), \
             patch('fortunes.getMultipleFortunes.random.randint', return_value=42):
            
            result = getMultipleFortunes(3)
            
            # Check if the result contains 3 unique fortunes
            assert len(result) == 3
            assert "🔮 Your Fortune: Fortune 1\n🍀 Your Lucky Number: 42" in result
            assert "🔮 Your Fortune: Fortune 2\n🍀 Your Lucky Number: 42" in result
            assert "🔮 Your Fortune: Fortune 3\n🍀 Your Lucky Number: 42" in result

def test_get_multiple_fortunes_duplicates():
    # Mock the content of fortune.txt with duplicate fortunes in the result
    mock_fortunes = "Fortune 1 % Fortune 2 % Fortune 3"
    
    with patch('fortunes.getMultipleFortunes.importlib.resources.open_text', mock_open(read_data=mock_fortunes)):
        with patch('fortunes.getMultipleFortunes.random.choice', side_effect=["Fortune 1", "Fortune 2", "Fortune 3"]), \
             patch('fortunes.getMultipleFortunes.random.randint', return_value=88):
            
            result = getMultipleFortunes(3)
            
            # Check that there are no duplicates in the result
            assert len(result) == len(set(result))

def test_get_multiple_fortunes_more_than_available():
    # Test for requesting more fortunes than are available in the file
    mock_fortunes = "Fortune 1 % Fortune 2"
    
    with patch('fortunes.getMultipleFortunes.importlib.resources.open_text', mock_open(read_data=mock_fortunes)):
        # Add ValueError handling in function to handle the request for more unique fortunes than available
        with pytest.raises(ValueError):
            getMultipleFortunes(3)

def test_get_multiple_fortunes_single():
    # Test with a single fortune request
    mock_fortunes = "Only one fortune available"
    
    with patch('fortunes.getMultipleFortunes.importlib.resources.open_text', mock_open(read_data=mock_fortunes)):
        with patch('fortunes.getMultipleFortunes.random.choice', return_value="Only one fortune available"), \
             patch('fortunes.getMultipleFortunes.random.randint', return_value=13):
            
            result = getMultipleFortunes(1)
            
            # Check that a single fortune with the correct lucky number is returned
            assert result == ["🔮 Your Fortune: Only one fortune available\n🍀 Your Lucky Number: 13"]

def test_get_multiple_fortunes_random_calls():
    # Test if random.choice and random.randint are called as expected
    mock_fortunes = "Fortune 1 % Fortune 2 % Fortune 3"
    
    with patch('fortunes.getMultipleFortunes.importlib.resources.open_text', mock_open(read_data=mock_fortunes)):
        with patch('fortunes.getMultipleFortunes.random.choice') as mock_choice, \
             patch('fortunes.getMultipleFortunes.random.randint') as mock_randint:
            
            mock_choice.side_effect = ["Fortune 1", "Fortune 2", "Fortune 3"]
            mock_randint.side_effect = [10, 20, 30]
            
            getMultipleFortunes(3)
            
            # Ensure random.choice and random.randint were called exactly 3 times each
            assert mock_choice.call_count == 3
            assert mock_randint.call_count == 3
        
def test_get_fortune_cookie_basic():
    # Mock the content of the fortune.txt file with multiple fortunes
    mock_fortunes = "Fortune 1 % Fortune 2 % Fortune 3"
    
    with patch('fortunes.random_fortune.importlib.resources.open_text', mock_open(read_data=mock_fortunes)):
        with patch('fortunes.random_fortune.random.choice', return_value="Fortune 2"):
            with patch('fortunes.random_fortune.random.randint', return_value=42):
                result = get_fortune_cookie()
                
                # Check if the output matches the expected format
                assert result == "🔮 Your Fortune: Fortune 2\n🍀 Your Lucky Number: 42"

def test_get_fortune_cookie_random_calls():
    mock_fortunes = "Fortune 1 % Fortune 2 % Fortune 3"
    
    with patch('fortunes.random_fortune.importlib.resources.open_text', mock_open(read_data=mock_fortunes)):
        with patch('fortunes.random_fortune.random.choice') as mock_choice, \
             patch('fortunes.random_fortune.random.randint') as mock_randint:
            
            mock_choice.return_value = "Fortune 1"
            mock_randint.return_value = 88
            get_fortune_cookie()
            
            # Ensure random.choice and random.randint were called once each
            mock_choice.assert_called_once()
            mock_randint.assert_called_once()

def test_get_fortune_cookie_empty_file():
    # Test for an empty fortune file
    mock_fortunes = ""
    
    with patch('fortunes.random_fortune.importlib.resources.open_text', mock_open(read_data=mock_fortunes)):
        with pytest.raises(IndexError):  # random.choice will raise IndexError on an empty list
            get_fortune_cookie()

def test_get_fortune_cookie_single_fortune():
    # Test the case where there's only one fortune in the file
    mock_fortunes = "Single fortune only"
    
    with patch('fortunes.random_fortune.importlib.resources.open_text', mock_open(read_data=mock_fortunes)):
        with patch('fortunes.random_fortune.random.choice', return_value="Single fortune only"):
            with patch('fortunes.random_fortune.random.randint', return_value=7):
                result = get_fortune_cookie()
                
                # Ensure it returns the single fortune and a lucky number
                assert result == "🔮 Your Fortune: Single fortune only\n🍀 Your Lucky Number: 7"

def test_get_fortune_cookie_large_fortunes():
    # Test with a large number of fortunes in the file
    mock_fortunes = "Fortune " + " % ".join(str(i) for i in range(1000))
    
    with patch('fortunes.random_fortune.importlib.resources.open_text', mock_open(read_data=mock_fortunes)):
        with patch('fortunes.random_fortune.random.choice', return_value="Fortune 999"):
            with patch('fortunes.random_fortune.random.randint', return_value=99):
                result = get_fortune_cookie()
                
                # Ensure it selects a fortune from the large list
                assert result == "🔮 Your Fortune: Fortune 999\n🍀 Your Lucky Number: 99"

def test_send_fortune_email_single_fortune():
    recipient_email = "test@example.com"
    fortune = "🔮 Your Fortune: Good things are coming your way!\n🍀 Your Lucky Number: 7"

    with patch('fortunes.send_email.smtplib.SMTP') as mock_smtp:
        send_fortune_email(recipient_email, fortune)

        mock_smtp.assert_called_with("smtp.gmail.com", 587)
        instance = mock_smtp.return_value.__enter__.return_value
        instance.starttls.assert_called_once()
        instance.login.assert_called_once()
        instance.sendmail.assert_called_once()

def test_send_fortune_email_multiple_fortunes():
    recipient_email = "test@example.com"
    fortunes = [
        "🔮 Your Fortune: Happiness is around the corner.\n🍀 Your Lucky Number: 12",
        "🔮 Your Fortune: Success is in your future.\n🍀 Your Lucky Number: 24"
    ]

    with patch('fortunes.send_email.smtplib.SMTP') as mock_smtp:
        send_fortune_email(recipient_email, fortunes)

        mock_smtp.assert_called_with("smtp.gmail.com", 587)
        instance = mock_smtp.return_value.__enter__.return_value
        instance.starttls.assert_called_once()
        instance.login.assert_called_once()
        instance.sendmail.assert_called_once()

def test_send_fortune_email_invalid_email():
    recipient_email = "invalid-email"
    fortune = "🔮 Your Fortune: Be cautious today.\n🍀 Your Lucky Number: 13"

    with pytest.raises(Exception):
        send_fortune_email(recipient_email, fortune)

def test_send_fortune_email_server_connection_failure():
    recipient_email = "test@example.com"
    fortune = "🔮 Your Fortune: Good things are coming your way!\n🍀 Your Lucky Number: 7"

    with patch('fortunes.send_email.smtplib.SMTP', side_effect=Exception("Failed to connect")):
        with pytest.raises(Exception, match="Failed to connect"):
            send_fortune_email(recipient_email, fortune)

def test_send_fortune_email_empty_fortune():
    recipient_email = "test@example.com"
    fortune = ""

    with patch('fortunes.send_email.smtplib.SMTP') as mock_smtp:
        send_fortune_email(recipient_email, fortune)

        mock_smtp.assert_called_with("smtp.gmail.com", 587)
        instance = mock_smtp.return_value.__enter__.return_value
        instance.starttls.assert_called_once()
        instance.login.assert_called_once()
        instance.sendmail.assert_called_once()

def test_send_fortune_email_large_fortune():
    recipient_email = "test@example.com"
    fortune = "🔮 " + "Your Fortune is very bright! " * 1000  # Create a very large fortune message

    with patch('fortunes.send_email.smtplib.SMTP') as mock_smtp:
        send_fortune_email(recipient_email, fortune)

        mock_smtp.assert_called_with("smtp.gmail.com", 587)
        instance = mock_smtp.return_value.__enter__.return_value
        instance.starttls.assert_called_once()
        instance.login.assert_called_once()
        instance.sendmail.assert_called_once()

def test_send_fortune_email_with_special_characters():
    recipient_email = "test@example.com"
    fortune = "🔮 Your Fortune: 🎉 Congratulations! 💸 Money is coming your way! 🍀 Lucky Number: 88"

    with patch('fortunes.send_email.smtplib.SMTP') as mock_smtp:
        send_fortune_email(recipient_email, fortune)

        mock_smtp.assert_called_with("smtp.gmail.com", 587)
        instance = mock_smtp.return_value.__enter__.return_value
        instance.starttls.assert_called_once()
        instance.login.assert_called_once()
        instance.sendmail.assert_called_once()

# sample quotes dictionary
quotes_dict = {
    "Albert Claude": [
        "Once Ptolemy and Plato, yesterday Newton, today Einstein, and tomorrow new faiths, new beliefs, and new dimensions.",
        "When I went to the University, the medical school was the only place where one could hope to find the means to study life, its nature, its origins, and its ills.",
        "Looking back 25 years later, what I may say is that the facts have been far better than the dreams. In the long course of cell life on this earth it remained, for our age for our generation, to receive the full ownership of our inheritance.",
    ],
    "Mikhail Bakunin": [
        "The urge to destroy is also a creative urge.",
        "If God really existed, it would be necessary to abolish Him.",
        "People go to church for the same reasons they go to a tavern: to stupefy themselves, to forget their misery, to imagine themselves, for a few minutes anyway, free and happy."
    ]
}

@patch('builtins.input', side_effect=['Albert Claude', 'one'])
@patch('fortunes.get_quotes_by_author.random.choice', return_value="Once Ptolemy and Plato, yesterday Newton, today Einstein, and tomorrow new faiths, new beliefs, and new dimensions.")
@patch('fortunes.get_quotes_by_author.random.randint', return_value=42)
def test_get_one_quote(mock_input, mock_choice, mock_randint):

    quotes = get_quotes_by_author(quotes_dict)
    assert len(quotes) == 1
    assert "🔮 Your Fortune: Once Ptolemy and Plato, yesterday Newton, today Einstein, and tomorrow new faiths, new beliefs, and new dimensions." in quotes[0]
    assert "🍀 Your Lucky Number: 42" in quotes[0]

@patch('builtins.input', side_effect=['Mikhail Bakunin', 'multiple', '2'])
@patch('fortunes.get_quotes_by_author.random.sample', return_value=[
    "The urge to destroy is also a creative urge.",
    "If God really existed, it would be necessary to abolish Him."
])
@patch('fortunes.get_quotes_by_author.random.randint', side_effect=[17, 23])
def test_get_multiple_quotes(mock_input, mock_sample, mock_randint):

    quotes = get_quotes_by_author(quotes_dict)
    assert len(quotes) == 2
    assert "🔮 Your Fortune: The urge to destroy is also a creative urge." in quotes[0]
    assert "🍀 Your Lucky Number: 17" in quotes[0]
    assert "🔮 Your Fortune: If God really existed, it would be necessary to abolish Him." in quotes[1]
    assert "🍀 Your Lucky Number: 23" in quotes[1]

@patch('builtins.input', side_effect=['Non Existent Author'])
def test_invalid_author(mock_input):
    with pytest.raises(StopIteration):
        get_quotes_by_author(quotes_dict)

@patch('builtins.input', side_effect=['Albert Claude', 'multiple', '10'])
@patch('fortunes.get_quotes_by_author.random.sample', return_value=[
    "Once Ptolemy and Plato, yesterday Newton, today Einstein, and tomorrow new faiths, new beliefs, and new dimensions.",
    "When I went to the University, the medical school was the only place where one could hope to find the means to study life, its nature, its origins, and its ills.",
    "Looking back 25 years later, what I may say is that the facts have been far better than the dreams. In the long course of cell life on this earth it remained, for our age for our generation, to receive the full ownership of our inheritance."
])
@patch('fortunes.get_quotes_by_author.random.randint', side_effect=[5, 12, 30])
def test_get_more_quotes_than_available(mock_input, mock_sample, mock_randint):

    quotes = get_quotes_by_author(quotes_dict)
    assert len(quotes) == 3
    assert "🔮 Your Fortune: Once Ptolemy and Plato, yesterday Newton, today Einstein, and tomorrow new faiths, new beliefs, and new dimensions." in quotes[0]
    assert "🍀 Your Lucky Number: 5" in quotes[0]
    assert "🔮 Your Fortune: When I went to the University, the medical school was the only place where one could hope to find the means to study life, its nature, its origins, and its ills." in quotes[1]
    assert "🍀 Your Lucky Number: 12" in quotes[1]
    assert "🔮 Your Fortune: Looking back 25 years later, what I may say is that the facts have been far better than the dreams. In the long course of cell life on this earth it remained, for our age for our generation, to receive the full ownership of our inheritance." in quotes[2]
    assert "🍀 Your Lucky Number: 30" in quotes[2]

@patch('builtins.input', side_effect=['Albert Claude', 'invalid_choice'])
def test_invalid_choice(mock_input):
    with pytest.raises(StopIteration):
        get_quotes_by_author(quotes_dict)

@patch('builtins.input', side_effect=['Albert Claude', 'multiple', '-5'])
def test_negative_number_of_quotes(mock_input):
    with pytest.raises(StopIteration):
        get_quotes_by_author(quotes_dict)

@patch('builtins.input', side_effect=['Albert Claude', 'multiple', 'abc'])
def test_non_integer_number_of_quotes(mock_input):
    with pytest.raises(StopIteration):
        get_quotes_by_author(quotes_dict)