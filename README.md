# python-chartmogul
Extremely simple ChatMogul read-only API wrapper

## Example

```python
from chartmogul import ChartMogul
import datetime

token = "your_token"
secret = "your_secret"

mogul = ChartMogul(token, secret)

def first_day_of_month(d):
    return datetime.date(d.year, d.month, 1)

end_date = datetime.date.today()
start_date = first_day_of_month(end_date)
current_mrr = mogul.get_mrr('month', start_date, end_date)

yesterday = end_date - datetime.timedelta(days = 1)
current_all = mogul.get_all('day', yesterday, end_date)
```
