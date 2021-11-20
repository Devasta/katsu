import flask_wtf
import wtforms


class LoanSearchForm(flask_wtf.FlaskForm):
    class Meta:
        csrf = False

    memberid = wtforms.IntegerField('memberid',
                                    validators=[wtforms.validators.Optional()
                                                ])
    loanid = wtforms.IntegerField('loanid',
                                     validators=[wtforms.validators.Optional()
                                                 ])
    status = wtforms.StringField('status',
                                 validators=[wtforms.validators.Optional(),
                                             wtforms.validators.Length(max=1)])
    paymentmethod = wtforms.SelectField('paymentmethod',
                                           choices=[('DD', 'SEPA Payment'), ('CA', 'Cash Payment')],
                                           validators=[wtforms.validators.Optional()
                                                   ])


class MainLoanForm(flask_wtf.FlaskForm):
    memberid = wtforms.HiddenField('memberid',
                                    validators=[wtforms.validators.Optional()
                                                ])
    amount = wtforms.DecimalField('amount',
                                    places=2,
                                    validators=[wtforms.validators.Optional(),
                                                wtforms.validators.number_range(min=0, message='Loan amount must be greater than zero.')
                                                ])
    purpose = wtforms.StringField('purpose',
                                    validators=[wtforms.validators.Optional(),
                                                wtforms.validators.Length(max=100)
                                                ])
    statusid = wtforms.StringField('statusid',
                                       validators=[wtforms.validators.Optional(),
                                                   wtforms.validators.Length(max=1)
                                                   ])
    interestrate = wtforms.DecimalField('interestrate',
                                       validators=[wtforms.validators.Optional(),
                                                   wtforms.validators.number_range(min=0.01,
                                                                                   message='Interest amount must be positive.')
                                                   ])
    paymentmethodid = wtforms.SelectField('paymentmethodid',
                                           choices=[('DD', 'SEPA Payment'), ('CA', 'Cash Payment')],
                                           validators=[wtforms.validators.Optional()
                                                   ])
    paymentamount = wtforms.DecimalField('paymentamount',
                                       validators=[wtforms.validators.Optional()
                                                   ])
    nextpaymentdate = wtforms.DateField('nextpaymentdate',
                                       validators=[wtforms.validators.Optional()
                                                   ])
    paymentfrequency = wtforms.SelectField('paymentfrequency',
                                           choices=[('M', 'M'), ('W', 'W'), ('Q', 'Q'), ('F', 'F')],
                                           validators=[wtforms.validators.Optional()
                                                   ])
    closecode = wtforms.StringField('closecode',
                                       validators=[wtforms.validators.Optional()
                                                   ])

    savingsaccountid = wtforms.IntegerField('ssvingsaccountid',
                                     validators=[wtforms.validators.Optional()
                                                 ])

    def validate(self, method='NEW'):
        """
            We use the RFC-7396 JSON Merge Patch for the API, which may not necessarily receive all fields.
            We want to validate any fields we can, but must have additional checks for the mandatory fields, to ensure
            that there  are no attempts to delete them.

            It might be easier to have separate form classes for both methods. Feel free to change.
        """
        flask_wtf.FlaskForm.validate(self)
        if method == 'NEW':
            if self.memberid.data is None:
                self.memberid.errors.append("memberid cannot be null or empty.")
            if self.amount.data is None:
                self.amount.errors.append("loan amount cannot be null or empty.")
            if self.purpose.data is None:
                self.purpose.errors.append("loan purpose cannot be null or empty.")
            if self.statusid.data is not None and self.loanstatusid.data != 'P':
                self.statusid.errors.append("loan statusid must be set to 'P' for new loans. It will be automatically filled.")
        elif method == 'UPDATE':
            if 'memberid' in self.patch_data and self.memberid.data is None:
                self.memberid.errors.append("memberid cannot be null or empty. Don't send if not changing.")
            if 'amount' in self.patch_data and self.amount.data is None:
                self.amount.errors.append("loan amount cannot be null or empty. Don't send if not changing.")
            if 'purpose' in self.patch_data and self.purpose.data is None:
                self.purpose.errors.append("loan purpose cannot be null or empty. Don't send if not changing.")
            if 'statusid' in self.patch_data and self.statusid.data is None:
                self.statusid.errors.append("loan statusid cannot be null or empty. Don't send if not changing.")
            if 'statusid' in self.patch_data and self.statusid.data == 'C' and 'closecode' not in self.patch_data:
                self.statusid.errors.append("cannot close loan without a reason provided.")
            if 'statusid' in self.patch_data and self.statusid.data != 'C' and 'closecode' in self.patch_data:
                self.statusid.errors.append("close reason provided but loan not closing.")

        if len(self.errors) > 0:
            return False
        else:
            return True
