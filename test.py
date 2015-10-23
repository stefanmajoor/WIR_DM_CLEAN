import stefan_mathilde.Crawler.Article as A1
import roy_johan_1.Article as A2
import roy_johan_1.Features as f
import roy_johan_1.featurextractor as extraction
import tom_kaitao.trained_function as tf
import roy_johan_genetic.evaluation as e

a = A1.Article("test_source", "http://example.org/", "Title", "2012-01-01", "Stefan", "test but", 1)

b = A2(1, a.sourceId, a.title, a.author, a.date, a.html, a.companies, '')

extractor = extraction.FeatureExtractor()
'''
For Tom (This part):
use extractor.get_features(b) to get a features object
throw out all bad words from the features.text array
pass that into e.evaluate
For Tom(Training the genetic algorithm):
Goto roy_johan_genetic\training folder in evaluation.py
on line 25 the label should be taken from the database and the limit should be changed to something higher
Then run evaluation.py
Copy results.db to the roy_johan_genetic folder
'''
features = extractor.get_features(b)
print e.evaluate(features)
