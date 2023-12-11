# Dimensions Scientometric Analysis Framework

This repository contains Python code designed to interact with the Dimensions API for scientometric analysis. The framework allows users to perform queries, retrieve data, and analyze research-related information using the Dimensions database.

## Getting Started

Follow these steps to set up and use the scientometric analysis framework:

### 1. Clone the Repository

```bash
git clone https://github.com/dsrestrepo/Dimensions.git
cd Dimensions
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Create a .env file

Create a `.env` file in the root directory of the repository with the following content:

```env
DIMENSIONS_API_KEY=your_dimensions_api_key
```

Replace `your_dimensions_api_key` with your actual Dimensions API key.

### 4. Run the Example Notebook

Run the provided example notebook (`example.ipynb`) to ensure everything is set up correctly:

This notebook demonstrates how to use the `DimcliQuery` class to search for publications related to a specific topic.

### 5. Customize and Integrate

Modify the `DimcliQuery` class to fit your specific scientometric analysis needs. You can extend the class with additional methods, query parameters, or result processing based on your research objectives.

## Usage

```python
from dimensions import DimensionsQuery

# Search Query:
SEARCH = 'publications'
TOPIC = 'machine learning and healthcare'

YEAR = [2020, 2023]
WHERE = f'year in [{YEAR[0]}:{YEAR[1]}] and times_cited > 10'

COLUMNS = 'id+title+authors+pages+type+volume+year+journal+issue+times_cited'

# Create an instance of DimensionsQuery
dimensions_query = DimensionsQuery(topic=TOPIC, where=WHERE, return_cols=COLUMNS, search=SEARCH)

# Run the query
response = dimensions_query.run_query()

dimensions_query.results.head()
```

Customize the query parameters and result processing based on your specific analysis requirements.

## Contributing

If you have improvements or new features to suggest, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
