from flask import escape
import functions_framework
from genbluntfacts.gen_blunt_facts import gen_blunt_facts 

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'strain' in request_json:
        strain = request_json['strain']
    elif request_args and 'strain' in request_args:
        strain = request_args['strain']
    else:
        return 'Invalid strain'
    return gen_blunt_facts(escape(strain))