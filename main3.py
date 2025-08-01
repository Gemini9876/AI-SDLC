Okay, here's a requirement document for a "random" Python project that, if implemented fully, would easily span 200 lines of diverse Python code. The goal is to touch upon various aspects of the language and its standard libraries without necessarily forming one cohesive, logical application.

---

**Project Title: "Python Feature Showcase & Data Munger"**

**Overall Goal:** Implement a series of disconnected but functional Python scripts/modules demonstrating proficiency in core language features, data handling, basic networking, system interaction, and more. Each requirement below should be implemented as a separate function, class, or script where appropriate, with clear documentation (docstrings, comments).

---

**Requirements:**

**I. Core Python Features & Data Structures (Approx. 60 lines)**

1.  **List Comprehension & Filtering:**
    *   Create a function `filter_even_squares(numbers)` that takes a list of integers.
    *   It should return a new list containing only the squares of even numbers from the input list, using a list comprehension.
    *   Example: `filter_even_squares([1, 2, 3, 4, 5, 6])` should return `[4, 16, 36]`.
2.  **Dictionary Operations:**
    *   Write a function `merge_dicts(d1, d2)` that merges two dictionaries `d1` and `d2`. If a key exists in both, the value from `d2` should override `d1`.
    *   Also, add a function `find_max_value_key(data_dict)` that returns the key associated with the maximum numeric value in a given dictionary. Handle cases where the dictionary might be empty or values are not numeric.
3.  **Class Definition & Instance Methods:**
    *   Define a class `Product` with attributes `name` (string), `price` (float), and `quantity` (int).
    *   Include an `__init__` method.
    *   Add a method `get_total_cost()` that returns `price * quantity`.
    *   Add a method `apply_discount(percentage)` that reduces the price by the given percentage (e.g., 10 for 10%). Ensure the percentage is valid (0-100).
4.  **Generators:**
    *   Create a generator function `countdown(n)` that yields numbers from `n` down to 1.
    *   Demonstrate its usage with a `for` loop.
5.  **Decorators:**
    *   Implement a simple decorator `timer_decorator` that measures the execution time of any function it decorates and prints it to the console.
    *   Apply this decorator to a sample function that performs a short, time-consuming operation (e.g., summing a large list).
6.  **Context Managers:**
    *   Create a custom context manager `FileLogger` using `__enter__` and `__exit__`.
    *   It should take a filename as an argument. When entering the context, it opens the file. When exiting, it closes the file.
    *   Inside the `__enter__` method, it should return the file object.
    *   Demonstrate its use by writing a few lines to a file within a `with` statement.

**II. File Operations & Data Parsing (Approx. 50 lines)**

7.  **CSV Reader & Processor:**
    *   Create a script `process_sales.py` that reads a CSV file named `sales_data.csv`.
    *   Assume `sales_data.csv` has columns: `Item`, `Quantity`, `PricePerUnit`.
    *   Calculate the total revenue for each item and print it.
    *   Handle `FileNotFoundError` gracefully.
8.  **JSON Saver & Loader:**
    *   Write a function `save_data_to_json(data, filename)` that takes a Python dictionary/list and saves it as a JSON file.
    *   Write a function `load_data_from_json(filename)` that loads data from a JSON file and returns it as a Python object.
    *   Demonstrate saving and then loading a sample dictionary.
9.  **Log File Analyzer:**
    *   Simulate a log file (create `app.log` with a few lines, including some "ERROR" and "WARNING" lines).
    *   Write a function `analyze_log_file(log_filename)` that reads the log file line by line.
    *   Count the occurrences of "ERROR" and "WARNING" messages and print the counts.

**III. Web Interaction & Networking (Approx. 40 lines)**

10. **Simple API Data Fetcher:**
    *   Use the `requests` library (assume installed) to make an HTTP GET request to a public API (e.g., `https://jsonplaceholder.typicode.com/posts/1`).
    *   Parse the JSON response and print a specific field (e.g., "title").
    *   Implement error handling for network issues or bad responses (e.g., 404, 500).
11. **Basic Web Scraper (HTML Parsing):**
    *   Use `requests` to fetch the content of a simple webpage (e.g., `http://quotes.toscrape.com/`).
    *   Use `BeautifulSoup` (assume installed) to parse the HTML.
    *   Extract and print the text of the first 5 quotes on the page.
12. **Simple UDP Sender/Receiver:**
    *   Implement two separate scripts: `udp_sender.py` and `udp_receiver.py`.
    *   `udp_sender.py` should send a predefined message (e.g., "Hello UDP!") to `localhost` on a specific port (e.g., 12345).
    *   `udp_receiver.py` should listen on the same port, receive the message, and print it.

**IV. System & Utility Operations (Approx. 30 lines)**

13. **Directory Lister & Sorter:**
    *   Write a function `list_and_sort_files(directory_path)` that takes a directory path.
    *   It should list all files (not subdirectories) in that directory.
    *   Return a list of filenames, sorted alphabetically.
    *   Handle cases where the directory does not exist.
14. **Process Executor:**
    *   Use the `subprocess` module to execute a simple command (e.g., `ls -l` on Linux/macOS or `dir` on Windows).
    *   Capture its standard output and standard error, and print both.
15. **Date and Time Utility:**
    *   Create a function `days_until_event(year, month, day, event_name)` that calculates and prints the number of days remaining until a specified future date.
    *   Example: "There are X days until Christmas!"

**V. Error Handling & Logging (Approx. 20 lines)**

16. **Custom Exception:**
    *   Define a custom exception class `InvalidInputError` that inherits from `Exception`.
    *   Create a function `process_value(value)` that raises `InvalidInputError` if `value` is negative.
    *   Demonstrate catching this custom exception.
17. **Basic Logging Setup:**
    *   Configure Python's `logging` module to output messages to both the console (INFO level) and a file named `app_debug.log` (DEBUG level).
    *   Use `logging.debug()`, `logging.info()`, `logging.warning()`, `logging.error()`.

---

**Implementation Notes:**

*   Each numbered requirement should ideally translate into at least one distinct function, method, or small script.
*   Include comments and docstrings where necessary to explain logic and purpose.
*   Use f-strings for formatting output.
*   Assume necessary third-party libraries (`requests`, `beautifulsoup4`) are installed for the web-related tasks.
*   For tasks involving file creation, ensure the script can run without pre-existing files (it should create them if needed).