from io import BytesIO
from tokenize import tokenize, NUMBER, STRING, NAME, ENCODING, ENDMARKER, \
    NEWLINE

import json
import logging
import urllib.request

logging.basicConfig(level='ERROR')
logger = logging.getLogger('prom-metric-check')


class Token:

    def __init__(self, no, toknum, tokval):
        self.no = no
        self.toknum = toknum
        self.tokval = tokval

    def __repr__(self):
        return 'Token({no}, {toknum}, "{tokval}")'.format(
            no=self.no, toknum=self.toknum, tokval=self.tokval)

    def is_name(self):
        return self.toknum == NAME

    def is_string(self):
        return self.toknum == STRING

    def is_number(self):
        return self.toknum == NUMBER

    def is_operation(self):
        return self.tokval in [
            "+", "-", "*", "/", "%", "^",
            "==", "!=", ">", "<", ">=", "<="]

    def is_colon(self):
        return self.tokval == ":"

    def is_leftbracket(self):
        return self.tokval == "("

    def is_rightbracket(self):
        return self.tokval == ")"

    def is_leftcurltbracket(self):
        return self.tokval == "{"

    def is_rightcurltbracket(self):
        return self.tokval == "}"

    def is_leftsquarebracket(self):
        return self.tokval == "["

    def is_rightsquarebracket(self):
        return self.tokval == "]"

    def is_unnecessary(self):
        return self.tokval in [
            'by', 'without',
            'group_left', 'group_right',
            'and', 'or', 'unless', 'ignoring', 'on',
            'count_values', 'quantile', 'topk', 'bottomk']

    def get_next(self, heap):
        try:
            return heap[self.no + 1]
        except IndexError:
            return None

    def get_prev(self, heap):
        try:
            return heap[self.no - 1]
        except IndexError:
            return None


def tokenize_string(query):
    result, x = [], 0
    g = tokenize(BytesIO(query.encode('utf-8')).readline)
    for toknum, tokval, _a, _b, _c in g:
        if toknum not in [ENCODING, ENDMARKER, NEWLINE]:
            result.append(Token(x, toknum, tokval))
            x += 1
    return result


def find_metrics(tokenized_query):
    skip, temp, heap, metrics = False, None, [], []
    for token in tokenized_query:
        if skip == '(' and token.is_rightbracket():
            skip = False
            if heap:
                if heap[-1].is_leftbracket():
                    heap.pop()
                    if heap and heap[-1].is_name():
                        heap.pop()
                if temp:
                    metrics.append(temp)
                    temp = None
        elif skip in ['{', '['] and (
                token.is_rightcurltbracket() or token.is_rightsquarebracket()):
            skip = False
            if temp:
                metrics.append(temp)
                temp = None
        elif skip:
            continue
        elif token.is_leftbracket():
            heap.append(token)
        elif token.is_leftcurltbracket() or token.is_leftsquarebracket():
            skip = token.tokval
        elif token.is_colon():
            if temp:
                temp += token.tokval
            else:
                temp = token.tokval
        elif token.is_name():
            if token.is_unnecessary():
                if token.get_next(tokenized_query).is_leftbracket():
                    skip = token.get_next(tokenized_query).tokval
            elif token.get_next(tokenized_query):
                if token.get_next(tokenized_query).is_leftbracket():
                    heap.append(token)
                elif token.get_next(tokenized_query).is_leftcurltbracket() or \
                        token.get_next(
                            tokenized_query).is_leftsquarebracket() or \
                        token.get_next(
                            tokenized_query).is_operation() or \
                        token.get_next(
                            tokenized_query).is_rightbracket():
                    if temp:
                        temp += token.tokval
                        metrics.append(temp)
                        temp = None
                    else:
                        metrics.append(token.tokval)
                elif token.get_next(tokenized_query).is_colon():
                    if not temp:
                        temp = token.tokval
                    else:
                        temp += token.tokval
            elif not token.get_next(tokenized_query):
                if temp:
                    temp += token.tokval
                    metrics.append(temp)
                    temp = None
                else:
                    metrics.append(token.tokval)
    return list(set(metrics))


class Response:
    def __init__(self, response=None):
        self.response = response
        self.content = self.response.read()

    @property
    def ok(self):
        return 200 <= self.response.getcode() <= 299

    @property
    def text(self):
        return self.content.decode('utf-8')

    def json(self):
        if self.text:
            return json.loads(self.text)
        return {}


def request_get(url=None, token=None):
    request = urllib.request.Request(url)
    if token:
        request.add_header(
            "Authorization", "Bearer {token}".format(token=token))
    try:
        conn = urllib.request.urlopen(request, timeout=5)
    except urllib.error.URLError as e:
        print('{url}: {error}'.format(url=url, error=e.reason))
        exit(1)
    return Response(conn)


def check_exist_metrics(except_metrics=None, url=None):
    logger.info("Except metrics: {metrics}".format(
        metrics=', '.join(except_metrics)))
    exist_metrics = request_get(
        '{url}/api/v1/label/__name__/values'.format(url=url))
    if exist_metrics.ok:
        data = list(set(exist_metrics.json()['data']))
        logger.info("Exist metrics: {metrics}".format(metrics=', '.join(data)))
        difference = set(except_metrics).difference(
            set(exist_metrics.json()['data']))
        return list(difference)
    raise ValueError


def get_recursively(search_dict, field):
    """
    Takes a dict with nested lists and dicts, and searches all dicts
    for a key of the field provided.
    """
    fields_found = []

    for key, value in search_dict.items():

        if key == field:
            fields_found.append(value)

        elif isinstance(value, dict):
            results = get_recursively(value, field)
            for result in results:
                fields_found.append(result)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = get_recursively(item, field)
                    for another_result in more_results:
                        fields_found.append(another_result)

    return fields_found


def get_all_metrics(dashboards=None):
    expression, metrics = [], []
    for configration in dashboards:
        expression.extend(get_recursively(configration, 'expr'))
    for expr in expression:
        metrics.extend(find_metrics(tokenized_query=tokenize_string(expr)))
    return list(set(metrics))


def load_dashboard(url=None, key=None):
    dashboards, dashboards_uid = [], []
    search_dashboard = request_get(
        '{url}/api/search'.format(url=url), token=key)
    if search_dashboard.ok:
        dashboards_uid = [dash.get('uid') for dash in search_dashboard.json()]
    for name in dashboards_uid:
        dashboard = request_get('{url}/api/dashboards/uid/{name}'.format(
            url=url, name=name), token=key)
        if dashboard.ok:
            dashboards.append(dashboard.json().get('dashboard', {}))
    return dashboards
