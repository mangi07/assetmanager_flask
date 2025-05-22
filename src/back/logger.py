import pprint
import inspect, logging, datetime

def log(message):
    pp = pprint.PrettyPrinter(indent=2)

    #pp.pprint(message)

    # Get the previous frame in the stack, otherwise it would
    # be this function!!!
    func = inspect.currentframe().f_back.f_code
    
    with open("log.txt", "a") as f:
        trace = "Trace: %s in %s:%i" % (
           func.co_name, 
           func.co_filename, 
           func.co_firstlineno
        )
        message = pp.pformat(message)
        s = f"\n\n<<<{datetime.datetime.now()}\n" + "**" + trace + "\n\n" + message +  "\n>>>\n"
        f.write(s)

