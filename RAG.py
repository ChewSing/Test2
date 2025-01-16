import pandas as pd 
import openai 

class ExcelProcessor:
    def __init__(self, file_path, api_key):
        self.file_path = file_path
        self.api_key = api_key
        self.data = None
        openai.api_key = self.api_key
    
    def read_excel(self):
        """
        Reads the Excel file into a pandas DataFrame.
        """
        try:
            self.data = pd.read_excel(self.file_path)
            print(f"Excel file '{self.file_path}' successfully loaded.")
        except Exception as e:
            raise ValueError(f"Error reading the Excel file: {e}")
    
    def process_data(self):
        """
        Processes the data and returns key statistics as a dictionary.
        """
        if self.data is None:
            raise ValueError("No data found. Please read the Excel file first.")
        try:
            # Example metrics for processing
            return {
                "average_salary": self.data["Salary"].mean(),
                "department_distribution": self.data["Department"].value_counts().to_dict()
            }
        except KeyError as e:
            raise KeyError(f"Missing column in the data: {e}")
        
    def summarize_with_gpt(self, processed_data):
        """
        Uses OpenAI GPT API to summarize the processed data.
        """
        try:
        # Prepare the prompt for GPT in the format of a conversation (as required by chat models)
            messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following data insights:\n\n"
                                       f"Average Salary: {processed_data['average_salary']}\n"
                                       f"Department Distribution: {processed_data['department_distribution']}\n"}
            ]
        
        # Call OpenAI GPT API with the chat model
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or use gpt-4 if you have access
            messages=messages,
            max_tokens=150,
            temperature=0.5,
            )
        
        # Extract the generated summary from the response
            summary = response['choices'][0]['message']['content'].strip()
            return summary
        except Exception as e:
            raise RuntimeError(f"Error generating summary: {e}")

    def save_summary(self, summary, output_path):
        """
        Saves the summary to a text file.
        """
        try:
            with open(output_path, "w") as file:
                file.write(summary)
            print(f"Summary successfully saved to '{output_path}'.")
        except Exception as e:
            raise IOError(f"Error saving the summary: {e}")
        
#Demonstrating RAG system
if __name__ == "__main__":
    # Define file paths and API key
    #API_KEY = "OPEN_API_KEY"
    INPUT_FILE = "C:/Users/lleon/OneDrive/Desktop/test 2/EmployeeData.xlsx"
    OUTPUT_FILE = "C:/Users/lleon/OneDrive/Desktop/test 2/summary.txt"

    # Initialize the processor
    processor = ExcelProcessor(INPUT_FILE, API_KEY)

    # Step 1: Read Excel data
    try:
        processor.read_excel()
    except ValueError as e:
        print(e)
        exit()
    
    # Step 2: Process data
    try:
        processed_data = processor.process_data()
    except KeyError as e:
        print(e)
        exit()
    
    # Step 3: Summarize data
    try:
        summary = processor.summarize_data(processed_data)
        print("\nGenerated Summary:\n", summary)
    except RuntimeError as e:
        print(e)
        exit()
    
    # Step 4: Save the summary
    try:
        processor.save_summary(summary, OUTPUT_FILE)
    except IOError as e:
        print(e)



