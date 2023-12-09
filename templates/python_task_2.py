import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here

    distances = df.pivot_table(index='id_start', columns='id_end', values='distance', fill_value=0)
    # Add missing values by summing distances along known routes
    for start in distances.index:
        for end in distances.columns:
            if distances.loc[start, end] == 0:
                routes = df[(df['id_start'] == start) & (df['id_end'] != end)]
                distances.loc[start, end] = routes['distance'].sum()
    # Set diagonal values to 0 and ensure symmetry
    distances.fillna(0, inplace=True)
    np.fill_diagonal(distances.values, 0)
    return distances.T + distances


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here

    return pd.DataFrame.from_dict({
        'id_start': df.index.to_numpy().repeat(len(df.columns)),
        'id_end': df.columns.to_numpy().flatten(),
        'distance': df.values.flatten()
    })


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here

    reference_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold = reference_distance * 0.1
    return list(
        df[(df['id_start'] == reference_id) &
              (df['distance'].between(reference_distance - threshold,
                                         reference_distance + threshold))]['id_end']
    )


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here

    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }
    for vehicle, rate_coefficient in rate_coefficients.items():
        df[vehicle] = df['distance'] * rate_coefficient
    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

   def calculate_time_range(distance):
    """
    Calculates the start and end times for a given distance.

    Args:
        distance (float): The distance.

    Returns:
        tuple: A tuple of (start_time, end_time).
    """
    average_speed = 50  # Adjust this value as needed
    travel_time = timedelta(seconds=distance / average_speed * 3600)

    start_time = time(0, 0)
    end_time = start_time + travel_time
    return start_time, end_time

def apply_discount_factor(data, idx, vehicle, start_time, end_time):
    """
    Applies discount factor based on time and vehicle type.

    Args:
        data (DataFrame): The unrolled distance matrix DataFrame.
        idx (int): The index of the row.
        vehicle (str): The vehicle type.
        start_time (time): The start time.
        end_time (time): The end time.
    """
    discount_factor = 1
    weekday = start_time.weekday()
    if weekday >= 0 and weekday <= 4:
        if start_time < time(10, 0):
            discount_factor = 0.8
        elif start_time >= time(10, 0) and end_time <= time(18, 0):
            discount_factor = 1.2
        else:
            discount_factor = 0.8
    else:
        discount_factor = 0.7

    data.loc[idx, vehicle] *= discount_factor
