# Anthropic Agent in Docker

**Description**
This is an anthropic AI agent that analyzes CSV data and generates new rows based on analysis results. The agent uses OpenAI's Sonnet model to generate text and Docker to containerize the application.

**Features**

1. **Analyzer Agent**: Analyzes a given CSV file, identifying its structure, patterns, and meaning.
2. **Generator Agent**: Generates new CSV rows based on analysis results and sample data.
3. **Docker Containerization**: The agent is packaged in a Docker container for easy deployment and management.

**Prerequisites**

1. Python 3.11 or higher
2. Docker installed
3. Annotated Types, Anthropic, AnyIO, Certifi, and other dependencies (listed below)

**Dependencies**
See `requirements.txt` file for the list of dependencies.

**How to Use**

1. Run the Docker container: `docker run -it <image_name>`
2. Pass a CSV file as an argument to the agent: `<agent_name> analyze <csv_file>`
3. Generate new CSV rows based on analysis results and sample data: `<agent_name> generate <num_rows>`

**Code Structure**

The project consists of the following files:

* `prompts.py`: Defines system and user prompts for the analyzer and generator agents.
* `agents.py`: Contains the implementation of the analyzer and generator agents.
* `Dockerfile`: Builds a Docker image for the agent.
* `.pylintrc`: Configures Python linter settings.

**Additional Information**

For more information on how to use the agents or customize their behavior, refer to the code comments and prompts in `prompts.py` and `agents.py`.

I hope this helps! Let me know if you have any further questions.