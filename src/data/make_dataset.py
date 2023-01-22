"""Load the dataset and provide some basic info."""
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import numpy as np
import pandas as pd
import OpenBlender
import json


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()



class dataset():
    def load():
        dataset = pd.read_excel('../data/raw/2020Q1Q2Q3Q4-2021Q1.xlsx', sheet_name = None,
                                parse_dates=['Date'], index_col = 'Date', skipfooter=1)

        #check how many sheets are in the file
        print('Sheets in dataset: ',len(dataset.keys()))

        #Some basic info for every sheet in dataset.
        for sheet in range(len(dataset.keys())):
            each_set = dataset[list(dataset.keys())[sheet]]
            print(f'----------Name of dataset is "{list(dataset.keys())[sheet]}"----------')
            print(each_set.head())
            print(f'Null values in dataset are \n{each_set.isnull().sum()}')
            print(f'Duplicated values in dataset are {each_set.duplicated().sum()}')
            print('\n\n\n')

        return dataset

    def convert_vol(dataset):
        for sheet in range(len(dataset.keys())):
            each_set = dataset[list(dataset.keys())[sheet]]
            each_set['Vol.'] = each_set['Vol.'].apply(lambda x: float(x.strip('M'))*1000000 if x[-1]=='M'
                                                        else (float(x.strip('K'))*1000 if x[-1]=='K'
                                                              else(float(x.replace('-','0')) if x[-1]=='-' else x)))
        return dataset
    def load_apple_dataset():
        """ This function will download Apple stocks dataset using an api."""

        token = '63cd98c09516297b5fcd8293btc3HguH1xKdFsWILmZRu16j1tnF52'
        # Specify the action
        action = 'API_getObservationsFromDataset'
        interval = 60 * 60 * 24 # One day
        parameters = { 'token' : token,
                        'id_dataset':'5d4c39d09516290b01c8307b',
                        'date_filter':{"start_date":"2017-01-01T06:00:00.000Z",
                        "end_date":"2020-02-09T06:00:00.000Z"},
                        'aggregate_in_time_interval' : {
                        'time_interval_size' : interval,
                        'output' : 'avg',
                        'empty_intervals' : 'impute'
                    }
                }

        # Pull the data into a Pandas Dataframe
        df = pd.read_json(json.dumps(OpenBlender.call(action, parameters)['sample']), convert_dates=False, convert_axes=False)
        df.reset_index(drop=True, inplace=True)
        df['date'] = [OpenBlender.unixToDate(ts, timezone = 'GMT') for ts in df.timestamp]
        df = df.drop('timestamp', axis = 1)

        return df