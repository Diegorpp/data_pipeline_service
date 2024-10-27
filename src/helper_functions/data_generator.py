import pandas as pd
from datetime import datetime
from random import choice


def generate_more_data(csv_file: str, num_generated_rows: int) -> None:
    """Read a CSV file and generate another samples to generate a bigger file
    and save it as another csv file.
    """
    df = pd.read_csv(csv_file)
    datasource_list = df['datasource'].unique()
    region_list = df['region'].unique()
    origin = df['origin_coord'].unique()[:20]
    dst = df['destination_coord'].unique()[:20]
    dtime = str(datetime.now()).split('.')[0]

    for idx in range(num_generated_rows):
        # data = {'region':choice(region_list),'datasource':choice(datasource_list),'origin_coord':choice(origin),'destination_coord':choice(dst),'datatime':dtime}
        data = {
            'region':choice(region_list),
            'datasource':choice(datasource_list),
            'origin_coord':choice(origin),
            'destination_coord':choice(dst),
            'datatime':dtime
        }


        pass
    breakpoint()

    return df


if __name__ == '__main__':
    csv_file = '../data/trips_small.csv'
    generate_more_data(csv_file=csv_file)