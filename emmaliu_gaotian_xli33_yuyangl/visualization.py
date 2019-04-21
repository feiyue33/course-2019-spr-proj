import dml
import prov.model
import datetime
import uuid
import folium
from folium.plugins import HeatMap
import os
import re
import time
from google.cloud import translate
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Google Cloud
# To get the credential:
# 1. Create or select a project.
# 2. Enable the Cloud Translation API for that project.
# 3. Create a service account.
# 4. Download a private key as JSON.
credential_path = "../auth.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
translate_client = translate.Client()
analyzer = SentimentIntensityAnalyzer()


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


class visualization(dml.Algorithm):

    contributor = 'gaotian_xli33'
    reads = ['emmaliu_gaotian_xli33_yuyangl.tweets']
    writes = []

    @staticmethod
    def execute(trial=False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''

        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('emmaliu_gaotian_xli33_yuyangl', 'emmaliu_gaotian_xli33_yuyangl')

        # Get Tweets data
        tweetsData = repo.emmaliu_gaotian_xli33_yuyangl.tweets.find()

        # create heatmap
        heat_map = folium.Map(location=[31.947, 35.925])
        # create sentiment map
        sentiment_map = folium.Map(location=[31.947, 35.925])

        coordinates = []
        count = 0
        for item in tweetsData:
            if item['geo']:
                coordinates.append((item['geo']['coordinates'][0], item['geo']['coordinates'][1]))
                translated_text = translate_client.translate(remove_emoji(item['text']), target_language='en')['translatedText']
                vs = analyzer.polarity_scores(translated_text)
                # print("{:-<65} {}".format(sentence, str(vs)))
                if vs['compound'] < 0:
                    color = 'blue'
                    icon = 'thumbs-down'
                elif vs['compound'] > 0:
                    color = 'red'
                    icon = 'thumbs-up'
                else:
                    color = 'orange'
                    icon = ''
                folium.Marker(
                    location=[item['geo']['coordinates'][0], item['geo']['coordinates'][1]],
                    popup=item['text'],
                    icon=folium.Icon(color=color, icon=icon)
                ).add_to(sentiment_map)
                count += 1
                print(count)
                time.sleep(.6)

        HeatMap(coordinates).add_to(heat_map)

        heat_map.save('heat_map.html')
        sentiment_map.save('sentiment_map.html')


        repo.logout()

        endTime = datetime.datetime.now()

        return {"start": startTime, "end": endTime}

    @staticmethod
    def provenance(doc=prov.model.ProvDocument(), startTime=None, endTime=None):
        '''
            Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
            '''

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('emmaliu_gaotian_xli33_yuyangl', 'emmaliu_gaotian_xli33_yuyangl')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/emmaliu_gaotian_xli33_yuyangl')  # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/emmaliu_gaotian_xli33_yuyangl')  # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#')  # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/')  # The event log.
        doc.add_namespace('bdp', '')
        this_script = doc.agent('alg:emmaliu_gaotian_xli33_yuyangl#placeClustering',
                                {prov.model.PROV_TYPE: prov.model.PROV['SoftwareAgent'], 'ont:Extension': 'py'})
        resource = doc.entity('dat:emmaliu_gaotian_xli33_yuyangl#tweets',
                              {'prov:label': '311, Service Requests', prov.model.PROV_TYPE: 'ont:DataResource',
                               'ont:Extension': 'json'})
        visualization = doc.activity('log:uuid' + str(uuid.uuid4()), startTime, endTime)
        doc.wasAssociatedWith(visualization, this_script)
        doc.usage(visualization, resource, startTime, None,
                  {prov.model.PROV_TYPE: 'ont:calculation',
                   'ont:Query': ''
                   }
                  )

        repo.logout()

        return doc


visualization.execute()
# doc = visualization.provenance()
# print(doc.get_provn())
# print(json.dumps(json.loads(doc.serialize()), indent=4))

## eof
