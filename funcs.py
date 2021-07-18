from clients import lang_base, style_base


# загружаем все сохраненные пользователем треки
def get_tracks(sp):
    collection = {'artist': [],
                  'artist_id': [],
                  'name': [],
                  'id': []}
    i = 0
    while True:
        results = sp.current_user_saved_tracks(limit=50, offset=i)
        if len(results['items']) != 0:
            for item in results['items']:
                track = item['track']
                collection['artist'].append(track['artists'][0]['name'])
                collection['artist_id'].append(track['artists'][0]['id'])
                collection['name'].append(track['name'])
                collection['id'].append(track['id'])
            i += 50
        else:
            break
    return collection


# в spotify чаще всего музыкальный жанр не указан ни у трека, ни у альбома,
# зато почти всегда указан у артиста, поэтому считаем количество песен в коллекции каждого исполнителя
def get_artists(collection):
    artists = {}
    for artist_id in collection['artist_id']:
        if artist_id not in artists:
            artists[artist_id] = 0
        artists[artist_id] += 1
    return dict(sorted(artists.items(), key=lambda item: -item[1]))


# для дальнейшего анализа посчитаем частоту различных языков (более корректно: это региональное происхождение
# музыкальных жанров)
def langs_freq(genres):
    langs = {'russian': 0, 'french': 0, 'italian': 0, 'spanish': 0, 'uk': 0, 'german': 0, 'latino': 0, 'korean': 0,
             'japanese': 0, 'mexican': 0, 'scandinavian': 0, 'central asian': 0}
    for genre in genres:
        for lang in langs:
            if lang in genre:
                langs[lang] += genres[genre]
    langs = dict(sorted(langs.items(), key=lambda item: -item[1]))
    langs_list = list(langs.items())
    return langs_list


# а также считаем частоту вхождения более базовых музыкальных стилей среди всевозможных жанров
def styles_freq(genres):
    styles = {'rock': 0, 'hip hop': 0, 'rap': 0, 'pop': 0, 'soul': 0, 'r&b': 0, 'reggae': 0, 'jazz': 0,
              'electro': 0, 'emo': 0, 'dance': 0, 'indie': 0, 'punk': 0, 'metal': 0}
    for genre in genres:
        for key in styles:
            if key in genre:
                styles[key] += genres[genre]
    styles = dict(sorted(styles.items(), key=lambda item: -item[1]))
    style_list = list(styles.items())
    return style_list


# будем включать в подходящиие базы те, которые соответсвуют двум самым популярным регионам и стилям (или меньше,
# если столько не встречается)
def suitable_cocktail_bases(langs_frequency, styles_frequency):
    suitable_bases = []
    for ind in range(2):
        if langs_frequency[ind][1] > 0:
            for i in range(len(lang_base[langs_frequency[ind][0]])):
                suitable_bases.append(lang_base[langs_frequency[ind][0]][i])
        if styles_frequency[ind][1] > 0:
            for i in range(len(style_base[styles_frequency[ind][0]])):
                suitable_bases.append(style_base[styles_frequency[ind][0]][i])
    return suitable_bases
