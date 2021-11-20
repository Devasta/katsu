import flask_wtf
import wtforms


class membersearchform(flask_wtf.FlaskForm):
    class Meta:
        csrf = False

    memberid = wtforms.IntegerField('memberid',
                                validators=[wtforms.validators.Optional()
                                            ])
    surname = wtforms.StringField('surname',
                                validators=[wtforms.validators.Optional(),
                                            wtforms.validators.Length(max=35)
                                            ])
    addressline1 = wtforms.StringField('addressline1',
                                validators=[wtforms.validators.Optional(),
                                            wtforms.validators.Length(max=50)
                                            ])
    county = wtforms.StringField('county',
                                validators=[wtforms.validators.Optional(),
                                            wtforms.validators.Length(max=50)
                                            ])
    postcode = wtforms.StringField('postcode',
                                validators=[wtforms.validators.Optional(),
                                            wtforms.validators.Regexp('^[A-Za-z0-9]{3}[ ]{1}[A-Za-z0-9]{4}$')
                                            ])


class memberdetailsform(flask_wtf.FlaskForm):
    title = wtforms.SelectField('title',
                                default='',
                                choices=[('', ''), ('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Ms', 'Ms'), ('Dr', 'Dr'), ('Prof', 'Prof')],
                                validators=[wtforms.validators.Optional(),
                                            wtforms.validators.Length(max=6)
                                            ])
    forename = wtforms.StringField('forename',
                                validators=[wtforms.validators.Optional(),
                                            wtforms.validators.Length(max=35)
                                            ])
    surname = wtforms.StringField('surname',
                                validators=[wtforms.validators.Optional(),
                                            wtforms.validators.Length(max=35)
                                            ])
    companyname = wtforms.StringField('companyname',
                                validators=[wtforms.validators.Optional(),
                                            wtforms.validators.Length(max=100)
                                            ])
    addressline1 = wtforms.StringField('addressline1',
                                validators=[wtforms.validators.InputRequired(),
                                            wtforms.validators.Length(min=1, max=50)
                                            ])
    addressline2 = wtforms.StringField('addressline2',
                                validators=[wtforms.validators.Optional(),
                                            wtforms.validators.Length(max=50)
                                            ])
    city = wtforms.StringField('city',
                                validators=[wtforms.validators.Optional(),
                                            wtforms.validators.Length(max=50)
                                            ])
    county = wtforms.StringField('county',
                                validators=[wtforms.validators.InputRequired(),
                                            wtforms.validators.Length(min=1, max=50)
                                            ])
    country = wtforms.StringField('country',
                                validators=[wtforms.validators.Optional(),
                                            wtforms.validators.Length(max=50)
                                            ])
    postcode = wtforms.StringField('postcode',
                                validators=[wtforms.validators.InputRequired(),
                                            wtforms.validators.Regexp('^[A-Za-z0-9]{3}[ ]{1}[A-Za-z0-9]{4}$')
                                            ])
    homephone = wtforms.StringField('homephone',
                                validators=[wtforms.validators.Optional(),
                                            wtforms.validators.Length(max=20)
                                            ])
    mobilephone = wtforms.StringField('mobilephone',
                                validators=[wtforms.validators.Optional(),
                                            wtforms.validators.Length(max=20)
                                            ])
    dateofbirth = wtforms.DateField('dateofbirth',
                                format='%Y-%m-%d',
                                validators=[wtforms.validators.Optional(),
                                            ])
    gender = wtforms.SelectField('gender',
                                default='',
                                choices=[('', ''), ('M', 'M'), ('F', 'F')],
                                validators=[wtforms.validators.Optional()
                                            ])
    submit = wtforms.SubmitField('')

    def validate(self):
        if flask_wtf.FlaskForm.validate(self):
            if self.companyname.data is None and self.surname.data is None:
                self.surname.errors.append('Must provider either member name or company name.')
                return False
            else:
                return True
        else:
            return False
