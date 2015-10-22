from yahoo_finance import Share
from datetime import datetime, timedelta
import pytz

def StockIR(timeD, timeM, timeY, name="GOOG"):  # @DontTrace
    '''
    In oder to calculated the day before and after we first want to know if the stocks are open at the moment.
    Night: the time between 2 trade-day. So the time between friday closing time and moonday opening time is a night of more than 50 hours.
    If it is night yesterday is the night before yesterday night is the day before.    
    '''
    s = "-";
    '''
    To check wheter to the stocks are closed because the trade allready happend or is gone to happen we have the openingtime.
    The openingtime is choosen over the closing time because the closing time is more flexible.
    ALL TIMES ARE IN TIME ZONE Eastern Time (ET)
    '''
    
    def edt_to_utc(date, mask='%m/%d/%Y %I:%M%p'):
        utc = pytz.utc
        eastern = pytz.timezone('US/Eastern')
        date_ = datetime.strptime(date, mask)
        date_eastern = eastern.localize(date_, is_dst=None)
        date_utc = date_eastern.astimezone(utc)
        return date_utc

    def stock_open(YYYYmmdd, stock):
        price = stock.get_historical(YYYYmmdd, YYYYmmdd);
        if    price.__str__()=='[]':
            return(False)
        else:
            return(True)
    
                
    def next_day_open(_timeD, _timeM, _timeY, name):
        stock      = Share(name);
        mask       ='%Y-%m-%d';
        dateUTC    = edt_to_utc(s.join((str(_timeY),str(_timeM),str(_timeD))), mask);
        oneDay     = timedelta(days=1);
        
        if stock_open(s.join((str(_timeY),str(_timeM),str(_timeD))), stock):
            doubleDay = False
        else:
            doubleDay = True
        dateUTC    = dateUTC + oneDay;
        
        
        latestDate = stock.get_trade_datetime();
        latestDate = latestDate[0:10];
        
        
        while True:
            YYYYmmdd = dateUTC.strftime(mask);
            
            # If the given date is later than the latest trading date, then return the latest trading date
            if YYYYmmdd>latestDate:
                return(latestDate)
                break
        
            if stock_open(YYYYmmdd, stock):
                if doubleDay:
                    doubleDay = False
                    dateUTC    = dateUTC + oneDay;
                else:
                    return(YYYYmmdd)
                    break
            else:
                dateUTC    = dateUTC + oneDay;
    def last_day_open(_timeD, _timeM, _timeY, name):
        mask       ='%Y-%m-%d';
        dateUTC    = edt_to_utc(s.join((str(_timeY),str(_timeM),str(_timeD))), mask);
        oneDay     = timedelta(days=1);
        dateUTC    = dateUTC - oneDay;
        
        stock      = Share(name);
        latestDate = stock.get_trade_datetime();
        latestDate = latestDate[0:10];
        
        while True:
            YYYYmmdd = dateUTC.strftime(mask);
            
            # If the given date is later than the latest trading date, then return the latest trading date
            if YYYYmmdd>latestDate:
                return(latestDate)
                break
        
            if stock_open(YYYYmmdd, stock):
                return(YYYYmmdd)
                break
            else:
                dateUTC    = dateUTC - oneDay;
                

    stoke = Share(name) #open the share-data of yahoo
    time = next_day_open(timeD,timeM,timeY, name);
    time2= last_day_open(timeD,timeM,timeY, name);
    #Now we take the stoke date from the past year. 0 will be tomorrow, the last one the day a year back.
    stokeHis = stoke.get_historical(time2,time);
    #the stoke prices are ordert from newest to oldest so position 2 holds the data of yesterday 0 of tomorrow
    #the yeN is the night between today and yesterday.

    indexDayYe = float(stokeHis[2]['Close'])-float(stokeHis[2]['Open']);
    indexDayYeN = float(stokeHis[1]['Open'])-float(stokeHis[2]['Close']);
    indexDayTo = float(stokeHis[1]['Close'])-float(stokeHis[1]['Open']);
    indexDayMoN = float(stokeHis[0]['Open'])-float(stokeHis[1]['Close']);
    indexDayMo = float(stokeHis[0]['Close'])-float(stokeHis[0]['Open']);
    
    output = {"yesterday": (indexDayYe/float(stokeHis[2]['Open'])),"lastNight": (indexDayYeN/float(stokeHis[2]['Close'])),"today": (indexDayTo/float(stokeHis[1]['Open'])),"nextNight": (indexDayMoN/float(stokeHis[0]['Close'])),"tomorrow": (indexDayMo/float(stokeHis[0]['Open']))}
    del stokeHis[:];
    return[output]
