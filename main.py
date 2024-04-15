import script
from datetime import datetime

dt = datetime.now()
if dt.isoweekday() > 5:
    print("It's the weekend, no trading today")
else:
    script.initAcc()
    script.margin()
    script.main()
    script.TableValue()
