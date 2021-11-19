import flask

codelinks = flask.Blueprint('codelinks', __name__, url_prefix='/codelinks')
from . import views

'''
This blueprint handles some of the application configuration values. Everything is broker into two distinct groups

    CONFIGS - These are single values the application needs, a register of magic values!
                Example: the configvalue DOCUMENT_ARCHIVE specifies the location that any submitted documents the
                the members posted in should be stored.

    CODELINKS - These are used by financial transaction entries, so the user does not need to specify both sides
                of a transaction.
                Example : the codelink DAILY_LOAN_INTEREST is used to point to the account used to track revenues
                from the interest applied to loans.

    All the view, insert, update views and functions for configs and codelinks are mostly the same, only real difference
                is the configvalue is a string, and the codelink is an integer.

    This blueprint handles the codelinks, you'll find the configs are almost a copy/paste.

'''
