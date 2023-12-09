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
    # Get unique values from id_1 and id_2
    id_1_values = df['id_1'].unique()
    id_2_values = df['id_2'].unique()

    # Create an empty dataframe with id_1 as index and id_2 as columns
    car_matrix = pd.DataFrame(index=id_1_values, columns=id_2_values)

    # Iterate through each row in the dataframe
    for index, row in df.iterrows():
        id_1 = row['id_1']
        id_2 = row['id_2']
        car = row['car']
    
        # Set the car value in the car_matrix dataframe
        car_matrix.at[id_1, id_2] = car

    # Fill diagonal values with 0
    car_matrix.fillna(0, inplace=True)

    return car_matrix

    car_matrix = generate_car_matrix(df)
    print(car_matrix)

    #return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    # Add new categorical column car_type based on car values
    df['car_type'] = pd.cut(df['car'], bins=[-np.inf, 15, 25, np.inf], labels=['low', 'medium', 'high'])

    # Calculate count of occurrences for each car_type category
    type_count = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_count = dict(sorted(type_count.items(), key=lambda x: x[0]))

    return sorted_count

    #return dict()


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    mean_bus_value = df['bus'].mean()
    bus_indexes = df[dataframe['bus'] > 2 * mean_bus_value].index.tolist()
    return sorted(bus_indexes)

df = pd.read_csv('dataset-1.csv')
indexes = get_bus_indexes(df)
print(indexes)

    #return list()


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    # Group the DataFrame by the 'route' column and calculate the average of the 'truck' column for each group
    avg_truck = df.groupby('route')['truck'].mean()
    
    # Filter the routes where the average truck value is greater than 7
    filtered_routes = avg_truck[avg_truck > 7]
    
    # Sort the filtered routes and return as a list
    return sorted(filtered_routes.index.tolist())

df = pd.read_csv('dataset-1.csv')
filtered_routes = filter_routes(df)
print(filtered_routes)

    #return list()


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified_matrix = modified_matrix.round(1)
    return modified_matrix

df = pd.DataFrame('dataset-1.csv')
result =  multiply_matrix(df)
print(result)
    

    #return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    # Combine startDay and startTime columns into a single datetime column
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    
    # Combine endDay and endTime columns into a single datetime column
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    
    # Calculate the duration between start_datetime and end_datetime
    df['duration'] = df['end_datetime'] - df['start_datetime']
    
    # Group the data by id and id_2, and check if each group spans a full 24-hour period and all 7 days of the week
    completeness_check = df.groupby(['id', 'id_2']).apply(lambda x: 
        (x['duration'].min().days >= 7) and (x['duration'].max().days <= 7) and 
        (x['start_datetime'].min().time() == pd.Timestamp('00:00:00').time()) and 
        (x['end_datetime'].max().time() == pd.Timestamp('23:59:59').time())
    )
    
    return completeness_check

boolean_series = check_time_completeness(dataset_2_df)

    #return pd.Series()
