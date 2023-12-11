import dimcli
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import pandas as pd

# Load environment variables from .env
load_dotenv()

class DimensionsQuery:
    def __init__(self, topic='machine learning and healthcare', where=None, search = 'publications', return_cols=None, endpoint="https://app.dimensions.ai"):
        """
        Initializes a DimensionsQuery instance.

        Parameters:
        - topic (str): The topic for the query.
        - where (str): Additional conditions for the query.
        - search (str): The type of search (e.g., 'publications').
        - return_cols (srt): The columns to return in the query seperated by + (e.g., 'id+title+authors+pages+type+volume+year+journal.id+journal.title+issue+times_cited')
        - endpoint (str): The API endpoint for the Dimensions API.

        Raises:
        - ValueError: If API key is not found in the environment variables.
        """
        
        # Login
        self.endpoint = endpoint
        self.api_key = os.getenv("DIMENSIONS_API_KEY")
        self.dsl = self.validate_key()

        # Query attributes
        self.topic = topic
        self.where = where
        self.search = search
        self.return_cols = return_cols
        self.update_query()

    def validate_key(self):
        """
        Validates and logs in using the API key.

        Returns:
        - dimcli.Dsl: An instance of the Dimensions DSL.
        """
        if self.api_key is None:
            raise ValueError("API key not found. Make sure to set DIMENSIONS_API_KEY in your .env file.")

        dimcli.login(key=self.api_key, endpoint=self.endpoint)
        dsl = dimcli.Dsl()
        return dsl

    def update_query(self):
        """
        Updates the query based on the current topic, where clause, and search type.
        """
    
        if self.return_cols:
            _return = f'return {self.search}[{self.return_cols}]'
        else:
            _return = f'return {self.search}'

        if self.where:
            self.query = f'search {self.search} for "{self.topic}" where {self.where} {_return}'
        else:
            self.query = f'search {self.search} for "{self.topic}" {_return}'
    
            
    def update_topic(self, topic):
        """
        Updates the query topic and re-runs the query.

        Parameters:
        - topic (str): The new topic for the query.
        """
        self.topic = topic
        self.update_query()

    def update_where(self, where):
        """
        Updates the query where clause and re-runs the query.

        Parameters:
        - where (str): The new where clause for the query.
        """
        self.where = where
        self.update_query()

    def update_search(self, search):
        """
        Updates the query search type and re-runs the query.

        Parameters:
        - search (str): The new search type for the query.
        """
        self.search = search
        self.update_query()

    def run_query(self, df=True):
        """
        Runs the Dimensions query.

        Parameters:
        - df (bool): If True, returns the results as a DataFrame.

        Returns:
        - dimcli.DslDataset or pd.DataFrame: The query response.
        """
        if self.query is None:
            raise ValueError("Query not specified. Use update_query method to set the query.")

        response = self.dsl.query(self.query)
        print(f"Done! {response.stats['total_count']} results available")
        print("Errors: ", response.errors)

        if df:
            response = response.as_dataframe()

        self.results = response
        return response.copy()


    def analyze_results(self):
        """
        Analyzes the results of the Dimensions query.

        This method should be called after running the query.

        Plots and displays the most common journal, top authors, countries, and institutions.
        """
        if self.results is None:
            raise ValueError("No results to analyze. Run the query first.")

        # Convert results to DataFrame
        if isinstance(self.results, pd.DataFrame):
            df = self.results.copy()
        else:
            df = self.results.as_dataframe().copy()

        # Most Common Journal
        self.plot_most_common_journal(df)

        # Publications per Author
        self.plot_publications_per_author(df)

        # Most Common Country
        self.plot_most_common_country(df)

        # Most Common Institutions
        self.plot_most_common_institutions(df)
  
    def plot_most_common_journal(self, df):
        """
        Plots and displays the top 10 most common journals in the query results.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the query results.
        """

        print('#'*40, f' Most common Journal ' , '#'*40)
        journal_counts = df['journal.title'].value_counts()
        top_journals = journal_counts.head(10)

        # Plot
        top_journals.plot(kind='bar', color='skyblue')
        plt.title(f'Top 10 Journals in {self.topic} Publications')
        plt.xlabel('Journal')
        plt.ylabel('Number of Publications')
        plt.show()

        # Display frequency in a table
        top_journals_table = pd.DataFrame(top_journals.reset_index())
        top_journals_table.columns = ['Journal', 'Number of Publications']
        print(top_journals_table)


    def plot_publications_per_author(self, df):
        """
        Plots and displays the top 10 authors with the highest number of publications.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the query results.
        """
        print('#'*40, f' Publications Per Author ' , '#'*40)
        authors_df = pd.DataFrame([author for authors in df['authors'] for author in authors])
        author_counts = authors_df['researcher_id'].value_counts()
        top_authors = author_counts.head(10)

        # Plot
        top_authors.plot(kind='bar', color='salmon')
        plt.title(f'Top 10 Authors in {self.topic} Publications')
        plt.xlabel('Researcher ID')
        plt.ylabel('Number of Publications')
        plt.show()

        # Display frequency in a table
        top_authors_table = pd.DataFrame(top_authors.reset_index())
        top_authors_table.columns = ['Researcher ID', 'Number of Publications']
        print(top_authors_table)


    def plot_most_common_country(self, df):
        """
        Plots and displays the top 10 countries with the highest number of publications.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the query results.
        """
        print('#'*40, f' Publications Per Country ' , '#'*40)
        authors_df = pd.DataFrame([author for authors in df['authors'] for author in authors])
        country_counts = authors_df['affiliations'].apply(lambda x: x[0]['country'] if x else None).value_counts()
        top_countries = country_counts.head(10)

        # Plot
        top_countries.plot(kind='bar', color='lightgreen')
        plt.title(f'Top 10 Countries in {self.topic} Publications')
        plt.xlabel('Country')
        plt.ylabel('Number of Publications')
        plt.show()

        # Display frequency in a table
        top_countries_table = pd.DataFrame(top_countries.reset_index())
        top_countries_table.columns = ['Country', 'Number of Publications']
        print(top_countries_table)


    def plot_most_common_institutions(self, df):
        """
        Plots and displays the top 10 institutions with the highest number of publications.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing the query results.
        """
        print('#'*40, f' Publications Per Institutions ' , '#'*40)
        authors_df = pd.DataFrame([author for authors in df['authors'] for author in authors])
        institution_counts = authors_df['affiliations'].apply(lambda x: x[0]['name'] if x else None).value_counts()
        top_institutions = institution_counts.head(10)

        # Plot
        top_institutions.plot(kind='bar', color='lightcoral')
        plt.title(f'Top 10 Institutions in {self.topic} Publications')
        plt.xlabel('Institution')
        plt.ylabel('Number of Publications')
        plt.show()

        # Display frequency in a table
        top_institutions_table = pd.DataFrame(top_institutions.reset_index())
        top_institutions_table.columns = ['Institution', 'Number of Publications']
        print(top_institutions_table)

