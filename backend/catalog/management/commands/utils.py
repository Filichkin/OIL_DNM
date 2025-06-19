import pandas as pd


def excel_preprocess(file_path):
    df = pd.read_excel(file_path)
    df = df.drop((df.index[0:12])).reset_index(drop=True)
    df = df.drop('Примечание к заказу:', axis=1)
    df = df.drop(index=0)
    df.columns = [
        'brand',
        'name',
        'part_number',
        'volume',
        'price_per_box',
        'price_per_litre',
        'avalible_count',
        'transit_count',
        'arrival_date',
        'updated_date',
        'specification'
        ]
    df['arrival_date'] = df['arrival_date'].fillna('')
    df['avalible_count'] = df['avalible_count'].fillna(0).astype('int32')
    df['transit_count'] = df['transit_count'].fillna(0).astype('int32')

    return df
