'''
Created on 12 juin 2012

@author: maxisoft
'''

import urllib2
import os
import sys

import vote


import config as cfg

from HttpProxy import ProxyRot, getMyIp
from ThreadPool import timeout

from MyUrlOpener import updateUrlOp

#Global

config = cfg.ProxyConfig()
proxys = ProxyRot()
    

def voteall():
    
    #-------------------
    def oneVote(user, passw):
        ret = None
        configT = cfg.ProxyConfig()
        vote.config = configT
        try:
            print getMyIp(vote.urlOpener)
            print 'vote start'

            
            ret = vote.main(user, passw)
            
            print 'vote end'
            
        except Exception as inst:
            print 'e', inst 
            return inst
        
        configT.writeTime(user=user)
        return ret
    #-------------------
    print len(config.getReadyacc())
    for accinfo in config.getReadyacc():
        print accinfo['user']
        time_out = 5 # 5 chance
        while time_out:
            print time_out
            try:
                updateUrlOp(proxys())
                res = timeout(oneVote, kwargs=accinfo, timeout_duration=100)
                if res == 1:
                    time_out = 0
                    print 'ok'
                elif str(res).find('Proxy')!=-1:
                    import LogIt
                    log = LogIt.logit()
                    log.log('Ce proxy semble ne semble pas fonctionel : %s' % (proxys.getCurrentProxy()))
                    raise(Exception('erreur proxy'))
                else:
                    raise(Exception(str(res)))
            except:
                print 'erreur'
                time_out -= 1
        
        
        #MyUrlOpener.updateUrlOp(proxys())
        #updateVoteUrlO(proxys())
        
        
        
        
        
        
def main():
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
    except:
        pass
    proxys.getProxysFromFile(force=1)
    voteall()
    


if __name__ == '__main__':
    main()
#    except Exception as inst:
#            print inst
#    finally:
#        raw_input('\n\n>>> Tapez entre pour continue')
    
    pass
