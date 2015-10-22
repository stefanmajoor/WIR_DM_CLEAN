import stefan_mathilde.Crawler.Article as A1
import roy_johan_1.Article as A2
import roy_johan_1.Features as f
import tom_kaitao.trained_function as tf
import roy_johan_genetic.evaluation as e


a = A1.Article("test_source", "http://example.org/", "Title", "2012-01-01", "Stefan", "test but", 1)

b = A2(1, a.sourceId, a.title, a.author, a.date, a.html, a.companies, '')



a = tf.featureSelection(b)

#We need an actual featurse object here
features = f()
features.text = ['Even', 'stefan', 'but', 'test a b c']
features.length = 100
features.sentiment = (1,1)
print e.evaluate(features)
