--Note, the paymentinterval field must have a valid postgres interval.
--You can add more, but I don't think we need any more than those below.
INSERT INTO loanpaymentfrequencies
  (frequencyID, timesperyear, paymentinterval, description)
VALUES
  ('M', 12, '1 month', 'Monthly'),
  ('W', 52, '1 week' , 'Weekly'),
  ('Q',  4, '3 month', 'Quarterly'),
  ('F', 26, '2 week' , 'Fortnightly');