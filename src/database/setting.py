from database.model import Metric

DEFAULT_METRICS = [
    Metric(name='avg', description='среднее время обработки запроса'),
    Metric(name='std.dev', description='срендеквадратичное отклоние времени обработки запроса'),
    Metric(name='per90', description='90 персентиль времени обработки запроса'),
    Metric(name='per95', description='95 персентиль времени обработки запроса'),
    Metric(name='rps', description='количество запросов в секунду'),
    Metric(name='rpm', description='количество запросов в минуту'),
    Metric(name='rph', description='количество запросов в час')
]


