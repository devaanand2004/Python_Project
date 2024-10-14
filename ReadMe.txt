1. Install Python:
Ensure Python is installed on your system. Download it here if needed.

2. Open PyCharm:
Launch PyCharm.
Go to File > Open and select your project folder.

3. Set Up a Virtual Environment (Optional):
Navigate to File > Settings > Project: <your_project_name> > Python Interpreter.
Click the gear icon > Add > Choose New environment.

4. Install Required Libraries:
Open PyCharm’s terminal.
Run this command to install the libraries:
bash
Copy code
pip install requests beautifulsoup4 streamlit pillow lxml

5. Ensure Image Files Are Correct:
Verify that the Amazon and Flipkart logo images are in the correct paths in your script. If not, update the paths.

6. Run the Project in Streamlit:
In the PyCharm terminal, type the following to run the app:
bash
Copy code
streamlit run main.py
This opens the Streamlit app in your browser.

7. Use the App:
In the browser, enter the product name (e.g., "laptop") in the text input field.
Click the "Find Deal" button to start the price comparison.

8. View Results:
The app will display prices from Amazon and Flipkart, along with the best deal.

9. Check the Logs:
All logs (including errors or warnings) are saved in the price_tracker.log file in your project directory.