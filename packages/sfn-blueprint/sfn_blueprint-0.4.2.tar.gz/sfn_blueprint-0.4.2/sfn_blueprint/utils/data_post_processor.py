import pandas as pd

class SFNDataPostProcessor:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def view_data(self, num_rows: int = 5) -> pd.DataFrame:
        """Returns a preview of the modified data."""
        return self.data.head(num_rows)

    def download_data(self, file_format: str = 'csv', file_name: str = 'modified_data'):
        """Generates a downloadable file in the specified format."""
        if file_format == 'csv':
            return self.data.to_csv(index=False).encode('utf-8')
        elif file_format == 'excel':
            output = pd.ExcelWriter(f'{file_name}.xlsx', engine='xlsxwriter')
            self.data.to_excel(output, index=False, sheet_name='Sheet1')
            output.save()
            return output.getvalue()
        else:
            raise ValueError("Unsupported file format. Choose 'csv' or 'excel'.")

    def summarize_data(self) -> pd.DataFrame:
        """Returns summary statistics of the data."""
        return self.data.describe()

    def reset_data(self, original_data: pd.DataFrame):
        """Resets the modified data to the original state."""
        self.data = original_data

    def export_to_database(self, connection, table_name: str):
        """Exports the modified data to a specified database table."""
        self.data.to_sql(table_name, connection, if_exists='replace', index=False)
        return f"Data exported to {table_name} table in the database."
