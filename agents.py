import os
import csv
import anthropic
from prompts import ANALYZER_SYSTEM_PROMPT, ANALYZER_USER_PROMPT, GENERATOR_SYSTEM_PROMPT, GENERATOR_USER_PROMPT

if not os.getenv('ANTHROPIC_API_KEY'):
    os.environ['ANTHROPIC_API_KEY'] = input("Enter your Anthropic API key: ")

client = anthropic.Anthropic()
# https://docs.anthropic.com/en/docs/about-claude/models
sonnet = "claude-3-5-sonnet-20240620"

# Function to read the CSV file from the User
def read_csv(file_path):
    data = []
    # Open the CSV file in read mode
    with open(file_path, "r", newline="") as csvfile:
        # Create a CSV reader object
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # Add each row to the data list
            data.append(row)
    return data

# Function to save the generated data to a new CSV file
def save_to_csv(data, output_file, headers=None):
    # Set the file mode: 'w' (write) if headers are provided, else 'a' (append)
    mode = 'w' if headers else 'a'  
    with open(output_file, mode, newline="") as f:
        # Create a CSV writer object
        writer = csv.writer(f)  
        if headers:
            # Write the headers if provided
            writer.writerow(headers)
        # Split the data string into lines and create a CSV reader object
        for row in csv.reader(data.splitlines()):  
            writer.writerow(row)

# Create the Analyzer Agent. For more info: https://docs.anthropic.com/en/docs/quickstart
def analyzer_agent(sample_data):
    message = client.messages.create(
        model=sonnet,
        # Limit the response to 400 tokens
        max_tokens=400,
        # Set a low temperature for more focused, deterministic output
        temperature=0.1,
        # Use the predefined system prompt for the analyzer
        system=ANALYZER_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": ANALYZER_USER_PROMPT.format(sample_data=sample_data)
            # Format the user prompt with the provided sample data
            }
        ]
    )
    # Return the text content of the first message
    return message.content[0].text

# Create the Generator Agent
def generator_agent(analysis_result, sample_data, num_rows=30):
    message = client.messages.create(
        model=sonnet,
        # Allow for a longer response (1500 tokens)
        max_tokens=1500,
        # Set a high temperature for more creative, diverse output
        temperature=1,
        system=GENERATOR_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": GENERATOR_USER_PROMPT.format(
                    num_rows=num_rows,
                    analysis_result=analysis_result,
                    sample_data=sample_data
                )
                # Format the user prompt with the number of rows to generate, 
                # the analysis result, and the sample data
            }
        ]
    )
    return message.content[0].text

# Get input from the user
file_path = input("\nEnter the name of your CSV file: ")
file_path = os.path.join("/app/data", file_path)
desired_rows = int(input("\nEnter the number of rows you want to generate in the new dataset: "))

# Read the sample data from the input CSV file
sample_data = read_csv(file_path)
# Create a human-readable string representation of tabular data, which can be easily printed or written to a file.
sample_data_str = "\n".join([", ".join(row) for row in sample_data])

print("\nLaunching team of Agents...")
# Analyze the sample data using the Analyzer Agent
analysis_result = analyzer_agent(sample_data_str)
print("\n#### Analyzer Agent output: ####\n")
print(analysis_result)
print("\n----------------------------\n\nGenerating new data...")

# Set up the output file
output_file = "/app/data/new_dataset.csv"
headers = sample_data[0]

# Create the output file with headers
save_to_csv("", output_file, headers)

batch_size = 30  # Number of rows to generate in each batch
generated_rows = 0  # Counter to keep track of how many rows have been generated

# Generate data in batches until we reach the desired number of rows
while generated_rows < desired_rows:
    # Calculate how many rows to generate in this batch
    rows_to_generate = min(batch_size, desired_rows - generated_rows)
    
    # Generate a batch of data using the Generator Agent
    generated_data = generator_agent(analysis_result, sample_data_str, rows_to_generate)
    
    # Append the generated data to the output file
    save_to_csv(generated_data, output_file)
    
    # Update the count of generated rows
    generated_rows += rows_to_generate
    
    # Print progress update
    print(f"Generated {generated_rows} rows out of {desired_rows}")

print(f"\nNew dataset generated and saved to \"{output_file}\"")


