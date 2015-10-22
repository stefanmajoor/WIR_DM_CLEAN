import Mapper


'''
The real evaluator for the
'''
class Evaluator():

    def __init__(self):
        self.baseMapper = Mapper.Mapper()
        self.counter = [[0, 0], [0, 0]]


    '''
    Evaluate our classification algorithm
    '''
    def start(self, evaluator):
        i = 0
        for article in self.baseMapper.getAllArticles():
            i += 1
            print i, "\n";
            
            html = article[6]
            isEconomic = article[7]
            classification = evaluator.evaluate(html)
            #print isEconomic, classification

            if isEconomic != classification:
                print article[3]

            self.counter[isEconomic][classification] += 1

        print self.counter

