## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```sh
    python app.py
    ```

2. Open your web browser and navigate to `http://localhost:5000`.

3. Enter your research topic in the input field and click the "Research" button.

## Files Description

- `app.py`: Main Flask application that handles web requests and responses.
- `duck_research.py`: Contains the function to perform DuckDuckGo searches and scrape results.
- `graph/`: Contains the control flow and nodes for the state graph.
  - `control_flow.py`: Defines the workflow of the state graph.
  - `edges/`: Contains the edge functions for decision-making in the graph.
  - `nodes/`: Contains the node functions for various tasks like generating answers, grading documents, retrieving documents, and performing web searches.
- `ollama_helper.py`: Helper functions for generating search queries and creating summaries using the Ollama API.
- `ollama_wrapper.py`: Wrapper for the Ollama API.
- `vector_store.py`: Functions for adding and retrieving documents from the vector store.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.