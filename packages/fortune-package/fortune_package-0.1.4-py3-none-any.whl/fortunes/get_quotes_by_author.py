# get_quotes_by_authors.py
import importlib.resources
import re
import random

def parse_fortune_file():
    quotes_dict = {}

    with importlib.resources.open_text('fortunes', 'fortune.txt') as file:
        content = file.read()
        
        # Split fortunes using '%' as separator
        fortunes = re.split(r'\n%\n', content)
        
        for fortune in fortunes:
            fortune = fortune.strip()
            if not fortune:
                continue  # Skip empty entries
                
            lines = fortune.split('\n')
            if not lines:
                continue
            
            # Get the last line for the author
            last_line = lines[-1].strip()
            
            # Check for author line starting with '~' or dashes
            author_match = re.match(r'^~\s*(.*)$|^[-–—]{1,2}\s*(.*)$', last_line)
            if author_match:
                author = author_match.group(1) or author_match.group(2)
                author = author.strip()
                quote = '\n'.join(lines[:-1]).strip()
                
                # Add quote to the author's list in quotes_dict
                if author:
                    quotes_dict.setdefault(author, []).append(quote)
            else:
                # If no author is found, you can decide to skip or handle differently
                continue
        
    return quotes_dict

def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Please enter a valid integer.")

def get_quotes_by_author(quotes_dict):
    """
    This function will return either a random quote or multiple quotes from a specified author.
    """
    # Display the available authors before prompting the user
    print("\nAvailable authors:")
    for author in sorted(quotes_dict.keys()):
        print(f"- {author}")

    while True:
        # Ask the user to input the person name that they want quotes from
        author = input("\nEnter the name of a famous person: ").strip()
        if author in quotes_dict:
            # Ask the user if they want one quote or multiple quotes
            choice = input("Do you want a random quote or multiple quotes? Enter 'one' or 'multiple': ").strip().lower()
            # User only wants one quote
            if choice == 'one':
                quote = random.choice(quotes_dict[author])
                formatted_quote = f"🔮 Your Fortune: {quote}\n🍀 Your Lucky Number: {random.randint(0, 99)}"
                print(f"\n{formatted_quote}\n  ~ {author}")
                return [formatted_quote]
            # User wants multiple quotes
            elif choice == 'multiple':
                num_quotes = get_positive_integer(f"How many quotes do you want from {author}? ")
                selected_quotes = random.sample(quotes_dict[author], min(num_quotes, len(quotes_dict[author])))

                quotes_list = []
                for quote in selected_quotes:
                    formatted_quote = f"🔮 Your Fortune: {quote}\n🍀 Your Lucky Number: {random.randint(0, 99)}"
                    quotes_list.append(formatted_quote)
                    print(f"{formatted_quote}\n  ~ {author}\n")
                return quotes_list
            else:
                print("Invalid choice. Please enter 'one' or 'multiple'.")
                continue  # Ask again
            break  # Exit the loop after displaying quotes
        # Did not find the person, ask user again
        else:
            print("Person not found. Please choose again.")

# if __name__ == "__main__":
#     q = parse_fortune_file()
#     get_quotes_by_author(q)