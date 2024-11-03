import pathlib

import pandas as pd

from ddi_fw.langchain.embeddings import PoolingStrategy
from .. import BaseDataset
from ..db_utils import create_connection

HERE = pathlib.Path(__file__).resolve().parent
list_of_embedding_columns = ['all_text', 'description',
                     'synthesis_reference', 'indication',
                     'pharmacodynamics', 'mechanism_of_action',
                     'toxicity', 'metabolism',
                     'absorption', 'half_life',
                     'protein_binding', 'route_of_elimination',
                     'volume_of_distribution', 'clearance']

list_of_chemical_property_columns = ['enzyme',
                             'target',
                             'pathway',
                             'smile']
list_of_ner_columns = ['tui', 'cui', 'entities']


class DDIMDLDataset(BaseDataset):
    def __init__(self, embedding_size,
                 embedding_dict,
                 embeddings_pooling_strategy: PoolingStrategy,
                 ner_df,
                 chemical_property_columns=['enzyme',
                                            'target',
                                            'pathway',
                                            'smile'],
                 embedding_columns=[],
                 ner_columns=[],
                 **kwargs):
        columns = kwargs['columns']
        if columns is not None:
            chemical_property_columns = []
            embedding_columns=[]
            ner_columns=[]
            for column in columns:
                if column in list_of_chemical_property_columns:
                    chemical_property_columns.append(column)
                elif column in list_of_embedding_columns:
                    embedding_columns.append(column)
                elif column in list_of_ner_columns:
                    ner_columns.append(column)
                else:
                    raise Exception(f"{column} is not related this dataset")


        super().__init__(embedding_size=embedding_size,
                         embedding_dict=embedding_dict,
                         embeddings_pooling_strategy=embeddings_pooling_strategy,
                         ner_df=ner_df,
                         chemical_property_columns=chemical_property_columns,
                         embedding_columns=embedding_columns,
                         ner_columns=ner_columns,
                         **kwargs)

        # kwargs = {'index_path': str(HERE.joinpath('indexes'))}
        kwargs['index_path'] = str(HERE.joinpath('indexes'))

        db = HERE.joinpath('data/event.db')
        conn = create_connection(db)
        print("db prep")
        self.drugs_df = self.__select_all_drugs_as_dataframe__(conn)
        self.ddis_df = self.__select_all_events__(conn)
        print("db bitti")
        self.index_path = kwargs.get('index_path')

    def __select_all_drugs_as_dataframe__(self, conn):
        headers = ['index', 'id', 'name',
                   'target', 'enzyme', 'pathway', 'smile']
        cur = conn.cursor()
        cur.execute(
            '''select "index", id, name, target, enzyme, pathway, smile from drug''')
        rows = cur.fetchall()
        df = pd.DataFrame(columns=headers, data=rows)
        df['enzyme'] = df['enzyme'].apply(lambda x: x.split('|'))
        df['target'] = df['target'].apply(lambda x: x.split('|'))
        df['pathway'] = df['pathway'].apply(lambda x: x.split('|'))
        df['smile'] = df['smile'].apply(lambda x: x.split('|'))
        return df

    def __select_all_events__(self, conn):
        """
        Query all rows in the event table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute('''
                select ex."index", d1.id, d1.name, d2.id, d2.name,  mechanism || ' ' ||action from extraction ex
                join drug d1 on  d1.name = ex.drugA
                join drug d2 on  d2.name = ex.drugB
        ''')

        rows = cur.fetchall()

        headers = ["index", "id1", "name1", "id2", "name2", "event_category"]
        return pd.DataFrame(columns=headers, data=rows)
