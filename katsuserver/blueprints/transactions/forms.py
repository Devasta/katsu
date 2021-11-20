import flask_wtf
import wtforms

"""
    http://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields

    We will always be loading a transaction with multiple child records, so need to validate all at once.

    REST be damned. 
"""


class _TransactionDetailForm(wtforms.Form):  # Inner form must use wtforms.Form, if you don't you get CSRF errors.
    accountid = wtforms.IntegerField('accountid',
                                     validators=[wtforms.validators.InputRequired()
                                                 ])
    debit = wtforms.SelectField('Entry Type',
                                choices=[('', ''), ('Debit', 'Debit'), ('Credit', 'Credit')],
                                validators=[wtforms.validators.InputRequired()
                                            ])
    amount = wtforms.DecimalField('amount',
                                  validators=[wtforms.validators.InputRequired(),
                                              wtforms.validators.number_range(min=0,
                                                                              message='Transaction amount must be greater than zero.')
                                              ])


class TransactionMainForm(flask_wtf.FlaskForm):
    description = wtforms.StringField('description',
                                      validators=[wtforms.validators.InputRequired(),
                                                  wtforms.validators.Length(max=200)
                                                  ])
    entries = wtforms.FieldList(wtforms.FormField(_TransactionDetailForm), min_entries=2)
    submit = wtforms.SubmitField('')

    def validate(self):

        if not flask_wtf.FlaskForm.validate(self):
            return False
        else:
            #  Note: This check to see if Debits/Credits tally is also carried out in the DB, but should not be removed.
            diff = 0
            for t in self.entries.data:
                if t['debit'] == 'Debit':
                    diff = diff + t['amount']
                else:
                    diff = diff - t['amount']
            if diff == 0:
                return True
            else:
                self.entries.errors.append('Debits and Credits do not tally.')
                return False


class BasicTransactionForm(flask_wtf.FlaskForm):
    accountid = wtforms.IntegerField('accountid',
                                     validators=[wtforms.validators.InputRequired()
                                                 ])
    description = wtforms.StringField('description',
                                      validators=[wtforms.validators.InputRequired(),
                                                  wtforms.validators.Length(max=200)
                                                  ])
    amount = wtforms.DecimalField('amount',
                                  validators=[wtforms.validators.InputRequired(),
                                              ])


class TransactionSearchForm(flask_wtf.FlaskForm):
    class Meta:
        csrf = False

    transactionid = wtforms.IntegerField('transactionid',
                                         validators=[wtforms.validators.Optional()
                                                     ])
    accountid = wtforms.IntegerField('accountid',
                                     validators=[wtforms.validators.Optional()
                                                 ])
