import pandas as pd

# на основании страны/местности происхождения алкоголя составим словарь "регион_базы"
lang_base = {'russian': ['водке'], 'french': ['вине', 'коньяке', 'игристом', 'кальвадосе'],
             'italian': ['вермуте', 'граппе', 'самбуке'], 'spanish': ['хересе', 'ликере', 'вине'],
             'uk': ['джине', 'чае'], 'german': ['пиве'], 'latino': ['мескале', 'писко', 'кашасе'],
             'japanese': ['саке'], 'korean': ['соджу'], 'mexican': ['текиле'], 'scandinavian': ['аквавите'],
             'central asian': ['араке']}
# на основании ассоциаций (пусть и субъективных), а также более некоторых общепринятых мнений
# относительно музыки, подходящей конкретному алкогольному напитку, составим словарь "муз.стиль_базы"
style_base = {'rock': ['виски'], 'hip hop': ['бурбоне'], 'rap': ['пиве'], 'pop': ['игристом', 'газировке', 'содовой'],
              'jazz': ['джине'], 'r&b': ['ликере'], 'reggae': ['роме'], 'electro': ['текиле', 'кофе', 'энергетике'],
              'emo': ['вине'], 'dance': ['вермуте'], 'indie': ['соке'], 'punk': ['водке'], 'metal': ['абсенте']}


class SuitableCocktailFinder:

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def __call__(self, base: str) -> str:
        indexes_match_queries = self.data.apply(
            lambda row: base in row['drinks_bases'],
            axis=1,
        )
        data_sample = self.data[indexes_match_queries]
        random_query_response = data_sample.sample(1)
        return random_query_response.index
