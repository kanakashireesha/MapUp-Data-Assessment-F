import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    car_matrix = df.pivot_table(index='id_1', columns='id_2', values='car', fill_value=0)
    np.fill_diagonal(car_matrix.values, 0)
    return car_matrix


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here

    df['car_type'] = pd.cut(df['car'], bins=[-1, 15, 25, 100], labels=['low', 'medium', 'high'])
    
    return df['car_type'].value_counts().to_dict()


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here

    mean_bus = df['bus'].mean()
    bus_filtered = df[df['bus'] > 2 * mean_bus]
    return bus_filtered.index.tolist()


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here

    filtered_routes = df.groupby('route')['truck'].mean()
    filtered_routes = filtered_routes[filtered_routes > 7]
    return filtered_routes.index.to_list()


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here

    matrix.loc[matrix > 20] *= 0.75
    matrix.loc[matrix <= 20] *= 1.25
    return matrix.round(decimals=1)


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here

    df['start_datetime'] = pd.to_datetime(df[['startDay', 'startTime']])
    df['end_datetime'] = pd.to_datetime(df[['endDay', 'endTime']])

    def check_time_range(row):
        start_time = row['start_datetime'].time()
        end_time = row['end_datetime'].time()
        return start_time <= end_time <= (start_time + pd.Timedelta(days=1))

    return df.groupby(['id', 'id_2'])['start_datetime'].apply(check_time_range)
